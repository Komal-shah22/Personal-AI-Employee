import { NextRequest, NextResponse } from 'next/server';
import { writeFileSync } from 'fs';
import { join } from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import { getPythonCommand } from '@/lib/python-runner';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  let content = '';
  let imageUrl = '';
  let postType = '';

  try {
    const data = await request.json();
    content = data.content || '';
    imageUrl = data.imageUrl || '';
    postType = data.postType || '';

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

    // Use Playwright for direct posting (most reliable method)
    const scriptPath = join(process.cwd(), '..', 'playwright_linkedin_post.py');
    const parentDir = join(process.cwd(), '..');

    // Create a temporary Python script that modifies the post content
    const tempScriptPath = join(parentDir, 'temp_linkedin_post.py');
    const escapedContent = content.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');

    const tempScriptContent = `
import sys
sys.path.insert(0, '${parentDir.replace(/\\/g, '/')}')

# Import the playwright script but override the post text
import playwright_linkedin_post as p

# Override the post text
p.POST_TEXT = """${escapedContent}"""

# Run the main function
p.main()
`;

    try {
      // Write temp script
      writeFileSync(tempScriptPath, tempScriptContent, 'utf-8');

      // Execute the Playwright script
      const pythonCmd = getPythonCommand();
      const { stdout, stderr } = await execAsync(`${pythonCmd} "${tempScriptPath}"`, {
        cwd: parentDir,
        timeout: 120000, // 2 minutes for browser automation
        maxBuffer: 1024 * 1024
      });

      // Clean up temp script
      try {
        const fs = require('fs');
        fs.unlinkSync(tempScriptPath);
      } catch {}

      // Check if successful
      if (stdout.includes('SUCCESS') || stdout.includes('Done')) {
        return NextResponse.json({
          success: true,
          message: 'LinkedIn post published successfully!',
          details: {
            postedAt: new Date().toISOString(),
            method: 'playwright_automation',
            postType: postType || 'General'
          }
        });
      } else {
        throw new Error('Playwright script completed but did not report success');
      }
    } catch (execError: any) {
      console.error('Playwright posting error:', execError.message);

      // Clean up temp script on error
      try {
        const fs = require('fs');
        fs.unlinkSync(tempScriptPath);
      } catch {}

      throw execError;
    }

  } catch (error: any) {
    console.error('Error posting to LinkedIn:', error);

    // Fall back to queue method
    try {
      // Create timestamp
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);

      // Create action file in Needs_Action folder
      const vaultPath = process.env.VAULT_PATH || join(process.cwd(), '..', 'AI_Employee_Vault');
      const needsActionPath = join(vaultPath, 'Needs_Action');

      // Ensure directory exists
      try {
        const fs = require('fs');
        fs.mkdirSync(needsActionPath, { recursive: true });
      } catch {}

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
---

# LinkedIn Post Request from Dashboard

## Post Content

${content}

## Action Required

This LinkedIn post was created via the dashboard quick action form and requires processing by the orchestrator.

**Character Count:** ${content.length} / 3000

**Note:** Direct posting failed: ${error.message}

---
*Created: ${new Date().toLocaleString()}*
`;

      // Write file to Needs_Action
      writeFileSync(filepath, fileContent, 'utf-8');

      return NextResponse.json({
        success: true,
        message: 'LinkedIn post queued (direct posting failed)',
        filename: filename,
        status: 'pending_orchestrator',
        characterCount: content.length,
        fallback: true,
        error: error.message
      });
    } catch (fallbackError) {
      console.error('Fallback queue creation also failed:', fallbackError);
    }

    return NextResponse.json(
      { error: 'Failed to post to LinkedIn: ' + error.message },
      { status: 500 }
    );
  }
}
