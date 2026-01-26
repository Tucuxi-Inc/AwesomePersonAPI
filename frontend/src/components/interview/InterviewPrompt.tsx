import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { ProbeType } from '@/types';
import { Brain, MessageCircle, RefreshCw, Lightbulb, AlertTriangle, CheckCircle } from 'lucide-react';

interface InterviewPromptProps {
  prompt: string;
  promptType: ProbeType;
  traitName?: string | null;
  isLoading?: boolean;
}

const probeTypeConfig: Record<ProbeType, { label: string; icon: typeof Brain; color: string }> = {
  INTRODUCTION: { label: 'Introduction', icon: MessageCircle, color: 'text-blue-600 bg-blue-50' },
  PRIMARY: { label: 'Primary Question', icon: Brain, color: 'text-purple-600 bg-purple-50' },
  FOLLOW_UP: { label: 'Follow-up', icon: RefreshCw, color: 'text-amber-600 bg-amber-50' },
  RECURSION: { label: 'Additional Example', icon: RefreshCw, color: 'text-orange-600 bg-orange-50' },
  REFLECTION: { label: 'Reflection', icon: Lightbulb, color: 'text-green-600 bg-green-50' },
  CONFLICT: { label: 'Challenge Scenario', icon: AlertTriangle, color: 'text-red-600 bg-red-50' },
  CLOSING: { label: 'Closing', icon: CheckCircle, color: 'text-teal-600 bg-teal-50' },
  COMPLETE: { label: 'Complete', icon: CheckCircle, color: 'text-green-600 bg-green-50' },
};

export function InterviewPrompt({ prompt, promptType, traitName, isLoading }: InterviewPromptProps) {
  const config = probeTypeConfig[promptType] || probeTypeConfig.PRIMARY;
  const Icon = config.icon;

  if (isLoading) {
    return (
      <Card className="border-2 border-primary/20">
        <CardContent className="p-6">
          <div className="animate-pulse space-y-4">
            <div className="flex items-center gap-2">
              <div className="h-6 w-6 rounded-full bg-muted" />
              <div className="h-4 w-32 rounded bg-muted" />
            </div>
            <div className="space-y-2">
              <div className="h-4 w-full rounded bg-muted" />
              <div className="h-4 w-3/4 rounded bg-muted" />
              <div className="h-4 w-1/2 rounded bg-muted" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-2 border-primary/20">
      <CardContent className="p-6">
        <div className="space-y-4">
          {/* Probe type badge and trait indicator */}
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div className={cn('inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium', config.color)}>
              <Icon className="h-4 w-4" />
              {config.label}
            </div>
            {traitName && (
              <div className="text-sm text-muted-foreground">
                Assessing: <span className="font-medium text-foreground">{traitName}</span>
              </div>
            )}
          </div>

          {/* The question */}
          <div className="text-lg leading-relaxed">
            {prompt}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
