"""
Trait Extractor Service for extracting behavioral trait signals from top performer sessions.

This service analyzes profiling conversations with top performers to extract
trait signals, evidence, and patterns that can be used to generate
organization-specific scoring rubrics.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.services.llm_client import get_llm_client


@dataclass
class ExtractedSignal:
    """A single trait signal extracted from a response."""
    trait_id: str
    trait_name: str
    signal_type: str  # POSITIVE, NEGATIVE, NEUTRAL
    strength: float  # 0.0 to 1.0
    evidence_text: str
    behavioral_indicator: str
    context: str
    confidence: float


@dataclass
class BehavioralPattern:
    """A behavioral pattern identified across multiple responses."""
    trait_id: str
    trait_name: str
    pattern_description: str
    frequency: str  # ALWAYS, OFTEN, SOMETIMES, RARELY
    example_quotes: List[str]
    implications_for_role: str


@dataclass
class CounterIndicatorSignal:
    """A counter-indicator signal that might predict failure in certain contexts."""
    trait_id: str
    trait_name: str
    context: str
    evidence: str
    role_categories_affected: List[str]
    severity: str  # LOW, MEDIUM, HIGH


@dataclass
class TraitExtractionResult:
    """Complete result of trait extraction from a session."""
    session_id: str
    top_performer_id: str
    extracted_signals: List[ExtractedSignal]
    behavioral_patterns: List[BehavioralPattern]
    counter_indicators: List[CounterIndicatorSignal]
    trait_scores: Dict[str, Dict[str, Any]]  # trait_id -> {score, confidence, evidence_count}
    summary: str
    extraction_metadata: Dict[str, Any]


class TraitExtractor:
    """
    Extracts behavioral trait signals from top performer profiling sessions.

    Uses LLM to analyze conversation transcripts and identify:
    - Trait signals (positive/negative indicators)
    - Behavioral patterns
    - Counter-indicators
    - Evidence quality assessment
    """

    def __init__(self):
        self.llm_client = get_llm_client()

    async def extract_from_response(
        self,
        response_text: str,
        prompt_text: str,
        target_traits: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
    ) -> List[ExtractedSignal]:
        """
        Extract trait signals from a single response.

        Args:
            response_text: The top performer's response
            prompt_text: The prompt that elicited the response
            target_traits: List of traits to look for
            context: Additional context (role, department, etc.)

        Returns:
            List of extracted signals
        """
        traits_info = "\n".join([
            f"- {t['name']}: {t.get('definition', 'No definition')}"
            for t in target_traits
        ])

        system_prompt = """You are an expert organizational psychologist specializing in
behavioral trait extraction. Your task is to analyze a top performer's response
and identify behavioral trait signals.

Focus on:
1. SPECIFIC BEHAVIORS described (not opinions or self-assessments)
2. ACTIONS TAKEN in real situations
3. OUTCOMES achieved and their context
4. DECISION-MAKING patterns revealed
5. How they handled challenges or conflicts

For each signal, assess:
- Signal type: POSITIVE (trait present), NEGATIVE (trait absent/opposite), NEUTRAL
- Strength: 0.0-1.0 based on clarity and specificity of evidence
- Confidence: 0.0-1.0 based on reliability of the indicator"""

        user_prompt = f"""Analyze this response from a top performer and extract trait signals.

PROMPT GIVEN:
{prompt_text}

TOP PERFORMER'S RESPONSE:
{response_text}

TARGET TRAITS TO ASSESS:
{traits_info}

{f"CONTEXT: {json.dumps(context)}" if context else ""}

Extract all relevant trait signals. For each signal, provide:
1. trait_id: The trait identifier
2. trait_name: The trait name
3. signal_type: POSITIVE, NEGATIVE, or NEUTRAL
4. strength: 0.0-1.0
5. evidence_text: The specific quote or behavior
6. behavioral_indicator: What behavior this reveals
7. context: The situation context
8. confidence: 0.0-1.0

Respond with a JSON array of signals. If no clear signals, return empty array."""

        try:
            result = await self.llm_client.complete_structured(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )

            signals = []
            if isinstance(result, list):
                for item in result:
                    signals.append(ExtractedSignal(
                        trait_id=item.get("trait_id", ""),
                        trait_name=item.get("trait_name", ""),
                        signal_type=item.get("signal_type", "NEUTRAL"),
                        strength=float(item.get("strength", 0.5)),
                        evidence_text=item.get("evidence_text", ""),
                        behavioral_indicator=item.get("behavioral_indicator", ""),
                        context=item.get("context", ""),
                        confidence=float(item.get("confidence", 0.5)),
                    ))

            return signals

        except Exception as e:
            # Return empty list on error
            print(f"Error extracting signals: {e}")
            return []

    async def extract_from_session(
        self,
        session_id: str,
        top_performer_id: str,
        transcript: List[Dict[str, Any]],
        target_traits: List[Dict[str, Any]],
        role_context: Optional[Dict[str, Any]] = None,
    ) -> TraitExtractionResult:
        """
        Extract trait signals from an entire profiling session.

        Args:
            session_id: ID of the training session
            top_performer_id: ID of the top performer
            transcript: List of exchanges in the session
            target_traits: List of traits to extract
            role_context: Context about the performer's role

        Returns:
            Complete extraction result
        """
        all_signals: List[ExtractedSignal] = []

        # Extract signals from each response
        for i, exchange in enumerate(transcript):
            if exchange.get("role") == "performer":
                # Find the preceding prompt
                prompt_text = ""
                if i > 0 and transcript[i-1].get("role") == "interviewer":
                    prompt_text = transcript[i-1].get("content", "")

                signals = await self.extract_from_response(
                    response_text=exchange.get("content", ""),
                    prompt_text=prompt_text,
                    target_traits=target_traits,
                    context=role_context,
                )
                all_signals.extend(signals)

        # Identify behavioral patterns across the session
        patterns = await self._identify_patterns(
            all_signals, transcript, target_traits
        )

        # Identify counter-indicators
        counter_indicators = await self._identify_counter_indicators(
            all_signals, transcript, role_context
        )

        # Calculate trait scores
        trait_scores = self._calculate_trait_scores(all_signals, target_traits)

        # Generate session summary
        summary = await self._generate_summary(
            all_signals, patterns, counter_indicators, role_context
        )

        return TraitExtractionResult(
            session_id=session_id,
            top_performer_id=top_performer_id,
            extracted_signals=all_signals,
            behavioral_patterns=patterns,
            counter_indicators=counter_indicators,
            trait_scores=trait_scores,
            summary=summary,
            extraction_metadata={
                "total_exchanges": len(transcript),
                "signals_extracted": len(all_signals),
                "patterns_identified": len(patterns),
                "counter_indicators_found": len(counter_indicators),
            },
        )

    async def _identify_patterns(
        self,
        signals: List[ExtractedSignal],
        transcript: List[Dict[str, Any]],
        target_traits: List[Dict[str, Any]],
    ) -> List[BehavioralPattern]:
        """Identify recurring behavioral patterns across signals."""
        if not signals:
            return []

        # Group signals by trait
        trait_signals: Dict[str, List[ExtractedSignal]] = {}
        for signal in signals:
            if signal.trait_id not in trait_signals:
                trait_signals[signal.trait_id] = []
            trait_signals[signal.trait_id].append(signal)

        system_prompt = """You are an expert at identifying behavioral patterns.
Analyze the trait signals and identify recurring patterns that characterize
how this top performer consistently behaves."""

        signals_summary = []
        for trait_id, trait_sigs in trait_signals.items():
            signals_summary.append({
                "trait_id": trait_id,
                "trait_name": trait_sigs[0].trait_name if trait_sigs else "",
                "signals": [
                    {
                        "type": s.signal_type,
                        "evidence": s.evidence_text,
                        "indicator": s.behavioral_indicator,
                    }
                    for s in trait_sigs
                ]
            })

        user_prompt = f"""Analyze these trait signals and identify behavioral patterns.

TRAIT SIGNALS:
{json.dumps(signals_summary, indent=2)}

For each pattern, provide:
1. trait_id: The trait this pattern relates to
2. trait_name: The trait name
3. pattern_description: Clear description of the behavioral pattern
4. frequency: How often this pattern appears (ALWAYS, OFTEN, SOMETIMES, RARELY)
5. example_quotes: 1-2 specific quotes demonstrating the pattern
6. implications_for_role: What this means for job performance

Respond with a JSON array of patterns."""

        try:
            result = await self.llm_client.complete_structured(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )

            patterns = []
            if isinstance(result, list):
                for item in result:
                    patterns.append(BehavioralPattern(
                        trait_id=item.get("trait_id", ""),
                        trait_name=item.get("trait_name", ""),
                        pattern_description=item.get("pattern_description", ""),
                        frequency=item.get("frequency", "SOMETIMES"),
                        example_quotes=item.get("example_quotes", []),
                        implications_for_role=item.get("implications_for_role", ""),
                    ))

            return patterns

        except Exception as e:
            print(f"Error identifying patterns: {e}")
            return []

    async def _identify_counter_indicators(
        self,
        signals: List[ExtractedSignal],
        transcript: List[Dict[str, Any]],
        role_context: Optional[Dict[str, Any]],
    ) -> List[CounterIndicatorSignal]:
        """Identify potential counter-indicators from signals."""
        # Look for negative signals or patterns that might predict failure
        negative_signals = [s for s in signals if s.signal_type == "NEGATIVE"]

        if not negative_signals:
            return []

        system_prompt = """You are an expert at identifying counter-indicators in
behavioral assessments. Counter-indicators are traits or behaviors that might
predict failure in specific role contexts, even if they're positive in general."""

        negative_evidence = [
            {
                "trait_id": s.trait_id,
                "trait_name": s.trait_name,
                "evidence": s.evidence_text,
                "context": s.context,
            }
            for s in negative_signals
        ]

        user_prompt = f"""Analyze these negative trait signals for potential counter-indicators.

NEGATIVE SIGNALS:
{json.dumps(negative_evidence, indent=2)}

ROLE CONTEXT:
{json.dumps(role_context) if role_context else "Not specified"}

For each counter-indicator, provide:
1. trait_id: The trait involved
2. trait_name: The trait name
3. context: The specific context where this is a concern
4. evidence: The supporting evidence
5. role_categories_affected: Which types of roles would be affected
6. severity: LOW, MEDIUM, or HIGH

Respond with a JSON array. If no clear counter-indicators, return empty array."""

        try:
            result = await self.llm_client.complete_structured(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )

            indicators = []
            if isinstance(result, list):
                for item in result:
                    indicators.append(CounterIndicatorSignal(
                        trait_id=item.get("trait_id", ""),
                        trait_name=item.get("trait_name", ""),
                        context=item.get("context", ""),
                        evidence=item.get("evidence", ""),
                        role_categories_affected=item.get("role_categories_affected", []),
                        severity=item.get("severity", "LOW"),
                    ))

            return indicators

        except Exception as e:
            print(f"Error identifying counter-indicators: {e}")
            return []

    def _normalize_trait_id(self, trait_id: str) -> str:
        """Normalize trait ID for matching: lowercase, replace spaces/underscores."""
        return trait_id.lower().replace("_", " ").replace("-", " ")

    def _calculate_trait_scores(
        self,
        signals: List[ExtractedSignal],
        target_traits: List[Dict[str, Any]],
    ) -> Dict[str, Dict[str, Any]]:
        """Calculate aggregate trait scores from signals."""
        trait_scores: Dict[str, Dict[str, Any]] = {}

        # Build normalized lookup to handle case/underscore variations
        normalized_to_original: Dict[str, str] = {}

        # Initialize all target traits
        for trait in target_traits:
            trait_id = trait.get("id", trait.get("name", ""))
            normalized = self._normalize_trait_id(trait_id)
            normalized_to_original[normalized] = trait_id
            trait_scores[trait_id] = {
                "trait_name": trait.get("name", ""),
                "score": None,
                "confidence": 0.0,
                "evidence_count": 0,
                "positive_signals": 0,
                "negative_signals": 0,
            }

        # Aggregate signals - match using normalized IDs
        for signal in signals:
            normalized_signal_id = self._normalize_trait_id(signal.trait_id)
            original_id = normalized_to_original.get(normalized_signal_id)

            if original_id and original_id in trait_scores:
                scores = trait_scores[original_id]
                scores["evidence_count"] += 1

                if signal.signal_type == "POSITIVE":
                    scores["positive_signals"] += 1
                elif signal.signal_type == "NEGATIVE":
                    scores["negative_signals"] += 1

        # Calculate scores (1-5 scale)
        for trait_id, scores in trait_scores.items():
            if scores["evidence_count"] > 0:
                positive_ratio = scores["positive_signals"] / scores["evidence_count"]
                # Map to 1-5 scale
                scores["score"] = round(1 + (positive_ratio * 4), 1)
                # Confidence based on evidence count
                scores["confidence"] = min(0.95, scores["evidence_count"] * 0.15)

        return trait_scores

    async def _generate_summary(
        self,
        signals: List[ExtractedSignal],
        patterns: List[BehavioralPattern],
        counter_indicators: List[CounterIndicatorSignal],
        role_context: Optional[Dict[str, Any]],
    ) -> str:
        """Generate a summary of the extraction results."""
        if not signals:
            return "No significant trait signals were extracted from this session."

        system_prompt = """You are summarizing trait extraction results for an HR professional.
Be concise but informative. Focus on actionable insights."""

        summary_data = {
            "signal_count": len(signals),
            "pattern_count": len(patterns),
            "counter_indicator_count": len(counter_indicators),
            "top_patterns": [p.pattern_description for p in patterns[:3]],
            "key_counter_indicators": [
                f"{ci.trait_name}: {ci.context}"
                for ci in counter_indicators
            ],
        }

        user_prompt = f"""Summarize these trait extraction results in 2-3 sentences.

EXTRACTION DATA:
{json.dumps(summary_data, indent=2)}

ROLE CONTEXT:
{json.dumps(role_context) if role_context else "Not specified"}

Focus on the most important findings for hiring decisions."""

        try:
            summary = await self.llm_client.complete(
                prompt=user_prompt,
                system_prompt=system_prompt,
                max_tokens=200,
            )
            return summary.strip()

        except Exception as e:
            return f"Extracted {len(signals)} signals and {len(patterns)} patterns from this session."


# Singleton instance
trait_extractor = TraitExtractor()


def get_trait_extractor() -> TraitExtractor:
    """Get the trait extractor instance."""
    return trait_extractor
