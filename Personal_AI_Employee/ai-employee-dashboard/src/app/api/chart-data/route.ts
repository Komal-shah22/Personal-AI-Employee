import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const range = searchParams.get('range') || '7D';

    // Mock chart data (in production, this would come from database)
    let data = [];

    if (range === '1D') {
      data = [
        { date: '00:00', completed: 5, pending: 2, agent: 'Gmail', tasks: 12 },
        { date: '04:00', completed: 8, pending: 3, agent: 'WhatsApp', tasks: 8 },
        { date: '08:00', completed: 15, pending: 5, agent: 'LinkedIn', tasks: 5 },
        { date: '12:00', completed: 23, pending: 4, agent: 'File', tasks: 15 },
        { date: '16:00', completed: 31, pending: 6, agent: 'Orchestrator', tasks: 23 },
        { date: '20:00', completed: 38, pending: 3, agent: 'Total', tasks: 63 },
      ];
    } else if (range === '7D') {
      data = [
        { date: 'Mon', completed: 45, pending: 8, agent: 'Gmail', tasks: 45 },
        { date: 'Tue', completed: 52, pending: 6, agent: 'WhatsApp', tasks: 32 },
        { date: 'Wed', completed: 48, pending: 10, agent: 'LinkedIn', tasks: 18 },
        { date: 'Thu', completed: 61, pending: 7, agent: 'File', tasks: 28 },
        { date: 'Fri', completed: 58, pending: 9, agent: 'Orchestrator', tasks: 67 },
        { date: 'Sat', completed: 67, pending: 5, agent: 'Total', tasks: 190 },
        { date: 'Sun', completed: 73, pending: 3 },
      ];
    } else {
      data = [
        { date: 'Week 1', completed: 320, pending: 45, agent: 'Gmail', tasks: 320 },
        { date: 'Week 2', completed: 385, pending: 38, agent: 'WhatsApp', tasks: 245 },
        { date: 'Week 3', completed: 412, pending: 42, agent: 'LinkedIn', tasks: 156 },
        { date: 'Week 4', completed: 468, pending: 35, agent: 'File', tasks: 198 },
      ];
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error('Chart data error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch chart data' },
      { status: 500 }
    );
  }
}
