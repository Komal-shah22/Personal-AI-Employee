"""
File Watcher - Monitors AI_Drop_Folder for new files
Automatically processes and creates action items for dropped files
"""

import os
import time
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from plyer import notification

# Configuration
DROP_FOLDER = Path.home() / "Desktop" / "AI_Drop_Folder"
ACTION_DIR = Path("AI_Employee_Vault/Needs_Action")
LOG_DIR = Path("AI_Employee_Vault/Logs")
LOG_FILE = LOG_DIR / "file_watcher.log"

# File type detection mapping
FILE_TYPE_MAP = {
    '.pdf': 'invoice',
    '.csv': 'data',
    '.jpg': 'image',
    '.jpeg': 'image',
    '.png': 'image',
    '.docx': 'document',
    '.doc': 'document',
    '.txt': 'document',
    '.xlsx': 'data',
    '.xls': 'data',
}

# Suggested actions based on file type
SUGGESTED_ACTIONS = {
    'invoice': [
        '- [ ] Review invoice details',
        '- [ ] Verify amount and vendor',
        '- [ ] Process payment if approved',
        '- [ ] File in accounting system'
    ],
    'data': [
        '- [ ] Review data contents',
        '- [ ] Validate data format',
        '- [ ] Import to appropriate system',
        '- [ ] Archive original file'
    ],
    'image': [
        '- [ ] Review image content',
        '- [ ] Determine purpose (receipt, document scan, etc.)',
        '- [ ] Process accordingly',
        '- [ ] Archive or attach to relevant record'
    ],
    'document': [
        '- [ ] Read document',
        '- [ ] Determine required action',
        '- [ ] Respond or file as needed',
        '- [ ] Update status when complete'
    ],
    'unknown': [
        '- [ ] Identify file type and purpose',
        '- [ ] Determine appropriate action',
        '- [ ] Process accordingly'
    ]
}

# Setup logging
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FileDropHandler(FileSystemEventHandler):
    """Handler for file system events in the drop folder"""

    def __init__(self):
        super().__init__()
        self.processing = set()  # Track files being processed

    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Ignore temporary files and hidden files
        if file_path.name.startswith('.') or file_path.name.startswith('~'):
            return

        # Ignore metadata files we create
        if file_path.suffix == '.md':
            return

        # Avoid processing the same file multiple times
        if str(file_path) in self.processing:
            return

        self.processing.add(str(file_path))

        try:
            logger.info(f"New file detected: {file_path.name}")
            self.process_file(file_path)
        finally:
            self.processing.discard(str(file_path))

    def wait_for_file_ready(self, file_path: Path, max_attempts: int = 5) -> bool:
        """Wait for file to be fully written and not locked"""
        for attempt in range(max_attempts):
            try:
                # Try to open the file to check if it's locked
                with open(file_path, 'rb') as f:
                    f.read(1)

                # Check if file size is stable
                size1 = file_path.stat().st_size
                time.sleep(0.5)
                size2 = file_path.stat().st_size

                if size1 == size2:
                    return True

            except (PermissionError, IOError) as e:
                logger.warning(f"File locked or not ready (attempt {attempt + 1}/{max_attempts}): {file_path.name}")
                time.sleep(2)

        return False

    def get_file_type(self, file_path: Path) -> str:
        """Detect file type based on extension"""
        ext = file_path.suffix.lower()
        return FILE_TYPE_MAP.get(ext, 'unknown')

    def get_unique_filename(self, destination: Path, original_name: str) -> Path:
        """Generate unique filename if file already exists"""
        dest_path = destination / original_name

        if not dest_path.exists():
            return dest_path

        # Add timestamp suffix
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        stem = dest_path.stem
        suffix = dest_path.suffix
        unique_name = f"{stem}_{timestamp}{suffix}"

        logger.info(f"File already exists, using unique name: {unique_name}")
        return destination / unique_name

    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def create_metadata_file(self, file_info: Dict, dest_file_path: Path):
        """Create companion metadata markdown file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            metadata_filename = f"FILE_{dest_file_path.stem}_{timestamp}.md"
            metadata_path = ACTION_DIR / metadata_filename

            file_type = file_info['detected_type']
            actions = '\n'.join(SUGGESTED_ACTIONS.get(file_type, SUGGESTED_ACTIONS['unknown']))

            content = f"""---
type: file_drop
original_name: {file_info['original_name']}
size: {file_info['size']}
size_bytes: {file_info['size_bytes']}
date_added: {file_info['date_added']}
detected_type: {file_info['detected_type']}
file_location: {dest_file_path.name}
status: pending
---

# File Drop: {file_info['original_name']}

## File Information
- **Original Name**: {file_info['original_name']}
- **Size**: {file_info['size']}
- **Detected Type**: {file_info['detected_type'].upper()}
- **Date Added**: {file_info['date_added']}
- **Location**: `AI_Employee_Vault/Needs_Action/{dest_file_path.name}`

## Detected Type: {file_info['detected_type'].upper()}

## Suggested Actions
{actions}

## Notes
Add any additional notes or context about this file here.

---
*File automatically detected and processed by File Watcher*
"""

            with open(metadata_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Created metadata file: {metadata_filename}")
            return metadata_path

        except Exception as e:
            logger.error(f"Error creating metadata file: {e}")
            return None

    def send_notification(self, file_name: str, file_type: str):
        """Send desktop notification"""
        try:
            notification.notify(
                title='New File Detected',
                message=f'{file_name}\nType: {file_type.upper()}',
                app_name='AI Employee',
                timeout=5
            )
        except Exception as e:
            logger.warning(f"Could not send notification: {e}")

    def process_file(self, file_path: Path):
        """Process a newly detected file"""
        try:
            # Wait for file to be ready
            if not self.wait_for_file_ready(file_path):
                logger.error(f"File not ready after retries, skipping: {file_path.name}")
                return

            # Get file information
            file_stats = file_path.stat()
            file_size_bytes = file_stats.st_size
            file_size = self.format_file_size(file_size_bytes)
            file_type = self.get_file_type(file_path)
            date_added = datetime.now().isoformat()

            file_info = {
                'original_name': file_path.name,
                'size': file_size,
                'size_bytes': file_size_bytes,
                'detected_type': file_type,
                'date_added': date_added
            }

            # Ensure destination directory exists
            ACTION_DIR.mkdir(parents=True, exist_ok=True)

            # Get unique destination path
            dest_path = self.get_unique_filename(ACTION_DIR, file_path.name)

            # Copy file to action directory
            try:
                shutil.copy2(file_path, dest_path)
                logger.info(f"Copied file to: {dest_path}")
            except PermissionError as e:
                logger.error(f"Permission denied copying file: {file_path.name} - {e}")
                return
            except Exception as e:
                logger.error(f"Error copying file: {file_path.name} - {e}")
                return

            # Create metadata file
            self.create_metadata_file(file_info, dest_path)

            # Send notification
            self.send_notification(file_path.name, file_type)

            logger.info(f"Successfully processed: {file_path.name} (Type: {file_type})")

        except Exception as e:
            logger.error(f"Error processing file {file_path.name}: {e}")


class FileWatcher:
    """Main file watcher class"""

    def __init__(self):
        self.observer = Observer()
        self.handler = FileDropHandler()

        # Create drop folder if it doesn't exist
        DROP_FOLDER.mkdir(parents=True, exist_ok=True)
        logger.info(f"Drop folder ready: {DROP_FOLDER}")

    def start(self):
        """Start watching the drop folder"""
        logger.info("File Watcher started")
        logger.info(f"Monitoring: {DROP_FOLDER}")
        logger.info(f"Drop files here to automatically process them")

        # Schedule the observer
        self.observer.schedule(self.handler, str(DROP_FOLDER), recursive=False)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("File Watcher stopped by user")
            self.observer.stop()

        self.observer.join()


def main():
    """Main entry point"""
    print("=" * 60)
    print("AI Employee - File Watcher")
    print("=" * 60)
    print(f"\nDrop Folder: {DROP_FOLDER}")
    print(f"Action Folder: {ACTION_DIR}")
    print(f"Log File: {LOG_FILE}")
    print("\nDrop any file into the folder to automatically process it.")
    print("Press Ctrl+C to stop.\n")
    print("=" * 60)

    watcher = FileWatcher()
    watcher.start()


if __name__ == '__main__':
    main()
