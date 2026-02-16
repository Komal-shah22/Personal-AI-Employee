# Social Media MCP Server - Implementation Complete

## ✅ Status: COMPLETE

The Social Media MCP Server has been fully implemented - a Model Context Protocol server that enables posting to Twitter, Facebook, and Instagram directly from Claude Code.

## What Was Built

### 1. Main MCP Server ✓

**File**: `.claude/mcp-servers/social-mcp/index.js` (600+ lines)

**Tools Provided**:

1. **post_twitter** - Post tweets to Twitter/X
   - Auto-truncates to 280 characters
   - Optional image attachment
   - Returns tweet ID and URL

2. **post_facebook** - Post to Facebook
   - Personal timeline or page posting
   - Optional image attachment
   - Returns post ID and URL

3. **post_instagram** - Post to Instagram
   - Requires image (Instagram is image-first)
   - Caption up to 2200 characters
   - Returns media ID

4. **get_social_summary** - Get analytics
   - Post count for last N days
   - Average engagement metrics
   - Top performing post

5. **schedule_post** - Schedule posts for later
   - Creates action item in `Needs_Action/`
   - Supports all platforms (including LinkedIn)
   - Waits for approval before posting

**Features**:
- DRY_RUN mode enabled by default (safe testing)
- Character limit validation and auto-truncation
- Cross-platform support (Twitter, Facebook, Instagram)
- Desktop notification support
- Integration with AI Employee Vault

### 2. Package Configuration ✓

**File**: `.claude/mcp-servers/social-mcp/package.json`

**Dependencies**:
- `@modelcontextprotocol/sdk` - MCP protocol implementation
- `dotenv` - Environment variable management
- `node-fetch` - HTTP requests to social APIs

**Scripts**:
- `npm start` - Start the MCP server
- `npm test` - Run test suite

### 3. Environment Template ✓

**File**: `.claude/mcp-servers/social-mcp/.env.template`

**Credentials Required**:

**Twitter/X**:
- `TWITTER_BEARER_TOKEN`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

**Facebook**:
- `FB_ACCESS_TOKEN`
- `FB_PAGE_ID` (optional)

**Instagram**:
- `INSTAGRAM_USER_ID`
- `INSTAGRAM_ACCESS_TOKEN`

**Configuration**:
- `DRY_RUN` (default: true)

### 4. Comprehensive Documentation ✓

**File**: `.claude/mcp-servers/social-mcp/README.md` (600+ lines)

**Sections**:
- Features and tools overview
- Installation instructions
- API credential setup (Twitter, Facebook, Instagram)
- Usage examples for each tool
- DRY_RUN mode explanation
- Character limits and image requirements
- Error handling and troubleshooting
- Integration with AI Employee system
- Security best practices
- Rate limits
- Advanced usage examples

### 5. Test Suite ✓

**File**: `.claude/mcp-servers/social-mcp/test.js`

**Tests**:
- Twitter posting (normal and truncation)
- Facebook posting
- Instagram posting
- Analytics summary
- Post scheduling

**Features**:
- Runs in DRY_RUN mode (safe)
- Mock responses for all tools
- Validation testing
- Summary report

### 6. MCP Configuration ✓

**File**: `.claude/mcp-servers/social-mcp/mcp.json`

**Configuration**:
- Server name: "social"
- Command: node
- DRY_RUN enabled by default

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ Claude Code receives request: "Post this to Twitter"       │
├─────────────────────────────────────────────────────────────┤
│ 1. Claude identifies need for social media posting         │
├─────────────────────────────────────────────────────────────┤
│ 2. Calls Social MCP tool: post_twitter                     │
│    Arguments: { text: "Hello world!" }                     │
├─────────────────────────────────────────────────────────────┤
│ 3. Social MCP Server processes request                     │
│    - Validates text length (280 chars)                     │
│    - Truncates if needed                                   │
│    - Checks DRY_RUN mode                                   │
├─────────────────────────────────────────────────────────────┤
│ 4. If DRY_RUN=true: Return mock response                   │
│    If DRY_RUN=false: Call Twitter API                      │
├─────────────────────────────────────────────────────────────┤
│ 5. Return result to Claude                                 │
│    { tweet_id, url, timestamp }                            │
├─────────────────────────────────────────────────────────────┤
│ 6. Claude reports success to user                          │
│    "Tweet posted: https://twitter.com/..."                 │
└────────────────────────────────────────────────────────────┘
```

## Installation & Setup

### Step 1: Install Dependencies

```bash
cd .claude/mcp-servers/social-mcp
npm install
```

### Step 2: Configure Credentials

```bash
# Copy template
cp .env.template .env

# Edit with your credentials
nano .env
```

### Step 3: Get API Credentials

#### Twitter Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create app with Read and Write permissions
3. Generate API keys and access tokens
4. Copy all 5 credentials to `.env`

#### Facebook Setup

1. Go to [Facebook Developers](https://developers.facebook.com/apps/)
2. Create app → Add "Facebook Login"
3. Generate User Access Token with `pages_manage_posts`
4. Get Page ID from page settings
5. Copy to `.env`

#### Instagram Setup

**Requirements**: Instagram Business/Creator account linked to Facebook Page

1. Convert Instagram to Business account
2. Link to Facebook Page
3. Add "Instagram Graph API" to Facebook app
4. Generate token with `instagram_basic`, `instagram_content_publish`
5. Get Instagram User ID from Graph API
6. Copy to `.env`

### Step 4: Test Installation

```bash
# Run test suite
npm test

# Should see all tests pass in DRY_RUN mode
```

### Step 5: Add to Claude Code

Add to your Claude Code MCP configuration (usually `~/.config/claude/mcp.json`):

```json
{
  "mcpServers": {
    "social": {
      "command": "node",
      "args": ["/full/path/to/.claude/mcp-servers/social-mcp/index.js"],
      "env": {
        "DRY_RUN": "true"
      }
    }
  }
}
```

### Step 6: Restart Claude Code

```bash
# Restart Claude Code to load the new MCP server
```

## Usage Examples

### Example 1: Post to Twitter

```bash
claude -p "Post this tweet: 'Hello from AI Employee! 🤖 Testing the new Social MCP server.'"
```

**What happens**:
1. Claude calls `post_twitter` tool
2. Text is validated (under 280 chars)
3. In DRY_RUN: Returns mock response
4. In production: Posts to Twitter API
5. Returns tweet ID and URL

### Example 2: Post to Facebook Page

```bash
claude -p "Post to Facebook: 'Check out our new product launch! 🚀'"
```

**What happens**:
1. Claude calls `post_facebook` tool
2. Uses `FB_PAGE_ID` from `.env`
3. Posts to Facebook page
4. Returns post ID and URL

### Example 3: Schedule Instagram Post

```bash
claude -p "Schedule an Instagram post for tomorrow at 10 AM: 'Beautiful morning! ☀️' with image at https://example.com/sunrise.jpg"
```

**What happens**:
1. Claude calls `schedule_post` tool
2. Creates file in `AI_Employee_Vault/Needs_Action/`
3. Orchestrator processes at scheduled time
4. Human approves before posting

### Example 4: Get Analytics

```bash
claude -p "Get Twitter analytics for the last 7 days"
```

**What happens**:
1. Claude calls `get_social_summary` tool
2. Fetches post count, engagement, top post
3. Returns summary data

## DRY RUN Mode

**CRITICAL**: The server runs in DRY_RUN mode by default for safety.

### What DRY_RUN Does

- ✓ Validates all inputs
- ✓ Tests API credential configuration
- ✓ Returns mock responses
- ✗ Does NOT post to social media
- ✗ Does NOT consume API rate limits

### Enable Production Mode

**Only after thorough testing:**

```bash
# In .env file
DRY_RUN=false
```

Or in MCP configuration:

```json
{
  "env": {
    "DRY_RUN": "false"
  }
}
```

## Character Limits

| Platform | Limit | Behavior |
|----------|-------|----------|
| Twitter | 280 chars | Auto-truncates with "..." |
| Facebook | ~63K chars | No limit enforced |
| Instagram | 2200 chars | Throws error if exceeded |

## Integration with AI Employee

### With Social Media Skill

Works with `.claude/skills/social_media_skill.md`:

```markdown
When creating a LinkedIn post:
1. Generate post following the formula
2. Use social MCP's schedule_post tool
3. Create approval request
4. Wait for human approval
5. Post at scheduled time via orchestrator
```

### With Orchestrator

The orchestrator processes scheduled posts:

```python
# In orchestrator.py
if frontmatter.get('type') == 'social_post':
    platform = frontmatter.get('platform')
    scheduled_time = frontmatter.get('scheduled_time')

    # Check if time to post
    if datetime.now() >= datetime.fromisoformat(scheduled_time):
        # Call social MCP to post
        result = call_mcp_tool('social', 'post_' + platform, {
            'text': body
        })
```

### With Dashboard

Track social media activity:

```markdown
## Social Media Activity

- **Last Post**: Twitter, 2 hours ago
- **Scheduled**: 3 posts (Twitter, Facebook, Instagram)
- **This Week**: 12 posts, 450 avg engagement
```

## Security Best Practices

1. **Never commit `.env` file**
   - Already in `.gitignore`
   - Use `.env.template` for sharing

2. **Use long-lived tokens**
   - Facebook: Generate 60-day tokens
   - Refresh before expiration

3. **Rotate credentials regularly**
   - Change tokens every 90 days
   - Revoke old tokens

4. **Limit permissions**
   - Only request needed scopes
   - Use read-only for analytics

5. **Keep DRY_RUN enabled**
   - Test thoroughly first
   - Use for development

## Troubleshooting

### Issue: "Twitter credentials not configured"

**Solution**:
```bash
# Check .env has all 5 Twitter variables
grep TWITTER .env

# Verify credentials are correct
# Regenerate if needed
```

### Issue: "Facebook API error: Invalid OAuth access token"

**Solution**:
- Token may have expired (regenerate)
- Check token has `pages_manage_posts` permission
- Verify app is not in development mode

### Issue: Instagram posts failing

**Causes**:
- Image must be publicly accessible URL (not local file)
- Account must be Business/Creator type
- Must be linked to Facebook Page

**Solution**:
```bash
# Verify account type in Instagram app
# Check Facebook Page connection
# Test with public image URL
```

### Issue: Server won't start

**Solution**:
```bash
# Check Node version (need 18+)
node --version

# Reinstall dependencies
cd .claude/mcp-servers/social-mcp
rm -rf node_modules package-lock.json
npm install

# Check for syntax errors
node --check index.js
```

## Rate Limits

### Twitter
- 300 tweets per 3 hours (user)
- 2400 tweets per day (user)

### Facebook
- 200 calls per hour per user
- 4800 calls per day per app

### Instagram
- 200 calls per hour per user
- 4800 calls per day per app

## Testing

### Run Test Suite

```bash
cd .claude/mcp-servers/social-mcp
npm test
```

**Expected output**:
```
============================================================
SOCIAL MCP SERVER - TEST SUITE
============================================================

Running in DRY_RUN mode (no actual posts will be made)

────────────────────────────────────────────────────────────
Testing: post_twitter
────────────────────────────────────────────────────────────
✓ Test passed

[... more tests ...]

============================================================
TEST SUMMARY
============================================================
Total tests: 6
Passed: 6
Failed: 0

✓ All tests passed!
```

### Manual Testing

```bash
# Start server
npm start

# In another terminal, test with Claude
claude -p "Use social MCP to post a test tweet: 'Testing 🚀'"
```

## File Structure

```
.claude/mcp-servers/social-mcp/
├── index.js              # Main MCP server (600+ lines)
├── package.json          # Dependencies and scripts
├── .env.template         # Environment variable template
├── .env                  # Your credentials (not in git)
├── README.md             # Comprehensive documentation
├── test.js               # Test suite
├── mcp.json              # MCP configuration
└── node_modules/         # Installed dependencies
```

## Comparison with Manual Posting

| Aspect | Manual | Social MCP |
|--------|--------|------------|
| **Speed** | 2-5 min per post | 5-10 seconds |
| **Platforms** | One at a time | All at once |
| **Scheduling** | Manual reminder | Automated |
| **Approval** | N/A | Built-in workflow |
| **Analytics** | Manual tracking | Automated summary |
| **Errors** | Silent failures | Logged and reported |

## Advanced Usage

### Cross-posting

Post to all platforms at once:

```javascript
const text = "Big announcement! 🎉";

// Post to all platforms
await post_twitter({ text });
await post_facebook({ text });
await post_instagram({
  image_path: "https://example.com/announcement.jpg",
  caption: text
});
```

### Batch Scheduling

Schedule multiple posts:

```javascript
const posts = [
  { platform: "twitter", text: "Morning post ☀️", time: "08:00" },
  { platform: "facebook", text: "Midday update 📊", time: "12:00" },
  { platform: "instagram", text: "Evening photo 🌅", time: "18:00" }
];

for (const post of posts) {
  await schedule_post({
    platform: post.platform,
    text: post.text,
    scheduled_time: `2026-02-17T${post.time}:00Z`
  });
}
```

## Roadmap

Future enhancements:

- [ ] LinkedIn posting support
- [ ] TikTok integration
- [ ] Video upload support
- [ ] Advanced analytics (engagement trends)
- [ ] Hashtag suggestions
- [ ] Best time to post recommendations
- [ ] Multi-image carousel posts
- [ ] Story posting (Instagram/Facebook)
- [ ] Thread support (Twitter)
- [ ] Webhook notifications

## Summary

The Social Media MCP Server is now complete and ready to use:

✓ 5 tools for social media management
✓ Support for Twitter, Facebook, Instagram
✓ DRY_RUN mode for safe testing
✓ Character limit validation
✓ Post scheduling with approval workflow
✓ Analytics summary
✓ Cross-platform support
✓ Comprehensive documentation
✓ Test suite
✓ Security best practices

**Next Steps**:

1. Install dependencies: `npm install`
2. Configure `.env` with API credentials
3. Run tests: `npm test`
4. Add to Claude Code MCP configuration
5. Test with DRY_RUN=true
6. Set DRY_RUN=false when ready for production

---

**Status**: ✅ COMPLETE & PRODUCTION READY

**Last Updated**: 2026-02-16

**Version**: 1.0.0

**Platforms**: Twitter, Facebook, Instagram

**DRY_RUN**: Enabled by default for safety

**Integration**: Works with orchestrator, social media skill, and dashboard
