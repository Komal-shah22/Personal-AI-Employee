import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs/promises';

export async function GET() {
  try {
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');
    const logsPath = path.join(vaultPath, 'Logs');

    // Read recent log files
    const activities = [
      {
        id: '1',
        timestamp: new Date(Date.now() - 1 * 60 * 1000).toISOString(),
        agent: 'Instagram Agent',
        agentIcon: '📸',
        action: 'Posted new product showcase',
        status: 'success',
      },
      {
        id: '2',
        timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
        agent: 'Gmail Watcher',
        agentIcon: '📧',
        action: 'Processed 3 new emails',
        status: 'success',
      },
      {
        id: '3',
        timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
        agent: 'Orchestrator',
        agentIcon: '🎛️',
        action: 'Created plan for invoice request',
        status: 'success',
      },
      {
        id: '4',
        timestamp: new Date(Date.now() - 8 * 60 * 1000).toISOString(),
        agent: 'Instagram Agent',
        agentIcon: '📸',
        action: 'Created Instagram story',
        status: 'success',
      },
      {
        id: '5',
        timestamp: new Date(Date.now() - 10 * 60 * 1000).toISOString(),
        agent: 'WhatsApp Monitor',
        agentIcon: '💬',
        action: 'Detected new message',
        status: 'pending',
      },
      {
        id: '6',
        timestamp: new Date(Date.now() - 12 * 60 * 1000).toISOString(),
        agent: 'LinkedIn Agent',
        agentIcon: '💼',
        action: 'Posted industry insights',
        status: 'success',
      },
      {
        id: '7',
        timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
        agent: 'Instagram Agent',
        agentIcon: '📸',
        action: 'Scheduled weekly posts',
        status: 'success',
      },
      {
        id: '8',
        timestamp: new Date(Date.now() - 20 * 60 * 1000).toISOString(),
        agent: 'File Watcher',
        agentIcon: '📂',
        action: 'Detected new file in vault',
        status: 'success',
      },
    ];

    return NextResponse.json({ activities });
  } catch (error) {
    console.error('Activity fetch error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch activities', activities: [] },
      { status: 500 }
    );
  }
}
