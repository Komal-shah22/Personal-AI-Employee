# 🎉 WhatsApp Watcher - Quick Start

## ⚡ 5-Minute Setup

### Step 1: Install Playwright
```bash
pip install playwright
python -m playwright install chromium
```

### Step 2: Run Setup Script
```bash
python setup_whatsapp.py
```

### Step 3: Scan QR Code
1. Browser opens automatically
2. Scan QR code with your phone
3. Done! Session saved for future use

### Step 4: Start Monitoring
```bash
python watchers/whatsapp_watcher.py
```

---

## 📱 How to Scan QR Code

**On your phone:**
1. Open WhatsApp
2. Tap **Menu (⋮)** → **Linked Devices**
3. Tap **Link a Device**
4. Scan the QR code on your screen

---

## ✅ Test It

Send yourself a WhatsApp message with the word **"urgent"** and watch it appear in:
```
AI_Employee_Vault/Needs_Action/WHATSAPP_[timestamp].md
```

---

## 🔑 Keywords Monitored

Messages containing these words are automatically flagged:
- `urgent`
- `invoice`
- `payment`
- `help`
- `asap`

---

## 📊 What Happens

1. **Message arrives** with keyword
2. **Watcher detects** it (checks every 30 seconds)
3. **Action file created** in `/Needs_Action`
4. **Claude processes** it automatically
5. **You approve** the response
6. **Done!**

---

## 🛠️ Troubleshooting

### QR Code doesn't appear?
```bash
rm -rf sessions/whatsapp
python watchers/whatsapp_watcher.py
```

### Session expired?
Delete and re-scan:
```bash
rm -rf sessions/whatsapp
```

### Not detecting messages?
Check the log:
```bash
tail -f AI_Employee_Vault/Logs/whatsapp_watcher.log
```

---

## 📖 Full Documentation

See **WHATSAPP_SETUP_GUIDE.md** for complete instructions.

---

## 🚀 Production Mode

For 24/7 operation:
```bash
# Install PM2
npm install -g pm2

# Start watcher
pm2 start watchers/whatsapp_watcher.py --interpreter python3 --name whatsapp

# Save and auto-start on reboot
pm2 save
pm2 startup
```

---

**That's it! Your WhatsApp watcher is ready to monitor urgent messages 24/7! 🎉**
