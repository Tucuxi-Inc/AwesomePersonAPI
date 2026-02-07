import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '@/api/client';
import { SimpleAssessment, SimpleAssessmentStatus } from '@/types';
import { useSimpleStore } from '@/store/simpleStore';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
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
import { Skeleton } from '@/components/ui/skeleton';
import { Plus, Briefcase, Users, CheckCircle, Clock, Trash2 } from 'lucide-react';
import { toast } from 'sonner';
import { format } from 'date-fns';

const statusColors: Record<SimpleAssessmentStatus, string> = {
  DRAFT: 'bg-gray-100 text-gray-800',
  REQUIREMENTS_PENDING: 'bg-yellow-100 text-yellow-800',
  TRAITS_PENDING: 'bg-yellow-100 text-yellow-800',
  CANDIDATES_PENDING: 'bg-blue-100 text-blue-800',
  INTERVIEWING: 'bg-purple-100 text-purple-800',
  COMPLETED: 'bg-green-100 text-green-800',
};

const statusLabels: Record<SimpleAssessmentStatus, string> = {
  DRAFT: 'Draft',
  REQUIREMENTS_PENDING: 'Confirm Requirements',
  TRAITS_PENDING: 'Select Traits',
  CANDIDATES_PENDING: 'Add Candidates',
  INTERVIEWING: 'Interviewing',
  COMPLETED: 'Completed',
};

export default function SimpleDashboard() {
  const navigate = useNavigate();
  const { setAssessments, assessments, setCurrentAssessment, reset } = useSimpleStore();
  const [isLoading, setIsLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [assessmentToDelete, setAssessmentToDelete] = useState<SimpleAssessment | null>(null);

  useEffect(() => {
    loadAssessments();
  }, [statusFilter]);

  const loadAssessments = async () => {
    setIsLoading(true);
    try {
      const params: { status?: string } = {};
      if (statusFilter !== 'all') {
        params.status = statusFilter;
      }
      const response = await api.getSimpleAssessments(params);
      setAssessments(response.data.items || response.data);
    } catch (error) {
      console.error('Failed to load assessments:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewAssessment = () => {
    reset();
    navigate('/simple/new');
  };

  const handleViewAssessment = (assessment: SimpleAssessment) => {
    setCurrentAssessment(assessment);
    navigate(`/simple/assessments/${assessment.id}`);
  };

  const handleDeleteAssessment = async () => {
    if (!assessmentToDelete) return;
    try {
      await api.deleteSimpleAssessment(assessmentToDelete.id);
      toast.success(`Assessment "${assessmentToDelete.job_title}" deleted`);
      loadAssessments();
    } catch {
      toast.error('Failed to delete assessment');
    } finally {
      setDeleteDialogOpen(false);
      setAssessmentToDelete(null);
    }
  };

  // Calculate stats
  const stats = {
    total: assessments.length,
    active: assessments.filter((a) =>
      ['REQUIREMENTS_PENDING', 'TRAITS_PENDING', 'CANDIDATES_PENDING', 'INTERVIEWING'].includes(
        a.status
      )
    ).length,
    completed: assessments.filter((a) => a.status === 'COMPLETED').length,
    totalCandidates: assessments.reduce((sum, a) => sum + a.total_candidates, 0),
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Simple Assessments</h1>
          <p className="text-muted-foreground">
            Streamlined 7-step workflow for quick candidate assessments
          </p>
        </div>
        <Button onClick={handleNewAssessment}>
          <Plus className="mr-2 h-4 w-4" />
          New Assessment
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assessments</CardTitle>
            <Briefcase className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.active}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completed}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Candidates</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalCandidates}</div>
          </CardContent>
        </Card>
      </div>

      {/* Assessments Table */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Assessments</CardTitle>
              <CardDescription>
                Click on an assessment to continue the wizard or view results
              </CardDescription>
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                <SelectItem value="DRAFT">Draft</SelectItem>
                <SelectItem value="REQUIREMENTS_PENDING">Requirements Pending</SelectItem>
                <SelectItem value="TRAITS_PENDING">Traits Pending</SelectItem>
                <SelectItem value="CANDIDATES_PENDING">Candidates Pending</SelectItem>
                <SelectItem value="INTERVIEWING">Interviewing</SelectItem>
                <SelectItem value="COMPLETED">Completed</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="flex items-center gap-4 py-3">
                  <Skeleton className="h-5 w-48" />
                  <Skeleton className="h-6 w-24 rounded-full" />
                  <Skeleton className="h-5 w-12" />
                  <Skeleton className="h-5 w-16" />
                  <Skeleton className="h-5 w-28" />
                </div>
              ))}
            </div>
          ) : assessments.length === 0 ? (
            <div className="text-center py-8">
              <Briefcase className="mx-auto h-12 w-12 text-muted-foreground" />
              <h3 className="mt-2 text-sm font-semibold">No assessments</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                Get started by creating a new assessment.
              </p>
              <div className="mt-6">
                <Button onClick={handleNewAssessment}>
                  <Plus className="mr-2 h-4 w-4" />
                  New Assessment
                </Button>
              </div>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Job Title</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Candidates</TableHead>
                  <TableHead>Interviews</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {assessments.map((assessment) => (
                  <TableRow
                    key={assessment.id}
                    className="cursor-pointer hover:bg-muted/50"
                    onClick={() => handleViewAssessment(assessment)}
                  >
                    <TableCell className="font-medium">{assessment.job_title}</TableCell>
                    <TableCell>
                      <Badge className={statusColors[assessment.status]}>
                        {statusLabels[assessment.status]}
                      </Badge>
                    </TableCell>
                    <TableCell>{assessment.total_candidates}</TableCell>
                    <TableCell>
                      {assessment.interviews_completed} / {assessment.total_candidates}
                    </TableCell>
                    <TableCell>
                      {format(new Date(assessment.created_at), 'MMM d, yyyy')}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <Button variant="ghost" size="sm">
                          {assessment.status === 'COMPLETED' ? 'View Results' : 'Continue'}
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 text-muted-foreground hover:text-destructive"
                          onClick={(e) => {
                            e.stopPropagation();
                            setAssessmentToDelete(assessment);
                            setDeleteDialogOpen(true);
                          }}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Assessment?</AlertDialogTitle>
            <AlertDialogDescription>
              This will permanently delete the assessment "{assessmentToDelete?.job_title}" and all
              associated candidate data. This action cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteAssessment}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
