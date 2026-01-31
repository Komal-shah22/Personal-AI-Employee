#!/usr/bin/env python3
"""
Test script to run the original fixed filesystem watcher and wait for new PDF detection
"""
import subprocess
import time
import signal

def run_test():
    print("Starting filesystem watcher to detect NEW PDF file...")

    # Start the filesystem watcher in a subprocess
    proc = subprocess.Popen(['python', 'filesystem_watcher.py'])

    print("Filesystem watcher started. Waiting for 10 seconds to see if NEW PDF is detected...")

    # Wait to see if it gets processed
    time.sleep(10)

    # Terminate the process gracefully
    proc.terminate()
    time.sleep(1)  # Give it a moment to shut down cleanly
    if proc.poll() is None:  # Process still running
        proc.kill()  # Force kill if still running

    print("Filesystem watcher terminated.")

if __name__ == "__main__":
    run_test()