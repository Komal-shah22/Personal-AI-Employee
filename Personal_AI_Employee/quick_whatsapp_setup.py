"""
Quick WhatsApp Session Setup - No Prompts
==========================================

This version runs directly without asking for confirmation.
Just run and scan the QR code.

Usage:
    python quick_whatsapp_setup.py
"""

import time
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

session_path = Path('sessions/whatsapp')
session_path.mkdir(parents=True, exist_ok=True)

print("\n" + "=" * 70)
print("WhatsApp Web Session Setup - Quick Version")
print("=" * 70)
print("\n[*] Opening browser... Please wait...")
print("[*] Scan QR code when it appears")
print("[*] Press Ctrl+C when done\n")

try:
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(session_path.absolute()),
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox'],
            viewport={'width': 1280, 'height': 800}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto('https://web.whatsapp.com', timeout=60000)

        time.sleep(3)

        check_count = 0
        while True:
            check_count += 1

            # Check if logged in
            if page.query_selector('[data-testid="chat-list"]'):
                print("\n" + "=" * 70)
                print("[SUCCESS] WhatsApp Web is logged in!")
                print("=" * 70)
                print("\nSession saved to: sessions/whatsapp/")
                print("\nYou can now:")
                print("  1. Close this browser")
                print("  2. Press Ctrl+C here")
                print("  3. Run: python watchers/whatsapp_watcher.py")
                print("\n" + "=" * 70)
                break

            # Check for QR code
            if page.query_selector('canvas[aria-label="Scan me!"]'):
                if check_count == 1:
                    print("\n[*] QR CODE VISIBLE - Scan with your phone!")
                    print("    WhatsApp > Settings > Linked Devices > Link a Device\n")

                if check_count % 10 == 0:
                    print(f"[*] Waiting... ({check_count * 2}s elapsed)")

            time.sleep(2)

        # Keep open until user closes
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Closing browser...")

        browser.close()
        print("[SUCCESS] Setup complete!\n")

except KeyboardInterrupt:
    print("\n[*] Setup cancelled by user\n")
except Exception as e:
    print(f"\n[ERROR] {e}\n")
    print("Troubleshooting:")
    print("  1. Check internet connection")
    print("  2. Run: playwright install chromium")
    print("  3. Try opening WhatsApp Web in regular browser\n")
