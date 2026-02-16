#!/usr/bin/env node

/**
 * Test script for Email MCP Server
 * Tests all three tools: send_email, create_draft, search_emails
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

class MCPTester {
  constructor() {
    this.serverProcess = null;
    this.requestId = 1;
  }

  async startServer() {
    console.log('Starting Email MCP Server...\n');

    this.serverProcess = spawn('node', [join(__dirname, 'index.js')], {
      env: {
        ...process.env,
        DRY_RUN: 'true', // Always use dry-run for testing
      },
      stdio: ['pipe', 'pipe', 'inherit'],
    });

    // Wait for server to initialize
    await new Promise(resolve => setTimeout(resolve, 1000));
    console.log('Server started\n');
  }

  sendRequest(method, params) {
    return new Promise((resolve, reject) => {
      const request = {
        jsonrpc: '2.0',
        id: this.requestId++,
        method,
        params,
      };

      console.log(`Sending request: ${method}`);
      console.log(JSON.stringify(request, null, 2));
      console.log('');

      let responseData = '';

      const timeout = setTimeout(() => {
        reject(new Error('Request timeout'));
      }, 5000);

      this.serverProcess.stdout.once('data', (data) => {
        clearTimeout(timeout);
        responseData += data.toString();

        try {
          const response = JSON.parse(responseData);
          console.log('Response:');
          console.log(JSON.stringify(response, null, 2));
          console.log('\n' + '='.repeat(60) + '\n');
          resolve(response);
        } catch (error) {
          reject(new Error('Invalid JSON response'));
        }
      });

      this.serverProcess.stdin.write(JSON.stringify(request) + '\n');
    });
  }

  async testListTools() {
    console.log('TEST 1: List Available Tools\n');
    await this.sendRequest('tools/list', {});
  }

  async testSendEmail() {
    console.log('TEST 2: Send Email (DRY RUN)\n');
    await this.sendRequest('tools/call', {
      name: 'send_email',
      arguments: {
        to: 'test@example.com',
        subject: 'Test Email from MCP Server',
        body: 'This is a test email sent via the Email MCP Server.\n\nBest regards,\nAI Employee',
      },
    });
  }

  async testSendEmailWithAttachment() {
    console.log('TEST 3: Send Email with Attachment (DRY RUN)\n');
    await this.sendRequest('tools/call', {
      name: 'send_email',
      arguments: {
        to: 'client@example.com',
        subject: 'Invoice for January 2026',
        body: 'Dear Client,\n\nPlease find attached the invoice for January 2026.\n\nBest regards,\nAI Employee',
        attachment_path: 'E:\\hackathon-0\\Personal_AI_Employee\\AI_Employee_Vault\\Invoices\\sample_invoice.pdf',
      },
    });
  }

  async testCreateDraft() {
    console.log('TEST 4: Create Draft\n');
    await this.sendRequest('tools/call', {
      name: 'create_draft',
      arguments: {
        to: 'draft@example.com',
        subject: 'Draft Email',
        body: 'This is a draft email that will not be sent.',
      },
    });
  }

  async testSearchEmails() {
    console.log('TEST 5: Search Emails\n');
    await this.sendRequest('tools/call', {
      name: 'search_emails',
      arguments: {
        query: 'from:client@example.com',
        max_results: 5,
      },
    });
  }

  async runAllTests() {
    try {
      await this.startServer();

      await this.testListTools();
      await this.testSendEmail();
      await this.testSendEmailWithAttachment();
      await this.testCreateDraft();
      await this.testSearchEmails();

      console.log('✅ All tests completed successfully!\n');
      console.log('Note: All emails were in DRY_RUN mode (not actually sent)');

    } catch (error) {
      console.error('❌ Test failed:', error.message);
    } finally {
      this.stopServer();
    }
  }

  stopServer() {
    if (this.serverProcess) {
      console.log('\nStopping server...');
      this.serverProcess.kill();
    }
  }
}

// Run tests
const tester = new MCPTester();
tester.runAllTests();
