import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Mock activity data (in production, this would come from logs or database)
    const activities = [
      {
        id: '1',
        timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
        agent: 'Gmail Watcher',
        agentIcon: '📧',
        action: 'Processed 3 new emails',
        status: 'success',
        details: '→ /Needs_Action/',
      },
      {
        id: '2',
        timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
        agent: 'Orchestrator',
        agentIcon: '🎛️',
        action: 'Generated invoice plan',
        status: 'success',
        details: 'Client: Acme Corp',
      },
      {
        id: '3',
        timestamp: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
        agent: 'WhatsApp Monitor',
        agentIcon: '💬',
        action: 'Detected urgent message',
        status: 'pending',
        details: 'Awaiting approval',
      },
      {
        id: '4',
        timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
        agent: 'LinkedIn Agent',
        agentIcon: '💼',
        action: 'Posted update',
        status: 'success',
        details: '12 views, 3 likes',
      },
      {
        id: '5',
        timestamp: new Date(Date.now() - 20 * 60 * 1000).toISOString(),
        agent: 'File Watcher',
        agentIcon: '📂',
        action: 'New file detected',
        status: 'info',
        details: 'report_Q1.pdf',
      },
    ];

    return NextResponse.json({ activities });
  } catch (error) {
    console.error('Activity stream error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch activities', activities: [] },
      { status: 500 }
    );
  }
}
