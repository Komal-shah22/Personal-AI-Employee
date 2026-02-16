# Gmail Watcher Setup Guide

This guide will walk you through setting up the Gmail Watcher to monitor your Gmail inbox for important emails.

## Prerequisites

- Python 3.8 or higher
- A Google account with Gmail
- Access to Google Cloud Console

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top
3. Click "New Project"
4. Enter a project name (e.g., "AI Employee Gmail Watcher")
5. Click "Create"

## Step 2: Enable Gmail API

1. In your Google Cloud project, go to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click on "Gmail API"
4. Click "Enable"

## Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields:
     - App name: "AI Employee Gmail Watcher"
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"
   - Skip "Scopes" (click "Save and Continue")
   - Add your email as a test user
   - Click "Save and Continue"
4. Back to "Create OAuth client ID":
   - Application type: "Desktop app"
   - Name: "Gmail Watcher Desktop"
   - Click "Create"
5. Download the credentials:
   - Click "Download JSON" (optional - we'll use environment variables)
   - Or copy the Client ID and Client Secret

## Step 4: Configure Environment Variables

1. Copy `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and add your credentials:
   ```
   GMAIL_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
   GMAIL_CLIENT_SECRET=your_client_secret_here
   ```

## Step 5: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Step 6: Run the Gmail Watcher

Start the watcher:

```bash
python watchers/gmail_watcher.py
```

On first run:
1. A browser window will open
2. Sign in with your Google account
3. Click "Allow" to grant permissions
4. The browser will show "The authentication flow has completed"
5. Close the browser and return to the terminal

The watcher will now:
- Check for unread + important emails every 120 seconds
- Create action items in `AI_Employee_Vault/Needs_Action/`
- Log activity to `AI_Employee_Vault/Logs/gmail_watcher.log`

## How It Works

### Email Detection
- Monitors emails marked as **unread** AND **important**
- Gmail automatically marks emails as important based on your reading patterns
- You can manually mark emails as important using the "!" icon in Gmail

### Action Items Created
For each new important email, a markdown file is created with:
- Email metadata (from, subject, date, priority)
- Email snippet/preview
- Action checklist (reply, forward, archive)
- Space for notes

### File Naming
Files are named: `EMAIL_[Subject]_[Timestamp].md`

Example: `EMAIL_Invoice_Payment_Delay_20260216_143022.md`

### Duplicate Prevention
- Processed email IDs are stored in `.processed_ids.json`
- Emails are only processed once
- Delete this file to reprocess all emails

## Troubleshooting

### "Authentication failed"
- Check that your Client ID and Client Secret are correct in `.env`
- Ensure the Gmail API is enabled in Google Cloud Console
- Delete `token.json` and re-authenticate

### "No emails found"
- Check that you have unread emails marked as important
- In Gmail, click the "!" icon to mark emails as important
- Verify the watcher is running without errors

### "Permission denied" errors
- Ensure the OAuth consent screen is configured
- Add your email as a test user in Google Cloud Console
- Re-authenticate by deleting `token.json`

### Rate limiting
- The watcher includes exponential backoff (1s, 2s, 4s, up to 60s)
- Gmail API has generous quotas for personal use
- If you hit limits, the watcher will automatically retry

## Configuration

### Change Check Interval
Edit `watchers/gmail_watcher.py`:
```python
CHECK_INTERVAL = 120  # Change to desired seconds
```

### Change Email Query
Edit the query in `get_unread_important_emails()`:
```python
query = 'is:unread is:important'  # Modify as needed
```

Other query options:
- `is:unread` - All unread emails
- `is:starred` - Starred emails
- `from:someone@example.com` - From specific sender
- `subject:invoice` - Specific subject
- `newer_than:1d` - Last 24 hours

## Running as a Service

### Windows (Task Scheduler)
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At startup
4. Action: Start a program
5. Program: `python`
6. Arguments: `E:\hackathon-0\Personal_AI_Employee\watchers\gmail_watcher.py`
7. Start in: `E:\hackathon-0\Personal_AI_Employee`

### Linux/Mac (systemd or cron)
Create a systemd service or add to crontab:
```bash
@reboot cd /path/to/Personal_AI_Employee && python watchers/gmail_watcher.py
```

## Security Notes

- **Never commit `.env` or `token.json` to version control**
- The `.gitignore` file should exclude these files
- OAuth tokens are stored locally in `token.json`
- Tokens expire and are automatically refreshed
- Only grant read-only access (no email sending/deleting)

## Integration with AI Employee

The Gmail Watcher creates action items that can be processed by:
1. The email reply skill (`.claude/skills/email_reply_skill.md`)
2. The orchestrator (`orchestrator.py`)
3. Manual review through the dashboard

Action items follow the same format as other tasks in the system.

## Logs

View logs in real-time:
```bash
tail -f AI_Employee_Vault/Logs/gmail_watcher.log
```

Logs include:
- Timestamp of each check
- Number of emails found
- Action items created
- Any errors or warnings

---

**Need Help?**
- Check the logs first: `AI_Employee_Vault/Logs/gmail_watcher.log`
- Verify your `.env` configuration
- Ensure Gmail API is enabled in Google Cloud Console
- Review the troubleshooting section above
