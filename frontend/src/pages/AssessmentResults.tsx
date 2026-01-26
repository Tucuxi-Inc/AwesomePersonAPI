import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  RecommendationBanner,
  CompositeScoreCard,
  TraitScoreCard,
  StrengthsAndAreas,
  CounterIndicatorAlert,
} from '@/components/results';
import { useInterview } from '@/hooks/useInterview';
import {
  ArrowLeft,
  Download,
  User,
  Briefcase,
  Clock,
  FileText,
  AlertTriangle,
  Loader2,
} from 'lucide-react';

export default function AssessmentResults() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();

  const {
    candidate,
    assessment,
    transcript,
    isLoading,
    error,
    fetchResults,
    clearInterview,
  } = useInterview();

  // Fetch results on mount
  useEffect(() => {
    if (sessionId) {
      fetchResults(sessionId);
    }
  }, [sessionId, fetchResults]);

  // Handle starting new interview
  const handleNewInterview = () => {
    clearInterview();
    navigate('/candidates');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-4">
          <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto" />
          <p className="text-muted-foreground">Loading assessment results...</p>
        </div>
      </div>
    );
  }

  if (error || !assessment) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Card className="w-full max-w-md">
          <CardContent className="p-6 text-center">
            <AlertTriangle className="h-12 w-12 text-amber-500 mx-auto mb-4" />
            <h2 className="text-lg font-semibold mb-2">Results Not Available</h2>
            <p className="text-muted-foreground mb-4">
              {error || 'The assessment results could not be loaded. The interview may still be in progress.'}
            </p>
            <div className="flex gap-2 justify-center">
              <Button variant="outline" onClick={() => navigate(-1)}>
                Go Back
              </Button>
              <Button onClick={() => navigate('/candidates')}>
                View Candidates
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  const {
    recommendation,
    recommendation_rationale,
    composite_score,
    evidence_quality,
    confidence,
    trait_scores,
    key_strengths,
    development_areas,
    counter_indicator_flags,
    assessment_summary,
  } = assessment;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <Button
            variant="ghost"
            size="sm"
            className="mb-2"
            onClick={() => navigate('/candidates')}
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Candidates
          </Button>
          <h1 className="text-2xl font-bold tracking-tight">Assessment Results</h1>
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
                {new Date().toLocaleDateString()}
              </div>
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Button variant="outline" disabled>
            <Download className="mr-2 h-4 w-4" />
            Export PDF
          </Button>
          <Button onClick={handleNewInterview}>
            New Interview
          </Button>
        </div>
      </div>

      {/* Counter-indicator alerts (if any) */}
      {counter_indicator_flags.length > 0 && (
        <CounterIndicatorAlert flags={counter_indicator_flags} />
      )}

      {/* Recommendation banner */}
      <RecommendationBanner
        recommendation={recommendation}
        confidence={confidence}
        rationale={recommendation_rationale}
      />

      {/* Summary and composite score */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Assessment summary */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-primary" />
              Assessment Summary
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm leading-relaxed whitespace-pre-wrap">
              {assessment_summary}
            </p>
          </CardContent>
        </Card>

        {/* Composite score */}
        <CompositeScoreCard
          compositeScore={composite_score}
          evidenceQuality={evidence_quality}
          confidence={confidence}
          traitCount={trait_scores.length}
        />
      </div>

      {/* Strengths and development areas */}
      <StrengthsAndAreas
        strengths={key_strengths}
        developmentAreas={development_areas}
      />

      {/* Individual trait scores */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Trait Scores</h2>
        <div className="space-y-3">
          {trait_scores.map((score) => (
            <TraitScoreCard key={score.trait_id} score={score} />
          ))}
        </div>
      </div>

      {/* Transcript reference */}
      {transcript.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Interview Transcript</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              {transcript.length} exchange{transcript.length !== 1 ? 's' : ''} recorded during the interview.
            </p>
            <div className="max-h-96 overflow-y-auto space-y-4 pr-2">
              {transcript.map((exchange, index) => (
                <div key={index} className="border-b pb-4 last:border-0">
                  <div className="text-sm text-muted-foreground mb-1">
                    Q{index + 1} - {exchange.prompt_type}
                  </div>
                  <div className="bg-muted/50 rounded p-3 mb-2">
                    <p className="text-sm">{exchange.prompt}</p>
                  </div>
                  <div className="bg-green-50 rounded p-3 border border-green-100">
                    <p className="text-sm">{exchange.response}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
