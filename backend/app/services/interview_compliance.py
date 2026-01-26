"""
Interview compliance guard for ensuring probes and analysis don't touch protected characteristics.
"""

from typing import List, Optional
from datetime import datetime

from app.schemas.compliance import (
    ProbeViolation,
    ProbeWarning,
    ProbeValidationResult,
    AnalysisIssue,
    AnalysisValidationResult,
)


class InterviewComplianceGuard:
    """
    Ensure interview questions and analysis don't touch protected characteristics.
    """

    # Topics that should NEVER be probed
    PROHIBITED_TOPICS = [
        "age",
        "birth",
        "graduation year",
        "when did you graduate",
        "how old",
        "married",
        "spouse",
        "husband",
        "wife",
        "children",
        "kids",
        "family status",
        "pregnant",
        "pregnancy",
        "maternity",
        "paternity",
        "religion",
        "religious",
        "church",
        "worship",
        "faith",
        "beliefs",
        "pray",
        "god",
        "spiritual",
        "national origin",
        "citizenship",
        "visa",
        "where are you from",
        "where were you born",
        "native language",
        "accent",
        "immigrant",
        "disability",
        "disabled",
        "health condition",
        "medical",
        "accommodation",
        "wheelchair",
        "mental health",
        "psychiatric",
        "arrest",
        "criminal",
        "conviction",
        "jail",
        "prison",
        "military",
        "veteran",
        "political",
        "party",
        "vote",
        "democrat",
        "republican",
        "union",
        "organize",
        "labor",
        "genetic",
        "dna",
        "family medical history",
        "sexual orientation",
        "gender identity",
        "transgender",
        "race",
        "ethnicity",
        "skin color",
    ]

    # Phrases that might elicit protected information
    WARNING_PHRASES = [
        "tell me about yourself",  # Can elicit personal details
        "where did you grow up",
        "what are your hobbies",  # Can reveal religion, disability
        "do you have reliable transportation",  # Disability/economic proxy
        "can you work weekends",  # Religion proxy - rephrase as job requirement
        "can you work holidays",  # Religion proxy
        "what year did you",
        "when did you start",  # Can be age proxy
        "how long have you been",  # Can be age proxy
        "are you comfortable with",  # Can be disability proxy
    ]

    def validate_probe(self, probe_text: str) -> ProbeValidationResult:
        """
        Validate that a probe doesn't touch prohibited topics.

        Args:
            probe_text: The text of the probe to validate

        Returns:
            ProbeValidationResult with validation status and any issues
        """
        probe_lower = probe_text.lower()

        violations: List[ProbeViolation] = []
        warnings: List[ProbeWarning] = []

        # Check for prohibited topics
        for topic in self.PROHIBITED_TOPICS:
            if topic in probe_lower:
                violations.append(
                    ProbeViolation(
                        type="PROHIBITED_TOPIC",
                        topic=topic,
                        severity="HIGH",
                        recommendation=f"Remove or rephrase to avoid reference to '{topic}'"
                    )
                )

        # Check for warning phrases
        for phrase in self.WARNING_PHRASES:
            if phrase in probe_lower:
                warnings.append(
                    ProbeWarning(
                        type="RISKY_PHRASE",
                        phrase=phrase,
                        severity="MEDIUM",
                        recommendation="Consider rephrasing to avoid eliciting protected information"
                    )
                )

        return ProbeValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            probe_text=probe_text[:200] if len(probe_text) > 200 else probe_text
        )

    def validate_response_analysis(
        self,
        response_text: str,
        extracted_evidence: List[dict],
    ) -> AnalysisValidationResult:
        """
        Ensure response analysis doesn't incorporate protected information.

        Args:
            response_text: The candidate's response text
            extracted_evidence: List of evidence items extracted from the response

        Returns:
            AnalysisValidationResult with validation status and any issues
        """
        issues: List[AnalysisIssue] = []
        actions_taken: List[str] = []

        for evidence in extracted_evidence:
            evidence_text = evidence.get("source_text", "").lower()
            evidence_id = evidence.get("id", "unknown")

            # Check if evidence references protected characteristics
            for topic in self.PROHIBITED_TOPICS:
                if topic in evidence_text:
                    issues.append(
                        AnalysisIssue(
                            type="PROTECTED_INFO_IN_EVIDENCE",
                            evidence_id=str(evidence_id),
                            topic=topic,
                            action="EXCLUDE_FROM_SCORING",
                            rationale=f"Evidence references protected characteristic: {topic}"
                        )
                    )
                    actions_taken.append("EXCLUDE_FROM_SCORING")
                    break  # One issue per evidence item is enough

        return AnalysisValidationResult(
            is_clean=len(issues) == 0,
            issues=issues,
            actions_taken=list(set(actions_taken))
        )

    def sanitize_probe(self, probe_text: str) -> Optional[str]:
        """
        Attempt to sanitize a probe by removing problematic elements.

        Note: This is a best-effort function. Complex violations may require
        manual intervention.

        Args:
            probe_text: The probe text to sanitize

        Returns:
            Sanitized probe text, or None if the probe cannot be salvaged
        """
        validation = self.validate_probe(probe_text)

        if validation.is_valid:
            return probe_text

        # If there are high-severity violations, we cannot sanitize
        if any(v.severity == "HIGH" for v in validation.violations):
            return None

        # For warnings, we return the original with a note that it should be reviewed
        return probe_text

    def get_safe_alternative(self, risky_phrase: str) -> Optional[str]:
        """
        Suggest a safer alternative for a risky phrase.

        Args:
            risky_phrase: The phrase that was flagged

        Returns:
            Suggested safe alternative, or None if no suggestion available
        """
        alternatives = {
            "tell me about yourself": "Tell me about your professional experience",
            "where did you grow up": "What experiences shaped your professional development?",
            "what are your hobbies": "What activities outside work help you stay sharp professionally?",
            "do you have reliable transportation": "This role requires being on-site. Can you meet the attendance requirements?",
            "can you work weekends": "This role requires weekend availability. Is that compatible with your schedule?",
            "can you work holidays": "This role may require holiday coverage. Is that compatible with your schedule?",
        }

        return alternatives.get(risky_phrase.lower())


# Singleton instance
interview_compliance_guard = InterviewComplianceGuard()


def get_interview_compliance_guard() -> InterviewComplianceGuard:
    """Get the interview compliance guard instance."""
    return interview_compliance_guard
