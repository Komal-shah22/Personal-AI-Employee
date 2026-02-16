import { NextResponse } from 'next/server';

export async function POST() {
  try {
    // Simulate creating a test LinkedIn post
    // In production, this would call your LinkedIn MCP server

    return NextResponse.json({
      success: true,
      message: 'Test LinkedIn post draft created',
    });
  } catch (error) {
    console.error('Test LinkedIn error:', error);
    return NextResponse.json(
      { error: 'Failed to create test post' },
      { status: 500 }
    );
  }
}
