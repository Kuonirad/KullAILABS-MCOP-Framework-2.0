/**
 * @jest-environment node
 */
import { GET } from '../app/api/health/route';
import { NextResponse } from 'next/server';

describe('Health Check API', () => {
  it('returns 200 and status ok', async () => {
    const response = await GET();
    // In Next.js App Router handlers, the return type might not be exactly NextResponse in tests depending on mocks
    // but usually it behaves like one.
    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data).toEqual({ status: 'ok' });
  });
});
