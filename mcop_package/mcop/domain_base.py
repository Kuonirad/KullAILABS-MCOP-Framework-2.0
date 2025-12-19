"""
M-COP v3.1 Domain Adapter Base Classes

Base classes for creating domain-specific adapters.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from .mcop_types import Problem, Solution, ReasoningMode
from .engine import MCOPEngine, MCOPConfig
from .index import EvidenceHierarchy, GENERAL_HIERARCHY


@dataclass
class DomainConfig:
    """Configuration for a domain adapter."""
    name: str = "general"
    description: str = ""
    mode_mappings: Dict[ReasoningMode, str] = field(default_factory=dict)
    evidence_hierarchy: Optional[EvidenceHierarchy] = None
    mcop_config: Optional[MCOPConfig] = None
    default_constraints: List[str] = field(default_factory=list)
    terminology: Dict[str, str] = field(default_factory=dict)


class BaseDomainAdapter(ABC):
    """
    Abstract base class for domain-specific adapters.

    Domain adapters customize M-COP for specific fields like medicine,
    science, engineering, etc. They provide:
    - Domain-specific mode mappings
    - Evidence hierarchies
    - Problem/solution formatting
    - Domain-specific constraints
    """

    def __init__(self, config: Optional[DomainConfig] = None):
        self.config = config or self._default_config()
        self.engine = MCOPEngine(config=self.config.mcop_config)

        # Set evidence hierarchy if provided
        if self.config.evidence_hierarchy:
            self.evidence_hierarchy = self.config.evidence_hierarchy
        else:
            self.evidence_hierarchy = GENERAL_HIERARCHY

    @abstractmethod
    def _default_config(self) -> DomainConfig:
        """Return default configuration for this domain."""
        pass

    def solve(self, problem: Problem) -> Solution:
        """
        Solve a problem using this domain adapter.

        Args:
            problem: Problem to solve

        Returns:
            Solution with domain-specific formatting
        """
        # Preprocess problem
        problem = self.preprocess_problem(problem)

        # Solve using engine
        solution = self.engine.solve(problem)

        # Postprocess solution
        solution = self.postprocess_solution(solution, problem)

        # Add domain metadata
        solution.metadata['domain'] = self.config.name

        return solution

    def preprocess_problem(self, problem: Problem) -> Problem:
        """
        Preprocess problem before solving.
        Override this to add domain-specific preprocessing.
        """
        return problem

    def postprocess_solution(self, solution: Solution, problem: Problem) -> Solution:
        """
        Postprocess solution after solving.
        Override this to add domain-specific postprocessing.
        """
        return solution

    def format_solution(self, solution: Solution) -> str:
        """
        Format solution for display.
        Override this for domain-specific formatting.
        """
        output = []
        output.append(f"=== {self.config.name.upper()} SOLUTION ===\n")
        output.append(f"{solution.content}\n")
        output.append(f"\nConfidence: {solution.confidence * 100:.1f}%")
        output.append(f"Grounding: {solution.grounding_index:.2f}\n")

        if solution.evidence_chain:
            output.append("\n--- Evidence ---")
            for i, e in enumerate(solution.evidence_chain[:5], 1):
                output.append(f"{i}. {e.content[:100]}... (weight: {e.weight:.2f})")

        if solution.alternative_solutions:
            output.append("\n--- Alternatives ---")
            for i, alt in enumerate(solution.alternative_solutions[:3], 1):
                output.append(f"{i}. {alt.content[:100]}... (conf: {alt.confidence * 100:.1f}%)")

        if solution.key_uncertainties:
            output.append("\n--- Key Uncertainties ---")
            for i, unc in enumerate(solution.key_uncertainties[:5], 1):
                output.append(f"{i}. {unc}")

        return "\n".join(output)