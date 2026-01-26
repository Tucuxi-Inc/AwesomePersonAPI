import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import {
  InterviewSession,
  InterviewPromptResponse,
  TraitProgress,
  AssessmentSummaryResponse,
  InterviewExchange,
  Candidate,
} from '@/types';

interface InterviewState {
  // Session data
  session: InterviewSession | null;
  candidate: Candidate | null;

  // Current interview state
  currentPrompt: string | null;
  promptType: string | null;
  currentTraitId: string | null;
  currentTraitName: string | null;
  currentTraitProgress: TraitProgress | null;
  overallProgress: number;
  canEndInterview: boolean;
  isComplete: boolean;

  // Transcript
  transcript: InterviewExchange[];

  // Trait progress tracking
  traitProgressMap: Record<string, TraitProgress>;

  // Assessment
  assessment: AssessmentSummaryResponse | null;

  // UI state
  isLoading: boolean;
  isSubmitting: boolean;
  error: string | null;

  // Timer
  startTime: number | null;

  // Actions
  setSession: (session: InterviewSession) => void;
  setCandidate: (candidate: Candidate) => void;
  updateFromPromptResponse: (response: InterviewPromptResponse) => void;
  addExchange: (exchange: InterviewExchange) => void;
  setAssessment: (assessment: AssessmentSummaryResponse) => void;
  setLoading: (loading: boolean) => void;
  setSubmitting: (submitting: boolean) => void;
  setError: (error: string | null) => void;
  startTimer: () => void;
  resetInterview: () => void;
}

const initialState = {
  session: null,
  candidate: null,
  currentPrompt: null,
  promptType: null,
  currentTraitId: null,
  currentTraitName: null,
  currentTraitProgress: null,
  overallProgress: 0,
  canEndInterview: false,
  isComplete: false,
  transcript: [],
  traitProgressMap: {},
  assessment: null,
  isLoading: false,
  isSubmitting: false,
  error: null,
  startTime: null,
};

export const useInterviewStore = create<InterviewState>()(
  persist(
    (set, get) => ({
      ...initialState,

      setSession: (session) =>
        set({ session }),

      setCandidate: (candidate) =>
        set({ candidate }),

      updateFromPromptResponse: (response) => {
        const state = get();
        const updates: Partial<InterviewState> = {
          currentPrompt: response.next_prompt,
          promptType: response.prompt_type,
          currentTraitId: response.trait_id,
          currentTraitName: response.trait_name,
          currentTraitProgress: response.trait_progress,
          overallProgress: response.overall_progress,
          canEndInterview: response.can_end_interview,
          isComplete: response.interview_complete,
        };

        // Update trait progress map if we have trait progress
        if (response.trait_progress && response.trait_id) {
          updates.traitProgressMap = {
            ...state.traitProgressMap,
            [response.trait_id]: response.trait_progress,
          };
        }

        set(updates);
      },

      addExchange: (exchange) =>
        set((state) => ({
          transcript: [...state.transcript, exchange],
        })),

      setAssessment: (assessment) =>
        set({ assessment }),

      setLoading: (loading) =>
        set({ isLoading: loading }),

      setSubmitting: (submitting) =>
        set({ isSubmitting: submitting }),

      setError: (error) =>
        set({ error }),

      startTimer: () =>
        set({ startTime: Date.now() }),

      resetInterview: () =>
        set(initialState),
    }),
    {
      name: 'ap-api-interview',
      partialize: (state) => ({
        // Persist session data for recovery if browser closes
        session: state.session,
        candidate: state.candidate,
        transcript: state.transcript,
        traitProgressMap: state.traitProgressMap,
        overallProgress: state.overallProgress,
        startTime: state.startTime,
        currentPrompt: state.currentPrompt,
        promptType: state.promptType,
        currentTraitId: state.currentTraitId,
        currentTraitName: state.currentTraitName,
        currentTraitProgress: state.currentTraitProgress,
        canEndInterview: state.canEndInterview,
        isComplete: state.isComplete,
      }),
    }
  )
);
