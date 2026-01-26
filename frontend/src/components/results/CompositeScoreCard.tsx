import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { Target, BarChart3, FileCheck } from 'lucide-react';

interface CompositeScoreCardProps {
  compositeScore: number;
  evidenceQuality: string;
  confidence: number;
  traitCount: number;
  className?: string;
}

export function CompositeScoreCard({
  compositeScore,
  evidenceQuality,
  confidence,
  traitCount,
  className,
}: CompositeScoreCardProps) {
  const scorePercent = Math.round(compositeScore * 100);
  const confidencePercent = Math.round(confidence * 100);

  // Score color based on value
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-emerald-600';
    if (score >= 0.4) return 'text-amber-600';
    return 'text-red-600';
  };

  // Evidence quality color
  const getQualityColor = (quality: string) => {
    switch (quality.toLowerCase()) {
      case 'high':
        return 'text-green-600 bg-green-50';
      case 'medium':
        return 'text-amber-600 bg-amber-50';
      case 'low':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-muted-foreground bg-muted';
    }
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Target className="h-5 w-5 text-primary" />
          Composite Score
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Main score display */}
        <div className="text-center">
          <div className={cn('text-5xl font-bold', getScoreColor(compositeScore))}>
            {scorePercent}
          </div>
          <div className="text-sm text-muted-foreground mt-1">out of 100</div>
        </div>

        {/* Score bar */}
        <div className="space-y-2">
          <div className="h-3 bg-muted rounded-full overflow-hidden">
            <div
              className={cn(
                'h-full rounded-full transition-all duration-500',
                compositeScore >= 0.8 ? 'bg-green-500' :
                compositeScore >= 0.6 ? 'bg-emerald-500' :
                compositeScore >= 0.4 ? 'bg-amber-500' :
                'bg-red-500'
              )}
              style={{ width: `${scorePercent}%` }}
            />
          </div>
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-3 gap-4 pt-4 border-t">
          <div className="text-center">
            <div className="flex items-center justify-center gap-1 mb-1">
              <BarChart3 className="h-4 w-4 text-muted-foreground" />
            </div>
            <div className="text-lg font-semibold">{confidencePercent}%</div>
            <div className="text-xs text-muted-foreground">Confidence</div>
          </div>

          <div className="text-center">
            <div className="flex items-center justify-center gap-1 mb-1">
              <FileCheck className="h-4 w-4 text-muted-foreground" />
            </div>
            <div className={cn(
              'text-lg font-semibold px-2 py-0.5 rounded inline-block',
              getQualityColor(evidenceQuality)
            )}>
              {evidenceQuality}
            </div>
            <div className="text-xs text-muted-foreground">Evidence Quality</div>
          </div>

          <div className="text-center">
            <div className="flex items-center justify-center gap-1 mb-1">
              <Target className="h-4 w-4 text-muted-foreground" />
            </div>
            <div className="text-lg font-semibold">{traitCount}</div>
            <div className="text-xs text-muted-foreground">Traits Assessed</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
