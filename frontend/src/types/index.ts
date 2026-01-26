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
