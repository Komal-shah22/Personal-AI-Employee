import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs/promises';

export async function GET() {
  try {
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    // Count files in different folders
    const needsAction = await countFiles(path.join(vaultPath, 'Needs_Action'));
    const plans = await countFiles(path.join(vaultPath, 'Plans'));
    const done = await countFiles(path.join(vaultPath, 'Done'));
    const pendingApprovals = await countFiles(path.join(vaultPath, 'Pending_Approval'));

    // Mock agent data (in production, this would come from PM2 or process manager)
    const agents = [
      {
        id: 'gmail',
        name: 'Gmail Watcher',
        icon: '📧',
        status: 'running',
        lastActive: '2 min ago',
        stats: { processed: 45, label: 'Emails today' },
      },
      {
        id: 'whatsapp',
        name: 'WhatsApp Monitor',
        icon: '💬',
        status: 'running',
        lastActive: '5 min ago',
        stats: { processed: 12, label: 'Messages today' },
      },
      {
        id: 'linkedin',
        name: 'LinkedIn Agent',
        icon: '💼',
        status: 'stopped',
        lastActive: '2 hours ago',
        stats: { processed: 3, label: 'Posts today' },
      },
      {
        id: 'file',
        name: 'File Watcher',
        icon: '📂',
        status: 'running',
        lastActive: '1 min ago',
        stats: { processed: 8, label: 'Files processed' },
      },
      {
        id: 'orchestrator',
        name: 'Orchestrator',
        icon: '🎛️',
        status: 'running',
        lastActive: '30 sec ago',
        stats: { processed: 23, label: 'Tasks completed' },
      },
    ];

    return NextResponse.json({
      metrics: {
        tasksToday: done,
        activeAgents: agents.filter(a => a.status === 'running').length,
        pendingApprovals,
        systemHealth: 98,
      },
      agents,
    });
  } catch (error) {
    console.error('Dashboard API error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch dashboard data' },
      { status: 500 }
    );
  }
}

async function countFiles(dirPath: string): Promise<number> {
  try {
    const files = await fs.readdir(dirPath);
    return files.filter(f => f.endsWith('.md')).length;
  } catch {
    return 0;
  }
}
