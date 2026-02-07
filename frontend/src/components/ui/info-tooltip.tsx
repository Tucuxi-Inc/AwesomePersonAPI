import { Info } from 'lucide-react';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';

interface InfoTooltipProps {
  content: string;
  className?: string;
  iconClassName?: string;
  side?: 'top' | 'right' | 'bottom' | 'left';
  maxWidth?: string;
}

export function InfoTooltip({
  content,
  className,
  iconClassName,
  side = 'top',
  maxWidth = '280px',
}: InfoTooltipProps) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <span
          className={cn(
            'inline-flex items-center justify-center cursor-help',
            className
          )}
        >
          <Info
            className={cn('h-4 w-4 text-muted-foreground hover:text-foreground transition-colors', iconClassName)}
          />
        </span>
      </TooltipTrigger>
      <TooltipContent side={side} style={{ maxWidth }}>
        <p className="text-sm">{content}</p>
      </TooltipContent>
    </Tooltip>
  );
}
