import { useState, useEffect } from 'react';
import { api } from '@/api/client';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Plus,
  Edit,
  Trash2,
  Sparkles,
  Loader2,
  Briefcase,
  MapPin,
  Building2,
  ChevronDown,
  ChevronUp,
  X,
  Check,
} from 'lucide-react';

interface ObjectiveRequirement {
  id: string;
  type: string;
  requirement: string;
  required: boolean;
}

interface NiceToHave {
  description: string;
}

interface Job {
  id: string;
  organization_id: string;
  role_profile_id: string | null;
  title: string;
  description: string;
  department: string | null;
  location: string | null;
  employment_type: string | null;
  objective_requirements: ObjectiveRequirement[];
  nice_to_haves: NiceToHave[];
  responsibilities: string[];
  suggested_traits: string[];
  status: 'DRAFT' | 'OPEN' | 'CLOSED' | 'ON_HOLD';
  created_at: string;
  updated_at: string;
  role_profile_name?: string;
  role_profile_category?: string;
}

interface RoleProfile {
  id: string;
  name: string;
  role_category: string;
  is_template: boolean;
}

const JOB_STATUSES = ['DRAFT', 'OPEN', 'CLOSED', 'ON_HOLD'] as const;
const EMPLOYMENT_TYPES = ['FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERNSHIP'] as const;
const REQUIREMENT_TYPES = ['education', 'experience', 'certification', 'skill', 'other'] as const;

const statusColors: Record<string, string> = {
  DRAFT: 'bg-gray-100 text-gray-800',
  OPEN: 'bg-green-100 text-green-800',
  CLOSED: 'bg-red-100 text-red-800',
  ON_HOLD: 'bg-yellow-100 text-yellow-800',
};

export default function Jobs() {
  const { user } = useAuth();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [roleProfiles, setRoleProfiles] = useState<RoleProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Dialog states
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [requirementsDialogOpen, setRequirementsDialogOpen] = useState(false);
  const [dialogLoading, setDialogLoading] = useState(false);
  const [dialogError, setDialogError] = useState<string | null>(null);
  const [extracting, setExtracting] = useState(false);

  // Selected job for edit/delete
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  // Form state
  const [formTitle, setFormTitle] = useState('');
  const [formDescription, setFormDescription] = useState('');
  const [formDepartment, setFormDepartment] = useState('');
  const [formLocation, setFormLocation] = useState('');
  const [formEmploymentType, setFormEmploymentType] = useState('FULL_TIME');
  const [formRoleProfileId, setFormRoleProfileId] = useState<string>('');
  const [formStatus, setFormStatus] = useState<string>('DRAFT');
  const [formRequirements, setFormRequirements] = useState<ObjectiveRequirement[]>([]);
  const [formNiceToHaves, setFormNiceToHaves] = useState<NiceToHave[]>([]);
  const [formResponsibilities, setFormResponsibilities] = useState<string[]>([]);
  const [formSuggestedTraits, setFormSuggestedTraits] = useState<string[]>([]);

  // Expanded rows for viewing requirements
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());

  const isAdmin = user?.role === 'ADMIN' || user?.is_superuser;

  useEffect(() => {
    loadData();
  }, [statusFilter, searchQuery]);

  const loadData = async () => {
    try {
      setLoading(true);
      const params: Record<string, unknown> = {};
      if (statusFilter !== 'all') params.status = statusFilter;
      if (searchQuery) params.search = searchQuery;

      const [jobsRes, profilesRes] = await Promise.all([
        api.getJobs(params as { skip?: number; limit?: number; search?: string; status?: string }),
        api.getRoleProfiles({ limit: 100 }),
      ]);

      setJobs(jobsRes.data.items);
      setRoleProfiles(profilesRes.data.items);
    } catch (err) {
      setError('Failed to load jobs');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormTitle('');
    setFormDescription('');
    setFormDepartment('');
    setFormLocation('');
    setFormEmploymentType('FULL_TIME');
    setFormRoleProfileId('');
    setFormStatus('DRAFT');
    setFormRequirements([]);
    setFormNiceToHaves([]);
    setFormResponsibilities([]);
    setFormSuggestedTraits([]);
    setDialogError(null);
  };

  const handleOpenCreateDialog = () => {
    resetForm();
    setCreateDialogOpen(true);
  };

  const handleOpenEditDialog = (job: Job) => {
    setSelectedJob(job);
    setFormTitle(job.title);
    setFormDescription(job.description);
    setFormDepartment(job.department || '');
    setFormLocation(job.location || '');
    setFormEmploymentType(job.employment_type || 'FULL_TIME');
    setFormRoleProfileId(job.role_profile_id || '');
    setFormStatus(job.status);
    setFormRequirements(job.objective_requirements || []);
    setFormNiceToHaves(job.nice_to_haves || []);
    setFormResponsibilities(job.responsibilities || []);
    setFormSuggestedTraits(job.suggested_traits || []);
    setDialogError(null);
    setEditDialogOpen(true);
  };

  const handleOpenDeleteDialog = (job: Job) => {
    setSelectedJob(job);
    setDeleteDialogOpen(true);
  };

  const handleOpenRequirementsDialog = (job: Job) => {
    setSelectedJob(job);
    setFormRequirements(job.objective_requirements || []);
    setFormNiceToHaves(job.nice_to_haves || []);
    setFormResponsibilities(job.responsibilities || []);
    setFormSuggestedTraits(job.suggested_traits || []);
    setRequirementsDialogOpen(true);
  };

  const handleCreate = async () => {
    if (!formTitle.trim() || !formDescription.trim()) {
      setDialogError('Title and description are required');
      return;
    }

    setDialogLoading(true);
    setDialogError(null);

    try {
      await api.createJob({
        title: formTitle.trim(),
        description: formDescription.trim(),
        department: formDepartment.trim() || undefined,
        location: formLocation.trim() || undefined,
        employment_type: formEmploymentType || undefined,
        role_profile_id: formRoleProfileId || undefined,
        status: formStatus,
        objective_requirements: formRequirements,
        nice_to_haves: formNiceToHaves,
        responsibilities: formResponsibilities,
        suggested_traits: formSuggestedTraits,
      });

      setCreateDialogOpen(false);
      resetForm();
      loadData();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setDialogError(error.response?.data?.detail || 'Failed to create job');
    } finally {
      setDialogLoading(false);
    }
  };

  const handleUpdate = async () => {
    if (!selectedJob || !formTitle.trim() || !formDescription.trim()) {
      setDialogError('Title and description are required');
      return;
    }

    setDialogLoading(true);
    setDialogError(null);

    try {
      await api.updateJob(selectedJob.id, {
        title: formTitle.trim(),
        description: formDescription.trim(),
        department: formDepartment.trim() || undefined,
        location: formLocation.trim() || undefined,
        employment_type: formEmploymentType || undefined,
        role_profile_id: formRoleProfileId || undefined,
        status: formStatus,
        objective_requirements: formRequirements,
        nice_to_haves: formNiceToHaves,
        responsibilities: formResponsibilities,
        suggested_traits: formSuggestedTraits,
      });

      setEditDialogOpen(false);
      setSelectedJob(null);
      resetForm();
      loadData();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setDialogError(error.response?.data?.detail || 'Failed to update job');
    } finally {
      setDialogLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!selectedJob) return;

    setDialogLoading(true);

    try {
      await api.deleteJob(selectedJob.id);
      setDeleteDialogOpen(false);
      setSelectedJob(null);
      loadData();
    } catch (err) {
      console.error('Failed to delete job', err);
    } finally {
      setDialogLoading(false);
    }
  };

  const handleExtractRequirements = async () => {
    if (!selectedJob) return;

    setExtracting(true);
    setDialogError(null);

    try {
      const response = await api.extractJobRequirements(selectedJob.id);
      const extracted = response.data;

      setFormRequirements(extracted.objective_requirements || []);
      setFormNiceToHaves(extracted.nice_to_haves || []);
      setFormResponsibilities(extracted.responsibilities || []);
      setFormSuggestedTraits(extracted.suggested_traits || []);

      // Reload job data
      loadData();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setDialogError(error.response?.data?.detail || 'Failed to extract requirements');
    } finally {
      setExtracting(false);
    }
  };

  const handleSaveRequirements = async () => {
    if (!selectedJob) return;

    setDialogLoading(true);
    setDialogError(null);

    try {
      await api.saveJobRequirements(selectedJob.id, {
        objective_requirements: formRequirements,
        nice_to_haves: formNiceToHaves,
        responsibilities: formResponsibilities,
        suggested_traits: formSuggestedTraits,
      });

      setRequirementsDialogOpen(false);
      setSelectedJob(null);
      loadData();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setDialogError(error.response?.data?.detail || 'Failed to save requirements');
    } finally {
      setDialogLoading(false);
    }
  };

  // Requirement editing helpers
  const addRequirement = () => {
    setFormRequirements([
      ...formRequirements,
      { id: crypto.randomUUID(), type: 'skill', requirement: '', required: true },
    ]);
  };

  const updateRequirement = (index: number, field: keyof ObjectiveRequirement, value: unknown) => {
    const updated = [...formRequirements];
    updated[index] = { ...updated[index], [field]: value };
    setFormRequirements(updated);
  };

  const removeRequirement = (index: number) => {
    setFormRequirements(formRequirements.filter((_, i) => i !== index));
  };

  const addNiceToHave = () => {
    setFormNiceToHaves([...formNiceToHaves, { description: '' }]);
  };

  const updateNiceToHave = (index: number, value: string) => {
    const updated = [...formNiceToHaves];
    updated[index] = { description: value };
    setFormNiceToHaves(updated);
  };

  const removeNiceToHave = (index: number) => {
    setFormNiceToHaves(formNiceToHaves.filter((_, i) => i !== index));
  };

  const toggleRowExpansion = (jobId: string) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(jobId)) {
      newExpanded.delete(jobId);
    } else {
      newExpanded.add(jobId);
    }
    setExpandedRows(newExpanded);
  };

  if (loading && jobs.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">{error}</p>
        <Button onClick={loadData} className="mt-4">
          Retry
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Jobs</h1>
          <p className="text-gray-600">Manage job postings and objective requirements</p>
        </div>
        {isAdmin && (
          <Button onClick={handleOpenCreateDialog}>
            <Plus className="h-4 w-4 mr-2" />
            Create Job
          </Button>
        )}
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <Input
                placeholder="Search jobs..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                {JOB_STATUSES.map((status) => (
                  <SelectItem key={status} value={status}>
                    {status.replace('_', ' ')}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Jobs Table */}
      <Card>
        <CardHeader>
          <CardTitle>Job Postings</CardTitle>
          <CardDescription>
            {jobs.length} job{jobs.length !== 1 ? 's' : ''} found
          </CardDescription>
        </CardHeader>
        <CardContent>
          {jobs.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <Briefcase className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No jobs found</p>
              {isAdmin && (
                <Button onClick={handleOpenCreateDialog} className="mt-4" variant="outline">
                  Create your first job
                </Button>
              )}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-8"></TableHead>
                  <TableHead>Title</TableHead>
                  <TableHead>Department</TableHead>
                  <TableHead>Location</TableHead>
                  <TableHead>Role Profile</TableHead>
                  <TableHead>Requirements</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {jobs.map((job) => (
                  <>
                    <TableRow key={job.id}>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleRowExpansion(job.id)}
                        >
                          {expandedRows.has(job.id) ? (
                            <ChevronUp className="h-4 w-4" />
                          ) : (
                            <ChevronDown className="h-4 w-4" />
                          )}
                        </Button>
                      </TableCell>
                      <TableCell className="font-medium">{job.title}</TableCell>
                      <TableCell>
                        {job.department && (
                          <div className="flex items-center text-sm text-gray-600">
                            <Building2 className="h-3 w-3 mr-1" />
                            {job.department}
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        {job.location && (
                          <div className="flex items-center text-sm text-gray-600">
                            <MapPin className="h-3 w-3 mr-1" />
                            {job.location}
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        {job.role_profile_name ? (
                          <Badge variant="outline">{job.role_profile_name}</Badge>
                        ) : (
                          <span className="text-gray-400 text-sm">Not linked</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Badge variant="secondary">
                            {job.objective_requirements?.length || 0} requirements
                          </Badge>
                          {(!job.objective_requirements ||
                            job.objective_requirements.length === 0) && (
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleOpenRequirementsDialog(job)}
                              className="text-blue-600"
                            >
                              <Sparkles className="h-3 w-3 mr-1" />
                              Extract
                            </Button>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge className={statusColors[job.status]}>{job.status}</Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          {isAdmin && (
                            <>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleOpenEditDialog(job)}
                              >
                                <Edit className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleOpenDeleteDialog(job)}
                                className="text-red-600 hover:text-red-700"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </>
                          )}
                        </div>
                      </TableCell>
                    </TableRow>
                    {expandedRows.has(job.id) && (
                      <TableRow>
                        <TableCell colSpan={8} className="bg-gray-50">
                          <div className="p-4 space-y-4">
                            <div>
                              <h4 className="font-medium text-sm text-gray-700 mb-2">
                                Description
                              </h4>
                              <p className="text-sm text-gray-600 whitespace-pre-wrap">
                                {job.description.substring(0, 500)}
                                {job.description.length > 500 && '...'}
                              </p>
                            </div>

                            {job.objective_requirements &&
                              job.objective_requirements.length > 0 && (
                                <div>
                                  <h4 className="font-medium text-sm text-gray-700 mb-2">
                                    Objective Requirements
                                  </h4>
                                  <ul className="space-y-1">
                                    {job.objective_requirements.map((req, idx) => (
                                      <li key={idx} className="flex items-start gap-2 text-sm">
                                        {req.required ? (
                                          <Check className="h-4 w-4 text-green-600 mt-0.5" />
                                        ) : (
                                          <span className="h-4 w-4 text-gray-400 mt-0.5">○</span>
                                        )}
                                        <span>
                                          <Badge variant="outline" className="mr-2 text-xs">
                                            {req.type}
                                          </Badge>
                                          {req.requirement}
                                        </span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}

                            {job.responsibilities && job.responsibilities.length > 0 && (
                              <div>
                                <h4 className="font-medium text-sm text-gray-700 mb-2">
                                  Responsibilities
                                </h4>
                                <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                                  {job.responsibilities.map((resp, idx) => (
                                    <li key={idx}>{resp}</li>
                                  ))}
                                </ul>
                              </div>
                            )}

                            {job.suggested_traits && job.suggested_traits.length > 0 && (
                              <div>
                                <h4 className="font-medium text-sm text-gray-700 mb-2">
                                  Suggested Traits
                                </h4>
                                <div className="flex flex-wrap gap-1">
                                  {job.suggested_traits.map((trait, idx) => (
                                    <Badge key={idx} variant="secondary">
                                      {trait.replace(/_/g, ' ')}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            )}

                            <div className="pt-2">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleOpenRequirementsDialog(job)}
                              >
                                <Edit className="h-3 w-3 mr-2" />
                                Edit Requirements
                              </Button>
                            </div>
                          </div>
                        </TableCell>
                      </TableRow>
                    )}
                  </>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Create/Edit Dialog */}
      <Dialog
        open={createDialogOpen || editDialogOpen}
        onOpenChange={(open) => {
          if (!open) {
            setCreateDialogOpen(false);
            setEditDialogOpen(false);
            setSelectedJob(null);
            resetForm();
          }
        }}
      >
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{editDialogOpen ? 'Edit Job' : 'Create Job'}</DialogTitle>
            <DialogDescription>
              {editDialogOpen
                ? 'Update the job posting details'
                : 'Create a new job posting with objective requirements'}
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <Label htmlFor="title">Job Title *</Label>
                <Input
                  id="title"
                  value={formTitle}
                  onChange={(e) => setFormTitle(e.target.value)}
                  placeholder="e.g., Senior Software Engineer"
                />
              </div>

              <div>
                <Label htmlFor="department">Department</Label>
                <Input
                  id="department"
                  value={formDepartment}
                  onChange={(e) => setFormDepartment(e.target.value)}
                  placeholder="e.g., Engineering"
                />
              </div>

              <div>
                <Label htmlFor="location">Location</Label>
                <Input
                  id="location"
                  value={formLocation}
                  onChange={(e) => setFormLocation(e.target.value)}
                  placeholder="e.g., San Francisco, CA"
                />
              </div>

              <div>
                <Label htmlFor="employmentType">Employment Type</Label>
                <Select value={formEmploymentType} onValueChange={setFormEmploymentType}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {EMPLOYMENT_TYPES.map((type) => (
                      <SelectItem key={type} value={type}>
                        {type.replace('_', ' ')}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="status">Status</Label>
                <Select value={formStatus} onValueChange={setFormStatus}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {JOB_STATUSES.map((status) => (
                      <SelectItem key={status} value={status}>
                        {status.replace('_', ' ')}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="col-span-2">
                <Label htmlFor="roleProfile">Role Profile (for trait assessment)</Label>
                <Select value={formRoleProfileId} onValueChange={setFormRoleProfileId}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a role profile..." />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">None</SelectItem>
                    {roleProfiles.map((profile) => (
                      <SelectItem key={profile.id} value={profile.id}>
                        {profile.name} ({profile.role_category})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="col-span-2">
                <Label htmlFor="description">Job Description *</Label>
                <Textarea
                  id="description"
                  value={formDescription}
                  onChange={(e) => setFormDescription(e.target.value)}
                  placeholder="Paste the full job description here..."
                  rows={8}
                />
                <p className="text-xs text-gray-500 mt-1">
                  After creating the job, you can use AI to extract objective requirements from
                  this description.
                </p>
              </div>
            </div>

            {dialogError && (
              <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm">{dialogError}</div>
            )}
          </div>

          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => {
                setCreateDialogOpen(false);
                setEditDialogOpen(false);
                setSelectedJob(null);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button onClick={editDialogOpen ? handleUpdate : handleCreate} disabled={dialogLoading}>
              {dialogLoading && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
              {editDialogOpen ? 'Save Changes' : 'Create Job'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Requirements Dialog */}
      <Dialog open={requirementsDialogOpen} onOpenChange={setRequirementsDialogOpen}>
        <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Job Requirements - {selectedJob?.title}</DialogTitle>
            <DialogDescription>
              Define or edit the objective requirements for this job
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-6 py-4">
            {/* Extract button */}
            <div className="flex items-center justify-between bg-blue-50 p-4 rounded-lg">
              <div>
                <h4 className="font-medium text-blue-900">AI-Powered Extraction</h4>
                <p className="text-sm text-blue-700">
                  Automatically extract requirements from the job description
                </p>
              </div>
              <Button onClick={handleExtractRequirements} disabled={extracting}>
                {extracting ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <Sparkles className="h-4 w-4 mr-2" />
                )}
                Extract Requirements
              </Button>
            </div>

            {/* Objective Requirements */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <Label className="text-base font-medium">Objective Requirements</Label>
                <Button variant="outline" size="sm" onClick={addRequirement}>
                  <Plus className="h-3 w-3 mr-1" />
                  Add
                </Button>
              </div>
              <p className="text-sm text-gray-500 mb-3">
                These are hard requirements used for resume screening
              </p>
              <div className="space-y-2">
                {formRequirements.map((req, idx) => (
                  <div key={req.id} className="flex items-start gap-2 bg-gray-50 p-3 rounded-md">
                    <Select
                      value={req.type}
                      onValueChange={(v) => updateRequirement(idx, 'type', v)}
                    >
                      <SelectTrigger className="w-32">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {REQUIREMENT_TYPES.map((type) => (
                          <SelectItem key={type} value={type}>
                            {type}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Input
                      value={req.requirement}
                      onChange={(e) => updateRequirement(idx, 'requirement', e.target.value)}
                      placeholder="Describe the requirement..."
                      className="flex-1"
                    />
                    <Button
                      variant={req.required ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => updateRequirement(idx, 'required', !req.required)}
                      className="whitespace-nowrap"
                    >
                      {req.required ? 'Required' : 'Preferred'}
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => removeRequirement(idx)}>
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
                {formRequirements.length === 0 && (
                  <p className="text-sm text-gray-400 text-center py-4">
                    No requirements defined. Click &quot;Extract Requirements&quot; or add manually.
                  </p>
                )}
              </div>
            </div>

            {/* Nice to Haves */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <Label className="text-base font-medium">Nice-to-Haves</Label>
                <Button variant="outline" size="sm" onClick={addNiceToHave}>
                  <Plus className="h-3 w-3 mr-1" />
                  Add
                </Button>
              </div>
              <div className="space-y-2">
                {formNiceToHaves.map((item, idx) => (
                  <div key={idx} className="flex items-center gap-2">
                    <Input
                      value={item.description}
                      onChange={(e) => updateNiceToHave(idx, e.target.value)}
                      placeholder="Nice-to-have qualification..."
                      className="flex-1"
                    />
                    <Button variant="ghost" size="sm" onClick={() => removeNiceToHave(idx)}>
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
            </div>

            {/* Suggested Traits */}
            {formSuggestedTraits.length > 0 && (
              <div>
                <Label className="text-base font-medium">Suggested Traits</Label>
                <p className="text-sm text-gray-500 mb-2">
                  Traits recommended for assessment based on this role
                </p>
                <div className="flex flex-wrap gap-2">
                  {formSuggestedTraits.map((trait, idx) => (
                    <Badge key={idx} variant="secondary">
                      {trait.replace(/_/g, ' ')}
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {dialogError && (
              <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm">{dialogError}</div>
            )}
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setRequirementsDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleSaveRequirements} disabled={dialogLoading}>
              {dialogLoading && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
              Save Requirements
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Dialog */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Close Job</DialogTitle>
            <DialogDescription>
              Are you sure you want to close this job posting? This will mark it as closed but
              preserve the data.
            </DialogDescription>
          </DialogHeader>

          {selectedJob && (
            <div className="py-4">
              <p className="font-medium">{selectedJob.title}</p>
              <p className="text-sm text-gray-500">
                {selectedJob.department} {selectedJob.location && `• ${selectedJob.location}`}
              </p>
            </div>
          )}

          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteDialogOpen(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete} disabled={dialogLoading}>
              {dialogLoading && <Loader2 className="h-4 w-4 mr-2 animate-spin" />}
              Close Job
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
