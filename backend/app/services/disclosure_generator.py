"""
Candidate disclosure generator for AI assessment notices.

Generates required disclosures for candidates about AI assessment based on
jurisdiction requirements (NYC Local Law 144, Illinois AI Act, GDPR, etc.)
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organization, RoleProfile, Trait
from app.models.compliance import CandidateDisclosure
from app.schemas.compliance import (
    DisclosureSection,
    CandidateDisclosureContent,
)


class CandidateDisclosureGenerator:
    """
    Generate required disclosures for candidates about AI assessment.
    """

    # Jurisdictions that require specific disclosures
    JURISDICTIONS = {
        "NYC": {
            "name": "New York City",
            "law": "NYC Local Law 144",
            "consent_required": True,
            "audit_access": True,
        },
        "IL": {
            "name": "Illinois",
            "law": "Illinois AI Video Interview Act",
            "consent_required": True,
            "video_specific": True,
        },
        "CA": {
            "name": "California",
            "law": "CCPA/CPRA",
            "consent_required": False,
            "data_deletion": True,
        },
        "EU": {
            "name": "European Union",
            "law": "GDPR Article 22",
            "consent_required": True,
            "explanation_required": True,
        },
        "DEFAULT": {
            "name": "Default",
            "law": "Best Practice",
            "consent_required": False,
        },
    }

    async def generate_pre_assessment_disclosure(
        self,
        db: AsyncSession,
        organization_id: UUID,
        role_profile_id: Optional[UUID] = None,
        jurisdiction: str = "DEFAULT",
        trait_names: Optional[List[str]] = None,
    ) -> CandidateDisclosureContent:
        """
        Generate disclosure required before AI assessment.

        Required by:
        - Illinois AI Video Interview Act
        - NYC Local Law 144
        - Various state laws
        - GDPR Article 22 (for EU candidates)
        """
        # Get organization info
        org_result = await db.execute(
            select(Organization).where(Organization.id == organization_id)
        )
        org = org_result.scalar_one_or_none()
        org_name = org.name if org else "The Organization"

        # Get role profile info if provided
        role_name = "this position"
        if role_profile_id:
            role_result = await db.execute(
                select(RoleProfile).where(RoleProfile.id == role_profile_id)
            )
            role = role_result.scalar_one_or_none()
            if role:
                role_name = f"the {role.name} position"

        # Get trait names if not provided
        if not trait_names:
            trait_names = ["relevant job characteristics"]

        # Build sections
        sections: List[DisclosureSection] = []

        # Section 1: What We Use
        sections.append(
            DisclosureSection(
                heading="What We Use",
                content=f"""
{org_name} uses an AI-assisted assessment tool to help evaluate candidates
for {role_name}. This tool analyzes your responses to behavioral interview
questions to assess job-relevant characteristics.
                """.strip()
            )
        )

        # Section 2: What We Assess
        traits_text = ", ".join(trait_names[:5])
        if len(trait_names) > 5:
            traits_text += f", and {len(trait_names) - 5} other characteristics"

        rubric_source_text = self._describe_rubric_source(org)

        sections.append(
            DisclosureSection(
                heading="What We Assess",
                content=f"""
The assessment evaluates the following job-relevant characteristics:
{traits_text}

These characteristics were determined to be relevant to success in this role
based on {rubric_source_text}.
                """.strip()
            )
        )

        # Section 3: How It Works
        sections.append(
            DisclosureSection(
                heading="How It Works",
                content="""
During the assessment, you will be asked behavioral interview questions about
your past experiences. The AI analyzes your responses to identify evidence of
job-relevant characteristics. The assessment focuses on specific examples and
outcomes from your professional experience.

A qualified human reviewer will also review the assessment results before any
hiring decision is made. The AI assessment is one input into the hiring process,
not the sole determining factor.
                """.strip()
            )
        )

        # Section 4: What We Don't Consider
        sections.append(
            DisclosureSection(
                heading="What We Don't Consider",
                content="""
The assessment does NOT consider or score based on:
- Your name, gender, age, race, ethnicity, or national origin
- Your religion, disability status, or other protected characteristics
- The specific schools you attended or your graduation dates
- Your physical appearance, accent, or communication style preferences
- Any information not directly related to job performance

Technical safeguards are in place to exclude this information from scoring.
                """.strip()
            )
        )

        # Section 5: Your Rights (jurisdiction-specific)
        rights_content = self._generate_rights_section(jurisdiction)
        sections.append(
            DisclosureSection(
                heading="Your Rights",
                content=rights_content
            )
        )

        # Section 6: Questions or Accommodations
        hr_contact = org.settings.get("hr_contact_email", "hr@company.com") if org and org.settings else "the HR department"
        sections.append(
            DisclosureSection(
                heading="Questions or Accommodations",
                content=f"""
If you have questions about this assessment or need accommodations, please
contact {hr_contact} before beginning the assessment.

You may also request an alternative assessment process if you prefer not to
participate in the AI-assisted assessment.
                """.strip()
            )
        )

        # Determine consent requirements
        jurisdiction_info = self.JURISDICTIONS.get(jurisdiction, self.JURISDICTIONS["DEFAULT"])
        consent_required = jurisdiction_info.get("consent_required", False)

        consent_text = None
        if consent_required:
            consent_text = (
                "I acknowledge that I have read and understand this notice about "
                "AI-assisted assessment. I consent to participating in this assessment."
            )

        return CandidateDisclosureContent(
            title="Notice Regarding AI-Assisted Assessment",
            sections=sections,
            consent_required=consent_required,
            consent_text=consent_text,
            jurisdiction=jurisdiction,
        )

    def _describe_rubric_source(self, org: Optional[Organization]) -> str:
        """Describe the source of the assessment rubric."""
        # TODO: Check actual rubric source from org settings
        return (
            "research-validated assessment criteria and analysis of successful "
            "performers in similar roles"
        )

    def _generate_rights_section(self, jurisdiction: str) -> str:
        """Generate jurisdiction-specific rights disclosure."""
        base_rights = """
You have the right to:
- Request information about how the assessment works
- Request that a human review any automated decision
- Withdraw from the assessment process at any time
- Request an alternative assessment method
        """.strip()

        jurisdiction_additions = ""

        if jurisdiction == "NYC":
            jurisdiction_additions = """

Under NYC Local Law 144:
- You may request an alternative selection process
- You may access the most recent bias audit summary at [organization website]
- Annual bias audits are conducted and published
            """.strip()

        elif jurisdiction == "IL":
            jurisdiction_additions = """

Under Illinois Law:
- You have been notified that AI will be used to analyze your responses
- You may request all copies of your video interviews be deleted
- The AI analysis methodology has been disclosed to you
            """.strip()

        elif jurisdiction in ["CA", "EU"]:
            jurisdiction_additions = """

- You may request a copy of the information used in your assessment
- You may request deletion of your assessment data
- You may request an explanation of significant factors in any decision
- You have the right to object to automated decision-making
            """.strip()

        return base_rights + jurisdiction_additions

    async def record_disclosure(
        self,
        db: AsyncSession,
        candidate_id: UUID,
        organization_id: UUID,
        disclosure_type: str,
        disclosure_content: str,
        jurisdiction: Optional[str] = None,
        interview_session_id: Optional[UUID] = None,
        consent_required: bool = False,
        consent_given: Optional[bool] = None,
    ) -> CandidateDisclosure:
        """
        Record that a disclosure was shown to a candidate.
        """
        disclosure = CandidateDisclosure(
            candidate_id=candidate_id,
            organization_id=organization_id,
            interview_session_id=interview_session_id,
            disclosure_type=disclosure_type,
            disclosure_version="1.0",
            disclosure_content=disclosure_content,
            jurisdiction=jurisdiction,
            consent_required=consent_required,
            consent_given=consent_given,
            consent_given_at=datetime.utcnow() if consent_given else None,
            shown_at=datetime.utcnow(),
        )

        db.add(disclosure)
        await db.commit()
        await db.refresh(disclosure)

        return disclosure

    async def record_acknowledgement(
        self,
        db: AsyncSession,
        disclosure_id: UUID,
        consent_given: Optional[bool] = None,
    ) -> CandidateDisclosure:
        """
        Record that a candidate acknowledged a disclosure.
        """
        result = await db.execute(
            select(CandidateDisclosure).where(CandidateDisclosure.id == disclosure_id)
        )
        disclosure = result.scalar_one_or_none()

        if disclosure:
            disclosure.acknowledged_at = datetime.utcnow()
            if consent_given is not None:
                disclosure.consent_given = consent_given
                disclosure.consent_given_at = datetime.utcnow()

            await db.commit()
            await db.refresh(disclosure)

        return disclosure


# Singleton instance
disclosure_generator = CandidateDisclosureGenerator()


def get_disclosure_generator() -> CandidateDisclosureGenerator:
    """Get the disclosure generator instance."""
    return disclosure_generator
