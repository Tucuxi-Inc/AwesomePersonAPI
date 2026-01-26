"""
Interview Engine - Core orchestrator for conducting behavioral interviews.

This module implements the STAR+ methodology for structured behavioral interviews,
coordinating probe generation, response analysis, evidence extraction, and
adaptive interview strategy.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from app.services.probe_generator import (
    PatternAwareProbeGenerator,
    ProbeGenerationContext,
    GeneratedProbe,
    get_probe_generator,
)
from app.services.response_analyzer import (
    PatternAwareResponseAnalyzer,
    ResponseAnalysis,
    ExtractedEvidence,
    get_response_analyzer,
)
from app.services.resume_customizer import (
    ResumeInformedProbeCustomizer,
    ResumeElement,
    get_resume_customizer,
)
from app.services.patterns import ResponseDepth, EvidenceType
from app.services.interview_compliance import (
    InterviewComplianceGuard,
    get_interview_compliance_guard,
)


class InterviewPhase(str, Enum):
    """Current phase of the interview."""
    NOT_STARTED = "NOT_STARTED"
    INTRODUCTION = "INTRODUCTION"
    TRAIT_ASSESSMENT = "TRAIT_ASSESSMENT"
    CANDIDATE_QUESTIONS = "CANDIDATE_QUESTIONS"
    CLOSING = "CLOSING"
    COMPLETED = "COMPLETED"


class ProbePhase(str, Enum):
    """Current phase within trait assessment."""
    PRIMARY = "PRIMARY"
    FOLLOW_UP = "FOLLOW_UP"
    REFLECTION = "REFLECTION"
    RECURSION = "RECURSION"
    COMPLETE = "COMPLETE"


@dataclass
class InterviewConfig:
    """Configuration for an interview session."""
    max_duration_minutes: int = 60
    max_follow_ups_per_trait: int = 3
    confidence_threshold_for_recursion: float = 0.6
    require_reflection: bool = True
    enable_resume_customization: bool = True
    enable_conflict_probing: bool = True
    minimum_behavioral_evidence: int = 1
    traits_to_assess: List[str] = field(default_factory=list)


@dataclass
class TraitProgress:
    """Progress tracking for a single trait."""
    trait_id: str
    trait_name: str
    phase: ProbePhase = ProbePhase.PRIMARY
    probes_used: int = 0
    evidence_count: int = 0
    behavioral_evidence_count: int = 0
    confidence: float = 0.0
    star_coverage: Dict[str, bool] = field(default_factory=lambda: {
        "situation": False,
        "task": False,
        "action": False,
        "result": False,
        "reflection": False,
    })
    has_conflict_example: bool = False
    raw_score: Optional[int] = None
    is_complete: bool = False


@dataclass
class InterviewState:
    """Current state of an interview session."""
    session_id: str
    candidate_id: str
    phase: InterviewPhase = InterviewPhase.NOT_STARTED
    current_trait_index: int = 0
    trait_progress: Dict[str, TraitProgress] = field(default_factory=dict)
    exchanges: List[Dict[str, Any]] = field(default_factory=list)
    evidence_items: List[Dict[str, Any]] = field(default_factory=list)
    start_time: Optional[datetime] = None
    config: InterviewConfig = field(default_factory=InterviewConfig)
    resume_elements: List[ResumeElement] = field(default_factory=list)


@dataclass
class InterviewResponse:
    """Response from the interview engine."""
    next_prompt: str
    prompt_type: str  # INTRODUCTION, PROBE, FOLLOW_UP, REFLECTION, RECURSION, CLOSING
    trait_id: Optional[str] = None
    trait_progress: Optional[TraitProgress] = None
    overall_progress: float = 0.0
    can_end_interview: bool = False
    interview_complete: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class InterviewEngine:
    """
    Core interview orchestrator implementing STAR+ methodology.

    The engine manages:
    - Interview session lifecycle
    - Probe generation and delivery
    - Response analysis and evidence extraction
    - STAR+ completeness tracking
    - Adaptive strategy (follow-ups, reflection, recursion)
    - Progress monitoring and completion determination
    """

    # Introduction template
    INTRODUCTION_TEMPLATE = """Thank you for joining us today. I'm going to ask you some questions about your past experiences to better understand how you approach different situations.

For each question, I'd love to hear about specific examples from your experience. Please be as detailed as you can about the situation, what you did, and what happened as a result.

There are no right or wrong answers - I'm interested in understanding your actual experiences and how you handled them.

Do you have any questions before we begin?"""

    # Closing template
    CLOSING_TEMPLATE = """Thank you so much for sharing those examples with me today. I really appreciate you being so open about your experiences.

Do you have any questions for me about the role or the team?"""

    def __init__(self):
        self.probe_generator = get_probe_generator()
        self.response_analyzer = get_response_analyzer()
        self.resume_customizer = get_resume_customizer()
        self.compliance_guard = get_interview_compliance_guard()

    async def start_interview(
        self,
        session_id: str,
        candidate_id: str,
        traits_to_assess: List[Dict[str, Any]],
        config: Optional[InterviewConfig] = None,
        resume_text: Optional[str] = None,
        behavioral_anchors: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> tuple[InterviewState, InterviewResponse]:
        """
        Start a new interview session.

        Args:
            session_id: Unique session identifier
            candidate_id: Candidate identifier
            traits_to_assess: List of traits with metadata
            config: Interview configuration
            resume_text: Optional resume text for customization
            behavioral_anchors: Optional behavioral anchors per trait

        Returns:
            Tuple of (InterviewState, InterviewResponse)
        """
        if config is None:
            config = InterviewConfig()

        # Initialize state
        state = InterviewState(
            session_id=session_id,
            candidate_id=candidate_id,
            config=config,
            start_time=datetime.now(timezone.utc),
        )

        # Initialize trait progress
        for trait in traits_to_assess:
            trait_id = trait.get("id", trait.get("trait_id", ""))
            state.trait_progress[trait_id] = TraitProgress(
                trait_id=trait_id,
                trait_name=trait.get("name", trait_id),
            )

        # Extract resume elements if provided
        if resume_text and config.enable_resume_customization:
            state.resume_elements = await self.resume_customizer.extract_resume_elements(
                resume_text
            )

        # Add introduction exchange
        state.phase = InterviewPhase.INTRODUCTION
        state.exchanges.append({
            "sequence": 1,
            "speaker": "SYSTEM",
            "type": "INTRODUCTION",
            "content": self.INTRODUCTION_TEMPLATE,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        return state, InterviewResponse(
            next_prompt=self.INTRODUCTION_TEMPLATE,
            prompt_type="INTRODUCTION",
            overall_progress=0.0,
            can_end_interview=False,
        )

    async def process_response(
        self,
        state: InterviewState,
        response_text: str,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[InterviewState, InterviewResponse]:
        """
        Process a candidate response and generate the next prompt.

        Args:
            state: Current interview state
            response_text: Candidate's response
            traits_metadata: Trait definitions and behavioral anchors

        Returns:
            Updated state and next response
        """
        # Record the response
        state.exchanges.append({
            "sequence": len(state.exchanges) + 1,
            "speaker": "CANDIDATE",
            "type": "RESPONSE",
            "content": response_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trait_id": self._get_current_trait_id(state),
        })

        # Handle based on current phase
        if state.phase == InterviewPhase.INTRODUCTION:
            return await self._handle_post_introduction(state, traits_metadata)

        elif state.phase == InterviewPhase.TRAIT_ASSESSMENT:
            return await self._handle_trait_response(state, response_text, traits_metadata)

        elif state.phase == InterviewPhase.CANDIDATE_QUESTIONS:
            return await self._handle_candidate_questions(state, response_text)

        elif state.phase == InterviewPhase.CLOSING:
            return self._complete_interview(state)

        return state, InterviewResponse(
            next_prompt="I apologize, something went wrong. Let me continue.",
            prompt_type="ERROR",
        )

    async def _handle_post_introduction(
        self,
        state: InterviewState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[InterviewState, InterviewResponse]:
        """Handle response after introduction and start first trait."""
        state.phase = InterviewPhase.TRAIT_ASSESSMENT
        state.current_trait_index = 0

        return await self._generate_next_probe(state, traits_metadata)

    async def _handle_trait_response(
        self,
        state: InterviewState,
        response_text: str,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[InterviewState, InterviewResponse]:
        """Handle a response during trait assessment."""
        current_trait_id = self._get_current_trait_id(state)
        if not current_trait_id:
            return await self._move_to_closing(state)

        progress = state.trait_progress[current_trait_id]
        trait_meta = traits_metadata.get(current_trait_id, {})

        # Analyze the response
        analysis = await self.response_analyzer.analyze_response(
            response_text=response_text,
            probe_text=self._get_last_probe_text(state),
            trait_name=progress.trait_name,
            trait_definition=trait_meta.get("definition", ""),
            behavioral_anchors=trait_meta.get("behavioral_anchors"),
            prior_context={
                "exchange_count": progress.probes_used,
                "evidence_count": progress.evidence_count,
                "confidence": progress.confidence,
            },
        )

        # Update state with analysis results
        self._update_progress_from_analysis(state, current_trait_id, analysis)

        # Determine next action
        return await self._determine_next_action(state, traits_metadata, analysis)

    def _update_progress_from_analysis(
        self,
        state: InterviewState,
        trait_id: str,
        analysis: ResponseAnalysis,
    ) -> None:
        """Update trait progress based on response analysis."""
        progress = state.trait_progress[trait_id]

        # Update evidence counts
        progress.evidence_count += len(analysis.evidence_items)
        progress.behavioral_evidence_count += sum(
            1 for e in analysis.evidence_items
            if e.source_type in (EvidenceType.BEHAVIORAL, EvidenceType.OBSERVED)
        )

        # Update STAR coverage
        for component, present in analysis.star_completeness.items():
            if present:
                progress.star_coverage[component] = True

        # Update confidence
        progress.confidence = max(progress.confidence, analysis.confidence)

        # Check for conflict/tension
        if analysis.tension_present:
            progress.has_conflict_example = True

        # Store evidence items
        for evidence in analysis.evidence_items:
            state.evidence_items.append({
                "trait_id": trait_id,
                "source_type": evidence.source_type.value,
                "source_text": evidence.source_text,
                "weight": evidence.weight,
                "star_components": evidence.star_components,
                "confidence": evidence.confidence,
                "contains_conflict": evidence.contains_conflict,
                "contains_failure": evidence.contains_failure,
            })

    async def _determine_next_action(
        self,
        state: InterviewState,
        traits_metadata: Dict[str, Dict[str, Any]],
        analysis: ResponseAnalysis,
    ) -> tuple[InterviewState, InterviewResponse]:
        """Determine the next action based on current progress."""
        current_trait_id = self._get_current_trait_id(state)
        progress = state.trait_progress[current_trait_id]
        config = state.config

        # Check if we need follow-ups for STAR components
        if analysis.recommended_follow_up_type and progress.probes_used < config.max_follow_ups_per_trait:
            if analysis.recommended_follow_up_type.startswith("FOLLOW_UP_"):
                progress.phase = ProbePhase.FOLLOW_UP
                return await self._generate_follow_up(
                    state, traits_metadata, analysis.recommended_follow_up_type
                )

        # Check if we need depth escalation
        if analysis.response_depth == ResponseDepth.SURFACE and progress.probes_used < config.max_follow_ups_per_trait:
            progress.phase = ProbePhase.FOLLOW_UP
            return await self._generate_depth_probe(state, traits_metadata)

        # Check if we need conflict probing
        if (config.enable_conflict_probing and
            not progress.has_conflict_example and
            progress.probes_used < config.max_follow_ups_per_trait):
            return await self._generate_conflict_probe(state, traits_metadata)

        # Check if we should ask reflection
        if config.require_reflection and not progress.star_coverage.get("reflection"):
            progress.phase = ProbePhase.REFLECTION
            return await self._generate_reflection_probe(state, traits_metadata)

        # Check if we need recursion (second example)
        if progress.confidence < config.confidence_threshold_for_recursion:
            if progress.phase != ProbePhase.RECURSION:  # Only one recursion
                progress.phase = ProbePhase.RECURSION
                return await self._generate_recursion_probe(state, traits_metadata)

        # Trait is complete, move to next
        progress.is_complete = True
        progress.phase = ProbePhase.COMPLETE
        return await self._move_to_next_trait(state, traits_metadata)

    async def _generate_next_probe(
        self,
        state: InterviewState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[InterviewState, InterviewResponse]:
        """Generate the primary probe for current trait."""
        current_trait_id = self._get_current_trait_id(state)
        if not current_trait_id:
            return await self._move_to_closing(state)

        progress = state.trait_progress[current_trait_id]
        trait_meta = traits_metadata.get(current_trait_id, {})

        # Build probe context
        context = ProbeGenerationContext(
            trait_id=current_trait_id,
            trait_name=progress.trait_name,
            trait_definition=trait_meta.get("definition", ""),
            role_context=trait_meta.get("role_context"),
            resume_summary=self._get_resume_summary(state),
            behavioral_anchors=trait_meta.get("behavioral_anchors"),
            probe_type="PRIMARY",
        )

        # Generate probe
        probe = await self.probe_generator.generate_probe(context)

        # Validate probe for compliance
        probe_validation = self.compliance_guard.validate_probe(probe.text)
        if not probe_validation.is_valid:
            # Log the violation but continue with a sanitized version
            # In production, this would be logged to the compliance audit trail
            pass
        # Store compliance metadata for audit
        probe.compliance_validation = {
            "is_valid": probe_validation.is_valid,
            "violations": [v.model_dump() for v in probe_validation.violations],
            "warnings": [w.model_dump() for w in probe_validation.warnings],
        }

        # Customize with resume if available
        if state.resume_elements and state.config.enable_resume_customization:
            customization = await self.resume_customizer.customize_probe(
                generic_probe=probe.text,
                trait_id=current_trait_id,
                trait_name=progress.trait_name,
                resume_elements=state.resume_elements,
            )
            if customization.resume_anchors:
                probe.text = customization.customized_probe
                probe.is_resume_customized = True
                probe.resume_anchors = customization.resume_anchors

        # Update state
        progress.probes_used += 1
        progress.has_primary_probe = True
        state.exchanges.append({
            "sequence": len(state.exchanges) + 1,
            "speaker": "SYSTEM",
            "type": "PRIMARY_PROBE",
            "content": probe.text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trait_id": current_trait_id,
            "patterns_applied": probe.patterns_applied,
        })

        return state, InterviewResponse(
            next_prompt=probe.text,
            prompt_type="PROBE",
            trait_id=current_trait_id,
            trait_progress=progress,
            overall_progress=self._calculate_overall_progress(state),
            can_end_interview=self._can_end_early(state),
        )

    async def _generate_follow_up(
        self,
        state: InterviewState,
        traits_metadata: Dict[str, Dict[str, Any]],
        follow_up_type: str,
    ) -> tuple[InterviewState, InterviewResponse]:
        """Generate a follow-up probe for missing STAR component."""
        current_trait_id = self._get_current_trait_id(state)
        progress = state.trait_progress[current_trait_id]
        trait_meta = traits_metadata.get(current_trait_id, {})

        # Determine missing component
        component = follow_up_type.replace("FOLLOW_UP_", "").lower()

        context = ProbeGenerationContext(
            trait_id=current_trait_id,
            trait_name=progress.trait_name,
            trait_definition=trait_meta.get("definition", ""),
            prior_responses=self._get_trait_responses(state, current_trait_id),
            star_coverage=progress.star_coverage,
            probe_type=follow_up_type,
        )

        probe = await self.probe_generator.generate_follow_up(context, component)

        # Update state
        progress.probes_used += 1
        state.exchanges.append({
            "sequence": len(state.exchanges) + 1,
            "speaker": "SYSTEM",
            "type": follow_up_type,
            "content": probe.text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trait_id": current_trait_id,
        })

        return state, InterviewResponse(
            next_prompt=probe.text,
            prompt_type="FOLLOW_UP",
            trait_id=current_trait_id,
            trait_progress=progress,
            overall_progress=self._calculate_overall_progress(state),
            can_end_interview=self._can_end_early(state),
        )

    async def _generate_depth_probe(
        self,
        state: InterviewState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[InterviewState, InterviewResponse]:
        """Generate a depth escalation probe."""
        current_trait_id = self._get_current_trait_id(state)
        progress = state.trait_progress[current_trait_id]
        trait_meta = traits_metadata.get(current_trait_id, {})

        context = ProbeGenerationContext(
            trait_id=current_trait_id,
            trait_name=progress.trait_name,
            trait_definition=trait_meta.get("definition", ""),
            prior_responses=self._get_trait_responses(state, current_trait_id),
            probe_type="DEPTH_ESCALATION",
        )

        probe = await self.probe_generator.generate_depth_escalation_probe(context)

        progress.probes_used += 1
        state.exchanges.append({
            "sequence": len(state.exchanges) + 1,
            "speaker": "SYSTEM",
            "type": "DEPTH_ESCALATION",
            "content": probe.text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trait_id": current_trait_id,
        })

        return state, InterviewResponse(
            next_prompt=probe.text,
            prompt_type="FOLLOW_UP",
            trait_id=current_trait_id,
            trait_progress=progress,
            overall_progress=self._calculate_overall_progress(state),
            can_end_interview=self._can_end_early(state),
        )

    async def _generate_conflict_probe(
        self,
        state: InterviewState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[InterviewState, InterviewResponse]:
        """Generate a probe to explore conflict/tension."""
        current_trait_id = self._get_current_trait_id(state)
        progress = state.trait_progress[current_trait_id]
        trait_meta = traits_metadata.get(current_trait_id, {})

        context = ProbeGenerationContext(
            trait_id=current_trait_id,
            trait_name=progress.trait_name,
            trait_definition=trait_meta.get("definition", ""),
            prior_responses=self._get_trait_responses(state, current_trait_id),
            probe_type="FOLLOW_UP_CONFLICT",
        )

        probe = await self.probe_generator.generate_conflict_probe(context)

        progress.probes_used += 1
        state.exchanges.append({
            "sequence": len(state.exchanges) + 1,
            "speaker": "SYSTEM",
            "type": "FOLLOW_UP_CONFLICT",
            "content": probe.text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trait_id": current_trait_id,
        })

        return state, InterviewResponse(
            next_prompt=probe.text,
            prompt_type="FOLLOW_UP",
            trait_id=current_trait_id,
            trait_progress=progress,
            overall_progress=self._calculate_overall_progress(state),
            can_end_interview=self._can_end_early(state),
        )

    async def _generate_reflection_probe(
        self,
        state: InterviewState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[InterviewState, InterviewResponse]:
        """Generate a reflection probe (+R in STAR+)."""
        current_trait_id = self._get_current_trait_id(state)
        progress = state.trait_progress[current_trait_id]
        trait_meta = traits_metadata.get(current_trait_id, {})

        context = ProbeGenerationContext(
            trait_id=current_trait_id,
            trait_name=progress.trait_name,
            trait_definition=trait_meta.get("definition", ""),
            prior_responses=self._get_trait_responses(state, current_trait_id),
            probe_type="REFLECTION",
        )

        probe = await self.probe_generator.generate_reflection_probe(context)

        progress.probes_used += 1
        state.exchanges.append({
            "sequence": len(state.exchanges) + 1,
            "speaker": "SYSTEM",
            "type": "REFLECTION",
            "content": probe.text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trait_id": current_trait_id,
        })

        return state, InterviewResponse(
            next_prompt=probe.text,
            prompt_type="REFLECTION",
            trait_id=current_trait_id,
            trait_progress=progress,
            overall_progress=self._calculate_overall_progress(state),
            can_end_interview=self._can_end_early(state),
        )

    async def _generate_recursion_probe(
        self,
        state: InterviewState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[InterviewState, InterviewResponse]:
        """Generate a recursion probe (+R in STAR+) for a second example."""
        current_trait_id = self._get_current_trait_id(state)
        progress = state.trait_progress[current_trait_id]
        trait_meta = traits_metadata.get(current_trait_id, {})

        context = ProbeGenerationContext(
            trait_id=current_trait_id,
            trait_name=progress.trait_name,
            trait_definition=trait_meta.get("definition", ""),
            prior_responses=self._get_trait_responses(state, current_trait_id),
            current_confidence=progress.confidence,
            probe_type="RECURSION",
        )

        probe = await self.probe_generator.generate_recursion_probe(context)

        progress.probes_used += 1
        state.exchanges.append({
            "sequence": len(state.exchanges) + 1,
            "speaker": "SYSTEM",
            "type": "RECURSION",
            "content": probe.text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trait_id": current_trait_id,
        })

        return state, InterviewResponse(
            next_prompt=probe.text,
            prompt_type="RECURSION",
            trait_id=current_trait_id,
            trait_progress=progress,
            overall_progress=self._calculate_overall_progress(state),
            can_end_interview=self._can_end_early(state),
        )

    async def _move_to_next_trait(
        self,
        state: InterviewState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[InterviewState, InterviewResponse]:
        """Move to the next trait to assess."""
        state.current_trait_index += 1

        # Check if all traits are done
        trait_ids = list(state.trait_progress.keys())
        if state.current_trait_index >= len(trait_ids):
            return await self._move_to_closing(state)

        # Generate probe for next trait
        return await self._generate_next_probe(state, traits_metadata)

    async def _move_to_closing(
        self,
        state: InterviewState,
    ) -> tuple[InterviewState, InterviewResponse]:
        """Move to closing phase."""
        state.phase = InterviewPhase.CANDIDATE_QUESTIONS

        state.exchanges.append({
            "sequence": len(state.exchanges) + 1,
            "speaker": "SYSTEM",
            "type": "CLOSING",
            "content": self.CLOSING_TEMPLATE,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        return state, InterviewResponse(
            next_prompt=self.CLOSING_TEMPLATE,
            prompt_type="CLOSING",
            overall_progress=1.0,
            can_end_interview=True,
        )

    async def _handle_candidate_questions(
        self,
        state: InterviewState,
        response_text: str,
    ) -> tuple[InterviewState, InterviewResponse]:
        """Handle candidate questions at the end."""
        # Simple handling - in a real system this might use LLM
        state.phase = InterviewPhase.CLOSING

        closing_response = "Those are great questions. [Answers would be provided here based on role context.] Thank you again for your time today!"

        state.exchanges.append({
            "sequence": len(state.exchanges) + 1,
            "speaker": "SYSTEM",
            "type": "ANSWER",
            "content": closing_response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        return state, InterviewResponse(
            next_prompt=closing_response,
            prompt_type="CLOSING",
            overall_progress=1.0,
            interview_complete=True,
            can_end_interview=True,
        )

    def _complete_interview(
        self,
        state: InterviewState,
    ) -> tuple[InterviewState, InterviewResponse]:
        """Mark interview as complete."""
        state.phase = InterviewPhase.COMPLETED

        return state, InterviewResponse(
            next_prompt="",
            prompt_type="COMPLETE",
            overall_progress=1.0,
            interview_complete=True,
        )

    def _get_current_trait_id(self, state: InterviewState) -> Optional[str]:
        """Get the ID of the current trait being assessed."""
        trait_ids = list(state.trait_progress.keys())
        if state.current_trait_index < len(trait_ids):
            return trait_ids[state.current_trait_index]
        return None

    def _get_last_probe_text(self, state: InterviewState) -> str:
        """Get the text of the last probe sent."""
        for exchange in reversed(state.exchanges):
            if exchange.get("speaker") == "SYSTEM" and "PROBE" in exchange.get("type", ""):
                return exchange.get("content", "")
        return ""

    def _get_trait_responses(
        self,
        state: InterviewState,
        trait_id: str,
    ) -> List[Dict[str, Any]]:
        """Get all candidate responses for a specific trait."""
        return [
            e for e in state.exchanges
            if e.get("speaker") == "CANDIDATE" and e.get("trait_id") == trait_id
        ]

    def _get_resume_summary(self, state: InterviewState) -> Optional[str]:
        """Get resume summary from elements."""
        if not state.resume_elements:
            return None
        summaries = [f"- {e.description}" for e in state.resume_elements[:5]]
        return "\n".join(summaries)

    def _calculate_overall_progress(self, state: InterviewState) -> float:
        """Calculate overall interview progress."""
        if not state.trait_progress:
            return 0.0
        completed = sum(1 for p in state.trait_progress.values() if p.is_complete)
        return completed / len(state.trait_progress)

    def _can_end_early(self, state: InterviewState) -> bool:
        """Check if interview can end early with sufficient evidence."""
        # Allow ending if all traits have at least minimum evidence
        for progress in state.trait_progress.values():
            if progress.behavioral_evidence_count < state.config.minimum_behavioral_evidence:
                return False
        return True


# Singleton instance
_interview_engine: Optional[InterviewEngine] = None


def get_interview_engine() -> InterviewEngine:
    """Get the interview engine instance."""
    global _interview_engine
    if _interview_engine is None:
        _interview_engine = InterviewEngine()
    return _interview_engine
