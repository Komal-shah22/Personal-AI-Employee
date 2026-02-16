"""
WhatsApp Watcher for Personal AI Employee

IMPORTANT DISCLAIMER:
This script is intended for personal use only to monitor your own WhatsApp account.
Users are responsible for ensuring compliance with WhatsApp's Terms of Service.
Automated access to WhatsApp Web may violate their ToS. Use at your own risk.
This tool is provided for educational and personal productivity purposes only.

Monitors WhatsApp Web for new messages with specific keywords and creates action items.
Uses Playwright for browser automation with persistent session.
"""

import time
import logging
from pathlib import Path
from datetime import datetime
import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# Configure logging
LOG_DIR = Path('AI_Employee_Vault/Logs')
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'whatsapp_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WhatsAppWatcher:
    """
    Monitor WhatsApp Web for urgent messages and create action items.

    DISCLAIMER: This tool automates WhatsApp Web access. Users must ensure
    compliance with WhatsApp's Terms of Service. Use at your own risk.
    """

    def __init__(self, check_interval=30):
        self.check_interval = check_interval
        self.needs_action_dir = Path('AI_Employee_Vault/Needs_Action')
        self.session_path = Path('sessions/whatsapp')
        self.processed_file = Path('.whatsapp_processed.json')

        # Keywords to filter for urgent messages (as specified)
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'quote', 'bill']

        # Load processed messages from file
        self.processed_messages = self.load_processed_messages()

        # Ensure directories exist
        self.needs_action_dir.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)

        logger.info("WhatsApp Watcher initialized")
        logger.info(f"Session path: {self.session_path.absolute()}")
        logger.info(f"Monitoring keywords: {', '.join(self.keywords)}")
        logger.info(f"Check interval: {self.check_interval} seconds")

    def load_processed_messages(self) -> set:
        """Load previously processed message IDs from JSON file"""
        if self.processed_file.exists():
            try:
                with open(self.processed_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_ids', []))
            except Exception as e:
                logger.error(f"Error loading processed messages: {e}")
                return set()
        return set()

    def save_processed_messages(self):
        """Save processed message IDs to JSON file"""
        try:
            with open(self.processed_file, 'w') as f:
                json.dump({
                    'processed_ids': list(self.processed_messages),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving processed messages: {e}")

    def check_for_updates(self):
        """
        Check WhatsApp Web for new unread messages containing keywords.
        Returns list of messages that match the filter criteria.

        Implements browser crash recovery: waits 30 seconds and restarts on failure.
        """
        messages = []
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                with sync_playwright() as p:
                    # Launch browser with persistent context to save login session
                    logger.info("Launching browser with persistent session...")
                    browser = p.chromium.launch_persistent_context(
                        user_data_dir=str(self.session_path.absolute()),
                        headless=False,  # Set to True for production
                        args=[
                            '--no-sandbox',
                            '--disable-setuid-sandbox',
                            '--disable-blink-features=AutomationControlled',
                            '--disable-dev-shm-usage'
                        ],
                        viewport={'width': 1280, 'height': 720},
                        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    )

                    # Get or create page
                    page = browser.pages[0] if browser.pages else browser.new_page()

                    # Navigate to WhatsApp Web
                    logger.info("Navigating to WhatsApp Web...")
                    page.goto('https://web.whatsapp.com', wait_until='networkidle', timeout=30000)

                    # Wait for chat list to load (max 10 seconds as specified)
                    logger.info("Waiting for chat list to load (max 10 seconds)...")

                    try:
                        # Try multiple selectors
                        selectors = [
                            '[data-testid="chat-list"]',
                            '#side',
                            'canvas[aria-label="Scan me!"]'  # QR code if not logged in
                        ]

                        loaded = False
                        for selector in selectors:
                            try:
                                page.wait_for_selector(selector, timeout=10000)
                                logger.info(f"Found element: {selector}")
                                loaded = True
                                break
                            except PlaywrightTimeout:
                                continue

                        if not loaded:
                            logger.error("Could not find WhatsApp Web elements")
                            browser.close()
                            return messages

                        # Check if QR code is present (not logged in)
                        qr_code = page.query_selector('canvas[aria-label="Scan me!"]')
                        if qr_code:
                            logger.warning("=" * 60)
                            logger.warning("QR CODE DETECTED - Please scan to log in!")
                            logger.warning("Browser will stay open for 120 seconds...")
                            logger.warning("=" * 60)

                            # Wait for user to scan
                            for i in range(120, 0, -10):
                                logger.info(f"⏳ {i} seconds remaining...")
                                time.sleep(10)

                                if page.query_selector('[data-testid="chat-list"]'):
                                    logger.info("Successfully logged in!")
                                    break
                            else:
                                logger.warning("QR code scan timeout")
                                browser.close()
                                return messages

                    except PlaywrightTimeout:
                        logger.error("Timeout waiting for WhatsApp Web to load")
                        browser.close()
                        return messages

                    # Wait for chat list to stabilize
                    time.sleep(3)

                    # Find all unread chats
                    logger.info("Scanning for unread messages...")
                    unread_chats = []

                    # Try different selectors for unread indicators
                    unread_selectors = [
                        '[aria-label*="unread message"]',
                        'span[data-testid="icon-unread-count"]',
                        'div[aria-label*="unread"]'
                    ]

                    for selector in unread_selectors:
                        try:
                            found = page.query_selector_all(selector)
                            if found:
                                logger.info(f"Found {len(found)} unread indicators")
                                # Get parent chat containers
                                for elem in found:
                                    parent = elem.evaluate_handle(
                                        'el => el.closest("[data-testid=\\"cell-frame-container\\"]") || el.closest("div[role=\\"listitem\\"]")'
                                    )
                                    if parent:
                                        unread_chats.append(parent.as_element())
                                if unread_chats:
                                    break
                        except Exception as e:
                            logger.debug(f"Selector {selector} failed: {e}")
                            continue

                    if not unread_chats:
                        logger.info("No unread messages found")
                        browser.close()
                        return messages

                    logger.info(f"Found {len(unread_chats)} unread chat(s)")

                    # Process each unread chat
                    for idx, chat_element in enumerate(unread_chats[:10], 1):
                        try:
                            logger.info(f"Processing chat {idx}/{min(len(unread_chats), 10)}...")

                            # Get sender name
                            sender_name = "Unknown"
                            name_selectors = [
                                '[data-testid="cell-frame-title"]',
                                'span[title]',
                                'div._21S-L span'
                            ]

                            for selector in name_selectors:
                                try:
                                    elem = chat_element.query_selector(selector)
                                    if elem:
                                        sender_name = elem.inner_text()
                                        break
                                except:
                                    continue

                            # Get message text
                            message_text = ""
                            text_selectors = [
                                '[data-testid="last-msg-text"]',
                                'span[title]',
                                'div._1VfKB span'
                            ]

                            for selector in text_selectors:
                                try:
                                    elem = chat_element.query_selector(selector)
                                    if elem:
                                        message_text = elem.inner_text()
                                        break
                                except:
                                    continue

                            # Get timestamp (current time as fallback)
                            timestamp = datetime.now().isoformat()

                            logger.debug(f"Sender: {sender_name}, Message: {message_text[:50]}")

                            # Filter messages with keywords
                            message_lower = message_text.lower()
                            matched_keywords = [kw for kw in self.keywords if kw in message_lower]

                            if matched_keywords:
                                # Create unique message ID
                                message_id = f"{sender_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if message_id not in self.processed_messages:
                                    logger.info(f"✓ Found urgent message from {sender_name}")
                                    logger.info(f"  Keywords: {', '.join(matched_keywords)}")
                                    logger.info(f"  Preview: {message_text[:50]}...")

                                    messages.append({
                                        'id': message_id,
                                        'from': sender_name,
                                        'message_text': message_text,
                                        'message_preview': message_text[:200],
                                        'keywords_matched': matched_keywords,
                                        'timestamp': timestamp,
                                        'priority': 'high'
                                    })

                        except Exception as e:
                            logger.error(f"Error processing chat {idx}: {e}")
                            continue

                    # Close browser
                    browser.close()
                    logger.info(f"Scan complete. Found {len(messages)} urgent message(s)")

                    # Successfully completed, break retry loop
                    break

            except Exception as e:
                retry_count += 1
                logger.error(f"Browser crash or error (attempt {retry_count}/{max_retries}): {e}")

                if retry_count < max_retries:
                    logger.info("Waiting 30 seconds before restarting browser session...")
                    time.sleep(30)
                else:
                    logger.error("Max retries reached. Giving up for this cycle.")

        return messages

    def create_action_item(self, message):
        """
        Create a Markdown file in Needs_Action folder for a WhatsApp message.

        Format:
        - Filename: WHATSAPP_[timestamp]_[sender].md
        - YAML frontmatter: type, from, message_preview, keywords_matched, priority
        - Body: full message text, suggested actions checklist
        """
        try:
            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_sender = message['from'].replace(' ', '_').replace('/', '_')[:50]
            filename = f"WHATSAPP_{timestamp}_{safe_sender}.md"
            filepath = self.needs_action_dir / filename

            # Create content with YAML frontmatter
            content = f"""---
type: whatsapp
from: {message['from']}
message_preview: {message['message_preview']}
keywords_matched: {', '.join(message['keywords_matched'])}
priority: {message['priority']}
received: {message['timestamp']}
status: pending
---

# WhatsApp Message from {message['from']}

## Message Details
- **From**: {message['from']}
- **Received**: {message['timestamp']}
- **Priority**: {message['priority'].upper()}
- **Matched Keywords**: {', '.join(message['keywords_matched'])}

## Full Message
{message['message_text']}

## Suggested Actions
- [ ] Review full conversation in WhatsApp
- [ ] Determine urgency and required response
- [ ] Draft appropriate reply
- [ ] Get approval if needed (payments, commitments, quotes)
- [ ] Send response via WhatsApp
- [ ] Mark as complete and archive

## Notes
This message was flagged because it contains urgent keywords: {', '.join(message['keywords_matched'])}

---
*Detected by WhatsApp Watcher at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"Created action item: {filename}")

            # Mark as processed and save
            self.processed_messages.add(message['id'])
            self.save_processed_messages()

            return filepath

        except Exception as e:
            logger.error(f"Error creating action item: {e}")
            return None

    def run(self):
        """Main execution loop"""
        logger.info("=" * 60)
        logger.info("WhatsApp Watcher Started")
        logger.info("=" * 60)
        logger.info(f"Check interval: {self.check_interval} seconds")
        logger.info(f"Monitoring keywords: {', '.join(self.keywords)}")
        logger.info(f"Action items: {self.needs_action_dir.absolute()}")
        logger.info("")
        logger.info("FIRST RUN: Browser will open. Scan QR code if needed.")
        logger.info("Session will be saved for future runs.")
        logger.info("")
        logger.info("DISCLAIMER: Ensure compliance with WhatsApp ToS.")
        logger.info("=" * 60)

        iteration = 0

        while True:
            try:
                iteration += 1
                logger.info(f"\n--- Check #{iteration} at {datetime.now().strftime('%H:%M:%S')} ---")

                # Check for new messages
                messages = self.check_for_updates()

                # Create action items for each urgent message
                for message in messages:
                    self.create_action_item(message)

                if messages:
                    logger.info(f"✓ Processed {len(messages)} urgent message(s)")
                else:
                    logger.info("No urgent messages found")

                # Wait before next check
                logger.info(f"Waiting {self.check_interval} seconds until next check...")
                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("\n" + "=" * 60)
                logger.info("WhatsApp Watcher stopped by user")
                logger.info("=" * 60)
                break

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                logger.info("Waiting 30 seconds before retry...")
                time.sleep(30)


if __name__ == "__main__":
    watcher = WhatsAppWatcher(check_interval=30)
    watcher.run()
