import { NextResponse } from 'next/server';
import path from 'path';
import { readVaultFiles } from '@/lib/vault-reader';
import { parseMarkdown, extractFileInfo } from '@/lib/markdown-parser';

export async function GET() {
  try {
    // Get the vault path from environment variable or default to parent directory
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    const folders = ['Needs_Action', 'Plans', 'Done'];
    const allTasks = [];

    for (const folder of folders) {
      const files = await readVaultFiles(folder, vaultPath);

      files.forEach(file => {
        const { frontmatter, content } = parseMarkdown(file.content);

        // Determine status based on folder
        let status = 'inbox';
        if (folder === 'Plans') status = 'progress';
        if (folder === 'Done') status = 'done';

        // Extract title from filename or frontmatter
        const title = frontmatter.title || file.fileName.replace('.md', '').replace(/_/g, ' ');

        allTasks.push({
          id: `${folder}_${file.fileName}`,
          title,
          description: content.substring(0, 100) + (content.length > 100 ? '...' : ''),
          status,
          priority: frontmatter.priority || 'medium',
          assignee: frontmatter.assignee || 'AI Employee',
          dueDate: frontmatter.due_date || frontmatter.deadline || frontmatter.created_at || new Date().toISOString(),
        });
      });
    }

    return NextResponse.json(allTasks);
  } catch (error) {
    console.error('Error fetching tasks:', error);
    return NextResponse.json(
      { error: 'Failed to fetch tasks' },
      { status: 500 }
    );
  }
}