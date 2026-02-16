import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function GET() {
  try {
    // Try to get PM2 process list
    let agents = [];

    try {
      const { stdout } = await execAsync('pm2 jlist');
      const processes = JSON.parse(stdout);

      agents = [
        {
          id: 'gmail',
          name: 'Gmail Watcher',
          icon: '📧',
          status: processes.find((p: any) => p.name === 'gmail-watcher')?.pm2_env?.status === 'online' ? 'running' : 'stopped',
          lastActive: '2 minutes ago',
        },
        {
          id: 'whatsapp',
          name: 'WhatsApp Monitor',
          icon: '💬',
          status: processes.find((p: any) => p.name === 'whatsapp-watcher')?.pm2_env?.status === 'online' ? 'running' : 'stopped',
          lastActive: '5 minutes ago',
        },
        {
          id: 'file',
          name: 'File Watcher',
          icon: '📂',
          status: processes.find((p: any) => p.name === 'file-watcher')?.pm2_env?.status === 'online' ? 'running' : 'stopped',
          lastActive: '1 minute ago',
        },
        {
          id: 'linkedin',
          name: 'LinkedIn Agent',
          icon: '💼',
          status: processes.find((p: any) => p.name === 'linkedin-agent')?.pm2_env?.status === 'online' ? 'running' : 'stopped',
          lastActive: '10 minutes ago',
        },
        {
          id: 'orchestrator',
          name: 'Orchestrator',
          icon: '🎛️',
          status: processes.find((p: any) => p.name === 'orchestrator')?.pm2_env?.status === 'online' ? 'running' : 'stopped',
          lastActive: '30 seconds ago',
        },
      ];
    } catch (error) {
      // PM2 not available, return mock data
      agents = [
        { id: 'gmail', name: 'Gmail Watcher', icon: '📧', status: 'stopped', lastActive: '2 minutes ago' },
        { id: 'whatsapp', name: 'WhatsApp Monitor', icon: '💬', status: 'stopped', lastActive: '5 minutes ago' },
        { id: 'file', name: 'File Watcher', icon: '📂', status: 'stopped', lastActive: '1 minute ago' },
        { id: 'linkedin', name: 'LinkedIn Agent', icon: '💼', status: 'stopped', lastActive: '10 minutes ago' },
        { id: 'orchestrator', name: 'Orchestrator', icon: '🎛️', status: 'stopped', lastActive: '30 seconds ago' },
      ];
    }

    return NextResponse.json({
      agents,
      stats: {
        bronze: 5,
        silver: 4,
        gold: 5,
        platinum: 3,
        total: 17,
      },
    });
  } catch (error) {
    console.error('Status check error:', error);
    return NextResponse.json(
      { error: 'Failed to check status', agents: [] },
      { status: 500 }
    );
  }
}
