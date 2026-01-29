import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '@/api/client';
import { Trait } from '@/types';
import { useSimpleStore, WIZARD_STEPS, STEP_LABELS, WizardStep, statusToStep } from '@/store/simpleStore';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
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
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import {
  Check,
  ChevronRight,
  Plus,
  Trash2,
  Upload,
  Send,
  FileText,
  Loader2,
  AlertCircle,
  Copy,
  ExternalLink,
} from 'lucide-react';
import { format } from 'date-fns';
import { cn } from '@/lib/utils';

// Step indicator component
function StepIndicator({
  steps,
  currentStep,
  onStepClick,
}: {
  steps: WizardStep[];
  currentStep: WizardStep;
  onStepClick?: (step: WizardStep) => void;
}) {
  const currentIndex = steps.indexOf(currentStep);

  return (
    <nav aria-label="Progress">
      <ol className="flex items-center">
        {steps.map((step, index) => {
          const isComplete = index < currentIndex;
          const isCurrent = index === currentIndex;

          return (
            <li key={step} className={cn('relative', index !== steps.length - 1 && 'pr-8 sm:pr-20')}>
              <div className="flex items-center">
                <button
                  onClick={() => onStepClick?.(step)}
                  disabled={index > currentIndex}
                  className={cn(
                    'relative flex h-8 w-8 items-center justify-center rounded-full',
                    isComplete && 'bg-primary hover:bg-primary/90',
                    isCurrent && 'border-2 border-primary bg-white',
                    !isComplete && !isCurrent && 'border-2 border-gray-300 bg-white',
                    index <= currentIndex && 'cursor-pointer'
                  )}
                >
                  {isComplete ? (
                    <Check className="h-5 w-5 text-white" />
                  ) : (
                    <span
                      className={cn(
                        'text-sm font-medium',
                        isCurrent ? 'text-primary' : 'text-gray-500'
                      )}
                    >
                      {index + 1}
                    </span>
                  )}
                </button>
                {index !== steps.length - 1 && (
                  <div
                    className={cn(
                      'absolute top-4 left-8 -ml-px h-0.5 w-full sm:w-20',
                      isComplete ? 'bg-primary' : 'bg-gray-300'
                    )}
                  />
                )}
              </div>
              <span
                className={cn(
                  'absolute -bottom-6 left-1/2 -translate-x-1/2 whitespace-nowrap text-xs',
                  isCurrent ? 'font-medium text-primary' : 'text-gray-500'
                )}
              >
                {STEP_LABELS[step]}
              </span>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

export default function SimpleAssessment() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const {
    currentAssessment,
    setCurrentAssessment,
    candidates,
    setCandidates,
    addCandidate,
    removeCandidate,
    selectedTraits,
    setSelectedTraits,
    currentStep,
    setCurrentStep,
    draftRequirements,
    setDraftRequirements,
    isLoading,
    setLoading,
    isSubmitting,
    setSubmitting,
    error,
    setError,
  } = useSimpleStore();

  const [availableTraits, setAvailableTraits] = useState<Trait[]>([]);
  const [addCandidateOpen, setAddCandidateOpen] = useState(false);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [candidateToDelete, setCandidateToDelete] = useState<string | null>(null);
  const [newCandidate, setNewCandidate] = useState({ email: '', full_name: '', phone: '' });
  const [inviteDialogOpen, setInviteDialogOpen] = useState(false);
  const [inviteLink, setInviteLink] = useState('');

  // Load assessment if we have an ID
  useEffect(() => {
    if (id && id !== 'new') {
      loadAssessment(id);
    }
    loadTraits();
  }, [id]);

  const loadAssessment = async (assessmentId: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.getSimpleAssessment(assessmentId);
      const assessment = response.data;
      setCurrentAssessment(assessment);
      setDraftRequirements(assessment.extracted_requirements);

      // Load candidates
      const candidatesResponse = await api.getSimpleCandidates(assessmentId);
      setCandidates(candidatesResponse.data.items || candidatesResponse.data);

      // Load selected traits if any
      if (assessment.selected_trait_ids?.length > 0) {
        const traitsResponse = await api.getTraits();
        const allTraits = traitsResponse.data.items || traitsResponse.data;
        const selected = allTraits.filter((t: Trait) =>
          assessment.selected_trait_ids.includes(t.id)
        );
        setSelectedTraits(selected);
      }

      // Set step based on status
      setCurrentStep(statusToStep(assessment.status));
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to load assessment');
    } finally {
      setLoading(false);
    }
  };

  const loadTraits = async () => {
    try {
      const response = await api.getTraits({ limit: 100 });
      setAvailableTraits(response.data.items || response.data);
    } catch (err) {
      console.error('Failed to load traits:', err);
    }
  };

  // Step 2: Confirm Requirements
  const handleConfirmRequirements = async () => {
    if (!currentAssessment || !draftRequirements) return;
    setSubmitting(true);
    setError(null);
    try {
      await api.confirmSimpleRequirements(currentAssessment.id, draftRequirements);
      const response = await api.getSimpleAssessment(currentAssessment.id);
      setCurrentAssessment(response.data);
      setCurrentStep('candidates');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to confirm requirements');
    } finally {
      setSubmitting(false);
    }
  };

  // Step 3: Add Candidates
  const handleAddCandidate = async () => {
    if (!currentAssessment) return;
    setSubmitting(true);
    setError(null);
    try {
      const response = await api.addSimpleCandidate(currentAssessment.id, newCandidate);
      addCandidate(response.data);
      setNewCandidate({ email: '', full_name: '', phone: '' });
      setAddCandidateOpen(false);

      // Refresh assessment to get updated counts
      const assessmentResponse = await api.getSimpleAssessment(currentAssessment.id);
      setCurrentAssessment(assessmentResponse.data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to add candidate');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteCandidate = async () => {
    if (!currentAssessment || !candidateToDelete) return;
    setSubmitting(true);
    try {
      await api.deleteSimpleCandidate(currentAssessment.id, candidateToDelete);
      removeCandidate(candidateToDelete);
      setCandidateToDelete(null);
      setDeleteConfirmOpen(false);

      // Refresh assessment
      const response = await api.getSimpleAssessment(currentAssessment.id);
      setCurrentAssessment(response.data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to delete candidate');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUploadResume = async (candidateId: string, file: File) => {
    if (!currentAssessment) return;
    try {
      await api.uploadSimpleCandidateResume(currentAssessment.id, candidateId, file);
      // Refresh candidates
      const response = await api.getSimpleCandidates(currentAssessment.id);
      setCandidates(response.data.items || response.data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to upload resume');
    }
  };

  const handleProceedToTraits = async () => {
    if (candidates.length === 0) {
      setError('Please add at least one candidate before proceeding');
      return;
    }
    setCurrentStep('traits');
  };

  // Step 4: Select Traits
  const toggleTrait = (trait: Trait) => {
    const isSelected = selectedTraits.some((t) => t.id === trait.id);
    if (isSelected) {
      setSelectedTraits(selectedTraits.filter((t) => t.id !== trait.id));
    } else if (selectedTraits.length < 5) {
      setSelectedTraits([...selectedTraits, trait]);
    }
  };

  const handleConfirmTraits = async () => {
    if (!currentAssessment) return;
    if (selectedTraits.length === 0) {
      setError('Please select at least one trait');
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      await api.selectSimpleTraits(currentAssessment.id, {
        trait_ids: selectedTraits.map((t) => t.id),
      });
      const response = await api.getSimpleAssessment(currentAssessment.id);
      setCurrentAssessment(response.data);
      setCurrentStep('interviews');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to save traits');
    } finally {
      setSubmitting(false);
    }
  };

  // Step 5: Send Invites
  const handleSendInvite = async (candidateId: string) => {
    if (!currentAssessment) return;
    setSubmitting(true);
    setError(null);
    try {
      const response = await api.sendSimpleInvite(currentAssessment.id, candidateId);
      setInviteLink(response.data.magic_link);
      setInviteDialogOpen(true);

      // Refresh candidates
      const candidatesResponse = await api.getSimpleCandidates(currentAssessment.id);
      setCandidates(candidatesResponse.data.items || candidatesResponse.data);

      // Refresh assessment
      const assessmentResponse = await api.getSimpleAssessment(currentAssessment.id);
      setCurrentAssessment(assessmentResponse.data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to send invite');
    } finally {
      setSubmitting(false);
    }
  };

  const copyInviteLink = () => {
    navigator.clipboard.writeText(inviteLink);
  };

  // Step 6: View Results
  const handleViewResults = () => {
    if (currentAssessment) {
      navigate(`/simple/assessments/${currentAssessment.id}/results`);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (!currentAssessment) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="mx-auto h-12 w-12 text-muted-foreground" />
        <h3 className="mt-2 text-sm font-semibold">Assessment not found</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          The assessment you're looking for doesn't exist or has been deleted.
        </p>
        <Button className="mt-4" onClick={() => navigate('/simple')}>
          Back to Dashboard
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">{currentAssessment.job_title}</h1>
        <p className="text-muted-foreground">Simple Assessment Wizard</p>
      </div>

      {/* Step Indicator */}
      <div className="py-4 overflow-x-auto">
        <StepIndicator steps={WIZARD_STEPS} currentStep={currentStep} onStepClick={setCurrentStep} />
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Step Content */}
      <div className="mt-12">
        {/* Step 2: Requirements */}
        {currentStep === 'requirements' && (
          <Card>
            <CardHeader>
              <CardTitle>Confirm Requirements</CardTitle>
              <CardDescription>
                Review and edit the extracted requirements from the job description
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Objective Requirements */}
              <div>
                <Label className="text-base font-semibold">Objective Requirements</Label>
                <div className="mt-2 space-y-2">
                  {draftRequirements?.objective_requirements.map((req, index) => (
                    <div key={req.id || index} className="flex items-center gap-2 p-2 border rounded">
                      <Badge variant={req.required ? 'default' : 'secondary'}>
                        {req.type}
                      </Badge>
                      <span className="flex-1">{req.requirement}</span>
                      <Badge variant={req.required ? 'destructive' : 'outline'}>
                        {req.required ? 'Required' : 'Preferred'}
                      </Badge>
                    </div>
                  ))}
                  {(!draftRequirements?.objective_requirements ||
                    draftRequirements.objective_requirements.length === 0) && (
                    <p className="text-sm text-muted-foreground">
                      No objective requirements extracted
                    </p>
                  )}
                </div>
              </div>

              {/* Nice-to-haves */}
              <div>
                <Label className="text-base font-semibold">Nice-to-Haves</Label>
                <div className="mt-2 space-y-2">
                  {draftRequirements?.nice_to_haves.map((item, index) => (
                    <div key={index} className="p-2 border rounded">
                      {item.description}
                    </div>
                  ))}
                  {(!draftRequirements?.nice_to_haves ||
                    draftRequirements.nice_to_haves.length === 0) && (
                    <p className="text-sm text-muted-foreground">No nice-to-haves extracted</p>
                  )}
                </div>
              </div>

              {/* Responsibilities */}
              <div>
                <Label className="text-base font-semibold">Key Responsibilities</Label>
                <div className="mt-2 space-y-2">
                  {draftRequirements?.responsibilities.map((resp, index) => (
                    <div key={index} className="p-2 border rounded">
                      {resp}
                    </div>
                  ))}
                  {(!draftRequirements?.responsibilities ||
                    draftRequirements.responsibilities.length === 0) && (
                    <p className="text-sm text-muted-foreground">No responsibilities extracted</p>
                  )}
                </div>
              </div>

              {/* Suggested Traits */}
              <div>
                <Label className="text-base font-semibold">Suggested Traits</Label>
                <div className="mt-2 flex flex-wrap gap-2">
                  {draftRequirements?.suggested_traits.map((trait, index) => (
                    <Badge key={index} variant="outline">
                      {trait}
                    </Badge>
                  ))}
                  {(!draftRequirements?.suggested_traits ||
                    draftRequirements.suggested_traits.length === 0) && (
                    <p className="text-sm text-muted-foreground">No traits suggested</p>
                  )}
                </div>
              </div>

              <div className="flex justify-end">
                <Button onClick={handleConfirmRequirements} disabled={isSubmitting}>
                  {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  Confirm & Continue
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 3: Candidates */}
        {currentStep === 'candidates' && (
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Add Candidates</CardTitle>
                  <CardDescription>
                    Add candidates and optionally upload their resumes for qualification screening
                  </CardDescription>
                </div>
                <Button onClick={() => setAddCandidateOpen(true)}>
                  <Plus className="mr-2 h-4 w-4" />
                  Add Candidate
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {candidates.length === 0 ? (
                <div className="text-center py-8">
                  <Users className="mx-auto h-12 w-12 text-muted-foreground" />
                  <h3 className="mt-2 text-sm font-semibold">No candidates yet</h3>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Add candidates to start the assessment process.
                  </p>
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Resume</TableHead>
                      <TableHead>Qualification</TableHead>
                      <TableHead></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {candidates.map((candidate) => (
                      <TableRow key={candidate.id}>
                        <TableCell className="font-medium">{candidate.full_name}</TableCell>
                        <TableCell>{candidate.email}</TableCell>
                        <TableCell>
                          {candidate.resume_filename ? (
                            <Badge variant="outline" className="gap-1">
                              <FileText className="h-3 w-3" />
                              {candidate.resume_filename}
                            </Badge>
                          ) : (
                            <label className="cursor-pointer">
                              <input
                                type="file"
                                className="hidden"
                                accept=".pdf,.doc,.docx,.txt"
                                onChange={(e) => {
                                  const file = e.target.files?.[0];
                                  if (file) handleUploadResume(candidate.id, file);
                                }}
                              />
                              <Badge
                                variant="outline"
                                className="gap-1 cursor-pointer hover:bg-muted"
                              >
                                <Upload className="h-3 w-3" />
                                Upload
                              </Badge>
                            </label>
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
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => {
                              setCandidateToDelete(candidate.id);
                              setDeleteConfirmOpen(true);
                            }}
                          >
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}

              <div className="flex justify-end mt-6">
                <Button onClick={handleProceedToTraits} disabled={candidates.length === 0}>
                  Continue to Trait Selection
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 4: Traits */}
        {currentStep === 'traits' && (
          <Card>
            <CardHeader>
              <CardTitle>Select Traits to Assess</CardTitle>
              <CardDescription>
                Choose up to 5 personality traits to evaluate during interviews. Based on the job
                description, we suggest: {draftRequirements?.suggested_traits.join(', ')}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-4">
                <Badge variant={selectedTraits.length >= 5 ? 'destructive' : 'secondary'}>
                  {selectedTraits.length}/5 traits selected
                </Badge>
              </div>

              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {availableTraits.map((trait) => {
                  const isSelected = selectedTraits.some((t) => t.id === trait.id);
                  const isSuggested = draftRequirements?.suggested_traits.includes(trait.name);

                  return (
                    <div
                      key={trait.id}
                      onClick={() => toggleTrait(trait)}
                      className={cn(
                        'p-4 border rounded-lg cursor-pointer transition-colors',
                        isSelected && 'border-primary bg-primary/5',
                        !isSelected && selectedTraits.length >= 5 && 'opacity-50 cursor-not-allowed',
                        isSuggested && !isSelected && 'border-dashed border-primary/50'
                      )}
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="font-medium">{trait.name}</h4>
                            {isSuggested && (
                              <Badge variant="outline" className="text-xs">
                                Suggested
                              </Badge>
                            )}
                          </div>
                          <p className="text-sm text-muted-foreground mt-1">{trait.definition}</p>
                          <Badge variant="secondary" className="mt-2">
                            {trait.category}
                          </Badge>
                        </div>
                        <Checkbox checked={isSelected} />
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="flex justify-end mt-6">
                <Button
                  onClick={handleConfirmTraits}
                  disabled={selectedTraits.length === 0 || isSubmitting}
                >
                  {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                  Confirm Traits & Continue
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 5: Interviews */}
        {currentStep === 'interviews' && (
          <Card>
            <CardHeader>
              <CardTitle>Conduct Interviews</CardTitle>
              <CardDescription>
                Send interview invites to candidates. They will receive a magic link to complete the
                interview at their convenience.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="mb-4">
                <Progress
                  value={
                    candidates.length > 0
                      ? (candidates.filter((c) => c.interview_status === 'COMPLETED').length /
                          candidates.length) *
                        100
                      : 0
                  }
                />
                <p className="text-sm text-muted-foreground mt-2">
                  {candidates.filter((c) => c.interview_status === 'COMPLETED').length} of{' '}
                  {candidates.length} interviews completed
                </p>
              </div>

              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Candidate</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Interview Status</TableHead>
                    <TableHead>Invited At</TableHead>
                    <TableHead></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {candidates.map((candidate) => (
                    <TableRow key={candidate.id}>
                      <TableCell className="font-medium">{candidate.full_name}</TableCell>
                      <TableCell>{candidate.email}</TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            candidate.interview_status === 'COMPLETED'
                              ? 'default'
                              : candidate.interview_status === 'IN_PROGRESS'
                              ? 'secondary'
                              : candidate.interview_status === 'INVITED'
                              ? 'outline'
                              : 'secondary'
                          }
                        >
                          {candidate.interview_status}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {candidate.invited_at
                          ? format(new Date(candidate.invited_at), 'MMM d, yyyy h:mm a')
                          : '-'}
                      </TableCell>
                      <TableCell>
                        {candidate.interview_status === 'NOT_STARTED' && (
                          <Button
                            size="sm"
                            onClick={() => handleSendInvite(candidate.id)}
                            disabled={isSubmitting}
                          >
                            <Send className="mr-2 h-4 w-4" />
                            Send Invite
                          </Button>
                        )}
                        {candidate.interview_status === 'INVITED' && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleSendInvite(candidate.id)}
                            disabled={isSubmitting}
                          >
                            Resend
                          </Button>
                        )}
                        {candidate.interview_status === 'COMPLETED' && (
                          <Badge variant="default">
                            <Check className="mr-1 h-3 w-3" />
                            Done
                          </Badge>
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              <div className="flex justify-end mt-6">
                <Button
                  onClick={handleViewResults}
                  disabled={
                    candidates.filter((c) => c.interview_status === 'COMPLETED').length === 0
                  }
                >
                  View Results
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 6: Results */}
        {currentStep === 'results' && (
          <Card>
            <CardHeader>
              <CardTitle>Assessment Complete</CardTitle>
              <CardDescription>
                All interviews have been completed. View the results below.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button onClick={handleViewResults}>
                View Full Results
                <ExternalLink className="ml-2 h-4 w-4" />
              </Button>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Add Candidate Dialog */}
      <Dialog open={addCandidateOpen} onOpenChange={setAddCandidateOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Candidate</DialogTitle>
            <DialogDescription>Enter the candidate's information</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="full_name">Full Name</Label>
              <Input
                id="full_name"
                value={newCandidate.full_name}
                onChange={(e) => setNewCandidate({ ...newCandidate, full_name: e.target.value })}
                placeholder="John Doe"
              />
            </div>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={newCandidate.email}
                onChange={(e) => setNewCandidate({ ...newCandidate, email: e.target.value })}
                placeholder="john@example.com"
              />
            </div>
            <div>
              <Label htmlFor="phone">Phone (Optional)</Label>
              <Input
                id="phone"
                value={newCandidate.phone}
                onChange={(e) => setNewCandidate({ ...newCandidate, phone: e.target.value })}
                placeholder="+1 (555) 123-4567"
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setAddCandidateOpen(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleAddCandidate}
              disabled={!newCandidate.email || !newCandidate.full_name || isSubmitting}
            >
              {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Add Candidate
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteConfirmOpen} onOpenChange={setDeleteConfirmOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Candidate?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. The candidate and all their data will be permanently
              deleted.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleDeleteCandidate}>Delete</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* Invite Link Dialog */}
      <Dialog open={inviteDialogOpen} onOpenChange={setInviteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Interview Invite Sent</DialogTitle>
            <DialogDescription>
              Share this link with the candidate to start their interview
            </DialogDescription>
          </DialogHeader>
          <div className="flex items-center gap-2 p-3 bg-muted rounded-lg">
            <code className="flex-1 text-sm break-all">{inviteLink}</code>
            <Button size="sm" variant="outline" onClick={copyInviteLink}>
              <Copy className="h-4 w-4" />
            </Button>
          </div>
          <p className="text-sm text-muted-foreground">
            This link expires in 7 days. The candidate can use it to complete their interview at any
            time.
          </p>
          <DialogFooter>
            <Button onClick={() => setInviteDialogOpen(false)}>Done</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

// Icon component for Users
function Users(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  );
}
