"""
WhatsApp Watcher Setup Script

This script helps you set up the WhatsApp watcher for the first time.
It will guide you through the QR code scanning process.
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 70)
    print("🚀 WhatsApp Watcher Setup")
    print("=" * 70)
    print()
    print("This script will help you set up WhatsApp Web integration.")
    print()
    print("📋 Prerequisites:")
    print("   ✓ Playwright must be installed")
    print("   ✓ Your phone must have WhatsApp installed")
    print("   ✓ Your phone must be connected to the internet")
    print()
    print("=" * 70)
    print()

    # Check if playwright is installed
    try:
        import playwright
        print("✅ Playwright is installed")
    except ImportError:
        print("❌ Playwright is not installed!")
        print()
        print("Installing Playwright...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"])
        print()
        print("Installing Playwright browsers...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
        print()
        print("✅ Playwright installation complete!")
        print()

    # Check if browsers are installed
    print("Checking Playwright browsers...")
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True,
        text=True
    )
    print("✅ Chromium browser ready")
    print()

    # Create sessions directory
    sessions_dir = Path("sessions/whatsapp")
    sessions_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created session directory: {sessions_dir.absolute()}")
    print()

    print("=" * 70)
    print("📱 NEXT STEPS:")
    print("=" * 70)
    print()
    print("1. Run the WhatsApp watcher:")
    print("   python watchers/whatsapp_watcher.py")
    print()
    print("2. A browser window will open with WhatsApp Web")
    print()
    print("3. Scan the QR code with your phone:")
    print("   • Open WhatsApp on your phone")
    print("   • Tap Menu (⋮) or Settings")
    print("   • Tap 'Linked Devices'")
    print("   • Tap 'Link a Device'")
    print("   • Scan the QR code on your computer screen")
    print()
    print("4. Once logged in, the session will be saved")
    print()
    print("5. Future runs will use the saved session (no QR code needed)")
    print()
    print("=" * 70)
    print()

    response = input("Ready to start the watcher now? (y/n): ").strip().lower()

    if response == 'y':
        print()
        print("🚀 Starting WhatsApp Watcher...")
        print("   Press Ctrl+C to stop")
        print()
        subprocess.run([sys.executable, "watchers/whatsapp_watcher.py"])
    else:
        print()
        print("Setup complete! Run the watcher when you're ready:")
        print("   python watchers/whatsapp_watcher.py")
        print()

if __name__ == "__main__":
    main()
