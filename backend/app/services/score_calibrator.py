"""
Score Calibrator - Evidence-weighted scoring with explanations.

This module provides the scoring system that:
- Weights evidence by type (OBSERVED > BEHAVIORAL > HYPOTHETICAL > SELF_REPORT)
- Applies role-specific valence adjustments
- Matches evidence to behavioral anchors
- Generates human-readable explanations
- Produces final recommendations
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from app.services.patterns import EvidenceType, EVIDENCE_WEIGHTS
from app.services.llm_client import get_llm_client


class Recommendation(str, Enum):
    """Hiring recommendation levels."""
    STRONG_HIRE = "STRONG_HIRE"
    HIRE = "HIRE"
    HOLD = "HOLD"
    NO_HIRE = "NO_HIRE"


@dataclass
class EvidenceForScoring:
    """Evidence item prepared for scoring."""
    source_type: EvidenceType
    source_text: str
    weight: float
    trait_signal: str  # positive, negative, neutral
    signal_strength: float
    star_components: Dict[str, bool]
    contains_conflict: bool = False
    contains_failure: bool = False


@dataclass
class CalibratedTraitScore:
    """A calibrated score for a single trait."""
    trait_id: str
    trait_name: str
    raw_score: int  # 1-5
    calibrated_score: int  # 1-5 after adjustments
    confidence: float
    evidence_summary: str
    evidence_items: List[EvidenceForScoring]
    explanation: str
    score_rationale: str
    matched_anchors: List[str]
    signal_gaps: List[str]
    is_counter_indicator: bool = False
    counter_indicator_severity: Optional[str] = None  # HIGH, MEDIUM, LOW


@dataclass
class CompositeScore:
    """Composite assessment score."""
    composite_score: float  # 0-100
    trait_average: float
    weighted_average: float
    evidence_quality: str  # HIGH, MEDIUM, LOW
    confidence: float
    rationale: str


@dataclass
class AssessmentResult:
    """Complete assessment result."""
    trait_scores: List[CalibratedTraitScore]
    composite_score: CompositeScore
    recommendation: Recommendation
    recommendation_rationale: str
    key_strengths: List[Dict[str, str]]
    development_areas: List[Dict[str, str]]
    counter_indicator_flags: List[Dict[str, Any]]
    assessment_summary: str


class ScoreCalibrator:
    """
    Calibrates and generates final scores from interview evidence.

    The calibrator:
    - Weights evidence by type (OBSERVED: 1.2, BEHAVIORAL: 1.0, etc.)
    - Matches evidence to behavioral anchors
    - Adjusts scores based on evidence quality
    - Applies role-specific valence adjustments
    - Identifies counter-indicators
    - Generates explanations with full evidence traces
    """

    def __init__(self):
        self.llm_client = get_llm_client()

    async def calibrate_trait_score(
        self,
        trait_id: str,
        trait_name: str,
        evidence_items: List[EvidenceForScoring],
        behavioral_anchors: Dict[str, Any],
        role_valence: Optional[Dict[str, Any]] = None,
        counter_indicators: Optional[List[str]] = None,
    ) -> CalibratedTraitScore:
        """
        Calibrate a score for a single trait.

        Args:
            trait_id: Trait identifier
            trait_name: Human-readable trait name
            evidence_items: List of evidence items
            behavioral_anchors: Behavioral anchors for each score level
            role_valence: Optional role-specific valence adjustments
            counter_indicators: Optional list of counter-indicator roles

        Returns:
            CalibratedTraitScore with full explanation
        """
        # Calculate weighted evidence score
        weighted_score = self._calculate_weighted_score(evidence_items)

        # Match evidence to behavioral anchors
        matched_anchors = await self._match_behavioral_anchors(
            evidence_items, behavioral_anchors, trait_name
        )

        # Determine raw score based on anchors and evidence
        raw_score = self._determine_raw_score(weighted_score, matched_anchors)

        # Apply calibration adjustments
        calibrated_score, calibration_notes = self._apply_calibration(
            raw_score, evidence_items, role_valence
        )

        # Check for counter-indicators
        is_counter_indicator = False
        counter_severity = None
        if counter_indicators and calibrated_score >= 4:
            is_counter_indicator = True
            counter_severity = "HIGH" if calibrated_score == 5 else "MEDIUM"

        # Calculate confidence
        confidence = self._calculate_confidence(evidence_items)

        # Identify signal gaps
        signal_gaps = self._identify_signal_gaps(evidence_items)

        # Generate explanation
        explanation = await self._generate_explanation(
            trait_name=trait_name,
            calibrated_score=calibrated_score,
            evidence_items=evidence_items,
            matched_anchors=matched_anchors,
            calibration_notes=calibration_notes,
        )

        # Generate evidence summary
        evidence_summary = self._generate_evidence_summary(evidence_items)

        return CalibratedTraitScore(
            trait_id=trait_id,
            trait_name=trait_name,
            raw_score=raw_score,
            calibrated_score=calibrated_score,
            confidence=confidence,
            evidence_summary=evidence_summary,
            evidence_items=evidence_items,
            explanation=explanation,
            score_rationale=calibration_notes,
            matched_anchors=matched_anchors,
            signal_gaps=signal_gaps,
            is_counter_indicator=is_counter_indicator,
            counter_indicator_severity=counter_severity,
        )

    async def generate_assessment(
        self,
        trait_scores: List[CalibratedTraitScore],
        role_profile: Optional[Dict[str, Any]] = None,
    ) -> AssessmentResult:
        """
        Generate complete assessment from trait scores.

        Args:
            trait_scores: List of calibrated trait scores
            role_profile: Optional role profile for context

        Returns:
            Complete AssessmentResult
        """
        # Calculate composite score
        composite = self._calculate_composite_score(trait_scores)

        # Determine recommendation
        recommendation, rec_rationale = await self._determine_recommendation(
            trait_scores, composite, role_profile
        )

        # Identify strengths and development areas
        strengths = self._identify_strengths(trait_scores)
        development_areas = self._identify_development_areas(trait_scores)

        # Collect counter-indicator flags
        counter_flags = [
            {
                "trait_id": ts.trait_id,
                "trait_name": ts.trait_name,
                "score": ts.calibrated_score,
                "severity": ts.counter_indicator_severity,
                "rationale": f"High {ts.trait_name} may be counter-productive for this role",
            }
            for ts in trait_scores
            if ts.is_counter_indicator
        ]

        # Generate assessment summary
        summary = await self._generate_assessment_summary(
            trait_scores, composite, recommendation, role_profile
        )

        return AssessmentResult(
            trait_scores=trait_scores,
            composite_score=composite,
            recommendation=recommendation,
            recommendation_rationale=rec_rationale,
            key_strengths=strengths,
            development_areas=development_areas,
            counter_indicator_flags=counter_flags,
            assessment_summary=summary,
        )

    def _calculate_weighted_score(
        self,
        evidence_items: List[EvidenceForScoring],
    ) -> float:
        """Calculate weighted average score from evidence."""
        if not evidence_items:
            return 0.0

        total_weight = 0.0
        weighted_sum = 0.0

        for item in evidence_items:
            # Convert signal to numeric
            signal_value = {
                "positive": 1.0,
                "neutral": 0.5,
                "negative": 0.0,
            }.get(item.trait_signal, 0.5)

            # Apply evidence type weight
            type_weight = EVIDENCE_WEIGHTS.get(item.source_type, 0.3)
            combined_weight = type_weight * item.signal_strength

            weighted_sum += signal_value * combined_weight
            total_weight += combined_weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    async def _match_behavioral_anchors(
        self,
        evidence_items: List[EvidenceForScoring],
        behavioral_anchors: Dict[str, Any],
        trait_name: str,
    ) -> List[str]:
        """Match evidence to behavioral anchors using LLM."""
        if not evidence_items or not behavioral_anchors:
            return []

        evidence_texts = [item.source_text for item in evidence_items[:5]]

        prompt = f"""Match this interview evidence to behavioral anchors for {trait_name}.

EVIDENCE:
{chr(10).join(f'- {e}' for e in evidence_texts)}

BEHAVIORAL ANCHORS:
{self._format_anchors(behavioral_anchors)}

Identify which specific behavioral anchor indicators the evidence matches.
Return JSON: {{"matched_anchors": ["Score X: indicator text", ...], "best_fit_score": 1-5}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You match interview evidence to behavioral anchors. Be specific about which indicators match.",
            max_tokens=512,
        )

        return result.get("matched_anchors", [])

    def _determine_raw_score(
        self,
        weighted_score: float,
        matched_anchors: List[str],
    ) -> int:
        """Determine raw score from weighted evidence and anchors."""
        # Base score from weighted evidence
        base_score = int(weighted_score * 4) + 1  # Maps 0-1 to 1-5

        # Adjust based on anchor matches
        if matched_anchors:
            # Extract scores from matched anchors
            anchor_scores = []
            for anchor in matched_anchors:
                for score in range(1, 6):
                    if f"Score {score}" in anchor:
                        anchor_scores.append(score)
                        break

            if anchor_scores:
                avg_anchor = sum(anchor_scores) / len(anchor_scores)
                # Weighted average of base and anchor scores
                final_score = (base_score * 0.4 + avg_anchor * 0.6)
                return max(1, min(5, round(final_score)))

        return max(1, min(5, base_score))

    def _apply_calibration(
        self,
        raw_score: int,
        evidence_items: List[EvidenceForScoring],
        role_valence: Optional[Dict[str, Any]],
    ) -> tuple[int, str]:
        """Apply calibration adjustments to raw score."""
        calibrated = raw_score
        notes = []

        # Check evidence quality
        behavioral_count = sum(
            1 for e in evidence_items
            if e.source_type in (EvidenceType.BEHAVIORAL, EvidenceType.OBSERVED)
        )

        if behavioral_count == 0 and evidence_items:
            # No behavioral evidence - reduce score
            calibrated = max(1, calibrated - 1)
            notes.append("Reduced by 1: no behavioral evidence")

        # Check for conflict/failure examples
        has_tension = any(e.contains_conflict or e.contains_failure for e in evidence_items)
        if not has_tension and len(evidence_items) >= 2:
            notes.append("Note: No conflict/failure examples provided")

        # Apply role valence if provided
        if role_valence:
            optimal_range = role_valence.get("optimal_range", [2, 4])
            if calibrated > optimal_range[1]:
                notes.append(f"Note: Score {calibrated} exceeds optimal range for role ({optimal_range[0]}-{optimal_range[1]})")
            elif calibrated < optimal_range[0]:
                notes.append(f"Note: Score {calibrated} below optimal range for role ({optimal_range[0]}-{optimal_range[1]})")

        return calibrated, "; ".join(notes) if notes else "No adjustments applied"

    def _calculate_confidence(
        self,
        evidence_items: List[EvidenceForScoring],
    ) -> float:
        """Calculate confidence in the assessment."""
        if not evidence_items:
            return 0.0

        # Factors that increase confidence
        confidence = 0.3  # Base confidence

        # Behavioral evidence
        behavioral_count = sum(
            1 for e in evidence_items
            if e.source_type in (EvidenceType.BEHAVIORAL, EvidenceType.OBSERVED)
        )
        confidence += min(0.3, behavioral_count * 0.15)

        # STAR completeness
        star_complete = sum(
            1 for e in evidence_items
            if sum(e.star_components.values()) >= 3
        )
        confidence += min(0.2, star_complete * 0.1)

        # Evidence quantity
        confidence += min(0.1, len(evidence_items) * 0.02)

        # Conflict/tension examples
        if any(e.contains_conflict or e.contains_failure for e in evidence_items):
            confidence += 0.1

        return min(1.0, confidence)

    def _identify_signal_gaps(
        self,
        evidence_items: List[EvidenceForScoring],
    ) -> List[str]:
        """Identify gaps in the evidence."""
        gaps = []

        # Check for behavioral evidence
        behavioral_count = sum(
            1 for e in evidence_items
            if e.source_type in (EvidenceType.BEHAVIORAL, EvidenceType.OBSERVED)
        )
        if behavioral_count == 0:
            gaps.append("No behavioral evidence collected")

        # Check for tension/conflict
        has_tension = any(e.contains_conflict or e.contains_failure for e in evidence_items)
        if not has_tension:
            gaps.append("No conflict/failure example provided")

        # Check STAR completeness
        fully_complete = sum(
            1 for e in evidence_items
            if all(e.star_components.get(c, False) for c in ["situation", "task", "action", "result"])
        )
        if fully_complete == 0 and evidence_items:
            gaps.append("No fully STAR-complete examples")

        return gaps

    async def _generate_explanation(
        self,
        trait_name: str,
        calibrated_score: int,
        evidence_items: List[EvidenceForScoring],
        matched_anchors: List[str],
        calibration_notes: str,
    ) -> str:
        """Generate human-readable explanation for the score."""
        evidence_summary = "\n".join([
            f"- [{e.source_type.value}] {e.source_text[:100]}..."
            for e in evidence_items[:3]
        ])

        prompt = f"""Generate a clear, professional explanation for this trait assessment.

TRAIT: {trait_name}
SCORE: {calibrated_score}/5

SUPPORTING EVIDENCE:
{evidence_summary}

MATCHED BEHAVIORAL ANCHORS:
{chr(10).join(f'- {a}' for a in matched_anchors[:3]) if matched_anchors else 'None identified'}

CALIBRATION NOTES: {calibration_notes}

Write a 2-3 sentence explanation that:
1. States the score and what it means
2. Cites specific evidence that supports it
3. Notes any limitations or areas for follow-up

Keep it professional and objective."""

        result = await self.llm_client.complete(
            prompt=prompt,
            system_prompt="You write clear, evidence-based assessment explanations.",
            max_tokens=256,
        )

        return result if isinstance(result, str) else str(result)

    def _generate_evidence_summary(
        self,
        evidence_items: List[EvidenceForScoring],
    ) -> str:
        """Generate a brief summary of the evidence."""
        if not evidence_items:
            return "No evidence collected."

        type_counts = {}
        for item in evidence_items:
            type_name = item.source_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1

        parts = [f"{count} {type_name.lower()}" for type_name, count in type_counts.items()]
        return f"Based on {len(evidence_items)} evidence items: {', '.join(parts)}."

    def _calculate_composite_score(
        self,
        trait_scores: List[CalibratedTraitScore],
    ) -> CompositeScore:
        """Calculate composite score from trait scores."""
        if not trait_scores:
            return CompositeScore(
                composite_score=0.0,
                trait_average=0.0,
                weighted_average=0.0,
                evidence_quality="LOW",
                confidence=0.0,
                rationale="No trait scores available",
            )

        # Simple average
        trait_avg = sum(ts.calibrated_score for ts in trait_scores) / len(trait_scores)

        # Weighted by confidence
        total_conf = sum(ts.confidence for ts in trait_scores)
        if total_conf > 0:
            weighted_avg = sum(
                ts.calibrated_score * ts.confidence for ts in trait_scores
            ) / total_conf
        else:
            weighted_avg = trait_avg

        # Convert to 0-100 scale
        composite = (weighted_avg - 1) / 4 * 100

        # Determine evidence quality
        avg_confidence = total_conf / len(trait_scores) if trait_scores else 0
        if avg_confidence >= 0.7:
            quality = "HIGH"
        elif avg_confidence >= 0.4:
            quality = "MEDIUM"
        else:
            quality = "LOW"

        return CompositeScore(
            composite_score=round(composite, 1),
            trait_average=round(trait_avg, 2),
            weighted_average=round(weighted_avg, 2),
            evidence_quality=quality,
            confidence=round(avg_confidence, 2),
            rationale=f"Based on {len(trait_scores)} traits with {quality.lower()} confidence evidence",
        )

    async def _determine_recommendation(
        self,
        trait_scores: List[CalibratedTraitScore],
        composite: CompositeScore,
        role_profile: Optional[Dict[str, Any]],
    ) -> tuple[Recommendation, str]:
        """Determine hiring recommendation."""
        # Check for counter-indicators
        counter_indicators = [ts for ts in trait_scores if ts.is_counter_indicator]
        if any(ci.counter_indicator_severity == "HIGH" for ci in counter_indicators):
            return Recommendation.HOLD, "Counter-indicator flag requires human review"

        # Determine based on composite score
        if composite.composite_score >= 75 and composite.confidence >= 0.6:
            return Recommendation.STRONG_HIRE, f"Strong performance across traits ({composite.composite_score:.0f}/100) with good evidence quality"

        elif composite.composite_score >= 60 and composite.confidence >= 0.5:
            return Recommendation.HIRE, f"Solid performance ({composite.composite_score:.0f}/100) meeting key requirements"

        elif composite.composite_score >= 40 or composite.confidence < 0.4:
            return Recommendation.HOLD, f"Additional evaluation recommended (score: {composite.composite_score:.0f}/100, confidence: {composite.confidence:.0%})"

        else:
            return Recommendation.NO_HIRE, f"Performance below threshold ({composite.composite_score:.0f}/100)"

    def _identify_strengths(
        self,
        trait_scores: List[CalibratedTraitScore],
    ) -> List[Dict[str, str]]:
        """Identify key strengths from trait scores."""
        strengths = []
        for ts in sorted(trait_scores, key=lambda x: x.calibrated_score, reverse=True)[:3]:
            if ts.calibrated_score >= 4:
                strengths.append({
                    "trait_id": ts.trait_id,
                    "trait_name": ts.trait_name,
                    "description": f"Strong {ts.trait_name.lower()} (score: {ts.calibrated_score}/5)",
                })
        return strengths

    def _identify_development_areas(
        self,
        trait_scores: List[CalibratedTraitScore],
    ) -> List[Dict[str, str]]:
        """Identify development areas from trait scores."""
        areas = []
        for ts in sorted(trait_scores, key=lambda x: x.calibrated_score)[:2]:
            if ts.calibrated_score <= 2:
                areas.append({
                    "trait_id": ts.trait_id,
                    "trait_name": ts.trait_name,
                    "description": f"Opportunity to develop {ts.trait_name.lower()} (score: {ts.calibrated_score}/5)",
                    "suggestions": ts.signal_gaps,
                })
        return areas

    async def _generate_assessment_summary(
        self,
        trait_scores: List[CalibratedTraitScore],
        composite: CompositeScore,
        recommendation: Recommendation,
        role_profile: Optional[Dict[str, Any]],
    ) -> str:
        """Generate overall assessment summary."""
        traits_summary = ", ".join([
            f"{ts.trait_name} ({ts.calibrated_score}/5)"
            for ts in sorted(trait_scores, key=lambda x: x.calibrated_score, reverse=True)[:4]
        ])

        prompt = f"""Write a brief (3-4 sentence) professional assessment summary.

RECOMMENDATION: {recommendation.value}
COMPOSITE SCORE: {composite.composite_score:.0f}/100
EVIDENCE QUALITY: {composite.evidence_quality}
TOP TRAITS: {traits_summary}

Write an objective, balanced summary suitable for a hiring manager."""

        result = await self.llm_client.complete(
            prompt=prompt,
            system_prompt="You write professional, balanced candidate assessment summaries.",
            max_tokens=200,
        )

        return result if isinstance(result, str) else str(result)

    def _format_anchors(self, anchors: Dict[str, Any]) -> str:
        """Format behavioral anchors for prompt."""
        lines = []
        for score, data in sorted(anchors.items()):
            if isinstance(data, dict):
                indicators = data.get("indicators", [])
                lines.append(f"Score {score}: {', '.join(indicators[:3])}")
        return "\n".join(lines)


# Singleton instance
_score_calibrator: Optional[ScoreCalibrator] = None


def get_score_calibrator() -> ScoreCalibrator:
    """Get the score calibrator instance."""
    global _score_calibrator
    if _score_calibrator is None:
        _score_calibrator = ScoreCalibrator()
    return _score_calibrator
