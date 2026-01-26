import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { TraitProgress, ProbePhase } from '@/types';
import { Brain, CheckCircle2, AlertCircle, TrendingUp } from 'lucide-react';

interface TraitProgressCardProps {
  progress: TraitProgress;
  className?: string;
}

const phaseLabels: Record<ProbePhase, string> = {
  PRIMARY: 'Primary Question',
  FOLLOW_UP: 'Follow-up Questions',
  RECURSION: 'Additional Examples',
  REFLECTION: 'Reflection',
  CONFLICT: 'Challenge Exploration',
  COMPLETE: 'Complete',
};

export function TraitProgressCard({ progress, className }: TraitProgressCardProps) {
  const {
    trait_name,
    phase,
    probes_used,
    evidence_count,
    behavioral_evidence_count,
    confidence,
    star_coverage,
    has_conflict_example,
    is_complete,
  } = progress;

  const confidencePercent = Math.round(confidence * 100);
  const starComponents = ['situation', 'task', 'action', 'result'] as const;

  return (
    <Card className={cn('overflow-hidden', className)}>
      <CardContent className="p-4">
        <div className="space-y-4">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <div className={cn(
                'p-2 rounded-lg',
                is_complete ? 'bg-green-100' : 'bg-primary/10'
              )}>
                {is_complete ? (
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                ) : (
                  <Brain className="h-5 w-5 text-primary" />
                )}
              </div>
              <div>
                <h3 className="font-semibold">{trait_name}</h3>
                <p className="text-sm text-muted-foreground">{phaseLabels[phase]}</p>
              </div>
            </div>

            {/* Confidence badge */}
            <div className={cn(
              'px-2.5 py-1 rounded-full text-sm font-medium',
              confidencePercent >= 70 ? 'bg-green-100 text-green-700' :
              confidencePercent >= 40 ? 'bg-amber-100 text-amber-700' :
              'bg-red-100 text-red-700'
            )}>
              {confidencePercent}% confidence
            </div>
          </div>

          {/* STAR Coverage */}
          <div className="space-y-2">
            <div className="text-sm font-medium text-muted-foreground">STAR Coverage</div>
            <div className="grid grid-cols-4 gap-2">
              {starComponents.map((component) => (
                <div
                  key={component}
                  className={cn(
                    'text-center p-2 rounded-lg text-sm font-medium',
                    star_coverage[component]
                      ? 'bg-primary/10 text-primary'
                      : 'bg-muted text-muted-foreground'
                  )}
                >
                  <div className="text-xs mb-1">
                    {component.charAt(0).toUpperCase()}
                  </div>
                  <div className="text-xs opacity-75">
                    {component.charAt(0).toUpperCase() + component.slice(1)}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4 pt-2 border-t">
            <div className="text-center">
              <div className="text-lg font-semibold">{probes_used}</div>
              <div className="text-xs text-muted-foreground">Probes Used</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold">{evidence_count}</div>
              <div className="text-xs text-muted-foreground">Evidence Items</div>
            </div>
            <div className="text-center">
              <div className="text-lg font-semibold">{behavioral_evidence_count}</div>
              <div className="text-xs text-muted-foreground">Behavioral</div>
            </div>
          </div>

          {/* Indicators */}
          <div className="flex items-center gap-4 pt-2 border-t">
            {has_conflict_example && (
              <div className="flex items-center gap-1.5 text-sm text-amber-600">
                <AlertCircle className="h-4 w-4" />
                <span>Has conflict example</span>
              </div>
            )}
            {behavioral_evidence_count > 0 && (
              <div className="flex items-center gap-1.5 text-sm text-green-600">
                <TrendingUp className="h-4 w-4" />
                <span>Strong behavioral evidence</span>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
