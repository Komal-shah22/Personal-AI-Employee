"""
Unified Watcher Launcher
Starts all available watchers for the AI Employee system
"""

import sys
import time
import logging
import subprocess
from pathlib import Path
from typing import List, Dict
import signal

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Available watchers
WATCHERS = {
    'gmail': {
        'name': 'Gmail Watcher',
        'script': 'watchers/gmail_watcher.py',
        'description': 'Monitors Gmail for unread important emails',
        'requires_setup': True,
        'setup_file': 'README_gmail_setup.md'
    },
    'whatsapp': {
        'name': 'WhatsApp Watcher',
        'script': 'watchers/whatsapp_watcher.py',
        'description': 'Monitors WhatsApp for urgent messages (30s interval)',
        'requires_setup': True,
        'setup_file': 'WHATSAPP_SETUP_GUIDE.md'
    },
    'file': {
        'name': 'File Watcher',
        'script': 'watchers/file_watcher.py',
        'description': 'Monitors desktop drop folder for new files',
        'requires_setup': False,
        'setup_file': 'README_file_watcher.md'
    },
    'email_processor': {
        'name': 'Email Processor',
        'script': 'process_email_queue.py',
        'description': 'Processes email queues and handles work-related opportunities',
        'requires_setup': False,
        'setup_file': 'README_email_processor.md'
    }
}


class WatcherManager:
    """Manages multiple watcher processes"""

    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.running = True

    def start_watcher(self, watcher_key: str) -> bool:
        """Start a specific watcher"""
        watcher = WATCHERS.get(watcher_key)
        if not watcher:
            logger.error(f"Unknown watcher: {watcher_key}")
            return False

        script_path = Path(watcher['script'])
        if not script_path.exists():
            logger.error(f"Watcher script not found: {script_path}")
            return False

        try:
            logger.info(f"Starting {watcher['name']}...")
            process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            self.processes[watcher_key] = process
            logger.info(f"✓ {watcher['name']} started (PID: {process.pid})")
            return True

        except Exception as e:
            logger.error(f"Failed to start {watcher['name']}: {e}")
            return False

    def stop_watcher(self, watcher_key: str):
        """Stop a specific watcher"""
        if watcher_key in self.processes:
            process = self.processes[watcher_key]
            watcher = WATCHERS[watcher_key]

            logger.info(f"Stopping {watcher['name']}...")
            process.terminate()

            try:
                process.wait(timeout=5)
                logger.info(f"✓ {watcher['name']} stopped")
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {watcher['name']}...")
                process.kill()
                process.wait()

            del self.processes[watcher_key]

    def stop_all(self):
        """Stop all running watchers"""
        logger.info("Stopping all watchers...")
        for watcher_key in list(self.processes.keys()):
            self.stop_watcher(watcher_key)

    def check_processes(self):
        """Check if processes are still running and restart if needed"""
        for watcher_key, process in list(self.processes.items()):
            if process.poll() is not None:
                # Process has terminated
                watcher = WATCHERS[watcher_key]
                logger.warning(f"{watcher['name']} has stopped unexpectedly")
                logger.info(f"Restarting {watcher['name']}...")
                del self.processes[watcher_key]
                self.start_watcher(watcher_key)

    def run(self, watchers_to_start: List[str]):
        """Main run loop"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, lambda s, f: self.shutdown())
        signal.signal(signal.SIGTERM, lambda s, f: self.shutdown())

        # Start requested watchers
        for watcher_key in watchers_to_start:
            self.start_watcher(watcher_key)

        if not self.processes:
            logger.error("No watchers started. Exiting.")
            return

        logger.info(f"\n{'='*60}")
        logger.info(f"Running {len(self.processes)} watcher(s)")
        logger.info(f"Press Ctrl+C to stop all watchers")
        logger.info(f"{'='*60}\n")

        # Monitor processes
        try:
            while self.running:
                self.check_processes()
                time.sleep(5)
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()

    def shutdown(self):
        """Graceful shutdown"""
        self.running = False
        self.stop_all()
        logger.info("All watchers stopped. Goodbye!")


def print_banner():
    """Print startup banner"""
    print("\n" + "="*60)
    print("AI EMPLOYEE - WATCHER MANAGER")
    print("="*60)


def print_available_watchers():
    """Print list of available watchers"""
    print("\nAvailable Watchers:")
    print("-" * 60)
    for key, watcher in WATCHERS.items():
        status = "⚠ Requires setup" if watcher['requires_setup'] else "✓ Ready"
        print(f"\n[{key}] {watcher['name']}")
        print(f"    {watcher['description']}")
        print(f"    Status: {status}")
        if watcher['requires_setup']:
            print(f"    Setup: See {watcher['setup_file']}")
    print("\n" + "-" * 60)


def print_usage():
    """Print usage instructions"""
    print("\nUsage:")
    print("  python start_watchers.py [watcher1] [watcher2] ...")
    print("  python start_watchers.py all")
    print("\nExamples:")
    print("  python start_watchers.py file          # Start file watcher only")
    print("  python start_watchers.py gmail file    # Start Gmail and file watchers")
    print("  python start_watchers.py all           # Start all watchers")
    print("\nOptions:")
    print("  --list    Show available watchers")
    print("  --help    Show this help message")
    print()


def main():
    """Main entry point"""
    print_banner()

    # Parse arguments
    args = sys.argv[1:]

    if not args or '--help' in args:
        print_available_watchers()
        print_usage()
        return

    if '--list' in args:
        print_available_watchers()
        return

    # Determine which watchers to start
    if 'all' in args:
        watchers_to_start = list(WATCHERS.keys())
    else:
        watchers_to_start = [w for w in args if w in WATCHERS]

    if not watchers_to_start:
        logger.error("No valid watchers specified")
        print_usage()
        return

    # Check for setup requirements
    needs_setup = []
    for watcher_key in watchers_to_start:
        watcher = WATCHERS[watcher_key]
        if watcher['requires_setup']:
            needs_setup.append(f"{watcher['name']} - See {watcher['setup_file']}")

    if needs_setup:
        print("\n⚠ Warning: Some watchers require setup:")
        for item in needs_setup:
            print(f"  - {item}")
        print("\nThey may fail to start if not configured properly.")
        print("Continue anyway? (y/n): ", end='')

        try:
            response = input().strip().lower()
            if response != 'y':
                print("Cancelled.")
                return
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
            return

    # Start watcher manager
    manager = WatcherManager()
    manager.run(watchers_to_start)


if __name__ == '__main__':
    main()
