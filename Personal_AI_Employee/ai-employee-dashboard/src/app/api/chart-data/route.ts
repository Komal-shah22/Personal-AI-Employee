import { NextResponse } from 'next/server';
import path from 'path';
import { readVaultFiles } from '@/lib/vault-reader';
import { parseMarkdown } from '@/lib/markdown-parser';

export async function GET() {
  try {
    // Get the vault path from environment variable or default to parent directory
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');

    // Read files from different vault directories
    const needsActionFiles = await readVaultFiles('Needs_Action', vaultPath);
    const plansFiles = await readVaultFiles('Plans', vaultPath);
    const doneFiles = await readVaultFiles('Done', vaultPath);

    // Count files by date for the last 7 days
    const now = new Date();
    const sevenDaysAgo = new Date(now);
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

    // Helper function to get date string in 'YYYY-MM-DD' format
    const getDateStr = (date: Date) => date.toISOString().split('T')[0];

    // Create an object to store counts per day
    const dateCounts: Record<string, { pending: number; inProgress: number; completed: number }> = {};

    // Initialize all dates in the range
    for (let d = new Date(sevenDaysAgo); d <= now; d.setDate(d.getDate() + 1)) {
      const dateStr = getDateStr(d);
      dateCounts[dateStr] = { pending: 0, inProgress: 0, completed: 0 };
    }

    // Count files by date
    const fs = await import('fs/promises');

    for (const file of needsActionFiles) {
      const stat = await fs.stat(file.filePath);
      const fileDate = new Date(stat.mtime);
      const dateStr = getDateStr(fileDate);

      if (dateCounts[dateStr]) {
        dateCounts[dateStr].pending++;
      }
    }

    for (const file of plansFiles) {
      const stat = await fs.stat(file.filePath);
      const fileDate = new Date(stat.mtime);
      const dateStr = getDateStr(fileDate);

      if (dateCounts[dateStr]) {
        dateCounts[dateStr].inProgress++;
      }
    }

    for (const file of doneFiles) {
      const stat = await fs.stat(file.filePath);
      const fileDate = new Date(stat.mtime);
      const dateStr = getDateStr(fileDate);

      if (dateCounts[dateStr]) {
        dateCounts[dateStr].completed++;
      }
    }

    // Convert to chart format
    const chartData = Object.entries(dateCounts)
      .sort(([dateA], [dateB]) => new Date(dateA).getTime() - new Date(dateB).getTime())
      .map(([date, counts]) => ({
        date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        pending: counts.pending,
        inProgress: counts.inProgress,
        completed: counts.completed,
      }));

    return NextResponse.json(chartData);
  } catch (error) {
    console.error('Error fetching chart data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch chart data' },
      { status: 500 }
    );
  }
}