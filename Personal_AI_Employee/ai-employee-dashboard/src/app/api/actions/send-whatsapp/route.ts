import { NextRequest, NextResponse } from 'next/server';
import { writeFileSync } from 'fs';
import { join } from 'path';

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
    if (!phoneRegex.test(phone.replace(/[\s-]/g, ''))) {
      return NextResponse.json(
        { error: 'Invalid phone number format. Use international format with country code (e.g., +923001234567)' },
        { status: 400 }
      );
    }

    // Create timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);

    // Create action file in Needs_Action folder
    const vaultPath = process.env.VAULT_PATH || join(process.cwd(), '..', 'AI_Employee_Vault');
    const needsActionPath = join(vaultPath, 'Needs_Action');

    const sanitizedPhone = phone.replace(/[^0-9+]/g, '');
    const filename = `WHATSAPP_DASHBOARD_${sanitizedPhone}_${timestamp}.md`;
    const filepath = join(needsActionPath, filename);

    const content = `---
type: whatsapp
from: dashboard
to: ${phone}
priority: normal
status: pending
created: ${new Date().toISOString()}
source: dashboard_quick_action
---

# WhatsApp Message Request from Dashboard

**To:** ${phone}

## Message

${message}

## Action Required

This WhatsApp message was created via the dashboard quick action form and requires processing by the orchestrator.

**Note:** Make sure WhatsApp Web session is active before sending.

---
*Created: ${new Date().toLocaleString()}*
`;

    // Write file to Needs_Action
    writeFileSync(filepath, content, 'utf-8');

    return NextResponse.json({
      success: true,
      message: 'WhatsApp message request created successfully',
      filename: filename,
      status: 'pending_orchestrator',
      note: 'Message will be sent when orchestrator processes the queue'
    });

  } catch (error) {
    console.error('Error creating WhatsApp request:', error);
    return NextResponse.json(
      { error: 'Failed to create WhatsApp message request' },
      { status: 500 }
    );
  }
}
