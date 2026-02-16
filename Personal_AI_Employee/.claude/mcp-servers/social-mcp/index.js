#!/usr/bin/env node

/**
 * Social Media MCP Server
 *
 * Provides tools for posting to Twitter, Facebook, and Instagram via MCP protocol.
 *
 * Tools:
 * - post_twitter: Post to Twitter (280 char limit)
 * - post_facebook: Post to Facebook (personal or page)
 * - post_instagram: Post to Instagram (requires image)
 * - get_social_summary: Get analytics for any platform
 * - schedule_post: Schedule a post for later (creates action item)
 *
 * Environment Variables:
 * - TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
 * - FB_ACCESS_TOKEN, FB_PAGE_ID
 * - INSTAGRAM_USER_ID, INSTAGRAM_ACCESS_TOKEN
 * - DRY_RUN (optional, default: true)
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import dotenv from 'dotenv';
import fetch from 'node-fetch';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const DRY_RUN = process.env.DRY_RUN !== 'false'; // Default to true for safety

// Twitter API v2 endpoints
const TWITTER_API_BASE = 'https://api.twitter.com/2';
const TWITTER_UPLOAD_BASE = 'https://upload.twitter.com/1.1';

// Facebook Graph API
const FB_GRAPH_API = 'https://graph.facebook.com/v18.0';

// Instagram Graph API
const IG_GRAPH_API = 'https://graph.facebook.com/v18.0';

class SocialMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'social-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
  }

  setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'post_twitter',
          description: 'Post a tweet to Twitter (max 280 characters, auto-truncates)',
          inputSchema: {
            type: 'object',
            properties: {
              text: {
                type: 'string',
                description: 'Tweet text (max 280 characters)',
              },
              image_path: {
                type: 'string',
                description: 'Optional path to image file',
              },
            },
            required: ['text'],
          },
        },
        {
          name: 'post_facebook',
          description: 'Post to Facebook (personal timeline or page)',
          inputSchema: {
            type: 'object',
            properties: {
              text: {
                type: 'string',
                description: 'Post text',
              },
              image_path: {
                type: 'string',
                description: 'Optional path to image file',
              },
              page_id: {
                type: 'string',
                description: 'Optional Facebook Page ID (uses FB_PAGE_ID from .env if not provided)',
              },
            },
            required: ['text'],
          },
        },
        {
          name: 'post_instagram',
          description: 'Post to Instagram (requires image, Business account)',
          inputSchema: {
            type: 'object',
            properties: {
              image_path: {
                type: 'string',
                description: 'Path to image file (required)',
              },
              caption: {
                type: 'string',
                description: 'Post caption (max 2200 characters)',
              },
            },
            required: ['image_path', 'caption'],
          },
        },
        {
          name: 'get_social_summary',
          description: 'Get analytics summary for a social platform',
          inputSchema: {
            type: 'object',
            properties: {
              platform: {
                type: 'string',
                enum: ['twitter', 'facebook', 'instagram'],
                description: 'Social media platform',
              },
              days: {
                type: 'number',
                description: 'Number of days to look back (default: 7)',
              },
            },
            required: ['platform'],
          },
        },
        {
          name: 'schedule_post',
          description: 'Schedule a post for later (creates action item in Needs_Action/)',
          inputSchema: {
            type: 'object',
            properties: {
              platform: {
                type: 'string',
                enum: ['twitter', 'facebook', 'instagram', 'linkedin'],
                description: 'Target platform',
              },
              text: {
                type: 'string',
                description: 'Post text/caption',
              },
              scheduled_time: {
                type: 'string',
                description: 'ISO 8601 timestamp (e.g., 2026-02-17T10:00:00Z)',
              },
              image_path: {
                type: 'string',
                description: 'Optional path to image',
              },
            },
            required: ['platform', 'text', 'scheduled_time'],
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'post_twitter':
            return await this.postTwitter(args);
          case 'post_facebook':
            return await this.postFacebook(args);
          case 'post_instagram':
            return await this.postInstagram(args);
          case 'get_social_summary':
            return await this.getSocialSummary(args);
          case 'schedule_post':
            return await this.schedulePost(args);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error.message}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  /**
   * Post to Twitter
   */
  async postTwitter(args) {
    const { text, image_path } = args;

    // Validate credentials
    if (!process.env.TWITTER_API_KEY || !process.env.TWITTER_API_SECRET ||
        !process.env.TWITTER_ACCESS_TOKEN || !process.env.TWITTER_ACCESS_SECRET) {
      throw new Error('Twitter credentials not configured in .env');
    }

    // Truncate text if needed
    let tweetText = text;
    if (text.length > 280) {
      tweetText = text.substring(0, 277) + '...';
      console.error(`[Social MCP] Tweet truncated from ${text.length} to 280 characters`);
    }

    const timestamp = new Date().toISOString();

    if (DRY_RUN) {
      console.error('[Social MCP] DRY RUN MODE - Tweet not actually posted');
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              dry_run: true,
              tweet_id: `dry_run_${Date.now()}`,
              url: 'https://twitter.com/user/status/dry_run',
              text: tweetText,
              timestamp,
              message: 'DRY RUN: Tweet not actually posted',
            }, null, 2),
          },
        ],
      };
    }

    // Post tweet using Twitter API v2
    // Note: This requires OAuth 1.0a signing, which is complex
    // For production, use a library like 'twitter-api-v2'
    const response = await fetch(`${TWITTER_API_BASE}/tweets`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.TWITTER_BEARER_TOKEN}`,
      },
      body: JSON.stringify({
        text: tweetText,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Twitter API error: ${error}`);
    }

    const data = await response.json();

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            tweet_id: data.data.id,
            url: `https://twitter.com/user/status/${data.data.id}`,
            text: data.data.text,
            timestamp,
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Post to Facebook
   */
  async postFacebook(args) {
    const { text, image_path, page_id } = args;

    if (!process.env.FB_ACCESS_TOKEN) {
      throw new Error('Facebook access token not configured in .env');
    }

    const targetId = page_id || process.env.FB_PAGE_ID || 'me';
    const timestamp = new Date().toISOString();

    if (DRY_RUN) {
      console.error('[Social MCP] DRY RUN MODE - Facebook post not actually created');
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              dry_run: true,
              post_id: `dry_run_${Date.now()}`,
              url: 'https://facebook.com/dry_run',
              text,
              timestamp,
              message: 'DRY RUN: Post not actually created',
            }, null, 2),
          },
        ],
      };
    }

    // Post to Facebook
    const url = `${FB_GRAPH_API}/${targetId}/feed`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: text,
        access_token: process.env.FB_ACCESS_TOKEN,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Facebook API error: ${error}`);
    }

    const data = await response.json();

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            post_id: data.id,
            url: `https://facebook.com/${data.id}`,
            timestamp,
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Post to Instagram
   */
  async postInstagram(args) {
    const { image_path, caption } = args;

    if (!process.env.INSTAGRAM_USER_ID || !process.env.INSTAGRAM_ACCESS_TOKEN) {
      throw new Error('Instagram credentials not configured in .env');
    }

    // Validate caption length
    if (caption.length > 2200) {
      throw new Error(`Caption too long: ${caption.length} characters (max 2200)`);
    }

    const timestamp = new Date().toISOString();

    if (DRY_RUN) {
      console.error('[Social MCP] DRY RUN MODE - Instagram post not actually created');
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              dry_run: true,
              media_id: `dry_run_${Date.now()}`,
              caption,
              timestamp,
              message: 'DRY RUN: Post not actually created',
            }, null, 2),
          },
        ],
      };
    }

    // Instagram posting is a 2-step process:
    // 1. Create media container
    // 2. Publish container

    // Step 1: Create container
    const containerUrl = `${IG_GRAPH_API}/${process.env.INSTAGRAM_USER_ID}/media`;
    const containerResponse = await fetch(containerUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        image_url: image_path, // Must be publicly accessible URL
        caption: caption,
        access_token: process.env.INSTAGRAM_ACCESS_TOKEN,
      }),
    });

    if (!containerResponse.ok) {
      const error = await containerResponse.text();
      throw new Error(`Instagram container creation error: ${error}`);
    }

    const containerData = await containerResponse.json();
    const containerId = containerData.id;

    // Step 2: Publish container
    const publishUrl = `${IG_GRAPH_API}/${process.env.INSTAGRAM_USER_ID}/media_publish`;
    const publishResponse = await fetch(publishUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        creation_id: containerId,
        access_token: process.env.INSTAGRAM_ACCESS_TOKEN,
      }),
    });

    if (!publishResponse.ok) {
      const error = await publishResponse.text();
      throw new Error(`Instagram publish error: ${error}`);
    }

    const publishData = await publishResponse.json();

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            media_id: publishData.id,
            timestamp,
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Get social media analytics summary
   */
  async getSocialSummary(args) {
    const { platform, days = 7 } = args;

    if (DRY_RUN) {
      console.error('[Social MCP] DRY RUN MODE - Returning mock analytics');
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              dry_run: true,
              platform,
              days,
              post_count: 12,
              avg_engagement: 45.5,
              top_post: {
                id: 'mock_post_123',
                text: 'Sample top performing post',
                engagement: 150,
              },
              message: 'DRY RUN: Mock analytics data',
            }, null, 2),
          },
        ],
      };
    }

    // Fetch analytics based on platform
    let summary;

    switch (platform) {
      case 'twitter':
        summary = await this.getTwitterSummary(days);
        break;
      case 'facebook':
        summary = await this.getFacebookSummary(days);
        break;
      case 'instagram':
        summary = await this.getInstagramSummary(days);
        break;
      default:
        throw new Error(`Unsupported platform: ${platform}`);
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(summary, null, 2),
        },
      ],
    };
  }

  async getTwitterSummary(days) {
    // Placeholder - would fetch from Twitter API
    return {
      success: true,
      platform: 'twitter',
      days,
      post_count: 0,
      avg_engagement: 0,
      message: 'Twitter analytics not yet implemented',
    };
  }

  async getFacebookSummary(days) {
    // Placeholder - would fetch from Facebook Graph API
    return {
      success: true,
      platform: 'facebook',
      days,
      post_count: 0,
      avg_engagement: 0,
      message: 'Facebook analytics not yet implemented',
    };
  }

  async getInstagramSummary(days) {
    // Placeholder - would fetch from Instagram Graph API
    return {
      success: true,
      platform: 'instagram',
      days,
      post_count: 0,
      avg_engagement: 0,
      message: 'Instagram analytics not yet implemented',
    };
  }

  /**
   * Schedule a post for later
   */
  async schedulePost(args) {
    const { platform, text, scheduled_time, image_path } = args;

    // Validate scheduled time
    const scheduledDate = new Date(scheduled_time);
    if (isNaN(scheduledDate.getTime())) {
      throw new Error(`Invalid scheduled_time: ${scheduled_time}`);
    }

    // Create filename
    const timestamp = scheduledDate.toISOString().replace(/[:.]/g, '-').split('T')[0] + '_' +
                     scheduledDate.toISOString().replace(/[:.]/g, '-').split('T')[1].split('Z')[0];
    const filename = `SOCIAL_${platform.toUpperCase()}_${timestamp}.md`;

    // Prepare file content
    const content = `---
type: social_post
platform: ${platform}
scheduled_time: ${scheduled_time}
status: pending
created: ${new Date().toISOString()}
${image_path ? `image_path: ${image_path}` : ''}
---

# Scheduled ${platform.charAt(0).toUpperCase() + platform.slice(1)} Post

**Scheduled for**: ${scheduledDate.toLocaleString()}

## Content

${text}

${image_path ? `\n## Image\n\n\`${image_path}\`\n` : ''}

## Actions

- [ ] Review content
- [ ] Approve for posting
- [ ] Post at scheduled time

---

*Created by Social MCP Server*
*Scheduled: ${scheduled_time}*
`;

    // Write to Needs_Action directory
    const needsActionDir = path.join(process.cwd(), 'AI_Employee_Vault', 'Needs_Action');
    const filePath = path.join(needsActionDir, filename);

    try {
      await fs.mkdir(needsActionDir, { recursive: true });
      await fs.writeFile(filePath, content, 'utf-8');

      console.error(`[Social MCP] Scheduled post created: ${filePath}`);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              success: true,
              scheduled: true,
              platform,
              scheduled_time,
              file_path: filePath,
              filename,
              message: `Post scheduled for ${scheduledDate.toLocaleString()}`,
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      throw new Error(`Failed to create scheduled post file: ${error.message}`);
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Social MCP Server running on stdio');
    console.error(`DRY_RUN mode: ${DRY_RUN ? 'ENABLED' : 'DISABLED'}`);
  }
}

// Start server
const server = new SocialMCPServer();
server.run().catch(console.error);
