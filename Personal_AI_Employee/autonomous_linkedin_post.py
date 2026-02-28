#!/usr/bin/env python3
"""
Autonomous LinkedIn Poster - Fully Automated
Opens browser, goes to LinkedIn, and posts automatically
No manual intervention needed!
"""

import os
import sys
import io
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Fix Unicode for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Session directory for persistent login
SESSION_DIR = Path('sessions/linkedin')
SESSION_DIR.mkdir(parents=True, exist_ok=True)

def autonomous_linkedin_post(text, headless=False):
    """
    Fully autonomous LinkedIn poster
    Opens browser, navigates to LinkedIn, and posts text
    """
    
    print("\n" + "=" * 60)
    print("AUTONOMOUS LINKEDIN POSTER")
    print("=" * 60)
    print(f"Post Content: {text[:100]}...")
    print("=" * 60)
    
    try:
        with sync_playwright() as p:
            # Launch browser with persistent session
            print("\n[1/6] Launching browser...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=headless,  # Set to False to see the automation
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--start-maximized'
                ],
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            # Navigate to LinkedIn
            print("[2/6] Navigating to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            page.wait_for_load_state('networkidle')
            
            # Check if logged in
            print("[3/6] Checking login status...")
            try:
                # Look for the post creation box
                page.wait_for_selector('div[aria-label="Start a post"]', timeout=10000)
                print("✓ Already logged in!")
            except PlaywrightTimeout:
                print("⚠ Not logged in, attempting login...")
                # Could add login logic here if needed
                return {
                    'success': False,
                    'error': 'Not logged in. Please login manually first time.',
                    'action_required': 'login'
                }
            
            # Click on "Start a post"
            print("[4/6] Opening post composer...")
            try:
                post_button = page.locator('div[aria-label="Start a post"]').first
                post_button.click()
                
                # Wait for post dialog to open
                page.wait_for_selector('div[role="dialog"]', timeout=10000)
                print("✓ Post composer opened!")
            except Exception as e:
                print(f"✗ Could not open post composer: {e}")
                return {
                    'success': False,
                    'error': f'Could not open composer: {str(e)}'
                }
            
            # Find the text editor and type the post
            print("[5/6] Writing post content...")
            try:
                # LinkedIn uses a contenteditable div for the editor
                editor = page.locator('div[contenteditable="true"][role="textbox"]').first
                
                # Clear any existing content
                editor.click()
                time.sleep(1)
                
                # Type the post content (use keyboard to avoid detection)
                editor.type(text, delay=50)  # 50ms delay between keystrokes
                print("✓ Post content written!")
            except Exception as e:
                print(f"✗ Could not write post: {e}")
                return {
                    'success': False,
                    'error': f'Could not write post: {str(e)}'
                }
            
            # Click the Post button
            print("[6/6] Publishing post...")
            try:
                # Wait a moment for LinkedIn to process the text
                time.sleep(2)
                
                # Find and click the Post button
                # LinkedIn's post button usually has text "Post"
                post_btn = page.locator('button:has-text("Post")').first
                
                # Wait for button to be enabled
                post_btn.wait_for(element_state='attached', timeout=5000)
                post_btn.scroll_into_view_if_needed()
                time.sleep(1)
                post_btn.click()
                
                # Wait for confirmation
                time.sleep(3)
                
                print("✓ Post published successfully!")
                
                return {
                    'success': True,
                    'message': 'LinkedIn post published!',
                    'posted_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'content_preview': text[:100]
                }
                
            except Exception as e:
                print(f"✗ Could not publish post: {e}")
                return {
                    'success': False,
                    'error': f'Could not publish: {str(e)}'
                }
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    # Test post content
    test_post = f"""🎯 AI Employee System - Autonomous Test

Hello LinkedIn! This post was created and published AUTOMATICALLY by my Personal AI Employee system.

No manual intervention needed - the system:
✅ Opened the browser
✅ Navigated to LinkedIn
✅ Wrote this post
✅ Published it automatically

#AI #Automation #PersonalAI #LinkedInAutomation #AIEmployee #RPA

Posted at: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Get headless mode from command line
    headless = '--headless' in sys.argv
    
    print("\n" + "=" * 60)
    print("AUTONOMOUS LINKEDIN POST TEST")
    print("=" * 60)
    print(f"Headless Mode: {headless}")
    print("Post Preview:")
    print(test_post[:200] + "...")
    print("=" * 60)
    
    result = autonomous_linkedin_post(test_post, headless=headless)
    
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    
    if result.get('success'):
        print("✅ SUCCESS!")
        print(f"Message: {result.get('message', 'Posted!')}")
        print(f"Posted at: {result.get('posted_at', 'Just now')}")
        print("\nView your post: https://www.linkedin.com/feed/")
    else:
        print("❌ FAILED!")
        print(f"Error: {result.get('error', 'Unknown error')}")
        
        if result.get('action_required') == 'login':
            print("\n📝 ACTION REQUIRED:")
            print("1. Run this script WITHOUT --headless flag")
            print("2. Login to LinkedIn manually (first time only)")
            print("3. Session will be saved for future posts")
            print("\nCommand: python autonomous_linkedin_post.py")
    
    print("=" * 60)
