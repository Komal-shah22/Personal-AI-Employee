import { NextResponse } from 'next/server';
import path from 'path';
import { readVaultFiles } from '@/lib/vault-reader';
import { parseMarkdown, extractFileInfo } from '@/lib/markdown-parser';

export async function GET() {
  try {
    // Get the vault path from environment variable or default to parent directory
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    // Read files from Needs_Action folder (where emails would be stored)
    const files = await readVaultFiles('Needs_Action', vaultPath);

    // Filter for email files (assuming they start with EMAIL_)
    const emailFiles = files.filter(file =>
      file.fileName.startsWith('EMAIL_')
    );

    const emails = emailFiles.map(file => {
      const { frontmatter, content } = parseMarkdown(file.content);

      // Extract preview from the first 100 characters of content
      const preview = content.substring(0, 100) + (content.length > 100 ? '...' : '');

      return {
        id: file.fileName.replace('.md', ''),
        from: frontmatter.from || 'Unknown Sender',
        subject: frontmatter.subject || file.fileName.replace('EMAIL_', '').replace('.md', ''),
        preview,
        priority: frontmatter.priority || 'normal',
        time: frontmatter.timestamp || frontmatter.created_at || new Date().toISOString(),
        unread: true, // All emails from vault are considered unread initially
      };
    });

    // Sort by priority and then by time (newest first)
    const priorityOrder = { urgent: 1, high: 2, normal: 3 };
    emails.sort((a, b) => {
      const priorityDiff = priorityOrder[a.priority] - priorityOrder[b.priority];
      if (priorityDiff !== 0) return priorityDiff;
      return new Date(b.time).getTime() - new Date(a.time).getTime();
    });

    return NextResponse.json(emails);
  } catch (error) {
    console.error('Error fetching emails:', error);
    return NextResponse.json(
      { error: 'Failed to fetch emails' },
      { status: 500 }
    );
  }
}