import crypto from 'crypto';
import { ContextTensor, PheromoneTrace, ResonanceResult } from './types';

export interface StigmergyConfig {
  resonanceThreshold?: number;
  maxTraces?: number;
}

export class StigmergyV5 {
  private readonly resonanceThreshold: number;
  private readonly maxTraces: number;
  private traces: PheromoneTrace[] = [];

  constructor(config: StigmergyConfig = {}) {
    this.resonanceThreshold = config.resonanceThreshold ?? 0.5;
    this.maxTraces = config.maxTraces ?? 2048;
  }

  private calculateMagnitude(vector: ContextTensor): number {
    let sumSq = 0;
    for (const val of vector) {
      sumSq += val * val;
    }
    return Math.sqrt(sumSq);
  }

  private cosine(
    a: ContextTensor,
    b: ContextTensor,
    magA: number,
    magB: number
  ): number {
    if (magA === 0 || magB === 0) return 0;

    const lenA = a.length;
    const lenB = b.length;
    const minLen = lenA < lenB ? lenA : lenB;

    let dot = 0;
    for (let i = 0; i < minLen; i++) {
      dot += a[i] * b[i];
    }

    return dot / (magA * magB);
  }

  private merkleHash(payload: unknown, parentHash?: string): string {
    const raw = JSON.stringify({ payload, parentHash });
    return crypto.createHash('sha256').update(raw).digest('hex');
  }

  recordTrace(
    context: ContextTensor,
    synthesisVector: number[],
    metadata?: Record<string, unknown>
  ): PheromoneTrace {
    const parentHash = this.traces.at(-1)?.hash;
    const id = crypto.randomUUID();

    // Calculate magnitudes
    const contextMag = this.calculateMagnitude(context);
    const synthesisMag = this.calculateMagnitude(synthesisVector);

    const weight = this.cosine(context, synthesisVector, contextMag, synthesisMag);

    const payload = { id, context, synthesisVector, metadata, weight };
    const hash = this.merkleHash(payload, parentHash);

    const trace: PheromoneTrace = {
      id,
      hash,
      parentHash,
      context,
      magnitude: contextMag, // Cache the magnitude
      synthesisVector,
      weight,
      metadata,
      timestamp: new Date().toISOString(),
    };

    this.traces.push(trace);
    if (this.traces.length > this.maxTraces) {
      this.traces.shift();
    }

    return trace;
  }

  getResonance(context: ContextTensor): ResonanceResult {
    const queryMag = this.calculateMagnitude(context);

    if (queryMag === 0) return { score: 0 };

    let bestScore = 0;
    let bestTrace: PheromoneTrace | undefined;

    for (const trace of this.traces) {
      // Use cached magnitude if available, otherwise calculate it
      const traceMag = trace.magnitude ?? this.calculateMagnitude(trace.context);

      const score = this.cosine(context, trace.context, queryMag, traceMag);

      if (score > bestScore) {
        bestScore = score;
        bestTrace = trace;
      }
    }

    if (bestTrace && bestScore >= this.resonanceThreshold) {
      return { score: bestScore, trace: bestTrace };
    }

    return { score: 0 };
  }

  getMerkleRoot(): string | undefined {
    return this.traces.at(-1)?.hash;
  }

  getRecent(limit = 5): PheromoneTrace[] {
    return this.traces.slice(-limit).reverse();
  }
}
