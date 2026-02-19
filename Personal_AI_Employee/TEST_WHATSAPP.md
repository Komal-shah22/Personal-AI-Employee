# WhatsApp Complete Testing Guide

## Your WhatsApp System is Ready! 🎉

### Architecture Overview:
```
Dashboard Form → API Route → Python Script → WhatsApp Web (Send)
WhatsApp Web → Python Watcher → Needs_Action Folder (Receive)
```

---

## Part 1: Testing WhatsApp SENDING (Dashboard → WhatsApp)

### Step 1: Start Dashboard
```bash
cd ai-employee-dashboard
npm run dev
```

### Step 2: Open Browser
- Go to: http://localhost:3000
- Click on "💬 WhatsApp" tab

### Step 3: Send Test Message
- Phone: +923170027046 (or any number with country code)
- Message: "Test message from AI Employee Dashboard"
- Click "Send WhatsApp Message"

### Expected Results:
- ✅ Browser will open WhatsApp Web
- ✅ If not logged in, scan QR code
- ✅ Message will be sent automatically
- ✅ Dashboard shows success message

---

## Part 2: Testing WhatsApp WATCHING (WhatsApp → Dashboard)

### Step 1: Start Watcher
```bash
# In project root
python watchers/whatsapp_watcher.py
```

### Step 2: First Time Setup
- Browser will open WhatsApp Web
- If QR code appears, scan it with your phone
- Session will be saved for future runs

### Step 3: Send Test Message to Yourself
From another phone or WhatsApp account, send a message containing keywords:
- "urgent help needed"
- "please send invoice"
- "payment required asap"

### Step 4: Check Results
Watcher will create a file in:
```
AI_Employee_Vault/Needs_Action/WHATSAPP_[timestamp]_[sender].md
```

### Expected Output:
```
--- Check #1 at 14:30:45 ---
Launching browser with persistent session...
Navigating to WhatsApp Web...
Scanning for unread messages...
Found 1 unread chat(s)
✓ Found urgent message from John Doe
  Keywords: urgent, help
  Preview: urgent help needed with project...
Created action item: WHATSAPP_20260217_143045_John_Doe.md
✓ Processed 1 urgent message(s)
Waiting 30 seconds until next check...
```

---

## Part 3: Run Both Together (Full System)

### Option A: Manual (2 Terminals)

**Terminal 1 - Dashboard:**
```bash
cd ai-employee-dashboard
npm run dev
```

**Terminal 2 - Watcher:**
```bash
python watchers/whatsapp_watcher.py
```

### Option B: Using Orchestrator (Recommended)

```bash
python orchestrator.py
```

This will start:
- Gmail Watcher
- WhatsApp Watcher
- File Watcher
- All monitoring systems

---

## Troubleshooting

### Issue 1: "WhatsApp Web not authenticated"
**Solution:**
```bash
# Run watcher once to authenticate
python watchers/whatsapp_watcher.py
# Scan QR code when browser opens
# Session will be saved in: sessions/whatsapp/
```

### Issue 2: "Could not find chat for phone number"
**Solution:**
- Verify phone number format: +[country code][number]
- Example: +923001234567 (Pakistan)
- Make sure the number has WhatsApp installed

### Issue 3: Watcher not detecting messages
**Solution:**
- Check if message contains keywords: urgent, asap, invoice, payment, help, quote, bill
- Check logs: AI_Employee_Vault/Logs/whatsapp_watcher.log
- Verify browser is staying open (headless=False for testing)

### Issue 4: Browser keeps crashing
**Solution:**
- Watcher has auto-retry (3 attempts)
- Waits 30 seconds between retries
- Check system resources (RAM, CPU)

---

## Configuration

### Change Keywords (watchers/whatsapp_watcher.py):
```python
self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'quote', 'bill']
# Add your own keywords here
```

### Change Check Interval:
```python
watcher = WhatsAppWatcher(check_interval=30)  # seconds
```

### Enable Headless Mode (Production):
```python
headless=True  # Line 106 in whatsapp_watcher.py
```

---

## File Structure

### Sending:
```
ai-employee-dashboard/
├── src/
│   ├── components/dashboard/QuickActionForms.tsx  (Form UI)
│   └── app/api/actions/send-whatsapp-direct/route.ts  (API)
└── send_whatsapp_direct.py  (Python sender)
```

### Watching:
```
watchers/
└── whatsapp_watcher.py  (Monitor incoming)

AI_Employee_Vault/
├── Needs_Action/  (Urgent messages appear here)
└── Logs/
    └── whatsapp_watcher.log  (Watcher logs)
```

---

## Quick Test Commands

### Test 1: Send WhatsApp from Command Line
```bash
python send_whatsapp_direct.py "+923001234567" "Test message"
```

### Test 2: Check Watcher Status
```bash
# Check if watcher is running
ps aux | grep whatsapp_watcher

# View live logs
tail -f AI_Employee_Vault/Logs/whatsapp_watcher.log
```

### Test 3: Verify Session
```bash
# Check if WhatsApp session exists
ls -la sessions/whatsapp/
# or
ls -la .whatsapp_session/
```

---

## Success Criteria ✅

Your WhatsApp system is working if:

1. ✅ Dashboard can send messages to any WhatsApp number
2. ✅ Watcher detects incoming messages with keywords
3. ✅ Action files are created in Needs_Action folder
4. ✅ Session persists (no QR code scan after first time)
5. ✅ Logs show successful operations

---

## Next Steps

1. **Test sending** from dashboard
2. **Test watching** by sending yourself a message with "urgent"
3. **Integrate with orchestrator** for 24/7 monitoring
4. **Add to startup** (PM2 or Task Scheduler)

---

## Status: GOLD TIER READY 🏆

Both WhatsApp features are implemented:
- ✅ Send messages from dashboard
- ✅ Watch and monitor incoming messages
- ✅ Keyword filtering
- ✅ Session persistence
- ✅ Error recovery
- ✅ Logging and audit trail

Your AI Employee can now handle WhatsApp communications autonomously!
