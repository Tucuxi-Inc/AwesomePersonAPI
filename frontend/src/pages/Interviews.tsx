import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { InterviewSession } from '@/types';
import {
  Play,
  Eye,
  Clock,
  CheckCircle2,
  AlertTriangle,
  Loader2,
  ClipboardList,
} from 'lucide-react';

const statusConfig: Record<string, { label: string; color: string; icon: typeof Clock }> = {
  NOT_STARTED: { label: 'Not Started', color: 'bg-gray-100 text-gray-800', icon: Clock },
  IN_PROGRESS: { label: 'In Progress', color: 'bg-amber-100 text-amber-800', icon: Play },
  COMPLETED: { label: 'Completed', color: 'bg-green-100 text-green-800', icon: CheckCircle2 },
  CANCELLED: { label: 'Cancelled', color: 'bg-red-100 text-red-800', icon: AlertTriangle },
};

export default function Interviews() {
  const navigate = useNavigate();
  const [sessions] = useState<InterviewSession[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error] = useState<string | null>(null);

  // For demo purposes, show the current active interview from localStorage if any
  useEffect(() => {
    // This would typically fetch from the API
    // For now, just show empty state since backend listing isn't implemented
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Interviews</h1>
          <p className="text-muted-foreground">View and manage interview sessions</p>
        </div>
        <Button onClick={() => navigate('/candidates')}>
          <Play className="mr-2 h-4 w-4" />
          Start New Interview
        </Button>
      </div>

      {/* Error state */}
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4 text-destructive">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Empty state */}
      {sessions.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center">
            <ClipboardList className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Interview Sessions</h3>
            <p className="text-muted-foreground mb-4">
              Start your first interview by selecting a candidate.
            </p>
            <Button onClick={() => navigate('/candidates')}>
              <Play className="mr-2 h-4 w-4" />
              Start Interview
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Sessions list */}
      {sessions.length > 0 && (
        <div className="space-y-4">
          {sessions.map((session) => {
            const config = statusConfig[session.status] || statusConfig.NOT_STARTED;
            const Icon = config.icon;

            return (
              <Card key={session.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                        <Icon className="h-5 w-5 text-primary" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-medium">Session {session.id.substring(0, 8)}</span>
                          <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
                            {config.label}
                          </span>
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {session.traits_completed} / {session.traits_total} traits assessed
                          {session.started_at && ` - Started ${new Date(session.started_at).toLocaleDateString()}`}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      {session.status === 'IN_PROGRESS' && (
                        <Button
                          size="sm"
                          onClick={() => navigate(`/interviews/${session.id}`)}
                        >
                          <Play className="mr-1.5 h-4 w-4" />
                          Continue
                        </Button>
                      )}
                      {session.status === 'COMPLETED' && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => navigate(`/interviews/${session.id}/results`)}
                        >
                          <Eye className="mr-1.5 h-4 w-4" />
                          View Results
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
