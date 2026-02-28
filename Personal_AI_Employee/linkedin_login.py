#!/usr/bin/env python3
"""
LinkedIn Login Helper - Save session for autonomous posting
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
print("LINKEDIN LOGIN HELPER")
print("=" * 60)
print("\nINSTRUCTIONS:")
print("1. Browser will open LinkedIn login page")
print("2. Login with your credentials")
print("3. Wait for feed page to load")
print("4. Session will be saved automatically")
print("5. Close browser after seeing 'Login Complete'")
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
        
        print("\nLoading LinkedIn login page...")
        page.goto('https://www.linkedin.com/login', timeout=60000)
        
        print("\n" + "=" * 60)
        print("PLEASE LOGIN TO LINKEDIN")
        print("=" * 60)
        print("\nWaiting 120 seconds for you to login...")
        print("(Script will auto-detect when you reach the feed)")
        print("=" * 60 + "\n")
        
        # Wait for user to login (max 120 seconds)
        for i in range(120):
            try:
                # Check if we're on the feed page (logged in)
                if 'feed' in page.url or page.query_selector('div[aria-label="Start a post"]'):
                    print("\n✅ LOGIN DETECTED!")
                    print(f"Current URL: {page.url}")
                    print("\nSession saved successfully!")
                    print("You can now use autonomous_linkedin_post.py")
                    time.sleep(5)  # Give time to see the success message
                    break
            except:
                pass
            
            time.sleep(1)
            
            # Show progress every 10 seconds
            if (i + 1) % 10 == 0:
                print(f"  Waiting... {i + 1}/120 seconds")
        
        browser.close()
        
        print("\n" + "=" * 60)
        print("LOGIN COMPLETE!")
        print("=" * 60)
        print("\nSession saved to: sessions/linkedin/")
        print("\nNow you can run:")
        print("  python autonomous_linkedin_post.py")
        print("=" * 60 + "\n")
        
except Exception as e:
    print(f"\nERROR: {e}")
    print("\nMake sure Playwright is installed:")
    print("  pip install playwright")
    print("  playwright install chromium")
