import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { useAuthStore } from '@/store/authStore';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8003';

const client: AxiosInstance = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
client.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = useAuthStore.getState().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
client.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && originalRequest && !originalRequest.headers['X-Retry']) {
      const refreshToken = useAuthStore.getState().refreshToken;

      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;
          useAuthStore.getState().setTokens(access_token, newRefreshToken);

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          originalRequest.headers['X-Retry'] = 'true';

          return client(originalRequest);
        } catch (refreshError) {
          useAuthStore.getState().logout();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

export default client;

// API helper functions
export const api = {
  // Auth
  login: (email: string, password: string) =>
    client.post('/auth/login', { email, password }),

  register: (email: string, password: string, full_name: string, organization_id?: string) =>
    client.post('/auth/register', { email, password, full_name, organization_id }),

  refreshToken: (refresh_token: string) =>
    client.post('/auth/refresh', { refresh_token }),

  getMe: () => client.get('/auth/me'),

  // Organizations
  getOrganizations: (params?: { skip?: number; limit?: number; search?: string }) =>
    client.get('/organizations', { params }),

  getOrganization: (id: string) => client.get(`/organizations/${id}`),

  createOrganization: (data: { name: string; slug: string; description?: string }) =>
    client.post('/organizations', data),

  updateOrganization: (id: string, data: Partial<{ name: string; description: string; is_active: boolean }>) =>
    client.put(`/organizations/${id}`, data),

  deleteOrganization: (id: string) => client.delete(`/organizations/${id}`),

  // Users
  getUsers: (params?: { skip?: number; limit?: number; search?: string; organization_id?: string }) =>
    client.get('/users', { params }),

  getUser: (id: string) => client.get(`/users/${id}`),

  createUser: (data: { email: string; password: string; full_name: string; role?: string; organization_id?: string }) =>
    client.post('/users', data),

  updateUser: (id: string, data: Partial<{ full_name: string; role: string; is_active: boolean }>) =>
    client.put(`/users/${id}`, data),

  deleteUser: (id: string) => client.delete(`/users/${id}`),

  // Traits
  getTraits: (params?: { skip?: number; limit?: number; category?: string; search?: string }) =>
    client.get('/traits', { params }),

  getTrait: (id: string) => client.get(`/traits/${id}`),

  getTraitByName: (name: string) => client.get(`/traits/name/${name}`),

  getTraitCategories: () => client.get('/traits/categories'),

  // Role Profiles
  getRoleProfiles: (params?: { skip?: number; limit?: number; search?: string; templates_only?: boolean }) =>
    client.get('/roles', { params }),

  getRoleTemplates: () => client.get('/roles/templates'),

  getRoleProfile: (id: string) => client.get(`/roles/${id}`),

  createRoleProfile: (data: { name: string; role_category: string; description?: string }) =>
    client.post('/roles', data),

  updateRoleProfile: (id: string, data: Partial<{ name: string; description: string; is_active: boolean }>) =>
    client.put(`/roles/${id}`, data),

  cloneRoleProfile: (id: string, data: { name: string; description?: string }) =>
    client.post(`/roles/${id}/clone`, data),

  deleteRoleProfile: (id: string) => client.delete(`/roles/${id}`),

  // Rubrics
  getRubrics: (params?: { skip?: number; limit?: number; trait_id?: string; defaults_only?: boolean }) =>
    client.get('/rubrics', { params }),

  getDefaultRubrics: () => client.get('/rubrics/defaults'),

  getRubric: (id: string) => client.get(`/rubrics/${id}`),

  createRubric: (data: { name: string; trait_id: string; behavioral_anchors: Record<string, unknown> }) =>
    client.post('/rubrics', data),

  updateRubric: (id: string, data: Partial<{ name: string; description: string; is_active: boolean }>) =>
    client.put(`/rubrics/${id}`, data),

  cloneRubric: (id: string, data: { name: string; description?: string; role_profile_id?: string }) =>
    client.post(`/rubrics/${id}/clone`, data),

  deleteRubric: (id: string) => client.delete(`/rubrics/${id}`),

  // Candidates
  getCandidates: (params?: { skip?: number; limit?: number; search?: string; status?: string }) =>
    client.get('/candidates', { params }),

  getCandidate: (id: string) => client.get(`/candidates/${id}`),

  createCandidate: (data: {
    email: string;
    full_name: string;
    phone?: string;
    current_title?: string;
    current_company?: string;
    linkedin_url?: string;
    years_experience?: number;
    source?: string;
    referrer?: string;
    role_profile_id?: string;
    notes?: string;
    tags?: string[];
  }) => client.post('/candidates', data),

  updateCandidate: (id: string, data: Partial<{
    email: string;
    full_name: string;
    phone: string;
    current_title: string;
    current_company: string;
    linkedin_url: string;
    years_experience: number;
    source: string;
    referrer: string;
    role_profile_id: string;
    status: string;
    notes: string;
    tags: string[];
    is_active: boolean;
  }>) => client.put(`/candidates/${id}`, data),

  deleteCandidate: (id: string) => client.delete(`/candidates/${id}`),

  // Interviews
  startInterview: (data: {
    candidate_id: string;
    rubric_id?: string;
    trait_ids?: string[];
    config?: {
      max_duration_minutes?: number;
      max_follow_ups_per_trait?: number;
      confidence_threshold_for_recursion?: number;
      require_reflection?: boolean;
      enable_resume_customization?: boolean;
      enable_conflict_probing?: boolean;
    };
  }) => client.post('/interviews/start', data),

  submitResponse: (sessionId: string, data: { response_text: string }) =>
    client.post(`/interviews/${sessionId}/respond`, data),

  getInterviewSession: (sessionId: string) =>
    client.get(`/interviews/${sessionId}`),

  endInterview: (sessionId: string) =>
    client.post(`/interviews/${sessionId}/end`),

  getInterviewResult: (sessionId: string) =>
    client.get(`/interviews/${sessionId}/result`),

  // Interview Sessions list (for candidate's interview history)
  getCandidateInterviews: (candidateId: string) =>
    client.get(`/candidates/${candidateId}/interviews`),

  // Compliance
  getImpactDashboard: () => client.get('/compliance/impact-dashboard'),

  getImpactReports: (params?: { limit?: number; offset?: number }) =>
    client.get('/compliance/impact-reports', { params }),

  generateImpactReport: (data: {
    organization_id: string;
    period_start: string;
    period_end: string;
    report_type?: string;
  }) => client.post('/compliance/impact-reports', data),

  getComplianceStatus: () => client.get('/compliance/status'),

  generateDisclosure: (params?: {
    role_profile_id?: string;
    jurisdiction?: string;
    trait_names?: string[];
  }) => client.post('/compliance/disclosures/generate', null, { params }),

  recordDisclosure: (data: {
    candidate_id: string;
    interview_session_id?: string;
    disclosure_type: string;
    disclosure_content: string;
    jurisdiction?: string;
    consent_required?: boolean;
    consent_given?: boolean;
  }) => client.post('/compliance/disclosures', data),

  acknowledgeDisclosure: (disclosureId: string, data: { consent_given?: boolean }) =>
    client.post(`/compliance/disclosures/${disclosureId}/acknowledge`, data),

  getCandidateDisclosures: (candidateId: string) =>
    client.get(`/compliance/disclosures/candidate/${candidateId}`),

  getAssessmentAudit: (assessmentId: string) =>
    client.get(`/compliance/audit/assessment/${assessmentId}`),

  // Profile Development - Top Performers
  getTopPerformers: (params?: {
    role_category?: string;
    profiling_status?: string;
    is_active?: boolean;
    skip?: number;
    limit?: number;
  }) => client.get('/profiling/top-performers', { params }),

  getTopPerformer: (id: string) => client.get(`/profiling/top-performers/${id}`),

  createTopPerformer: (data: {
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
  }) => client.post('/profiling/top-performers', data),

  updateTopPerformer: (id: string, data: Partial<{
    name: string;
    employee_id: string;
    email: string;
    job_title: string;
    department: string;
    role_category: string;
    tenure_months: number;
    performance_metrics: Record<string, unknown>;
    profiling_status: string;
    notes: string;
    is_active: boolean;
  }>) => client.patch(`/profiling/top-performers/${id}`, data),

  deleteTopPerformer: (id: string) => client.delete(`/profiling/top-performers/${id}`),

  // Profile Development - Training Sessions
  getTrainingSessions: (performerId: string, params?: {
    status?: string;
    skip?: number;
    limit?: number;
  }) => client.get(`/profiling/top-performers/${performerId}/sessions`, { params }),

  getTrainingSession: (sessionId: string) =>
    client.get(`/profiling/sessions/${sessionId}`),

  createTrainingSession: (data: {
    top_performer_id: string;
    target_traits: string[];
    focus_areas?: string;
    scheduled_at?: string;
  }) => client.post('/profiling/sessions', data),

  updateTrainingSession: (sessionId: string, data: Partial<{
    target_traits: string[];
    focus_areas: string;
    scheduled_at: string;
    status: string;
    interviewer_notes: string;
  }>) => client.patch(`/profiling/sessions/${sessionId}`, data),

  // Profile Development - Interactive Profiling
  startProfilingSession: (data: {
    top_performer_id: string;
    target_traits: string[];
    role_context?: Record<string, unknown>;
  }) => client.post('/profiling/sessions/start', data),

  submitProfilingResponse: (sessionId: string, data: { response_text: string }) =>
    client.post(`/profiling/sessions/${sessionId}/respond`, data),

  endProfilingSession: (sessionId: string) =>
    client.post(`/profiling/sessions/${sessionId}/end`),

  extractTraitsFromSession: (sessionId: string) =>
    client.post(`/profiling/sessions/${sessionId}/extract`),

  // Profile Development - Rubric Generation
  generateRubric: (data: {
    role_category: string;
    top_performer_ids: string[];
    target_trait_ids: string[];
    role_context?: Record<string, unknown>;
    base_rubric_id?: string;
  }) => client.post('/profiling/rubrics/generate', data),

  generateAndSaveRubric: (data: {
    role_category: string;
    top_performer_ids: string[];
    target_trait_ids: string[];
    role_context?: Record<string, unknown>;
    base_rubric_id?: string;
  }) => client.post('/profiling/rubrics/generate-and-save', data),

  // Profile Development - Synthesis
  synthesizeProfiles: (data: {
    top_performer_ids: string[];
    role_category: string;
  }) => client.post('/profiling/synthesize', data),

  // Invitations (Admin)
  getInvitations: (params?: {
    invitation_type?: string;
    status?: string;
    skip?: number;
    limit?: number;
  }) => client.get('/invitations', { params }),

  createCandidateInvitation: (data: {
    candidate_id: string;
    recipient_email: string;
    recipient_name?: string;
    trait_ids?: string[];
    role_profile_id?: string;
    expires_in_days?: number;
    custom_message?: string;
  }) => client.post('/invitations/candidate', data),

  createTopPerformerInvitation: (data: {
    top_performer_id: string;
    recipient_email: string;
    recipient_name?: string;
    trait_ids?: string[];
    expires_in_days?: number;
    custom_message?: string;
  }) => client.post('/invitations/top-performer', data),

  getInvitation: (id: string) => client.get(`/invitations/${id}`),

  resendInvitation: (id: string) => client.post(`/invitations/${id}/resend`),

  revokeInvitation: (id: string) => client.post(`/invitations/${id}/revoke`),

  // Public Self-Service (no auth required)
  validateInvitation: (token: string) =>
    client.get(`/public/invite/${token}/validate`),

  getInvitationDisclosure: (token: string) =>
    client.get(`/public/invite/${token}/disclosure`),

  startSelfServiceSession: (token: string, consentGiven: boolean) =>
    client.post(`/public/invite/${token}/start`, { token, consent_given: consentGiven }),

  submitSelfServiceResponse: (token: string, sessionId: string, responseText: string) =>
    client.post(`/public/invite/${token}/respond`, {
      token,
      session_id: sessionId,
      response_text: responseText,
    }),

  endSelfServiceSession: (token: string) =>
    client.post(`/public/invite/${token}/end`),
};
