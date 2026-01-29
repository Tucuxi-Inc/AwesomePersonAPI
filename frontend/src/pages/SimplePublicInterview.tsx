import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '@/api/client';
import {
  SimpleInterviewInfo,
  SimpleInterviewStartResponse,
  SimpleInterviewRespondResponse,
  SimpleTraitScore,
} from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import {
  Loader2,
  AlertCircle,
  CheckCircle2,
  MessageCircle,
  Send,
  Clock,
  Briefcase,
  Building,
  Target,
} from 'lucide-react';
import { cn } from '@/lib/utils';

type InterviewPhase = 'loading' | 'welcome' | 'interview' | 'complete' | 'error';

interface TranscriptEntry {
  role: 'system' | 'candidate';
  content: string;
  timestamp: Date;
}

export default function SimplePublicInterview() {
  const { token } = useParams<{ token: string }>();

  const [phase, setPhase] = useState<InterviewPhase>('loading');
  const [error, setError] = useState<string | null>(null);
  const [interviewInfo, setInterviewInfo] = useState<SimpleInterviewInfo | null>(null);

  // Interview state
  const [currentTrait, setCurrentTrait] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [response, setResponse] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [transcript, setTranscript] = useState<TranscriptEntry[]>([]);

  // Results
  const [results, setResults] = useState<{
    trait_scores: SimpleTraitScore[] | null;
    composite_score: number | null;
    recommendation: string | null;
  } | null>(null);

  useEffect(() => {
    if (token) {
      loadInterviewInfo(token);
    }
  }, [token]);

  const loadInterviewInfo = async (interviewToken: string) => {
    setPhase('loading');
    try {
      const response = await api.getSimpleInterviewInfo(interviewToken);
      setInterviewInfo(response.data);

      // Check if already completed
      if (response.data.interview_status === 'COMPLETED') {
        // Load results
        const statusResponse = await api.getSimpleInterviewStatus(interviewToken);
        setResults({
          trait_scores: statusResponse.data.trait_scores,
          composite_score: statusResponse.data.composite_score,
          recommendation: statusResponse.data.recommendation,
        });
        setPhase('complete');
      } else if (response.data.interview_status === 'IN_PROGRESS') {
        // Resume interview
        const statusResponse = await api.getSimpleInterviewStatus(interviewToken);
        setProgress(statusResponse.data.progress);
        // Continue with interview
        setPhase('interview');
      } else {
        setPhase('welcome');
      }
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Unable to load interview';
      setError(errorMessage);
      setPhase('error');
    }
  };

  const handleStartInterview = async () => {
    if (!token) return;
    setIsSubmitting(true);
    setError(null);
    try {
      const response = await api.startSimpleInterview(token);
      const data: SimpleInterviewStartResponse = response.data;

      setCurrentTrait(data.trait_name);
      setProgress(data.progress);
      setTranscript([{ role: 'system', content: data.next_prompt, timestamp: new Date() }]);

      if (data.is_complete) {
        await loadFinalResults();
      } else {
        setPhase('interview');
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to start interview');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSubmitResponse = async () => {
    if (!token || !response.trim()) return;
    setIsSubmitting(true);
    setError(null);

    const candidateResponse = response.trim();
    setResponse('');

    // Add candidate response to transcript
    setTranscript((prev) => [
      ...prev,
      { role: 'candidate', content: candidateResponse, timestamp: new Date() },
    ]);

    try {
      const apiResponse = await api.submitSimpleInterviewResponse(token, {
        response_text: candidateResponse,
      });
      const data: SimpleInterviewRespondResponse = apiResponse.data;

      setProgress(data.progress);
      setCurrentTrait(data.trait_name);

      if (data.is_complete) {
        await loadFinalResults();
      } else if (data.next_prompt) {
        setTranscript((prev) => [
          ...prev,
          { role: 'system', content: data.next_prompt!, timestamp: new Date() },
        ]);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to submit response');
    } finally {
      setIsSubmitting(false);
    }
  };

  const loadFinalResults = async () => {
    if (!token) return;
    try {
      const response = await api.getSimpleInterviewStatus(token);
      setResults({
        trait_scores: response.data.trait_scores,
        composite_score: response.data.composite_score,
        recommendation: response.data.recommendation,
      });
      setPhase('complete');
    } catch (err) {
      console.error('Failed to load results:', err);
      setPhase('complete');
    }
  };

  // Loading Phase
  if (phase === 'loading') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-muted flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="py-12 flex flex-col items-center">
            <Loader2 className="h-12 w-12 animate-spin text-primary mb-4" />
            <p className="text-muted-foreground">Loading interview...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Error Phase
  if (phase === 'error') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-muted flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardContent className="py-12">
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Unable to Load Interview</AlertTitle>
              <AlertDescription>
                {error || 'This interview link may be invalid or expired.'}
              </AlertDescription>
            </Alert>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Welcome Phase
  if (phase === 'welcome' && interviewInfo) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-muted flex items-center justify-center p-4">
        <Card className="w-full max-w-2xl">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 p-3 rounded-full bg-primary/10 w-fit">
              <MessageCircle className="h-8 w-8 text-primary" />
            </div>
            <CardTitle className="text-2xl">Welcome, {interviewInfo.candidate_name}!</CardTitle>
            <CardDescription className="text-base">
              You've been invited to complete a behavioral interview assessment
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Job Info */}
            <div className="grid gap-4 md:grid-cols-2">
              <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                <Briefcase className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm text-muted-foreground">Position</p>
                  <p className="font-medium">{interviewInfo.job_title}</p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 bg-muted rounded-lg">
                <Building className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm text-muted-foreground">Company</p>
                  <p className="font-medium">{interviewInfo.organization_name}</p>
                </div>
              </div>
            </div>

            {/* Traits to Assess */}
            <div className="p-4 border rounded-lg">
              <div className="flex items-center gap-2 mb-3">
                <Target className="h-5 w-5 text-primary" />
                <h3 className="font-semibold">Areas We'll Explore</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {interviewInfo.traits_to_assess.map((trait) => (
                  <Badge key={trait} variant="secondary">
                    {trait}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Instructions */}
            <div className="space-y-3 text-sm text-muted-foreground">
              <p className="flex items-center gap-2">
                <Clock className="h-4 w-4" />
                This interview typically takes 15-30 minutes to complete
              </p>
              <p>
                <strong>Tips for success:</strong>
              </p>
              <ul className="list-disc ml-6 space-y-1">
                <li>
                  Use the STAR method: describe the Situation, Task, Action, and Result
                </li>
                <li>Provide specific examples from your experience</li>
                <li>Be detailed but concise in your responses</li>
                <li>There are no right or wrong answers - be authentic</li>
              </ul>
            </div>

            {/* Start Button */}
            <Button onClick={handleStartInterview} className="w-full" size="lg" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Starting Interview...
                </>
              ) : (
                'Start Interview'
              )}
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Interview Phase
  if (phase === 'interview') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-muted">
        <div className="max-w-3xl mx-auto p-4 space-y-4">
          {/* Header with Progress */}
          <Card>
            <CardContent className="py-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <MessageCircle className="h-5 w-5 text-primary" />
                  <span className="font-semibold">Interview in Progress</span>
                </div>
                <span className="text-sm text-muted-foreground">
                  {Math.round(progress)}% complete
                </span>
              </div>
              <Progress value={progress} className="h-2" />
              {currentTrait && (
                <p className="text-sm text-muted-foreground mt-2">
                  Currently exploring: <Badge variant="outline">{currentTrait}</Badge>
                </p>
              )}
            </CardContent>
          </Card>

          {/* Error Alert */}
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Transcript */}
          <Card className="min-h-[400px] flex flex-col">
            <CardContent className="flex-1 p-4 space-y-4 overflow-y-auto max-h-[500px]">
              {transcript.map((entry, index) => (
                <div
                  key={index}
                  className={cn(
                    'flex',
                    entry.role === 'candidate' ? 'justify-end' : 'justify-start'
                  )}
                >
                  <div
                    className={cn(
                      'max-w-[80%] p-4 rounded-lg',
                      entry.role === 'candidate'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                    )}
                  >
                    <p className="whitespace-pre-wrap">{entry.content}</p>
                    <p
                      className={cn(
                        'text-xs mt-2',
                        entry.role === 'candidate'
                          ? 'text-primary-foreground/70'
                          : 'text-muted-foreground'
                      )}
                    >
                      {entry.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}

              {isSubmitting && (
                <div className="flex justify-start">
                  <div className="bg-muted p-4 rounded-lg flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span className="text-sm text-muted-foreground">Processing...</span>
                  </div>
                </div>
              )}
            </CardContent>

            {/* Response Input */}
            <div className="p-4 border-t">
              <div className="flex gap-2">
                <Textarea
                  value={response}
                  onChange={(e) => setResponse(e.target.value)}
                  placeholder="Type your response here... Be specific and use examples from your experience."
                  className="min-h-[100px] resize-none"
                  disabled={isSubmitting}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && e.metaKey) {
                      handleSubmitResponse();
                    }
                  }}
                />
              </div>
              <div className="flex items-center justify-between mt-2">
                <p className="text-xs text-muted-foreground">
                  Press Cmd+Enter to submit
                </p>
                <Button
                  onClick={handleSubmitResponse}
                  disabled={!response.trim() || isSubmitting}
                >
                  {isSubmitting ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <>
                      <Send className="mr-2 h-4 w-4" />
                      Submit
                    </>
                  )}
                </Button>
              </div>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  // Complete Phase
  if (phase === 'complete') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-background to-muted flex items-center justify-center p-4">
        <Card className="w-full max-w-2xl">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 p-3 rounded-full bg-green-100 w-fit">
              <CheckCircle2 className="h-8 w-8 text-green-600" />
            </div>
            <CardTitle className="text-2xl">Interview Complete!</CardTitle>
            <CardDescription className="text-base">
              Thank you for completing the interview assessment
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {results?.composite_score !== null && results?.composite_score !== undefined && (
              <div className="text-center p-6 bg-muted rounded-lg">
                <p className="text-sm text-muted-foreground mb-2">Your Overall Score</p>
                <div className="text-5xl font-bold text-primary">
                  {results.composite_score.toFixed(1)}
                  <span className="text-2xl text-muted-foreground">/10</span>
                </div>
              </div>
            )}

            {results?.trait_scores && results.trait_scores.length > 0 && (
              <div className="space-y-4">
                <h3 className="font-semibold">Trait Scores</h3>
                {results.trait_scores.map((traitScore) => (
                  <div key={traitScore.trait_id} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span>{traitScore.trait_name}</span>
                      <span className="font-medium">{traitScore.score.toFixed(1)}/10</span>
                    </div>
                    <Progress value={(traitScore.score / 10) * 100} className="h-2" />
                  </div>
                ))}
              </div>
            )}

            <div className="text-center text-muted-foreground">
              <p>The hiring team will review your responses and be in touch soon.</p>
              <p className="text-sm mt-2">You may now close this window.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return null;
}
