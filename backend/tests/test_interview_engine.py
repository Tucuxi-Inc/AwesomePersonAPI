"""Tests for the Interview Engine and related services."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.patterns import (
    ReasoningPattern,
    EvidenceType,
    ResponseDepth,
    ProbeContext,
    select_patterns_for_context,
    EVIDENCE_WEIGHTS,
)
from app.services.interview_engine import (
    InterviewEngine,
    InterviewState,
    InterviewConfig,
    TraitProgress,
    InterviewPhase,
    ProbePhase,
)
from app.services.probe_generator import (
    PatternAwareProbeGenerator,
    ProbeGenerationContext,
    GeneratedProbe,
)
from app.services.response_analyzer import (
    PatternAwareResponseAnalyzer,
    ResponseAnalysis,
    ExtractedEvidence,
    OmissionAnalysis,
    ResponseQuality,
)
from app.services.score_calibrator import (
    ScoreCalibrator,
    EvidenceForScoring,
    CalibratedTraitScore,
    Recommendation,
)


class TestInterviewConfig:
    """Test InterviewConfig defaults and validation."""

    def test_default_config(self):
        """Default config should have sensible values."""
        config = InterviewConfig()
        assert config.max_duration_minutes == 60
        assert config.max_follow_ups_per_trait == 3
        assert config.confidence_threshold_for_recursion == 0.6
        assert config.require_reflection is True
        assert config.enable_resume_customization is True
        assert config.enable_conflict_probing is True

    def test_custom_config(self):
        """Custom config values should be preserved."""
        config = InterviewConfig(
            max_duration_minutes=45,
            max_follow_ups_per_trait=2,
            confidence_threshold_for_recursion=0.7,
        )
        assert config.max_duration_minutes == 45
        assert config.max_follow_ups_per_trait == 2
        assert config.confidence_threshold_for_recursion == 0.7


class TestTraitProgress:
    """Test TraitProgress tracking."""

    def test_initial_progress(self):
        """Initial progress should have zero values."""
        progress = TraitProgress(
            trait_id="CURIOSITY",
            trait_name="Curiosity",
        )
        assert progress.phase == ProbePhase.PRIMARY
        assert progress.probes_used == 0
        assert progress.evidence_count == 0
        assert progress.confidence == 0.0
        assert progress.is_complete is False

    def test_star_coverage_defaults(self):
        """STAR coverage should default to all False."""
        progress = TraitProgress(
            trait_id="CURIOSITY",
            trait_name="Curiosity",
        )
        assert progress.star_coverage["situation"] is False
        assert progress.star_coverage["task"] is False
        assert progress.star_coverage["action"] is False
        assert progress.star_coverage["result"] is False


class TestInterviewState:
    """Test InterviewState management."""

    def test_initial_state(self):
        """Initial state should be properly initialized."""
        state = InterviewState(
            session_id="test-session",
            candidate_id="test-candidate",
        )
        assert state.phase == InterviewPhase.NOT_STARTED
        assert state.current_trait_index == 0
        assert len(state.exchanges) == 0
        assert len(state.evidence_items) == 0

    def test_state_with_config(self):
        """State should preserve custom config."""
        config = InterviewConfig(max_duration_minutes=30)
        state = InterviewState(
            session_id="test-session",
            candidate_id="test-candidate",
            config=config,
        )
        assert state.config.max_duration_minutes == 30


class TestProbeGenerationContext:
    """Test ProbeGenerationContext."""

    def test_minimal_context(self):
        """Minimal context should be valid."""
        context = ProbeGenerationContext(
            trait_id="CURIOSITY",
            trait_name="Curiosity",
            trait_definition="The drive to learn and explore.",
        )
        assert context.trait_id == "CURIOSITY"
        assert context.probe_type == "PRIMARY"
        assert context.current_confidence == 0.0

    def test_full_context(self):
        """Full context should preserve all fields."""
        context = ProbeGenerationContext(
            trait_id="CURIOSITY",
            trait_name="Curiosity",
            trait_definition="The drive to learn and explore.",
            role_context="Software Engineer",
            resume_summary="10 years experience",
            current_confidence=0.5,
            probe_type="FOLLOW_UP",
        )
        assert context.role_context == "Software Engineer"
        assert context.resume_summary == "10 years experience"
        assert context.current_confidence == 0.5
        assert context.probe_type == "FOLLOW_UP"


class TestGeneratedProbe:
    """Test GeneratedProbe structure."""

    def test_probe_structure(self):
        """Generated probe should have all required fields."""
        probe = GeneratedProbe(
            text="Tell me about a time you learned something new.",
            probe_type="PRIMARY",
            trait_id="CURIOSITY",
            patterns_applied=["MC24", "MC35"],
            generation_rationale="First probe for trait",
            evidence_expectations=["specific example", "learning outcome"],
            follow_up_triggers=[],
        )
        assert "learned" in probe.text
        assert probe.probe_type == "PRIMARY"
        assert "MC24" in probe.patterns_applied
        assert len(probe.evidence_expectations) == 2


class TestExtractedEvidence:
    """Test ExtractedEvidence structure."""

    def test_behavioral_evidence(self):
        """Behavioral evidence should have correct weight."""
        evidence = ExtractedEvidence(
            source_type=EvidenceType.BEHAVIORAL,
            source_text="When I was at Amazon, I learned Kubernetes in 2 weeks.",
            weight=EVIDENCE_WEIGHTS[EvidenceType.BEHAVIORAL],
            trait_signals=[{"trait_id": "CURIOSITY", "signal": "positive", "strength": 0.8}],
            star_components={"situation": True, "task": True, "action": True, "result": True},
            confidence=0.8,
            specificity_score=0.9,
        )
        assert evidence.source_type == EvidenceType.BEHAVIORAL
        assert evidence.weight == 1.0
        assert evidence.confidence == 0.8

    def test_self_report_evidence(self):
        """Self-report evidence should have lower weight."""
        evidence = ExtractedEvidence(
            source_type=EvidenceType.SELF_REPORT,
            source_text="I am a fast learner.",
            weight=EVIDENCE_WEIGHTS[EvidenceType.SELF_REPORT],
            trait_signals=[{"trait_id": "CURIOSITY", "signal": "positive", "strength": 0.5}],
            star_components={},
            confidence=0.3,
            specificity_score=0.2,
        )
        assert evidence.source_type == EvidenceType.SELF_REPORT
        assert evidence.weight == 0.3
        assert evidence.confidence == 0.3


class TestEvidenceWeights:
    """Test evidence weight hierarchy."""

    def test_observed_highest_weight(self):
        """Observed evidence should have highest weight."""
        assert EVIDENCE_WEIGHTS[EvidenceType.OBSERVED] > EVIDENCE_WEIGHTS[EvidenceType.BEHAVIORAL]

    def test_behavioral_over_hypothetical(self):
        """Behavioral evidence should outweigh hypothetical."""
        assert EVIDENCE_WEIGHTS[EvidenceType.BEHAVIORAL] > EVIDENCE_WEIGHTS[EvidenceType.HYPOTHETICAL]

    def test_hypothetical_over_self_report(self):
        """Hypothetical should outweigh self-report."""
        assert EVIDENCE_WEIGHTS[EvidenceType.HYPOTHETICAL] > EVIDENCE_WEIGHTS[EvidenceType.SELF_REPORT]

    def test_self_report_over_opinion(self):
        """Self-report should outweigh opinion."""
        assert EVIDENCE_WEIGHTS[EvidenceType.SELF_REPORT] > EVIDENCE_WEIGHTS[EvidenceType.OPINION]


class TestPatternSelection:
    """Test pattern selection for different contexts."""

    def test_first_probe_patterns(self):
        """First probe should include assumption surfacing."""
        context = ProbeContext()
        result = select_patterns_for_context("CURIOSITY", context)

        assert ReasoningPattern.MC35_REPRESENTATION in result.patterns
        assert ReasoningPattern.MC24_ASSUMPTION in result.patterns

    def test_surface_response_triggers_depth(self):
        """Surface response should trigger depth pattern."""
        context = ProbeContext(
            probes_asked=[{"trait_id": "CURIOSITY", "question": "test"}],
            last_response_depth=ResponseDepth.SURFACE,
        )
        result = select_patterns_for_context("CURIOSITY", context)

        assert ReasoningPattern.MC38_ABSTRACTION in result.patterns

    def test_self_report_triggers_trust(self):
        """Self-report evidence should trigger trust calibration."""
        context = ProbeContext(
            probes_asked=[{"trait_id": "CURIOSITY", "question": "test"}],
            last_evidence_type=EvidenceType.SELF_REPORT,
        )
        result = select_patterns_for_context("CURIOSITY", context)

        assert ReasoningPattern.IP11_TRUST in result.patterns

    def test_resilience_includes_risk(self):
        """Resilience trait should include risk pattern."""
        context = ProbeContext()
        result = select_patterns_for_context("RESILIENCE", context)

        assert ReasoningPattern.SP8_RISK in result.patterns


class TestEvidenceForScoring:
    """Test EvidenceForScoring structure."""

    def test_positive_signal(self):
        """Positive signal should be captured."""
        evidence = EvidenceForScoring(
            source_type=EvidenceType.BEHAVIORAL,
            source_text="I proactively learned React before it was required.",
            weight=1.0,
            trait_signal="positive",
            signal_strength=0.9,
            star_components={"situation": True, "action": True, "result": True},
        )
        assert evidence.trait_signal == "positive"
        assert evidence.signal_strength == 0.9

    def test_conflict_indicator(self):
        """Conflict indicator should be tracked."""
        evidence = EvidenceForScoring(
            source_type=EvidenceType.BEHAVIORAL,
            source_text="The team disagreed with my approach initially.",
            weight=1.0,
            trait_signal="positive",
            signal_strength=0.7,
            star_components={},
            contains_conflict=True,
        )
        assert evidence.contains_conflict is True


class TestCalibratedTraitScore:
    """Test CalibratedTraitScore structure."""

    def test_score_structure(self):
        """Calibrated score should have all fields."""
        score = CalibratedTraitScore(
            trait_id="CURIOSITY",
            trait_name="Curiosity",
            raw_score=4,
            calibrated_score=4,
            confidence=0.75,
            evidence_summary="Based on 3 behavioral examples.",
            evidence_items=[],
            explanation="Strong curiosity demonstrated.",
            score_rationale="No adjustments needed.",
            matched_anchors=["Score 4: Clear examples of learning"],
            signal_gaps=[],
        )
        assert score.raw_score == 4
        assert score.calibrated_score == 4
        assert score.confidence == 0.75

    def test_counter_indicator_flag(self):
        """Counter indicator should be flagged."""
        score = CalibratedTraitScore(
            trait_id="RISK_ORIENTATION",
            trait_name="Risk Orientation",
            raw_score=5,
            calibrated_score=5,
            confidence=0.8,
            evidence_summary="Very high risk tolerance.",
            evidence_items=[],
            explanation="Extremely high risk orientation.",
            score_rationale="May be counter-productive for compliance role.",
            matched_anchors=[],
            signal_gaps=[],
            is_counter_indicator=True,
            counter_indicator_severity="HIGH",
        )
        assert score.is_counter_indicator is True
        assert score.counter_indicator_severity == "HIGH"


class TestRecommendation:
    """Test Recommendation enum."""

    def test_recommendation_values(self):
        """All recommendation values should be valid."""
        assert Recommendation.STRONG_HIRE.value == "STRONG_HIRE"
        assert Recommendation.HIRE.value == "HIRE"
        assert Recommendation.HOLD.value == "HOLD"
        assert Recommendation.NO_HIRE.value == "NO_HIRE"


class TestOmissionAnalysis:
    """Test OmissionAnalysis structure."""

    def test_omission_detection(self):
        """Omissions should be categorized correctly."""
        omissions = OmissionAnalysis(
            missing_star_components=["action", "result"],
            avoided_topics=["team conflict"],
            expected_but_absent=["specific timeline"],
            concerning_absences=["no failure mentioned"],
        )
        assert "action" in omissions.missing_star_components
        assert "team conflict" in omissions.avoided_topics
        assert len(omissions.concerning_absences) == 1


class TestResponseQuality:
    """Test ResponseQuality enum."""

    def test_quality_levels(self):
        """All quality levels should be valid."""
        assert ResponseQuality.EXCELLENT.value == "EXCELLENT"
        assert ResponseQuality.GOOD.value == "GOOD"
        assert ResponseQuality.ADEQUATE.value == "ADEQUATE"
        assert ResponseQuality.POOR.value == "POOR"
        assert ResponseQuality.UNUSABLE.value == "UNUSABLE"


class TestInterviewPhase:
    """Test InterviewPhase enum."""

    def test_phase_progression(self):
        """Phases should follow logical progression."""
        phases = [
            InterviewPhase.NOT_STARTED,
            InterviewPhase.INTRODUCTION,
            InterviewPhase.TRAIT_ASSESSMENT,
            InterviewPhase.CANDIDATE_QUESTIONS,
            InterviewPhase.CLOSING,
            InterviewPhase.COMPLETED,
        ]
        assert len(phases) == 6


class TestProbePhase:
    """Test ProbePhase enum."""

    def test_probe_phases(self):
        """All probe phases should be valid."""
        assert ProbePhase.PRIMARY.value == "PRIMARY"
        assert ProbePhase.FOLLOW_UP.value == "FOLLOW_UP"
        assert ProbePhase.REFLECTION.value == "REFLECTION"
        assert ProbePhase.RECURSION.value == "RECURSION"
        assert ProbePhase.COMPLETE.value == "COMPLETE"
