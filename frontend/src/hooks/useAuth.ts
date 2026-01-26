import { useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { api } from '@/api/client';
import { User, LoginCredentials, RegisterData } from '@/types';

export function useAuth() {
  const navigate = useNavigate();
  const {
    user,
    accessToken,
    isAuthenticated,
    isLoading,
    setUser,
    setTokens,
    logout: clearAuth,
    setLoading,
  } = useAuthStore();

  // Fetch current user on mount if we have a token
  useEffect(() => {
    const fetchUser = async () => {
      if (accessToken && !user) {
        try {
          const response = await api.getMe();
          setUser(response.data as User);
        } catch (error) {
          clearAuth();
        }
      }
      setLoading(false);
    };

    fetchUser();
  }, [accessToken, user, setUser, clearAuth, setLoading]);

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      try {
        const response = await api.login(credentials.email, credentials.password);
        const { access_token, refresh_token } = response.data;
        setTokens(access_token, refresh_token);

        // Fetch user info
        const userResponse = await api.getMe();
        setUser(userResponse.data as User);

        navigate('/dashboard');
        return { success: true };
      } catch (error: unknown) {
        const err = error as { response?: { data?: { detail?: string } } };
        return {
          success: false,
          error: err.response?.data?.detail || 'Login failed',
        };
      }
    },
    [navigate, setTokens, setUser]
  );

  const register = useCallback(
    async (data: RegisterData) => {
      try {
        await api.register(data.email, data.password, data.full_name, data.organization_id);
        // Auto-login after registration
        return login({ email: data.email, password: data.password });
      } catch (error: unknown) {
        const err = error as { response?: { data?: { detail?: string } } };
        return {
          success: false,
          error: err.response?.data?.detail || 'Registration failed',
        };
      }
    },
    [login]
  );

  const logout = useCallback(() => {
    clearAuth();
    navigate('/login');
  }, [clearAuth, navigate]);

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
  };
}
