import { NextRequest, NextResponse } from 'next/server';
import { writeFileSync } from 'fs';
import { join } from 'path';

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

    // Create timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);

    // Create action file in Needs_Action folder
    const vaultPath = process.env.VAULT_PATH || join(process.cwd(), '..', 'AI_Employee_Vault');
    const needsActionPath = join(vaultPath, 'Needs_Action');

    const filename = `EMAIL_DASHBOARD_${to.split('@')[0]}_${timestamp}.md`;
    const filepath = join(needsActionPath, filename);

    const content = `---
type: email
from: dashboard
to: ${to}
subject: ${subject}
priority: normal
status: pending
created: ${new Date().toISOString()}
source: dashboard_quick_action
---

# Email Request from Dashboard

**To:** ${to}
**Subject:** ${subject}

## Message Body

${body}

## Action Required

This email was created via the dashboard quick action form and requires processing by the orchestrator.

---
*Created: ${new Date().toLocaleString()}*
`;

    // Write file to Needs_Action
    writeFileSync(filepath, content, 'utf-8');

    return NextResponse.json({
      success: true,
      message: 'Email request created successfully',
      filename: filename,
      status: 'pending_orchestrator'
    });

  } catch (error) {
    console.error('Error creating email request:', error);
    return NextResponse.json(
      { error: 'Failed to create email request' },
      { status: 500 }
    );
  }
}
