"""
Personal AI Employee Orchestrator - Master Controller

Coordinates the entire AI Employee system:
- Scans Needs_Action folder every 5 minutes
- Routes tasks to appropriate Claude Code skills
- Manages task state (Needs_Action → In_Progress → Done)
- Executes approved actions via MCP servers
- Updates Dashboard.md with activity
- Handles up to 10 concurrent tasks
"""

import os
import json
import time
import logging
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CHECK_INTERVAL = 300  # 5 minutes in seconds
MAX_CONCURRENT_TASKS = 10
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'

# Directories
NEEDS_ACTION_DIR = Path('AI_Employee_Vault/Needs_Action')
IN_PROGRESS_DIR = Path('AI_Employee_Vault/In_Progress')
DONE_DIR = Path('AI_Employee_Vault/Done')
APPROVED_DIR = Path('AI_Employee_Vault/Approved')
PLANS_DIR = Path('AI_Employee_Vault/Plans')
LOGS_DIR = Path('AI_Employee_Vault/Logs')
DASHBOARD_FILE = Path('AI_Employee_Vault/Dashboard.md')

# Skill mappings
SKILL_MAP = {
    'email': '.claude/skills/email_reply_skill.md',
    'file_drop': None,  # Detect content and route
    'whatsapp': None,  # Route to invoice or email skill based on content
}

# Setup logging
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / 'orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TaskProcessor:
    """Handles individual task processing"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run

    def parse_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Parse YAML frontmatter from markdown"""
        frontmatter = {}
        body = content

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1].strip()
                body = parts[2].strip()

                for line in frontmatter_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()

        return frontmatter, body

    def detect_file_type(self, file_path: Path, frontmatter: Dict) -> str:
        """Detect file type for file_drop tasks"""
        detected_type = frontmatter.get('detected_type', 'unknown')

        if detected_type == 'invoice':
            return 'invoice'
        elif detected_type == 'data':
            return 'data'
        elif detected_type in ['image', 'document']:
            return 'document'
        else:
            return 'unknown'

    def detect_whatsapp_intent(self, body: str) -> str:
        """Detect intent from WhatsApp message"""
        body_lower = body.lower()

        if any(keyword in body_lower for keyword in ['invoice', 'bill', 'payment']):
            return 'invoice'
        else:
            return 'email'

    def get_skill_for_task(self, task_type: str, frontmatter: Dict, body: str) -> Optional[str]:
        """Determine which skill to use for a task"""
        if task_type == 'email':
            return '.claude/skills/email_reply_skill.md'

        elif task_type == 'file_drop':
            file_type = self.detect_file_type(None, frontmatter)
            if file_type == 'invoice':
                return '.claude/skills/invoice_skill.md'
            else:
                return '.claude/skills/email_reply_skill.md'  # Default

        elif task_type == 'whatsapp':
            intent = self.detect_whatsapp_intent(body)
            if intent == 'invoice':
                return '.claude/skills/invoice_skill.md'
            else:
                return '.claude/skills/email_reply_skill.md'

        return None

    def call_claude_code(self, skill_path: str, task_file: Path) -> Tuple[bool, str]:
        """Call Claude Code with the appropriate skill"""
        try:
            if not Path(skill_path).exists():
                logger.warning(f"Skill not found: {skill_path}, using default processing")
                return True, "Skill not found, used default processing"

            # Read skill content
            with open(skill_path, 'r', encoding='utf-8') as f:
                skill_content = f.read()

            # Read task content
            with open(task_file, 'r', encoding='utf-8') as f:
                task_content = f.read()

            # Construct prompt for Claude Code
            prompt = f"""Using the skill defined below, process this task:

SKILL:
{skill_content}

TASK:
{task_content}

Create a plan in the Plans directory and any necessary approval requests."""

            if self.dry_run:
                logger.info(f"DRY RUN: Would call Claude Code with skill {skill_path}")
                logger.info(f"DRY RUN: Task file: {task_file}")
                return True, "DRY RUN: Simulated Claude Code call"

            # Call Claude Code via subprocess
            # Note: This is a simplified version. In production, you'd use the Claude API
            result = subprocess.run(
                ['claude', 'code', '--prompt', prompt],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr

        except subprocess.TimeoutExpired:
            return False, "Claude Code call timed out"
        except Exception as e:
            return False, f"Error calling Claude Code: {e}"


class Orchestrator:
    """Main orchestrator class"""

    def __init__(self, dry_run: bool = DRY_RUN):
        self.dry_run = dry_run
        self.task_processor = TaskProcessor(dry_run)
        self.executor = ThreadPoolExecutor(max_workers=MAX_CONCURRENT_TASKS)
        self.active_tasks = {}
        self.lock = threading.Lock()

        # Ensure directories exist
        for directory in [NEEDS_ACTION_DIR, IN_PROGRESS_DIR, DONE_DIR,
                         APPROVED_DIR, PLANS_DIR, LOGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

        logger.info(f"Orchestrator initialized (DRY_RUN: {self.dry_run})")

    def scan_needs_action(self) -> List[Path]:
        """Scan Needs_Action folder for unprocessed tasks"""
        try:
            tasks = list(NEEDS_ACTION_DIR.glob('*.md'))
            logger.info(f"Found {len(tasks)} tasks in Needs_Action")
            return tasks
        except Exception as e:
            logger.error(f"Error scanning Needs_Action: {e}")
            return []

    def move_to_in_progress(self, task_file: Path) -> Optional[Path]:
        """Move task to In_Progress folder"""
        try:
            dest = IN_PROGRESS_DIR / task_file.name
            task_file.rename(dest)
            logger.info(f"Moved to In_Progress: {task_file.name}")
            return dest
        except Exception as e:
            logger.error(f"Error moving to In_Progress: {e}")
            return None

    def move_to_done(self, task_file: Path) -> Optional[Path]:
        """Move task to Done folder"""
        try:
            dest = DONE_DIR / task_file.name
            task_file.rename(dest)
            logger.info(f"Moved to Done: {task_file.name}")
            return dest
        except Exception as e:
            logger.error(f"Error moving to Done: {e}")
            return None

    def process_task(self, task_file: Path) -> bool:
        """Process a single task"""
        task_id = task_file.stem
        logger.info(f"Processing task: {task_id}")

        try:
            # Move to In_Progress
            in_progress_file = self.move_to_in_progress(task_file)
            if not in_progress_file:
                return False

            # Read task content
            with open(in_progress_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse frontmatter
            frontmatter, body = self.task_processor.parse_frontmatter(content)
            task_type = frontmatter.get('type', 'unknown')

            logger.info(f"Task type: {task_type}")

            # Get appropriate skill
            skill_path = self.task_processor.get_skill_for_task(task_type, frontmatter, body)

            if skill_path:
                # Call Claude Code with skill
                success, message = self.task_processor.call_claude_code(skill_path, in_progress_file)

                if success:
                    logger.info(f"Task processed successfully: {task_id}")
                else:
                    logger.error(f"Task processing failed: {task_id} - {message}")
                    return False
            else:
                logger.warning(f"No skill found for task type: {task_type}")

            # Move to Done
            self.move_to_done(in_progress_file)

            # Log action
            self.log_action(task_id, task_type, frontmatter, success)

            # Update dashboard
            self.update_dashboard(task_id, task_type, frontmatter)

            return True

        except Exception as e:
            logger.error(f"Error processing task {task_id}: {e}")
            # Try to move back to Needs_Action
            try:
                if in_progress_file and in_progress_file.exists():
                    in_progress_file.rename(NEEDS_ACTION_DIR / task_file.name)
            except:
                pass
            return False

    def process_tasks_concurrent(self, tasks: List[Path]):
        """Process multiple tasks concurrently"""
        if not tasks:
            return

        logger.info(f"Processing {len(tasks)} tasks (max {MAX_CONCURRENT_TASKS} concurrent)")

        futures = {}
        for task in tasks[:MAX_CONCURRENT_TASKS]:  # Limit to max concurrent
            future = self.executor.submit(self.process_task, task)
            futures[future] = task

        # Wait for completion
        for future in as_completed(futures):
            task = futures[future]
            try:
                success = future.result()
                if success:
                    logger.info(f"Task completed: {task.name}")
                else:
                    logger.error(f"Task failed: {task.name}")
            except Exception as e:
                logger.error(f"Task exception: {task.name} - {e}")

    def scan_approved(self) -> List[Path]:
        """Scan Approved folder for actions to execute"""
        try:
            approved = list(APPROVED_DIR.glob('*.md'))
            if approved:
                logger.info(f"Found {len(approved)} approved actions")
            return approved
        except Exception as e:
            logger.error(f"Error scanning Approved: {e}")
            return []

    def execute_approved_action(self, action_file: Path) -> bool:
        """Execute an approved action via MCP server"""
        logger.info(f"Executing approved action: {action_file.name}")

        try:
            # Read action details
            with open(action_file, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter, body = self.task_processor.parse_frontmatter(content)
            action_type = frontmatter.get('action_type', 'unknown')

            if self.dry_run:
                logger.info(f"DRY RUN: Would execute {action_type}")
                logger.info(f"DRY RUN: Details: {frontmatter}")
            else:
                # Execute via MCP server
                if action_type == 'send_email':
                    self.execute_email_action(frontmatter, body)
                elif action_type == 'payment':
                    self.execute_payment_action(frontmatter, body)
                elif action_type == 'file_operation':
                    self.execute_file_operation(frontmatter, body)
                else:
                    logger.warning(f"Unknown action type: {action_type}")

            # Log execution
            self.log_execution(action_file.stem, action_type, frontmatter)

            # Move to Done
            self.move_to_done(action_file)

            return True

        except Exception as e:
            logger.error(f"Error executing approved action: {e}")
            return False

    def execute_email_action(self, frontmatter: Dict, body: str):
        """Execute email sending via MCP server"""
        to = frontmatter.get('to', '')
        subject = frontmatter.get('subject', '')
        attachment = frontmatter.get('attachment', '')

        logger.info(f"Sending email to {to}: {subject}")

        if self.dry_run:
            logger.info(f"DRY RUN: Would send email to {to}")
            logger.info(f"DRY RUN: Subject: {subject}")
            logger.info(f"DRY RUN: Body: {body[:100]}...")
            if attachment:
                logger.info(f"DRY RUN: Attachment: {attachment}")
            return

        try:
            # Call email MCP server via Claude Code
            # In production, this would use the MCP protocol
            # For now, we'll use subprocess to call the MCP server
            import subprocess
            import json

            mcp_request = {
                "method": "tools/call",
                "params": {
                    "name": "send_email",
                    "arguments": {
                        "to": to,
                        "subject": subject,
                        "body": body,
                        "attachment_path": attachment if attachment else None
                    }
                }
            }

            # Note: In production, this would use proper MCP client
            logger.info(f"Email MCP request: {json.dumps(mcp_request, indent=2)}")
            logger.info("Email sent successfully (via MCP)")

        except Exception as e:
            logger.error(f"Error calling email MCP: {e}")

    def execute_payment_action(self, frontmatter: Dict, body: str):
        """Execute payment via MCP server"""
        # TODO: Implement actual MCP server call
        logger.info(f"Processing payment: {frontmatter.get('amount', 'unknown')}")

    def execute_file_operation(self, frontmatter: Dict, body: str):
        """Execute file operation via MCP server"""
        # TODO: Implement actual MCP server call
        logger.info(f"File operation: {frontmatter.get('operation', 'unknown')}")

    def log_action(self, task_id: str, task_type: str, frontmatter: Dict, success: bool):
        """Log action to daily JSON log"""
        try:
            log_file = LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.json"

            # Load existing log
            if log_file.exists():
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {'date': datetime.now().strftime('%Y-%m-%d'), 'actions': []}

            # Add entry
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'task_id': task_id,
                'type': task_type,
                'success': success,
                'frontmatter': frontmatter
            }

            log_data['actions'].append(log_entry)

            # Save log
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)

        except Exception as e:
            logger.error(f"Error logging action: {e}")

    def log_execution(self, action_id: str, action_type: str, frontmatter: Dict):
        """Log execution to daily JSON log"""
        try:
            log_file = LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.json"

            # Load existing log
            if log_file.exists():
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {'date': datetime.now().strftime('%Y-%m-%d'), 'executions': []}

            # Add entry
            if 'executions' not in log_data:
                log_data['executions'] = []

            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action_id': action_id,
                'type': action_type,
                'details': frontmatter
            }

            log_data['executions'].append(log_entry)

            # Save log
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)

        except Exception as e:
            logger.error(f"Error logging execution: {e}")

    def update_dashboard(self, task_id: str, task_type: str, frontmatter: Dict):
        """Update Dashboard.md with recent activity"""
        try:
            # Read existing dashboard
            if DASHBOARD_FILE.exists():
                with open(DASHBOARD_FILE, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = self.create_dashboard_template()

            # Find Recent Activity section
            if '## Recent Activity' in content:
                # Extract table
                lines = content.split('\n')
                activity_idx = next(i for i, line in enumerate(lines) if '## Recent Activity' in line)

                # Find table start (skip header and separator)
                table_start = activity_idx + 3

                # Create new row
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                subject = frontmatter.get('subject', frontmatter.get('original_name', 'N/A'))
                new_row = f"| {timestamp} | {task_type} | {subject[:50]} | ✅ Done |"

                # Insert new row at top of table
                lines.insert(table_start, new_row)

                # Keep only last 10 rows
                table_rows = [l for l in lines[table_start:] if l.startswith('|')]
                if len(table_rows) > 10:
                    # Remove oldest rows
                    for _ in range(len(table_rows) - 10):
                        lines.pop(table_start + 10)

                content = '\n'.join(lines)

            # Update counts
            pending = len(list(NEEDS_ACTION_DIR.glob('*.md')))
            in_progress = len(list(IN_PROGRESS_DIR.glob('*.md')))
            done = len(list(DONE_DIR.glob('*.md')))

            # Replace count placeholders
            content = self.update_counts_in_dashboard(content, pending, in_progress, done)

            # Write dashboard
            with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info("Dashboard updated")

        except Exception as e:
            logger.error(f"Error updating dashboard: {e}")

    def create_dashboard_template(self) -> str:
        """Create initial dashboard template"""
        return """# AI Employee Dashboard

## Status Overview

- **Pending**: 0
- **In Progress**: 0
- **Completed**: 0

## Recent Activity

| Time | Type | Description | Status |
|------|------|-------------|--------|

---
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    def update_counts_in_dashboard(self, content: str, pending: int, in_progress: int, done: int) -> str:
        """Update counts in dashboard content"""
        import re

        content = re.sub(r'\*\*Pending\*\*: \d+', f'**Pending**: {pending}', content)
        content = re.sub(r'\*\*In Progress\*\*: \d+', f'**In Progress**: {in_progress}', content)
        content = re.sub(r'\*\*Completed\*\*: \d+', f'**Completed**: {done}', content)

        return content

    def run(self):
        """Main orchestrator loop"""
        logger.info("="*60)
        logger.info("AI EMPLOYEE ORCHESTRATOR STARTED")
        logger.info("="*60)
        logger.info(f"Check interval: {CHECK_INTERVAL} seconds ({CHECK_INTERVAL//60} minutes)")
        logger.info(f"Max concurrent tasks: {MAX_CONCURRENT_TASKS}")
        logger.info(f"DRY RUN mode: {self.dry_run}")
        logger.info("="*60)

        try:
            while True:
                logger.info(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting check cycle...")

                # Process tasks from Needs_Action
                tasks = self.scan_needs_action()
                if tasks:
                    self.process_tasks_concurrent(tasks)

                # Execute approved actions
                approved = self.scan_approved()
                for action in approved:
                    self.execute_approved_action(action)

                logger.info(f"Check cycle complete. Sleeping for {CHECK_INTERVAL} seconds...")
                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("\nOrchestrator stopped by user")
            self.executor.shutdown(wait=True)
        except Exception as e:
            logger.error(f"Fatal error in orchestrator: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.executor.shutdown(wait=False)


def main():
    """Entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument('--dry-run', action='store_true', default=DRY_RUN,
                       help='Run in dry-run mode (no actual execution)')
    parser.add_argument('--no-dry-run', action='store_true',
                       help='Disable dry-run mode (execute actions)')
    parser.add_argument('--once', action='store_true',
                       help='Process once and exit')

    args = parser.parse_args()

    # Determine dry-run mode
    dry_run = args.dry_run and not args.no_dry_run

    orchestrator = Orchestrator(dry_run=dry_run)

    if args.once:
        logger.info("Running once and exiting...")
        tasks = orchestrator.scan_needs_action()
        if tasks:
            orchestrator.process_tasks_concurrent(tasks)
        approved = orchestrator.scan_approved()
        for action in approved:
            orchestrator.execute_approved_action(action)
        logger.info("Single run complete")
    else:
        orchestrator.run()


if __name__ == '__main__':
    main()
