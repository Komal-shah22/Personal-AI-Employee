import { NextRequest, NextResponse } from 'next/server';
import { writeFileSync } from 'fs';
import { join } from 'path';

export async function POST(request: NextRequest) {
  try {
    const { content, imageUrl } = await request.json();

    // Validate input
    if (!content) {
      return NextResponse.json(
        { error: 'Missing required field: content' },
        { status: 400 }
      );
    }

    // Validate content length (LinkedIn limit is 3000 characters)
    if (content.length > 3000) {
      return NextResponse.json(
        { error: 'Content exceeds LinkedIn limit of 3000 characters' },
        { status: 400 }
      );
    }

    // Validate image URL if provided
    if (imageUrl) {
      try {
        new URL(imageUrl);
      } catch {
        return NextResponse.json(
          { error: 'Invalid image URL format' },
          { status: 400 }
        );
      }
    }

    // Create timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);

    // Create action file in Needs_Action folder
    const vaultPath = process.env.VAULT_PATH || join(process.cwd(), '..', 'AI_Employee_Vault');
    const needsActionPath = join(vaultPath, 'Needs_Action');

    const filename = `LINKEDIN_DASHBOARD_${timestamp}.md`;
    const filepath = join(needsActionPath, filename);

    const fileContent = `---
type: social_post
platform: linkedin
from: dashboard
priority: normal
status: pending
created: ${new Date().toISOString()}
source: dashboard_quick_action
${imageUrl ? `image_url: ${imageUrl}` : ''}
---

# LinkedIn Post Request from Dashboard

## Post Content

${content}

${imageUrl ? `## Image\n\n![Post Image](${imageUrl})\n` : ''}

## Action Required

This LinkedIn post was created via the dashboard quick action form and requires processing by the orchestrator.

**Character Count:** ${content.length} / 3000

---
*Created: ${new Date().toLocaleString()}*
`;

    // Write file to Needs_Action
    writeFileSync(filepath, fileContent, 'utf-8');

    return NextResponse.json({
      success: true,
      message: 'LinkedIn post request created successfully',
      filename: filename,
      status: 'pending_orchestrator',
      characterCount: content.length,
      note: 'Post will be published when orchestrator processes the queue'
    });

  } catch (error) {
    console.error('Error creating LinkedIn post request:', error);
    return NextResponse.json(
      { error: 'Failed to create LinkedIn post request' },
      { status: 500 }
    );
  }
}
