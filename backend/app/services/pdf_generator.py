"""
PDF Report Generator for Simple Mode Assessments.

Uses WeasyPrint with Jinja2 HTML templates for professional report generation.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

from app.models.simple_assessment import SimpleAssessment
from app.models.simple_candidate import SimpleCandidate, SimpleInterviewStatus
from app.models.trait import Trait


@dataclass
class CandidateReportData:
    """Data structure for candidate section of report."""
    id: str
    full_name: str
    email: str
    composite_score: Optional[float]
    recommendation: Optional[str]
    recommendation_rationale: Optional[str]
    qualification_status: str
    trait_scores: List[dict]  # [{trait_name, score, explanation, confidence}]
    rank: int


@dataclass
class AssessmentReportData:
    """Complete report data structure."""
    assessment_id: str
    job_title: str
    job_description: str
    organization_name: str
    generated_at: datetime
    selected_traits: List[dict]  # [{id, name, category}]
    total_candidates: int
    completed_interviews: int
    candidates: List[CandidateReportData]


class PDFReportGenerator:
    """
    Generates PDF reports for Simple Mode assessments.

    Uses WeasyPrint for HTML-to-PDF conversion with Jinja2 templates.
    """

    def __init__(self):
        # Set up template directory
        self.template_dir = Path(__file__).parent.parent / "templates" / "reports"
        self.template_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"])
        )
        self.css_path = self.template_dir / "partials" / "styles.css"

    async def generate_assessment_report(
        self,
        assessment: SimpleAssessment,
        candidates: List[SimpleCandidate],
        traits: List[Trait],
        organization_name: str,
    ) -> bytes:
        """
        Generate PDF report for a Simple Mode assessment.

        Args:
            assessment: The assessment to report on
            candidates: List of candidates with completed interviews
            traits: List of selected traits
            organization_name: Organization name for branding

        Returns:
            PDF bytes ready for download
        """
        # Build report data
        report_data = self._build_report_data(
            assessment, candidates, traits, organization_name
        )

        # Render HTML template
        template = self.template_env.get_template("simple_assessment.html")
        html_content = template.render(report=report_data)

        # Generate PDF
        html = HTML(string=html_content, base_url=str(self.template_dir))

        stylesheets = []
        if self.css_path.exists():
            stylesheets.append(CSS(filename=str(self.css_path)))

        pdf_bytes = html.write_pdf(stylesheets=stylesheets)

        return pdf_bytes

    def _build_report_data(
        self,
        assessment: SimpleAssessment,
        candidates: List[SimpleCandidate],
        traits: List[Trait],
        organization_name: str,
    ) -> AssessmentReportData:
        """Transform DB models into report data structure."""
        # Create trait lookup map
        trait_map = {str(t.id): t for t in traits}

        # Sort candidates by composite score (descending), completed only
        completed_candidates = [
            c for c in candidates
            if c.interview_status == SimpleInterviewStatus.COMPLETED
            and c.trait_scores is not None
        ]
        sorted_candidates = sorted(
            completed_candidates,
            key=lambda c: c.composite_score or 0,
            reverse=True
        )

        candidate_data = []
        for rank, candidate in enumerate(sorted_candidates, 1):
            trait_scores = []
            if candidate.trait_scores:
                for trait_id, score_data in candidate.trait_scores.items():
                    # Get trait name from map or use stored name
                    trait = trait_map.get(trait_id)
                    trait_name = trait.name if trait else score_data.get("trait_name", "Unknown")

                    trait_scores.append({
                        "trait_name": trait_name,
                        "score": score_data.get("score", 0),
                        "explanation": score_data.get("explanation", ""),
                        "confidence": score_data.get("confidence", 0),
                    })

            # Sort trait scores by score descending for consistent display
            trait_scores.sort(key=lambda x: x["score"], reverse=True)

            candidate_data.append(CandidateReportData(
                id=str(candidate.id),
                full_name=candidate.full_name,
                email=candidate.email,
                composite_score=candidate.composite_score,
                recommendation=candidate.recommendation,
                recommendation_rationale=candidate.recommendation_rationale,
                qualification_status=candidate.qualification_status.value,
                trait_scores=trait_scores,
                rank=rank,
            ))

        # Build trait info list
        selected_traits = []
        for trait in traits:
            selected_traits.append({
                "id": str(trait.id),
                "name": trait.name,
                "category": trait.category if isinstance(trait.category, str) else trait.category.value,
            })

        return AssessmentReportData(
            assessment_id=str(assessment.id),
            job_title=assessment.job_title,
            job_description=self._truncate_text(assessment.job_description, 500),
            organization_name=organization_name,
            generated_at=datetime.utcnow(),
            selected_traits=selected_traits,
            total_candidates=assessment.total_candidates,
            completed_interviews=assessment.interviews_completed,
            candidates=candidate_data,
        )

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text with ellipsis if too long."""
        if len(text) <= max_length:
            return text
        return text[:max_length].rsplit(" ", 1)[0] + "..."


# Singleton instance
_pdf_generator: Optional[PDFReportGenerator] = None


def get_pdf_generator() -> PDFReportGenerator:
    """Get PDF generator singleton."""
    global _pdf_generator
    if _pdf_generator is None:
        _pdf_generator = PDFReportGenerator()
    return _pdf_generator
