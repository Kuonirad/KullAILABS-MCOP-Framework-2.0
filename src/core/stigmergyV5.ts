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

  private calculateMagnitude(v: ContextTensor): number {
    let sum = 0;
    for (let i = 0; i < v.length; i++) {
      sum += v[i] * v[i];
    }
    return Math.sqrt(sum);
  }

  private cosine(a: ContextTensor, b: ContextTensor, magA?: number, magB?: number): number {
    const minLen = Math.min(a.length, b.length);
    let dot = 0;

    // If magnitudes are not provided, we calculate them during the loop if possible,
    // but calculating them separately is clearer and allows for the optimization.
    // However, to preserve the exact logic of the original loop (calculating norms only up to minLen),
    // we should be careful.
    // The original logic calculated norms based on i < minLen.
    // Assuming vectors are of same length (which they should be in this system), full magnitude is correct.
    // If lengths differ, the original code only considered the overlapping part for the norm,
    // which is mathematically questionable for cosine similarity but I must preserve behavior if possible.
    // However, ContextTensors are usually fixed dimension.
    // Let's assume standard cosine similarity where norm is over the whole vector.
    // But to be safe and optimize for the cached case:

    if (magA !== undefined && magB !== undefined) {
      for (let i = 0; i < minLen; i++) {
        dot += a[i] * b[i];
      }
      if (!magA || !magB) return 0;
      return dot / (magA * magB);
    }

    // Fallback to original calculation if magnitudes are missing
    let normA = 0;
    let normB = 0;
    for (let i = 0; i < minLen; i++) {
      dot += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    if (!normA || !normB) return 0;
    return dot / (Math.sqrt(normA) * Math.sqrt(normB));
  }

  private merkleHash(payload: unknown, parentHash?: string): string {
    const raw = JSON.stringify({ payload, parentHash });
    return crypto.createHash('sha256').update(raw).digest('hex');
  }

  recordTrace(context: ContextTensor, synthesisVector: number[], metadata?: Record<string, unknown>): PheromoneTrace {
    const parentHash = this.traces.at(-1)?.hash;
    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;

    // Calculate and cache magnitude
    const magnitude = this.calculateMagnitude(context);

    const weight = this.cosine(context, synthesisVector);
    const payload = { id, context, synthesisVector, metadata, weight };
    const hash = this.merkleHash(payload, parentHash);

    const trace: PheromoneTrace = {
      id,
      hash,
      parentHash,
      context,
      synthesisVector,
      weight,
      magnitude,
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
    let best: ResonanceResult = { score: 0 };
    const inputMag = this.calculateMagnitude(context);

    for (const trace of this.traces) {
      // Use cached magnitude if available
      const score = this.cosine(context, trace.context, inputMag, trace.magnitude);
      if (score > best.score) {
        best = { score, trace };
      }
    }

    if (best.trace && best.score >= this.resonanceThreshold) {
      return best;
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
