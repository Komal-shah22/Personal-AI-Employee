import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function GET() {
  try {
    let services = [];

    try {
      // Get PM2 process list
      const { stdout } = await execAsync('pm2 jlist');
      const processes = JSON.parse(stdout);

      services = processes.map((proc: any) => ({
        name: proc.name,
        status: proc.pm2_env.status === 'online' ? 'healthy' : 'unhealthy',
        uptime: proc.pm2_env.pm_uptime,
        restarts: proc.pm2_env.restart_time,
        cpu: proc.monit.cpu,
        memory: proc.monit.memory,
      }));
    } catch (error) {
      // PM2 not available
      services = [
        { name: 'gmail-watcher', status: 'unknown', uptime: 0, restarts: 0, cpu: 0, memory: 0 },
        { name: 'whatsapp-watcher', status: 'unknown', uptime: 0, restarts: 0, cpu: 0, memory: 0 },
        { name: 'orchestrator', status: 'unknown', uptime: 0, restarts: 0, cpu: 0, memory: 0 },
      ];
    }

    const overall = services.every((s: any) => s.status === 'healthy') ? 'healthy' : 'degraded';

    return NextResponse.json({
      services,
      overall,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Health check error:', error);
    return NextResponse.json(
      { error: 'Failed to check health', services: [], overall: 'unhealthy' },
      { status: 500 }
    );
  }
}

export async function POST() {
  // Same as GET for now
  return GET();
}
