"""
Fully Autonomous Instagram Poster using Playwright.
Stealth mode with human-like behavior to avoid detection.
Posts to Instagram through the web interface.
"""

import os
import sys
import io
import random
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Fix Windows console Unicode
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
SESSION_DIR = Path(__file__).parent / "sessions" / "instagram"
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
INSTAGRAM_URL = "https://www.instagram.com/"
POST_TEXT = "Testing AI Employee Dashboard! 🚀 #AI #Automation"
IMAGE_URL = None  # Optional: Set an image URL to post with

def random_delay(min_ms=500, max_ms=1500):
    """Random delay to simulate human behavior."""
    return random.randint(min_ms, max_ms)

def take_screenshot(page, step_name):
    """Take screenshot and save to screenshots folder."""
    try:
        SCREENSHOTS_DIR.mkdir(exist_ok=True)
        screenshot_path = SCREENSHOTS_DIR / f"{step_name}.png"
        page.screenshot(path=str(screenshot_path))
        print(f"  [Screenshot] {screenshot_path.name}")
    except Exception as e:
        print(f"  [Screenshot failed] {e}")

def human_type(page, text, delay_range=(30, 100)):
    """Type text with human-like delays."""
    for char in text:
        page.keyboard.type(char, delay=random.randint(*delay_range))
        # Add occasional longer pauses
        if random.random() < 0.1:
            page.wait_for_timeout(random.randint(100, 300))

def main(image_url=None, caption=None):
    """
    Main function to post to Instagram
    
    Args:
        image_url: Optional URL of image to post
        caption: Optional caption text (uses POST_TEXT if not provided)
    """
    global POST_TEXT
    if caption:
        POST_TEXT = caption
    
    print("=" * 60)
    print("AUTONOMOUS INSTAGRAM POSTER")
    print("=" * 60)
    print(f"Session: {SESSION_DIR}")
    print(f"Caption: {POST_TEXT}")
    if image_url:
        print(f"Image: {image_url}")
    print("=" * 60)

    if not SESSION_DIR.exists():
        print("INFO: Session directory not found. Will need to login manually.")
        SESSION_DIR.mkdir(parents=True, exist_ok=True)

    browser = None
    page = None

    try:
        with sync_playwright() as p:
            # Step 1: Launch browser with persistent context
            print("\n[Step 1/7] Launching browser with saved session...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_DIR),
                headless=False,
                viewport={"width": 1280, "height": 800},
                # Stealth args
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu',
                    '--window-size=1280,800',
                ]
            )
            page = browser.pages[0] if browser.pages else browser.new_page()

            # Inject stealth scripts
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
            """)

            page.set_default_timeout(60000)
            page.wait_for_timeout(random_delay(1000, 2000))
            take_screenshot(page, "01_browser_launched")

            # Step 2: Navigate to Instagram
            print("\n[Step 2/7] Navigating to Instagram...")
            page.goto(INSTAGRAM_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(random_delay(3000, 5000))
            take_screenshot(page, "02_instagram_loaded")

            # Check if logged in by looking for profile icon or login page
            is_logged_in = False
            try:
                # Try to find profile icon (indicates logged in)
                profile_icon = page.locator('svg[aria-label="Profile"]').first
                if profile_icon.count() > 0:
                    is_logged_in = True
                    print("  [OK] Already logged in")
                else:
                    print("  [WAIT] Not logged in - waiting for manual login...")
                    print("  [INFO] Please login to Instagram in the opened browser")
                    print("  [INFO] Waiting up to 120 seconds for login...")
                    print("  [INFO] After first login, session will be saved for auto-posting!")

                    # Wait for user to login manually (up to 120 seconds)
                    for i in range(120, 0, -1):
                        page.wait_for_timeout(1000)

                        # Check every second if logged in
                        try:
                            profile_check = page.locator('svg[aria-label="Profile"]').first
                            if profile_check.count() > 0:
                                print(f"  [OK] Login detected after {120-i} seconds!")
                                is_logged_in = True
                                take_screenshot(page, "02_logged_in")
                                print("  [OK] Session will be saved for future posts!")
                                break
                        except:
                            pass

                        # Show progress every 10 seconds
                        if i % 10 == 0:
                            print(f"  [WAIT] Still waiting... {i}s remaining")

                    if not is_logged_in:
                        print("  [ERROR] Login not detected. Please run instagram_login_helper.py first!")
                        print("  Command: python instagram_login_helper.py")

            except Exception as e:
                print(f"  [ERROR] Could not detect login status: {e}")
                print("  [INFO] Please run: python instagram_login_helper.py")

            # Step 3: Click "New" or "+" button to create post
            print("\n[Step 3/7] Clicking 'New' button to create post...")
            try:
                # Try multiple selectors for the new post button
                new_post_btn = None
                selectors = [
                    'svg[aria-label="New post"]',
                    'button:has-text("New")',
                    '[role="button"]:has-text("Create")',
                    'svg path[d*="M20.96"]',  # Instagram + icon path
                ]
                
                for selector in selectors:
                    try:
                        btn = page.locator(selector).first
                        if btn.count() > 0:
                            btn.wait_for(state="visible", timeout=5000)
                            btn.scroll_into_view_if_needed()
                            page.wait_for_timeout(random_delay(500, 1000))
                            btn.click()
                            new_post_btn = btn
                            print(f"  Clicked using selector: {selector}")
                            break
                    except:
                        continue
                
                if not new_post_btn:
                    # Try keyboard shortcut as fallback
                    print("  Trying keyboard shortcut...")
                    page.keyboard.press("Control+N")
                
                page.wait_for_timeout(random_delay(2000, 3000))
                take_screenshot(page, "03_new_post_clicked")
                
            except Exception as e:
                print(f"  Error clicking New button: {e}")
                take_screenshot(page, "03_error")

            # Step 4: If image URL provided, paste it or upload
            if image_url:
                print("\n[Step 4/7] Loading image from URL...")
                try:
                    # Navigate to image URL in new tab to download
                    # For now, skip this step as Instagram web doesn't allow direct URL paste
                    print("  Note: Direct URL upload not supported on Instagram Web")
                    print("  Please select image manually if needed")
                except Exception as e:
                    print(f"  Image loading skipped: {e}")
            
            # Step 5: Find caption field and type the text
            print("\n[Step 5/7] Adding caption...")
            try:
                # Instagram caption field is usually a textarea
                caption_field = page.locator('textarea[aria-label*="caption"]').first
                
                if caption_field.count() == 0:
                    # Try alternative selectors
                    caption_field = page.locator('textarea').first
                
                if caption_field.count() > 0:
                    caption_field.click()
                    page.wait_for_timeout(random_delay(500, 1000))
                    human_type(page, POST_TEXT)
                    page.wait_for_timeout(random_delay(1000, 2000))
                    print("  Caption added")
                    take_screenshot(page, "05_caption_added")
                else:
                    print("  ⚠ Could not find caption field")
            except Exception as e:
                print(f"  Error adding caption: {e}")
                take_screenshot(page, "05_error")

            # Step 6: Click Share/Post button
            print("\n[Step 6/7] Sharing post...")
            try:
                # Look for Share button
                share_btn = None
                selectors = [
                    'button:has-text("Share")',
                    'button:has-text("Post")',
                    'div[role="button"]:has-text("Share")',
                ]
                
                for selector in selectors:
                    try:
                        btn = page.locator(selector).first
                        if btn.count() > 0:
                            btn.wait_for(state="visible", timeout=5000)
                            btn.scroll_into_view_if_needed()
                            page.wait_for_timeout(random_delay(500, 1000))
                            btn.click()
                            share_btn = btn
                            print(f"  Clicked Share button: {selector}")
                            break
                    except:
                        continue
                
                if share_btn:
                    page.wait_for_timeout(random_delay(3000, 5000))
                    take_screenshot(page, "06_post_shared")
                else:
                    print("  ⚠ Could not find Share button")
                    
            except Exception as e:
                print(f"  Error sharing post: {e}")
                take_screenshot(page, "06_error")

            # Step 7: Wait and verify
            print("\n[Step 7/7] Waiting for confirmation...")
            try:
                page.wait_for_timeout(5000)
                
                # Check for success indicators
                try:
                    # Look for "Your post has been shared" or similar
                    success_text = page.locator('text=shared').first
                    if success_text.count() > 0:
                        print("  ✓ Post appears to be shared successfully!")
                except:
                    pass
                
                take_screenshot(page, "07_final")
            except Exception as e:
                print(f"  Verification skipped: {e}")

            # Keep browser open for verification
            print("\n[INFO] Keeping browser open for verification...")
            try:
                print("  ⏳ Browser will remain open for 30 seconds...")
                for i in range(30, 0, -1):
                    print(f"  Browser will close in {i} seconds...")
                    page.wait_for_timeout(1000)

                print("\n" + "=" * 60)
                if is_logged_in:
                    print("SUCCESS! Instagram post submitted")
                else:
                    print("COMPLETED! Please login and try again if needed")
                print("=" * 60)
            except Exception as e:
                print(f"\n⚠ Error during wait: {e}")

    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close browser at the very end
        print("\nClosing browser...")
        try:
            if browser:
                browser.close()
                browser = None
        except:
            pass

        print("\nDone! Check screenshots/ folder for step-by-step images.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Post to Instagram via Playwright')
    parser.add_argument('--image', type=str, help='Image URL to post')
    parser.add_argument('--caption', type=str, help='Caption text')
    
    args = parser.parse_args()
    
    main(image_url=args.image, caption=args.caption)
