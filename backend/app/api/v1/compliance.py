"""Compliance and bias monitoring API endpoints."""

from datetime import datetime, timedelta
from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.models import User, Candidate
from app.models.compliance import (
    AssessmentAuditRecord,
    ComplianceCheck,
    DisparateImpactReport,
    CandidateDemographics,
    CandidateDisclosure,
    RubricValidationRecord,
    ProtectedClass,
)
from app.schemas.compliance import (
    ProbeValidationResult,
    AnalysisValidationResult,
    RubricValidationResult,
    RubricValidationCreate,
    DisparateImpactReportResponse,
    DisparateImpactReportCreate,
    ImpactDashboardResponse,
    CandidateDemographicsCreate,
    CandidateDemographicsResponse,
    CandidateDisclosureCreate,
    CandidateDisclosureResponse,
    CandidateDisclosureContent,
    DisclosureAcknowledgement,
    AssessmentAuditRecordResponse,
    ComplianceStatusResponse,
    ConfigurationWarning,
    ConfigurationValidationResult,
)
from app.services.interview_compliance import get_interview_compliance_guard
from app.services.disparate_impact_monitor import get_disparate_impact_monitor
from app.services.disclosure_generator import get_disclosure_generator

router = APIRouter()


# ==================== Probe Validation ====================

@router.post("/validate-probe", response_model=ProbeValidationResult)
async def validate_probe(
    probe_text: str,
    current_user: Annotated[User, Depends(get_current_user)],
) -> ProbeValidationResult:
    """
    Validate that a probe doesn't touch prohibited topics.

    This endpoint checks interview questions against compliance rules
    to ensure they don't ask about protected characteristics.
    """
    guard = get_interview_compliance_guard()
    return guard.validate_probe(probe_text)


# ==================== Disparate Impact ====================

@router.get("/impact-dashboard", response_model=ImpactDashboardResponse)
async def get_impact_dashboard(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ImpactDashboardResponse:
    """
    Get real-time disparate impact monitoring dashboard.

    Shows:
    - Current impact ratios by protected class
    - Alerts for threshold violations
    - Last audit date and next due date

    Requires admin role.
    """
    if current_user.role not in ["ADMIN", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required for compliance dashboard"
        )

    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )

    monitor = get_disparate_impact_monitor()
    return await monitor.get_impact_dashboard(db, current_user.organization_id)


@router.post("/impact-reports", response_model=DisparateImpactReportResponse)
async def generate_impact_report(
    report_request: DisparateImpactReportCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> DisparateImpactReportResponse:
    """
    Generate a disparate impact report for the specified period.

    Required annually under NYC Local Law 144 and similar regulations.
    """
    if current_user.role not in ["ADMIN", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required to generate reports"
        )

    # Verify organization access
    if (current_user.organization_id != report_request.organization_id and
            not current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this organization"
        )

    monitor = get_disparate_impact_monitor()
    report = await monitor.generate_impact_report(
        db=db,
        organization_id=report_request.organization_id,
        date_range=(report_request.period_start, report_request.period_end),
        report_type=report_request.report_type,
        generated_by=current_user.id,
    )

    # Convert to response
    return DisparateImpactReportResponse(
        id=report.id,
        organization_id=report.organization_id,
        period_start=report.period_start,
        period_end=report.period_end,
        report_type=report.report_type,
        total_assessments=report.total_assessments,
        assessments_with_demographics=report.assessments_with_demographics,
        sections=[],  # Parsed from impact_analysis
        has_disparate_impact=report.has_disparate_impact,
        overall_assessment=report.overall_assessment,
        recommendations=report.recommendations or [],
        required_actions=report.required_actions or [],
        created_at=report.created_at,
    )


@router.get("/impact-reports", response_model=List[DisparateImpactReportResponse])
async def list_impact_reports(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0, ge=0),
) -> List[DisparateImpactReportResponse]:
    """
    List disparate impact reports for the organization.
    """
    if current_user.role not in ["ADMIN", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )

    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )

    query = (
        select(DisparateImpactReport)
        .where(DisparateImpactReport.organization_id == current_user.organization_id)
        .order_by(DisparateImpactReport.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(query)
    reports = result.scalars().all()

    return [
        DisparateImpactReportResponse(
            id=r.id,
            organization_id=r.organization_id,
            period_start=r.period_start,
            period_end=r.period_end,
            report_type=r.report_type,
            total_assessments=r.total_assessments,
            assessments_with_demographics=r.assessments_with_demographics,
            sections=[],
            has_disparate_impact=r.has_disparate_impact,
            overall_assessment=r.overall_assessment,
            recommendations=r.recommendations or [],
            required_actions=r.required_actions or [],
            created_at=r.created_at,
        )
        for r in reports
    ]


# ==================== Candidate Demographics ====================

@router.post("/demographics", response_model=CandidateDemographicsResponse)
async def submit_demographics(
    demographics: CandidateDemographicsCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> CandidateDemographicsResponse:
    """
    Submit voluntary demographic information for a candidate.

    This data is:
    - Separate from hiring decisions
    - Optional for candidates
    - Used only for bias monitoring, not scoring
    - Stored securely with access controls
    """
    # Check if demographics already exist
    existing = await db.execute(
        select(CandidateDemographics)
        .where(CandidateDemographics.candidate_id == demographics.candidate_id)
    )
    existing_record = existing.scalar_one_or_none()

    if existing_record:
        # Update existing
        existing_record.gender = demographics.gender
        existing_record.race_ethnicity = demographics.race_ethnicity
        existing_record.age_group = demographics.age_group
        existing_record.disability_status = demographics.disability_status
        existing_record.veteran_status = demographics.veteran_status
        existing_record.consent_given = demographics.consent_given
        if demographics.consent_given and not existing_record.consent_given_at:
            existing_record.consent_given_at = datetime.utcnow()

        await db.commit()
        await db.refresh(existing_record)
        return CandidateDemographicsResponse.model_validate(existing_record)

    # Create new
    new_demographics = CandidateDemographics(
        candidate_id=demographics.candidate_id,
        gender=demographics.gender,
        race_ethnicity=demographics.race_ethnicity,
        age_group=demographics.age_group,
        disability_status=demographics.disability_status,
        veteran_status=demographics.veteran_status,
        consent_given=demographics.consent_given,
        consent_given_at=datetime.utcnow() if demographics.consent_given else None,
    )

    db.add(new_demographics)
    await db.commit()
    await db.refresh(new_demographics)

    return CandidateDemographicsResponse.model_validate(new_demographics)


# ==================== Disclosures ====================

@router.post("/disclosures/generate", response_model=CandidateDisclosureContent)
async def generate_disclosure(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    role_profile_id: Optional[UUID] = None,
    jurisdiction: str = "DEFAULT",
    trait_names: Optional[List[str]] = Query(default=None),
) -> CandidateDisclosureContent:
    """
    Generate disclosure content for a candidate.

    Jurisdiction options: NYC, IL, CA, EU, DEFAULT
    """
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )

    generator = get_disclosure_generator()
    return await generator.generate_pre_assessment_disclosure(
        db=db,
        organization_id=current_user.organization_id,
        role_profile_id=role_profile_id,
        jurisdiction=jurisdiction,
        trait_names=trait_names,
    )


@router.post("/disclosures", response_model=CandidateDisclosureResponse)
async def record_disclosure(
    disclosure: CandidateDisclosureCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> CandidateDisclosureResponse:
    """
    Record that a disclosure was shown to a candidate.
    """
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )

    generator = get_disclosure_generator()
    record = await generator.record_disclosure(
        db=db,
        candidate_id=disclosure.candidate_id,
        organization_id=current_user.organization_id,
        disclosure_type=disclosure.disclosure_type,
        disclosure_content=disclosure.disclosure_content,
        jurisdiction=disclosure.jurisdiction,
        interview_session_id=disclosure.interview_session_id,
        consent_required=disclosure.consent_required,
        consent_given=disclosure.consent_given,
    )

    return CandidateDisclosureResponse.model_validate(record)


@router.post("/disclosures/{disclosure_id}/acknowledge", response_model=CandidateDisclosureResponse)
async def acknowledge_disclosure(
    disclosure_id: UUID,
    acknowledgement: DisclosureAcknowledgement,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> CandidateDisclosureResponse:
    """
    Record that a candidate acknowledged a disclosure.
    """
    generator = get_disclosure_generator()
    record = await generator.record_acknowledgement(
        db=db,
        disclosure_id=disclosure_id,
        consent_given=acknowledgement.consent_given,
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disclosure not found"
        )

    return CandidateDisclosureResponse.model_validate(record)


@router.get("/disclosures/candidate/{candidate_id}", response_model=List[CandidateDisclosureResponse])
async def get_candidate_disclosures(
    candidate_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> List[CandidateDisclosureResponse]:
    """
    Get all disclosures shown to a candidate.
    """
    query = (
        select(CandidateDisclosure)
        .where(CandidateDisclosure.candidate_id == candidate_id)
        .order_by(CandidateDisclosure.shown_at.desc())
    )

    result = await db.execute(query)
    disclosures = result.scalars().all()

    return [CandidateDisclosureResponse.model_validate(d) for d in disclosures]


# ==================== Audit Records ====================

@router.get("/audit/assessment/{assessment_id}", response_model=AssessmentAuditRecordResponse)
async def get_assessment_audit(
    assessment_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> AssessmentAuditRecordResponse:
    """
    Get complete audit trail for an assessment.

    Includes:
    - Every piece of evidence and its weight
    - Rubric derivation chain
    - Compliance checks performed
    - What information was excluded and why
    """
    if current_user.role not in ["ADMIN", "SUPER_ADMIN", "INTERVIEWER"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view audit records"
        )

    query = select(AssessmentAuditRecord).where(
        AssessmentAuditRecord.assessment_id == assessment_id
    )

    result = await db.execute(query)
    record = result.scalar_one_or_none()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit record not found"
        )

    return AssessmentAuditRecordResponse.model_validate(record)


# ==================== Compliance Status ====================

@router.get("/status", response_model=ComplianceStatusResponse)
async def get_compliance_status(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ComplianceStatusResponse:
    """
    Get organization compliance status.

    Shows:
    - Missing documentation
    - Warnings
    - Audit dates
    """
    if current_user.role not in ["ADMIN", "SUPER_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )

    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must belong to an organization"
        )

    org_id = current_user.organization_id

    # Check for last audit
    audit_query = (
        select(DisparateImpactReport)
        .where(
            and_(
                DisparateImpactReport.organization_id == org_id,
                DisparateImpactReport.report_type == "ANNUAL",
            )
        )
        .order_by(DisparateImpactReport.created_at.desc())
        .limit(1)
    )
    audit_result = await db.execute(audit_query)
    last_audit = audit_result.scalar_one_or_none()

    # Check for rubric validation issues
    validation_query = (
        select(RubricValidationRecord)
        .where(
            and_(
                RubricValidationRecord.organization_id == org_id,
                RubricValidationRecord.is_valid == False,
            )
        )
    )
    validation_result = await db.execute(validation_query)
    validation_issues = len(validation_result.scalars().all())

    # Build status response
    missing_docs = []
    warnings = []

    if not last_audit:
        missing_docs.append("bias_audit_report")
        warnings.append("No bias audit on record")
    elif (datetime.utcnow() - last_audit.created_at).days > 365:
        warnings.append("Bias audit is more than 12 months old")

    if validation_issues > 0:
        warnings.append(f"{validation_issues} rubric(s) have validation issues")

    is_compliant = len(missing_docs) == 0 and len([w for w in warnings if "URGENT" in w]) == 0

    return ComplianceStatusResponse(
        organization_id=org_id,
        is_compliant=is_compliant,
        missing_documentation=missing_docs,
        warnings=warnings,
        last_audit_date=last_audit.created_at if last_audit else None,
        next_audit_due=(
            last_audit.created_at + timedelta(days=365)
            if last_audit
            else datetime.utcnow()
        ),
        rubric_validation_issues=validation_issues,
        pending_disclosures=0,  # TODO: Implement pending disclosure check
    )
