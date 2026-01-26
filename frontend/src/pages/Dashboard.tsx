import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { api } from '@/api/client';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, Briefcase, FileText, Brain, UserCheck, PlayCircle, CheckCircle, Loader2 } from 'lucide-react';

interface DashboardStats {
  total_candidates: number;
  role_profiles: number;
  traits: number;
  rubrics: number;
  top_performers: number;
  interviews_completed: number;
  interviews_in_progress: number;
}

export function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const response = await api.getDashboardStats();
        setStats(response.data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch dashboard stats:', err);
        setError('Failed to load dashboard statistics');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const statCards = [
    { name: 'Total Candidates', value: stats?.total_candidates ?? 0, icon: Users, description: 'Active candidates' },
    { name: 'Role Profiles', value: stats?.role_profiles ?? 0, icon: Briefcase, description: 'Defined roles' },
    { name: 'Traits', value: stats?.traits ?? 0, icon: Brain, description: 'In taxonomy' },
    { name: 'Rubrics', value: stats?.rubrics ?? 0, icon: FileText, description: 'Scoring rubrics' },
  ];

  const activityCards = [
    { name: 'Top Performers', value: stats?.top_performers ?? 0, icon: UserCheck, description: 'Profiled performers' },
    { name: 'In Progress', value: stats?.interviews_in_progress ?? 0, icon: PlayCircle, description: 'Active interviews' },
    { name: 'Completed', value: stats?.interviews_completed ?? 0, icon: CheckCircle, description: 'Finished assessments' },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome section */}
      <div>
        <h1 className="text-3xl font-bold">Welcome back, {user?.full_name?.split(' ')[0]}</h1>
        <p className="text-muted-foreground mt-1">
          Here's an overview of your talent assessment platform.
        </p>
      </div>

      {/* Error state */}
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4 text-destructive">
          {error}
        </div>
      )}

      {/* Stats grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.name}</CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {loading ? (
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              ) : (
                <>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <p className="text-xs text-muted-foreground">{stat.description}</p>
                </>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Activity stats */}
      <div>
        <h2 className="text-lg font-semibold mb-4">Activity</h2>
        <div className="grid gap-4 md:grid-cols-3">
          {activityCards.map((stat) => (
            <Card key={stat.name}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.name}</CardTitle>
                <stat.icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                {loading ? (
                  <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                ) : (
                  <>
                    <div className="text-2xl font-bold">{stat.value}</div>
                    <p className="text-xs text-muted-foreground">{stat.description}</p>
                  </>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Quick actions */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Getting Started</CardTitle>
            <CardDescription>
              Set up your assessment platform in a few steps
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3 text-sm">
              <li className="flex items-center">
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs mr-3 ${
                  (stats?.role_profiles ?? 0) > 0 ? 'bg-green-500 text-white' : 'bg-primary text-primary-foreground'
                }`}>1</span>
                Create role profiles for positions you're hiring
              </li>
              <li className="flex items-center">
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs mr-3 ${
                  (stats?.rubrics ?? 0) > 6 ? 'bg-green-500 text-white' : 'bg-muted text-muted-foreground'
                }`}>2</span>
                Customize rubrics for your organization
              </li>
              <li className="flex items-center">
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs mr-3 ${
                  (stats?.total_candidates ?? 0) > 0 ? 'bg-green-500 text-white' : 'bg-muted text-muted-foreground'
                }`}>3</span>
                Add candidates and start assessments
              </li>
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>STAR+ Methodology</CardTitle>
            <CardDescription>
              Evidence-based behavioral assessment
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm">
              <li><strong>S</strong>ituation - What was the context?</li>
              <li><strong>T</strong>ask - What was your responsibility?</li>
              <li><strong>A</strong>ction - What did YOU do?</li>
              <li><strong>R</strong>esult - What happened?</li>
              <li><strong>+</strong> Reflection and Recursion</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
