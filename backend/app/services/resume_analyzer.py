"""Resume Analyzer service for extracting structured data using LLM."""

import logging
from typing import Any, Dict, Optional

from app.services.llm_client import get_llm_client

logger = logging.getLogger(__name__)


RESUME_ANALYSIS_SYSTEM_PROMPT = """You are an expert resume parser and analyzer. Your task is to extract structured information from resume text.

Be thorough and accurate. If information is not clearly present, leave the field as null or an empty list.
For dates, use ISO format (YYYY-MM) when possible, or descriptive text if exact dates aren't clear.
Calculate total years of experience by summing up work experience durations.

Always respond with valid JSON matching the requested schema."""


RESUME_EXTRACTION_PROMPT = """Extract structured information from this resume text:

<resume>
{resume_text}
</resume>

Return a JSON object with this exact structure:
{{
    "contact": {{
        "name": "Full name if found",
        "email": "Email if found",
        "phone": "Phone if found",
        "location": "Location/address if found",
        "linkedin": "LinkedIn URL if found"
    }},
    "summary": "Professional summary or objective if present, otherwise null",
    "experience": [
        {{
            "company": "Company name",
            "title": "Job title",
            "start_date": "Start date (YYYY-MM or descriptive)",
            "end_date": "End date or 'Present'",
            "duration_months": <estimated months as integer>,
            "description": "Role description if available",
            "achievements": ["List of achievements or responsibilities"]
        }}
    ],
    "education": [
        {{
            "institution": "School/University name",
            "degree": "Degree type (e.g., Bachelor's, Master's)",
            "field_of_study": "Major or field",
            "graduation_year": <year as integer or null>,
            "gpa": "GPA if listed"
        }}
    ],
    "skills": ["List of technical and professional skills mentioned"],
    "certifications": [
        {{
            "name": "Certification name",
            "issuer": "Issuing organization",
            "issue_date": "Date obtained",
            "expiration_date": "Expiration if applicable"
        }}
    ],
    "languages": ["Languages spoken if mentioned"],
    "total_years_experience": <estimated total years as a decimal number>
}}

Important:
- Extract all work experience entries, ordered from most recent to oldest
- For experience duration, estimate months even if only years are given
- Include ALL skills mentioned, including tools, technologies, and soft skills
- If a field is not found in the resume, use null for single values or [] for arrays"""


class ResumeAnalyzer:
    """Service for analyzing resume content and extracting structured data using LLM."""

    def __init__(self):
        self.llm = get_llm_client()

    async def analyze(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze resume text and extract structured data.

        Args:
            resume_text: Raw text extracted from resume

        Returns:
            Structured resume data
        """
        if not resume_text or len(resume_text.strip()) < 50:
            raise ValueError("Resume text is too short to analyze")

        # Truncate if too long (keep first ~10000 chars to fit in context)
        if len(resume_text) > 10000:
            resume_text = resume_text[:10000] + "\n...[truncated]"

        prompt = RESUME_EXTRACTION_PROMPT.format(resume_text=resume_text)

        try:
            result = await self.llm.complete_structured(
                prompt=prompt,
                system_prompt=RESUME_ANALYSIS_SYSTEM_PROMPT,
                max_tokens=4096,
            )

            # Validate and clean the result
            return self._clean_result(result)

        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            raise

    def _clean_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate the extracted data."""
        # Ensure all expected keys exist
        cleaned = {
            "contact": result.get("contact") or {},
            "summary": result.get("summary"),
            "experience": result.get("experience") or [],
            "education": result.get("education") or [],
            "skills": result.get("skills") or [],
            "certifications": result.get("certifications") or [],
            "languages": result.get("languages") or [],
            "total_years_experience": result.get("total_years_experience"),
        }

        # Clean experience entries
        cleaned_experience = []
        for exp in cleaned["experience"]:
            if isinstance(exp, dict) and exp.get("company"):
                cleaned_experience.append({
                    "company": exp.get("company", ""),
                    "title": exp.get("title", ""),
                    "start_date": exp.get("start_date"),
                    "end_date": exp.get("end_date"),
                    "duration_months": exp.get("duration_months"),
                    "description": exp.get("description"),
                    "achievements": exp.get("achievements") or [],
                })
        cleaned["experience"] = cleaned_experience

        # Clean education entries
        cleaned_education = []
        for edu in cleaned["education"]:
            if isinstance(edu, dict) and edu.get("institution"):
                cleaned_education.append({
                    "institution": edu.get("institution", ""),
                    "degree": edu.get("degree"),
                    "field_of_study": edu.get("field_of_study"),
                    "graduation_year": edu.get("graduation_year"),
                    "gpa": edu.get("gpa"),
                })
        cleaned["education"] = cleaned_education

        # Clean certifications
        cleaned_certs = []
        for cert in cleaned["certifications"]:
            if isinstance(cert, dict) and cert.get("name"):
                cleaned_certs.append({
                    "name": cert.get("name", ""),
                    "issuer": cert.get("issuer"),
                    "issue_date": cert.get("issue_date"),
                    "expiration_date": cert.get("expiration_date"),
                })
        cleaned["certifications"] = cleaned_certs

        # Ensure skills is a list of strings
        if cleaned["skills"]:
            cleaned["skills"] = [
                str(s).strip() for s in cleaned["skills"]
                if s and str(s).strip()
            ]

        # Ensure languages is a list of strings
        if cleaned["languages"]:
            cleaned["languages"] = [
                str(l).strip() for l in cleaned["languages"]
                if l and str(l).strip()
            ]

        return cleaned

    async def get_skills_match(
        self,
        parsed_resume: Dict[str, Any],
        required_skills: list[str],
    ) -> Dict[str, Any]:
        """
        Check how well resume skills match required skills.

        Args:
            parsed_resume: Previously parsed resume data
            required_skills: List of skills to match against

        Returns:
            Match results with matched and unmatched skills
        """
        resume_skills = set(s.lower() for s in (parsed_resume.get("skills") or []))

        matched = []
        unmatched = []

        for skill in required_skills:
            skill_lower = skill.lower()
            # Check for exact or partial match
            found = any(
                skill_lower in rs or rs in skill_lower
                for rs in resume_skills
            )
            if found:
                matched.append(skill)
            else:
                unmatched.append(skill)

        return {
            "matched": matched,
            "unmatched": unmatched,
            "match_rate": len(matched) / len(required_skills) if required_skills else 1.0,
        }


# Singleton instance
resume_analyzer = ResumeAnalyzer()


def get_resume_analyzer() -> ResumeAnalyzer:
    """Get the resume analyzer instance."""
    return resume_analyzer
