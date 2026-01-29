export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  is_superuser: boolean;
  organization_id: string | null;
  phone: string | null;
  title: string | null;
  bio: string | null;
  created_at: string;
  updated_at: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  website: string | null;
  industry: string | null;
  size: string | null;
  is_active: boolean;
  settings: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface Trait {
  id: string;
  name: string;
  category: string;
  definition: string;
  spectrum_low_label: string;
  spectrum_high_label: string;
  behavioral_markers_low: string[];
  behavioral_markers_high: string[];
  counter_indicator_for: string[];
  display_order: number;
  created_at: string;
  updated_at: string;
}

export interface TraitValenceMapping {
  id: string;
  role_category: string;
  valence: string;
  optimal_range_min: number;
  optimal_range_max: number;
  rationale: string;
  notes: string | null;
}

export interface TraitDetail extends Trait {
  valence_mappings: TraitValenceMapping[];
}

export interface RoleProfile {
  id: string;
  name: string;
  description: string | null;
  department: string | null;
  level: string | null;
  role_category: string;
  organization_id: string | null;
  critical_traits: TraitRequirement[];
  positive_traits: TraitRequirement[];
  counter_indicators: CounterIndicator[];
  valence_notes: Record<string, string> | null;
  is_template: boolean;
  is_active: boolean;
  derived_from: string | null;
  derivation_notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface RoleTemplateCategory {
  name: string;
  templates: RoleProfile[];
}

export interface RoleTemplatesByCategory {
  categories: RoleTemplateCategory[];
  total: number;
}

export interface TraitRequirement {
  trait_id: string;
  level: string;
  weight: number;
}

export interface CounterIndicator {
  trait_id: string;
  threshold: string;
  reason: string;
}

export interface ScoringRubric {
  id: string;
  name: string;
  description: string | null;
  trait_id: string;
  organization_id: string | null;
  role_profile_id: string | null;
  version: number;
  behavioral_anchors: Record<string, BehavioralAnchor>;
  primary_probes: Probe[];
  follow_up_probes: Record<string, string[]>;
  star_indicators: Record<string, string[]> | null;
  is_default: boolean;
  is_active: boolean;
  derived_from: string | null;
  derivation_notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface BehavioralAnchor {
  label: string;
  description: string;
  indicators: string[];
}

export interface Probe {
  question: string;
  purpose: string;
  star_focus: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  organization_id?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
}

// --- Candidate Types ---

export type CandidateStatus =
  | 'NEW'
  | 'SCREENING'
  | 'INTERVIEWING'
  | 'ASSESSED'
  | 'OFFER'
  | 'HIRED'
  | 'REJECTED'
  | 'WITHDRAWN';

export interface Candidate {
  id: string;
  organization_id: string;
  role_profile_id: string | null;
  email: string;
  full_name: string;
  phone: string | null;
  current_title: string | null;
  current_company: string | null;
  linkedin_url: string | null;
  years_experience: number | null;
  source: string | null;
  referrer: string | null;
  status: CandidateStatus;
  notes: string | null;
  tags: string[];
  custom_fields: Record<string, unknown> | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// --- Interview Types ---

export type InterviewStatus = 'NOT_STARTED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';

export type ProbeType =
  | 'INTRODUCTION'
  | 'PRIMARY'
  | 'FOLLOW_UP'
  | 'RECURSION'
  | 'REFLECTION'
  | 'CONFLICT'
  | 'CLOSING'
  | 'COMPLETE';

export type ProbePhase = 'PRIMARY' | 'FOLLOW_UP' | 'RECURSION' | 'REFLECTION' | 'CONFLICT' | 'COMPLETE';

export type EvidenceType = 'BEHAVIORAL' | 'HYPOTHETICAL' | 'SELF_REPORT' | 'OBSERVED';

export type Recommendation = 'STRONG_HIRE' | 'HIRE' | 'HOLD' | 'NO_HIRE';

export interface InterviewConfigRequest {
  max_duration_minutes?: number;
  max_follow_ups_per_trait?: number;
  confidence_threshold_for_recursion?: number;
  require_reflection?: boolean;
  enable_resume_customization?: boolean;
  enable_conflict_probing?: boolean;
}

export interface StartInterviewRequest {
  candidate_id: string;
  rubric_id?: string;
  trait_ids?: string[];
  config?: InterviewConfigRequest;
}

export interface TraitProgress {
  trait_id: string;
  trait_name: string;
  phase: ProbePhase;
  probes_used: number;
  evidence_count: number;
  behavioral_evidence_count: number;
  confidence: number;
  star_coverage: Record<string, boolean>;
  has_conflict_example: boolean;
  raw_score: number | null;
  is_complete: boolean;
}

export interface InterviewPromptResponse {
  session_id: string;
  next_prompt: string;
  prompt_type: ProbeType;
  trait_id: string | null;
  trait_name: string | null;
  trait_progress: TraitProgress | null;
  overall_progress: number;
  can_end_interview: boolean;
  interview_complete: boolean;
}

export interface CandidateResponseRequest {
  response_text: string;
}

export interface InterviewSession {
  id: string;
  candidate_id: string;
  status: InterviewStatus;
  session_type: string;
  started_at: string | null;
  completed_at: string | null;
  duration_minutes: number | null;
  target_traits: string[];
  overall_progress: number;
  traits_completed: number;
  traits_total: number;
}

export interface InterviewExchange {
  prompt: string;
  prompt_type: ProbeType;
  trait_id: string | null;
  response: string;
  timestamp: string;
}

export interface EvidenceItem {
  id: string;
  trait_id: string;
  source_type: EvidenceType;
  source_text: string;
  weight: number;
  trait_signal: string;
  signal_strength: number;
  star_components: {
    situation: boolean;
    task: boolean;
    action: boolean;
    result: boolean;
  };
  contains_conflict: boolean;
  contains_failure: boolean;
}

// --- Assessment Types ---

export interface TraitScoreResponse {
  trait_id: string;
  trait_name: string;
  raw_score: number;
  calibrated_score: number;
  confidence: number;
  explanation: string;
  evidence_summary: string;
  signal_gaps: string[];
}

export interface StrengthItem {
  trait_name: string;
  score: number;
  evidence: string;
}

export interface DevelopmentArea {
  trait_name: string;
  score: number;
  recommendation: string;
}

export interface CounterIndicatorFlag {
  trait_name: string;
  threshold: string;
  actual_score: number;
  reason: string;
  severity: 'WARNING' | 'CRITICAL';
}

export interface AssessmentSummaryResponse {
  session_id: string;
  candidate_id: string;
  recommendation: Recommendation;
  recommendation_rationale: string;
  composite_score: number;
  evidence_quality: string;
  confidence: number;
  trait_scores: TraitScoreResponse[];
  key_strengths: StrengthItem[];
  development_areas: DevelopmentArea[];
  counter_indicator_flags: CounterIndicatorFlag[];
  assessment_summary: string;
}

// --- Compliance Types ---

export type ProtectedClass = 'gender' | 'race_ethnicity' | 'age_group' | 'disability' | 'veteran_status';

export interface ImpactRatio {
  protected_class: string;
  group_a: string;
  group_b: string;
  group_a_selection_rate: number;
  group_b_selection_rate: number;
  impact_ratio: number;
  passes_four_fifths: boolean;
  sample_size_adequate: boolean;
  group_a_sample_size: number;
  group_b_sample_size: number;
}

export interface ImpactDashboardAlert {
  protected_class: string;
  group: string;
  current_ratio: number;
  threshold: number;
  severity: 'MEDIUM' | 'HIGH';
}

export interface ImpactDashboardResponse {
  current_ratios: ImpactRatio[];
  trends: Record<string, unknown>[];
  alerts: ImpactDashboardAlert[];
  last_full_audit: string | null;
  next_audit_due: string | null;
}

export interface DisparateImpactReport {
  id: string;
  organization_id: string;
  period_start: string;
  period_end: string;
  report_type: string;
  total_assessments: number;
  assessments_with_demographics: number;
  has_disparate_impact: boolean;
  overall_assessment: string | null;
  recommendations: string[];
  required_actions: string[];
  created_at: string;
}

export interface ComplianceStatus {
  organization_id: string;
  is_compliant: boolean;
  missing_documentation: string[];
  warnings: string[];
  last_audit_date: string | null;
  next_audit_due: string | null;
  rubric_validation_issues: number;
  pending_disclosures: number;
}

export interface CandidateDisclosure {
  id: string;
  candidate_id: string;
  interview_session_id: string | null;
  organization_id: string;
  disclosure_type: string;
  disclosure_version: string;
  jurisdiction: string | null;
  consent_required: boolean;
  consent_given: boolean | null;
  consent_given_at: string | null;
  shown_at: string;
  acknowledged_at: string | null;
}

export interface DisclosureSection {
  heading: string;
  content: string;
}

export interface DisclosureContent {
  title: string;
  sections: DisclosureSection[];
  consent_required: boolean;
  consent_text: string | null;
  jurisdiction: string | null;
}

// --- Profile Development Types ---

export type ProfilingStatus = 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'ARCHIVED';
export type TrainingSessionStatus = 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
export type ProfilingPhase = 'NOT_STARTED' | 'INTRODUCTION' | 'RAPPORT_BUILDING' | 'TRAIT_EXPLORATION' | 'DEEP_DIVE' | 'REFLECTION' | 'CLOSING' | 'COMPLETED';

export interface TopPerformer {
  id: string;
  organization_id: string;
  name: string | null;
  employee_id: string | null;
  email: string | null;
  is_anonymized: boolean;
  job_title: string;
  department: string | null;
  role_category: string;
  tenure_months: number | null;
  performance_metrics: Record<string, unknown> | null;
  profiling_status: ProfilingStatus;
  trait_profile: Record<string, TraitProfileData> | null;
  counter_indicators_identified: CounterIndicatorEvidence[];
  notes: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface TraitProfileData {
  scores: number[];
  evidence: string[];
  average_score: number | null;
  confidence: number;
}

export interface CounterIndicatorEvidence {
  trait_id: string;
  context: string;
  evidence: string;
  severity?: string;
}

export interface TopPerformerCreate {
  name?: string;
  employee_id?: string;
  email?: string;
  job_title: string;
  department?: string;
  role_category: string;
  tenure_months?: number;
  performance_metrics?: Record<string, unknown>;
  is_anonymized?: boolean;
  notes?: string;
}

export interface TrainingSession {
  id: string;
  top_performer_id: string;
  interviewer_id: string | null;
  session_number: number;
  status: TrainingSessionStatus;
  scheduled_at: string | null;
  started_at: string | null;
  completed_at: string | null;
  duration_minutes: number | null;
  target_traits: string[];
  focus_areas: string | null;
  ai_summary: string | null;
  created_at: string;
  updated_at: string;
}

export interface TrainingSessionDetail extends TrainingSession {
  transcript: TrainingExchange[];
  extracted_evidence: ExtractedEvidence[];
  trait_signals: TraitSignal[];
  counter_indicators_mentioned: CounterIndicatorMention[];
  interviewer_notes: string | null;
}

export interface TrainingExchange {
  role: 'interviewer' | 'performer';
  content: string;
  timestamp: string;
}

export interface ExtractedEvidence {
  trait_id: string;
  evidence_type: string;
  text: string;
  confidence: number;
}

export interface TraitSignal {
  trait_id: string;
  signal: 'positive' | 'negative' | 'neutral';
  strength: number;
  source: string;
}

export interface CounterIndicatorMention {
  trait_id: string;
  context: string;
  quote: string;
}

export interface ProfilingStartRequest {
  top_performer_id: string;
  target_traits: string[];
  role_context?: Record<string, unknown>;
}

export interface ProfilingPromptResponse {
  session_id: string;
  phase: ProfilingPhase;
  prompt_text: string;
  progress: ProfilingProgress;
  trait_being_explored: string | null;
  is_complete: boolean;
}

export interface ProfilingProgress {
  current_trait_index: number;
  total_traits: number;
  exchanges_count: number;
  traits_explored: string[];
}

export interface ProfilingCompleteResponse {
  session_id: string;
  summary: string;
  traits_profiled: string[];
  signals_extracted: number;
  patterns_identified: number;
  counter_indicators_found: number;
}

export interface ExtractedSignal {
  trait_id: string;
  trait_name: string;
  signal_type: 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL';
  strength: number;
  evidence_text: string;
  behavioral_indicator: string;
  context: string;
  confidence: number;
}

export interface BehavioralPattern {
  trait_id: string;
  trait_name: string;
  pattern_description: string;
  frequency: 'ALWAYS' | 'OFTEN' | 'SOMETIMES' | 'RARELY';
  example_quotes: string[];
  implications_for_role: string;
}

export interface TraitExtractionResult {
  session_id: string;
  top_performer_id: string;
  extracted_signals: ExtractedSignal[];
  behavioral_patterns: BehavioralPattern[];
  counter_indicators: CounterIndicatorSignal[];
  trait_scores: Record<string, TraitScoreData>;
  summary: string;
}

export interface CounterIndicatorSignal {
  trait_id: string;
  trait_name: string;
  context: string;
  evidence: string;
  role_categories_affected: string[];
  severity: 'LOW' | 'MEDIUM' | 'HIGH';
}

export interface TraitScoreData {
  trait_name: string;
  score: number | null;
  confidence: number;
  evidence_count: number;
  positive_signals: number;
  negative_signals: number;
}

export interface RubricGenerationRequest {
  role_category: string;
  top_performer_ids: string[];
  target_trait_ids: string[];
  role_context?: Record<string, unknown>;
  base_rubric_id?: string;
}

export interface GeneratedBehavioralAnchor {
  score: number;
  description: string;
  example_behaviors: string[];
  evidence_indicators: string[];
}

export interface GeneratedRubricItem {
  trait_id: string;
  trait_name: string;
  behavioral_anchors: GeneratedBehavioralAnchor[];
  primary_probes: string[];
  follow_up_probes: string[];
  star_indicators: Record<string, string[]>;
  job_relatedness_rationale: string;
  derivation_notes: string;
  confidence: number;
}

export interface GeneratedRubric {
  name: string;
  description: string;
  organization_id: string;
  role_category: string;
  items: GeneratedRubricItem[];
  derivation_metadata: Record<string, unknown>;
  research_basis: string | null;
  created_at: string;
}

export interface ProfileSynthesisRequest {
  top_performer_ids: string[];
  role_category: string;
}

export interface SynthesizedPattern {
  trait_id: string;
  trait_name: string;
  patterns: BehavioralPattern[];
  average_score: number | null;
  confidence: number;
}

export interface ProfileSynthesisResponse {
  role_category: string;
  top_performer_count: number;
  synthesized_patterns: SynthesizedPattern[];
  common_strengths: string[];
  role_success_indicators: string[];
  generated_at: string;
}

// --- Self-Service/Invitation Types ---

export type InvitationType = 'CANDIDATE_INTERVIEW' | 'TOP_PERFORMER_PROFILING';
export type InvitationStatus = 'PENDING' | 'VIEWED' | 'IN_PROGRESS' | 'COMPLETED' | 'EXPIRED' | 'REVOKED';

export interface InvitationValidateResponse {
  valid: boolean;
  invitation_type: InvitationType | null;
  recipient_name: string | null;
  organization_name: string | null;
  role_name: string | null;
  custom_message: string | null;
  expires_at: string | null;
  error: string | null;
}

export interface DisclosureSection {
  heading: string;
  content: string;
}

export interface DisclosureResponse {
  title: string;
  sections: DisclosureSection[];
  consent_required: boolean;
  consent_text: string | null;
  jurisdiction: string | null;
}

export interface SelfServiceSessionResponse {
  session_id: string;
  session_type: 'interview' | 'profiling';
  next_prompt: string;
  prompt_type: string;
  trait_name: string | null;
  overall_progress: number;
  is_complete: boolean;
}

// --- Job Types ---

export type JobStatus = 'DRAFT' | 'OPEN' | 'CLOSED' | 'ON_HOLD';

export interface ObjectiveRequirement {
  id: string;
  type: 'education' | 'experience' | 'certification' | 'skill' | 'other';
  requirement: string;
  required: boolean;
}

export interface NiceToHave {
  description: string;
}

export interface Job {
  id: string;
  organization_id: string;
  role_profile_id: string | null;
  title: string;
  description: string;
  department: string | null;
  location: string | null;
  employment_type: string | null;
  objective_requirements: ObjectiveRequirement[];
  nice_to_haves: NiceToHave[];
  responsibilities: string[];
  suggested_traits: string[];
  status: JobStatus;
  created_by_id: string | null;
  requirements_extracted_at: string | null;
  extraction_model: string | null;
  created_at: string;
  updated_at: string;
}

export interface JobWithRoleProfile extends Job {
  role_profile_name: string | null;
  role_profile_category: string | null;
}

// --- Resume Types ---

export type ResumeParseStatus = 'PENDING' | 'PARSING' | 'PARSED' | 'FAILED';

export interface ParsedExperience {
  company: string;
  title: string;
  start_date: string | null;
  end_date: string | null;
  duration_months: number | null;
  description: string | null;
  achievements: string[];
}

export interface ParsedEducation {
  institution: string;
  degree: string | null;
  field_of_study: string | null;
  graduation_year: number | null;
  gpa: string | null;
}

export interface ParsedCertification {
  name: string;
  issuer: string | null;
  issue_date: string | null;
  expiration_date: string | null;
}

export interface ParsedResumeData {
  contact: Record<string, string> | null;
  summary: string | null;
  experience: ParsedExperience[];
  education: ParsedEducation[];
  skills: string[];
  certifications: ParsedCertification[];
  languages: string[];
  total_years_experience: number | null;
}

export interface Resume {
  id: string;
  candidate_id: string;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  parse_status: ResumeParseStatus;
  parse_error: string | null;
  raw_text: string | null;
  parsed_data: ParsedResumeData | null;
  ai_analysis: Record<string, unknown> | null;
  version: number;
  is_primary: boolean;
  created_at: string;
  updated_at: string;
}

// --- Screening Types ---

export type QualificationStatus = 'PENDING' | 'QUALIFIED' | 'NOT_QUALIFIED' | 'NEEDS_REVIEW';
export type RequirementMatchStatus = 'MET' | 'NOT_MET' | 'UNCLEAR';

export interface RequirementResult {
  requirement_id: string;
  requirement_text: string;
  requirement_type: string;
  required: boolean;
  status: RequirementMatchStatus;
  evidence: string | null;
  explanation: string;
}

export interface GapItem {
  requirement_id: string;
  requirement: string;
  requirement_type: string;
  explanation: string;
}

export interface CandidateJobScreening {
  id: string;
  candidate_id: string;
  job_id: string;
  resume_id: string;
  qualification_status: QualificationStatus;
  requirement_results: RequirementResult[];
  gaps: GapItem[];
  gap_count: number;
  admin_override: boolean;
  override_by_id: string | null;
  override_reason: string | null;
  override_at: string | null;
  screened_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface ScreeningSummary {
  id: string;
  candidate_id: string;
  candidate_name: string;
  candidate_email: string;
  qualification_status: QualificationStatus;
  gap_count: number;
  admin_override: boolean;
  screened_at: string | null;
}

export interface JobCandidatesStats {
  total: number;
  qualified: number;
  not_qualified: number;
  needs_review: number;
  pending: number;
  overridden: number;
}
