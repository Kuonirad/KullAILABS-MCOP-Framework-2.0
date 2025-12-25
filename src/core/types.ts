export type ContextTensor = number[];

export interface NovaNeoConfig {
  dimensions: number;
  normalize?: boolean;
  entropyFloor?: number;
}

export interface PheromoneTrace {
  id: string;
  hash: string;
  parentHash?: string;
  context: ContextTensor;
  synthesisVector: number[];
  weight: number;
  magnitude?: number;
  metadata?: Record<string, unknown>;
  timestamp: string;
}

export interface ResonanceResult {
  score: number;
  trace?: PheromoneTrace;
}

export interface EtchRecord {
  hash: string;
  deltaWeight: number;
  note?: string;
  timestamp: string;
}
