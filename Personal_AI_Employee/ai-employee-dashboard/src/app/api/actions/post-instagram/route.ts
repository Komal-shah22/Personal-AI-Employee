import { NextRequest, NextResponse } from 'next/server';
import { writeFileSync } from 'fs';
import { join } from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import { getPythonCommand } from '@/lib/python-runner';

const execAsync = promisify(exec);

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { caption, imageUrl } = body;

    // Validate required fields
    if (!caption) {
      return NextResponse.json(
        { error: 'Caption is required' },
        { status: 400 }
      );
    }

    // Validate caption length (Instagram limit is 2200 characters)
    if (caption.length > 2200) {
      return NextResponse.json(
        { error: 'Caption exceeds Instagram limit of 2200 characters' },
        { status: 400 }
      );
    }

    // Use Playwright for direct posting (most reliable method)
    const scriptPath = join(process.cwd(), '..', 'playwright_instagram_post.py');
    const parentDir = join(process.cwd(), '..');

    // Create a temporary Python script that modifies the post content
    const tempScriptPath = join(parentDir, 'temp_instagram_post.py');
    const escapedCaption = caption.replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n');
    const escapedImageUrl = imageUrl ? imageUrl.replace(/\\/g, '\\\\').replace(/"/g, '\\"') : '';

    const tempScriptContent = `
import sys
sys.path.insert(0, '${parentDir.replace(/\\/g, '/')}')

# Import the instagram script but override the caption
import playwright_instagram_post as p

# Override the caption and image
p.POST_TEXT = """${escapedCaption}"""
${imageUrl ? `p.IMAGE_URL = "${escapedImageUrl}"` : '# No image URL provided'}

# Run the main function
p.main(${imageUrl ? `image_url="${escapedImageUrl}"` : ''}, caption="""${escapedCaption}""")
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
      if (stdout.includes('SUCCESS') || stdout.includes('COMPLETED') || stdout.includes('Done')) {
        return NextResponse.json({
          success: true,
          message: 'Instagram post created successfully!',
          details: {
            postedAt: new Date().toISOString(),
            method: 'playwright_automation',
            hasImage: !!imageUrl
          }
        });
      } else {
        throw new Error('Playwright script completed but did not report success');
      }
    } catch (execError: any) {
      console.error('Instagram posting error:', execError.message);

      // Clean up temp script on error
      try {
        const fs = require('fs');
        fs.unlinkSync(tempScriptPath);
      } catch {}

      throw execError;
    }

  } catch (error: any) {
    console.error('Error posting to Instagram:', error);
    return NextResponse.json(
      { error: 'Failed to post to Instagram: ' + error.message },
      { status: 500 }
    );
  }
}