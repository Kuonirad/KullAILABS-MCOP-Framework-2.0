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

  private computeMagnitude(tensor: ContextTensor): number {
    let sumSq = 0;
    for (const val of tensor) {
      sumSq += val * val;
    }
    return Math.sqrt(sumSq);
  }

  private cosine(a: ContextTensor, b: ContextTensor, magA?: number, magB?: number): number {
  private magnitude(tensor: ContextTensor): number {
    let sum = 0;
    for (let i = 0; i < tensor.length; i++) {
      sum += tensor[i] * tensor[i];
    }
    return Math.sqrt(sum);
  }

  private cosine(a: ContextTensor, b: ContextTensor, normA?: number, normB?: number): number {
    const minLen = Math.min(a.length, b.length);

    // Optimization: Use pre-calculated magnitudes if vectors are equal length
    // This avoids recalculating norms and Math.sqrt calls in the inner loop
    if (magA !== undefined && magB !== undefined && a.length === b.length) {
      let dot = 0;
      for (let i = 0; i < minLen; i++) {
        dot += a[i] * b[i];
      }
      // Avoid division by zero
      if (magA === 0 || magB === 0) return 0;
      return dot / (magA * magB);
    }

    // Standard path (lengths differ or no pre-calc)
    let dot = 0;
    let sumSqA = 0;
    let sumSqB = 0;
    for (let i = 0; i < minLen; i++) {
      dot += a[i] * b[i];
      sumSqA += a[i] * a[i];
      sumSqB += b[i] * b[i];
    }
    if (sumSqA === 0 || sumSqB === 0) return 0;
    return dot / (Math.sqrt(sumSqA) * Math.sqrt(sumSqB));

    // Only use pre-calculated norms if the operation covers the full vector
    // (i.e., the other vector is at least as long as the one we have the norm for)
    const useNormA = normA !== undefined && b.length >= a.length;
    const useNormB = normB !== undefined && a.length >= b.length;

    let calcNormA = 0;
    let calcNormB = 0;

    for (let i = 0; i < minLen; i++) {
      dot += a[i] * b[i];
      if (!useNormA) calcNormA += a[i] * a[i];
      if (!useNormB) calcNormB += b[i] * b[i];
    }

    const finalNormA = useNormA ? normA! : Math.sqrt(calcNormA);
    const finalNormB = useNormB ? normB! : Math.sqrt(calcNormB);

    if (!finalNormA || !finalNormB) return 0;
    return dot / (finalNormA * finalNormB);
  }

  private merkleHash(payload: unknown, parentHash?: string): string {
    const raw = JSON.stringify({ payload, parentHash });
    return crypto.createHash('sha256').update(raw).digest('hex');
  }

  recordTrace(context: ContextTensor, synthesisVector: number[], metadata?: Record<string, unknown>): PheromoneTrace {
    const parentHash = this.traces.at(-1)?.hash;
    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    const weight = this.cosine(context, synthesisVector);
    // Calculate magnitude once and cache it
    const magnitude = this.computeMagnitude(context);

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
    // Pre-calculate input magnitude once for the entire batch
    const inputMagnitude = this.computeMagnitude(context);

    for (const trace of this.traces) {
      const score = this.cosine(context, trace.context, inputMagnitude, trace.magnitude);
    // Optimization: Calculate context magnitude once to avoid re-calculation in the loop
    const contextMag = this.magnitude(context);

    for (const trace of this.traces) {
      const score = this.cosine(context, trace.context, contextMag);
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
