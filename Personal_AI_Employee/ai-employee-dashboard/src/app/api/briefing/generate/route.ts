import { NextResponse } from 'next/server';
import { exec } from 'child_process';
import path from 'path';

export async function POST() {
  try {
    const briefingPath = process.env.SCRIPTS_PATH
      ? path.join(process.env.SCRIPTS_PATH, 'ceo_briefing.py')
      : path.join(process.cwd(), '..', 'ceo_briefing.py');

    const command = `python "${briefingPath}"`;

    // Run briefing generation in background
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error('Briefing generation error:', error);
      }
    });

    return NextResponse.json({
      success: true,
      message: 'CEO briefing generation started',
      jobId: Date.now().toString(),
      status: 'running',
    });
  } catch (error) {
    console.error('Briefing generation error:', error);
    return NextResponse.json(
      { error: 'Failed to generate briefing' },
      { status: 500 }
    );
  }
}
