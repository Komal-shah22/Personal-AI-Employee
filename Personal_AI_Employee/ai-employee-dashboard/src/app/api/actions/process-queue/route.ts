import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import path from 'path';

export async function POST() {
  try {
    const orchestratorPath = process.env.SCRIPTS_PATH
      ? path.join(process.env.SCRIPTS_PATH, 'orchestrator.py')
      : path.join(process.cwd(), '..', 'orchestrator.py');

    const command = `python "${orchestratorPath}"`;

    // Run orchestrator in background
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error('Orchestrator error:', error);
      }
    });

    return NextResponse.json({
      success: true,
      started: true,
      message: 'Orchestrator started processing queue',
      queueSize: 0,
    });
  } catch (error) {
    console.error('Process queue error:', error);
    return NextResponse.json(
      { error: 'Failed to start orchestrator' },
      { status: 500 }
    );
  }
}
