import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { CounterIndicatorFlag } from '@/types';
import { AlertTriangle, ShieldAlert, AlertOctagon } from 'lucide-react';

interface CounterIndicatorAlertProps {
  flags: CounterIndicatorFlag[];
  className?: string;
}

export function CounterIndicatorAlert({ flags, className }: CounterIndicatorAlertProps) {
  if (flags.length === 0) {
    return null;
  }

  const criticalFlags = flags.filter(f => f.severity === 'CRITICAL');
  const warningFlags = flags.filter(f => f.severity === 'WARNING');
  const hasCritical = criticalFlags.length > 0;

  return (
    <Card className={cn(
      'border-2',
      hasCritical ? 'border-red-300 bg-red-50/50' : 'border-amber-300 bg-amber-50/50',
      className
    )}>
      <CardHeader className="pb-3">
        <CardTitle className={cn(
          'flex items-center gap-2 text-lg',
          hasCritical ? 'text-red-800' : 'text-amber-800'
        )}>
          {hasCritical ? (
            <AlertOctagon className="h-5 w-5" />
          ) : (
            <AlertTriangle className="h-5 w-5" />
          )}
          Counter-Indicator Alert{flags.length > 1 ? 's' : ''}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className={cn(
          'text-sm',
          hasCritical ? 'text-red-700' : 'text-amber-700'
        )}>
          {hasCritical
            ? 'Critical indicators detected that may predict failure in this role. Review carefully before proceeding.'
            : 'Warning indicators detected that warrant additional consideration.'}
        </p>

        {/* Critical flags */}
        {criticalFlags.length > 0 && (
          <div className="space-y-2">
            {criticalFlags.map((flag, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-3 bg-red-100 rounded-lg border border-red-200"
              >
                <ShieldAlert className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className="font-semibold text-red-800">
                      {flag.trait_name}
                    </span>
                    <div className="flex items-center gap-2 text-sm">
                      <span className="text-red-600">
                        Score: {flag.actual_score}
                      </span>
                      <span className="text-red-500">/</span>
                      <span className="text-red-600">
                        Threshold: {flag.threshold}
                      </span>
                    </div>
                  </div>
                  <p className="text-sm text-red-700">{flag.reason}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Warning flags */}
        {warningFlags.length > 0 && (
          <div className="space-y-2">
            {warningFlags.map((flag, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-3 bg-amber-100 rounded-lg border border-amber-200"
              >
                <AlertTriangle className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className="font-semibold text-amber-800">
                      {flag.trait_name}
                    </span>
                    <div className="flex items-center gap-2 text-sm">
                      <span className="text-amber-600">
                        Score: {flag.actual_score}
                      </span>
                      <span className="text-amber-500">/</span>
                      <span className="text-amber-600">
                        Threshold: {flag.threshold}
                      </span>
                    </div>
                  </div>
                  <p className="text-sm text-amber-700">{flag.reason}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
