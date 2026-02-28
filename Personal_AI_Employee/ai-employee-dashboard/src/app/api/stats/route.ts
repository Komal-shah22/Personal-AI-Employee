import { NextResponse } from 'next/server';
import path from 'path';
import { countVaultFiles } from '@/lib/vault-reader';

// Store historical data in memory for trend calculation (in production, you'd use a database)
interface HistoricalDataPoint {
  timestamp: number;
  stats: {
    pending: number;
    inProgress: number;
    completed: number;
    total: number;
    social?: {
      instagramFollowers: number;
      linkedinFollowers: number;
      totalPosts: number;
      engagementRate: number;
    };
  };
}

let historicalData: HistoricalDataPoint[] = [];

export async function GET() {
  try {
    // Get the vault path from environment variable or default to parent directory
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    const pending = await countVaultFiles('Needs_Action', vaultPath);
    const inProgress = await countVaultFiles('Plans', vaultPath);
    const completed = await countVaultFiles('Done', vaultPath);
    const total = pending + inProgress + completed;

    // Get social media metrics (simulated)
    const socialMetrics = {
      instagramFollowers: 1245,
      linkedinFollowers: 876,
      totalPosts: 42,
      engagementRate: 4.8
    };

    const currentStats = {
      pending,
      inProgress,
      completed,
      total,
      social: socialMetrics
    };

    // Store current data for trend calculation
    const now = Date.now();
    historicalData.push({ timestamp: now, stats: currentStats });

    // Keep only the last hour of data to prevent memory issues
    const oneHourAgo = now - (60 * 60 * 1000);
    historicalData = historicalData.filter((item: HistoricalDataPoint) => item.timestamp > oneHourAgo);

    // Calculate trends based on historical data
    const trends = calculateTrends(historicalData, currentStats);

    return NextResponse.json({
      pending,
      inProgress,
      completed,
      total,
      social: socialMetrics,
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

function calculateTrends(historicalData: HistoricalDataPoint[], currentStats: { pending: number; inProgress: number; completed: number; total: number; social?: any }) {
  if (historicalData.length < 2) {
    // If not enough historical data, return neutral trends
    return {
      pendingChange: 0,
      inProgressChange: 0,
      completedChange: 0,
      totalChange: 0,
      instagramGrowth: 0,
      linkedinGrowth: 0,
      postGrowth: 0,
      engagementChange: 0,
    };
  }

  // Get the data from 10 minutes ago or the oldest available data
  const tenMinutesAgo = Date.now() - (10 * 60 * 1000);
  const pastData = historicalData.find((item: HistoricalDataPoint) => item.timestamp < tenMinutesAgo) || historicalData[0];

  const calculateChange = (current: number, past: number) => {
    if (past === 0) return current > 0 ? 100 : 0;
    return Math.round(((current - past) / past) * 100);
  };

  // Calculate task trends
  const taskTrends = {
    pendingChange: calculateChange(currentStats.pending, pastData.stats.pending),
    inProgressChange: calculateChange(currentStats.inProgress, pastData.stats.inProgress),
    completedChange: calculateChange(currentStats.completed, pastData.stats.completed),
    totalChange: calculateChange(currentStats.total, pastData.stats.total),
  };

  // Calculate social media trends if social data exists
  if (currentStats.social && pastData.stats.social) {
    return {
      ...taskTrends,
      instagramGrowth: calculateChange(currentStats.social.instagramFollowers, pastData.stats.social.instagramFollowers),
      linkedinGrowth: calculateChange(currentStats.social.linkedinFollowers, pastData.stats.social.linkedinFollowers),
      postGrowth: calculateChange(currentStats.social.totalPosts, pastData.stats.social.totalPosts),
      engagementChange: calculateChange(currentStats.social.engagementRate, pastData.stats.social.engagementRate),
    };
  }

  // Return task trends only if no social data
  return {
    ...taskTrends,
    instagramGrowth: 0,
    linkedinGrowth: 0,
    postGrowth: 0,
    engagementChange: 0,
  };
}