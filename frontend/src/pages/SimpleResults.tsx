import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '@/api/client';
import { SimpleResultsResponse, SimpleCandidateResult, Recommendation } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  ArrowLeft,
  Download,
  AlertCircle,
  Loader2,
  ThumbsUp,
  ThumbsDown,
  Minus,
  Star,
  ChevronRight,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const recommendationConfig: Record<
  Recommendation,
  { label: string; color: string; icon: React.ReactNode; description: string }
> = {
  STRONG_HIRE: {
    label: 'Strong Hire',
    color: 'bg-green-500',
    icon: <Star className="h-4 w-4" />,
    description: 'Exceptional candidate, highly recommended',
  },
  HIRE: {
    label: 'Hire',
    color: 'bg-blue-500',
    icon: <ThumbsUp className="h-4 w-4" />,
    description: 'Good candidate, meets requirements',
  },
  HOLD: {
    label: 'Hold',
    color: 'bg-yellow-500',
    icon: <Minus className="h-4 w-4" />,
    description: 'Mixed signals, consider carefully',
  },
  NO_HIRE: {
    label: 'No Hire',
    color: 'bg-red-500',
    icon: <ThumbsDown className="h-4 w-4" />,
    description: 'Does not meet requirements',
  },
};

function ScoreBar({ score, label }: { score: number; label?: string }) {
  // Score is 0-10
  const percentage = (score / 10) * 100;
  const getColor = () => {
    if (score >= 8) return 'bg-green-500';
    if (score >= 6) return 'bg-blue-500';
    if (score >= 4) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="space-y-1">
      {label && <p className="text-sm font-medium">{label}</p>}
      <div className="flex items-center gap-2">
        <Progress value={percentage} className={cn('h-2 flex-1', getColor())} />
        <span className="text-sm font-medium w-8">{score.toFixed(1)}</span>
      </div>
    </div>
  );
}

export default function SimpleResults() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [results, setResults] = useState<SimpleResultsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCandidate, setSelectedCandidate] = useState<SimpleCandidateResult | null>(null);

  useEffect(() => {
    if (id) {
      loadResults(id);
    }
  }, [id]);

  const loadResults = async (assessmentId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.getSimpleResults(assessmentId);
      setResults(response.data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load results');
    } finally {
      setIsLoading(false);
    }
  };

  const handleExportPdf = async () => {
    if (!id) return;
    try {
      const response = await api.exportSimplePdf(id);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `assessment-${id}-results.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('PDF export is not yet available');
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (error || !results) {
    return (
      <div className="space-y-4">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error || 'Results not found'}</AlertDescription>
        </Alert>
        <Button variant="outline" onClick={() => navigate('/simple')}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Dashboard
        </Button>
      </div>
    );
  }

  // Sort candidates by composite score
  const sortedResults = [...results.results].sort(
    (a, b) => (b.composite_score || 0) - (a.composite_score || 0)
  );

  // Stats
  const completedCount = results.results.filter((r) => r.interview_status === 'COMPLETED').length;
  const strongHireCount = results.results.filter((r) => r.recommendation === 'STRONG_HIRE').length;
  const hireCount = results.results.filter((r) => r.recommendation === 'HIRE').length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Button variant="ghost" onClick={() => navigate('/simple')} className="mb-2">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Dashboard
          </Button>
          <h1 className="text-3xl font-bold tracking-tight">{results.job_title}</h1>
          <p className="text-muted-foreground">Assessment Results</p>
        </div>
        <Button onClick={handleExportPdf} disabled>
          <Download className="mr-2 h-4 w-4" />
          Export PDF
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total Candidates</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{results.total_candidates}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Interviews Completed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{completedCount}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Strong Hires</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{strongHireCount}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Hires</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{hireCount}</div>
          </CardContent>
        </Card>
      </div>

      {/* Results Table */}
      <Card>
        <CardHeader>
          <CardTitle>Candidate Rankings</CardTitle>
          <CardDescription>
            Candidates are ranked by composite score. Click on a candidate to see detailed trait
            scores.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12">Rank</TableHead>
                <TableHead>Candidate</TableHead>
                <TableHead>Composite Score</TableHead>
                <TableHead>Recommendation</TableHead>
                <TableHead>Qualification</TableHead>
                <TableHead></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedResults.map((candidate, index) => {
                const recConfig = candidate.recommendation
                  ? recommendationConfig[candidate.recommendation]
                  : null;

                return (
                  <TableRow
                    key={candidate.candidate_id}
                    className="cursor-pointer hover:bg-muted/50"
                    onClick={() => setSelectedCandidate(candidate)}
                  >
                    <TableCell className="font-bold text-lg">#{index + 1}</TableCell>
                    <TableCell>
                      <div>
                        <p className="font-medium">{candidate.full_name}</p>
                        <p className="text-sm text-muted-foreground">{candidate.email}</p>
                      </div>
                    </TableCell>
                    <TableCell>
                      {candidate.composite_score !== null ? (
                        <div className="flex items-center gap-2">
                          <Progress
                            value={(candidate.composite_score / 10) * 100}
                            className="w-24 h-2"
                          />
                          <span className="font-medium">
                            {candidate.composite_score.toFixed(1)}/10
                          </span>
                        </div>
                      ) : (
                        <span className="text-muted-foreground">-</span>
                      )}
                    </TableCell>
                    <TableCell>
                      {recConfig ? (
                        <Badge className={cn('gap-1', recConfig.color, 'text-white')}>
                          {recConfig.icon}
                          {recConfig.label}
                        </Badge>
                      ) : (
                        <Badge variant="secondary">Pending</Badge>
                      )}
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant={
                          candidate.qualification_status === 'QUALIFIED'
                            ? 'default'
                            : candidate.qualification_status === 'NOT_QUALIFIED'
                            ? 'destructive'
                            : 'secondary'
                        }
                      >
                        {candidate.qualification_status}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <ChevronRight className="h-4 w-4 text-muted-foreground" />
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Candidate Detail Dialog */}
      <Dialog open={!!selectedCandidate} onOpenChange={() => setSelectedCandidate(null)}>
        <DialogContent className="max-w-2xl">
          {selectedCandidate && (
            <>
              <DialogHeader>
                <DialogTitle>{selectedCandidate.full_name}</DialogTitle>
                <DialogDescription>{selectedCandidate.email}</DialogDescription>
              </DialogHeader>

              <div className="space-y-6">
                {/* Recommendation Banner */}
                {selectedCandidate.recommendation && (
                  <div
                    className={cn(
                      'p-4 rounded-lg text-white',
                      recommendationConfig[selectedCandidate.recommendation].color
                    )}
                  >
                    <div className="flex items-center gap-2">
                      {recommendationConfig[selectedCandidate.recommendation].icon}
                      <span className="font-semibold">
                        {recommendationConfig[selectedCandidate.recommendation].label}
                      </span>
                    </div>
                    <p className="text-sm mt-1 opacity-90">
                      {recommendationConfig[selectedCandidate.recommendation].description}
                    </p>
                  </div>
                )}

                {/* Composite Score */}
                {selectedCandidate.composite_score !== null && (
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm">Overall Score</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center gap-4">
                        <div className="text-4xl font-bold">
                          {selectedCandidate.composite_score.toFixed(1)}
                        </div>
                        <div className="text-muted-foreground">/ 10</div>
                        <Progress
                          value={(selectedCandidate.composite_score / 10) * 100}
                          className="flex-1 h-4"
                        />
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Trait Scores */}
                {selectedCandidate.trait_scores && selectedCandidate.trait_scores.length > 0 && (
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm">Trait Scores</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {selectedCandidate.trait_scores.map((traitScore) => (
                        <div key={traitScore.trait_id} className="space-y-2">
                          <ScoreBar score={traitScore.score} label={traitScore.trait_name} />
                          {traitScore.explanation && (
                            <p className="text-sm text-muted-foreground ml-4">
                              {traitScore.explanation}
                            </p>
                          )}
                        </div>
                      ))}
                    </CardContent>
                  </Card>
                )}

                {/* Recommendation Rationale */}
                {selectedCandidate.recommendation_rationale && (
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm">Assessment Summary</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm">{selectedCandidate.recommendation_rationale}</p>
                    </CardContent>
                  </Card>
                )}
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
