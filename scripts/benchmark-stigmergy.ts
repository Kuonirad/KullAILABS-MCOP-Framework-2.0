
import { StigmergyV5 } from '../src/core/stigmergyV5';
import { ContextTensor } from '../src/core/types';

// Helper to generate random tensor
const generateTensor = (size: number): ContextTensor => {
  const tensor = new Array(size);
  for (let i = 0; i < size; i++) {
    tensor[i] = Math.random() * 2 - 1;
  }
  return tensor;
};

// Benchmark
const runBenchmark = () => {
  const stigmergy = new StigmergyV5({ maxTraces: 5000 });
  const dimensions = 1536; // Simulating embedding size
  const numTraces = 1000;
  const numQueries = 100;

  console.log(`Preparing ${numTraces} traces with ${dimensions} dimensions...`);

  // Populate traces
  for (let i = 0; i < numTraces; i++) {
    stigmergy.recordTrace(generateTensor(dimensions), generateTensor(dimensions));
  }

  console.log(`Running ${numQueries} queries...`);

  const queries = [];
  for(let i=0; i<numQueries; i++) {
    queries.push(generateTensor(dimensions));
  }

  const start = performance.now();

  for (const query of queries) {
    stigmergy.getResonance(query);
  }

  const end = performance.now();
  const duration = end - start;
  const opsPerSec = (numQueries / duration) * 1000;

  console.log(`Total time: ${duration.toFixed(2)}ms`);
  console.log(`Average time per query: ${(duration / numQueries).toFixed(2)}ms`);
  console.log(`Queries per second: ${opsPerSec.toFixed(2)}`);

  // Verification of logic (sanity check)
  const res = stigmergy.getResonance(queries[0]);
  console.log(`Sanity check resonance score: ${res.score}`);
};

runBenchmark();
