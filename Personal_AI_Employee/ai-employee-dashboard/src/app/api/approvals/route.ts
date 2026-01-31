import { NextResponse } from 'next/server';
import path from 'path';
import { readVaultFiles } from '@/lib/vault-reader';
import { parseMarkdown, extractFileInfo } from '@/lib/markdown-parser';
import { moveFile } from '@/lib/file-mover';

export async function GET() {
  try {
    // Get the vault path from environment variable or default to parent directory
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    // Read files from Pending_Approval folder
    const files = await readVaultFiles('Pending_Approval', vaultPath);

    const approvals = files.map(file => {
      const { frontmatter, content } = parseMarkdown(file.content);

      return {
        id: file.fileName.replace('.md', ''),
        title: frontmatter.title || file.fileName.replace('.md', '').replace(/_/g, ' '),
        description: content.substring(0, 100) + (content.length > 100 ? '...' : ''),
        status: frontmatter.status || 'pending',
        requestedBy: frontmatter.requested_by || frontmatter.requester || 'Unknown',
        requestedAt: frontmatter.requested_at || frontmatter.created_at || new Date().toISOString(),
        expiresAt: frontmatter.expires_at || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(), // Default: 7 days from now
      };
    });

    // Filter only pending approvals
    const pendingApprovals = approvals.filter(approval => approval.status === 'pending');

    return NextResponse.json(pendingApprovals);
  } catch (error) {
    console.error('Error fetching approvals:', error);
    return NextResponse.json(
      { error: 'Failed to fetch approvals' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const { id, action } = await request.json();

    if (!id || !action) {
      return NextResponse.json(
        { error: 'Missing id or action' },
        { status: 400 }
      );
    }

    if (!['approve', 'reject'].includes(action)) {
      return NextResponse.json(
        { error: 'Action must be either "approve" or "reject"' },
        { status: 400 }
      );
    }

    // Get the vault path from environment variable or default to parent directory
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    // Verify the file exists in Pending_Approval before moving
    const fileName = `${id}.md`;
    const sourceDir = 'Pending_Approval';
    const destDir = action === 'approve' ? 'Approved' : 'Rejected';

    // Check if file exists in Pending_Approval
    const pendingFilePath = path.join(vaultPath, sourceDir, fileName);
    try {
      await import('fs/promises').then(fs => fs.access(pendingFilePath));
    } catch {
      return NextResponse.json(
        { error: `File ${fileName} not found in Pending_Approval` },
        { status: 404 }
      );
    }

    // Move the file
    const result = await moveFile(fileName, sourceDir, destDir, vaultPath);

    if (result.success) {
      return NextResponse.json({
        success: true,
        message: `Item ${action}d successfully`,
        action: action
      });
    } else {
      return NextResponse.json(
        { error: result.message },
        { status: 500 }
      );
    }
  } catch (error) {
    console.error('Error processing approval action:', error);
    return NextResponse.json(
      { error: 'Failed to process approval action' },
      { status: 500 }
    );
  }
}