"""
File System Watcher for Personal AI Employee

Monitors a designated drop folder for new files and creates action items.
"""

import time
import logging
from pathlib import Path
from datetime import datetime
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DropFolderHandler(FileSystemEventHandler):
    """Handle file system events in the drop folder"""

    def __init__(self, vault_path):
        self.needs_action = Path(vault_path) / 'Needs_Action'
        self.logger = logging.getLogger(self.__class__.__name__)

    def on_created(self, event):
        if event.is_directory:
            return

        # Copy the file to Needs_Action and create metadata
        source = Path(event.src_path)
        dest = self.needs_action / f'FILE_{source.name}'

        if not dest.exists():  # Avoid copying if already processed
            try:
                # Copy file content
                dest.write_text(source.read_text(encoding='utf-8', errors='ignore'))

                # Create metadata file
                self.create_metadata(source, dest)

                self.logger.info(f"Processed new file: {source.name}")
            except Exception as e:
                self.logger.error(f"Error processing file {source}: {e}")

    def create_metadata(self, source, dest):
        """Create metadata for the dropped file"""
        meta_path = dest.with_name(f"{dest.stem}_info.md")

        meta_content = f"""---
type: file_drop
original_name: {source.name}
size: {source.stat().st_size}
timestamp: {datetime.now().isoformat()}
status: pending
---

# New File Dropped for Processing

**Original Name:** {source.name}
**Size:** {source.stat().st_size} bytes
**Received:** {datetime.now().isoformat()}

## Action Required
- [ ] Review content
- [ ] Determine appropriate action
- [ ] Process according to Company Handbook
- [ ] Archive when complete

## Content Preview
```
{source.read_text(encoding='utf-8', errors='ignore')[:500]}
```
"""

        meta_path.write_text(meta_content)


class FileSystemWatcher:
    def __init__(self, config_path="config.json", drop_folder="./Inbox"):
        self.config = self.load_config(config_path)
        self.drop_folder = Path(drop_folder)
        self.observer = Observer()

        # Create the drop folder if it doesn't exist
        self.drop_folder.mkdir(exist_ok=True)

        logger.info(f"File System Watcher initialized for folder: {self.drop_folder}")

    def load_config(self, config_path):
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)

    def run(self):
        """Start watching the drop folder"""
        event_handler = DropFolderHandler(".")
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