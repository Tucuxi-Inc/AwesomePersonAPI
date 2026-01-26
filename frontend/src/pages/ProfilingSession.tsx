import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '@/api/client';
import { ProfilingPromptResponse, ProfilingCompleteResponse } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { Send, Loader2, StopCircle, CheckCircle, MessageSquare, Brain } from 'lucide-react';

interface TranscriptEntry {
  role: 'system' | 'performer';
  content: string;
  timestamp: string;
  trait?: string | null;
}

export default function ProfilingSession() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();

  const [currentPrompt, setCurrentPrompt] = useState<ProfilingPromptResponse | null>(null);
  const [transcript, setTranscript] = useState<TranscriptEntry[]>([]);
  const [response, setResponse] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [showEndConfirm, setShowEndConfirm] = useState(false);
  const [endingSession, setEndingSession] = useState(false);
  const [sessionComplete, setSessionComplete] = useState(false);
  const [completionResult, setCompletionResult] = useState<ProfilingCompleteResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // The session was already started, get initial prompt from localStorage or fetch
    const storedPrompt = localStorage.getItem(`profiling_${sessionId}`);
    if (storedPrompt) {
      const prompt = JSON.parse(storedPrompt) as ProfilingPromptResponse;
      setCurrentPrompt(prompt);
      setTranscript([{
        role: 'system',
        content: prompt.prompt_text,
        timestamp: new Date().toISOString(),
        trait: prompt.trait_being_explored,
      }]);
      localStorage.removeItem(`profiling_${sessionId}`);
    }
  }, [sessionId]);

  useEffect(() => {
    // Scroll to bottom when transcript updates
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [transcript]);

  const handleSubmit = async () => {
    if (!response.trim() || submitting || !sessionId) return;

    setSubmitting(true);
    setError(null);

    const performerResponse = response.trim();
    setResponse('');

    // Add performer response to transcript immediately
    setTranscript(prev => [...prev, {
      role: 'performer',
      content: performerResponse,
      timestamp: new Date().toISOString(),
    }]);

    try {
      const result = await api.submitProfilingResponse(sessionId, {
        response_text: performerResponse,
      });

      const promptResponse = result.data as ProfilingPromptResponse;
      setCurrentPrompt(promptResponse);

      if (promptResponse.is_complete) {
        setSessionComplete(true);
        // Fetch completion result
        const endResult = await api.endProfilingSession(sessionId);
        setCompletionResult(endResult.data as ProfilingCompleteResponse);
      } else {
        // Add system response to transcript
        setTranscript(prev => [...prev, {
          role: 'system',
          content: promptResponse.prompt_text,
          timestamp: new Date().toISOString(),
          trait: promptResponse.trait_being_explored,
        }]);
      }
    } catch (err) {
      console.error('Failed to submit response:', err);
      setError('Failed to submit response. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleEndSession = async () => {
    if (!sessionId) return;

    setEndingSession(true);
    try {
      const result = await api.endProfilingSession(sessionId);
      setCompletionResult(result.data as ProfilingCompleteResponse);
      setSessionComplete(true);
    } catch (err) {
      console.error('Failed to end session:', err);
      setError('Failed to end session. Please try again.');
    } finally {
      setEndingSession(false);
      setShowEndConfirm(false);
    }
  };

  const progress = currentPrompt?.progress
    ? Math.round((currentPrompt.progress.current_trait_index / currentPrompt.progress.total_traits) * 100)
    : 0;

  if (sessionComplete && completionResult) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <Card className="border-green-200 bg-green-50">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3 mb-4">
              <CheckCircle className="h-8 w-8 text-green-600" />
              <div>
                <h2 className="text-xl font-bold text-green-800">Profiling Complete</h2>
                <p className="text-green-600">Session ended successfully</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Session Summary</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-muted-foreground">{completionResult.summary}</p>

            <div className="grid grid-cols-3 gap-4">
              <div className="text-center p-4 bg-muted rounded-lg">
                <div className="text-2xl font-bold">{completionResult.signals_extracted}</div>
                <div className="text-sm text-muted-foreground">Signals Extracted</div>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <div className="text-2xl font-bold">{completionResult.patterns_identified}</div>
                <div className="text-sm text-muted-foreground">Patterns Identified</div>
              </div>
              <div className="text-center p-4 bg-muted rounded-lg">
                <div className="text-2xl font-bold">{completionResult.counter_indicators_found}</div>
                <div className="text-sm text-muted-foreground">Counter-Indicators</div>
              </div>
            </div>

            <div>
              <h4 className="font-medium mb-2">Traits Profiled</h4>
              <div className="flex flex-wrap gap-2">
                {completionResult.traits_profiled.map((trait) => (
                  <Badge key={trait} variant="secondary">{trait}</Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="flex justify-center gap-4">
          <Button variant="outline" onClick={() => navigate('/profiling')}>
            Back to Top Performers
          </Button>
          <Button onClick={() => navigate(`/profiling/performers/${sessionId}`)}>
            View Full Results
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-xl font-bold">Profiling Session</h1>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            {currentPrompt?.trait_being_explored && (
              <>
                <Brain className="h-4 w-4" />
                <span>Exploring: {currentPrompt.trait_being_explored}</span>
              </>
            )}
            <Badge variant="outline">{currentPrompt?.phase || 'Starting...'}</Badge>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-sm font-medium">
              {currentPrompt?.progress?.current_trait_index || 0} / {currentPrompt?.progress?.total_traits || 0} Traits
            </div>
            <Progress value={progress} className="w-32" />
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowEndConfirm(true)}
          >
            <StopCircle className="h-4 w-4 mr-2" />
            End Session
          </Button>
        </div>
      </div>

      {/* Transcript */}
      <Card className="flex-1 flex flex-col overflow-hidden">
        <CardHeader className="py-3 border-b">
          <CardTitle className="text-sm flex items-center gap-2">
            <MessageSquare className="h-4 w-4" />
            Conversation
          </CardTitle>
        </CardHeader>
        <ScrollArea className="flex-1 p-4" ref={scrollRef}>
          <div className="space-y-4">
            {transcript.map((entry, index) => (
              <div
                key={index}
                className={`flex ${entry.role === 'system' ? 'justify-start' : 'justify-end'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    entry.role === 'system'
                      ? 'bg-muted'
                      : 'bg-primary text-primary-foreground'
                  }`}
                >
                  {entry.role === 'system' && entry.trait && (
                    <Badge variant="outline" className="mb-2 text-xs">
                      {entry.trait}
                    </Badge>
                  )}
                  <p className="whitespace-pre-wrap">{entry.content}</p>
                </div>
              </div>
            ))}
            {submitting && (
              <div className="flex justify-start">
                <div className="bg-muted rounded-lg p-4">
                  <Loader2 className="h-5 w-5 animate-spin" />
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
      </Card>

      {/* Input */}
      <Card className="mt-4">
        <CardContent className="p-4">
          {error && (
            <div className="mb-4 p-3 text-sm text-destructive bg-destructive/10 rounded-md">
              {error}
            </div>
          )}
          <div className="flex gap-3">
            <Textarea
              value={response}
              onChange={(e) => setResponse(e.target.value)}
              placeholder="Enter the top performer's response..."
              className="min-h-[80px] resize-none"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && e.ctrlKey) {
                  handleSubmit();
                }
              }}
            />
            <Button
              onClick={handleSubmit}
              disabled={!response.trim() || submitting}
              className="self-end"
            >
              {submitting ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
          <p className="text-xs text-muted-foreground mt-2">
            Press Ctrl+Enter to submit
          </p>
        </CardContent>
      </Card>

      {/* End Session Confirmation */}
      <AlertDialog open={showEndConfirm} onOpenChange={setShowEndConfirm}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>End Profiling Session?</AlertDialogTitle>
            <AlertDialogDescription>
              This will end the current profiling session and extract traits from the conversation.
              Any unsaved progress will be processed.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Continue Session</AlertDialogCancel>
            <AlertDialogAction onClick={handleEndSession} disabled={endingSession}>
              {endingSession ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
              End Session
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
