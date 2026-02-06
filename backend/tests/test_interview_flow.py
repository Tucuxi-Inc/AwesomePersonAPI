"""
Tests for interview engine logic: state serialization, decision routing,
progress calculation, and evidence accumulation.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from app.services.interview_engine import (
    InterviewEngine,
    InterviewState,
    TraitProgress,
    InterviewConfig,
    InterviewPhase,
    ProbePhase,
    InterviewResponse,
    JobContext,
)
from app.services.resume_customizer import ResumeElement
from app.services.patterns import EvidenceType, ResponseDepth
from app.api.v1.interviews import _state_to_dict, _dict_to_state


# ---- Helpers ----

@dataclass
class MockExtractedEvidence:
    """Mock for ExtractedEvidence from response_analyzer."""
    source_type: EvidenceType = EvidenceType.BEHAVIORAL
    source_text: str = "Led a team of 5 engineers"
    weight: float = 1.0
    star_components: Dict[str, bool] = field(default_factory=lambda: {
        "situation": True, "task": True, "action": True, "result": False
    })
    confidence: float = 0.7
    contains_conflict: bool = False
    contains_failure: bool = False


@dataclass
class MockAnalysis:
    """Minimal mock for ResponseAnalysis."""
    recommended_follow_up_type: Optional[str] = None
    response_depth: ResponseDepth = ResponseDepth.DEEP
    evidence_items: list = field(default_factory=list)
    star_completeness: Dict[str, bool] = field(default_factory=lambda: {
        "situation": True, "task": True, "action": True, "result": False
    })
    confidence: float = 0.7
    tension_present: bool = False
    summary: str = "Mock analysis"


def _make_complex_state() -> InterviewState:
    """Create a complex state with multiple traits for serialization tests."""
    config = InterviewConfig(
        max_duration_minutes=45,
        max_follow_ups_per_trait=2,
        confidence_threshold_for_recursion=0.5,
        require_reflection=True,
        enable_resume_customization=True,
        enable_conflict_probing=True,
    )
    state = InterviewState(
        session_id="session-123",
        candidate_id="candidate-456",
        phase=InterviewPhase.TRAIT_ASSESSMENT,
        current_trait_index=1,
        config=config,
        start_time=datetime(2025, 6, 15, 10, 30, 0),
        exchanges=[
            {"role": "interviewer", "content": "Tell me about a time..."},
            {"role": "candidate", "content": "When I was at Company X..."},
        ],
        evidence_items=[
            {"trait_id": "t1", "source_type": "BEHAVIORAL", "source_text": "Led a team"},
        ],
        resume_elements=[
            ResumeElement(element_type="job_transition", description="Moved from IC to manager"),
            ResumeElement(element_type="project", description="Built ML pipeline"),
        ],
        job_context=JobContext(
            job_id="job-789",
            title="Engineering Manager",
            responsibilities=["Lead team", "Set roadmap", "Mentor"],
            objective_requirements=[{"requirement": "5+ years exp", "required": True}],
            nice_to_haves=[{"description": "ML experience"}],
        ),
        parsed_resume_data={"years_experience": 8, "skills": ["Python", "ML"]},
    )
    state.trait_progress = {
        "t1": TraitProgress(
            trait_id="t1",
            trait_name="Leadership",
            phase=ProbePhase.COMPLETE,
            probes_used=3,
            evidence_count=4,
            behavioral_evidence_count=2,
            confidence=0.85,
            star_coverage={"situation": True, "task": True, "action": True,
                           "result": True, "reflection": True},
            has_conflict_example=True,
            raw_score=4,
            is_complete=True,
        ),
        "t2": TraitProgress(
            trait_id="t2",
            trait_name="Adaptability",
            phase=ProbePhase.FOLLOW_UP,
            probes_used=1,
            evidence_count=1,
            behavioral_evidence_count=1,
            confidence=0.4,
            star_coverage={"situation": True, "task": False, "action": False,
                           "result": False, "reflection": False},
            has_conflict_example=False,
            raw_score=None,
            is_complete=False,
        ),
    }
    return state


def _make_simple_engine() -> InterviewEngine:
    """Create an InterviewEngine with mocked dependencies."""
    engine = InterviewEngine.__new__(InterviewEngine)
    engine.probe_generator = MagicMock()
    engine.response_analyzer = MagicMock()
    engine.resume_customizer = MagicMock()
    engine.compliance_guard = MagicMock()
    return engine


# ---- Test Classes ----

class TestStateSerializationRoundTrip:
    """_state_to_dict and _dict_to_state preserve all fields."""

    def test_complex_state_round_trips(self):
        """Complex state with multiple traits, job context, resume serializes correctly."""
        original = _make_complex_state()
        serialized = _state_to_dict(original)
        restored = _dict_to_state(serialized)

        assert restored.session_id == original.session_id
        assert restored.candidate_id == original.candidate_id
        assert restored.phase == original.phase
        assert restored.current_trait_index == original.current_trait_index

        # Config
        assert restored.config.max_duration_minutes == 45
        assert restored.config.require_reflection is True
        assert restored.config.enable_conflict_probing is True

        # Trait progress
        assert len(restored.trait_progress) == 2
        t1 = restored.trait_progress["t1"]
        assert t1.trait_name == "Leadership"
        assert t1.phase == ProbePhase.COMPLETE
        assert t1.is_complete is True
        assert t1.confidence == 0.85
        assert t1.star_coverage["reflection"] is True

        t2 = restored.trait_progress["t2"]
        assert t2.phase == ProbePhase.FOLLOW_UP
        assert t2.is_complete is False

        # Exchanges and evidence
        assert len(restored.exchanges) == 2
        assert len(restored.evidence_items) == 1

        # Resume elements
        assert len(restored.resume_elements) == 2
        assert restored.resume_elements[0].element_type == "job_transition"

        # Job context
        assert restored.job_context is not None
        assert restored.job_context.title == "Engineering Manager"
        assert len(restored.job_context.responsibilities) == 3

        # Parsed resume data
        assert restored.parsed_resume_data["years_experience"] == 8

    def test_state_with_no_job_context(self):
        """State with job_context=None round-trips correctly."""
        state = InterviewState(
            session_id="s1",
            candidate_id="c1",
            job_context=None,
        )
        serialized = _state_to_dict(state)
        assert serialized["job_context"] is None
        restored = _dict_to_state(serialized)
        assert restored.job_context is None

    def test_datetime_serialization(self):
        """start_time datetime survives round-trip."""
        state = InterviewState(
            session_id="s1",
            candidate_id="c1",
            start_time=datetime(2025, 6, 15, 10, 30, 0),
        )
        serialized = _state_to_dict(state)
        assert serialized["start_time"] == "2025-06-15T10:30:00"
        restored = _dict_to_state(serialized)
        assert restored.start_time == datetime(2025, 6, 15, 10, 30, 0)

    def test_none_start_time(self):
        """None start_time round-trips as None."""
        state = InterviewState(session_id="s1", candidate_id="c1", start_time=None)
        serialized = _state_to_dict(state)
        assert serialized["start_time"] is None
        restored = _dict_to_state(serialized)
        assert restored.start_time is None

    def test_all_probe_phases_round_trip(self):
        """TraitProgress with each ProbePhase value round-trips correctly."""
        for phase in ProbePhase:
            state = InterviewState(session_id="s", candidate_id="c")
            state.trait_progress["t"] = TraitProgress(
                trait_id="t", trait_name="Test", phase=phase,
            )
            serialized = _state_to_dict(state)
            restored = _dict_to_state(serialized)
            assert restored.trait_progress["t"].phase == phase


class TestDetermineNextAction:
    """Decision routing in _determine_next_action."""

    @pytest.mark.asyncio
    async def test_follow_up_when_recommended(self):
        """Analysis recommending follow-up triggers follow-up generation."""
        engine = _make_simple_engine()
        state = InterviewState(
            session_id="s", candidate_id="c",
            phase=InterviewPhase.TRAIT_ASSESSMENT,
            config=InterviewConfig(max_follow_ups_per_trait=3, enable_conflict_probing=False),
        )
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership",
            probes_used=1, has_conflict_example=True,
        )
        analysis = MockAnalysis(recommended_follow_up_type="FOLLOW_UP_ACTION")

        with patch.object(engine, "_generate_follow_up", new_callable=AsyncMock) as mock_fu:
            mock_fu.return_value = (state, InterviewResponse(
                next_prompt="Tell me more about the action...",
                prompt_type="FOLLOW_UP",
            ))
            await engine._determine_next_action(state, {"t1": {}}, analysis)

        mock_fu.assert_called_once_with(state, {"t1": {}}, "FOLLOW_UP_ACTION")

    @pytest.mark.asyncio
    async def test_depth_probe_on_surface_response(self):
        """Surface-level response triggers depth probe."""
        engine = _make_simple_engine()
        state = InterviewState(
            session_id="s", candidate_id="c",
            phase=InterviewPhase.TRAIT_ASSESSMENT,
            config=InterviewConfig(max_follow_ups_per_trait=3, enable_conflict_probing=False),
        )
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership",
            probes_used=1, has_conflict_example=True,
        )
        analysis = MockAnalysis(response_depth=ResponseDepth.SURFACE)

        with patch.object(engine, "_generate_depth_probe", new_callable=AsyncMock) as mock_dp:
            mock_dp.return_value = (state, InterviewResponse(
                next_prompt="Can you be more specific?",
                prompt_type="FOLLOW_UP",
            ))
            await engine._determine_next_action(state, {"t1": {}}, analysis)

        mock_dp.assert_called_once()

    @pytest.mark.asyncio
    async def test_low_confidence_triggers_recursion(self):
        """Low confidence triggers recursion probe (second example)."""
        engine = _make_simple_engine()
        state = InterviewState(
            session_id="s", candidate_id="c",
            phase=InterviewPhase.TRAIT_ASSESSMENT,
            config=InterviewConfig(
                max_follow_ups_per_trait=3,
                confidence_threshold_for_recursion=0.6,
                require_reflection=False,
                enable_conflict_probing=False,
            ),
        )
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership",
            phase=ProbePhase.PRIMARY,
            probes_used=1,
            confidence=0.3,  # Below threshold
            has_conflict_example=True,
        )
        analysis = MockAnalysis(response_depth=ResponseDepth.DEEP)

        with patch.object(engine, "_generate_recursion_probe", new_callable=AsyncMock) as mock_rec:
            mock_rec.return_value = (state, InterviewResponse(
                next_prompt="Can you share another example?",
                prompt_type="RECURSION",
            ))
            await engine._determine_next_action(state, {"t1": {}}, analysis)

        mock_rec.assert_called_once()
        assert state.trait_progress["t1"].phase == ProbePhase.RECURSION

    @pytest.mark.asyncio
    async def test_trait_complete_when_all_checks_pass(self):
        """When all checks pass (high confidence, reflection done, etc.), trait is complete."""
        engine = _make_simple_engine()
        state = InterviewState(
            session_id="s", candidate_id="c",
            phase=InterviewPhase.TRAIT_ASSESSMENT,
            config=InterviewConfig(
                require_reflection=False,
                enable_conflict_probing=False,
                confidence_threshold_for_recursion=0.6,
            ),
        )
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership",
            phase=ProbePhase.PRIMARY,
            probes_used=2,
            confidence=0.8,
            has_conflict_example=True,
        )
        analysis = MockAnalysis(response_depth=ResponseDepth.DEEP)

        with patch.object(engine, "_move_to_next_trait", new_callable=AsyncMock) as mock_move:
            mock_move.return_value = (state, InterviewResponse(
                next_prompt="Next...", prompt_type="PROBE",
            ))
            await engine._determine_next_action(state, {"t1": {}}, analysis)

        progress = state.trait_progress["t1"]
        assert progress.is_complete is True
        assert progress.phase == ProbePhase.COMPLETE
        mock_move.assert_called_once()

    @pytest.mark.asyncio
    async def test_recursion_only_happens_once(self):
        """If already in RECURSION phase, don't recurse again — complete the trait."""
        engine = _make_simple_engine()
        state = InterviewState(
            session_id="s", candidate_id="c",
            phase=InterviewPhase.TRAIT_ASSESSMENT,
            config=InterviewConfig(
                require_reflection=False,
                enable_conflict_probing=False,
                confidence_threshold_for_recursion=0.6,
            ),
        )
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership",
            phase=ProbePhase.RECURSION,  # Already recursed
            probes_used=2,
            confidence=0.3,  # Still low
            has_conflict_example=True,
        )
        analysis = MockAnalysis(response_depth=ResponseDepth.DEEP)

        with patch.object(engine, "_move_to_next_trait", new_callable=AsyncMock) as mock_move:
            mock_move.return_value = (state, InterviewResponse(
                next_prompt="Next...", prompt_type="PROBE",
            ))
            await engine._determine_next_action(state, {"t1": {}}, analysis)

        # Should complete, not recurse again
        assert state.trait_progress["t1"].is_complete is True


class TestProgressCalculation:
    """_calculate_overall_progress tests."""

    def test_zero_of_three_traits(self):
        """0 of 3 traits complete → 0.0."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        state.trait_progress = {
            "t1": TraitProgress(trait_id="t1", trait_name="A", is_complete=False),
            "t2": TraitProgress(trait_id="t2", trait_name="B", is_complete=False),
            "t3": TraitProgress(trait_id="t3", trait_name="C", is_complete=False),
        }
        assert engine._calculate_overall_progress(state) == 0.0

    def test_one_of_three_traits(self):
        """1 of 3 traits complete → ~0.333."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        state.trait_progress = {
            "t1": TraitProgress(trait_id="t1", trait_name="A", is_complete=True),
            "t2": TraitProgress(trait_id="t2", trait_name="B", is_complete=False),
            "t3": TraitProgress(trait_id="t3", trait_name="C", is_complete=False),
        }
        assert abs(engine._calculate_overall_progress(state) - 1/3) < 0.01

    def test_three_of_three_traits(self):
        """3 of 3 complete → 1.0."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        state.trait_progress = {
            "t1": TraitProgress(trait_id="t1", trait_name="A", is_complete=True),
            "t2": TraitProgress(trait_id="t2", trait_name="B", is_complete=True),
            "t3": TraitProgress(trait_id="t3", trait_name="C", is_complete=True),
        }
        assert engine._calculate_overall_progress(state) == 1.0

    def test_empty_trait_progress(self):
        """No traits → 0.0."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        assert engine._calculate_overall_progress(state) == 0.0


class TestUpdateProgressFromAnalysis:
    """Evidence accumulation via _update_progress_from_analysis."""

    def test_star_components_marked_true_when_present(self):
        """STAR components set to True only when analysis says True."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership",
            star_coverage={"situation": False, "task": False, "action": False,
                           "result": False, "reflection": False},
        )
        analysis = MockAnalysis(
            star_completeness={"situation": True, "task": True, "action": False, "result": False},
            evidence_items=[MockExtractedEvidence()],
        )
        engine._update_progress_from_analysis(state, "t1", analysis)

        coverage = state.trait_progress["t1"].star_coverage
        assert coverage["situation"] is True
        assert coverage["task"] is True
        assert coverage["action"] is False
        assert coverage["result"] is False

    def test_star_components_never_reset_to_false(self):
        """Previously True STAR components stay True even if later analysis says False."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership",
            star_coverage={"situation": True, "task": True, "action": False,
                           "result": False, "reflection": False},
        )
        # This analysis has situation=False — but existing True shouldn't be overwritten
        analysis = MockAnalysis(
            star_completeness={"situation": False, "task": False, "action": True, "result": False},
            evidence_items=[],
        )
        engine._update_progress_from_analysis(state, "t1", analysis)

        coverage = state.trait_progress["t1"].star_coverage
        assert coverage["situation"] is True   # Preserved from before
        assert coverage["task"] is True         # Preserved from before
        assert coverage["action"] is True       # Newly set
        assert coverage["result"] is False

    def test_confidence_only_increases(self):
        """Confidence uses max() — never decreases."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership", confidence=0.7,
        )
        analysis = MockAnalysis(confidence=0.5, evidence_items=[])
        engine._update_progress_from_analysis(state, "t1", analysis)
        assert state.trait_progress["t1"].confidence == 0.7  # Didn't decrease

        analysis2 = MockAnalysis(confidence=0.9, evidence_items=[])
        engine._update_progress_from_analysis(state, "t1", analysis2)
        assert state.trait_progress["t1"].confidence == 0.9  # Increased

    def test_evidence_count_increments(self):
        """Evidence count increments by number of evidence items in analysis."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership", evidence_count=0,
        )
        analysis = MockAnalysis(
            evidence_items=[MockExtractedEvidence(), MockExtractedEvidence()],
        )
        engine._update_progress_from_analysis(state, "t1", analysis)
        assert state.trait_progress["t1"].evidence_count == 2

    def test_behavioral_evidence_counted_correctly(self):
        """Behavioral and observed evidence increment behavioral_evidence_count."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership",
            behavioral_evidence_count=0,
        )
        analysis = MockAnalysis(
            evidence_items=[
                MockExtractedEvidence(source_type=EvidenceType.BEHAVIORAL),
                MockExtractedEvidence(source_type=EvidenceType.OBSERVED),
                MockExtractedEvidence(source_type=EvidenceType.SELF_REPORT),
            ],
        )
        engine._update_progress_from_analysis(state, "t1", analysis)
        # BEHAVIORAL + OBSERVED = 2, SELF_REPORT doesn't count
        assert state.trait_progress["t1"].behavioral_evidence_count == 2

    def test_tension_sets_conflict_flag(self):
        """tension_present=True sets has_conflict_example on the trait."""
        engine = _make_simple_engine()
        state = InterviewState(session_id="s", candidate_id="c")
        state.trait_progress["t1"] = TraitProgress(
            trait_id="t1", trait_name="Leadership",
            has_conflict_example=False,
        )
        analysis = MockAnalysis(tension_present=True, evidence_items=[])
        engine._update_progress_from_analysis(state, "t1", analysis)
        assert state.trait_progress["t1"].has_conflict_example is True
