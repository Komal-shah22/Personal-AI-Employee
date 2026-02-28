# 🔗 LinkedIn Direct Posting Setup Guide

## Overview
Connect your LinkedIn account to the AI Employee Dashboard for direct posting.

---

## 📋 Prerequisites

1. **LinkedIn Account** - Personal or Company Page
2. **LinkedIn Developer App** - Create at https://www.linkedin.com/developers/apps
3. **Python Requests Library**
   ```bash
   pip install requests
   ```

---

## 🚀 Step-by-Step Setup

### Step 1: Create LinkedIn Developer App

1. **Go to LinkedIn Developers:**
   - Visit: https://www.linkedin.com/developers/apps
   - Click **"Create app"**

2. **Fill App Details:**
   - **App name:** AI Employee Dashboard
   - **LinkedIn Page:** Select your company page (or create one)
   - **App logo:** Upload any logo (optional)
   - **Legal agreement:** Check the box
   - Click **"Create app"**

3. **Get Credentials:**
   - Go to **"Auth"** tab
   - Copy **Client ID**
   - Copy **Client Secret**
   - Keep these safe!

4. **Add Redirect URL:**
   - In **"Auth"** tab, find **"Redirect URLs"**
   - Click **"Add redirect URL"**
   - Enter: `http://localhost:8888/callback`
   - Click **"Update"**

5. **Request API Access:**
   - Go to **"Products"** tab
   - Find **"Share on LinkedIn"**
   - Click **"Request access"**
   - Wait for approval (usually instant for personal use)

### Step 2: Configure Environment Variables

Create or update `.env.local` file:

```bash
# LinkedIn API Credentials
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
```

**Or set environment variables:**

```bash
# Windows (PowerShell)
$env:LINKEDIN_CLIENT_ID="your_client_id_here"
$env:LINKEDIN_CLIENT_SECRET="your_client_secret_here"

# Windows (CMD)
set LINKEDIN_CLIENT_ID=your_client_id_here
set LINKEDIN_CLIENT_SECRET=your_client_secret_here

# Linux/Mac
export LINKEDIN_CLIENT_ID="your_client_id_here"
export LINKEDIN_CLIENT_SECRET="your_client_secret_here"
```

### Step 3: Authenticate Your Account

Run the authentication script:

```bash
python setup_linkedin_auth.py
```

**What happens:**
1. Browser opens automatically
2. LinkedIn login page appears (if not logged in)
3. Authorization page shows permissions
4. Click **"Allow"** to authorize
5. Browser redirects to success page
6. Token saved to `credentials/linkedin_token.json`

**Success Message:**
```
✅ SUCCESS! LinkedIn authenticated successfully!
Token saved to: credentials/linkedin_token.json
```

### Step 4: Test Direct Posting

Test with a simple post:

```bash
python post_linkedin_direct.py "Test post from AI Employee Dashboard! 🚀"
```

**Expected Output:**
```json
{
  "success": true,
  "post_id": "urn:li:share:1234567890",
  "posted_at": "2026-02-20T02:00:00.000000",
  "content": "Test post from AI Employee Dashboard! 🚀",
  "method": "linkedin_api_direct"
}
```

---

## 🖥️ Using Dashboard Form

Once authenticated, the dashboard form will post directly:

1. **Open Dashboard:** http://localhost:3001
2. **Go to Quick Actions** → **LinkedIn Tab**
3. **Fill Form:**
   - Content: Your post (max 3000 chars)
   - Image URL: (Optional)
4. **Click "Post to LinkedIn"**
5. **Success!** Post appears on your LinkedIn immediately

---

## 🔄 How It Works

### Direct Posting Flow:
```
Dashboard Form → API Route → Python Script → LinkedIn API → Your Profile
```

### Fallback Flow (if not authenticated):
```
Dashboard Form → API Route → Queue File → Orchestrator → LinkedIn API
```

---

## 🔍 Troubleshooting

### Error: "LinkedIn not authenticated"

**Solution:**
```bash
python setup_linkedin_auth.py
```

### Error: "Token expired"

**Solution:**
LinkedIn tokens expire after 60 days. Re-authenticate:
```bash
rm credentials/linkedin_token.json
python setup_linkedin_auth.py
```

### Error: "Invalid client credentials"

**Check:**
- Client ID and Secret are correct
- No extra spaces in environment variables
- App is not in "Development" mode restrictions

### Error: "Redirect URI mismatch"

**Fix:**
- Go to LinkedIn App → Auth tab
- Ensure redirect URL is exactly: `http://localhost:8888/callback`
- No trailing slash

### Posts not appearing

**Check:**
1. Token is valid: `cat credentials/linkedin_token.json`
2. App has "Share on LinkedIn" product access
3. Account has posting permissions
4. Content doesn't violate LinkedIn policies

### Error: "Unable to retrieve user URN for posting. Token may be valid but lacks proper permissions for posting."

**Cause:** LinkedIn's API requires specific scopes for direct posting, specifically both `w_member_social` (for posting) and `r_liteprofile` (for retrieving user ID to create URN).

**Solution:**
LinkedIn's API requires the `r_liteprofile` scope to retrieve the user's profile information needed for direct posting. If you only have `w_member_social`, the system will automatically fall back to queue-based posting which is processed by the orchestrator.

**To enable direct posting:**
1. Update your LinkedIn app to request `r_liteprofile` scope along with `w_member_social`
2. Go to your LinkedIn app settings in https://www.linkedin.com/developers
3. In the "Auth" tab, ensure default scopes include both `w_member_social` and `r_liteprofile`
4. Re-run: `python setup_linkedin_auth.py` to get a new token with proper scopes

The queue-based fallback is working as intended and will still post your content via the orchestrator.

---

## 📊 Features

✅ **Direct Posting** - Instant publish to LinkedIn
✅ **Text Posts** - Up to 3000 characters
✅ **Image Support** - Add images via URL
✅ **Public Visibility** - Posts visible to all connections
✅ **Fallback Queue** - Auto-queue if direct posting fails
✅ **Token Management** - Secure credential storage

---

## 🔐 Security Notes

- **Never commit** `credentials/linkedin_token.json` to git
- **Keep secret** your Client ID and Client Secret
- **Token expires** after 60 days (re-authenticate when needed)
- **Permissions** - Only requests necessary scopes

---

## 📝 API Scopes Used

- `w_member_social` - Post on your behalf
- `r_liteprofile` - Read basic profile information (required for direct posting)
- `r_emailaddress` - Read email address (recommended)

**Note:** For direct posting to work properly, your LinkedIn app must be configured with both `w_member_social` and `r_liteprofile` scopes. If you only have `w_member_social`, the system will fall back to queue-based posting which is processed by the orchestrator.

---

## 🎯 Next Steps

After setup:
1. ✅ Test posting from dashboard
2. ✅ Create your first LinkedIn post
3. ✅ Monitor posts in LinkedIn activity
4. ✅ Set up automated posting workflows

---

**Last Updated:** 2026-02-20
**Support:** Check dashboard logs for detailed error messages
