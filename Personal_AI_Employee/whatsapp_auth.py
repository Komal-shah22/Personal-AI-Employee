#!/usr/bin/env python3
"""
WhatsApp QR Code Authentication
Opens WhatsApp Web in browser for QR code scanning
"""

import sys
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Session directory
SESSION_DIR = Path('sessions/whatsapp')
SESSION_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "=" * 60)
print("WHATSAPP QR CODE AUTHENTICATION")
print("=" * 60)
print("\nINSTRUCTIONS:")
print("1. WhatsApp Web will open in your browser")
print("2. Open WhatsApp on your phone")
print("3. Go to Settings > Linked Devices")
print("4. Tap 'Link a Device'")
print("5. Scan the QR code on your screen")
print("6. After scanning, close the browser")
print("7. Session will be saved for future use")
print("\n" + "=" * 60)
print("\nOpening WhatsApp Web in 3 seconds...")
time.sleep(3)

try:
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,  # Show browser for QR code
            args=['--no-sandbox', '--start-maximized']
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        # Navigate to WhatsApp Web
        print("\nLoading WhatsApp Web...")
        page.goto('https://web.whatsapp.com', timeout=60000)
        
        print("\n" + "=" * 60)
        print("SCAN THE QR CODE!")
        print("=" * 60)
        print("\nWaiting for you to scan the QR code...")
        print("(Browser will stay open for 60 seconds)")
        print("=" * 60 + "\n")
        
        # Wait for 60 seconds for user to scan QR code
        try:
            # Wait for chat list to appear (means authenticated)
            page.wait_for_selector('div[contenteditable="true"][data-tab="3"]', timeout=60000)
            print("\nSUCCESS! WhatsApp authenticated!")
            print("Session saved. You can now send messages.")
        except Exception as e:
            print("\nTimeout! QR code not scanned.")
            print("Please run the script again.")
        
        # Keep browser open for a bit
        time.sleep(5)
        browser.close()
        
except Exception as e:
    print(f"\nERROR: {e}")
    print("\nMake sure Playwright is installed:")
    print("  pip install playwright")
    print("  playwright install chromium")

print("\n" + "=" * 60)
