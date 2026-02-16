# Social Media MCP Server

MCP server for posting to Twitter, Facebook, and Instagram via the Model Context Protocol.

## Features

### Tools Provided

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

## Installation

### 1. Install Dependencies

```bash
cd .claude/mcp-servers/social-mcp
npm install
```

### 2. Configure Environment

```bash
# Copy template
cp .env.template .env

# Edit with your credentials
nano .env
```

### 3. Get API Credentials

#### Twitter/X Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new app (or use existing)
3. Enable OAuth 1.0a with **Read and Write** permissions
4. Generate API keys and access tokens
5. Copy to `.env`:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_SECRET`
   - `TWITTER_BEARER_TOKEN`

#### Facebook Setup

1. Go to [Facebook Developers](https://developers.facebook.com/apps/)
2. Create app → Select "Business" type
3. Add "Facebook Login" product
4. Generate User Access Token with permissions:
   - `pages_manage_posts` (for page posting)
   - `publish_to_groups` (optional)
5. Get Page ID from your Facebook page settings
6. Copy to `.env`:
   - `FB_ACCESS_TOKEN`
   - `FB_PAGE_ID` (optional)

#### Instagram Setup

**Requirements**: Instagram Business or Creator account linked to Facebook Page

1. Convert Instagram to Business account (in Instagram app)
2. Link to Facebook Page
3. Go to [Facebook Developers](https://developers.facebook.com/apps/)
4. Add "Instagram Graph API" product
5. Generate access token with permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
6. Get Instagram User ID:
   ```bash
   curl "https://graph.facebook.com/v18.0/me/accounts?access_token=YOUR_TOKEN"
   ```
7. Copy to `.env`:
   - `INSTAGRAM_USER_ID`
   - `INSTAGRAM_ACCESS_TOKEN`

### 4. Configure MCP

Add to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "social": {
      "command": "node",
      "args": [".claude/mcp-servers/social-mcp/index.js"],
      "env": {
        "DRY_RUN": "true"
      }
    }
  }
}
```

## Usage

### Post to Twitter

```javascript
// Via Claude Code
"Post this tweet: 'Hello from AI Employee! 🤖'"

// Direct MCP call
{
  "tool": "post_twitter",
  "arguments": {
    "text": "Hello from AI Employee! 🤖",
    "image_path": "/path/to/image.jpg"  // optional
  }
}
```

**Response**:
```json
{
  "success": true,
  "tweet_id": "1234567890",
  "url": "https://twitter.com/user/status/1234567890",
  "text": "Hello from AI Employee! 🤖",
  "timestamp": "2026-02-16T10:00:00Z"
}
```

### Post to Facebook

```javascript
// Via Claude Code
"Post to Facebook: 'Check out our new product launch!'"

// Direct MCP call
{
  "tool": "post_facebook",
  "arguments": {
    "text": "Check out our new product launch!",
    "page_id": "123456789"  // optional, uses FB_PAGE_ID if not provided
  }
}
```

### Post to Instagram

```javascript
// Via Claude Code
"Post this image to Instagram with caption: 'Beautiful sunset 🌅'"

// Direct MCP call
{
  "tool": "post_instagram",
  "arguments": {
    "image_path": "https://example.com/sunset.jpg",  // must be public URL
    "caption": "Beautiful sunset 🌅 #nature #photography"
  }
}
```

**Note**: Instagram requires a publicly accessible image URL, not a local file path.

### Get Analytics

```javascript
{
  "tool": "get_social_summary",
  "arguments": {
    "platform": "twitter",
    "days": 7
  }
}
```

**Response**:
```json
{
  "success": true,
  "platform": "twitter",
  "days": 7,
  "post_count": 12,
  "avg_engagement": 45.5,
  "top_post": {
    "id": "1234567890",
    "text": "Our most engaging tweet",
    "engagement": 150
  }
}
```

### Schedule a Post

```javascript
{
  "tool": "schedule_post",
  "arguments": {
    "platform": "twitter",
    "text": "Good morning! ☀️",
    "scheduled_time": "2026-02-17T08:00:00Z"
  }
}
```

This creates a file in `AI_Employee_Vault/Needs_Action/SOCIAL_TWITTER_2026-02-17_08-00-00.md` that the orchestrator will process at the scheduled time.

## DRY RUN Mode

**IMPORTANT**: By default, the server runs in DRY RUN mode for safety.

In DRY RUN mode:
- No actual posts are made to social media
- All API calls are simulated
- Mock responses are returned
- Safe for testing

To disable DRY RUN and post for real:

```bash
# In .env file
DRY_RUN=false
```

Or in MCP configuration:

```json
{
  "mcpServers": {
    "social": {
      "command": "node",
      "args": [".claude/mcp-servers/social-mcp/index.js"],
      "env": {
        "DRY_RUN": "false"
      }
    }
  }
}
```

## Testing

### Test Script

```bash
npm test
```

This runs `test.js` which tests all tools in DRY RUN mode.

### Manual Testing

```bash
# Start server
npm start

# In another terminal, send MCP request
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | node index.js
```

### Test with Claude Code

```bash
# Enable the MCP server in Claude Code
claude mcp list

# Test a post
claude -p "Use the social MCP to post a test tweet: 'Testing Social MCP 🚀'"
```

## Character Limits

| Platform | Text Limit | Notes |
|----------|------------|-------|
| Twitter | 280 chars | Auto-truncates with "..." |
| Facebook | ~63,206 chars | Practically unlimited |
| Instagram | 2200 chars | Caption only, image required |
| LinkedIn | 3000 chars | Via schedule_post |

## Image Requirements

### Twitter
- Formats: JPG, PNG, GIF, WEBP
- Max size: 5MB (photos), 15MB (GIFs)
- Max dimensions: 8192x8192

### Facebook
- Formats: JPG, PNG, GIF, BMP
- Max size: 4MB
- Recommended: 1200x630 (link posts)

### Instagram
- Formats: JPG, PNG
- Max size: 8MB
- Aspect ratio: 1.91:1 to 4:5
- Min resolution: 320px width
- **Must be publicly accessible URL** (not local file)

## Error Handling

### Common Errors

**"Twitter credentials not configured"**
- Check `.env` file has all 5 Twitter variables
- Verify credentials are correct

**"Facebook API error: Invalid OAuth access token"**
- Token may have expired (regenerate)
- Check token has correct permissions
- Verify app is not in development mode

**"Instagram container creation error"**
- Image URL must be publicly accessible
- Check image meets format/size requirements
- Verify Instagram account is Business/Creator type

**"Caption too long"**
- Instagram: max 2200 characters
- Twitter: max 280 characters (auto-truncates)

## Integration with AI Employee

### With Orchestrator

The orchestrator can process scheduled posts:

```python
# In orchestrator.py
if frontmatter.get('type') == 'social_post':
    platform = frontmatter.get('platform')
    scheduled_time = frontmatter.get('scheduled_time')

    # Check if time to post
    if datetime.now() >= datetime.fromisoformat(scheduled_time):
        # Call social MCP to post
        execute_social_post(frontmatter, body)
```

### With Social Media Skill

Use with `.claude/skills/social_media_skill.md`:

```markdown
When creating a LinkedIn post:
1. Generate post following the formula
2. Use social MCP's schedule_post tool
3. Create approval request
4. Wait for human approval
5. Post at scheduled time
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
   - Add to `.gitignore`
   - Use `.env.template` for sharing

2. **Use long-lived tokens**
   - Facebook: Generate 60-day tokens
   - Twitter: Tokens don't expire
   - Instagram: Refresh tokens regularly

3. **Rotate credentials regularly**
   - Change tokens every 90 days
   - Revoke old tokens

4. **Limit permissions**
   - Only request needed scopes
   - Use read-only tokens for analytics

5. **Keep DRY_RUN enabled**
   - Test thoroughly before going live
   - Use DRY_RUN for development

## Troubleshooting

### Server won't start

```bash
# Check Node version (need 18+)
node --version

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check for syntax errors
node --check index.js
```

### Posts not appearing

1. Check DRY_RUN is disabled
2. Verify credentials are correct
3. Check API rate limits
4. Review platform-specific requirements

### Instagram posts failing

- Image must be publicly accessible URL
- Account must be Business/Creator type
- Must be linked to Facebook Page
- Check image format and size

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

## Advanced Usage

### Custom Image Upload

For local images, upload to a CDN first:

```javascript
// Upload to CDN
const imageUrl = await uploadToCDN(localImagePath);

// Then post to Instagram
await post_instagram({
  image_path: imageUrl,
  caption: "My photo"
});
```

### Batch Posting

```javascript
// Schedule multiple posts
const posts = [
  { platform: "twitter", text: "Post 1", time: "2026-02-17T08:00:00Z" },
  { platform: "facebook", text: "Post 2", time: "2026-02-17T10:00:00Z" },
  { platform: "instagram", text: "Post 3", time: "2026-02-17T12:00:00Z" }
];

for (const post of posts) {
  await schedule_post(post);
}
```

### Cross-posting

```javascript
// Post to all platforms
const text = "Big announcement! 🎉";

await post_twitter({ text });
await post_facebook({ text });
// Instagram needs image
await post_instagram({
  image_path: "https://example.com/announcement.jpg",
  caption: text
});
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

## Support

For issues or questions:

1. Check this README
2. Review `.env.template` for credential setup
3. Test with DRY_RUN enabled
4. Check platform API documentation
5. Review error messages in logs

## License

MIT

---

**Version**: 1.0.0

**Last Updated**: 2026-02-16

**Platforms**: Twitter, Facebook, Instagram

**Status**: Production Ready (with DRY_RUN enabled by default)
