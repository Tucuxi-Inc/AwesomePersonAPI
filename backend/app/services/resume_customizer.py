"""
Resume-informed probe customizer for anchoring questions to candidate experience.

This module customizes generic interview probes using specific resume details
to make questions impossible to answer with rehearsed responses and to ground
the conversation in the candidate's actual experience.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.services.llm_client import get_llm_client


@dataclass
class ResumeElement:
    """An element extracted from a resume."""
    element_type: str  # job_transition, project, leadership, skill_growth, etc.
    description: str
    company: Optional[str] = None
    timeframe: Optional[str] = None
    relevance_to_traits: List[str] = field(default_factory=list)


@dataclass
class ProbeCustomization:
    """A customized probe with resume anchors."""
    original_probe: str
    customized_probe: str
    resume_anchors: List[str]
    customization_rationale: str
    trait_id: str


@dataclass
class ResumeProbeOpportunity:
    """An opportunity to create a resume-anchored probe."""
    trait_id: str
    trait_name: str
    resume_element: ResumeElement
    suggested_probe_angle: str
    strength: float  # How strong this opportunity is (0-1)


class ResumeInformedProbeCustomizer:
    """
    Customizes interview probes using candidate resume details.

    This service:
    - Extracts probe-relevant elements from resumes
    - Maps resume elements to trait assessment opportunities
    - Transforms generic probes into resume-anchored questions
    - Ensures questions cannot be answered with rehearsed responses
    """

    # Mapping of resume elements to relevant traits
    ELEMENT_TRAIT_MAP = {
        "job_transition": ["ADAPTABILITY", "RESILIENCE", "LEARNING_ORIENTATION"],
        "promotion": ["INITIATIVE", "ACHIEVEMENT_ORIENTATION", "INFLUENCE"],
        "leadership_role": ["COLLABORATION", "ASSERTIVENESS", "INFLUENCE"],
        "cross_functional": ["COLLABORATION", "EMPATHY", "CONFLICT_TOLERANCE"],
        "project_pivot": ["ADAPTABILITY", "RESILIENCE", "AMBIGUITY_TOLERANCE"],
        "skill_acquisition": ["CURIOSITY", "LEARNING_ORIENTATION", "INITIATIVE"],
        "failure_recovery": ["RESILIENCE", "ACCOUNTABILITY", "SELF_AWARENESS"],
        "team_building": ["COLLABORATION", "EMPATHY", "SERVICE_ORIENTATION"],
        "process_improvement": ["INITIATIVE", "ANALYTICAL_THINKING", "STRATEGIC_THINKING"],
        "crisis_management": ["STRESS_TOLERANCE", "EMOTIONAL_REGULATION", "URGENCY"],
        "innovation": ["CREATIVITY", "CURIOSITY", "RISK_ORIENTATION"],
        "mentorship": ["EMPATHY", "SERVICE_ORIENTATION", "COLLABORATION"],
    }

    def __init__(self):
        self.llm_client = get_llm_client()

    async def extract_resume_elements(
        self,
        resume_text: str,
    ) -> List[ResumeElement]:
        """
        Extract probe-relevant elements from a resume.

        Args:
            resume_text: The full resume text or summary

        Returns:
            List of ResumeElements suitable for probe customization
        """
        prompt = f"""Analyze this resume and extract elements that can be used to customize behavioral interview questions.

RESUME:
{resume_text}

Extract elements in these categories:
1. Job transitions (role changes, company changes, career pivots)
2. Promotions or increased responsibility
3. Leadership roles or team management
4. Cross-functional work or collaboration
5. Project pivots or strategy changes
6. New skill acquisition or learning
7. Challenging situations or failures mentioned
8. Team building or hiring
9. Process improvements or innovations
10. Crisis or high-pressure situations

For each element, identify:
- Type of element
- Description (specific enough to reference in a question)
- Company/context
- Timeframe if available
- Which traits this could help assess

Return JSON:
{{
    "elements": [
        {{
            "element_type": "job_transition|promotion|leadership_role|cross_functional|project_pivot|skill_acquisition|failure_recovery|team_building|process_improvement|crisis_management|innovation|mentorship",
            "description": "specific description",
            "company": "company name or null",
            "timeframe": "timeframe or null",
            "relevance_to_traits": ["TRAIT1", "TRAIT2"]
        }}
    ]
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You extract interview-relevant elements from resumes. Be specific - vague elements can't be used in questions.",
            max_tokens=1024,
        )

        elements = []
        for item in result.get("elements", []):
            # Enhance trait relevance using our mapping
            element_type = item.get("element_type", "")
            base_traits = self.ELEMENT_TRAIT_MAP.get(element_type, [])
            mentioned_traits = item.get("relevance_to_traits", [])
            all_traits = list(set(base_traits + mentioned_traits))

            elements.append(ResumeElement(
                element_type=element_type,
                description=item.get("description", ""),
                company=item.get("company"),
                timeframe=item.get("timeframe"),
                relevance_to_traits=all_traits,
            ))

        return elements

    async def identify_probe_opportunities(
        self,
        resume_elements: List[ResumeElement],
        target_traits: List[str],
    ) -> List[ResumeProbeOpportunity]:
        """
        Identify opportunities to create resume-anchored probes.

        Args:
            resume_elements: Elements extracted from resume
            target_traits: List of trait IDs we want to assess

        Returns:
            List of probe opportunities sorted by strength
        """
        opportunities = []

        for element in resume_elements:
            # Find matching traits
            matching_traits = [
                t for t in target_traits
                if t.upper() in [r.upper() for r in element.relevance_to_traits]
            ]

            for trait in matching_traits:
                # Calculate strength based on element specificity
                strength = self._calculate_opportunity_strength(element)

                opportunities.append(ResumeProbeOpportunity(
                    trait_id=trait,
                    trait_name=trait.replace("_", " ").title(),
                    resume_element=element,
                    suggested_probe_angle=self._suggest_probe_angle(element, trait),
                    strength=strength,
                ))

        # Sort by strength
        opportunities.sort(key=lambda x: x.strength, reverse=True)
        return opportunities

    async def customize_probe(
        self,
        generic_probe: str,
        trait_id: str,
        trait_name: str,
        resume_elements: List[ResumeElement],
        max_anchors: int = 2,
    ) -> ProbeCustomization:
        """
        Customize a generic probe using resume elements.

        Args:
            generic_probe: The generic interview probe
            trait_id: The trait being assessed
            trait_name: Human-readable trait name
            resume_elements: Available resume elements
            max_anchors: Maximum number of resume anchors to use

        Returns:
            ProbeCustomization with the customized probe
        """
        # Find relevant elements for this trait
        relevant_elements = [
            e for e in resume_elements
            if trait_id.upper() in [r.upper() for r in e.relevance_to_traits]
        ][:max_anchors]

        if not relevant_elements:
            # No relevant elements - return original probe
            return ProbeCustomization(
                original_probe=generic_probe,
                customized_probe=generic_probe,
                resume_anchors=[],
                customization_rationale="No relevant resume elements found",
                trait_id=trait_id,
            )

        # Build customization prompt
        elements_text = "\n".join([
            f"- {e.element_type}: {e.description} ({e.company or 'unknown company'}, {e.timeframe or 'unknown time'})"
            for e in relevant_elements
        ])

        prompt = f"""Transform this generic interview probe into a RESUME-ANCHORED question.

GENERIC PROBE: "{generic_probe}"

TRAIT: {trait_name}

CANDIDATE'S RESUME ELEMENTS:
{elements_text}

Create a customized probe that:
1. References SPECIFIC details from the resume (company names, role transitions, projects)
2. Makes the question impossible to answer with a rehearsed response
3. Maintains focus on the trait ({trait_name})
4. Feels natural and conversational
5. Invites a SPECIFIC behavioral example

Example transformation:
- Generic: "Tell me about a time you adapted to change"
- Customized: "You moved from the Kindle team to Echo at Amazon. Tell me about a specific moment during that transition when your usual approach wasn't working and you had to adapt."

Return JSON:
{{
    "customized_probe": "your customized question",
    "resume_anchors": ["specific resume elements referenced"],
    "customization_rationale": "why this approach"
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You customize interview questions using resume details. Make questions specific and impossible to answer with generic rehearsed answers.",
            max_tokens=512,
        )

        return ProbeCustomization(
            original_probe=generic_probe,
            customized_probe=result.get("customized_probe", generic_probe),
            resume_anchors=result.get("resume_anchors", []),
            customization_rationale=result.get("customization_rationale", ""),
            trait_id=trait_id,
        )

    async def generate_resume_based_probe(
        self,
        trait_id: str,
        trait_name: str,
        trait_definition: str,
        resume_element: ResumeElement,
    ) -> ProbeCustomization:
        """
        Generate a completely new probe based on a resume element.

        Unlike customize_probe which transforms a generic probe, this
        creates a new probe from scratch based on the resume element.

        Args:
            trait_id: The trait to assess
            trait_name: Human-readable trait name
            trait_definition: Definition of the trait
            resume_element: The resume element to base the probe on

        Returns:
            ProbeCustomization with the new probe
        """
        prompt = f"""Generate a behavioral interview probe based on this resume element.

TRAIT TO ASSESS: {trait_name}
TRAIT DEFINITION: {trait_definition}

RESUME ELEMENT:
- Type: {resume_element.element_type}
- Description: {resume_element.description}
- Company: {resume_element.company or 'Not specified'}
- Timeframe: {resume_element.timeframe or 'Not specified'}

Create a probe that:
1. Directly references this specific experience
2. Targets the trait ({trait_name})
3. Asks for a SPECIFIC behavioral example
4. Cannot be answered with a rehearsed response
5. Uses "Tell me about..." or "Walk me through..." format

Return JSON:
{{
    "probe": "your behavioral interview probe",
    "probe_angle": "what aspect of the trait this targets",
    "expected_response_elements": ["what a good answer should include"]
}}"""

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt="You generate targeted behavioral interview probes based on resume details.",
            max_tokens=512,
        )

        return ProbeCustomization(
            original_probe="[Generated from resume element]",
            customized_probe=result.get("probe", f"Tell me about your experience with {resume_element.description}"),
            resume_anchors=[resume_element.description],
            customization_rationale=result.get("probe_angle", ""),
            trait_id=trait_id,
        )

    def _calculate_opportunity_strength(self, element: ResumeElement) -> float:
        """Calculate the strength of a probe opportunity."""
        strength = 0.5  # Base strength

        # Boost for specific company mention
        if element.company:
            strength += 0.15

        # Boost for timeframe
        if element.timeframe:
            strength += 0.1

        # Boost for description length (more specific)
        if len(element.description) > 50:
            strength += 0.15
        elif len(element.description) > 25:
            strength += 0.1

        # Boost for certain element types (higher signal)
        high_signal_types = ["job_transition", "failure_recovery", "crisis_management", "project_pivot"]
        if element.element_type in high_signal_types:
            strength += 0.1

        return min(strength, 1.0)

    def _suggest_probe_angle(self, element: ResumeElement, trait_id: str) -> str:
        """Suggest a probe angle based on element and trait."""
        angles = {
            ("job_transition", "ADAPTABILITY"): "How they adjusted during the transition",
            ("job_transition", "RESILIENCE"): "Challenges faced during the change",
            ("promotion", "INITIATIVE"): "What they did to earn the promotion",
            ("leadership_role", "COLLABORATION"): "How they built and led the team",
            ("cross_functional", "EMPATHY"): "Understanding different perspectives",
            ("project_pivot", "AMBIGUITY_TOLERANCE"): "Handling uncertainty during pivot",
            ("skill_acquisition", "CURIOSITY"): "What drove them to learn",
            ("failure_recovery", "ACCOUNTABILITY"): "Taking responsibility and learning",
            ("crisis_management", "STRESS_TOLERANCE"): "Staying effective under pressure",
        }

        key = (element.element_type, trait_id.upper())
        return angles.get(key, f"Demonstrating {trait_id.lower().replace('_', ' ')} in this context")


# Singleton instance
_resume_customizer: Optional[ResumeInformedProbeCustomizer] = None


def get_resume_customizer() -> ResumeInformedProbeCustomizer:
    """Get the resume customizer instance."""
    global _resume_customizer
    if _resume_customizer is None:
        _resume_customizer = ResumeInformedProbeCustomizer()
    return _resume_customizer
