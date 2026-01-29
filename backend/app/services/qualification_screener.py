"""Qualification Screener service for comparing resumes against job requirements."""

import logging
from typing import Any, Dict, List, Tuple

from app.services.llm_client import get_llm_client

logger = logging.getLogger(__name__)


SCREENING_SYSTEM_PROMPT = """You are an expert HR qualification screener. Your task is to compare a candidate's resume against job requirements.

Be fair and objective. Focus on the requirements as stated, not on making assumptions.
- MET: The resume clearly shows the candidate meets this requirement
- NOT_MET: The resume clearly shows the candidate does NOT meet this requirement
- UNCLEAR: The information is ambiguous or not clearly present

For experience requirements, check both total years and relevance of experience.
For education requirements, consider equivalent experience when appropriate.
For skill requirements, look for direct mentions or related technologies/tools.

Always provide specific evidence from the resume to support your assessment."""


SCREENING_PROMPT = """Compare this candidate's resume against the job requirements.

<job_requirements>
{requirements_json}
</job_requirements>

<parsed_resume>
{resume_json}
</parsed_resume>

For each requirement, determine if the candidate meets it based on the resume.

Return a JSON object with this exact structure:
{{
    "results": [
        {{
            "requirement_id": "The requirement ID from the input",
            "requirement_text": "The requirement text",
            "requirement_type": "education/experience/certification/skill",
            "required": true/false,
            "status": "MET" or "NOT_MET" or "UNCLEAR",
            "evidence": "Specific text or data from the resume that supports this assessment",
            "explanation": "Brief explanation of why this status was determined"
        }}
    ],
    "overall_assessment": {{
        "qualification_status": "QUALIFIED" or "NOT_QUALIFIED" or "NEEDS_REVIEW",
        "summary": "Brief summary of the candidate's overall qualification",
        "strengths": ["List of areas where candidate is strong"],
        "gaps": ["List of areas where candidate falls short"]
    }}
}}

Qualification Status Rules:
- QUALIFIED: All required requirements are MET
- NOT_QUALIFIED: Any required requirement is NOT_MET
- NEEDS_REVIEW: All required requirements are either MET or UNCLEAR (none NOT_MET)"""


class QualificationScreener:
    """Service for screening candidates against job requirements."""

    def __init__(self):
        self.llm = get_llm_client()

    async def screen(
        self,
        parsed_resume: Dict[str, Any],
        job_requirements: List[Dict[str, Any]],
    ) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Screen a candidate's resume against job requirements.

        Args:
            parsed_resume: Structured resume data from ResumeAnalyzer
            job_requirements: List of job requirements with id, type, requirement, required

        Returns:
            Tuple of (qualification_status, requirement_results, gaps)
        """
        if not job_requirements:
            # No requirements = automatically qualified
            return "QUALIFIED", [], []

        # Prepare data for LLM
        requirements_json = self._format_requirements(job_requirements)
        resume_json = self._format_resume(parsed_resume)

        prompt = SCREENING_PROMPT.format(
            requirements_json=requirements_json,
            resume_json=resume_json,
        )

        try:
            result = await self.llm.complete_structured(
                prompt=prompt,
                system_prompt=SCREENING_SYSTEM_PROMPT,
                max_tokens=4096,
            )

            # Extract and validate results
            return self._process_results(result, job_requirements)

        except Exception as e:
            logger.error(f"Error during qualification screening: {e}")
            raise

    def _format_requirements(self, requirements: List[Dict[str, Any]]) -> str:
        """Format requirements for the prompt."""
        formatted = []
        for req in requirements:
            formatted.append({
                "id": req.get("id", ""),
                "type": req.get("type", "skill"),
                "requirement": req.get("requirement", ""),
                "required": req.get("required", True),
            })
        import json
        return json.dumps(formatted, indent=2)

    def _format_resume(self, resume: Dict[str, Any]) -> str:
        """Format resume data for the prompt."""
        # Create a condensed version for the LLM
        summary = {
            "contact": resume.get("contact", {}),
            "summary": resume.get("summary"),
            "total_years_experience": resume.get("total_years_experience"),
            "experience": [
                {
                    "company": exp.get("company"),
                    "title": exp.get("title"),
                    "duration_months": exp.get("duration_months"),
                    "start_date": exp.get("start_date"),
                    "end_date": exp.get("end_date"),
                    "achievements": exp.get("achievements", [])[:3],  # Limit achievements
                }
                for exp in (resume.get("experience") or [])[:5]  # Limit to 5 most recent
            ],
            "education": resume.get("education", []),
            "skills": resume.get("skills", []),
            "certifications": resume.get("certifications", []),
        }
        import json
        return json.dumps(summary, indent=2)

    def _process_results(
        self,
        llm_result: Dict[str, Any],
        original_requirements: List[Dict[str, Any]],
    ) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Process LLM results and determine final status."""
        results = llm_result.get("results", [])
        overall = llm_result.get("overall_assessment", {})

        # Build requirement results
        requirement_results = []
        for result in results:
            requirement_results.append({
                "requirement_id": result.get("requirement_id", ""),
                "requirement_text": result.get("requirement_text", ""),
                "requirement_type": result.get("requirement_type", ""),
                "required": result.get("required", True),
                "status": result.get("status", "UNCLEAR"),
                "evidence": result.get("evidence"),
                "explanation": result.get("explanation", ""),
            })

        # Determine qualification status based on rules
        status = self._determine_status(requirement_results)

        # Build gaps list
        gaps = []
        for result in requirement_results:
            if result["status"] == "NOT_MET" and result.get("required", True):
                gaps.append({
                    "requirement_id": result["requirement_id"],
                    "requirement": result["requirement_text"],
                    "requirement_type": result["requirement_type"],
                    "explanation": result["explanation"],
                })

        # Also add gaps from LLM assessment if they add context
        llm_gaps = overall.get("gaps", [])
        for gap in llm_gaps:
            if isinstance(gap, str) and gap not in [g["requirement"] for g in gaps]:
                gaps.append({
                    "requirement_id": "",
                    "requirement": gap,
                    "requirement_type": "general",
                    "explanation": gap,
                })

        return status, requirement_results, gaps

    def _determine_status(self, requirement_results: List[Dict[str, Any]]) -> str:
        """
        Determine overall qualification status based on requirement results.

        Rules:
        - QUALIFIED: All required requirements are MET
        - NOT_QUALIFIED: Any required requirement is NOT_MET
        - NEEDS_REVIEW: All required requirements are either MET or UNCLEAR
        """
        required_results = [r for r in requirement_results if r.get("required", True)]

        if not required_results:
            return "QUALIFIED"

        has_not_met = any(r["status"] == "NOT_MET" for r in required_results)
        has_unclear = any(r["status"] == "UNCLEAR" for r in required_results)
        all_met = all(r["status"] == "MET" for r in required_results)

        if has_not_met:
            return "NOT_QUALIFIED"
        elif all_met:
            return "QUALIFIED"
        elif has_unclear:
            return "NEEDS_REVIEW"
        else:
            return "QUALIFIED"

    async def quick_screen(
        self,
        parsed_resume: Dict[str, Any],
        job_requirements: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Perform a quick rule-based screen without LLM (for basic checks).

        This is a fast preliminary check before the full LLM-based screening.
        """
        results = []
        gaps = []

        for req in job_requirements:
            req_type = req.get("type", "skill")
            req_text = req.get("requirement", "").lower()
            required = req.get("required", True)

            status = "UNCLEAR"
            evidence = None
            explanation = "Requires manual review"

            # Basic experience check
            if req_type == "experience":
                # Look for years pattern
                import re
                years_match = re.search(r"(\d+)\+?\s*years?", req_text)
                if years_match:
                    required_years = int(years_match.group(1))
                    resume_years = parsed_resume.get("total_years_experience") or 0
                    if resume_years >= required_years:
                        status = "MET"
                        evidence = f"Resume shows {resume_years} years of experience"
                        explanation = f"Candidate has {resume_years} years, meets {required_years}+ requirement"
                    else:
                        status = "NOT_MET"
                        evidence = f"Resume shows {resume_years} years of experience"
                        explanation = f"Candidate has {resume_years} years, below {required_years}+ requirement"

            # Basic education check
            elif req_type == "education":
                education = parsed_resume.get("education", [])
                degree_keywords = ["bachelor", "master", "phd", "doctorate", "associate", "bs", "ba", "ms", "ma", "mba"]
                has_degree = any(
                    any(kw in (edu.get("degree") or "").lower() for kw in degree_keywords)
                    for edu in education
                )
                if has_degree:
                    status = "MET" if "degree" in req_text.lower() else "UNCLEAR"
                    evidence = f"Education: {education[0].get('degree', '')} from {education[0].get('institution', '')}" if education else None

            # Basic skill check
            elif req_type == "skill":
                skills = [s.lower() for s in (parsed_resume.get("skills") or [])]
                # Check if the main skill keyword appears in resume skills
                skill_found = any(
                    word in skill for word in req_text.split() for skill in skills
                    if len(word) > 2  # Skip short words
                )
                if skill_found:
                    status = "MET"
                    evidence = f"Skills found: {', '.join(skills[:5])}"
                    explanation = "Skill mentioned in resume"

            results.append({
                "requirement_id": req.get("id", ""),
                "requirement_text": req.get("requirement", ""),
                "requirement_type": req_type,
                "required": required,
                "status": status,
                "evidence": evidence,
                "explanation": explanation,
            })

            if status == "NOT_MET" and required:
                gaps.append({
                    "requirement_id": req.get("id", ""),
                    "requirement": req.get("requirement", ""),
                    "requirement_type": req_type,
                    "explanation": explanation,
                })

        qualification_status = self._determine_status(results)

        return {
            "qualification_status": qualification_status,
            "requirement_results": results,
            "gaps": gaps,
            "gap_count": len(gaps),
        }


# Singleton instance
qualification_screener = QualificationScreener()


def get_qualification_screener() -> QualificationScreener:
    """Get the qualification screener instance."""
    return qualification_screener
