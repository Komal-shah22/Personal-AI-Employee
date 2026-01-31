import { NextResponse } from 'next/server';
import path from 'path';
import { readVaultFiles } from '@/lib/vault-reader';

export async function GET() {
  try {
    // Get the vault path from environment variable or default to parent directory
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    // Read files from all relevant vault directories to get recent activity
    const needsActionFiles = await readVaultFiles('Needs_Action', vaultPath);
    const doneFiles = await readVaultFiles('Done', vaultPath);
    const plansFiles = await readVaultFiles('Plans', vaultPath);
    const pendingApprovalFiles = await readVaultFiles('Pending_Approval', vaultPath);

    // Combine all files and sort by creation/modification time
    let allFiles = [
      ...needsActionFiles.map(file => ({ ...file, category: 'task', action: 'pending' })),
      ...doneFiles.map(file => ({ ...file, category: 'task', action: 'completed' })),
      ...plansFiles.map(file => ({ ...file, category: 'plan', action: 'created' })),
      ...pendingApprovalFiles.map(file => ({ ...file, category: 'approval', action: 'requested' }))
    ];

    // Sort by modification time (most recent first)
    allFiles.sort((a, b) => {
      const timeA = a.frontmatter.timestamp ? new Date(a.frontmatter.timestamp).getTime() : new Date(a.filePath).getTime();
      const timeB = b.frontmatter.timestamp ? new Date(b.frontmatter.timestamp).getTime() : new Date(b.filePath).getTime();
      return timeB - timeA;
    });

    // Take the 10 most recent activities
    const recentActivities = allFiles.slice(0, 10);

    // Convert to activity feed format
    const activities = recentActivities.map(async (file, index) => {
      // Safely get timestamp from frontmatter or file modification time
      let timestamp = file.frontmatter.timestamp;
      if (!timestamp || isNaN(new Date(timestamp).getTime())) {
        // If timestamp in frontmatter is invalid, use file modification time
        try {
          const fs = await import('fs/promises');
          const stats = await fs.stat(file.filePath);
          timestamp = new Date(stats.mtime).toISOString();
        } catch (e) {
          // Fallback to current time if we can't get file stats
          timestamp = new Date().toISOString();
        }
      }

      let title = '';
      let description = '';

      // Determine title and description based on file type and content
      if (file.frontmatter.subject) {
        title = file.frontmatter.subject;
      } else if (file.fileName.startsWith('EMAIL_')) {
        title = 'Email processed';
        description = file.frontmatter.subject || file.fileName;
      } else if (file.fileName.startsWith('PLAN_')) {
        title = 'Plan created';
        description = file.fileName;
      } else if (file.fileName.startsWith('APPROVAL_')) {
        title = 'Approval requested';
        description = file.fileName;
      } else {
        title = 'Task updated';
        description = file.fileName;
      }

      // Determine type based on category
      let type: 'email' | 'task' | 'approval' | 'plan' = 'task';
      if (file.category === 'email') type = 'email';
      else if (file.category === 'approval') type = 'approval';
      else if (file.category === 'plan') type = 'plan';

      return {
        id: `${index}-${timestamp}`,
        title,
        description,
        time: timestamp,
        type,
        icon: null, // Will be determined client-side
      };
    });

    // Resolve all promises
    const resolvedActivities = await Promise.all(activities);

    return NextResponse.json({
      activities: resolvedActivities,
    });
  } catch (error) {
    console.error('Error fetching activities:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch activities',
        activities: []
      },
      { status: 500 }
    );
  }
}