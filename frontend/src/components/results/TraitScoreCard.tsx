import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { TraitScoreResponse } from '@/types';
import { Brain, AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

interface TraitScoreCardProps {
  score: TraitScoreResponse;
  className?: string;
}

export function TraitScoreCard({ score, className }: TraitScoreCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const {
    trait_name,
    raw_score,
    calibrated_score,
    confidence,
    explanation,
    evidence_summary,
    signal_gaps,
  } = score;

  const confidencePercent = Math.round(confidence * 100);

  // Score color based on calibrated score (1-5 scale)
  const getScoreColor = (score: number) => {
    if (score >= 4) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 3) return 'text-emerald-600 bg-emerald-50 border-emerald-200';
    if (score >= 2) return 'text-amber-600 bg-amber-50 border-amber-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  // Score label
  const getScoreLabel = (score: number) => {
    if (score >= 5) return 'Exceptional';
    if (score >= 4) return 'Strong';
    if (score >= 3) return 'Competent';
    if (score >= 2) return 'Developing';
    return 'Limited';
  };

  const scoreColorClass = getScoreColor(calibrated_score);

  return (
    <Card className={cn('overflow-hidden', className)}>
      <CardContent className="p-0">
        {/* Header - always visible */}
        <button
          className="w-full p-4 flex items-center justify-between hover:bg-muted/30 transition-colors"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-primary/10">
              <Brain className="h-5 w-5 text-primary" />
            </div>
            <div className="text-left">
              <h3 className="font-semibold">{trait_name}</h3>
              <p className="text-sm text-muted-foreground">
                {confidencePercent}% confidence
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Score badge */}
            <div className={cn(
              'px-3 py-1.5 rounded-lg border font-semibold',
              scoreColorClass
            )}>
              <span className="text-xl">{calibrated_score}</span>
              <span className="text-sm ml-1">/ 5</span>
            </div>

            {/* Expand icon */}
            {isExpanded ? (
              <ChevronUp className="h-5 w-5 text-muted-foreground" />
            ) : (
              <ChevronDown className="h-5 w-5 text-muted-foreground" />
            )}
          </div>
        </button>

        {/* Expanded content */}
        {isExpanded && (
          <div className="px-4 pb-4 pt-0 space-y-4 border-t">
            {/* Score visualization */}
            <div className="pt-4">
              <div className="flex items-center justify-between text-sm mb-2">
                <span className="text-muted-foreground">Score Level</span>
                <span className={cn('font-medium', scoreColorClass.split(' ')[0])}>
                  {getScoreLabel(calibrated_score)}
                </span>
              </div>
              <div className="flex gap-1">
                {[1, 2, 3, 4, 5].map((level) => (
                  <div
                    key={level}
                    className={cn(
                      'flex-1 h-2 rounded-full',
                      level <= calibrated_score
                        ? calibrated_score >= 4
                          ? 'bg-green-500'
                          : calibrated_score >= 3
                          ? 'bg-emerald-500'
                          : calibrated_score >= 2
                          ? 'bg-amber-500'
                          : 'bg-red-500'
                        : 'bg-muted'
                    )}
                  />
                ))}
              </div>
            </div>

            {/* Explanation */}
            <div>
              <div className="text-sm font-medium text-muted-foreground mb-1">
                Score Explanation
              </div>
              <p className="text-sm">{explanation}</p>
            </div>

            {/* Evidence summary */}
            {evidence_summary && (
              <div>
                <div className="text-sm font-medium text-muted-foreground mb-1">
                  Evidence Summary
                </div>
                <p className="text-sm">{evidence_summary}</p>
              </div>
            )}

            {/* Signal gaps */}
            {signal_gaps.length > 0 && (
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-3">
                <div className="flex items-center gap-2 text-amber-800 mb-2">
                  <AlertCircle className="h-4 w-4" />
                  <span className="text-sm font-medium">Signal Gaps</span>
                </div>
                <ul className="text-sm text-amber-700 space-y-1">
                  {signal_gaps.map((gap, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="text-amber-500">-</span>
                      {gap}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Raw vs calibrated score note */}
            {raw_score !== calibrated_score && (
              <div className="text-xs text-muted-foreground pt-2 border-t">
                Raw score: {raw_score} / Calibrated score: {calibrated_score}
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
