"""Job Description Analyzer service.

Uses LLM to extract objective requirements, nice-to-haves, responsibilities,
and suggested traits from job descriptions.
"""

import uuid
from typing import List, Dict, Any

from app.services.llm_client import get_llm_client
from app.schemas.job import ExtractedRequirements


EXTRACTION_SYSTEM_PROMPT = """You are an expert HR analyst and job requirements specialist.

Your task is to analyze job descriptions and extract structured information that will be used
to screen candidate resumes. Focus on:

1. OBJECTIVE REQUIREMENTS: These are hard requirements that can be objectively verified from a resume.
   - Education requirements (degrees, fields of study)
   - Years of experience (specific numbers)
   - Required certifications or licenses
   - Required technical skills (specific technologies, tools, languages)
   - Required domain knowledge (e.g., "healthcare industry experience")

2. NICE-TO-HAVES: Preferred but not required qualifications
   - Preferred skills or experience
   - "Plus" items mentioned in the description
   - Industry preferences that aren't strict requirements

3. RESPONSIBILITIES: Key duties and responsibilities of the role
   - Main functions they'll perform
   - Teams or stakeholders they'll work with
   - Scope of the role

4. SUGGESTED TRAITS: Based on the responsibilities, suggest which personality/behavioral traits
   would be important to assess. Choose from this list:
   - CURIOSITY (desire to learn and explore)
   - ANALYTICAL_THINKING (logical problem-solving)
   - CREATIVITY (innovative thinking)
   - DETAIL_ORIENTATION (precision and thoroughness)
   - STRATEGIC_THINKING (long-term planning)
   - COLLABORATION (teamwork)
   - ASSERTIVENESS (confidence in communication)
   - EMPATHY (understanding others)
   - INFLUENCE (persuasion ability)
   - CONFLICT_TOLERANCE (handling disagreements)
   - INITIATIVE (self-starting)
   - CONSISTENCY (reliable performance)
   - URGENCY (pace and deadlines)
   - PERFECTIONISM (quality standards)
   - FOLLOW_THROUGH (completion)
   - RESILIENCE (handling setbacks)
   - STRESS_TOLERANCE (pressure handling)
   - EMOTIONAL_REGULATION (composure)
   - AMBIGUITY_TOLERANCE (handling uncertainty)
   - ADAPTABILITY (flexibility)
   - INDEPENDENCE (autonomous work)
   - SELF_AWARENESS (knowing own strengths/weaknesses)
   - ACCOUNTABILITY (ownership)

Be specific and extract exact requirements from the text. If a requirement is implied but not explicit,
note it as a nice-to-have rather than an objective requirement.

For objective requirements, be conservative - only include things that are clearly stated as required,
not preferred or nice-to-have items."""


EXTRACTION_PROMPT_TEMPLATE = """Analyze this job posting and extract structured requirements.

JOB TITLE: {job_title}

JOB DESCRIPTION:
{job_description}

Extract and return a JSON object with this exact structure:
{{
    "objective_requirements": [
        {{
            "id": "<unique-uuid>",
            "type": "education|experience|certification|skill|other",
            "requirement": "<specific requirement text>",
            "required": true
        }}
    ],
    "nice_to_haves": [
        {{
            "description": "<nice-to-have item>"
        }}
    ],
    "responsibilities": [
        "<responsibility 1>",
        "<responsibility 2>"
    ],
    "suggested_traits": [
        "TRAIT_NAME_1",
        "TRAIT_NAME_2"
    ]
}}

Guidelines:
- For objective_requirements, generate a UUID for each id field
- type should be one of: education, experience, certification, skill, other
- Only mark as "required": true if explicitly required in the description
- suggested_traits should be 3-6 traits most relevant to the role
- Be specific and extract exact language where possible"""


class JobDescriptionAnalyzer:
    """Analyzes job descriptions to extract structured requirements."""

    def __init__(self):
        self.llm_client = get_llm_client()

    async def extract_requirements(
        self,
        job_title: str,
        job_description: str,
    ) -> ExtractedRequirements:
        """
        Extract structured requirements from a job description.

        Args:
            job_title: The job title
            job_description: The full job description text

        Returns:
            ExtractedRequirements with objective_requirements, nice_to_haves,
            responsibilities, and suggested_traits
        """
        prompt = EXTRACTION_PROMPT_TEMPLATE.format(
            job_title=job_title,
            job_description=job_description,
        )

        result = await self.llm_client.complete_structured(
            prompt=prompt,
            system_prompt=EXTRACTION_SYSTEM_PROMPT,
            max_tokens=4096,
        )

        # Validate and clean up the result
        objective_requirements = self._clean_requirements(
            result.get("objective_requirements", [])
        )
        nice_to_haves = result.get("nice_to_haves", [])
        responsibilities = result.get("responsibilities", [])
        suggested_traits = self._validate_traits(result.get("suggested_traits", []))

        return ExtractedRequirements(
            objective_requirements=objective_requirements,
            nice_to_haves=nice_to_haves,
            responsibilities=responsibilities,
            suggested_traits=suggested_traits,
            extraction_notes="claude-sonnet-4-20250514",
        )

    def _clean_requirements(
        self, requirements: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Ensure all requirements have valid IDs and required fields."""
        cleaned = []
        valid_types = {"education", "experience", "certification", "skill", "other"}

        for req in requirements:
            # Ensure ID exists
            if "id" not in req or not req["id"]:
                req["id"] = str(uuid.uuid4())

            # Validate type
            if req.get("type") not in valid_types:
                req["type"] = "other"

            # Ensure required fields
            if "requirement" not in req:
                continue  # Skip invalid requirements

            if "required" not in req:
                req["required"] = True

            cleaned.append(req)

        return cleaned

    def _validate_traits(self, traits: List[str]) -> List[str]:
        """Validate that traits are from the allowed list."""
        valid_traits = {
            "CURIOSITY",
            "ANALYTICAL_THINKING",
            "CREATIVITY",
            "DETAIL_ORIENTATION",
            "STRATEGIC_THINKING",
            "COLLABORATION",
            "ASSERTIVENESS",
            "EMPATHY",
            "INFLUENCE",
            "CONFLICT_TOLERANCE",
            "INITIATIVE",
            "CONSISTENCY",
            "URGENCY",
            "PERFECTIONISM",
            "FOLLOW_THROUGH",
            "RESILIENCE",
            "STRESS_TOLERANCE",
            "EMOTIONAL_REGULATION",
            "AMBIGUITY_TOLERANCE",
            "ADAPTABILITY",
            "INDEPENDENCE",
            "SELF_AWARENESS",
            "ACCOUNTABILITY",
        }

        return [t.upper() for t in traits if t.upper() in valid_traits]
