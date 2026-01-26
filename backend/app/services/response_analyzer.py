"""
Pattern-aware response analyzer for extracting evidence from interview responses.

This module applies Universal Reasoning Patterns to analyze candidate responses,
extract behavioral evidence, classify evidence types, assess STAR completeness,
and recommend follow-up strategies.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from app.services.patterns import (
    ReasoningPattern,
    EvidenceType,
    ResponseDepth,
    EVIDENCE_WEIGHTS,
)
from app.services.llm_client import get_llm_client


class ResponseQuality(str, Enum):
    """Quality assessment of a response."""
    EXCELLENT = "EXCELLENT"  # Specific, detailed, behavioral
    GOOD = "GOOD"           # Has details but missing some elements
    ADEQUATE = "ADEQUATE"   # Usable but needs follow-up
    POOR = "POOR"           # Vague, hypothetical, or off-topic
    UNUSABLE = "UNUSABLE"   # Cannot extract meaningful evidence


@dataclass
class ExtractedEvidence:
    """Evidence extracted from a response."""
    source_type: EvidenceType
    source_text: str
    weight: float
    trait_signals: List[Dict[str, Any]]
    star_components: Dict[str, bool]
    confidence: float
    specificity_score: float
    contains_conflict: bool = False
    contains_failure: bool = False
    contains_challenge: bool = False
    matched_anchors: List[str] = field(default_factory=list)
    extraction_rationale: str = ""


@dataclass
class OmissionAnalysis:
    """Analysis of what's missing from a response (IP3 pattern)."""
    missing_star_components: List[str]
    avoided_topics: List[str]
    expected_but_absent: List[str]
    concerning_absences: List[str]


@dataclass
class AlternativeInterpretation:
    """Alternative interpretation of a response (MC44 pattern)."""
    interpretation_type: str  # favorable, concerning, non_obvious
    interpretation: str
    confidence: float


@dataclass
class ResponseAnalysis:
    """Complete analysis of a candidate response."""
    # Evidence extraction
    evidence_items: List[ExtractedEvidence]
    primary_evidence_type: EvidenceType

    # STAR completeness
    star_completeness: Dict[str, bool]
    star_completeness_score: float

    # Response quality
    response_depth: ResponseDepth
    response_quality: ResponseQuality
    specificity_score: float

    # Pattern-based analysis
    omissions: OmissionAnalysis
    alternative_interpretations: List[AlternativeInterpretation]
    tension_present: bool

    # Recommendations
    recommended_follow_up_patterns: List[ReasoningPattern]
    recommended_follow_up_type: Optional[str]

    # Summary
    summary: str
    confidence: float


class PatternAwareResponseAnalyzer:
    """
    Analyzes interview responses using Universal Reasoning Patterns.

    Applies multiple cognitive patterns to:
    - Extract behavioral evidence (IP11 Trust Calibration)
    - Identify omissions (IP3 Active Listening)
    - Generate alternative interpretations (MC44 Solution Space)
    - Assess response depth (MC38 Abstraction Level)
    - Detect conflict/tension (IP7 Conflict Exploration)
    """

    def __init__(self):
        self.llm_client = get_llm_client()

    async def analyze_response(
        self,
        response_text: str,
        probe_text: str,
        trait_name: str,
        trait_definition: str,
        behavioral_anchors: Optional[Dict[str, Any]] = None,
        prior_context: Optional[Dict[str, Any]] = None,
    ) -> ResponseAnalysis:
        """
        Perform comprehensive analysis of a candidate response.

        Args:
            response_text: The candidate's response
            probe_text: The probe/question that was asked
            trait_name: The trait being assessed
            trait_definition: Definition of the trait
            behavioral_anchors: Rubric behavioral anchors for matching
            prior_context: Previous exchanges and evidence for context

        Returns:
            Complete ResponseAnalysis with evidence and recommendations
        """
        # Run multiple analysis patterns in parallel conceptually
        # (In practice, we batch them in one LLM call for efficiency)

        prompt = self._build_comprehensive_analysis_prompt(
            response_text=response_text,
            probe_text=probe_text,
            trait_name=trait_name,
            trait_definition=trait_definition,
            behavioral_anchors=behavioral_anchors,
            prior_context=prior_context,
        )

        system_prompt = self._build_system_prompt()

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2048,
        )

        return self._parse_analysis_result(result, trait_name)

    async def classify_evidence_type(
        self,
        text: str,
        trait_name: str,
    ) -> EvidenceType:
        """
        Classify a piece of text by evidence type (IP11 Trust Calibration).

        Args:
            text: The text to classify
            trait_name: The trait context

        Returns:
            The evidence type classification
        """
        prompt = f"""Classify this text by evidence type for the trait "{trait_name}":

Text: "{text}"

Evidence types (from most to least valuable):
1. OBSERVED - Demonstrated during the interview itself
2. BEHAVIORAL - Specific past action with concrete details (names, dates, outcomes)
3. HYPOTHETICAL - What they would do in a situation
4. SELF_REPORT - Claims about themselves without backing evidence
5. OPINION - General beliefs or values

Key indicators:
- BEHAVIORAL: Past tense, specific details, named people/projects, measurable outcomes
- SELF_REPORT: "I am...", "I always...", "I tend to..." without examples
- HYPOTHETICAL: "I would...", "If... then I would..."
- OPINION: "I believe...", "I think that..."

Return JSON: {{"evidence_type": "BEHAVIORAL|SELF_REPORT|HYPOTHETICAL|OPINION|OBSERVED", "rationale": "brief explanation"}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You are an expert at classifying interview evidence. Be strict - only BEHAVIORAL if truly specific.",
            max_tokens=128,
        )

        type_str = result.get("evidence_type", "SELF_REPORT")
        return EvidenceType(type_str) if type_str in [e.value for e in EvidenceType] else EvidenceType.SELF_REPORT

    async def assess_star_completeness(
        self,
        response_text: str,
        trait_name: str,
    ) -> Dict[str, Any]:
        """
        Assess STAR+ component completeness in a response.

        Args:
            response_text: The candidate's response
            trait_name: The trait being assessed

        Returns:
            Dict with component presence and details
        """
        prompt = f"""Analyze this interview response for STAR+ component completeness:

Response: "{response_text}"

STAR+ Components:
- Situation: Context, setting, what was happening
- Task: Their specific role/responsibility, what they needed to accomplish
- Action: What THEY specifically did (not the team)
- Result: The outcome, impact, measurable results

For each component, determine:
1. Is it present? (true/false)
2. How complete is it? (score 0-1)
3. What specific text supports it?

Return JSON:
{{
    "situation": {{"present": bool, "completeness": float, "text": "quoted text or null"}},
    "task": {{"present": bool, "completeness": float, "text": "quoted text or null"}},
    "action": {{"present": bool, "completeness": float, "text": "quoted text or null"}},
    "result": {{"present": bool, "completeness": float, "text": "quoted text or null"}},
    "overall_completeness": float,
    "missing_components": ["list of missing components"],
    "strongest_component": "situation|task|action|result",
    "weakest_component": "situation|task|action|result"
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You are an expert STAR methodology assessor. Be thorough but fair.",
            max_tokens=512,
        )

        return result

    async def detect_omissions(
        self,
        response_text: str,
        probe_text: str,
        trait_name: str,
        expected_elements: Optional[List[str]] = None,
    ) -> OmissionAnalysis:
        """
        Detect what's missing from a response (IP3 Active Listening).

        Args:
            response_text: The candidate's response
            probe_text: The original probe
            trait_name: The trait being assessed
            expected_elements: Optional list of expected elements

        Returns:
            OmissionAnalysis with missing elements
        """
        expected_str = ""
        if expected_elements:
            expected_str = f"\nExpected elements for a good answer: {', '.join(expected_elements)}"

        prompt = f"""Analyze what's MISSING from this interview response (IP3 Active Listening pattern):

Probe: "{probe_text}"
Response: "{response_text}"
Trait: {trait_name}
{expected_str}

Identify:
1. Missing STAR components (situation, task, action, result)
2. Topics the candidate seemed to AVOID (touched on but redirected)
3. Elements we expected but didn't get
4. Concerning absences (red flags)

Return JSON:
{{
    "missing_star_components": ["list"],
    "avoided_topics": ["topics they seemed to redirect away from"],
    "expected_but_absent": ["things a good answer would have included"],
    "concerning_absences": ["potentially problematic omissions"]
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You are an expert at detecting what's missing in interview responses. Focus on substance, not style.",
            max_tokens=512,
        )

        return OmissionAnalysis(
            missing_star_components=result.get("missing_star_components", []),
            avoided_topics=result.get("avoided_topics", []),
            expected_but_absent=result.get("expected_but_absent", []),
            concerning_absences=result.get("concerning_absences", []),
        )

    async def generate_alternative_interpretations(
        self,
        response_text: str,
        trait_name: str,
        initial_interpretation: str,
    ) -> List[AlternativeInterpretation]:
        """
        Generate alternative interpretations (MC44 Solution Space Exploration).

        Args:
            response_text: The candidate's response
            trait_name: The trait being assessed
            initial_interpretation: The initial/obvious interpretation

        Returns:
            List of alternative interpretations
        """
        prompt = f"""Apply MC44 (Solution Space Exploration) to this interview response:

Response: "{response_text}"
Trait: {trait_name}
Initial interpretation: {initial_interpretation}

Generate THREE alternative interpretations:
1. FAVORABLE: Most charitable interpretation
2. CONCERNING: Most concerning interpretation
3. NON_OBVIOUS: A non-obvious angle we might miss

For each, explain what evidence supports it and your confidence (0-1).

Return JSON:
{{
    "favorable": {{"interpretation": "...", "supporting_evidence": "...", "confidence": float}},
    "concerning": {{"interpretation": "...", "supporting_evidence": "...", "confidence": float}},
    "non_obvious": {{"interpretation": "...", "supporting_evidence": "...", "confidence": float}}
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You are an expert at considering multiple interpretations. Be genuinely open to different readings.",
            max_tokens=512,
        )

        interpretations = []
        for interp_type in ["favorable", "concerning", "non_obvious"]:
            if interp_type in result:
                data = result[interp_type]
                interpretations.append(AlternativeInterpretation(
                    interpretation_type=interp_type,
                    interpretation=data.get("interpretation", ""),
                    confidence=data.get("confidence", 0.5),
                ))

        return interpretations

    async def assess_response_depth(
        self,
        response_text: str,
    ) -> ResponseDepth:
        """
        Assess response depth (MC38 Abstraction Level).

        Args:
            response_text: The candidate's response

        Returns:
            ResponseDepth classification
        """
        prompt = f"""Assess the DEPTH of this interview response (MC38 Abstraction Level):

Response: "{response_text}"

SURFACE indicators:
- General statements without specifics
- "Usually I..." or "Typically we..." language
- No names, dates, numbers, or outcomes
- Could apply to anyone

MODERATE indicators:
- Some specific details but gaps
- Mix of general and specific
- Partial examples

DEEP indicators:
- Specific situation with context
- Named people, projects, timeframes
- Concrete actions they personally took
- Measurable outcomes or specific impacts
- Reflection on what they learned

Return JSON: {{"depth": "SURFACE|MODERATE|DEEP", "indicators": ["list of specific indicators observed"], "rationale": "brief explanation"}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You assess response depth. Be strict - DEEP requires genuine specificity.",
            max_tokens=256,
        )

        depth_str = result.get("depth", "SURFACE")
        return ResponseDepth(depth_str) if depth_str in [d.value for d in ResponseDepth] else ResponseDepth.SURFACE

    async def detect_tension_presence(
        self,
        response_text: str,
    ) -> Dict[str, Any]:
        """
        Detect presence of conflict/tension/failure (IP7 pattern).

        Args:
            response_text: The candidate's response

        Returns:
            Dict with tension indicators
        """
        prompt = f"""Analyze this response for conflict/tension/failure presence (IP7 Conflict Exploration):

Response: "{response_text}"

Look for:
1. Interpersonal conflict (disagreement with others)
2. Personal failure (something they did wrong or that didn't work)
3. Challenges overcome (obstacles, difficulties)
4. Difficult decisions (trade-offs, hard choices)
5. Negative outcomes (things that went wrong)

Return JSON:
{{
    "has_conflict": bool,
    "has_failure": bool,
    "has_challenge": bool,
    "has_difficult_decision": bool,
    "has_negative_outcome": bool,
    "overall_tension_present": bool,
    "tension_details": "brief description of tension if present",
    "all_smooth_flag": bool  // true if response is only positive/smooth
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You detect tension and conflict in interview responses. Be thorough.",
            max_tokens=256,
        )

        return result

    def _recommend_follow_ups(
        self,
        star_completeness: Dict[str, bool],
        evidence_type: EvidenceType,
        depth: ResponseDepth,
        tension_present: bool,
        confidence: float,
    ) -> tuple[List[ReasoningPattern], Optional[str]]:
        """
        Recommend follow-up patterns based on analysis.

        Returns:
            Tuple of (recommended patterns, follow-up type)
        """
        patterns = []
        follow_up_type = None

        # Check STAR completeness
        missing = [k for k, v in star_completeness.items() if not v]
        if missing:
            patterns.append(ReasoningPattern.IP3_ACTIVE_LISTENING)
            # Prioritize action > result > situation > task
            priority = ["action", "result", "situation", "task"]
            for component in priority:
                if component in missing:
                    follow_up_type = f"FOLLOW_UP_{component.upper()}"
                    break

        # Check evidence type
        if evidence_type in (EvidenceType.SELF_REPORT, EvidenceType.OPINION):
            patterns.append(ReasoningPattern.IP11_TRUST)
            if not follow_up_type:
                follow_up_type = "FOLLOW_UP_BEHAVIORAL"

        # Check depth
        if depth == ResponseDepth.SURFACE:
            patterns.append(ReasoningPattern.MC38_ABSTRACTION)
            if not follow_up_type:
                follow_up_type = "DEPTH_ESCALATION"

        # Check tension
        if not tension_present:
            patterns.append(ReasoningPattern.IP7_CONFLICT)
            # Only suggest conflict probe if other aspects are covered
            if not follow_up_type and len(missing) == 0:
                follow_up_type = "FOLLOW_UP_CONFLICT"

        # Check confidence
        if confidence < 0.5:
            patterns.append(ReasoningPattern.MC44_SOLUTION_SPACE)

        return patterns, follow_up_type

    def _build_system_prompt(self) -> str:
        """Build system prompt for response analysis."""
        return """You are an expert behavioral interview analyst trained in STAR+ methodology and Universal Reasoning Patterns.

Your role is to analyze candidate responses to:
1. Extract behavioral evidence (specific, past actions with details)
2. Classify evidence types (BEHAVIORAL vs SELF_REPORT vs HYPOTHETICAL)
3. Assess STAR completeness (Situation, Task, Action, Result)
4. Identify omissions and gaps
5. Generate alternative interpretations
6. Detect conflict/tension presence
7. Assess response depth

Key principles:
- BEHAVIORAL evidence requires specifics: names, dates, numbers, outcomes
- Self-reports ("I am a quick learner") are low-value without examples
- Hypotheticals ("I would...") indicate lack of actual experience
- Missing conflict/failure examples may indicate inexperience or avoidance
- Surface responses need depth escalation

Always return valid JSON with all requested fields."""

    def _build_comprehensive_analysis_prompt(
        self,
        response_text: str,
        probe_text: str,
        trait_name: str,
        trait_definition: str,
        behavioral_anchors: Optional[Dict[str, Any]],
        prior_context: Optional[Dict[str, Any]],
    ) -> str:
        """Build comprehensive analysis prompt."""
        anchor_section = ""
        if behavioral_anchors:
            anchor_section = f"""
BEHAVIORAL ANCHORS (for matching evidence to scores):
{self._format_anchors(behavioral_anchors)}
"""

        context_section = ""
        if prior_context:
            context_section = f"""
PRIOR CONTEXT:
- Previous exchanges: {prior_context.get('exchange_count', 0)}
- Evidence collected so far: {prior_context.get('evidence_count', 0)}
- Current confidence: {prior_context.get('confidence', 0):.0%}
"""

        return f"""Perform COMPREHENSIVE analysis of this interview response:

PROBE: "{probe_text}"

RESPONSE: "{response_text}"

TRAIT: {trait_name}
DEFINITION: {trait_definition}
{anchor_section}
{context_section}

Analyze using these patterns:
1. IP11 (Trust Calibration): Classify evidence type
2. IP3 (Active Listening): Identify omissions
3. MC38 (Abstraction Level): Assess depth
4. MC44 (Solution Space): Generate alternatives
5. IP7 (Conflict Exploration): Detect tension

Return JSON:
{{
    "evidence_items": [
        {{
            "source_type": "BEHAVIORAL|SELF_REPORT|HYPOTHETICAL|OPINION",
            "source_text": "quoted text from response",
            "trait_signal": "positive|negative|neutral",
            "signal_strength": float,
            "star_components": {{"situation": bool, "task": bool, "action": bool, "result": bool}},
            "confidence": float,
            "specificity_score": float,
            "contains_conflict": bool,
            "contains_failure": bool,
            "matched_anchors": ["matched behavioral anchor texts"]
        }}
    ],
    "primary_evidence_type": "BEHAVIORAL|SELF_REPORT|HYPOTHETICAL|OPINION",
    "star_completeness": {{"situation": bool, "task": bool, "action": bool, "result": bool}},
    "star_completeness_score": float,
    "response_depth": "SURFACE|MODERATE|DEEP",
    "response_quality": "EXCELLENT|GOOD|ADEQUATE|POOR|UNUSABLE",
    "specificity_score": float,
    "omissions": {{
        "missing_star_components": ["list"],
        "avoided_topics": ["list"],
        "expected_but_absent": ["list"],
        "concerning_absences": ["list"]
    }},
    "alternative_interpretations": [
        {{"type": "favorable|concerning|non_obvious", "interpretation": "...", "confidence": float}}
    ],
    "tension_present": bool,
    "tension_details": "description if present",
    "summary": "brief summary of analysis",
    "overall_confidence": float
}}"""

    def _format_anchors(self, anchors: Dict[str, Any]) -> str:
        """Format behavioral anchors for prompt."""
        lines = []
        for score, data in sorted(anchors.items()):
            if isinstance(data, dict):
                indicators = data.get("indicators", [])
                lines.append(f"Score {score}: {', '.join(indicators[:3])}")
        return "\n".join(lines)

    def _parse_analysis_result(
        self,
        result: Dict[str, Any],
        trait_name: str,
    ) -> ResponseAnalysis:
        """Parse LLM result into ResponseAnalysis."""
        # Parse evidence items
        evidence_items = []
        for item in result.get("evidence_items", []):
            source_type_str = item.get("source_type", "SELF_REPORT")
            try:
                source_type = EvidenceType(source_type_str)
            except ValueError:
                source_type = EvidenceType.SELF_REPORT

            evidence_items.append(ExtractedEvidence(
                source_type=source_type,
                source_text=item.get("source_text", ""),
                weight=EVIDENCE_WEIGHTS.get(source_type, 0.3),
                trait_signals=[{
                    "trait_id": trait_name,
                    "signal": item.get("trait_signal", "neutral"),
                    "strength": item.get("signal_strength", 0.5),
                }],
                star_components=item.get("star_components", {}),
                confidence=item.get("confidence", 0.5),
                specificity_score=item.get("specificity_score", 0.5),
                contains_conflict=item.get("contains_conflict", False),
                contains_failure=item.get("contains_failure", False),
                contains_challenge=item.get("contains_challenge", False),
                matched_anchors=item.get("matched_anchors", []),
            ))

        # Parse primary evidence type
        primary_type_str = result.get("primary_evidence_type", "SELF_REPORT")
        try:
            primary_evidence_type = EvidenceType(primary_type_str)
        except ValueError:
            primary_evidence_type = EvidenceType.SELF_REPORT

        # Parse response depth
        depth_str = result.get("response_depth", "SURFACE")
        try:
            response_depth = ResponseDepth(depth_str)
        except ValueError:
            response_depth = ResponseDepth.SURFACE

        # Parse response quality
        quality_str = result.get("response_quality", "ADEQUATE")
        try:
            response_quality = ResponseQuality(quality_str)
        except ValueError:
            response_quality = ResponseQuality.ADEQUATE

        # Parse STAR completeness
        star_completeness = result.get("star_completeness", {})
        star_score = result.get("star_completeness_score", 0.0)

        # Parse omissions
        omissions_data = result.get("omissions", {})
        omissions = OmissionAnalysis(
            missing_star_components=omissions_data.get("missing_star_components", []),
            avoided_topics=omissions_data.get("avoided_topics", []),
            expected_but_absent=omissions_data.get("expected_but_absent", []),
            concerning_absences=omissions_data.get("concerning_absences", []),
        )

        # Parse alternative interpretations
        alt_interps = []
        for interp in result.get("alternative_interpretations", []):
            alt_interps.append(AlternativeInterpretation(
                interpretation_type=interp.get("type", "non_obvious"),
                interpretation=interp.get("interpretation", ""),
                confidence=interp.get("confidence", 0.5),
            ))

        # Determine tension presence
        tension_present = result.get("tension_present", False)

        # Get recommendations
        confidence = result.get("overall_confidence", 0.5)
        recommended_patterns, follow_up_type = self._recommend_follow_ups(
            star_completeness=star_completeness,
            evidence_type=primary_evidence_type,
            depth=response_depth,
            tension_present=tension_present,
            confidence=confidence,
        )

        return ResponseAnalysis(
            evidence_items=evidence_items,
            primary_evidence_type=primary_evidence_type,
            star_completeness=star_completeness,
            star_completeness_score=star_score,
            response_depth=response_depth,
            response_quality=response_quality,
            specificity_score=result.get("specificity_score", 0.5),
            omissions=omissions,
            alternative_interpretations=alt_interps,
            tension_present=tension_present,
            recommended_follow_up_patterns=recommended_patterns,
            recommended_follow_up_type=follow_up_type,
            summary=result.get("summary", ""),
            confidence=confidence,
        )


# Singleton instance
_response_analyzer: Optional[PatternAwareResponseAnalyzer] = None


def get_response_analyzer() -> PatternAwareResponseAnalyzer:
    """Get the response analyzer instance."""
    global _response_analyzer
    if _response_analyzer is None:
        _response_analyzer = PatternAwareResponseAnalyzer()
    return _response_analyzer
