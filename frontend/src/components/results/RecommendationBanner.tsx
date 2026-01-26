import { cn } from '@/lib/utils';
import { Recommendation } from '@/types';
import { CheckCircle2, ThumbsUp, Pause, XCircle, Shield } from 'lucide-react';

interface RecommendationBannerProps {
  recommendation: Recommendation;
  confidence: number;
  rationale: string;
  className?: string;
}

const recommendationConfig: Record<Recommendation, {
  label: string;
  icon: typeof CheckCircle2;
  bgColor: string;
  textColor: string;
  borderColor: string;
}> = {
  STRONG_HIRE: {
    label: 'Strong Hire',
    icon: CheckCircle2,
    bgColor: 'bg-green-50',
    textColor: 'text-green-800',
    borderColor: 'border-green-200',
  },
  HIRE: {
    label: 'Hire',
    icon: ThumbsUp,
    bgColor: 'bg-emerald-50',
    textColor: 'text-emerald-800',
    borderColor: 'border-emerald-200',
  },
  HOLD: {
    label: 'Hold',
    icon: Pause,
    bgColor: 'bg-amber-50',
    textColor: 'text-amber-800',
    borderColor: 'border-amber-200',
  },
  NO_HIRE: {
    label: 'No Hire',
    icon: XCircle,
    bgColor: 'bg-red-50',
    textColor: 'text-red-800',
    borderColor: 'border-red-200',
  },
};

export function RecommendationBanner({
  recommendation,
  confidence,
  rationale,
  className,
}: RecommendationBannerProps) {
  const config = recommendationConfig[recommendation];
  const Icon = config.icon;
  const confidencePercent = Math.round(confidence * 100);

  return (
    <div
      className={cn(
        'rounded-lg border-2 p-6',
        config.bgColor,
        config.borderColor,
        className
      )}
    >
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className={cn('p-3 rounded-full', config.bgColor, 'ring-2 ring-white')}>
            <Icon className={cn('h-8 w-8', config.textColor)} />
          </div>
          <div>
            <div className="text-sm text-muted-foreground mb-1">Overall Recommendation</div>
            <div className={cn('text-2xl font-bold', config.textColor)}>
              {config.label}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Shield className={cn('h-5 w-5', config.textColor)} />
            <div>
              <div className="text-sm text-muted-foreground">Confidence</div>
              <div className={cn('text-lg font-semibold', config.textColor)}>
                {confidencePercent}%
              </div>
            </div>
          </div>
        </div>
      </div>

      {rationale && (
        <div className="mt-4 pt-4 border-t border-current/10">
          <div className="text-sm text-muted-foreground mb-1">Rationale</div>
          <p className={cn('text-sm', config.textColor)}>{rationale}</p>
        </div>
      )}
    </div>
  );
}
