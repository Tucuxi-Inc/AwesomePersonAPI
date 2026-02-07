import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Send, Loader2 } from 'lucide-react';

interface ResponseInputProps {
  onSubmit: (response: string) => void;
  isSubmitting?: boolean;
  isDisabled?: boolean;
  minLength?: number;
  maxLength?: number;
  placeholder?: string;
}

export function ResponseInput({
  onSubmit,
  isSubmitting = false,
  isDisabled = false,
  minLength = 50,
  maxLength = 10000,
  placeholder = "Share your experience here. Be specific about the situation, your actions, and the results...",
}: ResponseInputProps) {
  const [response, setResponse] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const charCount = response.length;
  const isValid = charCount >= minLength && charCount <= maxLength;
  const canSubmit = isValid && !isSubmitting && !isDisabled;

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 400)}px`;
    }
  }, [response]);

  // Focus textarea on mount
  useEffect(() => {
    if (textareaRef.current && !isDisabled) {
      textareaRef.current.focus();
    }
  }, [isDisabled]);

  const handleSubmit = () => {
    if (canSubmit) {
      onSubmit(response);
      setResponse('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Submit on Ctrl/Cmd + Enter
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && canSubmit) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <Card>
      <CardContent className="p-4 pb-2">
        <textarea
          ref={textareaRef}
          value={response}
          onChange={(e) => setResponse(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={isSubmitting || isDisabled}
          className="w-full min-h-[150px] p-3 text-base resize-none border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          maxLength={maxLength}
        />
      </CardContent>
      <CardFooter className="flex items-center justify-between px-4 py-3 border-t bg-muted/30">
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span className={charCount < minLength ? 'text-amber-600' : charCount > maxLength ? 'text-destructive' : ''}>
            {charCount.toLocaleString()} / {maxLength.toLocaleString()} characters
          </span>
          {charCount < minLength && (
            <span className="text-amber-600">
              (minimum {minLength} characters)
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground hidden sm:inline">
            Press {navigator.platform.includes('Mac') ? '⌘' : 'Ctrl'}+Enter to submit
          </span>
          <Button
            onClick={handleSubmit}
            disabled={!canSubmit}
            size="default"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" />
                Submit Response
              </>
            )}
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}
