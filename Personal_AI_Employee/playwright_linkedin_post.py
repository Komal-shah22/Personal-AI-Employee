"""
Fully Autonomous LinkedIn Poster using Playwright.
Stealth mode with human-like behavior to avoid detection.
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
SESSION_DIR = Path(__file__).parent / "sessions" / "linkedin"
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
LINKEDIN_URL = "https://www.linkedin.com/feed/"
POST_TEXT = "Testing AI Employee Dashboard! 🚀 #AI #Automation"

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

def main():
    print("=" * 60)
    print("AUTONOMOUS LINKEDIN POSTER")
    print("=" * 60)
    print(f"Session: {SESSION_DIR}")
    print(f"Post: {POST_TEXT}")
    print("=" * 60)

    if not SESSION_DIR.exists():
        print("ERROR: Session directory not found. Please log in manually first.")
        sys.exit(1)

    browser = None
    page = None
    
    try:
        with sync_playwright() as p:
            # Step 1: Launch browser with persistent context
            print("\n[Step 1/6] Launching browser with saved session...")
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

            # Step 2: Navigate to LinkedIn feed
            print("\n[Step 2/6] Navigating to LinkedIn feed...")
            page.goto(LINKEDIN_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(random_delay(3000, 5000))
            take_screenshot(page, "02_linkedin_loaded")

            # Check if logged in
            is_logged_in = False
            try:
                # Try to find the "Start a post" button (indicates logged in)
                start_post_btn = page.locator('button:has-text("Start a post")').first
                if start_post_btn.count() > 0:
                    is_logged_in = True
                    print("  ✓ Already logged in")
                else:
                    # Check for login page
                    if "login" in page.url.lower() or "checkpoint" in page.url.lower():
                        print("  ⚠ Login page detected - waiting for manual login...")
                        print("  💡 Please login to LinkedIn in the opened browser")
                        print("  ⏳ Waiting up to 60 seconds for login...")

                        # Wait for user to login manually (up to 60 seconds)
                        for i in range(60, 0, -1):
                            page.wait_for_timeout(1000)

                            # Check every second if logged in
                            try:
                                btn_check = page.locator('button:has-text("Start a post")').first
                                if btn_check.count() > 0:
                                    print(f"  ✓ Login detected after {60-i} seconds!")
                                    is_logged_in = True
                                    take_screenshot(page, "02_logged_in")
                                    break
                            except:
                                pass

                            # Show progress every 10 seconds
                            if i % 10 == 0:
                                print(f"  ⏳ Still waiting... {i}s remaining")

                        if not is_logged_in:
                            print("  ⚠ Login not detected. Continuing anyway...")
                    else:
                        print("  ⚠ Could not detect login status")
            except Exception as e:
                print(f"  ⚠ Error checking login status: {e}")

            # Step 3: Click "Start a post" button
            print("\n[Step 3/6] Clicking 'Start a post' button...")
            composer = None
            try:
                start_post_btn = page.locator('button:has-text("Start a post")').first
                start_post_btn.wait_for(state="visible", timeout=10000)
                start_post_btn.scroll_into_view_if_needed()
                page.wait_for_timeout(random_delay(500, 1000))
                start_post_btn.click()
                print("  Clicked 'Start a post' button")
                page.wait_for_timeout(random_delay(1500, 2500))
                take_screenshot(page, "03_post_clicked")

                # Find composer
                composer = page.locator('div[contenteditable="true"][role="textbox"]').first
                if composer.count() == 0:
                    composer = page.locator('div[contenteditable]').first
            except Exception as e:
                print(f"  Error: {e}")
                take_screenshot(page, "03_error")

            if not composer or composer.count() == 0:
                print("ERROR: Could not find post composer")
                take_screenshot(page, "03_composer_error")
                page.wait_for_timeout(10000)
                if browser:
                    browser.close()
                sys.exit(1)

            # Step 4: Type the post content
            print("\n[Step 4/6] Typing post content...")
            try:
                composer.click()
                page.wait_for_timeout(random_delay(500, 1000))
                human_type(page, POST_TEXT)
                page.wait_for_timeout(random_delay(1500, 2500))
                take_screenshot(page, "04_text_typed")
            except Exception as e:
                print(f"  Error typing: {e}")
                take_screenshot(page, "04_error")

            # Step 5: Submit post using keyboard only (most reliable)
            print("\n[Step 5/6] Submitting post...")
            
            # Wait before attempting to post
            page.wait_for_timeout(random_delay(2000, 3000))
            
            # Method: Use Ctrl+Enter (LinkedIn native shortcut)
            try:
                print("  Using Ctrl+Enter shortcut...")
                # Make sure composer is focused
                composer.click()
                page.wait_for_timeout(random_delay(300, 500))
                
                # Press Ctrl+Enter to submit
                page.keyboard.press("Control+Enter")
                print("  Pressed Ctrl+Enter")
                
                # Wait for submission
                page.wait_for_timeout(random_delay(3000, 5000))
                take_screenshot(page, "05_ctrl_enter")
                
            except Exception as e:
                print(f"  Ctrl+Enter failed: {e}")
                take_screenshot(page, "05_error")
                
                # Fallback: Tab + Enter
                try:
                    print("  Trying Tab + Enter fallback...")
                    composer.click()
                    page.wait_for_timeout(500)
                    
                    # Tab to Post button
                    for i in range(8):
                        page.keyboard.press("Tab")
                        page.wait_for_timeout(200)
                    
                    page.keyboard.press("Enter")
                    print("  Pressed Tab + Enter")
                    page.wait_for_timeout(3000)
                    take_screenshot(page, "05_tab_enter")
                except Exception as e2:
                    print(f"  Tab+Enter also failed: {e2}")

            # Wait for post to complete
            print("  Waiting for post to submit...")
            try:
                page.wait_for_timeout(5000)
            except:
                pass

            try:
                take_screenshot(page, "06_final")
            except Exception as e:
                print(f"  Final screenshot failed: {e}")

            # Step 6: Keep browser open for verification
            print("\n[Step 6/6] Keeping browser open for verification...")
            try:
                print("  ⏳ Browser will remain open for 30 seconds...")
                for i in range(30, 0, -1):
                    print(f"  Browser will close in {i} seconds...")
                    page.wait_for_timeout(1000)
                
                # Check URL
                try:
                    current_url = page.url
                    if "linkedin.com/feed" in current_url:
                        print("\n" + "=" * 60)
                        print("SUCCESS! Post submitted to LinkedIn")
                        print("=" * 60)
                    else:
                        print(f"\n⚠ Current page: {current_url}")
                except:
                    print("\n⚠ Could not verify URL")
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
            pass  # Browser already closed

        print("\nDone! Check screenshots/ folder for step-by-step images.")


if __name__ == "__main__":
    main()
