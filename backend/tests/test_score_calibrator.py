"""
Tests for the score calibrator: evidence weighting, raw scores,
recommendations, composite scoring, strengths and development areas.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.services.score_calibrator import (
    ScoreCalibrator,
    EvidenceForScoring,
    CalibratedTraitScore,
    CompositeScore,
    Recommendation,
)
from app.services.patterns import EvidenceType, EVIDENCE_WEIGHTS


# ---- Helpers ----

def _make_evidence(
    source_type: EvidenceType = EvidenceType.BEHAVIORAL,
    trait_signal: str = "positive",
    signal_strength: float = 0.8,
    contains_conflict: bool = False,
    contains_failure: bool = False,
    star_complete: bool = False,
) -> EvidenceForScoring:
    """Create an EvidenceForScoring with sensible defaults."""
    return EvidenceForScoring(
        source_type=source_type,
        source_text="Sample evidence text",
        weight=EVIDENCE_WEIGHTS.get(source_type, 0.3),
        trait_signal=trait_signal,
        signal_strength=signal_strength,
        star_components={
            "situation": star_complete, "task": star_complete,
            "action": star_complete, "result": star_complete,
        },
        contains_conflict=contains_conflict,
        contains_failure=contains_failure,
    )


def _make_trait_score(
    trait_id: str = "t1",
    trait_name: str = "Leadership",
    calibrated_score: int = 4,
    confidence: float = 0.7,
    is_counter_indicator: bool = False,
    counter_indicator_severity: str = None,
) -> CalibratedTraitScore:
    """Create a CalibratedTraitScore with sensible defaults."""
    return CalibratedTraitScore(
        trait_id=trait_id,
        trait_name=trait_name,
        raw_score=calibrated_score,
        calibrated_score=calibrated_score,
        confidence=confidence,
        evidence_summary="Test evidence",
        evidence_items=[],
        explanation="Test explanation",
        score_rationale="Test rationale",
        matched_anchors=[],
        signal_gaps=[],
        is_counter_indicator=is_counter_indicator,
        counter_indicator_severity=counter_indicator_severity,
    )


def _make_calibrator() -> ScoreCalibrator:
    """Create a ScoreCalibrator with mocked LLM client."""
    calibrator = ScoreCalibrator.__new__(ScoreCalibrator)
    calibrator.llm_client = MagicMock()
    return calibrator


# ---- Test Classes ----

class TestWeightedScoreCalculation:
    """_calculate_weighted_score tests."""

    def test_empty_evidence_returns_zero(self):
        """Empty evidence list returns 0.0."""
        cal = _make_calibrator()
        assert cal._calculate_weighted_score([]) == 0.0

    def test_single_positive_observed_evidence(self):
        """Single positive OBSERVED evidence produces high score."""
        cal = _make_calibrator()
        evidence = [_make_evidence(
            source_type=EvidenceType.OBSERVED,
            trait_signal="positive",
            signal_strength=1.0,
        )]
        score = cal._calculate_weighted_score(evidence)
        # positive=1.0, OBSERVED weight=1.2, strength=1.0 → 1.0
        assert score == pytest.approx(1.0)

    def test_single_negative_self_report_evidence(self):
        """Single negative SELF_REPORT produces low score."""
        cal = _make_calibrator()
        evidence = [_make_evidence(
            source_type=EvidenceType.SELF_REPORT,
            trait_signal="negative",
            signal_strength=1.0,
        )]
        score = cal._calculate_weighted_score(evidence)
        # negative=0.0, so weighted score = 0.0
        assert score == pytest.approx(0.0)

    def test_mixed_evidence_weighted_correctly(self):
        """Mixed positive/negative evidence with different types gives intermediate score."""
        cal = _make_calibrator()
        evidence = [
            _make_evidence(
                source_type=EvidenceType.BEHAVIORAL,
                trait_signal="positive",
                signal_strength=0.8,
            ),
            _make_evidence(
                source_type=EvidenceType.SELF_REPORT,
                trait_signal="negative",
                signal_strength=0.8,
            ),
        ]
        score = cal._calculate_weighted_score(evidence)
        # positive BEHAVIORAL: signal=1.0, weight=1.0*0.8=0.8, contribution=0.8
        # negative SELF_REPORT: signal=0.0, weight=0.3*0.8=0.24, contribution=0.0
        # total_weight=1.04, weighted_sum=0.8
        # score = 0.8/1.04 ≈ 0.769
        assert 0.5 < score < 1.0

    def test_neutral_signal_gives_half(self):
        """Neutral signal maps to 0.5."""
        cal = _make_calibrator()
        evidence = [_make_evidence(
            source_type=EvidenceType.BEHAVIORAL,
            trait_signal="neutral",
            signal_strength=1.0,
        )]
        score = cal._calculate_weighted_score(evidence)
        assert score == pytest.approx(0.5)

    def test_signal_strength_affects_weighting(self):
        """Higher signal_strength gives more weight to that evidence item."""
        cal = _make_calibrator()
        # Strong positive + weak negative: should be > 0.5
        evidence = [
            _make_evidence(trait_signal="positive", signal_strength=1.0),
            _make_evidence(trait_signal="negative", signal_strength=0.1),
        ]
        score = cal._calculate_weighted_score(evidence)
        assert score > 0.8


class TestDetermineRawScore:
    """_determine_raw_score tests."""

    def test_high_weighted_score_with_high_anchors(self):
        """High weighted score + high anchor match → score 5."""
        cal = _make_calibrator()
        score = cal._determine_raw_score(1.0, ["Score 5: excellent leader"])
        assert score == 5

    def test_low_weighted_score_no_anchors(self):
        """Low weighted score with no anchors → score 1."""
        cal = _make_calibrator()
        score = cal._determine_raw_score(0.0, [])
        assert score == 1

    def test_mid_range_no_anchors(self):
        """Mid-range weighted score with no anchors → score 3."""
        cal = _make_calibrator()
        score = cal._determine_raw_score(0.5, [])
        assert score == 3

    def test_anchors_influence_final_score(self):
        """Anchors weighted 60% vs base 40%."""
        cal = _make_calibrator()
        # base from 0.5 = 3, anchor score 5 → 3*0.4 + 5*0.6 = 4.2 → 4
        score = cal._determine_raw_score(0.5, ["Score 5: strong evidence"])
        assert score == 4

    def test_score_clamped_to_1_5(self):
        """Score is always between 1 and 5."""
        cal = _make_calibrator()
        assert cal._determine_raw_score(0.0, []) >= 1
        assert cal._determine_raw_score(1.0, ["Score 5: max"]) <= 5


class TestRecommendation:
    """_determine_recommendation tests."""

    @pytest.mark.asyncio
    async def test_strong_hire_high_score_high_confidence(self):
        """score>=75, confidence>=0.6 → STRONG_HIRE."""
        cal = _make_calibrator()
        composite = CompositeScore(
            composite_score=80.0, trait_average=4.2, weighted_average=4.2,
            evidence_quality="HIGH", confidence=0.7, rationale="",
        )
        rec, _ = await cal._determine_recommendation([], composite, None)
        assert rec == Recommendation.STRONG_HIRE

    @pytest.mark.asyncio
    async def test_strong_hire_boundary(self):
        """score=75, confidence=0.6 → STRONG_HIRE (boundary)."""
        cal = _make_calibrator()
        composite = CompositeScore(
            composite_score=75.0, trait_average=4.0, weighted_average=4.0,
            evidence_quality="HIGH", confidence=0.6, rationale="",
        )
        rec, _ = await cal._determine_recommendation([], composite, None)
        assert rec == Recommendation.STRONG_HIRE

    @pytest.mark.asyncio
    async def test_hire_just_below_strong(self):
        """score=74, confidence=0.6 → HIRE (just below STRONG_HIRE threshold)."""
        cal = _make_calibrator()
        composite = CompositeScore(
            composite_score=74.0, trait_average=3.9, weighted_average=3.9,
            evidence_quality="HIGH", confidence=0.6, rationale="",
        )
        rec, _ = await cal._determine_recommendation([], composite, None)
        assert rec == Recommendation.HIRE

    @pytest.mark.asyncio
    async def test_hire_mid_range(self):
        """score=65, confidence=0.5 → HIRE."""
        cal = _make_calibrator()
        composite = CompositeScore(
            composite_score=65.0, trait_average=3.6, weighted_average=3.6,
            evidence_quality="MEDIUM", confidence=0.5, rationale="",
        )
        rec, _ = await cal._determine_recommendation([], composite, None)
        assert rec == Recommendation.HIRE

    @pytest.mark.asyncio
    async def test_hold_mid_score(self):
        """score=45, confidence=0.5 → HOLD."""
        cal = _make_calibrator()
        composite = CompositeScore(
            composite_score=45.0, trait_average=2.8, weighted_average=2.8,
            evidence_quality="MEDIUM", confidence=0.5, rationale="",
        )
        rec, _ = await cal._determine_recommendation([], composite, None)
        assert rec == Recommendation.HOLD

    @pytest.mark.asyncio
    async def test_no_hire_low_score(self):
        """score=30, confidence=0.5 → NO_HIRE."""
        cal = _make_calibrator()
        composite = CompositeScore(
            composite_score=30.0, trait_average=2.2, weighted_average=2.2,
            evidence_quality="MEDIUM", confidence=0.5, rationale="",
        )
        rec, _ = await cal._determine_recommendation([], composite, None)
        assert rec == Recommendation.NO_HIRE

    @pytest.mark.asyncio
    async def test_hold_low_confidence_override(self):
        """High score but low confidence → HOLD."""
        cal = _make_calibrator()
        composite = CompositeScore(
            composite_score=80.0, trait_average=4.2, weighted_average=4.2,
            evidence_quality="LOW", confidence=0.3, rationale="",
        )
        rec, _ = await cal._determine_recommendation([], composite, None)
        assert rec == Recommendation.HOLD

    @pytest.mark.asyncio
    async def test_counter_indicator_high_forces_hold(self):
        """HIGH counter-indicator → HOLD regardless of score."""
        cal = _make_calibrator()
        trait_scores = [_make_trait_score(
            is_counter_indicator=True,
            counter_indicator_severity="HIGH",
        )]
        composite = CompositeScore(
            composite_score=90.0, trait_average=4.6, weighted_average=4.6,
            evidence_quality="HIGH", confidence=0.9, rationale="",
        )
        rec, _ = await cal._determine_recommendation(trait_scores, composite, None)
        assert rec == Recommendation.HOLD


class TestCompositeScore:
    """_calculate_composite_score tests."""

    def test_all_high_scores(self):
        """All high calibrated scores → composite > 75."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", calibrated_score=5, confidence=0.8),
            _make_trait_score(trait_id="t2", calibrated_score=5, confidence=0.8),
            _make_trait_score(trait_id="t3", calibrated_score=4, confidence=0.7),
        ]
        composite = cal._calculate_composite_score(scores)
        assert composite.composite_score > 75

    def test_all_low_scores(self):
        """All low calibrated scores → composite < 40."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", calibrated_score=1, confidence=0.5),
            _make_trait_score(trait_id="t2", calibrated_score=1, confidence=0.5),
            _make_trait_score(trait_id="t3", calibrated_score=2, confidence=0.4),
        ]
        composite = cal._calculate_composite_score(scores)
        assert composite.composite_score < 40

    def test_mixed_scores_proportional(self):
        """Mixed scores produce proportional composite."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", calibrated_score=5, confidence=0.8),
            _make_trait_score(trait_id="t2", calibrated_score=1, confidence=0.5),
        ]
        composite = cal._calculate_composite_score(scores)
        assert 20 < composite.composite_score < 80

    def test_empty_scores(self):
        """No trait scores → composite 0."""
        cal = _make_calibrator()
        composite = cal._calculate_composite_score([])
        assert composite.composite_score == 0.0
        assert composite.evidence_quality == "LOW"

    def test_evidence_quality_high(self):
        """High average confidence → HIGH evidence quality."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", confidence=0.8),
            _make_trait_score(trait_id="t2", confidence=0.7),
        ]
        composite = cal._calculate_composite_score(scores)
        assert composite.evidence_quality == "HIGH"

    def test_evidence_quality_medium(self):
        """Medium confidence → MEDIUM evidence quality."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", confidence=0.5),
            _make_trait_score(trait_id="t2", confidence=0.5),
        ]
        composite = cal._calculate_composite_score(scores)
        assert composite.evidence_quality == "MEDIUM"

    def test_evidence_quality_low(self):
        """Low confidence → LOW evidence quality."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", confidence=0.2),
            _make_trait_score(trait_id="t2", confidence=0.3),
        ]
        composite = cal._calculate_composite_score(scores)
        assert composite.evidence_quality == "LOW"


class TestIdentifyStrengths:
    """_identify_strengths tests."""

    def test_scores_at_4_or_above_are_strengths(self):
        """Scores >= 4 identified as strengths."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", trait_name="Leadership", calibrated_score=5),
            _make_trait_score(trait_id="t2", trait_name="Empathy", calibrated_score=4),
            _make_trait_score(trait_id="t3", trait_name="Grit", calibrated_score=3),
        ]
        strengths = cal._identify_strengths(scores)
        names = [s["trait_name"] for s in strengths]
        assert "Leadership" in names
        assert "Empathy" in names
        assert "Grit" not in names

    def test_max_three_strengths(self):
        """At most 3 strengths returned even if more qualify."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id=f"t{i}", trait_name=f"Trait{i}", calibrated_score=5)
            for i in range(5)
        ]
        strengths = cal._identify_strengths(scores)
        assert len(strengths) <= 3

    def test_no_strengths_when_all_low(self):
        """No scores >= 4 → empty list."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", calibrated_score=2),
            _make_trait_score(trait_id="t2", calibrated_score=3),
        ]
        strengths = cal._identify_strengths(scores)
        assert len(strengths) == 0


class TestIdentifyDevelopmentAreas:
    """_identify_development_areas tests."""

    def test_scores_at_2_or_below_are_dev_areas(self):
        """Scores <= 2 identified as development areas."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", trait_name="Leadership", calibrated_score=1),
            _make_trait_score(trait_id="t2", trait_name="Empathy", calibrated_score=2),
            _make_trait_score(trait_id="t3", trait_name="Grit", calibrated_score=3),
        ]
        areas = cal._identify_development_areas(scores)
        names = [a["trait_name"] for a in areas]
        assert "Leadership" in names
        assert "Empathy" in names
        assert "Grit" not in names

    def test_max_two_dev_areas(self):
        """At most 2 development areas returned."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id=f"t{i}", calibrated_score=1) for i in range(5)
        ]
        areas = cal._identify_development_areas(scores)
        assert len(areas) <= 2

    def test_no_dev_areas_when_all_high(self):
        """No scores <= 2 → empty list."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(trait_id="t1", calibrated_score=4),
            _make_trait_score(trait_id="t2", calibrated_score=5),
        ]
        areas = cal._identify_development_areas(scores)
        assert len(areas) == 0


class TestApplyCalibration:
    """_apply_calibration tests."""

    def test_no_behavioral_evidence_reduces_score(self):
        """Score reduced by 1 when no behavioral/observed evidence."""
        cal = _make_calibrator()
        evidence = [_make_evidence(source_type=EvidenceType.SELF_REPORT)]
        calibrated, notes = cal._apply_calibration(4, evidence, None)
        assert calibrated == 3
        assert "no behavioral evidence" in notes.lower()

    def test_with_behavioral_evidence_no_reduction(self):
        """Score preserved when behavioral evidence exists."""
        cal = _make_calibrator()
        evidence = [_make_evidence(source_type=EvidenceType.BEHAVIORAL)]
        calibrated, notes = cal._apply_calibration(4, evidence, None)
        assert calibrated == 4

    def test_score_never_below_one(self):
        """Calibrated score cannot go below 1."""
        cal = _make_calibrator()
        evidence = [_make_evidence(source_type=EvidenceType.SELF_REPORT)]
        calibrated, _ = cal._apply_calibration(1, evidence, None)
        assert calibrated >= 1


class TestCalculateConfidence:
    """_calculate_confidence tests."""

    def test_empty_evidence_zero_confidence(self):
        """No evidence → 0.0 confidence."""
        cal = _make_calibrator()
        assert cal._calculate_confidence([]) == 0.0

    def test_base_confidence_with_single_self_report(self):
        """Single self-report evidence → base confidence (0.3 + quantity bonus)."""
        cal = _make_calibrator()
        evidence = [_make_evidence(source_type=EvidenceType.SELF_REPORT)]
        conf = cal._calculate_confidence(evidence)
        assert conf == pytest.approx(0.32)  # 0.3 base + 0.02 quantity

    def test_behavioral_evidence_increases_confidence(self):
        """Behavioral evidence adds to confidence."""
        cal = _make_calibrator()
        evidence = [
            _make_evidence(source_type=EvidenceType.BEHAVIORAL),
            _make_evidence(source_type=EvidenceType.BEHAVIORAL),
        ]
        conf = cal._calculate_confidence(evidence)
        # 0.3 + 0.3 (2 behavioral, capped at 0.3) + 0.04 quantity = 0.64
        assert conf == pytest.approx(0.64)

    def test_conflict_evidence_adds_confidence(self):
        """Conflict/failure evidence adds 0.1 to confidence."""
        cal = _make_calibrator()
        evidence = [_make_evidence(contains_conflict=True)]
        conf = cal._calculate_confidence(evidence)
        # 0.3 + 0.15 (1 behavioral) + 0.02 (1 item) + 0.1 (conflict) = 0.57
        assert conf == pytest.approx(0.57)

    def test_confidence_capped_at_one(self):
        """Confidence never exceeds 1.0."""
        cal = _make_calibrator()
        evidence = [
            _make_evidence(
                source_type=EvidenceType.BEHAVIORAL,
                contains_conflict=True,
                star_complete=True,
            )
            for _ in range(10)
        ]
        conf = cal._calculate_confidence(evidence)
        assert conf <= 1.0
