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
