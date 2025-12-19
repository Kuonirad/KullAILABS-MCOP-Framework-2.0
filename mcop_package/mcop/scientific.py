"""
M-COP v3.1 Scientific Research Domain Adapter

Adapts M-COP for scientific hypothesis generation and experimental design.

Mode Mappings:
- CAUSAL → Mechanism (causal explanations)
- STRUCTURAL → Experimental Design (methodology)
- SELECTIVE → Hypothesis Pruning (falsification)
- COMPOSITIONAL → Research Program (multi-phase studies)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field as dataclass_field

from .domain_base import BaseDomainAdapter, DomainConfig
from .mcop_types import (
    Problem, Solution, Hypothesis, Evidence, ReasoningChain,
    MCOPContext, ReasoningMode
)
from .index import SCIENTIFIC_HIERARCHY


@dataclass
class ResearchQuestion:
    """Structured research question."""
    question: str
    research_field: str = ""
    subfield: str = ""
    prior_work: List[str] = dataclass_field(default_factory=list)
    known_constraints: List[str] = dataclass_field(default_factory=list)
    available_methods: List[str] = dataclass_field(default_factory=list)
    resources: Dict[str, Any] = dataclass_field(default_factory=dict)


@dataclass
class ExperimentDesign:
    """A proposed experimental design."""
    hypothesis: str
    method: str
    variables: Dict[str, str] = dataclass_field(default_factory=dict)
    sample_size: Optional[int] = None
    expected_duration: str = ""
    expected_outcome: str = ""
    potential_confounds: List[str] = dataclass_field(default_factory=list)


class ScientificDomainAdapter(BaseDomainAdapter):
    """
    Scientific research domain adapter for M-COP.

    Specializes in:
    - Hypothesis generation from literature
    - Experimental design
    - Research program planning
    - Evidence synthesis
    """

    def _default_config(self) -> DomainConfig:
        return DomainConfig(
            name="scientific",
            description="Scientific hypothesis generation and experimental design",
            mode_mappings={
                'mechanism': ReasoningMode.CAUSAL,
                'experimental_design': ReasoningMode.STRUCTURAL,
                'hypothesis_pruning': ReasoningMode.SELECTIVE,
                'research_program': ReasoningMode.COMPOSITIONAL
            },
            evidence_hierarchy=SCIENTIFIC_HIERARCHY,
            default_constraints=[
                "Hypotheses must be falsifiable",
                "Methods must be reproducible",
                "Results must be statistically valid",
                "Conclusions must follow from evidence"
            ],
            terminology={
                'hypothesis': 'scientific_hypothesis',
                'evidence': 'experimental_data',
                'solution': 'research_conclusion',
                'confidence': 'statistical_confidence',
                'grounding': 'reproducibility_index'
            }
        )

    def preprocess_problem(self, problem: Problem) -> Problem:
        """
        Preprocess scientific problem.

        Structures the research question and identifies key variables.
        """
        # Add scientific constraints
        problem.constraints.extend(self.config.default_constraints)

        # Extract research components
        research_components = self._extract_research_components(problem.description)
        problem.context['research_components'] = research_components

        # Set domain
        problem.domain = "scientific"

        # Add success criteria for scientific research
        if not problem.success_criteria:
            problem.success_criteria = [
                "Generate testable hypotheses",
                "Design valid experiments",
                "Identify potential confounds",
                "Propose research timeline"
            ]

        return problem

    def postprocess_solution(self, solution: Solution, problem: Problem) -> Solution:
        """
        Postprocess scientific solution.

        Formats as research proposal or findings.
        """
        # Add scientific metadata
        solution.metadata['domain'] = 'scientific'
        solution.metadata['reproducibility_notes'] = self._assess_reproducibility(solution)

        # Assess statistical considerations
        solution.metadata['statistical_considerations'] = self._assess_statistics(solution)

        # Generate next steps
        solution.metadata['next_steps'] = self._generate_next_steps(solution)

        return solution

    def _extract_research_components(self, description: str) -> Dict[str, Any]:
        """Extract research components from problem description."""
        components = {
            'variables': [],
            'methods_mentioned': [],
            'theories_referenced': [],
            'gaps_identified': []
        }

        # Simple extraction (in production, use NLP/LLM)
        method_keywords = [
            'experiment', 'study', 'analysis', 'measurement', 'observation',
            'simulation', 'model', 'survey', 'trial', 'test'
        ]

        description_lower = description.lower()
        for keyword in method_keywords:
            if keyword in description_lower:
                components['methods_mentioned'].append(keyword)

        return components

    def _assess_reproducibility(self, solution: Solution) -> Dict[str, Any]:
        """Assess reproducibility of proposed research."""
        notes = {
            'reproducibility_score': solution.grounding_index,
            'concerns': [],
            'strengths': []
        }

        if solution.grounding_index >= 0.8:
            notes['strengths'].append("Strong evidence base supports reproducibility")
        elif solution.grounding_index < 0.5:
            notes['concerns'].append("Limited evidence may affect reproducibility")

        if len(solution.evidence_chain) >= 3:
            notes['strengths'].append("Multiple lines of evidence")
        else:
            notes['concerns'].append("Consider gathering additional evidence")

        return notes

    def _assess_statistics(self, solution: Solution) -> List[str]:
        """Assess statistical considerations."""
        considerations = []

        if solution.confidence < 0.95:
            considerations.append(
                f"Current confidence ({solution.confidence:.2f}) below typical alpha=0.05 threshold"
            )

        considerations.append("Consider power analysis for sample size determination")
        considerations.append("Plan for multiple comparison corrections if needed")

        return considerations

    def _generate_next_steps(self, solution: Solution) -> List[str]:
        """Generate recommended next steps for research."""
        steps = []

        if solution.confidence < 0.6:
            steps.append("Conduct preliminary/pilot study")

        steps.append("Develop detailed experimental protocol")
        steps.append("Identify required resources and timeline")
        steps.append("Submit for ethics/IRB review if applicable")
        steps.append("Pre-register hypothesis and analysis plan")

        return steps

    def create_research_problem(self, question: ResearchQuestion) -> Problem:
        """
        Create a Problem from a structured research question.
        """
        description_parts = [f"Research Question: {question.question}"]

        if question.research_field:
            description_parts.append(f"Field: {question.research_field}")
            if question.subfield:
                description_parts.append(f"Subfield: {question.subfield}")

        if question.prior_work:
            description_parts.append(f"Prior work: {', '.join(question.prior_work)}")

        if question.available_methods:
            description_parts.append(f"Available methods: {', '.join(question.available_methods)}")

        problem = Problem(
            description='\n'.join(description_parts),
            domain="scientific",
            context={
                'research_question': question.__dict__,
                'research_field': question.research_field,
                'methods': question.available_methods
            },
            constraints=question.known_constraints
        )

        return problem

    def format_research_proposal(self, solution: Solution) -> str:
        """
        Format solution as a research proposal outline.
        """
        lines = [
            "=" * 70,
            "RESEARCH PROPOSAL OUTLINE",
            "=" * 70,
            "",
            "ABSTRACT",
            "-" * 70,
            solution.content.split('\n')[0] if solution.content else "No abstract generated",
            "",
            f"Confidence Level: {solution.confidence * 100:.1f}%",
            f"Evidence Strength: {solution.grounding_index:.2f}",
            "",
            "BACKGROUND & RATIONALE",
            "-" * 70
        ]

        # Add evidence as background
        for i, evidence in enumerate(solution.evidence_chain[:3], 1):
            lines.append(f"  {i}. {evidence.content}")

        lines.extend([
            "",
            "HYPOTHESES",
            "-" * 70
        ])

        # Main hypothesis
        lines.append(f"  Primary: {solution.content.split(chr(10))[0]}")

        # Alternative hypotheses
        if solution.alternative_solutions:
            lines.append("  Alternatives:")
            for i, alt in enumerate(solution.alternative_solutions, 1):
                lines.append(f"    {i}. {alt.content.split(chr(10))[0]}")

        # Statistical considerations
        stats = solution.metadata.get('statistical_considerations', [])
        if stats:
            lines.extend([
                "",
                "STATISTICAL CONSIDERATIONS",
                "-" * 70
            ])
            for stat in stats:
                lines.append(f"  - {stat}")

        # Next steps
        next_steps = solution.metadata.get('next_steps', [])
        if next_steps:
            lines.extend([
                "",
                "PROPOSED TIMELINE / NEXT STEPS",
                "-" * 70
            ])
            for i, step in enumerate(next_steps, 1):
                lines.append(f"  {i}. {step}")

        # Uncertainties
        if solution.key_uncertainties:
            lines.extend([
                "",
                "LIMITATIONS & UNCERTAINTIES",
                "-" * 70
            ])
            for uncertainty in solution.key_uncertainties:
                lines.append(f"  - {uncertainty}")

        lines.extend([
            "",
            "=" * 70
        ])

        return '\n'.join(lines)