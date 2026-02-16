# WhatsApp Web Watcher - Troubleshooting Guide

## Quick Start

### Step 1: Test Your Connection
```bash
python test_whatsapp_connection.py
```

This will:
- Launch Chromium browser
- Navigate to WhatsApp Web
- Test all selectors
- Save a screenshot for debugging
- Give you 120 seconds to scan QR code if needed

### Step 2: Run the Watcher
```bash
python watchers/whatsapp_watcher.py
```

---

## What Was Fixed

### 1. **Improved Timeout Handling**
- Increased navigation timeout from 60s to 90s
- Changed wait strategy to `networkidle` for better reliability
- Added 5-second buffer after page load for dynamic content

### 2. **Multiple Selector Fallbacks**
The script now tries multiple selectors to detect WhatsApp Web:
- `canvas[aria-label="Scan me!"]` - QR code
- `[data-testid="chat-list"]` - Chat list
- `div[data-testid="default-user"]` - User profile
- `#side` - Sidebar element
- `div[role="textbox"]` - Search box

### 3. **Better Browser Configuration**
Added critical browser arguments:
```python
args=[
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-blink-features=AutomationControlled',  # Prevents detection
    '--disable-dev-shm-usage'  # Prevents memory issues
]
```

### 4. **Proper Viewport and User Agent**
- Set viewport to 1280x720 (standard desktop size)
- Added realistic Chrome user agent to avoid blocking

### 5. **Debug Screenshots**
Automatically saves screenshots to `sessions/whatsapp/debug_screenshot.png` for troubleshooting

### 6. **Extended QR Code Scan Time**
- Increased from 60s to 120s
- Shows countdown timer every 10 seconds
- Checks for successful login during wait period

### 7. **Better Unread Message Detection**
Now tries multiple selectors for unread chats:
- `[aria-label*="unread message"]`
- `span[data-testid="icon-unread-count"]`
- `div[aria-label*="unread"]`

---

## Common Issues & Solutions

### Issue 1: "Timeout waiting for WhatsApp Web to load"

**Solution:**
1. Run the test script first: `python test_whatsapp_connection.py`
2. Check the screenshot at `sessions/whatsapp/test_screenshot.png`
3. Verify your internet connection
4. Make sure WhatsApp Web is not blocked by firewall

### Issue 2: QR Code Not Appearing

**Possible causes:**
- Page still loading (wait longer)
- Already logged in (check screenshot)
- WhatsApp Web changed their interface

**Solution:**
- The script now waits 10 seconds after navigation
- Check the debug screenshot to see what's actually displayed
- Try clearing the session: delete `sessions/whatsapp` folder and restart

### Issue 3: Browser Closes Immediately

**Solution:**
- Check the logs in `AI_Employee_Vault/Logs/whatsapp_watcher.log`
- Run test script to see detailed error messages
- Verify Playwright is installed: `playwright install chromium`

### Issue 4: "No unread messages found" (but you have unread messages)

**Solution:**
- WhatsApp may have changed their HTML structure
- Check the screenshot to see if chats are visible
- The script now tries multiple selectors automatically

### Issue 5: Session Not Persisting

**Solution:**
- Make sure `sessions/whatsapp` directory has write permissions
- Don't delete the session folder between runs
- Complete the QR code scan within 120 seconds

---

## Environment Variables

If you have Playwright installed on E: drive, make sure this is set:

```bash
# Windows Command Prompt
set PLAYWRIGHT_BROWSERS_PATH=E:\playwright-browsers

# Windows PowerShell
$env:PLAYWRIGHT_BROWSERS_PATH="E:\playwright-browsers"
```

---

## File Locations

- **Session Data**: `sessions/whatsapp/`
- **Debug Screenshots**: `sessions/whatsapp/debug_screenshot.png` or `test_screenshot.png`
- **Logs**: `AI_Employee_Vault/Logs/whatsapp_watcher.log`
- **Action Files**: `AI_Employee_Vault/Needs_Action/WHATSAPP_*.md`

---

## Testing Checklist

- [ ] Run `python test_whatsapp_connection.py`
- [ ] Verify browser launches successfully
- [ ] Check that WhatsApp Web loads (look at browser window)
- [ ] Scan QR code if prompted
- [ ] Verify "Successfully logged in" message appears
- [ ] Check screenshot looks correct
- [ ] Run `python watchers/whatsapp_watcher.py`
- [ ] Verify watcher runs without timeout errors

---

## Advanced Debugging

### Enable Verbose Logging

Edit `watchers/whatsapp_watcher.py` and change:
```python
logging.basicConfig(level=logging.DEBUG)  # Changed from INFO
```

### Manual Browser Test

1. Open Chromium manually
2. Navigate to https://web.whatsapp.com
3. Check if it loads correctly
4. If it works manually but not via script, it's likely a detection issue

### Check Playwright Installation

```bash
# Verify Playwright is installed
python -c "from playwright.sync_api import sync_playwright; print('OK')"

# Reinstall if needed
pip install playwright
playwright install chromium
```

---

## Performance Tips

### For Production Use

1. **Enable Headless Mode** (after first login):
   ```python
   headless=True  # In launch_persistent_context
   ```

2. **Adjust Check Interval**:
   ```python
   watcher = WhatsAppWatcher(check_interval=60)  # Check every 60 seconds
   ```

3. **Customize Keywords**:
   Edit the keywords list in `__init__`:
   ```python
   self.keywords = ['urgent', 'invoice', 'payment', 'help', 'asap', 'important']
   ```

---

## Getting Help

If issues persist:

1. Check the screenshot at `sessions/whatsapp/debug_screenshot.png`
2. Review logs at `AI_Employee_Vault/Logs/whatsapp_watcher.log`
3. Run test script with verbose output
4. Verify Playwright and Chromium are properly installed
5. Ensure E: drive has sufficient space (at least 500MB free)

---

## Success Indicators

You'll know it's working when you see:

```
✅ Page loaded successfully
✅ Found element with selector: [data-testid="chat-list"]
✅ Already logged in to WhatsApp Web
Scanning for unread messages...
```

Or for first-time setup:

```
⚠️  QR CODE DETECTED - Please scan the QR code to log in!
✅ Successfully logged in to WhatsApp Web!
```
