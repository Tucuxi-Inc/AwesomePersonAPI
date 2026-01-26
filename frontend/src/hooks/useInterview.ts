import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useInterviewStore } from '@/store/interviewStore';
import { api } from '@/api/client';
import {
  StartInterviewRequest,
  InterviewPromptResponse,
  AssessmentSummaryResponse,
  Candidate,
  InterviewExchange,
} from '@/types';

export function useInterview() {
  const navigate = useNavigate();
  const {
    session,
    candidate,
    currentPrompt,
    promptType,
    currentTraitId,
    currentTraitName,
    currentTraitProgress,
    overallProgress,
    canEndInterview,
    isComplete,
    transcript,
    traitProgressMap,
    assessment,
    isLoading,
    isSubmitting,
    error,
    startTime,
    setSession,
    setCandidate,
    updateFromPromptResponse,
    addExchange,
    setAssessment,
    setLoading,
    setSubmitting,
    setError,
    startTimer,
    resetInterview,
  } = useInterviewStore();

  const startInterview = useCallback(
    async (request: StartInterviewRequest, candidateData: Candidate) => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.startInterview(request);
        const data = response.data as InterviewPromptResponse;

        // Store session info
        setSession({
          id: data.session_id,
          candidate_id: request.candidate_id,
          status: 'IN_PROGRESS',
          session_type: 'BEHAVIORAL',
          started_at: new Date().toISOString(),
          completed_at: null,
          duration_minutes: null,
          target_traits: request.trait_ids || [],
          overall_progress: data.overall_progress,
          traits_completed: 0,
          traits_total: request.trait_ids?.length || 6,
        });

        setCandidate(candidateData);
        updateFromPromptResponse(data);
        startTimer();

        // Navigate to interview page
        navigate(`/interviews/${data.session_id}`);

        return { success: true, sessionId: data.session_id };
      } catch (err: unknown) {
        const error = err as { response?: { data?: { detail?: string } } };
        const message = error.response?.data?.detail || 'Failed to start interview';
        setError(message);
        return { success: false, error: message };
      } finally {
        setLoading(false);
      }
    },
    [navigate, setSession, setCandidate, updateFromPromptResponse, startTimer, setLoading, setError]
  );

  const submitResponse = useCallback(
    async (responseText: string) => {
      if (!session) {
        setError('No active interview session');
        return { success: false, error: 'No active interview session' };
      }

      setSubmitting(true);
      setError(null);

      // Record the exchange immediately for UI responsiveness
      const exchange: InterviewExchange = {
        prompt: currentPrompt || '',
        prompt_type: promptType as InterviewExchange['prompt_type'],
        trait_id: currentTraitId,
        response: responseText,
        timestamp: new Date().toISOString(),
      };
      addExchange(exchange);

      try {
        const response = await api.submitResponse(session.id, { response_text: responseText });
        const data = response.data as InterviewPromptResponse;

        updateFromPromptResponse(data);

        // If interview is complete, navigate to results
        if (data.interview_complete) {
          navigate(`/interviews/${session.id}/results`);
        }

        return { success: true, isComplete: data.interview_complete };
      } catch (err: unknown) {
        const error = err as { response?: { data?: { detail?: string } } };
        const message = error.response?.data?.detail || 'Failed to submit response';
        setError(message);
        return { success: false, error: message };
      } finally {
        setSubmitting(false);
      }
    },
    [session, currentPrompt, promptType, currentTraitId, addExchange, updateFromPromptResponse, navigate, setSubmitting, setError]
  );

  const endInterviewEarly = useCallback(
    async () => {
      if (!session) {
        setError('No active interview session');
        return { success: false, error: 'No active interview session' };
      }

      setLoading(true);
      setError(null);

      try {
        await api.endInterview(session.id);
        navigate(`/interviews/${session.id}/results`);
        return { success: true };
      } catch (err: unknown) {
        const error = err as { response?: { data?: { detail?: string } } };
        const message = error.response?.data?.detail || 'Failed to end interview';
        setError(message);
        return { success: false, error: message };
      } finally {
        setLoading(false);
      }
    },
    [session, navigate, setLoading, setError]
  );

  const fetchResults = useCallback(
    async (sessionId?: string) => {
      const id = sessionId || session?.id;
      if (!id) {
        setError('No session ID provided');
        return { success: false, error: 'No session ID provided' };
      }

      setLoading(true);
      setError(null);

      try {
        const response = await api.getInterviewResult(id);
        const data = response.data as AssessmentSummaryResponse;
        setAssessment(data);
        return { success: true, assessment: data };
      } catch (err: unknown) {
        const error = err as { response?: { data?: { detail?: string } } };
        const message = error.response?.data?.detail || 'Failed to fetch results';
        setError(message);
        return { success: false, error: message };
      } finally {
        setLoading(false);
      }
    },
    [session, setAssessment, setLoading, setError]
  );

  const fetchSession = useCallback(
    async (sessionId: string) => {
      setLoading(true);
      setError(null);

      try {
        const response = await api.getInterviewSession(sessionId);
        const data = response.data;
        setSession(data);
        return { success: true, session: data };
      } catch (err: unknown) {
        const error = err as { response?: { data?: { detail?: string } } };
        const message = error.response?.data?.detail || 'Failed to fetch session';
        setError(message);
        return { success: false, error: message };
      } finally {
        setLoading(false);
      }
    },
    [setSession, setLoading, setError]
  );

  const getElapsedTime = useCallback(() => {
    if (!startTime) return 0;
    return Math.floor((Date.now() - startTime) / 1000 / 60); // Returns minutes
  }, [startTime]);

  const clearInterview = useCallback(() => {
    resetInterview();
  }, [resetInterview]);

  return {
    // State
    session,
    candidate,
    currentPrompt,
    promptType,
    currentTraitId,
    currentTraitName,
    currentTraitProgress,
    overallProgress,
    canEndInterview,
    isComplete,
    transcript,
    traitProgressMap,
    assessment,
    isLoading,
    isSubmitting,
    error,

    // Actions
    startInterview,
    submitResponse,
    endInterviewEarly,
    fetchResults,
    fetchSession,
    getElapsedTime,
    clearInterview,
  };
}
