# M-COP v3.1 - Meta-Cognitive Operating Protocol

A universal reasoning framework that implements multi-modal reasoning, mycelial chaining, and evidence grounding for domain-agnostic problem solving.

## Overview

M-COP (Meta-Cognitive Operating Protocol) is a reasoning system that mirrors how high-functioning human experts actually reason:

1. **Generate multiple hypotheses** (not just one)
2. **Test them recursively** (not just once)
3. **Ground in evidence** (not just intuition)
4. **Preserve diversity** (not just pick first idea)
5. **Challenge assumptions** (not just confirm bias)

## Key Features

### Multi-Modal Reasoning
Four fundamental reasoning modes that map to any domain:
- **CAUSAL**: Cause-effect, mechanistic reasoning
- **STRUCTURAL**: Pattern recognition, architectural analysis
- **SELECTIVE**: Filtering, constraint satisfaction
- **COMPOSITIONAL**: Multi-step synthesis

### Mycelial Chaining
Recursive hypothesis refinement inspired by mycelium networks:
- Branching exploration of solution space
- Cross-linking related hypotheses
- Pruning weak branches
- Synthesizing strongest paths

### Grounding Index
Evidence quality tracking with domain-specific hierarchies:
- Medical: RCTs > Cohort studies > Case reports
- Scientific: Reproduced experiments > Peer-reviewed > Preprints
- General: Verified facts > Expert consensus > Speculation

### Domain Adapters
Pre-built adapters for specific fields:
- **Medical**: Differential diagnosis, treatment planning
- **Scientific**: Hypothesis generation, experimental design
- **General**: Flexible problem-solving

## Installation

```bash
pip install -e .
```

## Quick Start

### Basic Usage

```python
from mcop import solve

solution = solve("What causes climate change?")
print(solution.content)
print(f"Confidence: {solution.confidence * 100:.1f}%")
print(f"Grounding: {solution.grounding_index:.2f}")
```

### Using the Engine Directly

```python
from mcop import MCOPEngine, Problem

engine = MCOPEngine()
problem = Problem(description="Your problem here")
solution = engine.solve(problem)
```

### Domain-Specific Usage

```python
from mcop.domains import MedicalDomainAdapter, PatientPresentation

adapter = MedicalDomainAdapter()
presentation = PatientPresentation(
    chief_complaint="Chest pain",
    symptoms=["chest pain", "shortness of breath"]
)
problem = adapter.create_patient_problem(presentation)
solution = adapter.solve(problem)
print(adapter.format_differential_diagnosis(solution))
```

## Command Line Interface

```bash
# Solve a problem
mcop solve "What are the causes of inflation?"

# Use a specific domain
mcop solve --domain medical "Patient with fever and cough"

# Interactive mode
mcop interactive
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     M-COP v3.1 Engine                       │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: Seed Generation (Multi-Modal Hypotheses)          │
│  Phase 2: Mycelial Chaining (Recursive Refinement)          │
│  Phase 3: Intermediate Validation (Evidence Integration)    │
│  Phase 4: Diversity Preservation (Prevent Anchoring)        │
│  Phase 5: Synthesis (Solution with Grounding)               │
│  Phase 6: Epistemic Challenge (Question Assumptions)        │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

```python
from mcop import MCOPEngine, MCOPConfig

config = MCOPConfig(
    max_iterations=10,
    confidence_threshold=0.7,
    grounding_threshold=0.5,
    diversity_threshold=0.3,
    min_alternatives=2,
    enable_epistemic_challenge=True
)

engine = MCOPEngine(config)
```

## Output Format

Every M-COP solution includes:
- **Solution**: The primary answer
- **Confidence**: How confident the system is (0-100%)
- **Grounding Index**: Evidence quality score (0-1)
- **Evidence Chain**: Supporting evidence with sources
- **Alternative Solutions**: Other viable approaches
- **Key Uncertainties**: What we don't know

## License

MIT License

## Contributing

Contributions welcome! Please read the contributing guidelines first.
# M-COP v3.1 Installation Guide

## Quick Install

### Option 1: Development Installation (Recommended)
```bash
cd mcop_package
pip install -e .
```

### Option 2: Production Installation
```bash
cd mcop_package
pip install .
```

### Option 3: From Setup Script
```bash
cd mcop_package
python setup.py install
```

## Verification

### 1. Run Tests
```bash
cd mcop_package
python test_mcop_runner.py
```

Expected output:
```
======================================================================
M-COP v3.1 Test Suite
======================================================================
...
✓ ALL TESTS PASSED
======================================================================
```

### 2. Run Demonstrations
```bash
python DEMO.py
```

### 3. Try It Out
```python
from mcop import solve

solution = solve("What is gravity?")
print(solution.content)
print(f"Confidence: {solution.confidence * 100:.1f}%")
```

## Requirements

- Python 3.8 or higher
- No external dependencies required!

## Usage

### Command Line
```bash
# Solve a problem
mcop solve "What causes rain?"

# Interactive mode
mcop interactive
```

### Python API
```python
from mcop import solve, MCOPEngine, Problem

# Simple usage
solution = solve("Your question here")

# Advanced usage
engine = MCOPEngine()
problem = Problem(description="...", constraints=[...])
solution = engine.solve(problem)
```

## Next Steps

1. Read `USAGE_GUIDE.md` for comprehensive examples
2. Check `API_REFERENCE.md` for complete API documentation
3. Explore `DEMO.py` for working examples
4. Review `PROJECT_STRUCTURE.md` for architecture details

## Troubleshooting

### Import Error
If you get `ModuleNotFoundError: No module named 'mcop'`:
```bash
cd mcop_package
pip install -e .
```

### Test Failures
Ensure you're in the correct directory:
```bash
cd mcop_package
python test_mcop_runner.py
```

## Support

For issues or questions:
1. Check the documentation files
2. Review the demo script
3. Examine the test suite for examples

---

Ready to use M-COP v3.1!