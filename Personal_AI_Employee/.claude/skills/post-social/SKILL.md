# Post Social Skill

The `post-social` skill automates social media posting across multiple platforms (Facebook, Instagram, Twitter) for your Personal AI Employee.

## Overview

This skill enables your AI employee to automatically post content to social media platforms based on files placed in the `Needs_Action` folder. It processes social media requests, formats content appropriately for each platform, and manages the posting workflow.

## Capabilities

- **Multi-platform posting**: Supports Facebook, Instagram, and Twitter
- **Smart content formatting**: Adapts content to each platform's requirements
- **Hashtag optimization**: Adds relevant hashtags based on content
- **Scheduling support**: Can schedule posts for optimal times
- **Audit trail**: Maintains logs of all social media activity
- **Workflow integration**: Moves processed files to Done folder
- **Dashboard updates**: Updates statistics after posting

## Usage

### Basic Usage
```bash
claude skill post-social
```

### With Parameters
```bash
claude skill post-social --platform instagram --caption "Check out our new product!" --hashtags "#product #launch #news"
```

## Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `platform` | string | No | Target platform (facebook, instagram, twitter, or auto) |
| `caption` | string | No | Post caption or content |
| `hashtags` | array | No | Array of hashtags to include |

## File Format

The skill looks for specially formatted files in the `Needs_Action` folder:

```markdown
---
type: social_post
platform: auto  # facebook, instagram, twitter, or auto
caption: Your post content here
hashtags:
  - #marketing
  - #business
  - #automation
schedule: 2026-02-03T09:00:00Z  # Optional scheduling
---

# Social Media Post

This content will be formatted and posted to social media platforms.
```

## Output

The skill returns:
- Status of the posting operation
- Number of posts processed
- Details of each processed post
- Platform-specific post URLs

## Integration

- **Triggers**: Automatically processes files matching patterns:
  - `SOCIAL_*.md`
  - `FACEBOOK_*.md`
  - `INSTAGRAM_*.md`
  - `TWITTER_*.md`
- **Workflow**: Moves processed files to `Done` folder
- **Dashboard**: Updates statistics after processing
- **Logging**: Records all activity in vault logs

## Security

- All social media credentials are managed securely
- Human-in-the-loop approval for sensitive content
- Comprehensive audit logging
- Platform-specific content validation

## Best Practices

- Use clear, engaging captions
- Include relevant hashtags for discoverability
- Schedule posts for optimal engagement times
- Monitor and review posted content regularly
- Follow platform-specific content guidelines

## Troubleshooting

- If posts aren't appearing, check social media credentials
- Verify that files are in the correct format
- Check the logs in the `Logs` folder for error details
- Ensure MCP server is running for actual posting

## Dependencies

- PyYAML (for configuration parsing)
- MCP server for actual posting (in production)
- Vault access for file operations