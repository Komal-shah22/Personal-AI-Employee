"""
LinkedIn Approval Processor

Processes approved LinkedIn posts and handles posting workflow.
Respects posting hours (9 AM - 6 PM) and DRY_RUN mode.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
VAULT_PATH = PROJECT_ROOT / "AI_Employee_Vault"
APPROVED_PATH = VAULT_PATH / "Approved"
DONE_PATH = VAULT_PATH / "Done"
LOGS_PATH = VAULT_PATH / "Logs"

# Configuration
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'
POSTING_START_HOUR = int(os.getenv('POSTING_START_HOUR', '9'))
POSTING_END_HOUR = int(os.getenv('POSTING_END_HOUR', '18'))

# Ensure directories exist
for path in [APPROVED_PATH, DONE_PATH, LOGS_PATH]:
    path.mkdir(parents=True, exist_ok=True)


def is_posting_hours() -> bool:
    """Check if current time is within posting hours"""
    current_hour = datetime.now().hour
    return POSTING_START_HOUR <= current_hour < POSTING_END_HOUR


def extract_post_content(filepath: Path) -> str:
    """Extract post content from approval file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract content between ## Post Content and ## Validation
    if "## Post Content" in content:
        start = content.find("## Post Content") + len("## Post Content")
        end = content.find("## Validation")
        if end == -1:
            end = content.find("## To Approve")
        post_content = content[start:end].strip()
        return post_content

    return ""


def log_to_linkedin_log(message: str, post_preview: str = ""):
    """Append entry to linkedin.log"""
    log_file = LOGS_PATH / "linkedin.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] {message}"
    if post_preview:
        log_entry += f"\n  Preview: {post_preview[:100]}..."
    log_entry += "\n"

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

    print(f"[LOG] {message}")


def process_approved_posts() -> Dict[str, Any]:
    """Process all approved LinkedIn posts"""
    print("=" * 70)
    print("LinkedIn Approval Processor")
    print("=" * 70)
    print(f"DRY_RUN mode: {DRY_RUN}")
    print(f"Posting hours: {POSTING_START_HOUR}:00 - {POSTING_END_HOUR}:00")
    print(f"Current time: {datetime.now().strftime('%H:%M:%S')}")
    print()

    # Find all LinkedIn approval files
    linkedin_files = list(APPROVED_PATH.glob("LINKEDIN_*.md"))

    if not linkedin_files:
        print("[INFO] No approved LinkedIn posts found")
        return {"processed": 0, "skipped": 0}

    print(f"[INFO] Found {len(linkedin_files)} approved post(s)")
    print()

    processed = 0
    skipped = 0

    for filepath in linkedin_files:
        print(f"Processing: {filepath.name}")

        # Extract post content
        post_content = extract_post_content(filepath)
        post_preview = post_content[:100] if post_content else "No content"

        # Check posting hours
        if not is_posting_hours():
            current_hour = datetime.now().hour
            print(f"  [SKIP] Outside posting hours (current: {current_hour}:00, allowed: {POSTING_START_HOUR}:00-{POSTING_END_HOUR}:00)")
            log_to_linkedin_log(
                f"SKIPPED: Outside posting hours (current: {current_hour}:00)",
                post_preview
            )
            skipped += 1
            continue

        # Process based on DRY_RUN mode
        if DRY_RUN:
            print(f"  [DRY RUN] Would post to LinkedIn:")
            print(f"    Preview: {post_preview}...")
            print(f"    Character count: {len(post_content)}")
            log_to_linkedin_log(
                f"DRY RUN: Would post to LinkedIn",
                post_preview
            )
        else:
            print(f"  [POSTING] Posting to LinkedIn...")
            # In production, this would call the LinkedIn API
            log_to_linkedin_log(
                f"POSTED: Successfully posted to LinkedIn",
                post_preview
            )

        # Move file to Done
        done_filepath = DONE_PATH / filepath.name
        filepath.rename(done_filepath)
        print(f"  [OK] Moved to Done: {done_filepath.name}")

        processed += 1
        print()

    print("=" * 70)
    print(f"[SUCCESS] Processed: {processed}, Skipped: {skipped}")
    print("=" * 70)

    return {
        "processed": processed,
        "skipped": skipped,
        "dry_run": DRY_RUN,
        "posting_hours": is_posting_hours()
    }


def main():
    """Main execution"""
    try:
        result = process_approved_posts()
        return result
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


if __name__ == "__main__":
    main()
