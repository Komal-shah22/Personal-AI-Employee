#!/usr/bin/env python3
"""
Direct WhatsApp Sender - Send WhatsApp messages immediately
Uses Playwright to automate WhatsApp Web for instant message sending
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Session storage
SESSION_DIR = Path('.whatsapp_session')
SESSION_DIR.mkdir(exist_ok=True)

def send_whatsapp_direct(phone, message):
    """Send WhatsApp message directly via WhatsApp Web automation"""

    try:
        with sync_playwright() as p:
            # Launch browser with persistent context to maintain session
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=False,  # Need to see for QR code if not authenticated
                args=['--no-sandbox']
            )

            page = browser.pages[0] if browser.pages else browser.new_page()

            # Navigate to WhatsApp Web
            page.goto('https://web.whatsapp.com', timeout=60000)

            # Wait for WhatsApp to load (either QR code or chat list)
            try:
                # Check if already logged in by looking for search box
                page.wait_for_selector('div[contenteditable="true"][data-tab="3"]', timeout=10000)
                authenticated = True
            except PlaywrightTimeout:
                # Not authenticated, need QR code scan
                return {
                    'success': False,
                    'error': 'WhatsApp Web not authenticated. Please scan QR code first.',
                    'action_required': 'qr_scan'
                }

            # Format phone number (remove spaces, dashes, etc.)
            clean_phone = ''.join(filter(str.isdigit, phone))
            if not clean_phone.startswith('+'):
                clean_phone = '+' + clean_phone

            # Navigate to chat using WhatsApp Web URL
            chat_url = f'https://web.whatsapp.com/send?phone={clean_phone}'
            page.goto(chat_url, timeout=30000)

            # Wait for chat to load
            time.sleep(3)

            # Check if chat loaded successfully
            try:
                # Look for the message input box
                message_box = page.wait_for_selector(
                    'div[contenteditable="true"][data-tab="10"]',
                    timeout=10000
                )

                # Type the message
                message_box.click()
                message_box.fill(message)

                # Wait a moment for the message to be typed
                time.sleep(1)

                # Find and click send button
                send_button = page.wait_for_selector(
                    'button[aria-label="Send"], span[data-icon="send"]',
                    timeout=5000
                )
                send_button.click()

                # Wait for message to be sent
                time.sleep(2)

                browser.close()

                return {
                    'success': True,
                    'to': phone,
                    'message': message,
                    'sent_at': datetime.now().isoformat(),
                    'method': 'whatsapp_web_direct'
                }

            except PlaywrightTimeout:
                browser.close()
                return {
                    'success': False,
                    'error': f'Could not find chat for {phone}. Please verify the number is correct and has WhatsApp.',
                    'fallback': 'queued_for_orchestrator'
                }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'fallback': 'queued_for_orchestrator'
        }

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python send_whatsapp_direct.py <phone> <message>'
        }))
        sys.exit(1)

    phone = sys.argv[1]
    message = sys.argv[2]

    result = send_whatsapp_direct(phone, message)
    print(json.dumps(result))
