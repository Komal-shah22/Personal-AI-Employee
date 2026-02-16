import { NextResponse } from 'next/server';

export async function POST() {
  try {
    // Simulate sending a test email
    // In production, this would call your email MCP server

    return NextResponse.json({
      success: true,
      message: 'Test email sent successfully',
    });
  } catch (error) {
    console.error('Test email error:', error);
    return NextResponse.json(
      { error: 'Failed to send test email' },
      { status: 500 }
    );
  }
}
