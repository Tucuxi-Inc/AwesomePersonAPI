"""
Rubric Generator Service for creating organization-specific scoring rubrics.

This service synthesizes trait extraction results from multiple top performers
to generate customized scoring rubrics that reflect what success actually
looks like in the organization.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.services.llm_client import get_llm_client
from app.services.trait_extractor import (
    TraitExtractionResult,
    BehavioralPattern,
    CounterIndicatorSignal,
)


@dataclass
class BehavioralAnchor:
    """A behavioral anchor for a scoring level."""
    score: int  # 1-5
    description: str
    example_behaviors: List[str]
    evidence_indicators: List[str]


@dataclass
class GeneratedRubricItem:
    """A single trait rubric item generated from profile data."""
    trait_id: str
    trait_name: str
    behavioral_anchors: List[BehavioralAnchor]
    primary_probes: List[str]
    follow_up_probes: List[str]
    star_indicators: Dict[str, List[str]]
    job_relatedness_rationale: str
    derivation_notes: str
    confidence: float


@dataclass
class GeneratedRubric:
    """A complete generated scoring rubric."""
    name: str
    description: str
    organization_id: str
    role_category: str
    items: List[GeneratedRubricItem]
    derivation_metadata: Dict[str, Any]
    research_basis: Optional[str]
    created_at: datetime


class RubricGenerator:
    """
    Generates organization-specific scoring rubrics from top performer profiles.

    The generator:
    1. Synthesizes patterns across multiple top performers
    2. Creates behavioral anchors for each score level (1-5)
    3. Generates probe questions that elicit relevant behaviors
    4. Documents the derivation chain for compliance
    """

    def __init__(self):
        self.llm_client = get_llm_client()

    async def generate_rubric(
        self,
        organization_id: str,
        role_category: str,
        extraction_results: List[TraitExtractionResult],
        target_traits: List[Dict[str, Any]],
        role_context: Optional[Dict[str, Any]] = None,
        base_rubric: Optional[Dict[str, Any]] = None,
    ) -> GeneratedRubric:
        """
        Generate a complete scoring rubric from extraction results.

        Args:
            organization_id: ID of the organization
            role_category: Category of role this rubric is for
            extraction_results: List of extraction results from top performers
            target_traits: List of traits to include in the rubric
            role_context: Additional context about the role
            base_rubric: Optional research-based rubric to start from

        Returns:
            Generated rubric with behavioral anchors and probes
        """
        # Synthesize patterns across all extractions
        synthesized_patterns = self._synthesize_patterns(extraction_results)
        synthesized_scores = self._synthesize_scores(extraction_results)
        synthesized_counter_indicators = self._synthesize_counter_indicators(extraction_results)

        # Generate rubric items for each trait
        rubric_items: List[GeneratedRubricItem] = []

        for trait in target_traits:
            trait_id = trait.get("id", trait.get("name", ""))
            trait_name = trait.get("name", "")

            # Get patterns and scores for this trait
            trait_patterns = synthesized_patterns.get(trait_id, [])
            trait_scores = synthesized_scores.get(trait_id, {})

            # Get base rubric item if available
            base_item = None
            if base_rubric:
                base_items = base_rubric.get("items", [])
                for item in base_items:
                    if item.get("trait_id") == trait_id:
                        base_item = item
                        break

            # Generate rubric item
            rubric_item = await self._generate_rubric_item(
                trait_id=trait_id,
                trait_name=trait_name,
                trait_definition=trait.get("definition", ""),
                patterns=trait_patterns,
                scores=trait_scores,
                role_category=role_category,
                role_context=role_context,
                base_item=base_item,
                extraction_count=len(extraction_results),
            )

            rubric_items.append(rubric_item)

        # Build derivation metadata
        derivation_metadata = {
            "top_performer_count": len(extraction_results),
            "session_ids": [r.session_id for r in extraction_results],
            "patterns_synthesized": sum(len(p) for p in synthesized_patterns.values()),
            "generated_at": datetime.utcnow().isoformat(),
            "role_category": role_category,
            "base_rubric_used": base_rubric is not None,
        }

        # Generate rubric name and description
        name = f"{role_category} Assessment Rubric - {organization_id[:8]}"
        description = await self._generate_rubric_description(
            role_category, rubric_items, len(extraction_results)
        )

        return GeneratedRubric(
            name=name,
            description=description,
            organization_id=organization_id,
            role_category=role_category,
            items=rubric_items,
            derivation_metadata=derivation_metadata,
            research_basis="Derived from top performer profiling with research-validated trait framework",
            created_at=datetime.utcnow(),
        )

    async def _generate_rubric_item(
        self,
        trait_id: str,
        trait_name: str,
        trait_definition: str,
        patterns: List[BehavioralPattern],
        scores: Dict[str, Any],
        role_category: str,
        role_context: Optional[Dict[str, Any]],
        base_item: Optional[Dict[str, Any]],
        extraction_count: int,
    ) -> GeneratedRubricItem:
        """Generate a single rubric item for a trait."""

        # Generate behavioral anchors
        anchors = await self._generate_behavioral_anchors(
            trait_name=trait_name,
            trait_definition=trait_definition,
            patterns=patterns,
            role_category=role_category,
            base_item=base_item,
        )

        # Generate probes
        primary_probes = await self._generate_primary_probes(
            trait_name=trait_name,
            trait_definition=trait_definition,
            patterns=patterns,
            role_context=role_context,
        )

        follow_up_probes = await self._generate_follow_up_probes(
            trait_name=trait_name,
            patterns=patterns,
        )

        # Generate STAR indicators
        star_indicators = self._generate_star_indicators(patterns)

        # Generate job-relatedness rationale
        job_relatedness = await self._generate_job_relatedness(
            trait_name=trait_name,
            role_category=role_category,
            patterns=patterns,
            scores=scores,
        )

        # Derivation notes
        derivation_notes = f"Generated from {extraction_count} top performer(s). "
        if patterns:
            derivation_notes += f"Identified {len(patterns)} behavioral patterns. "
        if base_item:
            derivation_notes += "Augmented with research-based defaults."

        # Calculate confidence based on evidence
        confidence = min(0.95, 0.5 + (extraction_count * 0.1) + (len(patterns) * 0.05))

        return GeneratedRubricItem(
            trait_id=trait_id,
            trait_name=trait_name,
            behavioral_anchors=anchors,
            primary_probes=primary_probes,
            follow_up_probes=follow_up_probes,
            star_indicators=star_indicators,
            job_relatedness_rationale=job_relatedness,
            derivation_notes=derivation_notes,
            confidence=confidence,
        )

    async def _generate_behavioral_anchors(
        self,
        trait_name: str,
        trait_definition: str,
        patterns: List[BehavioralPattern],
        role_category: str,
        base_item: Optional[Dict[str, Any]],
    ) -> List[BehavioralAnchor]:
        """Generate behavioral anchors for scores 1-5."""

        patterns_text = "\n".join([
            f"- {p.pattern_description} (frequency: {p.frequency})"
            for p in patterns[:5]
        ]) if patterns else "No specific patterns extracted"

        base_anchors_text = ""
        if base_item and base_item.get("behavioral_anchors"):
            base_anchors_text = f"\nBASE ANCHORS (from research):\n{json.dumps(base_item['behavioral_anchors'], indent=2)}"

        system_prompt = """You are an expert at creating behavioral scoring rubrics.
Generate clear, observable behavioral anchors for each score level (1-5).

Each anchor should:
- Describe OBSERVABLE behaviors, not attitudes or intentions
- Be specific enough to differentiate between levels
- Reflect the patterns seen in top performers for higher scores
- Be applicable to the role category"""

        user_prompt = f"""Create behavioral anchors for the trait "{trait_name}".

DEFINITION: {trait_definition}
ROLE CATEGORY: {role_category}

PATTERNS FROM TOP PERFORMERS:
{patterns_text}
{base_anchors_text}

For each score (1-5), provide:
1. score: The numeric score
2. description: A brief description of this level
3. example_behaviors: 2-3 specific observable behaviors
4. evidence_indicators: What to look for in responses

Respond with a JSON array of 5 anchors, one for each score level."""

        try:
            result = await self.llm_client.complete_structured(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )

            anchors = []
            if isinstance(result, list):
                for item in result:
                    anchors.append(BehavioralAnchor(
                        score=item.get("score", 1),
                        description=item.get("description", ""),
                        example_behaviors=item.get("example_behaviors", []),
                        evidence_indicators=item.get("evidence_indicators", []),
                    ))

            # Ensure we have all 5 levels
            existing_scores = {a.score for a in anchors}
            for score in range(1, 6):
                if score not in existing_scores:
                    anchors.append(BehavioralAnchor(
                        score=score,
                        description=f"Level {score} performance",
                        example_behaviors=[],
                        evidence_indicators=[],
                    ))

            return sorted(anchors, key=lambda x: x.score)

        except Exception as e:
            print(f"Error generating anchors: {e}")
            # Return basic anchors
            return [
                BehavioralAnchor(
                    score=i,
                    description=f"Level {i} performance for {trait_name}",
                    example_behaviors=[],
                    evidence_indicators=[],
                )
                for i in range(1, 6)
            ]

    async def _generate_primary_probes(
        self,
        trait_name: str,
        trait_definition: str,
        patterns: List[BehavioralPattern],
        role_context: Optional[Dict[str, Any]],
    ) -> List[str]:
        """Generate primary probe questions."""

        system_prompt = """You are an expert at creating behavioral interview questions.
Generate probes that will elicit specific past examples revealing the trait.

Guidelines:
- Ask about SPECIFIC situations from the past
- Focus on behaviors and actions, not opinions
- Make questions role-relevant when possible
- Avoid leading questions or revealing the "right" answer"""

        patterns_text = "\n".join([
            f"- {p.pattern_description}"
            for p in patterns[:3]
        ]) if patterns else "No specific patterns"

        user_prompt = f"""Generate 3 primary probe questions for assessing "{trait_name}".

DEFINITION: {trait_definition}
TOP PERFORMER PATTERNS: {patterns_text}
ROLE CONTEXT: {json.dumps(role_context) if role_context else 'General'}

Respond with a JSON array of 3 question strings."""

        try:
            result = await self.llm_client.complete_structured(
                prompt=user_prompt,
                system_prompt=system_prompt,
            )

            if isinstance(result, list):
                return [str(q) for q in result[:3]]

            return [f"Tell me about a time when you demonstrated {trait_name.lower()}."]

        except Exception:
            return [f"Tell me about a time when you demonstrated {trait_name.lower()}."]

    async def _generate_follow_up_probes(
        self,
        trait_name: str,
        patterns: List[BehavioralPattern],
    ) -> List[str]:
        """Generate follow-up probe questions."""

        follow_ups = [
            "Can you walk me through specifically what you did?",
            "What was going through your mind at that point?",
            "How did others respond to your approach?",
            "What would you do differently if you faced this again?",
            "What was the measurable outcome of your actions?",
        ]

        # If we have patterns, generate more specific follow-ups
        if patterns:
            system_prompt = "Generate follow-up questions to dig deeper into behavioral examples."

            user_prompt = f"""Generate 2 follow-up questions for "{trait_name}" based on these patterns:
{json.dumps([p.pattern_description for p in patterns[:2]])}

Make them specific to these patterns. Respond with JSON array of strings."""

            try:
                result = await self.llm_client.complete_structured(
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                )

                if isinstance(result, list):
                    follow_ups = [str(q) for q in result] + follow_ups[:3]

            except Exception:
                pass

        return follow_ups[:5]

    def _generate_star_indicators(
        self,
        patterns: List[BehavioralPattern],
    ) -> Dict[str, List[str]]:
        """Generate STAR component indicators."""

        indicators = {
            "situation": [
                "Specific context described",
                "Timeframe mentioned",
                "Stakeholders identified",
            ],
            "task": [
                "Clear objective stated",
                "Personal responsibility clarified",
                "Constraints acknowledged",
            ],
            "action": [
                "Specific steps described",
                "Decision rationale explained",
                "Personal contribution clear",
            ],
            "result": [
                "Outcome quantified",
                "Impact described",
                "Lessons articulated",
            ],
        }

        # Enhance with pattern-specific indicators
        for pattern in patterns[:3]:
            if "proactive" in pattern.pattern_description.lower():
                indicators["action"].append("Initiative demonstrated")
            if "collaborat" in pattern.pattern_description.lower():
                indicators["action"].append("Collaboration approach described")
            if "measur" in pattern.pattern_description.lower():
                indicators["result"].append("Metrics referenced")

        return indicators

    async def _generate_job_relatedness(
        self,
        trait_name: str,
        role_category: str,
        patterns: List[BehavioralPattern],
        scores: Dict[str, Any],
    ) -> str:
        """Generate job-relatedness rationale."""

        system_prompt = """Write a clear, defensible rationale for why this trait
is job-related. This will be used for compliance documentation."""

        patterns_text = "; ".join([
            p.implications_for_role for p in patterns[:3]
            if p.implications_for_role
        ]) if patterns else "General performance relevance"

        user_prompt = f"""Write a job-relatedness rationale for "{trait_name}" in {role_category} roles.

EVIDENCE FROM TOP PERFORMERS: {patterns_text}
AVERAGE SCORE IN TOP PERFORMERS: {scores.get('score', 'Not calculated')}

Write 2-3 sentences explaining why this trait is essential for job performance.
Be specific and cite the top performer evidence."""

        try:
            rationale = await self.llm_client.complete(
                prompt=user_prompt,
                system_prompt=system_prompt,
                max_tokens=200,
            )
            return rationale.strip()

        except Exception:
            return f"{trait_name} is essential for {role_category} roles based on patterns observed in top performers."

    async def _generate_rubric_description(
        self,
        role_category: str,
        items: List[GeneratedRubricItem],
        performer_count: int,
    ) -> str:
        """Generate rubric description."""

        trait_names = [item.trait_name for item in items[:5]]

        return (
            f"Assessment rubric for {role_category} roles, derived from profiling "
            f"{performer_count} top performer(s). Covers {len(items)} traits including "
            f"{', '.join(trait_names)}. Each trait includes behavioral anchors calibrated "
            "to observed patterns and research-validated frameworks."
        )

    def _synthesize_patterns(
        self,
        results: List[TraitExtractionResult],
    ) -> Dict[str, List[BehavioralPattern]]:
        """Synthesize patterns across multiple extractions."""
        patterns_by_trait: Dict[str, List[BehavioralPattern]] = {}

        for result in results:
            for pattern in result.behavioral_patterns:
                if pattern.trait_id not in patterns_by_trait:
                    patterns_by_trait[pattern.trait_id] = []
                patterns_by_trait[pattern.trait_id].append(pattern)

        return patterns_by_trait

    def _synthesize_scores(
        self,
        results: List[TraitExtractionResult],
    ) -> Dict[str, Dict[str, Any]]:
        """Synthesize scores across multiple extractions."""
        scores_by_trait: Dict[str, List[Dict[str, Any]]] = {}

        for result in results:
            for trait_id, scores in result.trait_scores.items():
                if trait_id not in scores_by_trait:
                    scores_by_trait[trait_id] = []
                scores_by_trait[trait_id].append(scores)

        # Calculate averages
        synthesized = {}
        for trait_id, score_list in scores_by_trait.items():
            valid_scores = [s["score"] for s in score_list if s.get("score") is not None]
            if valid_scores:
                synthesized[trait_id] = {
                    "score": sum(valid_scores) / len(valid_scores),
                    "count": len(valid_scores),
                    "confidence": sum(s.get("confidence", 0) for s in score_list) / len(score_list),
                }

        return synthesized

    def _synthesize_counter_indicators(
        self,
        results: List[TraitExtractionResult],
    ) -> List[CounterIndicatorSignal]:
        """Synthesize counter-indicators across extractions."""
        all_indicators: List[CounterIndicatorSignal] = []

        for result in results:
            all_indicators.extend(result.counter_indicators)

        return all_indicators


# Singleton instance
rubric_generator = RubricGenerator()


def get_rubric_generator() -> RubricGenerator:
    """Get the rubric generator instance."""
    return rubric_generator
