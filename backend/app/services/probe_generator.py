"""Pattern-aware probe generator for intelligent interview question generation."""

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.services.patterns import (
    ReasoningPattern,
    EvidenceType,
    ResponseDepth,
    ProbeContext,
    PatternSelectionResult,
    select_patterns_for_context,
    PATTERN_DESCRIPTIONS,
)
from app.services.llm_client import get_llm_client


@dataclass
class GeneratedProbe:
    """A generated interview probe with metadata."""
    text: str
    probe_type: str
    trait_id: str
    patterns_applied: List[str]
    generation_rationale: str
    evidence_expectations: List[str]
    follow_up_triggers: List[Dict[str, str]]
    star_focus: Optional[str] = None
    is_resume_customized: bool = False
    resume_anchors: List[str] = field(default_factory=list)


@dataclass
class ProbeGenerationContext:
    """Context for generating a probe."""
    trait_id: str
    trait_name: str
    trait_definition: str
    role_context: Optional[str] = None
    resume_summary: Optional[str] = None
    prior_probes: List[Dict[str, Any]] = field(default_factory=list)
    prior_responses: List[Dict[str, Any]] = field(default_factory=list)
    evidence_collected: List[Dict[str, Any]] = field(default_factory=list)
    current_confidence: float = 0.0
    star_coverage: Dict[str, bool] = field(default_factory=dict)
    last_response_depth: Optional[ResponseDepth] = None
    last_evidence_type: Optional[EvidenceType] = None
    behavioral_anchors: Optional[Dict[str, Any]] = None
    probe_type: str = "PRIMARY"


class PatternAwareProbeGenerator:
    """
    Generates interview probes using Universal Reasoning Patterns.

    This generator applies cognitive patterns to create contextually intelligent
    probes that:
    - Surface assumptions (MC24)
    - Choose appropriate representation (MC35)
    - Calibrate abstraction level (MC38)
    - Explore solution space (MC44)
    - Detect omissions (IP3)
    - Explore conflict/tension (IP7)
    - Calibrate trust in evidence (IP11)
    - Identify risks (SP8)
    - Project scenarios (SP12)
    """

    def __init__(self):
        self.llm_client = get_llm_client()

    async def generate_probe(
        self,
        context: ProbeGenerationContext,
        patterns_override: Optional[List[ReasoningPattern]] = None,
    ) -> GeneratedProbe:
        """
        Generate a probe for the given context.

        Args:
            context: The context for probe generation
            patterns_override: Optional list of patterns to apply (otherwise auto-selected)

        Returns:
            A GeneratedProbe with the question and metadata
        """
        # Build probe context for pattern selection
        probe_context = self._build_probe_context(context)

        # Select patterns to apply
        if patterns_override:
            patterns = patterns_override
            rationale = "Patterns specified by caller"
        else:
            selection_result = select_patterns_for_context(context.trait_id, probe_context)
            patterns = selection_result.patterns
            rationale = selection_result.rationale

        # Build the generation prompt
        prompt = self._build_generation_prompt(context, patterns)

        # Generate the probe using LLM
        system_prompt = self._build_system_prompt()

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1024,
        )

        # Parse and return the generated probe
        return GeneratedProbe(
            text=result.get("probe_text", ""),
            probe_type=context.probe_type,
            trait_id=context.trait_id,
            patterns_applied=[p.value for p in patterns],
            generation_rationale=result.get("rationale", rationale),
            evidence_expectations=result.get("evidence_expectations", []),
            follow_up_triggers=result.get("follow_up_triggers", []),
            star_focus=result.get("star_focus"),
            is_resume_customized=bool(context.resume_summary and result.get("uses_resume_context")),
            resume_anchors=result.get("resume_anchors", []),
        )

    async def generate_follow_up(
        self,
        context: ProbeGenerationContext,
        missing_component: str,
    ) -> GeneratedProbe:
        """
        Generate a follow-up probe for a missing STAR component.

        Args:
            context: The context for probe generation
            missing_component: The STAR component that's missing (situation/task/action/result)

        Returns:
            A targeted follow-up probe
        """
        # Set probe type based on missing component
        probe_type_map = {
            "situation": "FOLLOW_UP_SITUATION",
            "task": "FOLLOW_UP_TASK",
            "action": "FOLLOW_UP_ACTION",
            "result": "FOLLOW_UP_RESULT",
        }
        context.probe_type = probe_type_map.get(missing_component, "FOLLOW_UP_DEPTH")

        # Always apply IP3 (omission detection) for follow-ups
        patterns = [ReasoningPattern.IP3_ACTIVE_LISTENING, ReasoningPattern.MC35_REPRESENTATION]

        prompt = self._build_follow_up_prompt(context, missing_component)
        system_prompt = self._build_system_prompt()

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=512,
        )

        return GeneratedProbe(
            text=result.get("probe_text", ""),
            probe_type=context.probe_type,
            trait_id=context.trait_id,
            patterns_applied=[p.value for p in patterns],
            generation_rationale=f"Follow-up for missing {missing_component}",
            evidence_expectations=result.get("evidence_expectations", []),
            follow_up_triggers=[],
            star_focus=missing_component,
        )

    async def generate_reflection_probe(
        self,
        context: ProbeGenerationContext,
    ) -> GeneratedProbe:
        """
        Generate a reflection probe (+R in STAR+).

        The reflection probe asks "What would you do differently?"
        to assess self-awareness and learning.
        """
        context.probe_type = "REFLECTION"

        # Use standard reflection templates with minor customization
        reflection_templates = [
            "Looking back at that situation, what would you do differently if you could do it again?",
            "If you faced a similar situation today, what might you change about your approach?",
            "What did you learn from that experience that changed how you handle similar situations?",
        ]

        # Simple LLM call to select and adapt the most appropriate template
        prompt = f"""Given this interview context about {context.trait_name}:

Prior response summary: {self._summarize_responses(context.prior_responses)}

Select and adapt ONE reflection question from these templates:
{chr(10).join(f'- {t}' for t in reflection_templates)}

Return JSON:
{{
    "probe_text": "Your adapted reflection question",
    "evidence_expectations": ["what good answers should include"]
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You are an expert behavioral interviewer. Generate targeted reflection questions.",
            max_tokens=256,
        )

        return GeneratedProbe(
            text=result.get("probe_text", reflection_templates[0]),
            probe_type="REFLECTION",
            trait_id=context.trait_id,
            patterns_applied=["REFLECTION"],
            generation_rationale="Reflection probe to assess self-awareness",
            evidence_expectations=result.get("evidence_expectations", [
                "acknowledgment of what could be improved",
                "specific lessons learned",
                "evidence of growth mindset"
            ]),
            follow_up_triggers=[],
            star_focus="reflection",
        )

    async def generate_recursion_probe(
        self,
        context: ProbeGenerationContext,
    ) -> GeneratedProbe:
        """
        Generate a recursion probe (+R in STAR+).

        The recursion probe asks for a second example to test
        pattern consistency and build confidence.
        """
        context.probe_type = "RECURSION"

        # Apply solution space exploration to find alternative angles
        patterns = [ReasoningPattern.MC44_SOLUTION_SPACE, ReasoningPattern.MC35_REPRESENTATION]

        prompt = f"""Generate a RECURSION probe asking for a SECOND example of {context.trait_name}.

Trait: {context.trait_name}
Definition: {context.trait_definition}

The candidate has already provided one example. We need a second example to:
1. Test pattern consistency (is this a real behavior pattern or one-off?)
2. Build confidence in our assessment
3. See the trait in a different context

First example was about: {self._summarize_responses(context.prior_responses)}

Generate a probe that:
- Explicitly asks for ANOTHER/DIFFERENT example
- Ideally targets a different context (different project, team, timeframe)
- Maintains focus on {context.trait_name}

Return JSON:
{{
    "probe_text": "Your recursion probe",
    "evidence_expectations": ["what to look for"],
    "rationale": "why this angle"
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt=self._build_system_prompt(),
            max_tokens=512,
        )

        return GeneratedProbe(
            text=result.get("probe_text", f"Can you tell me about another time when you demonstrated {context.trait_name}?"),
            probe_type="RECURSION",
            trait_id=context.trait_id,
            patterns_applied=[p.value for p in patterns],
            generation_rationale=result.get("rationale", "Recursion probe for pattern consistency"),
            evidence_expectations=result.get("evidence_expectations", []),
            follow_up_triggers=[],
            star_focus=None,
        )

    async def generate_depth_escalation_probe(
        self,
        context: ProbeGenerationContext,
    ) -> GeneratedProbe:
        """
        Generate a depth escalation probe when response is too surface-level.

        Applies MC38 (Abstraction Level) to dig deeper.
        """
        context.probe_type = "DEPTH_ESCALATION"
        patterns = [ReasoningPattern.MC38_ABSTRACTION, ReasoningPattern.IP3_ACTIVE_LISTENING]

        prompt = f"""The candidate's response about {context.trait_name} was SURFACE-LEVEL.
We need to dig deeper for specific behavioral evidence.

Trait: {context.trait_name}
Their response: {self._summarize_responses(context.prior_responses[-1:] if context.prior_responses else [])}

Generate a probe that:
- Pushes for SPECIFIC details (names, dates, numbers, outcomes)
- Asks for a CONCRETE moment, not generalities
- Uses phrases like "walk me through specifically", "give me an example of"

Return JSON:
{{
    "probe_text": "Your depth probe",
    "evidence_expectations": ["specific details to look for"],
    "rationale": "why this approach"
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt=self._build_system_prompt(),
            max_tokens=512,
        )

        return GeneratedProbe(
            text=result.get("probe_text", "Can you walk me through that more specifically? What exactly happened?"),
            probe_type="DEPTH_ESCALATION",
            trait_id=context.trait_id,
            patterns_applied=[p.value for p in patterns],
            generation_rationale=result.get("rationale", "Depth escalation for surface response"),
            evidence_expectations=result.get("evidence_expectations", []),
            follow_up_triggers=[],
            star_focus=None,
        )

    async def generate_conflict_probe(
        self,
        context: ProbeGenerationContext,
    ) -> GeneratedProbe:
        """
        Generate a probe to explore conflict/tension/failure.

        Applies IP7 (Conflict Exploration) when candidate gives only
        smooth/easy examples.
        """
        context.probe_type = "FOLLOW_UP_DEPTH"
        patterns = [ReasoningPattern.IP7_CONFLICT, ReasoningPattern.SP8_RISK]

        prompt = f"""The candidate has only shared smooth/successful examples for {context.trait_name}.
We need to probe for conflict, tension, or failure to get a fuller picture.

Trait: {context.trait_name}
Definition: {context.trait_definition}

Generate a probe that:
- Asks about a time when things DIDN'T go smoothly
- Explores disagreement, pushback, or difficulty
- Targets failure or challenge (not just success)

Good patterns:
- "Tell me about a time when [trait] didn't work out as planned"
- "When have you faced pushback when trying to [trait behavior]?"
- "What's the hardest part about [trait] for you?"

Return JSON:
{{
    "probe_text": "Your conflict exploration probe",
    "evidence_expectations": ["what to look for"],
    "rationale": "why this matters for assessment"
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt=self._build_system_prompt(),
            max_tokens=512,
        )

        return GeneratedProbe(
            text=result.get("probe_text", f"Tell me about a time when demonstrating {context.trait_name} was particularly challenging or didn't go as planned."),
            probe_type="FOLLOW_UP_DEPTH",
            trait_id=context.trait_id,
            patterns_applied=[p.value for p in patterns],
            generation_rationale=result.get("rationale", "Exploring conflict/challenge for fuller assessment"),
            evidence_expectations=result.get("evidence_expectations", []),
            follow_up_triggers=[],
            star_focus=None,
        )

    def _build_probe_context(self, context: ProbeGenerationContext) -> ProbeContext:
        """Convert generation context to pattern selection context."""
        return ProbeContext(
            probes_asked=[
                {"trait_id": context.trait_id, "question": p.get("text", "")}
                for p in context.prior_probes
            ],
            responses=[
                {"trait_id": context.trait_id, "response": r.get("content", "")}
                for r in context.prior_responses
            ],
            evidence_collected=[
                {
                    "trait_id": context.trait_id,
                    "type": e.get("source_type", "SELF_REPORT"),
                    "text": e.get("source_text", ""),
                    "contains_conflict": e.get("contains_conflict", False),
                }
                for e in context.evidence_collected
            ],
            current_confidence=context.current_confidence,
            last_response_depth=context.last_response_depth,
            last_evidence_type=context.last_evidence_type,
        )

    def _build_system_prompt(self) -> str:
        """Build the system prompt for probe generation."""
        return """You are an expert behavioral interviewer trained in the STAR+ methodology.

Your role is to generate interview probes that:
1. Elicit SPECIFIC behavioral examples (not hypotheticals or self-reports)
2. Target the STAR components: Situation, Task, Action, Result
3. Are open-ended but focused
4. Cannot be answered with rehearsed responses
5. Dig beneath surface-level answers

Key principles:
- Ask about past behavior, not future intentions ("Tell me about a time..." not "What would you do if...")
- Focus on what THEY did personally, not the team
- Probe for concrete details: names, numbers, timelines, outcomes
- When in doubt, ask for specifics

Always return valid JSON with the requested fields."""

    def _build_generation_prompt(
        self,
        context: ProbeGenerationContext,
        patterns: List[ReasoningPattern],
    ) -> str:
        """Build the full generation prompt with pattern instructions."""
        pattern_instructions = self._get_pattern_instructions(patterns)
        candidate_context = self._format_candidate_context(context)

        # Include behavioral anchors if available
        anchor_section = ""
        if context.behavioral_anchors:
            anchor_section = f"""
Behavioral Anchors for Reference (what good/poor answers look like):
{self._format_behavioral_anchors(context.behavioral_anchors)}
"""

        return f"""Generate a PRIMARY interview probe for the trait: {context.trait_name}

TRAIT DEFINITION:
{context.trait_definition}

{candidate_context}
{anchor_section}
REASONING PATTERNS TO APPLY:
{pattern_instructions}

PROBE TYPE: {context.probe_type}

Generate ONE focused behavioral interview probe that applies the patterns above.

Return JSON:
{{
    "probe_text": "Your interview question",
    "rationale": "Why this probe and how it applies the patterns",
    "evidence_expectations": ["list of things a good answer should include"],
    "follow_up_triggers": [
        {{"condition": "missing_action", "follow_up_type": "FOLLOW_UP_ACTION"}},
        {{"condition": "surface_response", "follow_up_type": "DEPTH_ESCALATION"}}
    ],
    "star_focus": "situation|task|action|result|null",
    "uses_resume_context": true/false,
    "resume_anchors": ["specific resume elements referenced"]
}}"""

    def _build_follow_up_prompt(
        self,
        context: ProbeGenerationContext,
        missing_component: str,
    ) -> str:
        """Build a follow-up prompt for missing STAR component."""
        component_guidance = {
            "situation": "Ask for context: What was happening? What led to this? What was the environment?",
            "task": "Ask for their specific role: What were YOU responsible for? What was YOUR goal?",
            "action": "Ask for specific actions: What did YOU do? Walk me through your steps.",
            "result": "Ask for outcomes: What happened? What was the impact? What were the measurable results?",
        }

        last_response = ""
        if context.prior_responses:
            last_response = context.prior_responses[-1].get("content", "")[:500]

        return f"""Generate a follow-up probe to get the MISSING {missing_component.upper()} component.

Trait: {context.trait_name}
Last response: "{last_response}"

What's missing: {component_guidance.get(missing_component, "Specific details")}

Generate a SHORT, focused follow-up question that:
- Directly targets the missing {missing_component}
- Doesn't repeat what they already said
- Encourages specific detail

Return JSON:
{{
    "probe_text": "Your follow-up question",
    "evidence_expectations": ["what the answer should include"]
}}"""

    def _get_pattern_instructions(self, patterns: List[ReasoningPattern]) -> str:
        """Get instructions for each pattern to apply."""
        instructions = []
        for pattern in patterns:
            desc = PATTERN_DESCRIPTIONS.get(pattern, {})
            instructions.append(f"""
{pattern.value} - {desc.get('name', pattern.name)}:
  Purpose: {desc.get('purpose', 'N/A')}
  Application: {desc.get('application', 'N/A')}
""")
        return "\n".join(instructions)

    def _format_candidate_context(self, context: ProbeGenerationContext) -> str:
        """Format candidate context for the prompt."""
        sections = []

        if context.resume_summary:
            sections.append(f"CANDIDATE RESUME SUMMARY:\n{context.resume_summary}")

        if context.role_context:
            sections.append(f"ROLE CONTEXT:\n{context.role_context}")

        if context.prior_probes:
            probe_list = [p.get("text", "")[:100] for p in context.prior_probes[-3:]]
            sections.append(f"PRIOR PROBES FOR THIS TRAIT:\n" + "\n".join(f"- {p}" for p in probe_list))

        if context.prior_responses:
            response_list = [r.get("content", "")[:200] for r in context.prior_responses[-2:]]
            sections.append(f"CANDIDATE'S PRIOR RESPONSES:\n" + "\n".join(f"- {r}" for r in response_list))

        if context.star_coverage:
            covered = [k for k, v in context.star_coverage.items() if v]
            missing = [k for k, v in context.star_coverage.items() if not v]
            sections.append(f"STAR COVERAGE:\n  Covered: {', '.join(covered) or 'None'}\n  Missing: {', '.join(missing) or 'None'}")

        if context.current_confidence > 0:
            sections.append(f"CURRENT CONFIDENCE: {context.current_confidence:.0%}")

        return "\n\n".join(sections) if sections else "No prior context available."

    def _format_behavioral_anchors(self, anchors: Dict[str, Any]) -> str:
        """Format behavioral anchors for the prompt."""
        lines = []
        for score, data in sorted(anchors.items()):
            if isinstance(data, dict):
                label = data.get("label", f"Score {score}")
                indicators = data.get("indicators", [])
                lines.append(f"  Score {score} ({label}): {', '.join(indicators[:3])}")
        return "\n".join(lines)

    def _summarize_responses(self, responses: List[Dict[str, Any]]) -> str:
        """Summarize responses for context."""
        if not responses:
            return "No responses yet"
        summaries = []
        for r in responses[-2:]:
            content = r.get("content", "")[:300]
            summaries.append(content)
        return " | ".join(summaries)


# Singleton instance
_probe_generator: Optional[PatternAwareProbeGenerator] = None


def get_probe_generator() -> PatternAwareProbeGenerator:
    """Get the probe generator instance."""
    global _probe_generator
    if _probe_generator is None:
        _probe_generator = PatternAwareProbeGenerator()
    return _probe_generator
