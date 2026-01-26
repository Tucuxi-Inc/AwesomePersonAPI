import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { api } from '@/api/client';
import { Candidate, CandidateStatus } from '@/types';
import {
  Plus,
  Search,
  Play,
  Eye,
  User,
  Briefcase,
  Mail,
  MoreHorizontal,
  AlertTriangle,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Filter,
} from 'lucide-react';

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

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Candidates</h1>
          <p className="text-muted-foreground">Manage candidates and conduct interviews</p>
        </div>
        <Button onClick={() => navigate('/candidates/new')} disabled>
          <Plus className="mr-2 h-4 w-4" />
          Add Candidate
        </Button>
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
                : 'Get started by adding your first candidate.'}
            </p>
            <Button onClick={() => navigate('/candidates/new')} disabled>
              <Plus className="mr-2 h-4 w-4" />
              Add Candidate
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
                      variant="default"
                      size="sm"
                      onClick={() => handleStartInterview(candidate.id)}
                    >
                      <Play className="mr-1.5 h-4 w-4" />
                      Interview
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
                    <Button variant="ghost" size="icon">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
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
    </div>
  );
}
