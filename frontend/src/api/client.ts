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

  updateMe: (data: { full_name?: string; phone?: string; title?: string; bio?: string }) =>
    client.put('/auth/me', data),

  changePassword: (data: { current_password: string; new_password: string }) =>
    client.put('/auth/me/password', data),

  // Organizations
  getOrganizations: (params?: { skip?: number; limit?: number; search?: string }) =>
    client.get('/organizations', { params }),

  getOrganization: (id: string) => client.get(`/organizations/${id}`),

  createOrganization: (data: { name: string; slug: string; description?: string }) =>
    client.post('/organizations', data),

  updateOrganization: (id: string, data: Partial<{ name: string; description: string; is_active: boolean }>) =>
    client.put(`/organizations/${id}`, data),

  deleteOrganization: (id: string) => client.delete(`/organizations/${id}`),

  // Email Settings (Admin)
  getEmailSettings: (orgId: string) =>
    client.get(`/organizations/${orgId}/email-settings`),

  updateEmailSettings: (orgId: string, data: {
    smtp_host: string;
    smtp_port: number;
    smtp_user: string;
    smtp_password?: string;
    smtp_from_email: string;
    smtp_from_name: string;
    smtp_use_tls: boolean;
  }) => client.put(`/organizations/${orgId}/email-settings`, data),

  testEmailSettings: (orgId: string, recipientEmail: string) =>
    client.post(`/organizations/${orgId}/email-settings/test`, {
      recipient_email: recipientEmail,
    }),

  // Users
  getUsers: (params?: { skip?: number; limit?: number; search?: string; organization_id?: string }) =>
    client.get('/users', { params }),

  getUser: (id: string) => client.get(`/users/${id}`),

  createUser: (data: { email: string; password: string; full_name: string; role?: string; organization_id?: string }) =>
    client.post('/users', data),

  updateUser: (id: string, data: Partial<{ full_name: string; role: string; is_active: boolean }>) =>
    client.put(`/users/${id}`, data),

  deleteUser: (id: string) => client.delete(`/users/${id}`),

  // Dashboard
  getDashboardStats: () => client.get('/dashboard/stats'),

  // Traits
  getTraits: (params?: { skip?: number; limit?: number; category?: string; search?: string }) =>
    client.get('/traits', { params }),

  getTrait: (id: string) => client.get(`/traits/${id}`),

  getTraitByName: (name: string) => client.get(`/traits/name/${name}`),

  createTrait: (data: {
    name: string;
    category: string;
    definition: string;
    spectrum_low_label: string;
    spectrum_high_label: string;
    behavioral_markers_low?: string[];
    behavioral_markers_high?: string[];
    counter_indicator_for?: string[];
    display_order?: number;
  }) => client.post('/traits', data),

  updateTrait: (id: string, data: Partial<{
    name: string;
    category: string;
    definition: string;
    spectrum_low_label: string;
    spectrum_high_label: string;
    behavioral_markers_low: string[];
    behavioral_markers_high: string[];
    counter_indicator_for: string[];
    display_order: number;
  }>) => client.put(`/traits/${id}`, data),

  deleteTrait: (id: string) => client.delete(`/traits/${id}`),

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
    job_id?: string; // Phase 7: Link interview to a job for resume-informed probes
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

  // Jobs
  getJobs: (params?: { skip?: number; limit?: number; search?: string; status?: string }) =>
    client.get('/jobs', { params }),

  getJob: (id: string) => client.get(`/jobs/${id}`),

  createJob: (data: {
    title: string;
    description: string;
    department?: string;
    location?: string;
    employment_type?: string;
    role_profile_id?: string;
    objective_requirements?: Array<{
      id?: string;
      type: string;
      requirement: string;
      required: boolean;
    }>;
    nice_to_haves?: Array<{ description: string }>;
    responsibilities?: string[];
    suggested_traits?: string[];
    status?: string;
  }) => client.post('/jobs', data),

  updateJob: (id: string, data: Partial<{
    title: string;
    description: string;
    department: string;
    location: string;
    employment_type: string;
    role_profile_id: string;
    objective_requirements: Array<{
      id?: string;
      type: string;
      requirement: string;
      required: boolean;
    }>;
    nice_to_haves: Array<{ description: string }>;
    responsibilities: string[];
    suggested_traits: string[];
    status: string;
  }>) => client.put(`/jobs/${id}`, data),

  deleteJob: (id: string) => client.delete(`/jobs/${id}`),

  extractJobRequirements: (id: string) =>
    client.post(`/jobs/${id}/extract-requirements`),

  saveJobRequirements: (id: string, data: {
    objective_requirements: Array<{
      id?: string;
      type: string;
      requirement: string;
      required: boolean;
    }>;
    nice_to_haves: Array<{ description: string }>;
    responsibilities: string[];
    suggested_traits: string[];
  }) => client.post(`/jobs/${id}/save-requirements`, data),

  // Resumes
  uploadResume: (candidateId: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return client.post(`/candidates/${candidateId}/resume`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  getCandidateResumes: (candidateId: string) =>
    client.get(`/candidates/${candidateId}/resumes`),

  getCandidateResume: (candidateId: string) =>
    client.get(`/candidates/${candidateId}/resume`),

  getResume: (candidateId: string, resumeId: string) =>
    client.get(`/candidates/${candidateId}/resume/${resumeId}`),

  reparseResume: (candidateId: string, resumeId: string) =>
    client.post(`/candidates/${candidateId}/resume/${resumeId}/reparse`),

  // Job Candidate Screening
  screenCandidate: (jobId: string, candidateId: string, resumeId?: string) =>
    client.post(`/jobs/${jobId}/screen-candidate/${candidateId}`, { resume_id: resumeId }),

  getJobCandidatesStats: (jobId: string) =>
    client.get(`/jobs/${jobId}/candidates/stats`),

  getQualifiedCandidates: (jobId: string, params?: { skip?: number; limit?: number }) =>
    client.get(`/jobs/${jobId}/candidates/qualified`, { params }),

  getCandidatesWithGaps: (jobId: string, params?: { skip?: number; limit?: number; sort_by?: string }) =>
    client.get(`/jobs/${jobId}/candidates/gaps`, { params }),

  getCandidatesNeedingReview: (jobId: string, params?: { skip?: number; limit?: number }) =>
    client.get(`/jobs/${jobId}/candidates/needs-review`, { params }),

  getScreeningDetails: (jobId: string, candidateId: string) =>
    client.get(`/jobs/${jobId}/screening/${candidateId}`),

  overrideQualification: (jobId: string, candidateId: string, reason: string) =>
    client.post(`/jobs/${jobId}/candidates/${candidateId}/override`, { reason }),

  removeOverride: (jobId: string, candidateId: string) =>
    client.delete(`/jobs/${jobId}/candidates/${candidateId}/override`),

  // ==================== SIMPLE MODE API ====================

  // Simple Assessments
  getSimpleAssessments: (params?: { skip?: number; limit?: number; status?: string }) =>
    client.get('/simple/assessments', { params }),

  getSimpleAssessment: (id: string) =>
    client.get(`/simple/assessments/${id}`),

  createSimpleAssessment: (data: { job_title: string; job_description: string }) =>
    client.post('/simple/assessments', data),

  deleteSimpleAssessment: (id: string) =>
    client.delete(`/simple/assessments/${id}`),

  // Step 2: Confirm Requirements
  confirmSimpleRequirements: (id: string, data: {
    requirements: Record<string, unknown>;
  }) => client.post(`/simple/assessments/${id}/requirements/confirm`, data),

  // Step 3: Add Candidates
  addSimpleCandidate: (assessmentId: string, data: {
    email: string;
    full_name: string;
    phone?: string;
  }) => client.post(`/simple/assessments/${assessmentId}/candidates`, data),

  getSimpleCandidates: (assessmentId: string) =>
    client.get(`/simple/assessments/${assessmentId}/candidates`),

  getSimpleCandidate: (assessmentId: string, candidateId: string) =>
    client.get(`/simple/assessments/${assessmentId}/candidates/${candidateId}`),

  deleteSimpleCandidate: (assessmentId: string, candidateId: string) =>
    client.delete(`/simple/assessments/${assessmentId}/candidates/${candidateId}`),

  // Upload resume for Simple candidate
  uploadSimpleCandidateResume: (assessmentId: string, candidateId: string, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return client.post(`/simple/assessments/${assessmentId}/candidates/${candidateId}/resume`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Step 4: Select Traits (max 5)
  selectSimpleTraits: (assessmentId: string, data: { trait_ids: string[] }) =>
    client.post(`/simple/assessments/${assessmentId}/traits`, data),

  // Step 5: Send Interview Invites
  sendSimpleInvite: (assessmentId: string, candidateId: string) =>
    client.post(`/simple/assessments/${assessmentId}/candidates/${candidateId}/send-invite`),

  // Step 6: Get Results
  getSimpleResults: (assessmentId: string) =>
    client.get(`/simple/assessments/${assessmentId}/results`),

  // Step 7: Export PDF (TODO)
  exportSimplePdf: (assessmentId: string) =>
    client.get(`/simple/assessments/${assessmentId}/export/pdf`, { responseType: 'blob' }),

  // ==================== PUBLIC SIMPLE INTERVIEW API ====================
  // These endpoints don't require auth - they use magic link tokens

  getSimpleInterviewInfo: (token: string) =>
    axios.get(`${API_URL}/api/v1/public/simple/${token}`),

  startSimpleInterview: (token: string) =>
    axios.post(`${API_URL}/api/v1/public/simple/${token}/start`),

  submitSimpleInterviewResponse: (token: string, data: { response_text: string }) =>
    axios.post(`${API_URL}/api/v1/public/simple/${token}/respond`, data),

  getSimpleInterviewStatus: (token: string) =>
    axios.get(`${API_URL}/api/v1/public/simple/${token}/status`),
};
