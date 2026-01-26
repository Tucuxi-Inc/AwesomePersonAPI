import { useAuth } from '@/hooks/useAuth';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, Briefcase, FileText, Brain } from 'lucide-react';

const stats = [
  { name: 'Total Candidates', value: '0', icon: Users, description: 'Active candidates' },
  { name: 'Role Profiles', value: '0', icon: Briefcase, description: 'Defined roles' },
  { name: 'Traits', value: '24', icon: Brain, description: 'In taxonomy' },
  { name: 'Rubrics', value: '6', icon: FileText, description: 'Default rubrics' },
];

export function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="space-y-8">
      {/* Welcome section */}
      <div>
        <h1 className="text-3xl font-bold">Welcome back, {user?.full_name?.split(' ')[0]}</h1>
        <p className="text-muted-foreground mt-1">
          Here's an overview of your talent assessment platform.
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.name}</CardTitle>
              <stat.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">{stat.description}</p>
            </CardContent>
          </Card>
        ))}
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
                <span className="w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs mr-3">1</span>
                Create role profiles for positions you're hiring
              </li>
              <li className="flex items-center">
                <span className="w-6 h-6 rounded-full bg-muted text-muted-foreground flex items-center justify-center text-xs mr-3">2</span>
                Customize rubrics for your organization
              </li>
              <li className="flex items-center">
                <span className="w-6 h-6 rounded-full bg-muted text-muted-foreground flex items-center justify-center text-xs mr-3">3</span>
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
