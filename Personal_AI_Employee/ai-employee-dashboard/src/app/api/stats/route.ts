import { NextResponse } from 'next/server';
import path from 'path';
import { countVaultFiles } from '@/lib/vault-reader';

// Store historical data in memory for trend calculation (in production, you'd use a database)
let historicalData: { timestamp: number; stats: { pending: number; inProgress: number; completed: number; total: number } }[] = [];

export async function GET() {
  try {
    // Get the vault path from environment variable or default to parent directory
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    const pending = await countVaultFiles('Needs_Action', vaultPath);
    const inProgress = await countVaultFiles('Plans', vaultPath);
    const completed = await countVaultFiles('Done', vaultPath);
    const total = pending + inProgress + completed;

    const currentStats = {
      pending,
      inProgress,
      completed,
      total,
    };

    // Store current data for trend calculation
    const now = Date.now();
    historicalData.push({ timestamp: now, stats: currentStats });

    // Keep only the last hour of data to prevent memory issues
    const oneHourAgo = now - (60 * 60 * 1000);
    historicalData = historicalData.filter(item => item.timestamp > oneHourAgo);

    // Calculate trends based on historical data
    const trends = calculateTrends(historicalData, currentStats);

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

function calculateTrends(historicalData: typeof historicalData, currentStats: { pending: number; inProgress: number; completed: number; total: number }) {
  if (historicalData.length < 2) {
    // If not enough historical data, return neutral trends
    return {
      pendingChange: 0,
      inProgressChange: 0,
      completedChange: 0,
      totalChange: 0,
    };
  }

  // Get the data from 10 minutes ago or the oldest available data
  const tenMinutesAgo = Date.now() - (10 * 60 * 1000);
  const pastData = historicalData.find(item => item.timestamp < tenMinutesAgo) || historicalData[0];

  const calculateChange = (current: number, past: number) => {
    if (past === 0) return current > 0 ? 100 : 0;
    return Math.round(((current - past) / past) * 100);
  };

  return {
    pendingChange: calculateChange(currentStats.pending, pastData.stats.pending),
    inProgressChange: calculateChange(currentStats.inProgress, pastData.stats.inProgress),
    completedChange: calculateChange(currentStats.completed, pastData.stats.completed),
    totalChange: calculateChange(currentStats.total, pastData.stats.total),
  };
}