# LinkedIn & Instagram Dashboard Posting Guide

## Overview

You can now post to **LinkedIn** and **Instagram** directly from your AI Employee Dashboard using browser automation (Playwright).

---

## 🚀 How to Use

### 1. Start the Dashboard

```bash
cd ai-employee-dashboard
npm run dev
```

Dashboard will be available at: **http://localhost:3000**

---

## 📱 Posting to LinkedIn

### Steps:

1. **Open Dashboard** → Click **"LinkedIn"** in the side navigation

2. **Fill the Form**:
   - **Post Type**: Select from dropdown (Business Insight, Client Success, etc.)
   - **Topic** (Optional): Add a topic/title
   - **Content**: Write your post (up to 3000 characters)

3. **Click "Post to LinkedIn"**

4. **What Happens**:
   - Browser opens automatically
   - Uses your saved LinkedIn session
   - Navigates to LinkedIn feed
   - Clicks "Start a post"
   - Types your content
   - Submits using Ctrl+Enter
   - Takes screenshots at each step
   - Closes after 10 seconds

### Example Post:

```
Post Type: Business Insight
Topic: AI Automation Benefits
Content: 
🚀 Excited to share how AI automation is transforming businesses!

Key benefits we've seen:
✅ 80% reduction in manual tasks
✅ 24/7 productivity
✅ Faster response times
✅ Cost savings

#AI #Automation #BusinessGrowth #Innovation
```

---

## 📸 Posting to Instagram

### Steps:

1. **Open Dashboard** → Click **"Instagram"** in the side navigation

2. **Fill the Form**:
   - **Image**: Upload an image (JPG, PNG up to 10MB) - Optional
   - **Caption**: Write your caption (up to 2200 characters)

3. **Click "Post Now"**

4. **What Happens**:
   - Browser opens automatically
   - Uses your saved Instagram session
   - Navigates to Instagram
   - Clicks "New" button
   - Adds your caption
   - Clicks "Share"
   - Takes screenshots at each step
   - Closes after 10 seconds

### Example Post:

```
Image: (upload your image)
Caption:
Behind the scenes of building an AI Employee! 🤖✨

This automation system handles:
📧 Email management
💬 WhatsApp messaging
📱 Social media posting
📊 Task orchestration

The future of work is here! 

#AI #Automation #TechLife #Innovation #Startup #Coding
```

---

## 🔧 How It Works

### Architecture:

```
Dashboard Form (Next.js)
       ↓
API Route (/api/actions/post-linkedin or /api/actions/post-instagram)
       ↓
Creates temporary Python script
       ↓
Runs Playwright script (playwright_linkedin_post.py or playwright_instagram_post.py)
       ↓
Browser automation posts to social media
       ↓
Returns success/failure to dashboard
```

### Files Created:

- `playwright_linkedin_post.py` - LinkedIn browser automation
- `playwright_instagram_post.py` - Instagram browser automation
- `ai-employee-dashboard/src/app/api/actions/post-linkedin/route.ts` - LinkedIn API
- `ai-employee-dashboard/src/app/api/actions/post-instagram/route.ts` - Instagram API

### Session Storage:

- **LinkedIn**: `sessions/linkedin/` folder
- **Instagram**: `sessions/instagram/` folder

First time you'll need to login manually. After that, sessions are saved!

---

## ⚠️ Important Notes

### For LinkedIn:
- ✅ Uses your saved browser session
- ✅ Supports text-only posts
- ✅ Character limit: 3000
- ✅ Takes 30-60 seconds to post
- ✅ Screenshots saved in `screenshots/` folder

### For Instagram:
- ✅ Uses your saved browser session
- ✅ Supports captions (image upload is manual in browser)
- ✅ Character limit: 2200
- ✅ Takes 30-60 seconds to post
- ✅ Screenshots saved in `screenshots/` folder

### Browser Automation:
- Uses **Playwright** with Chromium
- Stealth mode to avoid detection
- Human-like typing delays
- Random pauses for natural behavior

---

## 🐛 Troubleshooting

### "Browser doesn't open"
- Make sure Playwright is installed: `pip install playwright && playwright install chromium`
- Check Python is in PATH

### "Not logged in"
- First time: Login manually when browser opens
- Session will be saved for next time
- Check `sessions/` folder exists

### "Post didn't submit"
- Check screenshots in `screenshots/` folder
- Look for errors in terminal
- Try again - sometimes needs retry

### "Dashboard API error"
- Check dashboard terminal for errors
- Verify `.env.local` has correct paths
- Restart dev server: `npm run dev`

---

## 📊 Testing

### Test LinkedIn Posting:

```bash
# Direct from command line
python playwright_linkedin_post.py

# With custom caption
python playwright_linkedin_post.py --caption "Your custom text here"
```

### Test Instagram Posting:

```bash
# Direct from command line
python playwright_instagram_post.py --caption "Your caption"

# With image URL (if supported)
python playwright_instagram_post.py --caption "Your caption" --image "https://example.com/image.jpg"
```

---

## 🎯 Fallback Behavior

If direct posting fails:

1. **LinkedIn**: Creates file in `AI_Employee_Vault/Needs_Action/LINKEDIN_DASHBOARD_*.md`
2. **Instagram**: Returns error to dashboard for retry

The orchestrator can process queued posts later.

---

## 📝 Character Limits

| Platform | Limit | Best Practice |
|----------|-------|---------------|
| LinkedIn | 3000 | 1000-1500 for engagement |
| Instagram | 2200 | 150-200 + hashtags |

---

## 🔐 Security

- Sessions stored locally in `sessions/` folder
- No credentials sent to external servers
- All automation runs on your machine
- Browser runs in normal mode (not headless) for transparency

---

## 📈 Future Enhancements

- [ ] Image upload support for Instagram
- [ ] Schedule posts for later
- [ ] Post analytics/insights
- [ ] Multi-image carousel posts
- [ ] Video posts
- [ ] Story posting
- [ ] Hashtag suggestions

---

**Last Updated**: 2026-02-28
**Version**: 1.0.0
