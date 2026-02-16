import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs/promises';

interface Approval {
  id: string;
  type: 'email' | 'payment' | 'post' | 'file';
  title: string;
  preview: string;
  priority: 'high' | 'normal';
  requestedAt: string;
  amount?: string;
}

export async function GET() {
  try {
    const vaultPath = process.env.VAULT_PATH || path.join(process.cwd(), '..', 'AI_Employee_Vault');
    const pendingPath = path.join(vaultPath, 'Pending_Approval');

    let approvals: Approval[] = [];

    try {
      const files = await fs.readdir(pendingPath);
      const mdFiles = files.filter((f) => f.endsWith('.md'));

      approvals = await Promise.all(
        mdFiles.slice(0, 10).map(async (file): Promise<Approval> => {
          const content = await fs.readFile(path.join(pendingPath, file), 'utf-8');
          const preview = content.substring(0, 200);

          return {
            id: file.replace('.md', ''),
            type: file.includes('EMAIL') ? 'email' : file.includes('PAYMENT') ? 'payment' : 'file',
            title: file.replace('.md', '').replace(/_/g, ' '),
            preview,
            priority: file.includes('URGENT') ? 'high' : 'normal',
            requestedAt: new Date().toISOString(),
            amount: file.includes('PAYMENT') ? '$1,250.00' : undefined,
          };
        })
      );
    } catch (error) {
      // Folder doesn't exist or is empty
      approvals = [];
    }

    return NextResponse.json(approvals);
  } catch (error) {
    console.error('Approvals fetch error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch approvals' },
      { status: 500 }
    );
  }
}
