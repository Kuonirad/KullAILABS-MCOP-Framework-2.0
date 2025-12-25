/**
 * @jest-environment node
 */
import { GET } from '../app/api/health/route';
import { NextResponse } from 'next/server';

describe('Health Check API', () => {
  it('returns 200 and status ok', async () => {
    const response = await GET();
    expect(response).toBeInstanceOf(NextResponse);
    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data).toEqual({ status: 'ok' });
  });
});
