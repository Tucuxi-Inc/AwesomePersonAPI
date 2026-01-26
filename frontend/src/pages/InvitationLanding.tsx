import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '@/api/client';
import {
  InvitationValidateResponse,
  DisclosureResponse,
  SelfServiceSessionResponse,
} from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { ScrollArea } from '@/components/ui/scroll-area';
import { AlertCircle, CheckCircle, Clock, Building2 } from 'lucide-react';

type PageState = 'loading' | 'invalid' | 'disclosure' | 'ready' | 'session' | 'complete';

export default function InvitationLanding() {
  const { token } = useParams<{ token: string }>();

  const [pageState, setPageState] = useState<PageState>('loading');
  const [error, setError] = useState<string | null>(null);
  const [invitation, setInvitation] = useState<InvitationValidateResponse | null>(null);
  const [disclosure, setDisclosure] = useState<DisclosureResponse | null>(null);
  const [consentGiven, setConsentGiven] = useState(false);
  const [session, setSession] = useState<SelfServiceSessionResponse | null>(null);
  const [responseText, setResponseText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (token) {
      validateToken();
    }
  }, [token]);

  const validateToken = async () => {
    if (!token) return;

    try {
      const response = await api.validateInvitation(token);
      const data = response.data as InvitationValidateResponse;

      if (!data.valid) {
        setError(data.error || 'Invalid invitation');
        setPageState('invalid');
        return;
      }

      setInvitation(data);

      // For candidate interviews, show disclosure first
      if (data.invitation_type === 'CANDIDATE_INTERVIEW') {
        const disclosureResponse = await api.getInvitationDisclosure(token);
        setDisclosure(disclosureResponse.data);
        setPageState('disclosure');
      } else {
        // For top performer profiling, go straight to ready
        setPageState('ready');
      }
    } catch (err) {
      setError('Failed to validate invitation');
      setPageState('invalid');
    }
  };

  const handleAcceptDisclosure = async () => {
    if (!token || !consentGiven) return;

    try {
      setSubmitting(true);
      const response = await api.startSelfServiceSession(token, true);
      setSession(response.data);
      setPageState('session');
    } catch (err) {
      setError('Failed to start session');
    } finally {
      setSubmitting(false);
    }
  };

  const handleStartProfiling = async () => {
    if (!token) return;

    try {
      setSubmitting(true);
      const response = await api.startSelfServiceSession(token, false);
      setSession(response.data);
      setPageState('session');
    } catch (err) {
      setError('Failed to start session');
    } finally {
      setSubmitting(false);
    }
  };

  const handleSubmitResponse = async () => {
    if (!token || !session || !responseText.trim()) return;

    try {
      setSubmitting(true);
      const response = await api.submitSelfServiceResponse(
        token,
        session.session_id,
        responseText.trim()
      );
      const newSession = response.data as SelfServiceSessionResponse;
      setSession(newSession);
      setResponseText('');

      if (newSession.is_complete) {
        setPageState('complete');
      }
    } catch (err) {
      setError('Failed to submit response');
    } finally {
      setSubmitting(false);
    }
  };

  const handleEndSession = async () => {
    if (!token) return;

    try {
      await api.endSelfServiceSession(token);
      setPageState('complete');
    } catch (err) {
      console.error('Failed to end session:', err);
    }
  };

  // Loading state
  if (pageState === 'loading') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Validating your invitation...</p>
        </div>
      </div>
    );
  }

  // Invalid invitation
  if (pageState === 'invalid') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 rounded-full bg-red-100 flex items-center justify-center mb-4">
              <AlertCircle className="w-6 h-6 text-red-600" />
            </div>
            <CardTitle>Invalid Invitation</CardTitle>
            <CardDescription>{error}</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <p className="text-sm text-muted-foreground mb-4">
              This link may have expired or been revoked. Please contact the person who sent you
              this invitation for a new link.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Disclosure view (for candidates)
  if (pageState === 'disclosure' && disclosure) {
    return (
      <div className="min-h-screen bg-background py-8 px-4">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                <Building2 className="w-4 h-4" />
                {invitation?.organization_name}
              </div>
              <CardTitle>{disclosure.title}</CardTitle>
              {invitation?.recipient_name && (
                <CardDescription>
                  Hello {invitation.recipient_name}, please review the following information before
                  proceeding with your assessment.
                </CardDescription>
              )}
            </CardHeader>
            <CardContent className="space-y-6">
              <ScrollArea className="h-[400px] rounded-md border p-4">
                {disclosure.sections.map((section, index) => (
                  <div key={index} className="mb-6 last:mb-0">
                    <h3 className="font-semibold text-lg mb-2">{section.heading}</h3>
                    <p className="text-muted-foreground whitespace-pre-line">{section.content}</p>
                  </div>
                ))}
              </ScrollArea>

              {disclosure.consent_required && (
                <div className="flex items-start space-x-3 p-4 border rounded-lg bg-muted/50">
                  <Checkbox
                    id="consent"
                    checked={consentGiven}
                    onCheckedChange={(checked) => setConsentGiven(checked as boolean)}
                  />
                  <div className="grid gap-1.5 leading-none">
                    <Label htmlFor="consent" className="cursor-pointer">
                      {disclosure.consent_text ||
                        'I acknowledge that I have read and understand this notice.'}
                    </Label>
                  </div>
                </div>
              )}

              <div className="flex justify-end gap-3">
                <Button
                  onClick={handleAcceptDisclosure}
                  disabled={disclosure.consent_required && !consentGiven}
                >
                  {submitting ? 'Starting...' : 'Continue to Assessment'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // Ready to start (for top performers)
  if (pageState === 'ready') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <CheckCircle className="w-6 h-6 text-primary" />
            </div>
            <CardTitle>Welcome{invitation?.recipient_name ? `, ${invitation.recipient_name}` : ''}!</CardTitle>
            <CardDescription>
              {invitation?.organization_name} has invited you to participate in a
              {invitation?.invitation_type === 'TOP_PERFORMER_PROFILING'
                ? ' profile development session'
                : ' candidate assessment'}.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {invitation?.custom_message && (
              <div className="p-4 bg-muted rounded-lg">
                <p className="text-sm italic">"{invitation.custom_message}"</p>
              </div>
            )}

            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Clock className="w-4 h-4" />
              <span>This session typically takes 15-30 minutes</span>
            </div>

            <Button onClick={handleStartProfiling} className="w-full" disabled={submitting}>
              {submitting ? 'Starting...' : 'Begin Session'}
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Active session
  if (pageState === 'session' && session) {
    return (
      <div className="min-h-screen bg-background py-8 px-4">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>
                    {session.session_type === 'interview' ? 'Assessment' : 'Profile Session'}
                  </CardTitle>
                  {session.trait_name && (
                    <CardDescription>Exploring: {session.trait_name}</CardDescription>
                  )}
                </div>
                <div className="text-sm text-muted-foreground">
                  Progress: {Math.round(session.overall_progress * 100)}%
                </div>
              </div>
              {/* Progress bar */}
              <div className="w-full bg-muted rounded-full h-2 mt-2">
                <div
                  className="bg-primary h-2 rounded-full transition-all"
                  style={{ width: `${session.overall_progress * 100}%` }}
                />
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="p-4 bg-muted rounded-lg">
                <p className="whitespace-pre-line">{session.next_prompt}</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="response">Your Response</Label>
                <textarea
                  id="response"
                  className="flex min-h-[200px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Type your response here..."
                  value={responseText}
                  onChange={(e) => setResponseText(e.target.value)}
                  disabled={submitting}
                />
                <div className="text-xs text-muted-foreground text-right">
                  {responseText.length} characters
                </div>
              </div>

              {error && (
                <div className="p-3 bg-red-50 text-red-600 rounded-lg text-sm">{error}</div>
              )}

              <div className="flex justify-between">
                <Button variant="outline" onClick={handleEndSession} disabled={submitting}>
                  End Session Early
                </Button>
                <Button
                  onClick={handleSubmitResponse}
                  disabled={!responseText.trim() || submitting}
                >
                  {submitting ? 'Submitting...' : 'Submit Response'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // Complete
  if (pageState === 'complete') {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <CardTitle>Session Complete</CardTitle>
            <CardDescription>Thank you for your time and participation!</CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <p className="text-sm text-muted-foreground">
              {session?.session_type === 'interview'
                ? 'Your assessment has been submitted. The hiring team will review your responses and be in touch soon.'
                : 'Your input has been recorded. This information will help improve our hiring practices.'}
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return null;
}
