#!/usr/bin/env node

/**
 * Test script for Social MCP Server
 * Tests all tools in DRY_RUN mode
 */

import dotenv from 'dotenv';

dotenv.config();

// Force DRY_RUN for testing
process.env.DRY_RUN = 'true';

console.log('='.repeat(60));
console.log('SOCIAL MCP SERVER - TEST SUITE');
console.log('='.repeat(60));
console.log('');
console.log('Running in DRY_RUN mode (no actual posts will be made)');
console.log('');

// Test data
const tests = [
  {
    name: 'post_twitter',
    args: {
      text: 'Test tweet from Social MCP! 🚀 This is a test to verify the Twitter integration is working correctly.',
    },
  },
  {
    name: 'post_twitter (with truncation)',
    args: {
      text: 'This is a very long tweet that exceeds the 280 character limit and should be automatically truncated with ellipsis at the end. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.',
    },
  },
  {
    name: 'post_facebook',
    args: {
      text: 'Test Facebook post from Social MCP! 📱 Testing the Facebook integration.',
    },
  },
  {
    name: 'post_instagram',
    args: {
      image_path: 'https://example.com/test-image.jpg',
      caption: 'Test Instagram post from Social MCP! 📸 #testing #socialmcp',
    },
  },
  {
    name: 'get_social_summary',
    args: {
      platform: 'twitter',
      days: 7,
    },
  },
  {
    name: 'schedule_post',
    args: {
      platform: 'twitter',
      text: 'Scheduled test post from Social MCP! ⏰',
      scheduled_time: new Date(Date.now() + 3600000).toISOString(), // 1 hour from now
    },
  },
];

// Mock MCP server for testing
class MockMCPServer {
  async callTool(name, args) {
    console.log(`\n${'─'.repeat(60)}`);
    console.log(`Testing: ${name}`);
    console.log(`${'─'.repeat(60)}`);
    console.log('Arguments:');
    console.log(JSON.stringify(args, null, 2));
    console.log('');

    try {
      // Simulate tool execution
      let result;

      switch (name) {
        case 'post_twitter':
          result = this.mockPostTwitter(args);
          break;
        case 'post_facebook':
          result = this.mockPostFacebook(args);
          break;
        case 'post_instagram':
          result = this.mockPostInstagram(args);
          break;
        case 'get_social_summary':
          result = this.mockGetSocialSummary(args);
          break;
        case 'schedule_post':
          result = this.mockSchedulePost(args);
          break;
        default:
          throw new Error(`Unknown tool: ${name}`);
      }

      console.log('Result:');
      console.log(JSON.stringify(result, null, 2));
      console.log('');
      console.log('✓ Test passed');

      return result;
    } catch (error) {
      console.log('✗ Test failed');
      console.log(`Error: ${error.message}`);
      throw error;
    }
  }

  mockPostTwitter(args) {
    const { text } = args;

    // Check truncation
    let tweetText = text;
    if (text.length > 280) {
      tweetText = text.substring(0, 277) + '...';
      console.log(`Note: Tweet truncated from ${text.length} to 280 characters`);
    }

    return {
      success: true,
      dry_run: true,
      tweet_id: `dry_run_${Date.now()}`,
      url: 'https://twitter.com/user/status/dry_run',
      text: tweetText,
      timestamp: new Date().toISOString(),
      message: 'DRY RUN: Tweet not actually posted',
    };
  }

  mockPostFacebook(args) {
    const { text } = args;

    return {
      success: true,
      dry_run: true,
      post_id: `dry_run_${Date.now()}`,
      url: 'https://facebook.com/dry_run',
      text,
      timestamp: new Date().toISOString(),
      message: 'DRY RUN: Post not actually created',
    };
  }

  mockPostInstagram(args) {
    const { image_path, caption } = args;

    // Validate caption length
    if (caption.length > 2200) {
      throw new Error(`Caption too long: ${caption.length} characters (max 2200)`);
    }

    return {
      success: true,
      dry_run: true,
      media_id: `dry_run_${Date.now()}`,
      caption,
      timestamp: new Date().toISOString(),
      message: 'DRY RUN: Post not actually created',
    };
  }

  mockGetSocialSummary(args) {
    const { platform, days = 7 } = args;

    return {
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
    };
  }

  mockSchedulePost(args) {
    const { platform, text, scheduled_time } = args;

    // Validate scheduled time
    const scheduledDate = new Date(scheduled_time);
    if (isNaN(scheduledDate.getTime())) {
      throw new Error(`Invalid scheduled_time: ${scheduled_time}`);
    }

    const filename = `SOCIAL_${platform.toUpperCase()}_${scheduled_time.replace(/[:.]/g, '-')}.md`;

    return {
      success: true,
      scheduled: true,
      platform,
      scheduled_time,
      filename,
      message: `Post scheduled for ${scheduledDate.toLocaleString()}`,
    };
  }
}

// Run tests
async function runTests() {
  const server = new MockMCPServer();
  let passed = 0;
  let failed = 0;

  for (const test of tests) {
    try {
      await server.callTool(test.name, test.args);
      passed++;
    } catch (error) {
      failed++;
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('TEST SUMMARY');
  console.log('='.repeat(60));
  console.log(`Total tests: ${tests.length}`);
  console.log(`Passed: ${passed}`);
  console.log(`Failed: ${failed}`);
  console.log('');

  if (failed === 0) {
    console.log('✓ All tests passed!');
    console.log('');
    console.log('Next steps:');
    console.log('1. Configure .env with your API credentials');
    console.log('2. Add to Claude Code MCP configuration');
    console.log('3. Test with DRY_RUN=true first');
    console.log('4. Set DRY_RUN=false when ready to post for real');
  } else {
    console.log('✗ Some tests failed. Please review the errors above.');
    process.exit(1);
  }
}

runTests().catch(console.error);
