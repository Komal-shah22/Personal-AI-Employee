import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import { safeParseJSON } from '@/lib/json-parser';
import { getPythonCommand } from '@/lib/python-runner';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const { phone, message } = await request.json();

    // Validate input
    if (!phone || !message) {
      return NextResponse.json(
        { error: 'Missing required fields: phone, message' },
        { status: 400 }
      );
    }

    // Validate phone format (basic check)
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    const cleanPhone = phone.replace(/[\s\-\(\)]/g, '');
    if (!phoneRegex.test(cleanPhone)) {
      return NextResponse.json(
        { error: 'Invalid phone number format. Use international format (e.g., +923001234567)' },
        { status: 400 }
      );
    }

    // Path to Python script
    const scriptPath = path.join(process.cwd(), '..', 'send_whatsapp_direct.py');

    // Escape arguments for shell
    const escapedPhone = phone.replace(/"/g, '\\"');
    const escapedMessage = message.replace(/"/g, '\\"');

    try {
      // Call Python script to send WhatsApp message directly
      // Execute from parent directory so script can find sessions folder
      const parentDir = path.join(process.cwd(), '..');
      const pythonCmd = getPythonCommand();
      const { stdout, stderr } = await execAsync(
        `${pythonCmd} "${scriptPath}" "${escapedPhone}" "${escapedMessage}"`,
        {
          cwd: parentDir, // Run from parent directory
          timeout: 60000, // 60 seconds for WhatsApp Web to load
          maxBuffer: 1024 * 1024
        }
      );

      const result = safeParseJSON(stdout);

      if (result.success) {
        return NextResponse.json({
          success: true,
          message: 'WhatsApp message sent successfully',
          details: {
            to: result.to,
            message: result.message,
            sentAt: result.sent_at,
            method: 'whatsapp_web_direct'
          }
        });
      } else {
        // If direct send failed, create file for orchestrator
        if (result.action_required === 'qr_scan') {
          return NextResponse.json({
            success: false,
            error: result.error,
            action_required: 'qr_scan',
            note: 'Please authenticate WhatsApp Web first by running: python watchers/whatsapp_watcher.py'
          }, { status: 401 });
        }

        // Create fallback file for orchestrator
        const { writeFileSync } = await import('fs');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');
        const needsActionPath = path.join(vaultPath, 'Needs_Action');
        const filename = `WHATSAPP_DASHBOARD_${cleanPhone}_${timestamp}.md`;
        const filepath = path.join(needsActionPath, filename);

        const content = `---
type: whatsapp
from: dashboard
to: ${phone}
priority: high
status: pending
created: ${new Date().toISOString()}
source: dashboard_direct_send_fallback
---

# WhatsApp Message Request from Dashboard (Queued)

**To:** ${phone}

## Message

${message}

## Note

Direct send failed: ${result.error}

This message will be processed by orchestrator.

---
*Created: ${new Date().toLocaleString()}*
`;

        writeFileSync(filepath, content, 'utf-8');

        return NextResponse.json({
          success: true,
          message: 'WhatsApp message queued for orchestrator (direct send unavailable)',
          fallback: true,
          filename: filename,
          error: result.error,
          note: 'Message will be sent when orchestrator processes the queue'
        });
      }

    } catch (execError: any) {
      console.error('Execution Error:', execError);

      return NextResponse.json(
        {
          error: 'Failed to send WhatsApp message: ' + execError.message,
          details: execError.stderr || execError.message
        },
        { status: 500 }
      );
    }

  } catch (error: any) {
    console.error('Error in send-whatsapp-direct:', error);
    return NextResponse.json(
      { error: 'Failed to process WhatsApp request: ' + error.message },
      { status: 500 }
    );
  }
}
