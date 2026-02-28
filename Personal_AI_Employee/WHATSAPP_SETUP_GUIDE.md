# 🔧 WhatsApp Watcher Setup Guide

## Problem
WhatsApp watcher shows QR code but closes too quickly (120 seconds timeout).

## Solution
Use dedicated setup script with unlimited time for QR scanning.

---

## 📋 Prerequisites

1. **Install Playwright:**
```bash
pip install playwright
playwright install chromium
```

2. **Verify Installation:**
```bash
python test_whatsapp_watcher.py
```

---

## 🚀 Setup Process

### Step 1: Run Setup Script

```bash
python setup_whatsapp_session.py
```

**What happens:**
- Browser opens automatically
- WhatsApp Web loads
- QR code appears
- **UNLIMITED TIME** - no timeout!

### Step 2: Scan QR Code

**On your phone:**
1. Open WhatsApp
2. Tap Menu (⋮) → **Linked Devices**
3. Tap **Link a Device**
4. Scan the QR code on screen

**Wait for success message:**
```
✅ SUCCESS! WhatsApp Web is logged in!
Your session has been saved to: sessions/whatsapp/
```

### Step 3: Close Browser

- Browser will stay open
- Press **Ctrl+C** in terminal when done
- Session is saved automatically

---

## ✅ Verify Setup

### Test with Real Message

1. Send yourself a WhatsApp message with word "urgent"
2. Run: `python watchers/whatsapp_watcher.py`
3. Check: `AI_Employee_Vault/Needs_Action/` for new file

---

## 🔄 Run Continuously

```bash
# Foreground (for testing)
python watchers/whatsapp_watcher.py

# Press Ctrl+C to stop
```

---

## 🔍 Troubleshooting

### QR Code Not Appearing
```bash
rm -rf sessions/whatsapp/*
python setup_whatsapp_session.py
```

### Session Expired
- Re-run setup script to re-authenticate

### No Messages Detected
- Check message contains keywords: urgent, asap, invoice, payment, help
- Message must be unread

---

**Last Updated:** 2026-02-19
