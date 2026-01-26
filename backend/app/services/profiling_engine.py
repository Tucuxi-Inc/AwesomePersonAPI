"""
Profiling Session Engine for conducting training-framed conversations with top performers.

This engine orchestrates the profile development workflow, using a "training AI" framing
to elicit authentic behavioral examples from top performers without triggering
interview-mode responses.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from app.services.llm_client import get_llm_client
from app.services.trait_extractor import get_trait_extractor, TraitExtractionResult


class ProfilingPhase(str, Enum):
    """Phases of a profiling session."""
    NOT_STARTED = "NOT_STARTED"
    INTRODUCTION = "INTRODUCTION"
    RAPPORT_BUILDING = "RAPPORT_BUILDING"
    TRAIT_EXPLORATION = "TRAIT_EXPLORATION"
    DEEP_DIVE = "DEEP_DIVE"
    REFLECTION = "REFLECTION"
    CLOSING = "CLOSING"
    COMPLETED = "COMPLETED"


@dataclass
class ProfilingConfig:
    """Configuration for a profiling session."""
    target_traits: List[str] = field(default_factory=list)
    max_duration_minutes: int = 45
    max_questions_per_trait: int = 3
    include_scenario_probes: bool = True
    focus_on_challenges: bool = True
    extract_counter_indicators: bool = True


@dataclass
class ProfilingState:
    """Current state of a profiling session."""
    session_id: str
    top_performer_id: str
    phase: ProfilingPhase = ProfilingPhase.NOT_STARTED
    current_trait_index: int = 0
    current_trait_questions: int = 0
    transcript: List[Dict[str, Any]] = field(default_factory=list)
    extracted_signals: List[Dict[str, Any]] = field(default_factory=list)
    start_time: Optional[datetime] = None
    config: ProfilingConfig = field(default_factory=ProfilingConfig)
    performer_context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProfilingResponse:
    """Response from the profiling engine."""
    next_prompt: str
    prompt_type: str  # INTRODUCTION, RAPPORT, EXPLORATION, DEEP_DIVE, REFLECTION, CLOSING
    current_trait: Optional[str] = None
    phase: ProfilingPhase = ProfilingPhase.TRAIT_EXPLORATION
    progress: float = 0.0
    can_end_session: bool = False
    session_complete: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class ProfilingEngine:
    """
    Orchestrates profiling sessions with top performers.

    Uses a "training AI" framing where the top performer believes they're
    helping to train an AI system, which elicits more authentic responses
    than traditional interview questioning.
    """

    INTRODUCTION_TEMPLATE = """Thank you so much for taking the time to help us today! Your expertise and success in your role make you exactly the kind of person we want to learn from.

We're building an AI system to help identify great candidates for roles like yours, and we need to understand what actually makes someone successful - not just the job description, but the real day-to-day stuff that matters.

The best way you can help is just by sharing real examples from your experience. There are no right or wrong answers - we're trying to capture the authentic patterns of how top performers like yourself approach situations.

Feel free to be as specific as you want. The more details about real situations, the better the AI will learn.

Ready to get started?"""

    RAPPORT_TEMPLATE = """Before we dive into specific situations, I'd love to understand your role a bit better.

Tell me about a typical week in your job - what are the kinds of challenges or decisions you face regularly? I'm trying to understand what "success" actually looks like in your position."""

    CLOSING_TEMPLATE = """This has been incredibly helpful - you've given us exactly the kind of real-world examples that will help the AI understand what great performance looks like.

Is there anything else you think is important for understanding success in your role that we haven't covered? Any advice you'd give to someone just starting out?"""

    def __init__(self):
        self.llm_client = get_llm_client()
        self.trait_extractor = get_trait_extractor()

    async def start_session(
        self,
        session_id: str,
        top_performer_id: str,
        performer_context: Dict[str, Any],
        target_traits: List[Dict[str, Any]],
        config: Optional[ProfilingConfig] = None,
    ) -> tuple["ProfilingState", ProfilingResponse]:
        """
        Start a new profiling session.

        Args:
            session_id: Unique session identifier
            top_performer_id: ID of the top performer
            performer_context: Information about the performer's role
            target_traits: Traits to explore in this session
            config: Optional session configuration

        Returns:
            Tuple of (state, response)
        """
        if config is None:
            config = ProfilingConfig(
                target_traits=[t.get("id", t.get("name")) for t in target_traits]
            )

        state = ProfilingState(
            session_id=session_id,
            top_performer_id=top_performer_id,
            phase=ProfilingPhase.INTRODUCTION,
            config=config,
            performer_context=performer_context,
            start_time=datetime.now(timezone.utc),
        )

        # Add performer name if available
        performer_name = performer_context.get("name", "there")
        intro = self.INTRODUCTION_TEMPLATE

        # Record the introduction in transcript
        state.transcript.append({
            "role": "interviewer",
            "content": intro,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "phase": ProfilingPhase.INTRODUCTION.value,
        })

        return state, ProfilingResponse(
            next_prompt=intro,
            prompt_type="INTRODUCTION",
            phase=ProfilingPhase.INTRODUCTION,
            progress=0.0,
            can_end_session=False,
            session_complete=False,
        )

    async def process_response(
        self,
        state: ProfilingState,
        response_text: str,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """
        Process a response from the top performer and generate next prompt.

        Args:
            state: Current session state
            response_text: The performer's response
            traits_metadata: Metadata about target traits

        Returns:
            Tuple of (updated_state, response)
        """
        # Record the response
        state.transcript.append({
            "role": "performer",
            "content": response_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "phase": state.phase.value,
        })

        # Extract signals from response if in exploration/deep-dive phase
        if state.phase in [ProfilingPhase.TRAIT_EXPLORATION, ProfilingPhase.DEEP_DIVE]:
            await self._extract_and_store_signals(state, response_text, traits_metadata)

        # Determine next action based on phase
        if state.phase == ProfilingPhase.INTRODUCTION:
            return await self._handle_introduction_response(state, traits_metadata)

        elif state.phase == ProfilingPhase.RAPPORT_BUILDING:
            return await self._handle_rapport_response(state, traits_metadata)

        elif state.phase == ProfilingPhase.TRAIT_EXPLORATION:
            return await self._handle_exploration_response(state, response_text, traits_metadata)

        elif state.phase == ProfilingPhase.DEEP_DIVE:
            return await self._handle_deep_dive_response(state, response_text, traits_metadata)

        elif state.phase == ProfilingPhase.REFLECTION:
            return await self._handle_reflection_response(state, traits_metadata)

        elif state.phase == ProfilingPhase.CLOSING:
            return await self._complete_session(state)

        return state, ProfilingResponse(
            next_prompt="Thank you for your time!",
            prompt_type="CLOSING",
            phase=ProfilingPhase.COMPLETED,
            progress=1.0,
            session_complete=True,
        )

    async def _handle_introduction_response(
        self,
        state: ProfilingState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """Handle response to introduction, move to rapport building."""
        state.phase = ProfilingPhase.RAPPORT_BUILDING

        rapport_prompt = self.RAPPORT_TEMPLATE

        state.transcript.append({
            "role": "interviewer",
            "content": rapport_prompt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "phase": state.phase.value,
        })

        return state, ProfilingResponse(
            next_prompt=rapport_prompt,
            prompt_type="RAPPORT",
            phase=state.phase,
            progress=0.05,
            can_end_session=False,
        )

    async def _handle_rapport_response(
        self,
        state: ProfilingState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """Handle rapport response, move to trait exploration."""
        state.phase = ProfilingPhase.TRAIT_EXPLORATION
        state.current_trait_index = 0
        state.current_trait_questions = 0

        # Generate first trait exploration prompt
        return await self._generate_exploration_prompt(state, traits_metadata)

    async def _handle_exploration_response(
        self,
        state: ProfilingState,
        response_text: str,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """Handle trait exploration response."""
        state.current_trait_questions += 1

        # Check if we should do a deep dive on this response
        if await self._should_deep_dive(response_text, traits_metadata):
            state.phase = ProfilingPhase.DEEP_DIVE
            return await self._generate_deep_dive_prompt(state, response_text, traits_metadata)

        # Check if we've asked enough questions for this trait
        if state.current_trait_questions >= state.config.max_questions_per_trait:
            state.current_trait_index += 1
            state.current_trait_questions = 0

            # Check if we've covered all traits
            if state.current_trait_index >= len(state.config.target_traits):
                state.phase = ProfilingPhase.REFLECTION
                return await self._generate_reflection_prompt(state, traits_metadata)

        # Continue exploration
        return await self._generate_exploration_prompt(state, traits_metadata)

    async def _handle_deep_dive_response(
        self,
        state: ProfilingState,
        response_text: str,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """Handle deep dive response, return to exploration."""
        state.phase = ProfilingPhase.TRAIT_EXPLORATION
        state.current_trait_questions += 1

        # Check if we should move to next trait
        if state.current_trait_questions >= state.config.max_questions_per_trait:
            state.current_trait_index += 1
            state.current_trait_questions = 0

            if state.current_trait_index >= len(state.config.target_traits):
                state.phase = ProfilingPhase.REFLECTION
                return await self._generate_reflection_prompt(state, traits_metadata)

        return await self._generate_exploration_prompt(state, traits_metadata)

    async def _handle_reflection_response(
        self,
        state: ProfilingState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """Handle reflection response, move to closing."""
        state.phase = ProfilingPhase.CLOSING

        closing_prompt = self.CLOSING_TEMPLATE

        state.transcript.append({
            "role": "interviewer",
            "content": closing_prompt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "phase": state.phase.value,
        })

        return state, ProfilingResponse(
            next_prompt=closing_prompt,
            prompt_type="CLOSING",
            phase=state.phase,
            progress=0.95,
            can_end_session=True,
        )

    async def _complete_session(
        self,
        state: ProfilingState,
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """Complete the session."""
        state.phase = ProfilingPhase.COMPLETED

        return state, ProfilingResponse(
            next_prompt="Thank you! This session has been completed.",
            prompt_type="COMPLETE",
            phase=state.phase,
            progress=1.0,
            session_complete=True,
        )

    async def _generate_exploration_prompt(
        self,
        state: ProfilingState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """Generate a trait exploration prompt."""
        if state.current_trait_index >= len(state.config.target_traits):
            state.phase = ProfilingPhase.REFLECTION
            return await self._generate_reflection_prompt(state, traits_metadata)

        current_trait_id = state.config.target_traits[state.current_trait_index]
        trait_meta = traits_metadata.get(current_trait_id, {})
        trait_name = trait_meta.get("name", current_trait_id)

        # Get previous responses for context
        recent_responses = [
            t["content"] for t in state.transcript[-4:]
            if t["role"] == "performer"
        ]

        system_prompt = """You are conducting a profiling conversation with a top performer.
Your goal is to elicit specific behavioral examples that reveal how they approach situations.

IMPORTANT FRAMING: The performer believes they're helping train an AI system.
Use language like "help the AI understand" or "what patterns should the AI look for".

Guidelines:
- Ask about SPECIFIC past situations, not hypotheticals
- Use the "training AI" framing to get authentic responses
- Focus on challenges, decisions, and how they handled uncertainty
- Avoid asking direct questions about traits - ask about situations that reveal traits
- Reference their role context when relevant
- Keep questions conversational and natural"""

        user_prompt = f"""Generate the next exploration question for this profiling session.

TARGET TRAIT: {trait_name}
TRAIT DEFINITION: {trait_meta.get('definition', 'Not specified')}

PERFORMER CONTEXT:
- Job Title: {state.performer_context.get('job_title', 'Not specified')}
- Department: {state.performer_context.get('department', 'Not specified')}
- Role Category: {state.performer_context.get('role_category', 'Not specified')}

RECENT RESPONSES: {recent_responses if recent_responses else 'This is the first exploration question'}

QUESTIONS ASKED FOR THIS TRAIT: {state.current_trait_questions}

Generate a natural, conversational question that will elicit behavioral examples related to {trait_name}.
Use the "training AI" framing. Just provide the question, no explanation."""

        try:
            prompt = await self.llm_client.complete(
                prompt=user_prompt,
                system_prompt=system_prompt,
                max_tokens=300,
                temperature=0.7,
            )

            prompt = prompt.strip()

            state.transcript.append({
                "role": "interviewer",
                "content": prompt,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "phase": state.phase.value,
                "target_trait": current_trait_id,
            })

            progress = self._calculate_progress(state)

            return state, ProfilingResponse(
                next_prompt=prompt,
                prompt_type="EXPLORATION",
                current_trait=trait_name,
                phase=state.phase,
                progress=progress,
                can_end_session=progress > 0.3,
            )

        except Exception as e:
            # Fallback prompt
            fallback = f"Can you tell me about a specific situation where you had to {trait_meta.get('definition', 'handle a challenging situation').lower()}? What did you do and what happened?"

            state.transcript.append({
                "role": "interviewer",
                "content": fallback,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "phase": state.phase.value,
                "target_trait": current_trait_id,
            })

            return state, ProfilingResponse(
                next_prompt=fallback,
                prompt_type="EXPLORATION",
                current_trait=trait_name,
                phase=state.phase,
                progress=self._calculate_progress(state),
            )

    async def _generate_deep_dive_prompt(
        self,
        state: ProfilingState,
        response_text: str,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """Generate a deep dive follow-up question."""
        current_trait_id = state.config.target_traits[state.current_trait_index]
        trait_meta = traits_metadata.get(current_trait_id, {})

        system_prompt = """You are following up on a top performer's response to get more detail.
Your goal is to understand the SPECIFIC behaviors, decisions, and thought processes.

Use the "training AI" framing - e.g., "That's helpful for the AI to understand.
Can you tell me more about..." """

        user_prompt = f"""Generate a follow-up question to dig deeper into this response.

THEIR RESPONSE: {response_text[:500]}

TARGET TRAIT: {trait_meta.get('name', current_trait_id)}

Focus on:
- Specific actions they took
- How they made decisions
- What they were thinking
- What challenges they faced

Just provide the follow-up question."""

        try:
            prompt = await self.llm_client.complete(
                prompt=user_prompt,
                system_prompt=system_prompt,
                max_tokens=200,
            )

            prompt = prompt.strip()

            state.transcript.append({
                "role": "interviewer",
                "content": prompt,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "phase": state.phase.value,
                "target_trait": current_trait_id,
            })

            return state, ProfilingResponse(
                next_prompt=prompt,
                prompt_type="DEEP_DIVE",
                current_trait=trait_meta.get("name"),
                phase=state.phase,
                progress=self._calculate_progress(state),
            )

        except Exception:
            fallback = "That's really helpful. Can you tell me more about how you approached that decision specifically?"

            state.transcript.append({
                "role": "interviewer",
                "content": fallback,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "phase": state.phase.value,
            })

            return state, ProfilingResponse(
                next_prompt=fallback,
                prompt_type="DEEP_DIVE",
                phase=state.phase,
                progress=self._calculate_progress(state),
            )

    async def _generate_reflection_prompt(
        self,
        state: ProfilingState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> tuple[ProfilingState, ProfilingResponse]:
        """Generate a reflection prompt."""
        prompt = """We've covered a lot of ground. Looking back at your experience, what do you think separates good performers from great performers in your role? What's the thing that really makes the difference?"""

        state.transcript.append({
            "role": "interviewer",
            "content": prompt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "phase": state.phase.value,
        })

        return state, ProfilingResponse(
            next_prompt=prompt,
            prompt_type="REFLECTION",
            phase=state.phase,
            progress=0.9,
            can_end_session=True,
        )

    async def _should_deep_dive(
        self,
        response_text: str,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> bool:
        """Determine if we should do a deep dive on this response."""
        # Simple heuristic: dive deeper if response is substantive but could use more detail
        word_count = len(response_text.split())

        # Short responses might need probing
        if word_count < 50:
            return True

        # Medium-length responses are good candidates for deep dives
        if 50 <= word_count <= 150:
            # Check for specific indicators
            specificity_markers = [
                "for example", "specifically", "the numbers",
                "we achieved", "I decided", "the result was"
            ]
            has_specifics = any(marker in response_text.lower() for marker in specificity_markers)
            return not has_specifics

        # Long responses usually don't need immediate deep dive
        return False

    async def _extract_and_store_signals(
        self,
        state: ProfilingState,
        response_text: str,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> None:
        """Extract signals from a response and store in state."""
        if state.current_trait_index >= len(state.config.target_traits):
            return

        current_trait_id = state.config.target_traits[state.current_trait_index]
        trait_meta = traits_metadata.get(current_trait_id, {})

        # Get the prompt that elicited this response
        prompt_text = ""
        for entry in reversed(state.transcript[:-1]):
            if entry["role"] == "interviewer":
                prompt_text = entry["content"]
                break

        signals = await self.trait_extractor.extract_from_response(
            response_text=response_text,
            prompt_text=prompt_text,
            target_traits=[trait_meta] if trait_meta else [],
            context=state.performer_context,
        )

        # Store signals
        for signal in signals:
            state.extracted_signals.append({
                "trait_id": signal.trait_id,
                "trait_name": signal.trait_name,
                "signal_type": signal.signal_type,
                "strength": signal.strength,
                "evidence_text": signal.evidence_text,
                "confidence": signal.confidence,
            })

    def _calculate_progress(self, state: ProfilingState) -> float:
        """Calculate session progress."""
        if not state.config.target_traits:
            return 0.0

        total_traits = len(state.config.target_traits)
        questions_per_trait = state.config.max_questions_per_trait

        traits_completed = state.current_trait_index
        current_trait_progress = state.current_trait_questions / questions_per_trait

        progress = (traits_completed + current_trait_progress) / total_traits

        # Account for intro and closing phases
        return 0.1 + (progress * 0.8)

    async def end_session(
        self,
        state: ProfilingState,
        traits_metadata: Dict[str, Dict[str, Any]],
    ) -> TraitExtractionResult:
        """
        End the session and generate final extraction results.

        Args:
            state: Current session state
            traits_metadata: Metadata about target traits

        Returns:
            Complete extraction result for the session
        """
        # Get full list of traits for extraction
        target_traits = [
            traits_metadata.get(t_id, {"id": t_id, "name": t_id})
            for t_id in state.config.target_traits
        ]

        # Perform full extraction on the session
        result = await self.trait_extractor.extract_from_session(
            session_id=state.session_id,
            top_performer_id=state.top_performer_id,
            transcript=state.transcript,
            target_traits=target_traits,
            role_context=state.performer_context,
        )

        return result


# Singleton instance
profiling_engine = ProfilingEngine()


def get_profiling_engine() -> ProfilingEngine:
    """Get the profiling engine instance."""
    return profiling_engine
