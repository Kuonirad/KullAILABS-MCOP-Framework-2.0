"""
M-COP v3.1 General Purpose Domain Adapter

A flexible adapter for general problem-solving that doesn't require
domain-specific customization.
"""

from typing import List, Dict, Any, Optional

from .domain_base import BaseDomainAdapter, DomainConfig
from .mcop_types import Problem, Solution, ReasoningMode
from .index import GENERAL_HIERARCHY


class GeneralDomainAdapter(BaseDomainAdapter):
    """
    General purpose domain adapter for M-COP.

    Suitable for:
    - General reasoning tasks
    - Problem-solving without domain constraints
    - Exploratory analysis
    - Cross-domain problems
    """

    def _default_config(self) -> DomainConfig:
        return DomainConfig(
            name="general",
            description="General purpose reasoning and problem-solving",
            mode_mappings={
                'causal': ReasoningMode.CAUSAL,
                'structural': ReasoningMode.STRUCTURAL,
                'selective': ReasoningMode.SELECTIVE,
                'compositional': ReasoningMode.COMPOSITIONAL
            },
            evidence_hierarchy=GENERAL_HIERARCHY,
            default_constraints=[
                "Maintain logical consistency",
                "Consider multiple perspectives",
                "Ground conclusions in evidence"
            ],
            terminology={}  # Use default terminology
        )

    def preprocess_problem(self, problem: Problem) -> Problem:
        """
        Minimal preprocessing for general problems.
        """
        # Add general constraints if none specified
        if not problem.constraints:
            problem.constraints = self.config.default_constraints.copy()

        # Set domain
        problem.domain = "general"

        # Add default success criteria if none specified
        if not problem.success_criteria:
            problem.success_criteria = [
                "Provide well-reasoned solution",
                "Support with evidence",
                "Consider alternatives"
            ]

        return problem

    def postprocess_solution(self, solution: Solution, problem: Problem) -> Solution:
        """
        Minimal postprocessing for general solutions.
        """
        solution.metadata['domain'] = 'general'
        return solution

    def format_solution(self, solution: Solution) -> str:
        """
        Format solution as readable text.
        """
        lines = [
            "=" * 60,
            "M-COP SOLUTION",
            "=" * 60,
            "",
            "SOLUTION:",
            "-" * 60,
            solution.content,
            "",
            f"Confidence: {solution.confidence * 100:.1f}%",
            f"Grounding Index: {solution.grounding_index:.2f}",
            ""
        ]

        if solution.evidence_chain:
            lines.extend([
                "SUPPORTING EVIDENCE:",
                "-" * 60
            ])
            for i, evidence in enumerate(solution.evidence_chain[:5], 1):
                lines.append(f"  {i}. {evidence.content} (weight: {evidence.weight:.2f})")
            lines.append("")

        if solution.alternative_solutions:
            lines.extend([
                "ALTERNATIVES CONSIDERED:",
                "-" * 60
            ])
            for i, alt in enumerate(solution.alternative_solutions, 1):
                lines.append(f"  {i}. {alt.content.split(chr(10))[0]}")
                lines.append(f"     Confidence: {alt.confidence * 100:.1f}%")
            lines.append("")

        if solution.key_uncertainties:
            lines.extend([
                "KEY UNCERTAINTIES:",
                "-" * 60
            ])
            for uncertainty in solution.key_uncertainties:
                lines.append(f"  • {uncertainty}")
            lines.append("")

        lines.append("=" * 60)

        return '\n'.join(lines)