# MCOP Framework 2.0 🌌

[![Eco-Fitness](https://img.shields.io/badge/Eco--Fitness-72.75%2F100-green?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNMTIgMmE3IDcgMCAwIDAgLTcgN2MwIDIuNCAzIDcgNyAxMSA0IC00IDcgLTguNiA3IC0xMWE3IDcgMCAwIDAgLTcgLTd6Ii8+PGNpcmNsZSBjeD0iMTIiIGN5PSI5IiByPSIyIi8+PC9zdmc+)](./ROADMAP_TO_100.md)
[![Test Coverage](https://img.shields.io/badge/coverage-30%25-orange?style=flat-square)](./src/__tests__)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Contributors](https://img.shields.io/badge/contributors-6-brightgreen?style=flat-square)](https://github.com/Kuonirad/KullAILABS-MCOP-Framework-2.0/graphs/contributors)
[![Bus Factor](https://img.shields.io/badge/bus%20factor-1.5-red?style=flat-square)](./ROADMAP_TO_100.md#critical-vulnerabilities)

Meta-Cognitive Optimization Protocol for deterministic, auditable triad orchestration: **NOVA-NEO Encoder**, **Stigmergy v5 Resonance**, and **Holographic Etch Engine**. Built with Next.js + TypeScript and ready for research, prototyping, and production hardening.

> Crystalline entropy targets, Merkle-tracked pheromones, and rank-1 micro-etches—packaged for real-world deployment.

## 🔭 Vision
- **Deterministic cognition**: Reproducible context tensors with explicit entropy metrics.
- **Provenance-first**: Merkle-style lineage for every pheromone trace and etch update.
- **Hardware-aware**: Clear seams for GPU/FPGA acceleration of rank-1 updates and similarity search.
- **Human-in-the-loop**: Dialectical synthesis loop that embraces audits, overrides, and replay.

## 📐 Architecture
See [ARCHITECTURE.md](ARCHITECTURE.md) for diagrams and data flows.

```mermaid
graph TD
    U[User Input] -->|Context| N[NOVA-NEO Encoder]
    N -->|Tensor| S[Stigmergy v5]
    N -->|Tensor| H[Holographic Etch]
    S -->|Resonance| D[Dialectical Synthesizer]
    H -->|Micro-Etch Weights| D
    D -->|Synthesis| UI[Next.js Experience]
    UI -->|Feedback| S
```

## 🧠 Active Kernels
- **NOVA-NEO Encoder**: Deterministic hashing pipeline to generate fixed-dimension tensors with optional normalization and entropy estimates.
- **Stigmergy v5**: Vector pheromone store with cosine resonance scoring, configurable thresholds, and Merkle-proof hashes.
- **Holographic Etch**: Rank-1 micro-etch accumulator that tracks confidence deltas and exposes replayable audit trails.

## 🏁 Getting Started

### Prerequisites
- Node.js 18+
- npm 9+

### Installation
```bash
git clone https://github.com/Kuonirad/KullAILABS-MCOP-Framework-2.0.git
cd KullAILABS-MCOP-Framework-2.0
npm install
```

### Development
```bash
npm run dev   # Next.js dev server with triad modules available under src/core
npm test      # Jest suite (security + triad seeds)
```
Visit `http://localhost:3000` after starting the dev server.

### Docker Compose
```bash
cp .env.example .env
docker compose up -d
```
For local code mounting add `docker-compose.override.yml`:
```yaml
services:
  mcop-app:
    build: .
    volumes:
      - .:/app
    environment:
      - NODE_ENV=development
```

## 🧩 Triad SDK (TypeScript)
Minimal usage of the triad seeds introduced in `src/core`:
```ts
import { NovaNeoEncoder } from './src/core/novaNeoEncoder';
import { StigmergyV5 } from './src/core/stigmergyV5';
import { HolographicEtch } from './src/core/holographicEtch';

const encoder = new NovaNeoEncoder({ dimensions: 64, normalize: true });
const stigmergy = new StigmergyV5();
const etch = new HolographicEtch();

const context = encoder.encode('dialectical synthesis');
const trace = stigmergy.recordTrace(context, context, { note: 'bootstrap' });
const resonance = stigmergy.getResonance(context);
const etchRecord = etch.applyEtch(context, trace.synthesisVector, 'unit test');
```

Configuration knobs live in [`config/examples/mcop.config.example.json`](config/examples/mcop.config.example.json) and map directly to constructor parameters.

## 🧪 Validation
- Jest tests cover security baselines and triad seed behaviors.
- Deterministic hashing avoids side effects in CI.
- Provenance hashes and audit-friendly logging enable replay.

## 🤝 Contributing

**We need you!** Current bus factor: **1.5** (CRITICAL - ecosystem at risk)

Stigmergic contributions are welcome! Our ecological health depends on biodiversity:

- 🌱 **New contributors needed:** See [CONTRIBUTOR_ONBOARDING.md](CONTRIBUTOR_ONBOARDING.md) for 30-minute quick start
- 🎯 **Good first issues:** Check [issues labeled "good first issue"](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
- 📊 **Track our health:** Run `npm run eco:audit` to see ecosystem metrics
- 🗺️ **Roadmap to 100:** See [ROADMAP_TO_100.md](ROADMAP_TO_100.md) for the path to climax ecosystem

**Current Eco-Fitness Score:** 72.75/100 (Thriving Pioneer - needs biodiversity)

See [CONTRIBUTING.md](CONTRIBUTING.md) for pheromone drop protocol, branch hygiene, and review expectations.

## 🔒 Security
Responsible disclosure details are in [SECURITY.md](SECURITY.md). No secrets belong in source; tests guard against accidental leaks.

## 🪪 License
MIT © Kevin Kull
