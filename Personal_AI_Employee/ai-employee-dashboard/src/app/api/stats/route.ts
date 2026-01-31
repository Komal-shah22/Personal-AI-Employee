import { NextResponse } from 'next/server';
import path from 'path';
import { countVaultFiles } from '@/lib/vault-reader';

export async function GET() {
  try {
    // Get the vault path from environment variable or default to parent directory
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    const pending = await countVaultFiles('Needs_Action', vaultPath);
    const inProgress = await countVaultFiles('Plans', vaultPath);
    const completed = await countVaultFiles('Done', vaultPath);
    const total = pending + inProgress + completed;

    // Calculate trends based on some mock logic
    // In a real implementation, you'd calculate actual trends from historical data
    const trends = {
      pendingChange: Math.floor(Math.random() * 25 - 10), // Random change between -10% and +15%
      inProgressChange: Math.floor(Math.random() * 20 - 10), // Random change between -10% and +10%
      completedChange: Math.floor(Math.random() * 30 - 5), // Random change between -5% and +25%
      totalChange: Math.floor(Math.random() * 20 - 5), // Random change between -5% and +15%
    };

    return NextResponse.json({
      pending,
      inProgress,
      completed,
      total,
      trends,
    });
  } catch (error) {
    console.error('Error fetching stats:', error);
    return NextResponse.json(
      { error: 'Failed to fetch stats' },
      { status: 500 }
    );
  }
}