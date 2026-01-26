import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { StrengthItem, DevelopmentArea } from '@/types';
import { TrendingUp, TrendingDown, Star, Target } from 'lucide-react';

interface StrengthsAndAreasProps {
  strengths: StrengthItem[];
  developmentAreas: DevelopmentArea[];
  className?: string;
}

export function StrengthsAndAreas({
  strengths,
  developmentAreas,
  className,
}: StrengthsAndAreasProps) {
  return (
    <div className={cn('grid grid-cols-1 md:grid-cols-2 gap-6', className)}>
      {/* Strengths Card */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-lg">
            <TrendingUp className="h-5 w-5 text-green-600" />
            Key Strengths
          </CardTitle>
        </CardHeader>
        <CardContent>
          {strengths.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-4">
              No key strengths identified
            </p>
          ) : (
            <div className="space-y-3">
              {strengths.map((strength, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-3 bg-green-50 rounded-lg border border-green-100"
                >
                  <div className="flex-shrink-0 p-1.5 bg-green-100 rounded-full">
                    <Star className="h-4 w-4 text-green-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <span className="font-medium text-green-800">
                        {strength.trait_name}
                      </span>
                      <span className="text-sm font-semibold text-green-700 bg-green-100 px-2 py-0.5 rounded">
                        {strength.score}/5
                      </span>
                    </div>
                    <p className="text-sm text-green-700">{strength.evidence}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Development Areas Card */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-lg">
            <TrendingDown className="h-5 w-5 text-amber-600" />
            Development Areas
          </CardTitle>
        </CardHeader>
        <CardContent>
          {developmentAreas.length === 0 ? (
            <p className="text-sm text-muted-foreground text-center py-4">
              No development areas identified
            </p>
          ) : (
            <div className="space-y-3">
              {developmentAreas.map((area, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-3 bg-amber-50 rounded-lg border border-amber-100"
                >
                  <div className="flex-shrink-0 p-1.5 bg-amber-100 rounded-full">
                    <Target className="h-4 w-4 text-amber-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <span className="font-medium text-amber-800">
                        {area.trait_name}
                      </span>
                      <span className="text-sm font-semibold text-amber-700 bg-amber-100 px-2 py-0.5 rounded">
                        {area.score}/5
                      </span>
                    </div>
                    <p className="text-sm text-amber-700">{area.recommendation}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
