import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  InterviewPrompt,
  ResponseInput,
  TranscriptPanel,
  ProgressTracker,
  TraitProgressCard,
} from '@/components/interview';
import { useInterview } from '@/hooks/useInterview';
import { ProbeType } from '@/types';
import {
  AlertTriangle,
  CheckCircle2,
  Clock,
  LogOut,
  User,
  Briefcase,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';

export default function Interview() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const [showTranscript, setShowTranscript] = useState(false);
  const [showEndConfirm, setShowEndConfirm] = useState(false);

  const {
    session,
    candidate,
    currentPrompt,
    promptType,
    currentTraitName,
    currentTraitProgress,
    overallProgress,
    canEndInterview,
    isComplete,
    transcript,
    traitProgressMap,
    isLoading,
    isSubmitting,
    error,
    submitResponse,
    endInterviewEarly,
    fetchSession,
    getElapsedTime,
  } = useInterview();

  // Fetch session on mount if not loaded
  useEffect(() => {
    if (sessionId && !session) {
      fetchSession(sessionId);
    }
  }, [sessionId, session, fetchSession]);

  // Redirect to results if complete
  useEffect(() => {
    if (isComplete && sessionId) {
      navigate(`/interviews/${sessionId}/results`);
    }
  }, [isComplete, sessionId, navigate]);

  // Update elapsed time every minute
  const [elapsedMinutes, setElapsedMinutes] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => {
      setElapsedMinutes(getElapsedTime());
    }, 60000);
    setElapsedMinutes(getElapsedTime());
    return () => clearInterval(interval);
  }, [getElapsedTime]);

  const handleSubmit = async (responseText: string) => {
    await submitResponse(responseText);
  };

  const handleEndInterview = async () => {
    setShowEndConfirm(false);
    await endInterviewEarly();
  };

  if (isLoading && !session) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto" />
          <p className="text-muted-foreground">Loading interview session...</p>
        </div>
      </div>
    );
  }

  if (!session || !currentPrompt) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Card className="w-full max-w-md">
          <CardContent className="p-6 text-center">
            <AlertTriangle className="h-12 w-12 text-amber-500 mx-auto mb-4" />
            <h2 className="text-lg font-semibold mb-2">Session Not Found</h2>
            <p className="text-muted-foreground mb-4">
              The interview session could not be loaded. It may have expired or been completed.
            </p>
            <Button onClick={() => navigate('/candidates')}>
              Return to Candidates
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Interview Session</h1>
          {candidate && (
            <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground">
              <div className="flex items-center gap-1.5">
                <User className="h-4 w-4" />
                {candidate.full_name}
              </div>
              {candidate.current_title && (
                <div className="flex items-center gap-1.5">
                  <Briefcase className="h-4 w-4" />
                  {candidate.current_title}
                </div>
              )}
              <div className="flex items-center gap-1.5">
                <Clock className="h-4 w-4" />
                {elapsedMinutes} min elapsed
              </div>
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          {canEndInterview && !showEndConfirm && (
            <Button
              variant="outline"
              onClick={() => setShowEndConfirm(true)}
            >
              <LogOut className="mr-2 h-4 w-4" />
              End Interview
            </Button>
          )}
          {showEndConfirm && (
            <div className="flex items-center gap-2 p-2 bg-amber-50 border border-amber-200 rounded-lg">
              <span className="text-sm text-amber-800">End interview early?</span>
              <Button size="sm" variant="destructive" onClick={handleEndInterview}>
                Confirm
              </Button>
              <Button size="sm" variant="outline" onClick={() => setShowEndConfirm(false)}>
                Cancel
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Error display */}
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4 text-destructive">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Main content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column - Q&A Interface */}
        <div className="lg:col-span-2 space-y-6">
          {/* Current prompt */}
          <InterviewPrompt
            prompt={currentPrompt}
            promptType={promptType as ProbeType}
            traitName={currentTraitName}
            isLoading={isSubmitting}
          />

          {/* Response input */}
          <ResponseInput
            onSubmit={handleSubmit}
            isSubmitting={isSubmitting}
            isDisabled={isComplete}
          />

          {/* Current trait progress (detailed view) */}
          {currentTraitProgress && (
            <TraitProgressCard progress={currentTraitProgress} />
          )}

          {/* Transcript toggle for mobile */}
          <div className="lg:hidden">
            <Button
              variant="outline"
              className="w-full"
              onClick={() => setShowTranscript(!showTranscript)}
            >
              {showTranscript ? (
                <>
                  <ChevronUp className="mr-2 h-4 w-4" />
                  Hide Transcript
                </>
              ) : (
                <>
                  <ChevronDown className="mr-2 h-4 w-4" />
                  Show Transcript ({transcript.length})
                </>
              )}
            </Button>
            {showTranscript && (
              <div className="mt-4">
                <TranscriptPanel exchanges={transcript} />
              </div>
            )}
          </div>
        </div>

        {/* Right column - Progress & Transcript */}
        <div className="space-y-6">
          {/* Progress tracker */}
          <ProgressTracker
            overallProgress={overallProgress}
            traitProgressMap={traitProgressMap}
            currentTraitId={currentTraitProgress?.trait_id}
            elapsedMinutes={elapsedMinutes}
          />

          {/* Transcript (desktop only) */}
          <div className="hidden lg:block">
            <TranscriptPanel exchanges={transcript} />
          </div>
        </div>
      </div>

      {/* Interview complete overlay */}
      {isComplete && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md mx-4">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle2 className="h-6 w-6 text-green-600" />
                Interview Complete
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">
                The interview has been completed. You can now view the assessment results.
              </p>
              <Button
                className="w-full"
                onClick={() => navigate(`/interviews/${sessionId}/results`)}
              >
                View Results
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
