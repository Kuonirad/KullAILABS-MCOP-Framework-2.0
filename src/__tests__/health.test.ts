/**
 * @jest-environment node
 */
import { GET } from '../app/api/health/route';
import { NextResponse } from 'next/server';

describe('Health Check API', () => {
  it('should return 200 OK and correct status', async () => {
    const response = await GET();

    expect(response).toBeInstanceOf(NextResponse);
    expect(response.status).toBe(200);

    // Check response body
    const data = await response.json();
    expect(data.status).toBe('ok');
    expect(data.timestamp).toBeDefined();

    // Verify it's a valid date string
    const date = new Date(data.timestamp);
    expect(date.toString()).not.toBe('Invalid Date');
  });
});
