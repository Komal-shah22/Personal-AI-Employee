import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const { action } = await request.json();
    const agentId = params.id;

    // Map agent IDs to PM2 process names
    const processMap: Record<string, string> = {
      gmail: 'gmail-watcher',
      whatsapp: 'whatsapp-watcher',
      linkedin: 'linkedin-agent',
      file: 'file-watcher',
      orchestrator: 'orchestrator',
    };

    const processName = processMap[agentId];
    if (!processName) {
      return NextResponse.json(
        { error: 'Invalid agent ID' },
        { status: 400 }
      );
    }

    let command = '';
    switch (action) {
      case 'start':
        command = `pm2 start ${processName}`;
        break;
      case 'stop':
        command = `pm2 stop ${processName}`;
        break;
      case 'restart':
        command = `pm2 restart ${processName}`;
        break;
      default:
        return NextResponse.json(
          { error: 'Invalid action' },
          { status: 400 }
        );
    }

    await execAsync(command);

    return NextResponse.json({
      success: true,
      message: `Agent ${action}ed successfully`,
    });
  } catch (error) {
    console.error('Agent action error:', error);
    return NextResponse.json(
      { error: 'Failed to execute action' },
      { status: 500 }
    );
  }
}
