"""
Extended tests for score_calibrator: signal gaps, evidence summary,
calibration adjustments, format_anchors, composite edge cases, and singleton.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.score_calibrator import (
    ScoreCalibrator,
    EvidenceForScoring,
    CalibratedTraitScore,
    CompositeScore,
    Recommendation,
    get_score_calibrator,
)
from app.services.patterns import EvidenceType, EVIDENCE_WEIGHTS


# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_evidence(
    source_type: EvidenceType = EvidenceType.BEHAVIORAL,
    trait_signal: str = "positive",
    signal_strength: float = 0.8,
    contains_conflict: bool = False,
    contains_failure: bool = False,
    star_complete: bool = False,
    source_text: str = "Sample evidence text for testing purposes",
) -> EvidenceForScoring:
    return EvidenceForScoring(
        source_type=source_type,
        source_text=source_text,
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
    calibrator = ScoreCalibrator.__new__(ScoreCalibrator)
    calibrator.llm_client = MagicMock()
    return calibrator


# ── Signal Gaps Tests ─────────────────────────────────────────────────────────


class TestIdentifySignalGaps:
    """Tests for _identify_signal_gaps."""

    def test_no_behavioral_evidence_gap(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(source_type=EvidenceType.SELF_REPORT)]
        gaps = cal._identify_signal_gaps(evidence)
        assert "No behavioral evidence collected" in gaps

    def test_has_behavioral_evidence_no_gap(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(source_type=EvidenceType.BEHAVIORAL)]
        gaps = cal._identify_signal_gaps(evidence)
        assert "No behavioral evidence collected" not in gaps

    def test_observed_evidence_counts_as_behavioral(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(source_type=EvidenceType.OBSERVED)]
        gaps = cal._identify_signal_gaps(evidence)
        assert "No behavioral evidence collected" not in gaps

    def test_no_conflict_gap(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(contains_conflict=False, contains_failure=False)]
        gaps = cal._identify_signal_gaps(evidence)
        assert "No conflict/failure example provided" in gaps

    def test_conflict_present_no_gap(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(contains_conflict=True)]
        gaps = cal._identify_signal_gaps(evidence)
        assert "No conflict/failure example provided" not in gaps

    def test_failure_present_no_gap(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(contains_failure=True)]
        gaps = cal._identify_signal_gaps(evidence)
        assert "No conflict/failure example provided" not in gaps

    def test_no_star_complete_examples_gap(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(star_complete=False)]
        gaps = cal._identify_signal_gaps(evidence)
        assert "No fully STAR-complete examples" in gaps

    def test_star_complete_example_no_gap(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(star_complete=True)]
        gaps = cal._identify_signal_gaps(evidence)
        assert "No fully STAR-complete examples" not in gaps

    def test_empty_evidence_no_star_gap(self):
        """Empty evidence list shouldn't report STAR gap (no data)."""
        cal = _make_calibrator()
        gaps = cal._identify_signal_gaps([])
        assert "No fully STAR-complete examples" not in gaps

    def test_multiple_gaps_at_once(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(
            source_type=EvidenceType.SELF_REPORT,
            contains_conflict=False,
            star_complete=False,
        )]
        gaps = cal._identify_signal_gaps(evidence)
        assert len(gaps) == 3


# ── Evidence Summary Tests ────────────────────────────────────────────────────


class TestGenerateEvidenceSummary:
    """Tests for _generate_evidence_summary."""

    def test_empty_evidence_returns_no_evidence(self):
        cal = _make_calibrator()
        result = cal._generate_evidence_summary([])
        assert result == "No evidence collected."

    def test_single_evidence_item(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(source_type=EvidenceType.BEHAVIORAL)]
        result = cal._generate_evidence_summary(evidence)
        assert "1 evidence items" in result or "Based on 1 evidence" in result
        assert "behavioral" in result.lower()

    def test_mixed_evidence_types(self):
        cal = _make_calibrator()
        evidence = [
            _make_evidence(source_type=EvidenceType.BEHAVIORAL),
            _make_evidence(source_type=EvidenceType.BEHAVIORAL),
            _make_evidence(source_type=EvidenceType.SELF_REPORT),
        ]
        result = cal._generate_evidence_summary(evidence)
        assert "3 evidence items" in result
        assert "behavioral" in result.lower()
        assert "self_report" in result.lower()


# ── Calibration Adjustments Tests ─────────────────────────────────────────────


class TestApplyCalibrationExtended:
    """Tests for _apply_calibration tension and role valence paths."""

    def test_no_tension_with_multiple_evidence_notes(self):
        cal = _make_calibrator()
        evidence = [
            _make_evidence(contains_conflict=False, contains_failure=False),
            _make_evidence(contains_conflict=False, contains_failure=False),
        ]
        calibrated, notes = cal._apply_calibration(4, evidence, None)
        assert "No conflict/failure examples provided" in notes

    def test_has_tension_no_note(self):
        cal = _make_calibrator()
        evidence = [
            _make_evidence(contains_conflict=True),
            _make_evidence(contains_conflict=False),
        ]
        calibrated, notes = cal._apply_calibration(4, evidence, None)
        assert "No conflict/failure" not in notes

    def test_single_evidence_no_tension_note(self):
        """Only one evidence item — no tension note (needs >= 2)."""
        cal = _make_calibrator()
        evidence = [_make_evidence(contains_conflict=False)]
        calibrated, notes = cal._apply_calibration(4, evidence, None)
        assert "No conflict/failure" not in notes

    def test_role_valence_score_above_optimal(self):
        cal = _make_calibrator()
        evidence = [_make_evidence()]
        valence = {"optimal_range": [2, 4]}
        calibrated, notes = cal._apply_calibration(5, evidence, valence)
        assert "exceeds optimal range" in notes

    def test_role_valence_score_below_optimal(self):
        cal = _make_calibrator()
        evidence = [_make_evidence()]
        valence = {"optimal_range": [3, 5]}
        calibrated, notes = cal._apply_calibration(2, evidence, valence)
        assert "below optimal range" in notes

    def test_role_valence_score_within_range(self):
        cal = _make_calibrator()
        evidence = [_make_evidence()]
        valence = {"optimal_range": [2, 4]}
        calibrated, notes = cal._apply_calibration(3, evidence, valence)
        assert "optimal range" not in notes

    def test_role_valence_missing_optimal_range_uses_default(self):
        """When optimal_range key is missing, defaults to [2, 4]."""
        cal = _make_calibrator()
        evidence = [_make_evidence()]
        valence = {"some_other_key": "value"}  # No optimal_range key, but truthy dict
        calibrated, notes = cal._apply_calibration(5, evidence, valence)
        assert "exceeds optimal range" in notes

    def test_no_adjustments_message(self):
        cal = _make_calibrator()
        evidence = [_make_evidence(contains_conflict=True)]
        calibrated, notes = cal._apply_calibration(3, evidence, None)
        assert notes == "No adjustments applied"


# ── Format Anchors Tests ──────────────────────────────────────────────────────


class TestFormatAnchors:
    """Tests for _format_anchors."""

    def test_empty_anchors(self):
        cal = _make_calibrator()
        result = cal._format_anchors({})
        assert result == ""

    def test_single_anchor_with_indicators(self):
        cal = _make_calibrator()
        anchors = {
            "3": {
                "label": "Proficient",
                "indicators": ["Breaks problems down", "Uses data", "Systematic"],
            }
        }
        result = cal._format_anchors(anchors)
        assert "Score 3:" in result
        assert "Breaks problems down" in result

    def test_multiple_anchors_sorted(self):
        cal = _make_calibrator()
        anchors = {
            "5": {"label": "Exceptional", "indicators": ["Outstanding"]},
            "1": {"label": "Developing", "indicators": ["Needs work"]},
            "3": {"label": "Proficient", "indicators": ["Solid"]},
        }
        result = cal._format_anchors(anchors)
        lines = result.strip().split("\n")
        assert len(lines) == 3
        assert lines[0].startswith("Score 1:")
        assert lines[2].startswith("Score 5:")

    def test_non_dict_values_skipped(self):
        cal = _make_calibrator()
        anchors = {
            "3": {"indicators": ["Good"]},
            "4": "Not a dict",
            "5": {"indicators": ["Great"]},
        }
        result = cal._format_anchors(anchors)
        lines = result.strip().split("\n")
        assert len(lines) == 2

    def test_anchor_with_many_indicators_truncated(self):
        cal = _make_calibrator()
        anchors = {
            "3": {
                "indicators": ["one", "two", "three", "four", "five"],
            }
        }
        result = cal._format_anchors(anchors)
        # Only first 3 indicators should appear
        assert "four" not in result
        assert "one" in result


# ── Composite Score Edge Cases ────────────────────────────────────────────────


class TestCompositeScoreExtended:
    """Extended composite score tests for zero-confidence path."""

    def test_zero_confidence_uses_trait_average(self):
        """When all confidences are 0, weighted_average falls back to trait_average."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(calibrated_score=3, confidence=0.0),
            _make_trait_score(trait_id="t2", calibrated_score=5, confidence=0.0),
        ]
        composite = cal._calculate_composite_score(scores)
        assert composite.trait_average == composite.weighted_average
        assert composite.evidence_quality == "LOW"

    def test_mixed_confidence_weighted_correctly(self):
        """High-confidence scores should influence weighted_average more."""
        cal = _make_calibrator()
        scores = [
            _make_trait_score(calibrated_score=5, confidence=0.9),
            _make_trait_score(trait_id="t2", calibrated_score=1, confidence=0.1),
        ]
        composite = cal._calculate_composite_score(scores)
        # Weighted average: (5*0.9 + 1*0.1) / (0.9 + 0.1) = 4.6
        assert composite.weighted_average == pytest.approx(4.6, abs=0.01)
        assert composite.trait_average == pytest.approx(3.0, abs=0.01)

    def test_high_confidence_quality(self):
        cal = _make_calibrator()
        scores = [_make_trait_score(confidence=0.8)]
        composite = cal._calculate_composite_score(scores)
        assert composite.evidence_quality == "HIGH"

    def test_medium_confidence_quality(self):
        cal = _make_calibrator()
        scores = [_make_trait_score(confidence=0.5)]
        composite = cal._calculate_composite_score(scores)
        assert composite.evidence_quality == "MEDIUM"

    def test_rationale_includes_trait_count(self):
        cal = _make_calibrator()
        scores = [
            _make_trait_score(),
            _make_trait_score(trait_id="t2"),
            _make_trait_score(trait_id="t3"),
        ]
        composite = cal._calculate_composite_score(scores)
        assert "3 traits" in composite.rationale


# ── Singleton Tests ───────────────────────────────────────────────────────────


class TestScoreCalibratorSingleton:
    """Tests for get_score_calibrator singleton."""

    def test_returns_same_instance(self):
        import app.services.score_calibrator as mod
        mod._score_calibrator = None  # Reset
        first = get_score_calibrator()
        second = get_score_calibrator()
        assert first is second
        mod._score_calibrator = None  # Cleanup
