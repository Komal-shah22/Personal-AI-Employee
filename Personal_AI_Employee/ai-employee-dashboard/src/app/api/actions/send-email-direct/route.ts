import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import { safeParseJSON } from '@/lib/json-parser';

const execAsync = promisify(exec);

// Get the correct Python command for the platform
function getPythonCommand(): string {
  // On Windows, use the full Python path to avoid issues with the py launcher
  if (process.platform === 'win32') {
    return 'python';
  }
  return 'python3';
}

export async function POST(request: NextRequest) {
  try {
    const { to, subject, body } = await request.json();

    // Validate input
    if (!to || !subject || !body) {
      return NextResponse.json(
        { error: 'Missing required fields: to, subject, body' },
        { status: 400 }
      );
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(to)) {
      return NextResponse.json(
        { error: 'Invalid email address format' },
        { status: 400 }
      );
    }

    // Path to Python script
    const scriptPath = path.join(process.cwd(), '..', 'send_email_direct.py');
    const pythonCmd = getPythonCommand();

    // Escape arguments for shell
    const escapedTo = to.replace(/"/g, '\\"');
    const escapedSubject = subject.replace(/"/g, '\\"');
    const escapedBody = body.replace(/"/g, '\\"');

    try {
      // Call Python script to send email directly
      const { stdout, stderr } = await execAsync(
        `${pythonCmd} "${scriptPath}" "${escapedTo}" "${escapedSubject}" "${escapedBody}"`,
        {
          timeout: 30000,
          maxBuffer: 1024 * 1024
        }
      );

      const result = safeParseJSON(stdout);

      if (result.success) {
        return NextResponse.json({
          success: true,
          message: 'Email sent successfully via Gmail API',
          details: {
            to: result.to,
            subject: result.subject,
            messageId: result.message_id,
            sentAt: result.sent_at,
            method: 'direct_gmail_api'
          }
        });
      } else {
        // If direct send failed, create file for orchestrator
        const { writeFileSync } = await import('fs');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');
        const needsActionPath = path.join(vaultPath, 'Needs_Action');
        const filename = `EMAIL_DASHBOARD_${to.split('@')[0]}_${timestamp}.md`;
        const filepath = path.join(needsActionPath, filename);

        const content = `---
type: email
from: dashboard
to: ${to}
subject: ${subject}
priority: high
status: pending
created: ${new Date().toISOString()}
source: dashboard_direct_send_fallback
---

# Email Request from Dashboard (Queued)

**To:** ${to}
**Subject:** ${subject}

## Message Body

${body}

## Note

Direct send failed: ${result.error}

This email will be processed by orchestrator.

---
*Created: ${new Date().toLocaleString()}*
`;

        writeFileSync(filepath, content, 'utf-8');

        return NextResponse.json({
          success: true,
          message: 'Email queued for orchestrator (direct send unavailable)',
          fallback: true,
          filename: filename,
          error: result.error,
          note: 'Email will be sent when orchestrator processes the queue'
        });
      }

    } catch (execError: any) {
      console.error('Execution Error:', execError);

      return NextResponse.json(
        {
          error: 'Failed to send email: ' + execError.message,
          details: execError.stderr || execError.message
        },
        { status: 500 }
      );
    }

  } catch (error: any) {
    console.error('Error in send-email-direct:', error);
    return NextResponse.json(
      { error: 'Failed to process email request: ' + error.message },
      { status: 500 }
    );
  }
}

