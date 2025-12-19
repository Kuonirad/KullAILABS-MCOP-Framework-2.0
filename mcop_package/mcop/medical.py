"""
M-COP v3.1 Medical Domain Adapter

Adapts M-COP for medical diagnosis and treatment planning.

Mode Mappings:
- CAUSAL → Pathophysiology (disease mechanisms)
- STRUCTURAL → Anatomy (organ systems, structures)
- SELECTIVE → Differential Diagnosis (ruling in/out)
- COMPOSITIONAL → Treatment Protocol (multi-step care)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from .domain_base import BaseDomainAdapter, DomainConfig
from .mcop_types import (
    Problem, Solution, Hypothesis, Evidence, ReasoningChain,
    MCOPContext, ReasoningMode, EpistemicState
)
from .index import EvidenceHierarchy, MEDICAL_HIERARCHY


@dataclass
class PatientPresentation:
    """Structured patient presentation data."""
    chief_complaint: str = ""
    symptoms: List[str] = field(default_factory=list)
    vital_signs: Dict[str, Any] = field(default_factory=dict)
    lab_results: Dict[str, Any] = field(default_factory=dict)
    imaging: List[str] = field(default_factory=list)
    medical_history: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    social_history: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagnosticHypothesis:
    """A diagnostic hypothesis with medical-specific fields."""
    diagnosis: str
    icd_code: Optional[str] = None
    confidence: float = 0.5
    supporting_findings: List[str] = field(default_factory=list)
    contradicting_findings: List[str] = field(default_factory=list)
    tests_to_order: List[str] = field(default_factory=list)
    grounding_index: float = 0.0


class MedicalDomainAdapter(BaseDomainAdapter):
    """
    Medical domain adapter for M-COP.

    Specializes in:
    - Differential diagnosis generation
    - Evidence-based treatment planning
    - Clinical decision support
    """

    def _default_config(self) -> DomainConfig:
        return DomainConfig(
            name="medical",
            description="Medical diagnosis and treatment planning",
            mode_mappings={
                'pathophysiology': ReasoningMode.CAUSAL,
                'anatomy': ReasoningMode.STRUCTURAL,
                'differential_diagnosis': ReasoningMode.SELECTIVE,
                'treatment_protocol': ReasoningMode.COMPOSITIONAL
            },
            evidence_hierarchy=MEDICAL_HIERARCHY,
            default_constraints=[
                "First, do no harm (primum non nocere)",
                "Consider patient safety",
                "Follow evidence-based guidelines",
                "Account for contraindications"
            ],
            terminology={
                'hypothesis': 'diagnosis',
                'evidence': 'clinical_finding',
                'solution': 'treatment_plan',
                'confidence': 'clinical_certainty',
                'grounding': 'evidence_strength'
            }
        )

    def preprocess_problem(self, problem: Problem) -> Problem:
        """
        Preprocess medical problem.

        Extracts clinical features and structures the presentation.
        """
        # Add medical-specific constraints
        problem.constraints.extend(self.config.default_constraints)

        # Extract clinical features from description
        clinical_features = self._extract_clinical_features(problem.description)
        problem.context['clinical_features'] = clinical_features

        # Set domain
        problem.domain = "medical"

        # Add success criteria for medical diagnosis
        if not problem.success_criteria:
            problem.success_criteria = [
                "Identify most likely diagnosis",
                "Provide differential diagnoses",
                "Recommend diagnostic tests",
                "Suggest initial treatment approach"
            ]

        return problem

    def postprocess_solution(self, solution: Solution, problem: Problem) -> Solution:
        """
        Postprocess medical solution.

        Formats as clinical decision support output.
        """
        # Add medical-specific metadata
        solution.metadata['domain'] = 'medical'
        solution.metadata['disclaimer'] = (
            "This is AI-assisted clinical decision support. "
            "All recommendations should be verified by a qualified healthcare provider."
        )

        # Format evidence chain with medical terminology
        for evidence in solution.evidence_chain:
            evidence.metadata['clinical_relevance'] = self._assess_clinical_relevance(evidence)

        # Add clinical recommendations
        solution.metadata['clinical_recommendations'] = self._generate_recommendations(solution)

        return solution

    def _extract_clinical_features(self, description: str) -> Dict[str, Any]:
        """Extract clinical features from problem description."""
        features = {
            'symptoms': [],
            'signs': [],
            'risk_factors': [],
            'duration': None
        }

        # Simple keyword extraction (in production, use NLP/LLM)
        symptom_keywords = [
            'pain', 'fever', 'cough', 'fatigue', 'nausea', 'vomiting',
            'headache', 'dizziness', 'shortness of breath', 'swelling'
        ]

        description_lower = description.lower()
        for keyword in symptom_keywords:
            if keyword in description_lower:
                features['symptoms'].append(keyword)

        return features

    def _assess_clinical_relevance(self, evidence: Evidence) -> str:
        """Assess clinical relevance of evidence."""
        if evidence.weight >= 0.9:
            return "Highly relevant - strong clinical evidence"
        elif evidence.weight >= 0.7:
            return "Relevant - moderate clinical evidence"
        elif evidence.weight >= 0.5:
            return "Potentially relevant - limited evidence"
        else:
            return "Low relevance - weak evidence"

    def _generate_recommendations(self, solution: Solution) -> List[str]:
        """Generate clinical recommendations from solution."""
        recommendations = []

        if solution.confidence >= 0.8:
            recommendations.append("High confidence diagnosis - consider initiating treatment")
        elif solution.confidence >= 0.6:
            recommendations.append("Moderate confidence - recommend confirmatory testing")
        else:
            recommendations.append("Low confidence - gather additional clinical data")

        if solution.alternative_solutions:
            recommendations.append(
                f"Consider {len(solution.alternative_solutions)} alternative diagnoses"
            )

        if solution.key_uncertainties:
            recommendations.append("Address key uncertainties before finalizing diagnosis")

        return recommendations

    def create_patient_problem(self, presentation: PatientPresentation) -> Problem:
        """
        Create a Problem from a structured patient presentation.
        """
        # Build description from presentation
        description_parts = [f"Chief complaint: {presentation.chief_complaint}"]

        if presentation.symptoms:
            description_parts.append(f"Symptoms: {', '.join(presentation.symptoms)}")

        if presentation.vital_signs:
            vitals = ', '.join(f"{k}: {v}" for k, v in presentation.vital_signs.items())
            description_parts.append(f"Vital signs: {vitals}")

        if presentation.lab_results:
            labs = ', '.join(f"{k}: {v}" for k, v in presentation.lab_results.items())
            description_parts.append(f"Lab results: {labs}")

        if presentation.medical_history:
            description_parts.append(f"Medical history: {', '.join(presentation.medical_history)}")

        problem = Problem(
            description='\n'.join(description_parts),
            domain="medical",
            context={
                'presentation': presentation.__dict__,
                'clinical_features': {
                    'symptoms': presentation.symptoms,
                    'vitals': presentation.vital_signs,
                    'labs': presentation.lab_results
                }
            }
        )

        return problem

    def format_differential_diagnosis(self, solution: Solution) -> str:
        """
        Format solution as a differential diagnosis report.
        """
        lines = [
            "=" * 60,
            "DIFFERENTIAL DIAGNOSIS REPORT",
            "=" * 60,
            "",
            f"PRIMARY DIAGNOSIS: {solution.content.split(chr(10))[0]}",
            f"Clinical Certainty: {solution.confidence * 100:.1f}%",
            f"Evidence Strength: {solution.grounding_index:.2f}",
            "",
            "-" * 60,
            "EVIDENCE CHAIN:",
            "-" * 60
        ]

        for i, evidence in enumerate(solution.evidence_chain[:5], 1):
            lines.append(f"  {i}. {evidence.content}")
            lines.append(f"     Type: {evidence.evidence_type}, Weight: {evidence.weight:.2f}")

        if solution.alternative_solutions:
            lines.extend([
                "",
                "-" * 60,
                "ALTERNATIVE DIAGNOSES:",
                "-" * 60
            ])

            for i, alt in enumerate(solution.alternative_solutions, 1):
                lines.append(f"  {i}. {alt.content.split(chr(10))[0]}")
                lines.append(f"     Certainty: {alt.confidence * 100:.1f}%")

        if solution.key_uncertainties:
            lines.extend([
                "",
                "-" * 60,
                "KEY UNCERTAINTIES:",
                "-" * 60
            ])

            for uncertainty in solution.key_uncertainties:
                lines.append(f"  • {uncertainty}")

        # Add recommendations
        recommendations = solution.metadata.get('clinical_recommendations', [])
        if recommendations:
            lines.extend([
                "",
                "-" * 60,
                "RECOMMENDATIONS:",
                "-" * 60
            ])

            for rec in recommendations:
                lines.append(f"  → {rec}")

        lines.extend([
            "",
            "=" * 60,
            "DISCLAIMER: AI-assisted analysis. Verify with qualified provider.",
            "=" * 60
        ])

        return '\n'.join(lines)