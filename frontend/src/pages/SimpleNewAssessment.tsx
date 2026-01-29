import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '@/api/client';
import { useSimpleStore } from '@/store/simpleStore';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2, AlertCircle, Sparkles } from 'lucide-react';

export default function SimpleNewAssessment() {
  const navigate = useNavigate();
  const { setCurrentAssessment, setDraftRequirements } = useSimpleStore();

  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!jobTitle.trim() || !jobDescription.trim()) {
      setError('Please provide both a job title and description');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await api.createSimpleAssessment({
        job_title: jobTitle.trim(),
        job_description: jobDescription.trim(),
      });

      const assessment = response.data;
      setCurrentAssessment(assessment);
      setDraftRequirements(assessment.extracted_requirements);

      // Navigate to the assessment page to continue the wizard
      navigate(`/simple/assessments/${assessment.id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to create assessment');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Create New Assessment</h1>
        <p className="text-muted-foreground">
          Start by entering the job description. Our AI will extract requirements and suggest traits
          to assess.
        </p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Form */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            Step 1: Job Description
          </CardTitle>
          <CardDescription>
            Paste the job description and our AI will automatically extract objective requirements,
            responsibilities, and suggest relevant personality traits to assess.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="jobTitle">Job Title</Label>
              <Input
                id="jobTitle"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g., Senior Software Engineer"
                disabled={isSubmitting}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="jobDescription">Job Description</Label>
              <Textarea
                id="jobDescription"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the full job description here..."
                className="min-h-[300px]"
                disabled={isSubmitting}
              />
              <p className="text-sm text-muted-foreground">
                Include responsibilities, requirements, qualifications, and any nice-to-haves for
                best results.
              </p>
            </div>

            <div className="flex justify-end gap-4">
              <Button type="button" variant="outline" onClick={() => navigate('/simple')}>
                Cancel
              </Button>
              <Button type="submit" disabled={isSubmitting || !jobTitle || !jobDescription}>
                {isSubmitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing Job Description...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Extract Requirements
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Info Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">AI-Powered Extraction</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Our AI analyzes the job description to extract objective requirements that can be
              verified from resumes.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Trait Suggestions</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Based on the role responsibilities, we suggest relevant personality traits to assess
              during interviews.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">7-Step Workflow</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Follow our streamlined workflow to create assessments, add candidates, and conduct
              structured interviews.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
