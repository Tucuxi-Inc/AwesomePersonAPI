import { useRef, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { InterviewExchange, ProbeType } from '@/types';
import { Bot, User, Clock } from 'lucide-react';

interface TranscriptPanelProps {
  exchanges: InterviewExchange[];
  className?: string;
}

const probeTypeLabels: Record<ProbeType, string> = {
  INTRODUCTION: 'Introduction',
  PRIMARY: 'Primary',
  FOLLOW_UP: 'Follow-up',
  RECURSION: 'Additional Example',
  REFLECTION: 'Reflection',
  CONFLICT: 'Challenge',
  CLOSING: 'Closing',
  COMPLETE: 'Complete',
};

export function TranscriptPanel({ exchanges, className }: TranscriptPanelProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new exchanges are added
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [exchanges.length]);

  if (exchanges.length === 0) {
    return (
      <Card className={className}>
        <CardHeader className="pb-3">
          <CardTitle className="text-base font-medium">Transcript</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-muted-foreground text-center py-8">
            Interview transcript will appear here as you progress.
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <CardTitle className="text-base font-medium flex items-center justify-between">
          <span>Transcript</span>
          <span className="text-sm font-normal text-muted-foreground">
            {exchanges.length} exchange{exchanges.length !== 1 ? 's' : ''}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div
          ref={scrollRef}
          className="space-y-4 max-h-[400px] overflow-y-auto pr-2"
        >
          {exchanges.map((exchange, index) => (
            <div key={index} className="space-y-3">
              {/* Interviewer question */}
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                  <Bot className="h-4 w-4 text-primary" />
                </div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span className="font-medium text-foreground">Interviewer</span>
                    <span className="px-1.5 py-0.5 rounded bg-muted text-xs">
                      {probeTypeLabels[exchange.prompt_type] || exchange.prompt_type}
                    </span>
                    <Clock className="h-3 w-3 ml-auto" />
                    <span>{formatTime(exchange.timestamp)}</span>
                  </div>
                  <div className="text-sm bg-muted/50 rounded-lg p-3">
                    {exchange.prompt}
                  </div>
                </div>
              </div>

              {/* Candidate response */}
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
                  <User className="h-4 w-4 text-green-700" />
                </div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span className="font-medium text-foreground">Candidate</span>
                  </div>
                  <div className="text-sm bg-green-50 rounded-lg p-3 border border-green-100">
                    {exchange.response}
                  </div>
                </div>
              </div>

              {/* Divider between exchanges */}
              {index < exchanges.length - 1 && (
                <div className="border-t border-dashed my-4" />
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function formatTime(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
