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
};
