#!/usr/bin/env node

/**
 * Email MCP Server - Node.js Implementation
 *
 * Provides Gmail integration for the Personal AI Employee system
 * Tools: send_email, create_draft, search_emails
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { google } from 'googleapis';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Load environment variables
dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const DRY_RUN = process.env.DRY_RUN === 'true';
const GMAIL_CLIENT_ID = process.env.GMAIL_CLIENT_ID;
const GMAIL_CLIENT_SECRET = process.env.GMAIL_CLIENT_SECRET;
const TOKEN_PATH = process.env.TOKEN_PATH || path.join(__dirname, '../../../token.json');

// Gmail API scopes
const SCOPES = [
  'https://www.googleapis.com/auth/gmail.send',
  'https://www.googleapis.com/auth/gmail.compose',
  'https://www.googleapis.com/auth/gmail.readonly'
];

class EmailMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'email-mcp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.gmailClient = null;
    this.setupHandlers();
    this.setupErrorHandling();

    console.error(`[Email MCP] Server initialized (DRY_RUN: ${DRY_RUN})`);
  }

  setupErrorHandling() {
    this.server.onerror = (error) => {
      console.error('[Email MCP] Server error:', error);
    };

    process.on('SIGINT', async () => {
      console.error('[Email MCP] Shutting down...');
      await this.server.close();
      process.exit(0);
    });
  }

  async getGmailClient() {
    if (this.gmailClient) {
      return this.gmailClient;
    }

    if (!GMAIL_CLIENT_ID || !GMAIL_CLIENT_SECRET) {
      throw new Error('GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET must be set in .env');
    }

    const oauth2Client = new google.auth.OAuth2(
      GMAIL_CLIENT_ID,
      GMAIL_CLIENT_SECRET,
      'http://localhost'
    );

    // Load token if exists
    if (fs.existsSync(TOKEN_PATH)) {
      const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
      oauth2Client.setCredentials(token);
    } else {
      throw new Error(`Token not found at ${TOKEN_PATH}. Please authenticate first.`);
    }

    this.gmailClient = google.gmail({ version: 'v1', auth: oauth2Client });
    return this.gmailClient;
  }

  createEmailMessage(to, subject, body, attachmentPath = null) {
    const boundary = '----=_Part_0_' + Date.now();
    let message = [
      `To: ${to}`,
      `Subject: ${subject}`,
      'MIME-Version: 1.0',
      `Content-Type: multipart/mixed; boundary="${boundary}"`,
      '',
      `--${boundary}`,
      'Content-Type: text/plain; charset=UTF-8',
      '',
      body,
    ];

    // Add attachment if provided
    if (attachmentPath && fs.existsSync(attachmentPath)) {
      const fileName = path.basename(attachmentPath);
      const fileContent = fs.readFileSync(attachmentPath);
      const base64File = fileContent.toString('base64');

      message.push(
        `--${boundary}`,
        `Content-Type: application/octet-stream; name="${fileName}"`,
        'Content-Transfer-Encoding: base64',
        `Content-Disposition: attachment; filename="${fileName}"`,
        '',
        base64File
      );
    }

    message.push(`--${boundary}--`);

    const email = message.join('\r\n');
    return Buffer.from(email).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }

  async sendEmail(to, subject, body, attachmentPath = null) {
    const timestamp = new Date().toISOString();

    // Create draft first (for logging)
    console.error(`[Email MCP] Creating draft: To=${to}, Subject=${subject}`);

    if (DRY_RUN) {
      console.error('[Email MCP] DRY RUN MODE - Email not actually sent');
      console.error(`[Email MCP] Would send to: ${to}`);
      console.error(`[Email MCP] Subject: ${subject}`);
      console.error(`[Email MCP] Body: ${body.substring(0, 100)}...`);
      if (attachmentPath) {
        console.error(`[Email MCP] Attachment: ${attachmentPath}`);
      }

      return {
        success: true,
        message_id: `dry_run_${Date.now()}`,
        timestamp,
        dry_run: true,
        note: 'Email not sent (DRY_RUN=true)'
      };
    }

    try {
      const gmail = await this.getGmailClient();
      const encodedMessage = this.createEmailMessage(to, subject, body, attachmentPath);

      const response = await gmail.users.messages.send({
        userId: 'me',
        requestBody: {
          raw: encodedMessage,
        },
      });

      console.error(`[Email MCP] Email sent successfully: ${response.data.id}`);

      return {
        success: true,
        message_id: response.data.id,
        timestamp,
        to,
        subject,
        note: 'Email sent successfully'
      };
    } catch (error) {
      console.error('[Email MCP] Error sending email:', error.message);
      return {
        success: false,
        error: error.message,
        timestamp
      };
    }
  }

  async createDraft(to, subject, body) {
    console.error(`[Email MCP] Creating draft: To=${to}, Subject=${subject}`);

    try {
      const gmail = await this.getGmailClient();
      const encodedMessage = this.createEmailMessage(to, subject, body);

      const response = await gmail.users.drafts.create({
        userId: 'me',
        requestBody: {
          message: {
            raw: encodedMessage,
          },
        },
      });

      console.error(`[Email MCP] Draft created: ${response.data.id}`);

      return {
        success: true,
        draft_id: response.data.id,
        to,
        subject,
        note: 'Draft created successfully'
      };
    } catch (error) {
      console.error('[Email MCP] Error creating draft:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  async searchEmails(query, maxResults = 10) {
    console.error(`[Email MCP] Searching emails: query="${query}", max=${maxResults}`);

    try {
      const gmail = await this.getGmailClient();

      const response = await gmail.users.messages.list({
        userId: 'me',
        q: query,
        maxResults: maxResults,
      });

      const messages = response.data.messages || [];
      const results = [];

      // Fetch details for each message
      for (const message of messages) {
        const details = await gmail.users.messages.get({
          userId: 'me',
          id: message.id,
          format: 'metadata',
          metadataHeaders: ['From', 'Subject', 'Date'],
        });

        const headers = details.data.payload.headers;
        const from = headers.find(h => h.name === 'From')?.value || 'Unknown';
        const subject = headers.find(h => h.name === 'Subject')?.value || 'No Subject';
        const date = headers.find(h => h.name === 'Date')?.value || '';

        results.push({
          id: message.id,
          from,
          subject,
          snippet: details.data.snippet,
          date
        });
      }

      console.error(`[Email MCP] Found ${results.length} emails`);

      return {
        success: true,
        query,
        count: results.length,
        results
      };
    } catch (error) {
      console.error('[Email MCP] Error searching emails:', error.message);
      return {
        success: false,
        error: error.message
      };
    }
  }

  setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'send_email',
          description: 'Send an email via Gmail API. Creates draft first, then sends. Respects DRY_RUN mode.',
          inputSchema: {
            type: 'object',
            properties: {
              to: {
                type: 'string',
                description: 'Recipient email address',
              },
              subject: {
                type: 'string',
                description: 'Email subject',
              },
              body: {
                type: 'string',
                description: 'Email body (plain text)',
              },
              attachment_path: {
                type: 'string',
                description: 'Optional: Absolute path to attachment file',
              },
            },
            required: ['to', 'subject', 'body'],
          },
        },
        {
          name: 'create_draft',
          description: 'Create a Gmail draft without sending',
          inputSchema: {
            type: 'object',
            properties: {
              to: {
                type: 'string',
                description: 'Recipient email address',
              },
              subject: {
                type: 'string',
                description: 'Email subject',
              },
              body: {
                type: 'string',
                description: 'Email body (plain text)',
              },
            },
            required: ['to', 'subject', 'body'],
          },
        },
        {
          name: 'search_emails',
          description: 'Search Gmail with query string (e.g., "from:user@example.com", "is:unread")',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Gmail search query',
              },
              max_results: {
                type: 'number',
                description: 'Maximum number of results (default: 10)',
                default: 10,
              },
            },
            required: ['query'],
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'send_email': {
            const result = await this.sendEmail(
              args.to,
              args.subject,
              args.body,
              args.attachment_path
            );
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(result, null, 2),
                },
              ],
            };
          }

          case 'create_draft': {
            const result = await this.createDraft(
              args.to,
              args.subject,
              args.body
            );
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(result, null, 2),
                },
              ],
            };
          }

          case 'search_emails': {
            const result = await this.searchEmails(
              args.query,
              args.max_results || 10
            );
            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(result, null, 2),
                },
              ],
            };
          }

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                success: false,
                error: error.message,
              }, null, 2),
            },
          ],
          isError: true,
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('[Email MCP] Server running on stdio');
  }
}

// Start server
const server = new EmailMCPServer();
server.run().catch((error) => {
  console.error('[Email MCP] Fatal error:', error);
  process.exit(1);
});
