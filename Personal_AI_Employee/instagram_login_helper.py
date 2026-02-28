"""
Instagram Session Login Helper
Opens Instagram and waits for you to login, then saves the session.
Run this ONCE to save your login credentials for future use.
"""

import sys
import io
from pathlib import Path
from playwright.sync_api import sync_playwright

# Fix Windows console Unicode
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
SESSION_DIR = Path(__file__).parent / "sessions" / "instagram"
INSTAGRAM_URL = "https://www.instagram.com/"

def main():
    print("=" * 60)
    print("INSTAGRAM SESSION LOGIN HELPER")
    print("=" * 60)
    print()
    print("This will open Instagram and wait for you to login.")
    print("Once logged in, the session will be saved for future use.")
    print()
    print("Instructions:")
    print("1. Browser will open in 3 seconds")
    print("2. Login to Instagram normally")
    print("3. Wait for 'Session saved!' message")
    print("4. Browser will close automatically")
    print()
    print("Press Ctrl+C at any time to cancel")
    print("=" * 60)
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"Opening in {i}...")
        import time
        time.sleep(1)
    
    # Create session directory
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nSession directory: {SESSION_DIR}")
    print()
    
    browser = None
    
    try:
        with sync_playwright() as p:
            # Launch browser with persistent context
            print("Launching browser...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=False,
                viewport={"width": 1280, "height": 800},
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                ]
            )
            
            page = browser.pages[0] if browser.pages else browser.new_page()
            
            # Navigate to Instagram
            print("Navigating to Instagram...")
            page.goto(INSTAGRAM_URL, wait_until="domcontentloaded")
            
            print()
            print("=" * 60)
            print("LOGIN INSTRUCTIONS:")
            print("=" * 60)
            print("[OK] Enter your username/email and password")
            print("[OK] Complete 2FA if enabled")
            print("[OK] Wait until you see your Instagram feed")
            print("[OK] Script will auto-detect login and save session")
            print()
            print("Waiting for login... (press Ctrl+C to cancel)")
            print("=" * 60)
            print()
            
            # Wait for login (up to 5 minutes)
            logged_in = False
            wait_time = 0
            max_wait = 300  # 5 minutes
            
            while wait_time < max_wait:
                page.wait_for_timeout(1000)
                wait_time += 1
                
                # Check if logged in by looking for profile icon or feed
                try:
                    # Method 1: Check for profile icon
                    profile = page.locator('svg[aria-label="Profile"]').first
                    if profile.count() > 0:
                        logged_in = True
                        break
                    
                    # Method 2: Check for "Create" button (only visible when logged in)
                    create_btn = page.locator('svg[aria-label="New post"]').first
                    if create_btn.count() > 0:
                        logged_in = True
                        break
                    
                    # Method 3: Check URL (should not have login in it)
                    if "login" not in page.url.lower() and "instagram.com" in page.url:
                        # Method 4: Check for feed content
                        feed = page.locator('main').first
                        if feed.count() > 0:
                            logged_in = True
                            break
                            
                except:
                    pass
                
                # Show progress every 10 seconds
                if wait_time % 10 == 0:
                    print(f"  Still waiting... ({wait_time}s)")
            
            if logged_in:
                print()
                print("=" * 60)
                print(f"[SUCCESS] LOGIN DETECTED after {wait_time} seconds!")
                print("=" * 60)
                print()
                print("Saving session...")

                # Wait a bit for cookies to settle
                page.wait_for_timeout(3000)

                # Take screenshot
                screenshot_path = Path(__file__).parent / "screenshots" / "instagram_login_success.png"
                screenshot_path.parent.mkdir(exist_ok=True)
                page.screenshot(path=str(screenshot_path))
                print(f"Screenshot saved: {screenshot_path}")

                print()
                print("[SUCCESS] Session saved successfully!")
                print()
                print("You can now use:")
                print("  - python playwright_instagram_post.py --caption 'Your caption'")
                print("  - Dashboard Instagram form at http://localhost:3000")
                print()
                print("Session will remain valid for weeks/months.")
                print("To logout/delete session, delete the folder:")
                print(f"  {SESSION_DIR}")
                print()

                # Keep browser open for 5 more seconds
                for i in range(5, 0, -1):
                    page.wait_for_timeout(1000)
                    print(f"Closing in {i}...")
                    
            else:
                print()
                print("=" * 60)
                print("⚠ Login not detected within 5 minutes")
                print("=" * 60)
                print()
                print("Session NOT saved. Please try again.")
                print("Make sure to:")
                print("  1. Enter correct username/password")
                print("  2. Complete any 2FA verification")
                print("  3. Wait until you see your feed")
                print()
                
                # Keep browser open for user to see
                print("Browser will close in 10 seconds...")
                for i in range(10, 0, -1):
                    page.wait_for_timeout(1000)
                    print(f"  {i}")
    
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if browser:
            try:
                print("\nClosing browser...")
                browser.close()
                print("Done!")
            except:
                pass  # Browser already closed


if __name__ == "__main__":
    main()
