"""Tests for reasoning patterns functionality."""

import pytest
from app.services.patterns import (
    ReasoningPattern,
    EvidenceType,
    ResponseDepth,
    ProbeContext,
    PatternSelectionResult,
    select_patterns_for_context,
    EVIDENCE_WEIGHTS,
    PATTERN_DESCRIPTIONS,
)


class TestReasoningPatterns:
    """Test reasoning pattern enums and constants."""

    def test_all_patterns_have_descriptions(self):
        """All reasoning patterns should have descriptions."""
        for pattern in ReasoningPattern:
            assert pattern in PATTERN_DESCRIPTIONS
            assert "name" in PATTERN_DESCRIPTIONS[pattern]
            assert "purpose" in PATTERN_DESCRIPTIONS[pattern]
            assert "application" in PATTERN_DESCRIPTIONS[pattern]

    def test_evidence_weights_ordered(self):
        """Evidence weights should be properly ordered."""
        assert EVIDENCE_WEIGHTS[EvidenceType.OBSERVED] > EVIDENCE_WEIGHTS[EvidenceType.BEHAVIORAL]
        assert EVIDENCE_WEIGHTS[EvidenceType.BEHAVIORAL] > EVIDENCE_WEIGHTS[EvidenceType.HYPOTHETICAL]
        assert EVIDENCE_WEIGHTS[EvidenceType.HYPOTHETICAL] > EVIDENCE_WEIGHTS[EvidenceType.SELF_REPORT]
        assert EVIDENCE_WEIGHTS[EvidenceType.SELF_REPORT] > EVIDENCE_WEIGHTS[EvidenceType.OPINION]


class TestProbeContext:
    """Test ProbeContext functionality."""

    def test_empty_context(self):
        """Empty context should have sensible defaults."""
        context = ProbeContext()
        assert context.probes_asked == []
        assert context.responses == []
        assert context.evidence_collected == []
        assert context.current_confidence == 0.0

    def test_has_prior_probes_for_trait_false(self):
        """Should return False when no probes asked for trait."""
        context = ProbeContext()
        assert context.has_prior_probes_for_trait("CURIOSITY") is False

    def test_has_prior_probes_for_trait_true(self):
        """Should return True when probes have been asked for trait."""
        context = ProbeContext(
            probes_asked=[{"trait_id": "CURIOSITY", "question": "test"}]
        )
        assert context.has_prior_probes_for_trait("CURIOSITY") is True

    def test_evidence_for_trait_empty(self):
        """Should return empty list when no evidence for trait."""
        context = ProbeContext()
        assert context.evidence_for_trait("CURIOSITY") == []

    def test_evidence_for_trait_with_evidence(self):
        """Should return evidence items for trait."""
        context = ProbeContext(
            evidence_collected=[
                {"trait_id": "CURIOSITY", "type": "BEHAVIORAL", "text": "example1"},
                {"trait_id": "ADAPTABILITY", "type": "SELF_REPORT", "text": "example2"},
                {"trait_id": "CURIOSITY", "type": "BEHAVIORAL", "text": "example3"},
            ]
        )
        curiosity_evidence = context.evidence_for_trait("CURIOSITY")
        assert len(curiosity_evidence) == 2

    def test_confidence_for_trait_empty(self):
        """Should return 0 confidence with no evidence."""
        context = ProbeContext()
        assert context.confidence_for_trait("CURIOSITY") == 0.0

    def test_confidence_for_trait_with_behavioral(self):
        """Should have higher confidence with behavioral evidence."""
        context = ProbeContext(
            evidence_collected=[
                {"trait_id": "CURIOSITY", "type": "BEHAVIORAL", "text": "example1"},
                {"trait_id": "CURIOSITY", "type": "BEHAVIORAL", "text": "example2"},
            ]
        )
        confidence = context.confidence_for_trait("CURIOSITY")
        assert confidence > 0.5

    def test_signal_gaps_no_behavioral(self):
        """Should identify missing behavioral evidence."""
        context = ProbeContext(
            evidence_collected=[
                {"trait_id": "CURIOSITY", "type": "SELF_REPORT", "text": "example1"},
            ]
        )
        gaps = context.signal_gaps_for_trait("CURIOSITY")
        assert "No behavioral evidence" in gaps

    def test_signal_gaps_no_conflict(self):
        """Should identify missing conflict examples."""
        context = ProbeContext(
            evidence_collected=[
                {"trait_id": "CURIOSITY", "type": "BEHAVIORAL", "text": "example1", "contains_conflict": False},
            ]
        )
        gaps = context.signal_gaps_for_trait("CURIOSITY")
        assert "No conflict/failure example" in gaps


class TestPatternSelection:
    """Test pattern selection logic."""

    def test_first_probe_includes_mc35_and_mc24(self):
        """First probe should include representation and assumption patterns."""
        context = ProbeContext()
        result = select_patterns_for_context("CURIOSITY", context)

        assert ReasoningPattern.MC35_REPRESENTATION in result.patterns
        assert ReasoningPattern.MC24_ASSUMPTION in result.patterns

    def test_surface_response_triggers_depth(self):
        """Surface-level response should trigger depth pattern."""
        context = ProbeContext(
            last_response_depth=ResponseDepth.SURFACE,
            probes_asked=[{"trait_id": "CURIOSITY", "question": "test"}],
        )
        result = select_patterns_for_context("CURIOSITY", context)

        assert ReasoningPattern.MC38_ABSTRACTION in result.patterns

    def test_self_report_triggers_trust(self):
        """Self-report evidence should trigger trust calibration."""
        context = ProbeContext(
            last_evidence_type=EvidenceType.SELF_REPORT,
            probes_asked=[{"trait_id": "CURIOSITY", "question": "test"}],
        )
        result = select_patterns_for_context("CURIOSITY", context)

        assert ReasoningPattern.IP11_TRUST in result.patterns

    def test_low_confidence_triggers_alternatives(self):
        """Low confidence should trigger solution space exploration."""
        context = ProbeContext(
            current_confidence=0.3,
            probes_asked=[{"trait_id": "CURIOSITY", "question": "test"}],
        )
        result = select_patterns_for_context("CURIOSITY", context)

        assert ReasoningPattern.MC44_SOLUTION_SPACE in result.patterns

    def test_resilience_includes_risk_pattern(self):
        """Resilience trait should include risk identification pattern."""
        context = ProbeContext()
        result = select_patterns_for_context("RESILIENCE", context)

        assert ReasoningPattern.SP8_RISK in result.patterns

    def test_result_includes_rationale(self):
        """Pattern selection result should include rationale."""
        context = ProbeContext()
        result = select_patterns_for_context("CURIOSITY", context)

        assert result.rationale is not None
        assert len(result.rationale) > 0
