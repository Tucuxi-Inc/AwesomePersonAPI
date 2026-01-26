"""
Disparate impact monitoring service.

Monitors assessment outcomes for disparate impact using the Four-Fifths Rule.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    AssessmentReport,
    Candidate,
    Recommendation,
)
from app.models.compliance import (
    CandidateDemographics,
    DisparateImpactReport,
    ProtectedClass,
)
from app.schemas.compliance import (
    ImpactRatio,
    ImpactReportSection,
    ImpactDashboardAlert,
    DisparateImpactReportResponse,
    ImpactDashboardResponse,
)


class DisparateImpactMonitor:
    """
    Monitor assessment outcomes for disparate impact.

    IMPORTANT: This requires voluntary demographic data collection,
    which must be:
    - Separate from hiring decision
    - Optional for candidates
    - Used only for monitoring, not scoring
    - Stored securely with access controls
    """

    FOUR_FIFTHS_THRESHOLD = 0.8
    MINIMUM_SAMPLE_SIZE = 30  # Per group for statistical validity

    # Groups for each protected class
    DEMOGRAPHIC_GROUPS = {
        ProtectedClass.GENDER: ["male", "female", "non_binary"],
        ProtectedClass.RACE_ETHNICITY: [
            "white",
            "black_african_american",
            "hispanic_latino",
            "asian",
            "native_american",
            "pacific_islander",
            "two_or_more",
        ],
        ProtectedClass.AGE_GROUP: ["under_40", "40_plus"],
        ProtectedClass.DISABILITY: ["yes", "no"],
        ProtectedClass.VETERAN_STATUS: ["yes", "no"],
    }

    async def calculate_impact_ratios(
        self,
        db: AsyncSession,
        organization_id: UUID,
        protected_class: ProtectedClass,
        date_range: Tuple[datetime, datetime],
        role_profile_id: Optional[UUID] = None,
    ) -> List[ImpactRatio]:
        """
        Calculate selection rate ratios across demographic groups.

        Args:
            db: Database session
            organization_id: Organization to analyze
            protected_class: The protected class to analyze
            date_range: Start and end dates for the analysis period
            role_profile_id: Optional role profile to filter by

        Returns:
            List of ImpactRatio objects for each group
        """
        start_date, end_date = date_range

        # Get assessment outcomes with demographic data
        outcomes = await self._get_outcomes_with_demographics(
            db=db,
            organization_id=organization_id,
            protected_class=protected_class,
            date_range=date_range,
            role_profile_id=role_profile_id,
        )

        if not outcomes:
            return []

        # Group by demographic
        groups: Dict[str, List[dict]] = {}
        for outcome in outcomes:
            group_value = outcome.get("demographic_value")
            if group_value and group_value != "prefer_not_to_say":
                if group_value not in groups:
                    groups[group_value] = []
                groups[group_value].append(outcome)

        # Calculate selection rates per group
        selection_rates: Dict[str, float] = {}
        sample_sizes: Dict[str, int] = {}

        for group_name, group_outcomes in groups.items():
            # "Selected" means STRONG_HIRE or HIRE
            selected = len([
                o for o in group_outcomes
                if o.get("recommendation") in ["STRONG_HIRE", "HIRE"]
            ])
            total = len(group_outcomes)
            selection_rates[group_name] = selected / total if total > 0 else 0
            sample_sizes[group_name] = total

        if not selection_rates:
            return []

        # Find highest selection rate (reference group)
        max_rate = max(selection_rates.values())
        max_rate_group = [k for k, v in selection_rates.items() if v == max_rate][0]

        # Calculate impact ratios
        impact_ratios: List[ImpactRatio] = []
        for group_name, rate in selection_rates.items():
            if max_rate > 0:
                ratio = rate / max_rate
            else:
                ratio = 1.0

            impact_ratios.append(
                ImpactRatio(
                    protected_class=protected_class.value,
                    group_a=group_name,
                    group_b=max_rate_group,
                    group_a_selection_rate=round(rate, 4),
                    group_b_selection_rate=round(max_rate, 4),
                    impact_ratio=round(ratio, 4),
                    passes_four_fifths=ratio >= self.FOUR_FIFTHS_THRESHOLD,
                    sample_size_adequate=sample_sizes.get(group_name, 0) >= self.MINIMUM_SAMPLE_SIZE,
                    group_a_sample_size=sample_sizes.get(group_name, 0),
                    group_b_sample_size=sample_sizes.get(max_rate_group, 0),
                )
            )

        return impact_ratios

    async def _get_outcomes_with_demographics(
        self,
        db: AsyncSession,
        organization_id: UUID,
        protected_class: ProtectedClass,
        date_range: Tuple[datetime, datetime],
        role_profile_id: Optional[UUID] = None,
    ) -> List[dict]:
        """
        Get assessment outcomes joined with demographic data.
        """
        start_date, end_date = date_range

        # Build query to get assessments with demographics
        query = (
            select(
                AssessmentReport.id,
                AssessmentReport.candidate_id,
                AssessmentReport.recommendation,
                AssessmentReport.created_at,
                CandidateDemographics.gender,
                CandidateDemographics.race_ethnicity,
                CandidateDemographics.age_group,
                CandidateDemographics.disability_status,
                CandidateDemographics.veteran_status,
            )
            .join(
                Candidate,
                AssessmentReport.candidate_id == Candidate.id
            )
            .outerjoin(
                CandidateDemographics,
                Candidate.id == CandidateDemographics.candidate_id
            )
            .where(
                and_(
                    Candidate.organization_id == organization_id,
                    AssessmentReport.created_at >= start_date,
                    AssessmentReport.created_at <= end_date,
                )
            )
        )

        if role_profile_id:
            query = query.where(Candidate.role_profile_id == role_profile_id)

        result = await db.execute(query)
        rows = result.fetchall()

        # Map protected class to column
        class_column_map = {
            ProtectedClass.GENDER: "gender",
            ProtectedClass.RACE_ETHNICITY: "race_ethnicity",
            ProtectedClass.AGE_GROUP: "age_group",
            ProtectedClass.DISABILITY: "disability_status",
            ProtectedClass.VETERAN_STATUS: "veteran_status",
        }

        column_name = class_column_map.get(protected_class)

        outcomes = []
        for row in rows:
            demographic_value = getattr(row, column_name, None) if column_name else None
            if demographic_value:  # Only include records with demographic data
                outcomes.append({
                    "assessment_id": str(row.id),
                    "candidate_id": str(row.candidate_id),
                    "recommendation": row.recommendation,
                    "demographic_value": demographic_value,
                    "created_at": row.created_at,
                })

        return outcomes

    async def generate_impact_report(
        self,
        db: AsyncSession,
        organization_id: UUID,
        date_range: Tuple[datetime, datetime],
        report_type: str = "ANNUAL",
        generated_by: Optional[UUID] = None,
    ) -> DisparateImpactReport:
        """
        Generate comprehensive disparate impact report.
        Required annually under NYC Local Law 144 and similar regulations.
        """
        start_date, end_date = date_range

        # Count total assessments in period
        total_query = (
            select(func.count(AssessmentReport.id))
            .join(Candidate, AssessmentReport.candidate_id == Candidate.id)
            .where(
                and_(
                    Candidate.organization_id == organization_id,
                    AssessmentReport.created_at >= start_date,
                    AssessmentReport.created_at <= end_date,
                )
            )
        )
        total_result = await db.execute(total_query)
        total_assessments = total_result.scalar() or 0

        # Count assessments with demographics
        demo_query = (
            select(func.count(AssessmentReport.id))
            .join(Candidate, AssessmentReport.candidate_id == Candidate.id)
            .join(CandidateDemographics, Candidate.id == CandidateDemographics.candidate_id)
            .where(
                and_(
                    Candidate.organization_id == organization_id,
                    AssessmentReport.created_at >= start_date,
                    AssessmentReport.created_at <= end_date,
                    CandidateDemographics.consent_given == True,
                )
            )
        )
        demo_result = await db.execute(demo_query)
        assessments_with_demographics = demo_result.scalar() or 0

        # Calculate ratios for each protected class
        impact_analysis = {}
        sections = []
        has_any_disparate_impact = False

        for protected_class in ProtectedClass:
            ratios = await self.calculate_impact_ratios(
                db=db,
                organization_id=organization_id,
                protected_class=protected_class,
                date_range=date_range,
            )

            failing_groups = [
                r for r in ratios
                if not r.passes_four_fifths and r.sample_size_adequate
            ]

            has_disparate_impact = len(failing_groups) > 0
            if has_disparate_impact:
                has_any_disparate_impact = True

            section = ImpactReportSection(
                protected_class=protected_class.value,
                impact_ratios=ratios,
                has_disparate_impact=has_disparate_impact,
                failing_groups=failing_groups,
                sample_sizes={r.group_a: r.group_a_sample_size for r in ratios},
                recommendations=self._generate_recommendations(failing_groups),
            )
            sections.append(section)

            impact_analysis[protected_class.value] = {
                "ratios": [r.model_dump() for r in ratios],
                "has_disparate_impact": has_disparate_impact,
            }

        # Generate overall assessment
        overall_assessment = self._assess_overall(sections)
        required_actions = self._determine_required_actions(sections)
        all_recommendations = []
        for section in sections:
            all_recommendations.extend(section.recommendations)

        # Create report record
        report = DisparateImpactReport(
            organization_id=organization_id,
            period_start=start_date,
            period_end=end_date,
            report_type=report_type,
            generated_by=generated_by,
            total_assessments=total_assessments,
            assessments_with_demographics=assessments_with_demographics,
            impact_analysis=impact_analysis,
            has_disparate_impact=has_any_disparate_impact,
            overall_assessment=overall_assessment,
            recommendations=list(set(all_recommendations)),
            required_actions=required_actions,
        )

        db.add(report)
        await db.commit()
        await db.refresh(report)

        return report

    async def get_impact_dashboard(
        self,
        db: AsyncSession,
        organization_id: UUID,
    ) -> ImpactDashboardResponse:
        """
        Get real-time disparate impact monitoring dashboard.
        """
        # Current period (last 12 months)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=365)
        date_range = (start_date, end_date)

        # Calculate current ratios for all protected classes
        current_ratios: List[ImpactRatio] = []
        for protected_class in ProtectedClass:
            ratios = await self.calculate_impact_ratios(
                db=db,
                organization_id=organization_id,
                protected_class=protected_class,
                date_range=date_range,
            )
            current_ratios.extend(ratios)

        # Generate alerts for failing groups
        alerts: List[ImpactDashboardAlert] = []
        for ratio in current_ratios:
            if not ratio.passes_four_fifths and ratio.sample_size_adequate:
                alerts.append(
                    ImpactDashboardAlert(
                        protected_class=ratio.protected_class,
                        group=ratio.group_a,
                        current_ratio=ratio.impact_ratio,
                        threshold=self.FOUR_FIFTHS_THRESHOLD,
                        severity="HIGH" if ratio.impact_ratio < 0.7 else "MEDIUM",
                    )
                )

        # Get last audit date
        last_audit_query = (
            select(DisparateImpactReport)
            .where(
                and_(
                    DisparateImpactReport.organization_id == organization_id,
                    DisparateImpactReport.report_type == "ANNUAL",
                )
            )
            .order_by(DisparateImpactReport.created_at.desc())
            .limit(1)
        )
        last_audit_result = await db.execute(last_audit_query)
        last_audit = last_audit_result.scalar_one_or_none()

        last_audit_date = last_audit.created_at if last_audit else None
        next_audit_due = (
            last_audit_date + timedelta(days=365)
            if last_audit_date
            else datetime.utcnow()
        )

        return ImpactDashboardResponse(
            current_ratios=current_ratios,
            trends=[],  # TODO: Implement trend calculation
            alerts=alerts,
            last_full_audit=last_audit_date,
            next_audit_due=next_audit_due,
        )

    def _generate_recommendations(
        self,
        failing_groups: List[ImpactRatio],
    ) -> List[str]:
        """Generate recommendations for addressing disparate impact."""
        if not failing_groups:
            return []

        recommendations = [
            "Review trait weights and thresholds for job-relatedness",
            "Consider alternative assessment criteria with lower adverse impact",
            "Document business necessity for current criteria",
            "Consult with employment counsel before making changes",
        ]

        # Add specific recommendations based on severity
        for ratio in failing_groups:
            if ratio.impact_ratio < 0.5:
                recommendations.append(
                    f"URGENT: {ratio.group_a} has selection rate less than 50% of reference group"
                )

        return recommendations

    def _assess_overall(self, sections: List[ImpactReportSection]) -> str:
        """Generate overall assessment text."""
        failing_sections = [s for s in sections if s.has_disparate_impact]

        if not failing_sections:
            return (
                "No disparate impact detected across any protected class. "
                "All groups meet or exceed the four-fifths threshold."
            )

        failing_classes = [s.protected_class for s in failing_sections]
        return (
            f"Disparate impact detected in {len(failing_classes)} protected class(es): "
            f"{', '.join(failing_classes)}. Review recommended."
        )

    def _determine_required_actions(
        self,
        sections: List[ImpactReportSection],
    ) -> List[str]:
        """Determine required actions based on findings."""
        actions = []

        for section in sections:
            if section.has_disparate_impact:
                # Check severity
                severe_failures = [
                    r for r in section.failing_groups
                    if r.impact_ratio < 0.6
                ]

                if severe_failures:
                    actions.append(
                        f"REQUIRED: Review {section.protected_class} assessment criteria - "
                        f"severe disparity detected"
                    )
                else:
                    actions.append(
                        f"RECOMMENDED: Document business necessity for {section.protected_class} criteria"
                    )

        return actions


# Singleton instance
disparate_impact_monitor = DisparateImpactMonitor()


def get_disparate_impact_monitor() -> DisparateImpactMonitor:
    """Get the disparate impact monitor instance."""
    return disparate_impact_monitor
