import { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { api } from '@/api/client';
import { Candidate, CandidateStatus, Resume } from '@/types';
import {
  Search,
  Play,
  Eye,
  User,
  Briefcase,
  Mail,
  AlertTriangle,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Filter,
  Link2,
  Copy,
  Check,
  Upload,
  FileText,
  ChevronDown,
  ChevronUp,
  RefreshCw,
  GraduationCap,
  Award,
} from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

const statusConfig: Record<CandidateStatus, { label: string; color: string }> = {
  NEW: { label: 'New', color: 'bg-blue-100 text-blue-800' },
  SCREENING: { label: 'Screening', color: 'bg-purple-100 text-purple-800' },
  INTERVIEWING: { label: 'Interviewing', color: 'bg-amber-100 text-amber-800' },
  ASSESSED: { label: 'Assessed', color: 'bg-green-100 text-green-800' },
  OFFER: { label: 'Offer', color: 'bg-emerald-100 text-emerald-800' },
  HIRED: { label: 'Hired', color: 'bg-teal-100 text-teal-800' },
  REJECTED: { label: 'Rejected', color: 'bg-red-100 text-red-800' },
  WITHDRAWN: { label: 'Withdrawn', color: 'bg-gray-100 text-gray-800' },
};

export default function Candidates() {
  const navigate = useNavigate();

  // State
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<CandidateStatus | ''>('');
  const [page, setPage] = useState(0);
  const [total, setTotal] = useState(0);
  const pageSize = 10;

  // Invitation dialog state
  const [inviteDialogOpen, setInviteDialogOpen] = useState(false);
  const [inviteCandidate, setInviteCandidate] = useState<Candidate | null>(null);
  const [inviteLink, setInviteLink] = useState<string | null>(null);
  const [inviteLoading, setInviteLoading] = useState(false);
  const [linkCopied, setLinkCopied] = useState(false);

  // Resume state
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());
  const [candidateResumes, setCandidateResumes] = useState<Record<string, Resume | null>>({});
  const [resumeLoading, setResumeLoading] = useState<Record<string, boolean>>({});
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [uploadCandidate, setUploadCandidate] = useState<Candidate | null>(null);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Fetch candidates
  useEffect(() => {
    const fetchCandidates = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await api.getCandidates({
          skip: page * pageSize,
          limit: pageSize,
          search: searchQuery || undefined,
          status: statusFilter || undefined,
        });

        const data = response.data;
        setCandidates(data.items || data);
        setTotal(data.total || data.length);
      } catch (err: unknown) {
        const error = err as { response?: { data?: { detail?: string } } };
        setError(error.response?.data?.detail || 'Failed to load candidates');
      } finally {
        setIsLoading(false);
      }
    };

    fetchCandidates();
  }, [page, searchQuery, statusFilter]);

  // Handle search with debounce
  const handleSearch = (value: string) => {
    setSearchQuery(value);
    setPage(0);
  };

  // Navigate to start interview
  const handleStartInterview = (candidateId: string) => {
    navigate(`/candidates/${candidateId}/start-interview`);
  };

  // Navigate to view results (placeholder for now)
  const handleViewResults = (candidateId: string) => {
    // TODO: Implement viewing past interview results
    navigate(`/candidates/${candidateId}/interviews`);
  };

  // Open invite dialog
  const handleOpenInviteDialog = (candidate: Candidate) => {
    setInviteCandidate(candidate);
    setInviteLink(null);
    setLinkCopied(false);
    setInviteDialogOpen(true);
  };

  // Create invitation
  const handleCreateInvitation = async () => {
    if (!inviteCandidate) return;

    setInviteLoading(true);
    try {
      const response = await api.createCandidateInvitation({
        candidate_id: inviteCandidate.id,
        recipient_email: inviteCandidate.email,
        recipient_name: inviteCandidate.full_name,
        custom_message: `You've been invited to complete an interview assessment.`,
      });
      // Build full link from token
      const baseUrl = window.location.origin;
      setInviteLink(`${baseUrl}/invite/${response.data.token}`);
    } catch (err) {
      console.error('Failed to create invitation:', err);
    } finally {
      setInviteLoading(false);
    }
  };

  // Copy link to clipboard
  const handleCopyLink = async () => {
    if (!inviteLink) return;
    try {
      await navigator.clipboard.writeText(inviteLink);
      setLinkCopied(true);
      setTimeout(() => setLinkCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  // Toggle expanded row and load resume if needed
  const toggleExpanded = useCallback(async (candidateId: string) => {
    setExpandedRows(prev => {
      const newSet = new Set(prev);
      if (newSet.has(candidateId)) {
        newSet.delete(candidateId);
      } else {
        newSet.add(candidateId);
        // Load resume if not already loaded
        if (candidateResumes[candidateId] === undefined) {
          loadCandidateResume(candidateId);
        }
      }
      return newSet;
    });
  }, [candidateResumes]);

  // Load candidate's primary resume
  const loadCandidateResume = async (candidateId: string) => {
    setResumeLoading(prev => ({ ...prev, [candidateId]: true }));
    try {
      const response = await api.getCandidateResume(candidateId);
      setCandidateResumes(prev => ({ ...prev, [candidateId]: response.data }));
    } catch {
      // No resume found - set to null
      setCandidateResumes(prev => ({ ...prev, [candidateId]: null }));
    } finally {
      setResumeLoading(prev => ({ ...prev, [candidateId]: false }));
    }
  };

  // Open upload dialog
  const handleOpenUploadDialog = (candidate: Candidate) => {
    setUploadCandidate(candidate);
    setUploadDialogOpen(true);
  };

  // Handle file selection
  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || !uploadCandidate) return;

    setUploading(true);
    try {
      const response = await api.uploadResume(uploadCandidate.id, file);
      // Update local state
      setCandidateResumes(prev => ({
        ...prev,
        [uploadCandidate.id]: response.data,
      }));
      setUploadDialogOpen(false);
      // Expand row to show the uploaded resume
      setExpandedRows(prev => new Set(prev).add(uploadCandidate.id));
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      alert(error.response?.data?.detail || 'Failed to upload resume');
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  // Reparse resume
  const handleReparseResume = async (candidateId: string, resumeId: string) => {
    setResumeLoading(prev => ({ ...prev, [candidateId]: true }));
    try {
      const response = await api.reparseResume(candidateId, resumeId);
      setCandidateResumes(prev => ({ ...prev, [candidateId]: response.data }));
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      alert(error.response?.data?.detail || 'Failed to reparse resume');
    } finally {
      setResumeLoading(prev => ({ ...prev, [candidateId]: false }));
    }
  };

  // Get parse status badge
  const getParseStatusBadge = (status: string) => {
    switch (status) {
      case 'PARSED':
        return 'bg-green-100 text-green-800';
      case 'PARSING':
        return 'bg-blue-100 text-blue-800';
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800';
      case 'FAILED':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Candidates</h1>
          <p className="text-muted-foreground">Manage candidates and conduct interviews</p>
        </div>
        <p className="text-sm text-muted-foreground">
          Use <span className="font-medium">Simple Mode</span> to add candidates to an assessment
        </p>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="py-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search by name or email..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                className="pl-10"
              />
            </div>
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4 text-muted-foreground" />
              <select
                value={statusFilter}
                onChange={(e) => {
                  setStatusFilter(e.target.value as CandidateStatus | '');
                  setPage(0);
                }}
                className="h-10 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
              >
                <option value="">All Statuses</option>
                {Object.entries(statusConfig).map(([status, config]) => (
                  <option key={status} value={status}>
                    {config.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Error state */}
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4 text-destructive">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Loading state */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      )}

      {/* Empty state */}
      {!isLoading && candidates.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center">
            <User className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Candidates Found</h3>
            <p className="text-muted-foreground mb-4">
              {searchQuery || statusFilter
                ? 'Try adjusting your search or filters.'
                : 'Create an assessment in Simple Mode to get started.'}
            </p>
            <Button onClick={() => navigate('/simple')}>
              Go to Simple Mode
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Candidates list */}
      {!isLoading && candidates.length > 0 && (
        <div className="space-y-4">
          {candidates.map((candidate) => (
            <Card key={candidate.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  {/* Candidate info */}
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <User className="h-6 w-6 text-primary" />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="font-semibold">{candidate.full_name}</h3>
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                          statusConfig[candidate.status]?.color || 'bg-gray-100 text-gray-800'
                        }`}>
                          {statusConfig[candidate.status]?.label || candidate.status}
                        </span>
                      </div>
                      <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground flex-wrap">
                        {candidate.current_title && (
                          <div className="flex items-center gap-1">
                            <Briefcase className="h-3.5 w-3.5" />
                            {candidate.current_title}
                            {candidate.current_company && ` at ${candidate.current_company}`}
                          </div>
                        )}
                        <div className="flex items-center gap-1">
                          <Mail className="h-3.5 w-3.5" />
                          {candidate.email}
                        </div>
                      </div>
                      {candidate.tags && candidate.tags.length > 0 && (
                        <div className="flex items-center gap-1 mt-2">
                          {candidate.tags.slice(0, 3).map((tag) => (
                            <span
                              key={tag}
                              className="px-2 py-0.5 bg-muted rounded text-xs"
                            >
                              {tag}
                            </span>
                          ))}
                          {candidate.tags.length > 3 && (
                            <span className="text-xs text-muted-foreground">
                              +{candidate.tags.length - 3} more
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleOpenUploadDialog(candidate)}
                    >
                      <Upload className="mr-1.5 h-4 w-4" />
                      Resume
                    </Button>
                    <Button
                      variant="default"
                      size="sm"
                      onClick={() => handleStartInterview(candidate.id)}
                    >
                      <Play className="mr-1.5 h-4 w-4" />
                      Interview
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleOpenInviteDialog(candidate)}
                    >
                      <Link2 className="mr-1.5 h-4 w-4" />
                      Send Invite
                    </Button>
                    {candidate.status === 'ASSESSED' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleViewResults(candidate.id)}
                      >
                        <Eye className="mr-1.5 h-4 w-4" />
                        Results
                      </Button>
                    )}
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => toggleExpanded(candidate.id)}
                    >
                      {expandedRows.has(candidate.id) ? (
                        <ChevronUp className="h-4 w-4" />
                      ) : (
                        <ChevronDown className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>

                {/* Expanded Resume Section */}
                {expandedRows.has(candidate.id) && (
                  <div className="mt-4 pt-4 border-t">
                    {resumeLoading[candidate.id] ? (
                      <div className="flex items-center gap-2 text-muted-foreground">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        Loading resume...
                      </div>
                    ) : candidateResumes[candidate.id] ? (
                      <div className="space-y-4">
                        {/* Resume Header */}
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <FileText className="h-5 w-5 text-muted-foreground" />
                            <div>
                              <p className="font-medium">{candidateResumes[candidate.id]?.filename}</p>
                              <p className="text-sm text-muted-foreground">
                                {(candidateResumes[candidate.id]?.file_size_bytes ?? 0 / 1024).toFixed(1)} KB
                                {' '}• Version {candidateResumes[candidate.id]?.version}
                              </p>
                            </div>
                            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${getParseStatusBadge(candidateResumes[candidate.id]?.parse_status || '')}`}>
                              {candidateResumes[candidate.id]?.parse_status}
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleReparseResume(candidate.id, candidateResumes[candidate.id]!.id)}
                              disabled={resumeLoading[candidate.id]}
                            >
                              <RefreshCw className="mr-1.5 h-3.5 w-3.5" />
                              Reparse
                            </Button>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleOpenUploadDialog(candidate)}
                            >
                              <Upload className="mr-1.5 h-3.5 w-3.5" />
                              Upload New
                            </Button>
                          </div>
                        </div>

                        {/* Parsed Data Preview */}
                        {candidateResumes[candidate.id]?.parse_status === 'PARSED' &&
                         candidateResumes[candidate.id]?.parsed_data && (
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {/* Experience */}
                            <div className="p-3 bg-muted/50 rounded-lg">
                              <div className="flex items-center gap-2 mb-2">
                                <Briefcase className="h-4 w-4 text-muted-foreground" />
                                <span className="font-medium text-sm">Experience</span>
                              </div>
                              <p className="text-2xl font-bold">
                                {candidateResumes[candidate.id]?.parsed_data?.total_years_experience?.toFixed(1) || '?'} years
                              </p>
                              <p className="text-xs text-muted-foreground mt-1">
                                {candidateResumes[candidate.id]?.parsed_data?.experience?.length || 0} positions
                              </p>
                            </div>

                            {/* Education */}
                            <div className="p-3 bg-muted/50 rounded-lg">
                              <div className="flex items-center gap-2 mb-2">
                                <GraduationCap className="h-4 w-4 text-muted-foreground" />
                                <span className="font-medium text-sm">Education</span>
                              </div>
                              {candidateResumes[candidate.id]?.parsed_data?.education?.length ? (
                                <>
                                  <p className="text-sm font-medium">
                                    {candidateResumes[candidate.id]?.parsed_data?.education[0]?.degree || 'Degree'}
                                  </p>
                                  <p className="text-xs text-muted-foreground">
                                    {candidateResumes[candidate.id]?.parsed_data?.education[0]?.institution}
                                  </p>
                                </>
                              ) : (
                                <p className="text-sm text-muted-foreground">No education data</p>
                              )}
                            </div>

                            {/* Skills */}
                            <div className="p-3 bg-muted/50 rounded-lg">
                              <div className="flex items-center gap-2 mb-2">
                                <Award className="h-4 w-4 text-muted-foreground" />
                                <span className="font-medium text-sm">Skills</span>
                              </div>
                              <div className="flex flex-wrap gap-1">
                                {candidateResumes[candidate.id]?.parsed_data?.skills?.slice(0, 5).map((skill, idx) => (
                                  <span key={idx} className="px-1.5 py-0.5 bg-background rounded text-xs">
                                    {skill}
                                  </span>
                                ))}
                                {(candidateResumes[candidate.id]?.parsed_data?.skills?.length || 0) > 5 && (
                                  <span className="text-xs text-muted-foreground">
                                    +{(candidateResumes[candidate.id]?.parsed_data?.skills?.length || 0) - 5} more
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Parse Error */}
                        {candidateResumes[candidate.id]?.parse_status === 'FAILED' && (
                          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-sm text-red-800">
                              <strong>Parse Error:</strong> {candidateResumes[candidate.id]?.parse_error}
                            </p>
                          </div>
                        )}

                        {/* Parsing in Progress */}
                        {(candidateResumes[candidate.id]?.parse_status === 'PENDING' ||
                          candidateResumes[candidate.id]?.parse_status === 'PARSING') && (
                          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg flex items-center gap-2">
                            <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
                            <p className="text-sm text-blue-800">
                              Resume is being processed. Refresh to check status.
                            </p>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="text-center py-4">
                        <FileText className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                        <p className="text-sm text-muted-foreground mb-2">No resume uploaded</p>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleOpenUploadDialog(candidate)}
                        >
                          <Upload className="mr-1.5 h-4 w-4" />
                          Upload Resume
                        </Button>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between pt-4">
              <div className="text-sm text-muted-foreground">
                Showing {page * pageSize + 1}-{Math.min((page + 1) * pageSize, total)} of {total} candidates
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage(p => Math.max(0, p - 1))}
                  disabled={page === 0}
                >
                  <ChevronLeft className="h-4 w-4" />
                  Previous
                </Button>
                <span className="text-sm text-muted-foreground px-2">
                  Page {page + 1} of {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
                  disabled={page >= totalPages - 1}
                >
                  Next
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Invitation Dialog */}
      <Dialog open={inviteDialogOpen} onOpenChange={setInviteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Send Interview Invitation</DialogTitle>
            <DialogDescription>
              Generate a self-service interview link for {inviteCandidate?.full_name}.
            </DialogDescription>
          </DialogHeader>

          <div className="py-4">
            {!inviteLink ? (
              <div className="text-center">
                <p className="text-sm text-muted-foreground mb-4">
                  Click the button below to generate a unique interview invitation link that will
                  be sent to <strong>{inviteCandidate?.email}</strong>.
                </p>
                <p className="text-xs text-muted-foreground">
                  The link will expire in 7 days.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium mb-2">Invitation Link:</p>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 text-xs bg-background p-2 rounded border overflow-x-auto">
                      {inviteLink}
                    </code>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleCopyLink}
                    >
                      {linkCopied ? (
                        <Check className="h-4 w-4 text-green-600" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground">
                  Share this link with the candidate. They will be shown disclosure information and
                  can then complete their interview assessment.
                </p>
              </div>
            )}
          </div>

          <DialogFooter>
            {!inviteLink ? (
              <>
                <Button variant="outline" onClick={() => setInviteDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleCreateInvitation} disabled={inviteLoading}>
                  {inviteLoading ? 'Generating...' : 'Generate Link'}
                </Button>
              </>
            ) : (
              <Button onClick={() => setInviteDialogOpen(false)}>
                Done
              </Button>
            )}
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Upload Resume Dialog */}
      <Dialog open={uploadDialogOpen} onOpenChange={setUploadDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Upload Resume</DialogTitle>
            <DialogDescription>
              Upload a resume for {uploadCandidate?.full_name}. Supported formats: PDF, DOCX, DOC, TXT.
            </DialogDescription>
          </DialogHeader>

          <div className="py-4">
            <div
              className="border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:border-primary hover:bg-primary/5 transition-colors"
              onClick={() => fileInputRef.current?.click()}
            >
              {uploading ? (
                <div className="flex flex-col items-center gap-2">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  <p className="text-sm text-muted-foreground">Uploading resume...</p>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-2">
                  <Upload className="h-8 w-8 text-muted-foreground" />
                  <p className="text-sm text-muted-foreground">
                    Click to select a file or drag and drop
                  </p>
                  <p className="text-xs text-muted-foreground">
                    PDF, DOCX, DOC, TXT up to 10MB
                  </p>
                </div>
              )}
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.doc,.txt"
                onChange={handleFileSelect}
                className="hidden"
                disabled={uploading}
              />
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setUploadDialogOpen(false)} disabled={uploading}>
              Cancel
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
