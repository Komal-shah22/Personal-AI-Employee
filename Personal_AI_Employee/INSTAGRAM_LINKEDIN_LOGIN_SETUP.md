# First-Time Social Media Login Setup

## Problem
Browser closes too fast when you're not logged in to Instagram/LinkedIn.

## Solution ✅
Scripts now **wait up to 60 seconds** for you to login manually!

---

## 📸 Instagram First-Time Setup

### Step 1: Run the Instagram script
```bash
python playwright_instagram_post.py --caption "Test post"
```

### Step 2: Browser Opens
- You'll see: **"⚠ Not logged in - waiting for manual login..."**
- Message: **"💡 Please login to Instagram in the opened browser"**
- Timer: **"⏳ Waiting up to 60 seconds for login..."**

### Step 3: Login to Instagram
1. Enter your **username/email**
2. Enter your **password**
3. Complete 2FA if enabled
4. You should see your Instagram feed

### Step 4: Script Detects Login
- Automatically detects when you're logged in
- Message: **"✓ Login detected after X seconds!"**
- Takes screenshot: `02_logged_in.png`
- Proceeds to post automatically

### Step 5: Future Runs
- **Session is saved** in `sessions/instagram/` folder
- Next time: **"✓ Already logged in"** - no manual login needed!
- Session lasts for weeks/months

---

## 💼 LinkedIn First-Time Setup

### Step 1: Run the LinkedIn script
```bash
python playwright_linkedin_post.py --caption "Test post"
```

### Step 2: Browser Opens
- If login page shows: **"⚠ Login page detected - waiting for manual login..."**
- Message: **"💡 Please login to LinkedIn in the opened browser"**
- Timer: **"⏳ Waiting up to 60 seconds for login..."**

### Step 3: Login to LinkedIn
1. Enter your **email/phone**
2. Enter your **password**
3. Complete verification if needed
4. You should see your LinkedIn feed

### Step 4: Script Detects Login
- Automatically detects when you're logged in
- Message: **"✓ Login detected after X seconds!"**
- Takes screenshot: `02_logged_in.png`
- Proceeds to post automatically

### Step 5: Future Runs
- **Session is saved** in `sessions/linkedin/` folder
- Next time: **"✓ Already logged in"** - no manual login needed!

---

## ⏱️ Timing Details

| Action | Time |
|--------|------|
| Login wait | Up to 60 seconds |
| Final verification | 30 seconds |
| Total script time | 1-2 minutes |

---

## 📸 Screenshots

All steps are captured in `screenshots/` folder:
- `01_browser_launched.png` - Browser opened
- `02_instagram_loaded.png` or `02_linkedin_loaded.png` - Site loaded
- `02_logged_in.png` - After you login (if needed)
- `03_new_post_clicked.png` - Creating post
- `05_caption_added.png` - Caption typed
- `06_post_shared.png` - Post submitted
- `07_final.png` - Final state

---

## 🔧 Troubleshooting

### "Browser closes before I can login"
- Script now waits 60 seconds - plenty of time!
- If still too fast, edit the script and change `range(60, 0, -1)` to `range(120, 0, -1)`

### "Login not detected"
- Script continues anyway - you can still post manually
- Check screenshots to see what happened
- Try running again - sometimes cookies need to be set first

### "Session doesn't save"
- Check `sessions/instagram/` or `sessions/linkedin/` folders exist
- Make sure browser closes properly (wait for "Closing browser..." message)
- Try logging in again - sometimes needs 2-3 successful logins

### "Instagram doesn't show 'New' button"
- Make sure you're logged in (look for profile icon)
- Instagram sometimes hides it on mobile view - use desktop browser
- Try refreshing the page manually

### "LinkedIn doesn't show 'Start a post' button"
- Make sure you're on the feed page (linkedin.com/feed)
- Some account types don't have posting enabled
- Try navigating to feed manually

---

## 🔐 Security Notes

- ✅ Sessions stored **locally** on your computer
- ✅ No passwords saved in code
- ✅ Uses browser's built-in cookie storage
- ✅ Same security as normal browser browsing

---

## 🎯 Quick Reference

### Instagram Commands
```bash
# Simple test
python playwright_instagram_post.py --caption "Hello Instagram! #AI"

# With image URL (if supported)
python playwright_instagram_post.py --caption "Check this out!" --image "https://example.com/pic.jpg"
```

### LinkedIn Commands
```bash
# Simple test
python playwright_linkedin_post.py --caption "Hello LinkedIn! #AI"

# Custom caption
python playwright_linkedin_post.py --caption "Excited to share my AI automation project! 🚀"
```

---

## 📞 Need Help?

1. **Check screenshots** in `screenshots/` folder
2. **Read console output** - shows exactly what's happening
3. **Try manual login first** - open browser, login, then run script
4. **Check session folders** exist:
   - `E:\hackathon-0\Personal_AI_Employee\sessions\instagram\`
   - `E:\hackathon-0\Personal_AI_Employee\sessions\linkedin\`

---

**Last Updated**: 2026-02-28
**Version**: 1.1.0 (with login wait)
