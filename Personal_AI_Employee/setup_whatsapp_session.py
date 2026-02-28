"""
WhatsApp Session Setup Script
==============================

This script helps you set up WhatsApp Web session for the first time.
It will keep the browser open until you successfully scan the QR code.

Usage:
    python setup_whatsapp_session.py

Instructions:
1. Run this script
2. Browser will open with WhatsApp Web
3. Scan the QR code with your phone
4. Wait for "Successfully logged in!" message
5. Press Ctrl+C to close when done
"""

import time
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_whatsapp_session():
    """
    One-time setup to authenticate WhatsApp Web and save session.
    Browser stays open until you manually close it.
    """

    session_path = Path('sessions/whatsapp')
    session_path.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 70)
    logger.info("WhatsApp Web Session Setup")
    logger.info("=" * 70)
    logger.info("")
    logger.info("[*] Instructions:")
    logger.info("1. Browser will open with WhatsApp Web")
    logger.info("2. Scan the QR code with your phone:")
    logger.info("   - Open WhatsApp on your phone")
    logger.info("   - Go to Settings > Linked Devices")
    logger.info("   - Tap 'Link a Device'")
    logger.info("   - Scan the QR code on screen")
    logger.info("3. Wait for chat list to load")
    logger.info("4. Press Ctrl+C in this terminal when done")
    logger.info("")
    logger.info("[*] Browser will stay open - take your time!")
    logger.info("=" * 70)
    logger.info("")

    try:
        with sync_playwright() as p:
            # Launch browser with persistent context
            logger.info("[*] Opening browser...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(session_path.absolute()),
                headless=False,  # Must be False to see QR code
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage'
                ],
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            # Get or create page
            page = browser.pages[0] if browser.pages else browser.new_page()

            # Navigate to WhatsApp Web
            logger.info("[*] Loading WhatsApp Web...")
            page.goto('https://web.whatsapp.com', wait_until='domcontentloaded', timeout=60000)

            # Wait a bit for page to stabilize
            time.sleep(3)

            # Check if already logged in
            logger.info("[*] Checking login status...")

            # Wait indefinitely for either QR code or chat list
            logged_in = False
            check_count = 0

            while not logged_in:
                check_count += 1

                # Check for chat list (logged in)
                chat_list = page.query_selector('[data-testid="chat-list"]')
                if chat_list:
                    logger.info("")
                    logger.info("=" * 70)
                    logger.info("[SUCCESS] WhatsApp Web is logged in!")
                    logger.info("=" * 70)
                    logger.info("")
                    logger.info("Your session has been saved to: sessions/whatsapp/")
                    logger.info("")
                    logger.info("You can now:")
                    logger.info("1. Close this browser window")
                    logger.info("2. Press Ctrl+C in this terminal")
                    logger.info("3. Run the WhatsApp watcher: python watchers/whatsapp_watcher.py")
                    logger.info("")
                    logger.info("The watcher will use this saved session automatically.")
                    logger.info("=" * 70)
                    logged_in = True
                    break

                # Check for QR code (not logged in)
                qr_code = page.query_selector('canvas[aria-label="Scan me!"]')
                if qr_code:
                    if check_count == 1:
                        logger.info("")
                        logger.info("=" * 70)
                        logger.info("[*] QR CODE VISIBLE - Please scan now!")
                        logger.info("=" * 70)
                        logger.info("")
                        logger.info("Steps to scan:")
                        logger.info("1. Open WhatsApp on your phone")
                        logger.info("2. Tap Menu or Settings")
                        logger.info("3. Tap 'Linked Devices'")
                        logger.info("4. Tap 'Link a Device'")
                        logger.info("5. Point your phone at the QR code on screen")
                        logger.info("")
                        logger.info("[*] Waiting for scan... (unlimited time)")
                        logger.info("=" * 70)

                    # Show progress dots
                    if check_count % 10 == 0:
                        logger.info(f"[*] Still waiting... ({check_count * 2} seconds elapsed)")

                # Wait 2 seconds before checking again
                time.sleep(2)

            # Keep browser open until user closes it
            logger.info("")
            logger.info("Browser will stay open. Press Ctrl+C when you're done exploring.")
            logger.info("")

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("")
                logger.info("=" * 70)
                logger.info("[SUCCESS] Setup complete! Closing browser...")
                logger.info("=" * 70)

            browser.close()

    except KeyboardInterrupt:
        logger.info("")
        logger.info("=" * 70)
        logger.info("Setup interrupted by user")
        logger.info("=" * 70)

    except Exception as e:
        logger.error("")
        logger.error("=" * 70)
        logger.error(f"[ERROR] Error during setup: {e}")
        logger.error("=" * 70)
        logger.error("")
        logger.error("Troubleshooting:")
        logger.error("1. Make sure you have internet connection")
        logger.error("2. Try running: playwright install chromium")
        logger.error("3. Check if WhatsApp Web is accessible in regular browser")
        raise


if __name__ == "__main__":
    print("")
    print("=" * 70)
    print("WhatsApp Web Session Setup")
    print("=" * 70)
    print("")
    print("[!] DISCLAIMER:")
    print("This tool is for personal use only. Ensure compliance with")
    print("WhatsApp's Terms of Service. Use at your own risk.")
    print("")
    print("Press Enter to continue or Ctrl+C to cancel...")
    print("=" * 70)

    try:
        input()
        setup_whatsapp_session()
    except KeyboardInterrupt:
        print("\nSetup cancelled by user")
