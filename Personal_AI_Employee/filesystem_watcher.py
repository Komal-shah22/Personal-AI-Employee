"""
File System Watcher for Personal AI Employee

Monitors a designated drop folder for new files and creates action items.
"""

import time
import logging
from pathlib import Path
from datetime import datetime
import json
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging to show INFO and above
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('filesystem_watcher.log')  # Also log to file
    ]
)
logger = logging.getLogger(__name__)

class DropFolderHandler(FileSystemEventHandler):
    """Handle file system events in the drop folder"""

    def __init__(self, config):
        self.vault_path = Path(config['directories']['inbox']).parent  # Get parent of inbox (AI_Employee_Vault)
        self.needs_action = Path(config['directories']['needs_action'])
        self.logger = logging.getLogger(self.__class__.__name__)

        # Ensure the destination directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return

        # Check if it's a PDF file (or any file)
        source = Path(event.src_path)

        # Log the detected file creation
        self.logger.info(f"Detected new file: {source.name}")

        # Only process files that exist and have valid extensions
        if source.exists() and source.suffix.lower() in ['.pdf', '.txt', '.docx', '.doc', '.xlsx', '.xls', '.csv', '.jpg', '.jpeg', '.png']:
            # Create metadata file in Needs_Action directory
            self.create_metadata(source)

            self.logger.info(f"Processed new file: {source.name}")
        else:
            self.logger.info(f"Ignoring file: {source.name} (unsupported type)")

    def create_metadata(self, source):
        """Create metadata for the dropped file"""
        # Create a unique filename for the metadata
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        meta_filename = f"FILE_{timestamp}_{source.name.replace('.', '_')}_info.md"
        meta_path = self.needs_action / meta_filename

        # Handle different file types appropriately
        try:
            if source.suffix.lower() in ['.txt', '.md']:
                # Text files - read content
                content_preview = source.read_text(encoding='utf-8', errors='ignore')[:500]
            elif source.suffix.lower() in ['.pdf']:
                # PDF files - don't try to read content, just note it's a PDF
                content_preview = f"[PDF file: {source.name}] Contains binary PDF data - will be processed separately"
            elif source.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                # Image files
                content_preview = f"[Image file: {source.name}] Contains image data - will be processed separately"
            elif source.suffix.lower() in ['.docx', '.doc']:
                # Document files
                content_preview = f"[Document file: {source.name}] Contains document data - will be processed separately"
            else:
                # Other files
                content_preview = f"[File: {source.name}] Contains binary data - will be processed separately"

            meta_content = f"""---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size}
timestamp: {datetime.now().isoformat()}
status: pending
file_path: {str(source.absolute())}
---

# New File Dropped for Processing

**Original Name:** {source.name}
**Size:** {source.stat().st_size} bytes
**Received:** {datetime.now().isoformat()}
**Type:** {source.suffix.lower()}

## Action Required
- [ ] Review content
- [ ] Determine appropriate action
- [ ] Process according to Company Handbook
- [ ] Archive when complete

## Content Preview
```
{content_preview}
```
"""

            meta_path.write_text(meta_content)
            self.logger.info(f"Created metadata file: {meta_path}")

            # Update dashboard to reflect the new file
            self.update_dashboard()

        except Exception as e:
            self.logger.error(f"Error creating metadata for file {source}: {e}")

    def update_dashboard(self):
        """Update the dashboard to reflect changes"""
        try:
            # Run the update-dashboard skill
            result = subprocess.run([sys.executable, '.claude/skills/update-dashboard/skill.py'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Dashboard updated successfully after file drop: {result.stdout}")
            else:
                print(f"Dashboard update failed: {result.stderr}")
        except Exception as e:
            print(f"Error updating dashboard: {e}")


class FileSystemWatcher:
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        # Use the inbox path from config
        self.drop_folder = Path(self.config['directories']['inbox'])
        self.observer = Observer()

        # Create the drop folder if it doesn't exist
        self.drop_folder.mkdir(parents=True, exist_ok=True)

        logger.info(f"File System Watcher initialized for folder: {self.drop_folder}")
        logger.info(f"Config loaded - Inbox: {self.config['directories']['inbox']}, Needs_Action: {self.config['directories']['needs_action']}")

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def run(self):
        """Start watching the drop folder"""
        event_handler = DropFolderHandler(self.config)
        self.observer.schedule(event_handler, str(self.drop_folder), recursive=False)

        self.observer.start()
        logger.info(f"Started watching folder: {self.drop_folder}")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            logger.info("File System Watcher stopped by user")

        self.observer.join()


if __name__ == "__main__":
    watcher = FileSystemWatcher()
    watcher.run()