"""
Personal AI Employee Orchestrator

This script serves as the main coordinator for the AI employee,
managing the flow between watchers, Claude Code reasoning,
and action execution via MCP servers.
"""

import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime
import subprocess
import threading
import sys

class PersonalAIEmployeeOrchestrator:
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        self.setup_logging()

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def setup_logging(self):
        """Setup logging for the orchestrator"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('orchestrator.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def update_dashboard(self):
        """Update the dashboard automatically when changes occur"""
        try:
            # Import the update-dashboard skill function
            sys.path.append('.claude/skills/update-dashboard/')
            from skill import run_skill
            result = run_skill()
            self.logger.info(f"Dashboard updated: {result}")
        except ImportError:
            # Alternative: run the skill as a subprocess
            try:
                import subprocess
                result = subprocess.run([sys.executable, '.claude/skills/update-dashboard/skill.py'],
                                      capture_output=True, text=True)
                self.logger.info(f"Dashboard update process completed: {result.returncode}")
                if result.stdout:
                    self.logger.debug(f"Dashboard update output: {result.stdout}")
                if result.stderr:
                    self.logger.error(f"Dashboard update error: {result.stderr}")
            except Exception as e:
                self.logger.error(f"Error updating dashboard: {e}")
        except Exception as e:
            self.logger.error(f"Error in dashboard update: {e}")

    def check_needs_action(self):
        """Check if there are items in the Needs_Action folder"""
        needs_action_dir = Path(self.config['directories']['needs_action'])

        # Ensure the directory exists
        needs_action_dir.mkdir(parents=True, exist_ok=True)

        action_items = list(needs_action_dir.glob('*.md'))

        # Update dashboard if there are changes in the number of pending items
        if hasattr(self, '_previous_pending_count'):
            current_count = len(action_items)
            if current_count != self._previous_pending_count:
                self.logger.info(f"Action items count changed from {self._previous_pending_count} to {current_count}, updating dashboard")
                self.update_dashboard()
        self._previous_pending_count = len(action_items)

        self.logger.info(f"Found {len(action_items)} action items in Needs_Action")
        return action_items

    def process_action_item(self, item_path):
        """Process a single action item using Claude Code"""
        self.logger.info(f"Processing action item: {item_path}")

        # Read the action item content
        with open(item_path, 'r') as f:
            content = f.read()

        # Create a plan based on the item
        plan_content = self.generate_plan(content, item_path)

        # Save the plan
        plan_path = Path(self.config['directories']['plans']) / f"PLAN_{item_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(plan_path, 'w') as f:
            f.write(plan_content)

        self.logger.info(f"Plan created: {plan_path}")

        # Move the original item to Done
        done_dir = Path(self.config['directories']['done'])
        done_path = done_dir / item_path.name
        item_path.rename(done_path)
        self.logger.info(f"Moved to Done: {done_path}")

        # Update the dashboard to reflect the change
        self.update_dashboard()

    def generate_plan(self, content, item_path):
        """Generate a plan using Claude Code logic"""
        # This is a simplified version - in practice, this would call Claude Code
        plan = f"""# Plan for {item_path.stem}

---
created: {datetime.now().isoformat()}
status: pending
---

## Original Request
{content}

## Proposed Actions
- [ ] Analyze the request
- [ ] Determine priority level
- [ ] Plan specific actions
- [ ] Execute or escalate as needed

## Priority
Medium

## Estimated Completion
Within 24 hours
"""
        return plan

    def run(self):
        """Main execution loop"""
        self.logger.info("Starting Personal AI Employee Orchestrator")

        # Initialize the previous pending count
        self._previous_pending_count = 0

        while True:
            try:
                # Check for action items
                action_items = self.check_needs_action()

                if action_items:
                    self.logger.info(f"Found {len(action_items)} items to process")

                    for item in action_items:
                        self.process_action_item(item)

                # Wait before checking again
                time.sleep(30)  # Check every 30 seconds

            except KeyboardInterrupt:
                self.logger.info("Orchestrator stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in orchestrator: {e}")
                time.sleep(60)  # Wait longer if there's an error

if __name__ == "__main__":
    orchestrator = PersonalAIEmployeeOrchestrator()
    orchestrator.run()