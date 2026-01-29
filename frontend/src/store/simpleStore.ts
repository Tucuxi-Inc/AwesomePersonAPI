import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import {
  SimpleAssessment,
  SimpleCandidate,
  SimpleAssessmentStatus,
  Trait,
  ObjectiveRequirement,
  NiceToHave,
} from '@/types';

// Wizard step definitions
export type WizardStep =
  | 'job_description'
  | 'requirements'
  | 'candidates'
  | 'traits'
  | 'interviews'
  | 'results';

export const WIZARD_STEPS: WizardStep[] = [
  'job_description',
  'requirements',
  'candidates',
  'traits',
  'interviews',
  'results',
];

export const STEP_LABELS: Record<WizardStep, string> = {
  job_description: 'Job Description',
  requirements: 'Confirm Requirements',
  candidates: 'Add Candidates',
  traits: 'Select Traits',
  interviews: 'Conduct Interviews',
  results: 'View Results',
};

// Map assessment status to wizard step
export function statusToStep(status: SimpleAssessmentStatus): WizardStep {
  switch (status) {
    case 'DRAFT':
    case 'REQUIREMENTS_PENDING':
      return 'requirements';
    case 'TRAITS_PENDING':
      return 'traits';
    case 'CANDIDATES_PENDING':
      return 'candidates';
    case 'INTERVIEWING':
      return 'interviews';
    case 'COMPLETED':
      return 'results';
    default:
      return 'job_description';
  }
}

interface SimpleState {
  // Current assessment being worked on
  currentAssessment: SimpleAssessment | null;
  candidates: SimpleCandidate[];
  selectedTraits: Trait[];

  // Wizard state
  currentStep: WizardStep;

  // Draft data for steps
  draftRequirements: {
    objective_requirements: ObjectiveRequirement[];
    nice_to_haves: NiceToHave[];
    responsibilities: string[];
    suggested_traits: string[];
  } | null;

  // List of all assessments
  assessments: SimpleAssessment[];

  // UI state
  isLoading: boolean;
  isSubmitting: boolean;
  error: string | null;

  // Actions
  setCurrentAssessment: (assessment: SimpleAssessment | null) => void;
  setCandidates: (candidates: SimpleCandidate[]) => void;
  addCandidate: (candidate: SimpleCandidate) => void;
  removeCandidate: (candidateId: string) => void;
  updateCandidate: (candidateId: string, updates: Partial<SimpleCandidate>) => void;
  setSelectedTraits: (traits: Trait[]) => void;
  setCurrentStep: (step: WizardStep) => void;
  setDraftRequirements: (requirements: SimpleState['draftRequirements']) => void;
  setAssessments: (assessments: SimpleAssessment[]) => void;
  setLoading: (loading: boolean) => void;
  setSubmitting: (submitting: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialState = {
  currentAssessment: null,
  candidates: [],
  selectedTraits: [],
  currentStep: 'job_description' as WizardStep,
  draftRequirements: null,
  assessments: [],
  isLoading: false,
  isSubmitting: false,
  error: null,
};

export const useSimpleStore = create<SimpleState>()(
  persist(
    (set) => ({
      ...initialState,

      setCurrentAssessment: (assessment) =>
        set({
          currentAssessment: assessment,
          currentStep: assessment ? statusToStep(assessment.status) : 'job_description',
          draftRequirements: assessment ? assessment.extracted_requirements : null,
        }),

      setCandidates: (candidates) =>
        set({ candidates }),

      addCandidate: (candidate) =>
        set((state) => ({ candidates: [...state.candidates, candidate] })),

      removeCandidate: (candidateId) =>
        set((state) => ({
          candidates: state.candidates.filter((c) => c.id !== candidateId),
        })),

      updateCandidate: (candidateId, updates) =>
        set((state) => ({
          candidates: state.candidates.map((c) =>
            c.id === candidateId ? { ...c, ...updates } : c
          ),
        })),

      setSelectedTraits: (traits) =>
        set({ selectedTraits: traits }),

      setCurrentStep: (step) =>
        set({ currentStep: step }),

      setDraftRequirements: (requirements) =>
        set({ draftRequirements: requirements }),

      setAssessments: (assessments) =>
        set({ assessments }),

      setLoading: (loading) =>
        set({ isLoading: loading }),

      setSubmitting: (submitting) =>
        set({ isSubmitting: submitting }),

      setError: (error) =>
        set({ error }),

      reset: () =>
        set(initialState),
    }),
    {
      name: 'ap-api-simple',
      partialize: (state) => ({
        // Only persist current assessment context
        currentAssessment: state.currentAssessment,
        candidates: state.candidates,
        selectedTraits: state.selectedTraits,
        currentStep: state.currentStep,
        draftRequirements: state.draftRequirements,
      }),
    }
  )
);
