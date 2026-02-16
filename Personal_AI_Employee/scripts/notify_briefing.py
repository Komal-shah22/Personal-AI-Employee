"""
Briefing Notification Script
Sends notification when CEO briefing is ready
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def find_latest_briefing():
    """Find the most recent CEO briefing file"""
    briefings_dir = Path('AI_Employee_Vault/Briefings')

    if not briefings_dir.exists():
        return None

    # Look for briefing files
    briefing_files = list(briefings_dir.glob('CEO_BRIEFING_*.md'))

    if not briefing_files:
        return None

    # Sort by modification time, most recent first
    briefing_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    return briefing_files[0]

def send_notification(briefing_path):
    """Send notification about briefing"""
    print(f"[{datetime.now().isoformat()}] CEO Briefing Ready")
    print(f"Location: {briefing_path}")
    print(f"Size: {briefing_path.stat().st_size} bytes")

    # Create notification file in Needs_Action
    notification_file = Path('AI_Employee_Vault/Needs_Action') / f'NOTIFICATION_briefing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'

    with open(notification_file, 'w', encoding='utf-8') as f:
        f.write(f"""---
type: notification
category: briefing
priority: high
created: {datetime.now().isoformat()}
status: pending
---

# CEO Briefing Ready

Your weekly CEO briefing has been generated and is ready for review.

## Details

- **File**: `{briefing_path}`
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Size**: {briefing_path.stat().st_size} bytes

## Actions

- [ ] Review briefing
- [ ] Share with team if needed
- [ ] Archive after review

## Quick View

To view the briefing:
```bash
cat "{briefing_path}"
```

Or open in your editor:
```bash
code "{briefing_path}"
```
""")

    print(f"Notification created: {notification_file}")

    # Log to activity
    log_file = Path('AI_Employee_Vault/Logs') / f'{datetime.now().strftime("%Y-%m-%d")}.txt'
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now().isoformat()}] NOTIFICATION: CEO Briefing ready at {briefing_path}\n")

def main():
    """Main entry point"""
    print(f"[{datetime.now().isoformat()}] Checking for CEO briefing...")

    # Find latest briefing
    briefing_path = find_latest_briefing()

    if not briefing_path:
        print("No briefing found. Skipping notification.")
        return

    # Check if briefing is recent (within last 24 hours)
    briefing_age = datetime.now().timestamp() - briefing_path.stat().st_mtime

    if briefing_age > 86400:  # 24 hours
        print(f"Latest briefing is {briefing_age/3600:.1f} hours old. Skipping notification.")
        return

    # Send notification
    send_notification(briefing_path)
    print("Notification sent successfully.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
