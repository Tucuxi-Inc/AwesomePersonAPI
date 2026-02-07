"""
Extended tests for patterns.py — covering signal_gaps_for_trait edge cases,
last_response_lacked, and conflict pattern selection.
"""

import pytest
from app.services.patterns import (
    ProbeContext,
    ReasoningPattern,
    EvidenceType,
    ResponseDepth,
    select_patterns_for_context,
)


# ── ProbeContext.signal_gaps_for_trait edge cases ──────────────────────────────


class TestSignalGapsSurfaceLevel:
    """Tests for the 'all responses surface-level' gap."""

    def test_all_surface_evidence_adds_gap(self):
        ctx = ProbeContext(
            evidence_collected=[
                {"trait_id": "t1", "type": "BEHAVIORAL", "depth": "SURFACE", "contains_conflict": True},
            ],
            responses=[],
        )
        gaps = ctx.signal_gaps_for_trait("t1")
        assert "All responses are surface-level" in gaps

    def test_mixed_depth_no_surface_gap(self):
        ctx = ProbeContext(
            evidence_collected=[
                {"trait_id": "t1", "type": "BEHAVIORAL", "depth": "SURFACE", "contains_conflict": True},
                {"trait_id": "t1", "type": "BEHAVIORAL", "depth": "DEEP", "contains_conflict": False},
            ],
            responses=[],
        )
        gaps = ctx.signal_gaps_for_trait("t1")
        assert "All responses are surface-level" not in gaps

    def test_empty_evidence_surface_gap(self):
        """all() on empty iterable returns True, so this should add the gap."""
        ctx = ProbeContext(evidence_collected=[], responses=[])
        gaps = ctx.signal_gaps_for_trait("t1")
        assert "All responses are surface-level" in gaps


# ── ProbeContext.last_response_lacked ─────────────────────────────────────────


class TestLastResponseLacked:
    """Tests for last_response_lacked method."""

    def test_empty_responses_returns_false(self):
        ctx = ProbeContext(evidence_collected=[], responses=[])
        assert ctx.last_response_lacked("conflict") is False

    def test_element_present_returns_false(self):
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[{"contains": ["conflict", "tension"]}],
        )
        assert ctx.last_response_lacked("conflict") is False

    def test_element_absent_returns_true(self):
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[{"contains": ["specifics"]}],
        )
        assert ctx.last_response_lacked("conflict") is True

    def test_multiple_elements_all_present(self):
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[{"contains": ["conflict", "failure", "tension"]}],
        )
        assert ctx.last_response_lacked("conflict", "failure", "tension") is False

    def test_multiple_elements_one_missing(self):
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[{"contains": ["conflict"]}],
        )
        assert ctx.last_response_lacked("conflict", "failure") is True

    def test_none_contains_field(self):
        """When 'contains' is None in the last response."""
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[{"contains": None}],
        )
        assert ctx.last_response_lacked("conflict") is True

    def test_missing_contains_key(self):
        """When 'contains' key is missing entirely."""
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[{"some_other_key": "value"}],
        )
        assert ctx.last_response_lacked("conflict") is True

    def test_only_checks_last_response(self):
        """Should only check the last response, not earlier ones."""
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[
                {"contains": ["conflict"]},  # earlier — has conflict
                {"contains": ["specifics"]},  # last — lacks conflict
            ],
        )
        assert ctx.last_response_lacked("conflict") is True


# ── Pattern selection: conflict probing ───────────────────────────────────────


class TestConflictPatternSelection:
    """Tests for IP7_CONFLICT pattern selection via last_response_lacked."""

    def test_conflict_pattern_added_when_lacking(self):
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[{"contains": ["specifics"]}],
            probes_asked=[{"trait_id": "t1"}],
            last_response_depth=ResponseDepth.DEEP,
            last_evidence_type=EvidenceType.BEHAVIORAL,
            current_confidence=0.8,
        )
        result = select_patterns_for_context("t1", ctx)
        assert ReasoningPattern.IP7_CONFLICT in result.patterns
        assert "IP7" in result.rationale

    def test_conflict_pattern_not_added_when_present(self):
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[{"contains": ["conflict", "failure", "tension"]}],
            probes_asked=[{"trait_id": "t1"}],
            last_response_depth=ResponseDepth.DEEP,
            last_evidence_type=EvidenceType.BEHAVIORAL,
            current_confidence=0.8,
        )
        result = select_patterns_for_context("t1", ctx)
        assert ReasoningPattern.IP7_CONFLICT not in result.patterns

    def test_no_responses_no_conflict_pattern(self):
        """Empty responses means last_response_lacked returns False."""
        ctx = ProbeContext(
            evidence_collected=[],
            responses=[],
            probes_asked=[{"trait_id": "t1"}],
            last_response_depth=ResponseDepth.DEEP,
            last_evidence_type=EvidenceType.BEHAVIORAL,
            current_confidence=0.8,
        )
        result = select_patterns_for_context("t1", ctx)
        assert ReasoningPattern.IP7_CONFLICT not in result.patterns
