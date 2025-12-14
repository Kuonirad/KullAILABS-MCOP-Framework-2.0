import crypto from 'crypto';
import { ContextTensor, NovaNeoConfig } from './types';

export class NovaNeoEncoder {
  private readonly dimensions: number;
  private readonly normalize: boolean;
  private readonly entropyFloor: number;

  constructor(config: NovaNeoConfig) {
    if (config.dimensions <= 0) {
      throw new Error('dimensions must be positive');
    }
    this.dimensions = config.dimensions;
    this.normalize = config.normalize ?? false;
    this.entropyFloor = config.entropyFloor ?? 0.0;
  }

  encode(text: string): ContextTensor {
    const hash = crypto.createHash('sha256').update(text).digest();
    const values: number[] = [];

    // Repeat the hash to fill the requested dimensions
    while (values.length < this.dimensions) {
      for (const byte of hash) {
        const signed = (byte / 255) * 2 - 1; // map 0-255 → -1..1
        values.push(signed);
        if (values.length === this.dimensions) break;
      }
    }

    if (this.normalize) {
      const norm = Math.sqrt(values.reduce((acc, v) => acc + v * v, 0)) || 1;
      return values.map(v => v / norm);
    }

    return values;
  }

  estimateEntropy(tensor: ContextTensor): number {
    // Simple entropy-like measure: variance of absolute values
    if (!tensor.length) return 0;
    const mean = tensor.reduce((acc, v) => acc + Math.abs(v), 0) / tensor.length;
    const variance =
      tensor.reduce((acc, v) => acc + Math.pow(Math.abs(v) - mean, 2), 0) /
      tensor.length;
    const entropy = Math.min(1, variance);
    return Math.max(entropy, this.entropyFloor);
  }
}
