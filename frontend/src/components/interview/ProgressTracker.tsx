import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { TraitProgress } from '@/types';
import { Clock, CheckCircle2, Circle, ArrowRight } from 'lucide-react';

interface ProgressTrackerProps {
  overallProgress: number;
  traitProgressMap: Record<string, TraitProgress>;
  currentTraitId?: string | null;
  elapsedMinutes: number;
  maxDurationMinutes?: number;
  className?: string;
}

export function ProgressTracker({
  overallProgress,
  traitProgressMap,
  currentTraitId,
  elapsedMinutes,
  maxDurationMinutes = 60,
  className,
}: ProgressTrackerProps) {
  const traitProgressList = Object.values(traitProgressMap);
  const completedTraits = traitProgressList.filter(tp => tp.is_complete).length;
  const totalTraits = traitProgressList.length;
  const progressPercent = Math.round(overallProgress * 100);
  const timeRemaining = Math.max(0, maxDurationMinutes - elapsedMinutes);

  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <CardTitle className="text-base font-medium">Progress</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Overall progress bar */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Overall Progress</span>
            <span className="font-medium">{progressPercent}%</span>
          </div>
          <div className="h-2.5 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full bg-primary transition-all duration-500 ease-out rounded-full"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>

        {/* Trait completion count */}
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 text-green-600" />
            <span>Traits Assessed</span>
          </div>
          <span className="font-medium">{completedTraits} / {totalTraits}</span>
        </div>

        {/* Time remaining */}
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2">
            <Clock className={cn('h-4 w-4', timeRemaining < 10 ? 'text-amber-600' : 'text-muted-foreground')} />
            <span>Time Elapsed</span>
          </div>
          <span className={cn('font-medium', timeRemaining < 10 && 'text-amber-600')}>
            {elapsedMinutes} min / {maxDurationMinutes} min
          </span>
        </div>

        {/* Trait list */}
        <div className="space-y-2">
          <div className="text-sm font-medium mb-3">Trait Assessment</div>
          <div className="space-y-2">
            {traitProgressList.map((tp) => (
              <TraitProgressItem
                key={tp.trait_id}
                progress={tp}
                isCurrent={tp.trait_id === currentTraitId}
              />
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

interface TraitProgressItemProps {
  progress: TraitProgress;
  isCurrent: boolean;
}

function TraitProgressItem({ progress, isCurrent }: TraitProgressItemProps) {
  const { trait_name, is_complete, phase, star_coverage } = progress;

  // Calculate STAR coverage
  const starComponents = ['situation', 'task', 'action', 'result'] as const;
  const coveredCount = starComponents.filter(s => star_coverage[s]).length;
  const starPercent = Math.round((coveredCount / 4) * 100);

  return (
    <div
      className={cn(
        'flex items-center gap-3 p-2.5 rounded-md transition-colors',
        isCurrent && 'bg-primary/5 ring-1 ring-primary/20',
        is_complete && 'bg-green-50'
      )}
    >
      {/* Status icon */}
      {is_complete ? (
        <CheckCircle2 className="h-4 w-4 text-green-600 flex-shrink-0" />
      ) : isCurrent ? (
        <ArrowRight className="h-4 w-4 text-primary flex-shrink-0 animate-pulse" />
      ) : (
        <Circle className="h-4 w-4 text-muted-foreground flex-shrink-0" />
      )}

      {/* Trait name and details */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <span className={cn(
            'text-sm font-medium truncate',
            is_complete && 'text-green-700',
            isCurrent && 'text-primary'
          )}>
            {trait_name}
          </span>
          <span className="text-xs text-muted-foreground flex-shrink-0">
            {is_complete ? 'Complete' : phase}
          </span>
        </div>

        {/* STAR mini-bar */}
        {!is_complete && isCurrent && (
          <div className="mt-1.5 flex items-center gap-1.5">
            <div className="flex gap-0.5">
              {starComponents.map((component) => (
                <div
                  key={component}
                  className={cn(
                    'w-5 h-1 rounded-full',
                    star_coverage[component] ? 'bg-primary' : 'bg-muted'
                  )}
                  title={`${component.charAt(0).toUpperCase() + component.slice(1)}: ${star_coverage[component] ? 'Covered' : 'Missing'}`}
                />
              ))}
            </div>
            <span className="text-xs text-muted-foreground">
              STAR {starPercent}%
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
