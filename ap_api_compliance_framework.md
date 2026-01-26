# AP API Compliance & Bias Monitoring Framework
## Defensible Design for Fair and Objective Candidate Assessment

**Version 1.0 | January 2026**
**Supplement to: AP API Development Specification**

---

## Executive Summary

This document specifies the compliance, bias monitoring, and audit infrastructure required to make the AP API defensible under employment discrimination law. The goal is not to guarantee zero disparate impact (which is impossible for any selection system), but to:

1. **Document job-relatedness** of all assessment criteria
2. **Monitor for disparate impact** and flag when it exceeds thresholds
3. **Provide complete audit trails** showing how decisions were made
4. **Enable customers to demonstrate compliance** with applicable laws
5. **Implement technical safeguards** against obvious bias vectors

---

## Part 1: Legal Framework Summary

### 1.1 Applicable Laws

| Law/Regulation | Jurisdiction | Key Requirements | AP API Relevance |
|----------------|--------------|------------------|------------------|
| **Title VII (Civil Rights Act)** | US Federal | No discrimination based on race, color, religion, sex, national origin | Core design principle |
| **ADEA** | US Federal | No age discrimination (40+) | Avoid age-correlated criteria |
| **ADA** | US Federal | Reasonable accommodation; job-related criteria | Trait requirements must be essential |
| **EEOC Uniform Guidelines** | US Federal | Selection procedures must be validated; job-related | Research basis + validation |
| **NYC Local Law 144** | NYC | Annual bias audits for AI hiring tools; notice to candidates | Audit infrastructure |
| **Illinois AI Video Interview Act** | Illinois | Consent + explanation for AI analysis | Disclosure requirements |
| **GDPR Article 22** | EU | Right to explanation for automated decisions | Explainability architecture |
| **EU AI Act** | EU | High-risk AI systems require conformity assessment | Documentation requirements |

### 1.2 Key Legal Standards

**Job-Relatedness**: Assessment criteria must be demonstrably related to job performance.
- ✅ AP API: Research-based rubrics cite validity studies; top performer profiling establishes empirical link

**Business Necessity**: If disparate impact exists, the practice must be necessary for the business.
- ✅ AP API: Trait selection tied to role requirements; customers document rationale

**Less Discriminatory Alternative**: If a less discriminatory method exists with equal validity, it should be used.
- ⚠️ AP API: Monitor for impact; provide alternative assessment options

**Validation**: Selection procedures should be validated per professional standards.
- ✅ AP API: Research citations; outcome tracking enables criterion validation

---

## Part 2: Technical Safeguards

### 2.1 Resume Processing Safeguards

```python
# backend/app/services/resume_processor.py

class BiasAwareResumeProcessor:
    """
    Process resumes with safeguards against demographic inference.
    """
    
    # Fields that should NEVER influence scoring
    EXCLUDED_FROM_SCORING = [
        "name",
        "email",  # Can reveal ethnicity
        "phone",  # Area codes can reveal location/demographics
        "address",
        "photo",
        "date_of_birth",
        "age",
        "gender",
        "marital_status",
        "nationality",
        "citizenship",
        "visa_status",
        "religion",
        "political_affiliation",
        "disability_status",
        "veteran_status",
        "pregnancy_status"
    ]
    
    # Fields that CAN be extracted but require careful handling
    SENSITIVE_CONTEXT_FIELDS = [
        "graduation_year",  # Age proxy - extract but don't score
        "school_names",      # Can correlate with demographics
        "organization_memberships",  # May reveal protected characteristics
        "languages",         # May reveal national origin (but can be job-relevant)
    ]
    
    async def process_resume(
        self,
        resume_file: bytes,
        job_requirements: JobRequirements,
        config: ResumeProcessingConfig
    ) -> ProcessedResume:
        """
        Extract and analyze resume with bias safeguards.
        """
        
        # Extract raw text and structure
        raw_extraction = await self._extract_resume_content(resume_file)
        
        # Separate fields by category
        scoring_fields = self._extract_scoring_fields(raw_extraction)
        context_fields = self._extract_context_fields(raw_extraction)
        excluded_fields = self._extract_excluded_fields(raw_extraction)
        
        # Analyze ONLY scoring fields against requirements
        requirement_matches = await self._match_requirements(
            scoring_fields=scoring_fields,
            requirements=job_requirements
        )
        
        # Log what was used vs. excluded
        processing_audit = ResumeProcessingAudit(
            fields_used_for_scoring=list(scoring_fields.keys()),
            fields_excluded_from_scoring=list(excluded_fields.keys()),
            fields_available_for_context=list(context_fields.keys()),
            requirement_match_details=requirement_matches,
            timestamp=datetime.utcnow()
        )
        
        return ProcessedResume(
            candidate_id=self._generate_anonymous_id(),
            scoring_data=scoring_fields,
            context_data=context_fields if config.include_context else None,
            requirement_matches=requirement_matches,
            processing_audit=processing_audit
        )
    
    def _extract_scoring_fields(self, raw: dict) -> dict:
        """Extract only fields safe for scoring."""
        
        return {
            "skills": raw.get("skills", []),
            "experience_descriptions": self._anonymize_experience(raw.get("experience", [])),
            "education_level": raw.get("education_level"),  # Degree type, not school
            "certifications": raw.get("certifications", []),
            "years_of_experience": self._calculate_experience_years(raw),
            "industries": raw.get("industries", []),
            "job_titles": raw.get("job_titles", []),
            "achievements": raw.get("achievements", [])
        }
    
    def _anonymize_experience(self, experiences: List[dict]) -> List[dict]:
        """Remove potentially identifying information from experience entries."""
        
        anonymized = []
        for exp in experiences:
            anonymized.append({
                "title": exp.get("title"),
                "description": exp.get("description"),
                "duration_months": exp.get("duration_months"),
                "industry": exp.get("industry"),
                # Explicitly exclude: company_name, location, specific dates
            })
        return anonymized
```

### 2.2 Interview Engine Safeguards

```python
# backend/app/services/interview_compliance.py

class InterviewComplianceGuard:
    """
    Ensure interview questions and analysis don't touch protected characteristics.
    """
    
    # Topics that should NEVER be probed
    PROHIBITED_TOPICS = [
        "age", "birth", "graduation year", "when did you",
        "married", "spouse", "children", "family", "pregnant",
        "religion", "church", "worship", "faith", "beliefs",
        "national origin", "citizenship", "visa", "where are you from",
        "disability", "health", "medical", "accommodation",
        "arrest", "criminal",  # Varies by jurisdiction
        "military", "veteran",  # Can be job-relevant in some contexts
        "political", "party", "vote",
        "union", "organize",
        "genetic", "DNA", "family medical history"
    ]
    
    # Phrases that might elicit protected information
    WARNING_PHRASES = [
        "tell me about yourself",  # Can elicit personal details
        "where did you grow up",
        "what are your hobbies",  # Can reveal religion, disability
        "do you have reliable transportation",  # Disability/economic proxy
        "can you work weekends",  # Religion proxy - rephrase as job requirement
    ]
    
    async def validate_probe(self, probe: Probe) -> ProbeValidation:
        """
        Validate that a probe doesn't touch prohibited topics.
        """
        
        probe_lower = probe.text.lower()
        
        # Check for prohibited topics
        violations = []
        for topic in self.PROHIBITED_TOPICS:
            if topic in probe_lower:
                violations.append(ProbeViolation(
                    type="PROHIBITED_TOPIC",
                    topic=topic,
                    severity="HIGH",
                    recommendation=f"Remove reference to '{topic}'"
                ))
        
        # Check for warning phrases
        warnings = []
        for phrase in self.WARNING_PHRASES:
            if phrase in probe_lower:
                warnings.append(ProbeWarning(
                    type="RISKY_PHRASE",
                    phrase=phrase,
                    severity="MEDIUM",
                    recommendation=f"Consider rephrasing to avoid eliciting protected information"
                ))
        
        return ProbeValidation(
            is_valid=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            probe_id=probe.id
        )
    
    async def validate_response_analysis(
        self,
        response_text: str,
        extracted_evidence: List[Evidence]
    ) -> AnalysisValidation:
        """
        Ensure response analysis doesn't incorporate protected information.
        """
        
        issues = []
        
        for evidence in extracted_evidence:
            # Check if evidence references protected characteristics
            for topic in self.PROHIBITED_TOPICS:
                if topic in evidence.source_text.lower():
                    issues.append(AnalysisIssue(
                        type="PROTECTED_INFO_IN_EVIDENCE",
                        evidence_id=evidence.id,
                        topic=topic,
                        action="EXCLUDE_FROM_SCORING",
                        rationale=f"Evidence references protected characteristic: {topic}"
                    ))
        
        return AnalysisValidation(
            is_clean=len(issues) == 0,
            issues=issues,
            action_taken=[i.action for i in issues]
        )
```

### 2.3 Scoring Safeguards

```python
# backend/app/services/scoring_compliance.py

class ScoringComplianceChecker:
    """
    Ensure scoring criteria and weights don't create prohibited discrimination.
    """
    
    # Traits that may have demographic correlations (research-based)
    DEMOGRAPHICALLY_SENSITIVE_TRAITS = {
        "ASSERTIVENESS": {
            "concern": "Gender correlations in perception",
            "mitigation": "Focus on behavioral outcomes, not style"
        },
        "COMMUNICATION": {
            "concern": "Cultural communication style differences",
            "mitigation": "Assess clarity of outcome, not style conformity"
        },
        "RISK_ORIENTATION": {
            "concern": "Age and gender correlations",
            "mitigation": "Contextualize to role requirements"
        }
    }
    
    async def validate_rubric_configuration(
        self,
        rubric: ScoringRubric,
        role_profile: RoleProfile
    ) -> RubricValidation:
        """
        Validate that rubric configuration is defensible.
        """
        
        issues = []
        recommendations = []
        
        # Check for over-reliance on sensitive traits
        sensitive_trait_weight = sum(
            item.importance_weight
            for item in rubric.items
            if item.trait_id in self.DEMOGRAPHICALLY_SENSITIVE_TRAITS
        )
        total_weight = sum(item.importance_weight for item in rubric.items)
        
        if sensitive_trait_weight / total_weight > 0.5:
            issues.append(RubricIssue(
                type="HIGH_SENSITIVE_TRAIT_WEIGHT",
                severity="MEDIUM",
                description="Over 50% of scoring weight is on demographically sensitive traits",
                recommendation="Consider whether all sensitive traits are essential for job performance"
            ))
        
        # Check for job-relatedness documentation
        for item in rubric.items:
            if not item.job_relatedness_rationale:
                issues.append(RubricIssue(
                    type="MISSING_JOB_RELATEDNESS",
                    severity="HIGH",
                    trait_id=item.trait_id,
                    description=f"No job-relatedness rationale for {item.trait_id}",
                    recommendation="Document why this trait is essential for job performance"
                ))
        
        # Check derivation documentation
        if rubric.source == "ORGANIZATIONAL" and not rubric.derivation_metadata:
            issues.append(RubricIssue(
                type="MISSING_DERIVATION_DOCUMENTATION",
                severity="MEDIUM",
                description="Organization-specific rubric lacks derivation documentation",
                recommendation="Document how rubric was derived from top performers"
            ))
        
        return RubricValidation(
            is_valid=len([i for i in issues if i.severity == "HIGH"]) == 0,
            issues=issues,
            recommendations=recommendations,
            validation_timestamp=datetime.utcnow()
        )
```

---

## Part 3: Disparate Impact Monitoring

### 3.1 Impact Ratio Calculation

```python
# backend/app/services/disparate_impact_monitor.py

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class ProtectedClass(Enum):
    GENDER = "gender"
    RACE_ETHNICITY = "race_ethnicity"
    AGE_GROUP = "age_group"
    # Note: Collecting this data is optional and requires consent

@dataclass
class ImpactRatio:
    """
    Four-Fifths Rule: Selection rate for protected group should be
    at least 80% of selection rate for highest-scoring group.
    """
    protected_class: ProtectedClass
    group_a: str
    group_b: str
    group_a_selection_rate: float
    group_b_selection_rate: float
    impact_ratio: float  # group_a_rate / group_b_rate
    passes_four_fifths: bool  # ratio >= 0.8
    sample_size_adequate: bool  # Statistical significance


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
    
    async def calculate_impact_ratios(
        self,
        organization_id: str,
        role_profile_id: Optional[str],
        date_range: tuple,
        protected_class: ProtectedClass
    ) -> List[ImpactRatio]:
        """
        Calculate selection rate ratios across demographic groups.
        """
        
        # Get assessment outcomes with demographic data (where provided)
        outcomes = await self._get_outcomes_with_demographics(
            organization_id=organization_id,
            role_profile_id=role_profile_id,
            date_range=date_range,
            protected_class=protected_class
        )
        
        # Group by demographic
        groups = self._group_by_demographic(outcomes, protected_class)
        
        # Calculate selection rates per group
        selection_rates = {}
        for group_name, group_outcomes in groups.items():
            selected = len([o for o in group_outcomes if o.recommendation in ["STRONG_HIRE", "HIRE"]])
            total = len(group_outcomes)
            selection_rates[group_name] = selected / total if total > 0 else 0
        
        # Find highest selection rate (reference group)
        max_rate = max(selection_rates.values()) if selection_rates else 0
        
        # Calculate impact ratios
        impact_ratios = []
        for group_name, rate in selection_rates.items():
            if max_rate > 0:
                ratio = rate / max_rate
            else:
                ratio = 1.0
            
            impact_ratios.append(ImpactRatio(
                protected_class=protected_class,
                group_a=group_name,
                group_b="highest_rate_group",
                group_a_selection_rate=rate,
                group_b_selection_rate=max_rate,
                impact_ratio=ratio,
                passes_four_fifths=ratio >= self.FOUR_FIFTHS_THRESHOLD,
                sample_size_adequate=len(groups.get(group_name, [])) >= self.MINIMUM_SAMPLE_SIZE
            ))
        
        return impact_ratios
    
    async def generate_impact_report(
        self,
        organization_id: str,
        date_range: tuple
    ) -> DisparateImpactReport:
        """
        Generate comprehensive disparate impact report.
        Required annually under NYC Local Law 144 and similar regulations.
        """
        
        report_sections = []
        
        for protected_class in ProtectedClass:
            ratios = await self.calculate_impact_ratios(
                organization_id=organization_id,
                role_profile_id=None,  # Org-wide
                date_range=date_range,
                protected_class=protected_class
            )
            
            # Determine if any group fails four-fifths
            failing_groups = [r for r in ratios if not r.passes_four_fifths and r.sample_size_adequate]
            
            section = ImpactReportSection(
                protected_class=protected_class,
                impact_ratios=ratios,
                has_disparate_impact=len(failing_groups) > 0,
                failing_groups=failing_groups,
                sample_sizes={r.group_a: r.sample_size_adequate for r in ratios},
                recommendations=self._generate_recommendations(failing_groups)
            )
            report_sections.append(section)
        
        return DisparateImpactReport(
            organization_id=organization_id,
            report_period=date_range,
            generated_at=datetime.utcnow(),
            sections=report_sections,
            overall_assessment=self._assess_overall(report_sections),
            required_actions=self._determine_required_actions(report_sections)
        )
    
    def _generate_recommendations(
        self,
        failing_groups: List[ImpactRatio]
    ) -> List[str]:
        """Generate recommendations for addressing disparate impact."""
        
        recommendations = []
        
        if failing_groups:
            recommendations.append(
                "Review trait weights and thresholds for job-relatedness"
            )
            recommendations.append(
                "Consider alternative assessment criteria with lower adverse impact"
            )
            recommendations.append(
                "Document business necessity for current criteria"
            )
            recommendations.append(
                "Consult with employment counsel before making changes"
            )
        
        return recommendations
```

### 3.2 Continuous Monitoring Dashboard

```python
# backend/app/api/v1/compliance.py

@router.get("/compliance/impact-dashboard")
async def get_impact_dashboard(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> ImpactDashboard:
    """
    Get real-time disparate impact monitoring dashboard.
    
    Shows:
    - Current impact ratios by protected class
    - Trend over time
    - Alerts for threshold violations
    - Recommendations
    """
    
    monitor = DisparateImpactMonitor()
    
    # Current period (last 12 months)
    current_ratios = await monitor.calculate_all_ratios(
        organization_id=organization_id,
        date_range=(datetime.utcnow() - timedelta(days=365), datetime.utcnow())
    )
    
    # Trend (quarterly for last 2 years)
    trends = await monitor.calculate_trends(
        organization_id=organization_id,
        periods=8,
        period_length_days=90
    )
    
    # Active alerts
    alerts = [
        ImpactAlert(
            protected_class=ratio.protected_class,
            group=ratio.group_a,
            current_ratio=ratio.impact_ratio,
            threshold=0.8,
            severity="HIGH" if ratio.impact_ratio < 0.7 else "MEDIUM"
        )
        for ratio in current_ratios
        if not ratio.passes_four_fifths and ratio.sample_size_adequate
    ]
    
    return ImpactDashboard(
        current_ratios=current_ratios,
        trends=trends,
        alerts=alerts,
        last_full_audit=await get_last_audit_date(organization_id),
        next_audit_due=calculate_next_audit_due(organization_id)
    )
```

---

## Part 4: Audit Trail Requirements

### 4.1 Comprehensive Audit Schema

```python
# backend/app/models/compliance_audit.py

class AssessmentAuditRecord(Base):
    """
    Complete audit record for every assessment decision.
    Designed to answer: "Why did this candidate receive this score?"
    """
    
    __tablename__ = "assessment_audit_records"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID, ForeignKey("assessment_reports.id"))
    
    # What was assessed
    candidate_id = Column(UUID, ForeignKey("candidates.id"))
    role_profile_id = Column(UUID, ForeignKey("role_profiles.id"))
    rubric_id = Column(UUID, ForeignKey("scoring_rubrics.id"))
    rubric_version = Column(String(50))
    
    # Rubric derivation chain
    rubric_source = Column(String(50))  # RESEARCH_DEFAULT, ORGANIZATIONAL, ADJUSTED
    rubric_derivation_trace = Column(JSONB)  # Full chain to research/extraction
    
    # For each trait
    trait_audit_records = Column(JSONB)  # Array of TraitAuditRecord
    
    # Final decision
    composite_score = Column(Float)
    recommendation = Column(String(50))
    recommendation_explanation = Column(Text)
    
    # Compliance metadata
    protected_info_excluded = Column(JSONB)  # What was explicitly excluded
    compliance_checks_passed = Column(JSONB)  # Which validations ran
    
    # Timestamps and actors
    assessed_at = Column(DateTime(timezone=True))
    assessed_by = Column(UUID, ForeignKey("users.id"))  # Or "SYSTEM"
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class TraitAuditRecord(TypedDict):
    """Audit record for a single trait assessment."""
    
    trait_id: str
    
    # Scoring
    raw_score: int
    calibrated_score: int
    confidence: float
    
    # Evidence chain
    evidence_items: List[EvidenceAuditRecord]
    
    # Scoring rationale
    matched_behavioral_anchors: List[str]
    scoring_criteria_applied: str
    score_explanation: str
    
    # Rubric item traceability
    rubric_item_id: str
    rubric_item_source: str  # RESEARCH or EXTRACTED
    job_relatedness_rationale: str
    
    # If research-based
    research_citations: Optional[List[str]]
    
    # If extraction-based
    extraction_session_ids: Optional[List[str]]
    top_performer_ids: Optional[List[str]]


class EvidenceAuditRecord(TypedDict):
    """Audit record for a single piece of evidence."""
    
    evidence_id: str
    
    # Source
    source_type: str  # BEHAVIORAL, HYPOTHETICAL, etc.
    source_exchange_id: str  # Links to interview transcript
    source_text: str  # Verbatim (for audit purposes)
    
    # Classification
    classification_rationale: str
    weight_applied: float
    weight_rationale: str
    
    # Compliance
    protected_info_detected: bool
    protected_info_excluded: bool
    exclusion_rationale: Optional[str]
```

### 4.2 Audit Trail API

```python
# backend/app/api/v1/audit.py

@router.get("/audit/assessment/{assessment_id}/full-trace")
async def get_full_assessment_trace(
    assessment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> FullAssessmentTrace:
    """
    Get complete audit trail for an assessment.
    
    Includes:
    - Every question asked and why
    - Every response and how it was scored
    - Every piece of evidence and its weight
    - Rubric derivation chain
    - Compliance checks performed
    - What information was excluded and why
    """
    
    audit_record = await get_audit_record(db, assessment_id)
    
    return FullAssessmentTrace(
        assessment_id=assessment_id,
        candidate_id=audit_record.candidate_id,
        
        # Rubric chain
        rubric_trace=RubricTrace(
            rubric_id=audit_record.rubric_id,
            rubric_source=audit_record.rubric_source,
            derivation_chain=audit_record.rubric_derivation_trace,
            job_relatedness_documentation=await get_job_relatedness_docs(
                audit_record.rubric_id
            )
        ),
        
        # Trait-by-trait breakdown
        trait_traces=[
            TraitTrace(
                trait_id=t["trait_id"],
                score=t["calibrated_score"],
                evidence_chain=t["evidence_items"],
                scoring_rationale=t["score_explanation"],
                rubric_item_trace=RubricItemTrace(
                    source=t["rubric_item_source"],
                    research_citations=t.get("research_citations"),
                    extraction_sessions=t.get("extraction_session_ids")
                )
            )
            for t in audit_record.trait_audit_records
        ],
        
        # Compliance documentation
        compliance_trace=ComplianceTrace(
            protected_info_handling=audit_record.protected_info_excluded,
            compliance_checks=audit_record.compliance_checks_passed,
            interview_compliance=await get_interview_compliance_record(assessment_id)
        ),
        
        # Final decision
        decision_trace=DecisionTrace(
            composite_score=audit_record.composite_score,
            recommendation=audit_record.recommendation,
            explanation=audit_record.recommendation_explanation,
            counter_indicators_flagged=await get_counter_indicator_flags(assessment_id)
        )
    )


@router.get("/audit/rubric/{rubric_id}/derivation-chain")
async def get_rubric_derivation_chain(
    rubric_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
) -> RubricDerivationChain:
    """
    Get complete derivation chain for a rubric.
    
    Answers: "How was this rubric created and why are these the criteria?"
    """
    
    rubric = await get_rubric(db, rubric_id)
    
    if rubric.source == "RESEARCH_DEFAULT":
        return RubricDerivationChain(
            rubric_id=rubric_id,
            source="RESEARCH_DEFAULT",
            research_basis=ResearchBasis(
                traits=[
                    TraitResearchBasis(
                        trait_id=item.trait_id,
                        research_foundation=item.research_foundation,
                        citations=item.citations,
                        validation_studies=item.validation_studies
                    )
                    for item in rubric.items
                ]
            )
        )
    
    elif rubric.source == "ORGANIZATIONAL":
        extraction_sessions = await get_extraction_sessions(rubric.derivation_metadata)
        
        return RubricDerivationChain(
            rubric_id=rubric_id,
            source="ORGANIZATIONAL",
            extraction_basis=ExtractionBasis(
                top_performers=[
                    TopPerformerSummary(
                        id=tp.id,
                        role_category=tp.role_category,
                        tenure_months=tp.tenure_months,
                        session_count=len([s for s in extraction_sessions if s.top_performer_id == tp.id])
                    )
                    for tp in await get_top_performers(extraction_sessions)
                ],
                sessions=[
                    SessionSummary(
                        id=s.id,
                        scenarios_used=len(s.scenarios),
                        signals_extracted=len(s.extracted_signals),
                        date=s.completed_at
                    )
                    for s in extraction_sessions
                ],
                synthesis_method=rubric.derivation_metadata.get("synthesis_method"),
                job_relatedness_documentation=rubric.derivation_metadata.get("job_relatedness")
            )
        )
```

---

## Part 5: Required Disclosures

### 5.1 Candidate Disclosure

```python
# backend/app/services/disclosure_generator.py

class CandidateDisclosureGenerator:
    """
    Generate required disclosures for candidates about AI assessment.
    """
    
    def generate_pre_assessment_disclosure(
        self,
        organization: Organization,
        role_profile: RoleProfile,
        jurisdiction: str
    ) -> CandidateDisclosure:
        """
        Generate disclosure required before AI assessment.
        
        Required by:
        - Illinois AI Video Interview Act
        - NYC Local Law 144
        - Various state laws
        - GDPR Article 22 (for EU candidates)
        """
        
        disclosure = CandidateDisclosure(
            title="Notice Regarding AI-Assisted Assessment",
            
            sections=[
                DisclosureSection(
                    heading="What We Use",
                    content=f"""
                    {organization.name} uses an AI-assisted assessment tool to help 
                    evaluate candidates for the {role_profile.name} position. This tool 
                    analyzes your responses to behavioral interview questions to assess 
                    job-relevant traits.
                    """
                ),
                
                DisclosureSection(
                    heading="What We Assess",
                    content=f"""
                    The assessment evaluates the following job-relevant characteristics:
                    {', '.join([t.name for t in role_profile.traits])}
                    
                    These characteristics were determined to be relevant to success in 
                    this role based on {self._describe_rubric_source(role_profile)}.
                    """
                ),
                
                DisclosureSection(
                    heading="How It Works",
                    content="""
                    During the assessment, you will be asked behavioral interview questions 
                    about your past experiences. The AI analyzes your responses to identify 
                    evidence of job-relevant characteristics. A human reviewer will also 
                    review the assessment results before any hiring decision is made.
                    """
                ),
                
                DisclosureSection(
                    heading="What We Don't Consider",
                    content="""
                    The assessment does NOT consider or score based on:
                    - Your name, gender, age, race, ethnicity, or national origin
                    - Your religion, disability status, or other protected characteristics
                    - The schools you attended or your graduation dates
                    - Any information not directly related to job performance
                    """
                ),
                
                DisclosureSection(
                    heading="Your Rights",
                    content=self._generate_rights_section(jurisdiction)
                ),
                
                DisclosureSection(
                    heading="Questions or Accommodations",
                    content=f"""
                    If you have questions about this assessment or need accommodations, 
                    please contact {organization.hr_contact_email}.
                    """
                )
            ],
            
            consent_required=self._requires_consent(jurisdiction),
            consent_text="I acknowledge that I have read and understand this notice about AI-assisted assessment." if self._requires_consent(jurisdiction) else None,
            
            jurisdiction_specific_additions=self._get_jurisdiction_additions(jurisdiction)
        )
        
        return disclosure
    
    def _generate_rights_section(self, jurisdiction: str) -> str:
        """Generate jurisdiction-specific rights disclosure."""
        
        base_rights = """
        You have the right to:
        - Request information about how the assessment works
        - Request that a human review any automated decision
        - Withdraw from the assessment process at any time
        """
        
        if jurisdiction == "NYC":
            base_rights += """
        
        Under NYC Local Law 144:
        - You may request an alternative selection process
        - You may access the most recent bias audit summary
        """
        
        if jurisdiction in ["CA", "EU"]:
            base_rights += """
        
        - You may request a copy of the information used in your assessment
        - You may request deletion of your assessment data
        """
        
        return base_rights
```

### 5.2 Organization Disclosure Requirements

```python
# backend/app/services/organization_compliance.py

class OrganizationComplianceChecker:
    """
    Check and enforce organization compliance requirements.
    """
    
    REQUIRED_DOCUMENTATION = [
        "job_relatedness_rationale",
        "rubric_derivation_documentation", 
        "bias_audit_report",
        "candidate_disclosure_template",
        "data_retention_policy"
    ]
    
    async def check_compliance_status(
        self,
        organization_id: str
    ) -> ComplianceStatus:
        """
        Check organization's compliance status.
        """
        
        missing_docs = []
        warnings = []
        
        for doc_type in self.REQUIRED_DOCUMENTATION:
            if not await self._has_documentation(organization_id, doc_type):
                missing_docs.append(doc_type)
        
        # Check bias audit recency
        last_audit = await self._get_last_bias_audit(organization_id)
        if last_audit is None:
            warnings.append("No bias audit on record")
        elif (datetime.utcnow() - last_audit.date).days > 365:
            warnings.append("Bias audit is more than 12 months old")
        
        # Check rubric documentation
        rubrics = await self._get_active_rubrics(organization_id)
        for rubric in rubrics:
            if not rubric.job_relatedness_documented:
                warnings.append(f"Rubric {rubric.id} missing job-relatedness documentation")
        
        return ComplianceStatus(
            is_compliant=len(missing_docs) == 0,
            missing_documentation=missing_docs,
            warnings=warnings,
            last_audit_date=last_audit.date if last_audit else None,
            next_audit_due=self._calculate_next_audit_due(last_audit)
        )
```

---

## Part 6: Customer Responsibility Disclaimer

### 6.1 Terms of Service Language

```
AP API CUSTOMER RESPONSIBILITY AGREEMENT

1. COMPLIANCE RESPONSIBILITY

Customer acknowledges and agrees that:

a) Customer is solely responsible for ensuring that its use of the AP API 
   complies with all applicable employment laws, including but not limited to 
   Title VII of the Civil Rights Act, the Age Discrimination in Employment 
   Act, the Americans with Disabilities Act, and applicable state and local 
   laws.

b) Customer is responsible for configuring assessment criteria (traits, 
   weights, thresholds) in a manner that is job-related and consistent with 
   business necessity.

c) Customer is responsible for documenting the job-relatedness of all 
   assessment criteria used.

d) Customer is responsible for monitoring assessment outcomes for disparate 
   impact and taking appropriate action if disparate impact is identified.

e) Customer is responsible for providing required disclosures to candidates 
   and obtaining any required consent.

2. SYSTEM CAPABILITIES AND LIMITATIONS

AP API provides:
- Research-based default rubrics with documented validity
- Tools for deriving organization-specific rubrics from top performer analysis
- Bias monitoring and disparate impact reporting tools
- Complete audit trails for all assessment decisions
- Technical safeguards against use of protected characteristics in scoring

AP API does NOT:
- Guarantee that any particular configuration will be compliant with 
  applicable law
- Provide legal advice regarding employment practices
- Make hiring decisions (Customer retains all hiring decision authority)
- Ensure that Customer's chosen criteria are job-related

3. RECOMMENDED PRACTICES

Anthropic recommends that Customer:
- Consult with employment counsel regarding assessment practices
- Document job-relatedness rationale for all trait configurations
- Conduct regular disparate impact analyses
- Maintain human review of AI-assisted recommendations
- Provide candidates with required disclosures and accommodation options
```

### 6.2 In-App Warnings

```python
# backend/app/services/configuration_warnings.py

class ConfigurationWarningGenerator:
    """
    Generate warnings when customers configure potentially problematic settings.
    """
    
    async def check_configuration(
        self,
        role_profile: RoleProfile,
        rubric: ScoringRubric
    ) -> List[ConfigurationWarning]:
        """
        Check for potentially problematic configurations and warn.
        """
        
        warnings = []
        
        # Check for high weight on demographically sensitive traits
        for item in rubric.items:
            if item.trait_id in DEMOGRAPHICALLY_SENSITIVE_TRAITS:
                if item.importance_weight >= 4:
                    warnings.append(ConfigurationWarning(
                        severity="MEDIUM",
                        trait_id=item.trait_id,
                        message=f"'{item.trait_id}' has high weight and may have demographic correlations. Ensure this trait is essential for job performance and document your rationale.",
                        action_required=False,
                        documentation_recommended=True
                    ))
        
        # Check for missing job-relatedness documentation
        if not role_profile.job_relatedness_documentation:
            warnings.append(ConfigurationWarning(
                severity="HIGH",
                message="This role profile does not have job-relatedness documentation. This documentation is important for legal defensibility.",
                action_required=True,
                link_to_documentation="/docs/job-relatedness"
            ))
        
        # Check for very high minimum thresholds
        high_threshold_traits = [
            item for item in rubric.items 
            if item.minimum_threshold >= 4
        ]
        if len(high_threshold_traits) > 3:
            warnings.append(ConfigurationWarning(
                severity="MEDIUM",
                message=f"You have {len(high_threshold_traits)} traits with minimum threshold of 4+. Very high thresholds may reduce candidate pool and increase disparate impact risk.",
                action_required=False
            ))
        
        return warnings
```

---

## Part 7: Implementation Checklist

### 7.1 Technical Implementation

```
□ Resume Processing
  □ Implement field exclusion for protected characteristics
  □ Log what fields were used vs. excluded
  □ Create anonymization option for customers who want it

□ Interview Engine
  □ Implement probe validation against prohibited topics
  □ Implement response analysis filtering for protected info
  □ Log all compliance checks performed

□ Scoring Engine
  □ Implement rubric validation for job-relatedness
  □ Create warnings for sensitive trait configurations
  □ Document scoring algorithm version

□ Audit Infrastructure
  □ Implement full assessment audit records
  □ Implement rubric derivation chain tracking
  □ Create audit trail API endpoints

□ Disparate Impact Monitoring
  □ Implement voluntary demographic data collection (separate from scoring)
  □ Implement impact ratio calculation
  □ Create monitoring dashboard
  □ Implement annual report generation

□ Disclosures
  □ Implement candidate disclosure generator
  □ Implement jurisdiction-specific variations
  □ Create consent flow for required jurisdictions
```

### 7.2 Documentation Requirements

```
□ For Each Role Profile
  □ Job-relatedness rationale for each trait
  □ Documentation of how traits were selected
  □ Business necessity justification

□ For Each Rubric
  □ Derivation chain documentation
  □ Research citations (if research-based)
  □ Extraction methodology (if organization-specific)
  □ Version history

□ Organization-Level
  □ Bias audit reports (annual minimum)
  □ Candidate disclosure templates
  □ Data retention policy
  □ Accommodation procedure
```

---

## Summary

This compliance framework provides:

1. **Technical Safeguards**: Resume field exclusion, interview compliance guards, scoring validation
2. **Monitoring**: Real-time disparate impact tracking with four-fifths rule alerts
3. **Audit Trails**: Complete chain from rubric derivation through individual scoring decisions
4. **Disclosures**: Jurisdiction-appropriate candidate notices
5. **Customer Guidance**: Clear responsibility delineation and configuration warnings

**Your position is correct**: You provide the tools and safeguards; customers are responsible for compliant configuration. The transparency and audit infrastructure makes this defensible—you can show exactly what the system considered and didn't consider.

---

*Document Version 1.0 | AP API Compliance & Bias Monitoring Framework*
*© 2026 Tucuxi Inc. All rights reserved.*
