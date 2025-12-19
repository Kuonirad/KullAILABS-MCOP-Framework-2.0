"""
M-COP v3.1 Grounding Index System

Implements the evidence grounding system that tracks and weights
evidence quality across different domains and evidence types.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum, auto
import math

from .mcop_types import Evidence, Hypothesis, ReasoningChain


class EvidenceQuality(Enum):
    """Standard evidence quality levels."""
    GOLD = auto()      # Highest quality (RCTs, reproduced experiments)
    HIGH = auto()      # Strong evidence (peer-reviewed, validated)
    MODERATE = auto()  # Acceptable evidence (case studies, observations)
    LOW = auto()       # Weak evidence (anecdotal, theoretical)
    MINIMAL = auto()   # Very weak (speculation, unverified)


@dataclass
class EvidenceHierarchy:
    """
    Defines the evidence hierarchy for a domain.
    Maps evidence types to quality weights.
    """
    name: str
    weights: Dict[str, float] = field(default_factory=dict)
    default_weight: float = 0.5

    def get_weight(self, evidence_type: str) -> float:
        """Get the weight for an evidence type."""
        return self.weights.get(evidence_type, self.default_weight)

    def add_type(self, evidence_type: str, weight: float):
        """Add or update an evidence type weight."""
        self.weights[evidence_type] = max(0.0, min(1.0, weight))


# Pre-defined domain hierarchies
GENERAL_HIERARCHY = EvidenceHierarchy(
    name="general",
    weights={
        'verified_fact': 1.0,
        'peer_reviewed': 0.9,
        'expert_consensus': 0.85,
        'documented_observation': 0.7,
        'logical_inference': 0.6,
        'theoretical': 0.5,
        'anecdotal': 0.3,
        'speculation': 0.2
    }
)

MEDICAL_HIERARCHY = EvidenceHierarchy(
    name="medical",
    weights={
        'randomized_controlled_trial': 1.0,
        'systematic_review': 0.95,
        'cohort_study': 0.85,
        'case_control_study': 0.70,
        'case_series': 0.50,
        'case_report': 0.40,
        'expert_opinion': 0.30,
        'mechanistic_reasoning': 0.60,
        'lab_result': 1.0,
        'imaging': 0.95,
        'pathology': 0.95
    }
)

SCIENTIFIC_HIERARCHY = EvidenceHierarchy(
    name="scientific",
    weights={
        'reproduced_experiment': 1.0,
        'peer_reviewed_publication': 0.90,
        'preprint_with_methods': 0.70,
        'conference_abstract': 0.50,
        'theoretical_prediction': 0.40,
        'computational_model': 0.60,
        'observational_data': 0.75,
        'anecdotal_observation': 0.20
    }
)

CREATIVE_HIERARCHY = EvidenceHierarchy(
    name="creative",
    weights={
        'client_explicit_requirement': 1.0,
        'reference_materials': 0.95,
        'historical_precedent': 0.85,
        'user_research': 0.80,
        'focus_group': 0.75,
        'artist_intuition': 0.60,
        'trend_prediction': 0.40
    }
)


class GroundingCalculator:
    """
    Calculates grounding indices for hypotheses and chains.

    The grounding index represents how well-supported a claim is
    by evidence, weighted by evidence quality.
    """

    def __init__(self, hierarchy: Optional[EvidenceHierarchy] = None):
        self.hierarchy = hierarchy or GENERAL_HIERARCHY

        # Configurable parameters
        self.min_evidence_for_grounding = 1
        self.evidence_diminishing_factor = 0.9  # Each additional evidence worth slightly less
        self.recency_weight = 0.1  # Weight for recent evidence

    def calculate_hypothesis_grounding(self, hypothesis: Hypothesis) -> float:
        """
        Calculate the grounding index for a hypothesis.

        Formula:
        G = Σ(w_i * q_i * d^i) / Σ(d^i)

        Where:
        - w_i = weight of evidence type
        - q_i = quality modifier (0-1)
        - d = diminishing factor
        - i = evidence index
        """
        if len(hypothesis.evidence) < self.min_evidence_for_grounding:
            return 0.0

        weighted_sum = 0.0
        weight_total = 0.0

        for i, evidence in enumerate(hypothesis.evidence):
            # Get base weight from hierarchy
            base_weight = self.hierarchy.get_weight(evidence.evidence_type)

            # Apply evidence's own weight modifier
            effective_weight = base_weight * evidence.weight

            # Apply diminishing returns
            diminish = self.evidence_diminishing_factor ** i

            weighted_sum += effective_weight * diminish
            weight_total += diminish

        if weight_total == 0:
            return 0.0

        grounding = weighted_sum / weight_total
        return min(1.0, max(0.0, grounding))

    def calculate_chain_grounding(self, chain: ReasoningChain) -> float:
        """
        Calculate the aggregate grounding for a reasoning chain.

        Considers:
        - Individual hypothesis groundings
        - Chain coherence (connected evidence)
        - Validation status
        """
        if not chain.hypotheses:
            return 0.0

        # Calculate individual groundings
        groundings = []
        for h in chain.hypotheses:
            if h.grounding_index == 0:
                h.grounding_index = self.calculate_hypothesis_grounding(h)
            groundings.append(h.grounding_index)

        # Base: weighted average (later hypotheses weighted more)
        weighted_sum = 0.0
        weight_total = 0.0

        for i, g in enumerate(groundings):
            weight = 1.0 + i * 0.1  # Later hypotheses weighted slightly more
            weighted_sum += g * weight
            weight_total += weight

        base_grounding = weighted_sum / weight_total if weight_total > 0 else 0.0

        # Coherence bonus: if evidence connects across hypotheses
        coherence_bonus = self._calculate_coherence(chain) * 0.1

        # Validation bonus
        validation_bonus = 0.1 if chain.is_complete else 0.0

        return min(1.0, base_grounding + coherence_bonus + validation_bonus)

    def _calculate_coherence(self, chain: ReasoningChain) -> float:
        """Calculate evidence coherence across the chain."""
        if len(chain.hypotheses) < 2:
            return 0.0

        # Check for evidence type consistency
        all_types = []
        for h in chain.hypotheses:
            all_types.extend(e.evidence_type for e in h.evidence)

        if not all_types:
            return 0.0

        # More unique types = less coherence (more diverse evidence)
        unique_ratio = len(set(all_types)) / len(all_types)

        # We want some diversity but not too much
        # Optimal is around 0.3-0.5 unique ratio
        if unique_ratio < 0.3:
            return 0.8  # Very coherent
        elif unique_ratio < 0.5:
            return 1.0  # Optimal diversity
        elif unique_ratio < 0.7:
            return 0.7  # Good diversity
        else:
            return 0.4  # Too fragmented

    def update_grounding(self, hypothesis: Hypothesis) -> float:
        """Update and return the grounding index for a hypothesis."""
        hypothesis.grounding_index = self.calculate_hypothesis_grounding(hypothesis)
        return hypothesis.grounding_index

    def set_hierarchy(self, hierarchy: EvidenceHierarchy):
        """Set a new evidence hierarchy."""
        self.hierarchy = hierarchy


@dataclass
class GroundingReport:
    """
    Detailed grounding report for a hypothesis or chain.
    """
    subject_id: str
    grounding_index: float
    evidence_breakdown: List[Dict[str, Any]] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'subject_id': self.subject_id,
            'grounding_index': f"{self.grounding_index:.2f}",
            'evidence_breakdown': self.evidence_breakdown,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'recommendations': self.recommendations
        }


class GroundingAnalyzer:
    """
    Analyzes grounding and provides detailed reports.
    """

    def __init__(self, calculator: Optional[GroundingCalculator] = None):
        self.calculator = calculator or GroundingCalculator()

    def analyze_hypothesis(self, hypothesis: Hypothesis) -> GroundingReport:
        """Generate a detailed grounding report for a hypothesis."""
        grounding = self.calculator.calculate_hypothesis_grounding(hypothesis)

        report = GroundingReport(
            subject_id=hypothesis.id,
            grounding_index=grounding
        )

        # Break down evidence
        for evidence in hypothesis.evidence:
            weight = self.calculator.hierarchy.get_weight(evidence.evidence_type)
            report.evidence_breakdown.append({
                'content': evidence.content[:50] + '...' if len(evidence.content) > 50 else evidence.content,
                'type': evidence.evidence_type,
                'hierarchy_weight': weight,
                'evidence_weight': evidence.weight,
                'effective_weight': weight * evidence.weight
            })

        # Identify strengths
        high_quality = [e for e in hypothesis.evidence if e.weight >= 0.8]
        if high_quality:
            report.strengths.append(f"{len(high_quality)} high-quality evidence items")

        if grounding >= 0.8:
            report.strengths.append("Strong overall grounding")

        # Identify weaknesses
        if len(hypothesis.evidence) < 3:
            report.weaknesses.append("Limited evidence base")

        low_quality = [e for e in hypothesis.evidence if e.weight < 0.4]
        if low_quality:
            report.weaknesses.append(f"{len(low_quality)} low-quality evidence items")

        if grounding < 0.5:
            report.weaknesses.append("Weak overall grounding")

        # Generate recommendations
        if grounding < 0.6:
            report.recommendations.append("Gather additional high-quality evidence")

        if not high_quality:
            report.recommendations.append("Seek gold-standard evidence (RCTs, reproduced experiments)")

        return report

    def analyze_chain(self, chain: ReasoningChain) -> GroundingReport:
        """Generate a detailed grounding report for a reasoning chain."""
        grounding = self.calculator.calculate_chain_grounding(chain)

        report = GroundingReport(
            subject_id=chain.id,
            grounding_index=grounding
        )

        # Analyze each hypothesis in chain
        for h in chain.hypotheses:
            h_grounding = self.calculator.calculate_hypothesis_grounding(h)
            report.evidence_breakdown.append({
                'hypothesis_id': h.id,
                'content': h.content[:50] + '...',
                'grounding': h_grounding,
                'evidence_count': len(h.evidence),
                'state': h.state.name
            })

        # Chain-level analysis
        if chain.is_complete:
            report.strengths.append("Chain reached validation")

        avg_grounding = sum(
            self.calculator.calculate_hypothesis_grounding(h)
            for h in chain.hypotheses
        ) / max(1, len(chain.hypotheses))

        if avg_grounding >= 0.7:
            report.strengths.append("Strong average hypothesis grounding")

        if chain.depth >= 3:
            report.strengths.append(f"Deep reasoning chain (depth {chain.depth})")

        # Weaknesses
        weak_hypotheses = [
            h for h in chain.hypotheses
            if self.calculator.calculate_hypothesis_grounding(h) < 0.4
        ]
        if weak_hypotheses:
            report.weaknesses.append(f"{len(weak_hypotheses)} weakly grounded hypotheses")

        return report

    def compare_groundings(
        self,
        items: List[Hypothesis]
    ) -> List[Dict[str, Any]]:
        """Compare grounding across multiple hypotheses."""
        results = []

        for h in items:
            grounding = self.calculator.calculate_hypothesis_grounding(h)
            results.append({
                'id': h.id,
                'content': h.content[:40] + '...',
                'grounding': grounding,
                'evidence_count': len(h.evidence),
                'mode': h.mode.name
            })

        # Sort by grounding
        results.sort(key=lambda x: x['grounding'], reverse=True)

        return results


class DomainGroundingFactory:
    """
    Factory for creating domain-specific grounding calculators.
    """

    _hierarchies: Dict[str, EvidenceHierarchy] = {
        'general': GENERAL_HIERARCHY,
        'medical': MEDICAL_HIERARCHY,
        'scientific': SCIENTIFIC_HIERARCHY,
        'creative': CREATIVE_HIERARCHY
    }

    @classmethod
    def get_calculator(cls, domain: str) -> GroundingCalculator:
        """Get a grounding calculator for a specific domain."""
        hierarchy = cls._hierarchies.get(domain, GENERAL_HIERARCHY)
        return GroundingCalculator(hierarchy)

    @classmethod
    def register_hierarchy(cls, name: str, hierarchy: EvidenceHierarchy):
        """Register a new domain hierarchy."""
        cls._hierarchies[name] = hierarchy

    @classmethod
    def list_domains(cls) -> List[str]:
        """List available domain hierarchies."""
        return list(cls._hierarchies.keys())