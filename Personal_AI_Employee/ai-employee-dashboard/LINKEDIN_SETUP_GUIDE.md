# LinkedIn OAuth Setup Guide

This guide explains how to properly set up LinkedIn OAuth for your AI Employee Dashboard.

## Prerequisites

1. LinkedIn Application
2. Valid redirect URI (http://localhost:8888/callback in your case)
3. Client ID and Client Secret from LinkedIn

## Step 1: Create or Configure Your LinkedIn Application

1. Go to https://www.linkedin.com/developers/
2. Click "Create Application" or select your existing application
3. On the application page, ensure your:
   - Application name: [Your App Name]
   - Application description: [Your App Description]
   - Application logo: [Upload if desired]
   - Website URL: http://localhost:8888
   - Authorized redirect URLs: http://localhost:8888/callback

## Step 2: Enable LinkedIn Products

1. Go to the "Products" tab in your application
2. To post on behalf of users, you need to enable:
   - "Share on LinkedIn" (for w_member_social scope)
   - For user profile access, you need to enable:
     - "Sign In with LinkedIn" (for r_basicprofile, r_emailaddress scopes)

## Step 3: Submit for App Verification (Required for Most Scopes)

LinkedIn requires app verification for most API scopes:

1. Go to "Settings" tab of your application
2. Scroll down to "App Verification"
3. For "Share on LinkedIn":
   - Provide app description
   - Explain how you'll use the API
   - Submit for review
4. For "Sign In with LinkedIn" (for profile/email access):
   - This requires more extensive verification
   - You'll need to provide privacy policy URL
   - Go through additional security reviews

## Step 4: Environment Variables

Your .env.local file should contain:

```
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8888/callback
```

## Step 5: Running the OAuth Setup

1. Use the setup script: `python setup_linkedin_auth.py`
2. The script will open your browser to the LinkedIn authorization page
3. Log in to LinkedIn and approve the requested permissions
4. You'll be redirected to your callback URL
5. The access token will be saved to `credentials/linkedin_token.json`

## Alternative: Manual Token Setup

If you already have an access token:

1. Run: `python create_linkedin_token.py`
2. This creates a template file at `credentials/linkedin_token.json`
3. Replace the placeholder token with your actual access token

## Available Scopes

- `w_member_social`: Post updates, articles, share content (verified app required)
- `r_basicprofile`: Read basic profile information (verified app required)
- `r_emailaddress`: Read email address (verified app required)

## Troubleshooting

1. **Scope errors**: Most scopes require app verification
2. **Redirect URI errors**: Ensure it matches exactly what's registered
3. **Authorization timeout**: Check for browser pop-up blockers
4. **Invalid credentials**: Verify client ID and secret

## Security Notes

- Never commit your .env.local file to version control
- Store tokens securely
- Tokens typically expire after 60 days for LinkedIn

## Testing Your Setup

After getting your token, you can test it:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://api.linkedin.com/v2/userinfo"
```