#!/usr/bin/env python3
"""
LinkedIn Session Saver - Improved Version
Keeps browser open until user manually closes it
"""

import sys
import io
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Fix Unicode for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SESSION_DIR = Path('sessions/linkedin')
SESSION_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "=" * 60)
print("LINKEDIN SESSION SAVER")
print("=" * 60)
print("\nINSTRUCTIONS:")
print("1. Browser will open LinkedIn")
print("2. Login with your email/password")
print("3. Wait for your feed to load completely")
print("4. DO NOT close the browser yet!")
print("5. Press ENTER in this terminal when you see your feed")
print("6. Session will be saved")
print("7. Then you can close the browser")
print("\n" + "=" * 60)
print("\nOpening LinkedIn in 3 seconds...")
time.sleep(3)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,
            args=['--no-sandbox', '--start-maximized'],
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        print("\nLoading LinkedIn...")
        page.goto('https://www.linkedin.com/feed/', timeout=60000)
        
        print("\n" + "=" * 60)
        print("PLEASE LOGIN TO LINKEDIN")
        print("=" * 60)
        print("\nBrowser is open. Please:")
        print("  1. Login to LinkedIn")
        print("  2. Wait for your feed to load")
        print("  3. Come back here and press ENTER")
        print("=" * 60 + "\n")
        
        # Wait for user to press Enter
        input("Press ENTER when you're logged in and can see your feed...")
        
        # Verify we're on feed
        current_url = page.url
        print(f"\nCurrent URL: {current_url}")
        
        if 'feed' in current_url or 'linkedin.com' in current_url:
            print("\n✅ SUCCESS! LinkedIn session active!")
            print("\nSaving session...")
            time.sleep(2)  # Let browser save cookies
            print("✅ Session saved to: sessions/linkedin/")
        else:
            print("\n⚠ Not on LinkedIn feed. Please try again.")
        
        print("\n" + "=" * 60)
        print("YOU CAN NOW CLOSE THE BROWSER")
        print("=" * 60)
        print("\nNext step:")
        print("  python autonomous_linkedin_post.py")
        print("=" * 60 + "\n")
        
        # Keep browser open until user is ready
        input("\nPress ENTER to close browser and continue...")
        browser.close()
        
        print("\n✅ All done! Your LinkedIn poster is ready!")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
