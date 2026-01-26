import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { api } from '@/api/client';
import { useInterview } from '@/hooks/useInterview';
import { Candidate, Trait, ScoringRubric } from '@/types';
import {
  ArrowLeft,
  Play,
  User,
  Briefcase,
  Mail,
  Brain,
  FileText,
  Settings,
  Clock,
  CheckCircle2,
  AlertTriangle,
  Loader2,
} from 'lucide-react';

export default function StartInterview() {
  const { candidateId } = useParams<{ candidateId: string }>();
  const navigate = useNavigate();

  const { startInterview, isLoading: isStarting, error: startError } = useInterview();

  // Data loading state
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [candidate, setCandidate] = useState<Candidate | null>(null);
  const [traits, setTraits] = useState<Trait[]>([]);
  const [rubrics, setRubrics] = useState<ScoringRubric[]>([]);

  // Selection state
  const [selectedTraitIds, setSelectedTraitIds] = useState<string[]>([]);
  const [selectedRubricId, setSelectedRubricId] = useState<string | null>(null);

  // Configuration state
  const [config, setConfig] = useState({
    max_duration_minutes: 60,
    max_follow_ups_per_trait: 3,
    enable_resume_customization: true,
    enable_conflict_probing: true,
    require_reflection: true,
  });

  // Fetch data on mount
  useEffect(() => {
    const fetchData = async () => {
      if (!candidateId) {
        setError('No candidate ID provided');
        setIsLoading(false);
        return;
      }

      try {
        // Fetch candidate, traits, and rubrics in parallel
        const [candidateRes, traitsRes, rubricsRes] = await Promise.all([
          api.getCandidate(candidateId),
          api.getTraits({ limit: 100 }),
          api.getDefaultRubrics(),
        ]);

        setCandidate(candidateRes.data);
        setTraits(traitsRes.data.items || traitsRes.data);
        setRubrics(rubricsRes.data.items || rubricsRes.data || []);

        // Pre-select first 6 traits by default
        const defaultTraits = (traitsRes.data.items || traitsRes.data).slice(0, 6);
        setSelectedTraitIds(defaultTraits.map((t: Trait) => t.id));
      } catch (err: unknown) {
        const error = err as { response?: { data?: { detail?: string } } };
        setError(error.response?.data?.detail || 'Failed to load data');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [candidateId]);

  // Toggle trait selection
  const toggleTrait = (traitId: string) => {
    setSelectedTraitIds((prev) =>
      prev.includes(traitId)
        ? prev.filter((id) => id !== traitId)
        : [...prev, traitId]
    );
  };

  // Handle start interview
  const handleStart = async () => {
    if (!candidate || selectedTraitIds.length === 0) return;

    await startInterview(
      {
        candidate_id: candidate.id,
        trait_ids: selectedTraitIds,
        rubric_id: selectedRubricId || undefined,
        config,
      },
      candidate
    );
  };

  // Group traits by category
  const traitsByCategory = traits.reduce((acc, trait) => {
    const category = trait.category || 'Other';
    if (!acc[category]) acc[category] = [];
    acc[category].push(trait);
    return acc;
  }, {} as Record<string, Trait[]>);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-4">
          <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto" />
          <p className="text-muted-foreground">Loading interview setup...</p>
        </div>
      </div>
    );
  }

  if (error || !candidate) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Card className="w-full max-w-md">
          <CardContent className="p-6 text-center">
            <AlertTriangle className="h-12 w-12 text-amber-500 mx-auto mb-4" />
            <h2 className="text-lg font-semibold mb-2">Unable to Load</h2>
            <p className="text-muted-foreground mb-4">
              {error || 'Candidate data could not be loaded.'}
            </p>
            <Button onClick={() => navigate('/candidates')}>
              Return to Candidates
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Button
          variant="ghost"
          size="sm"
          className="mb-2"
          onClick={() => navigate('/candidates')}
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Candidates
        </Button>
        <h1 className="text-2xl font-bold tracking-tight">Start Interview</h1>
        <p className="text-muted-foreground">Configure and begin a STAR+ behavioral interview</p>
      </div>

      {/* Error display */}
      {startError && (
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4 text-destructive">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            <span>{startError}</span>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column - Candidate info and config */}
        <div className="space-y-6">
          {/* Candidate info */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Candidate
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <div className="font-semibold text-lg">{candidate.full_name}</div>
                {candidate.current_title && (
                  <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                    <Briefcase className="h-4 w-4" />
                    {candidate.current_title}
                    {candidate.current_company && ` at ${candidate.current_company}`}
                  </div>
                )}
              </div>
              <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
                <Mail className="h-4 w-4" />
                {candidate.email}
              </div>
              {candidate.years_experience && (
                <div className="text-sm text-muted-foreground">
                  {candidate.years_experience} years experience
                </div>
              )}
              <div className="pt-2 border-t">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  candidate.status === 'NEW' ? 'bg-blue-100 text-blue-800' :
                  candidate.status === 'SCREENING' ? 'bg-purple-100 text-purple-800' :
                  candidate.status === 'INTERVIEWING' ? 'bg-amber-100 text-amber-800' :
                  candidate.status === 'ASSESSED' ? 'bg-green-100 text-green-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {candidate.status}
                </span>
              </div>
            </CardContent>
          </Card>

          {/* Interview configuration */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                Configuration
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label className="flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  Max Duration (minutes)
                </Label>
                <Input
                  type="number"
                  min={10}
                  max={120}
                  value={config.max_duration_minutes}
                  onChange={(e) => setConfig({ ...config, max_duration_minutes: parseInt(e.target.value) || 60 })}
                />
              </div>

              <div className="space-y-2">
                <Label>Max Follow-ups per Trait</Label>
                <Input
                  type="number"
                  min={1}
                  max={5}
                  value={config.max_follow_ups_per_trait}
                  onChange={(e) => setConfig({ ...config, max_follow_ups_per_trait: parseInt(e.target.value) || 3 })}
                />
              </div>

              <div className="space-y-3 pt-2 border-t">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={config.enable_resume_customization}
                    onChange={(e) => setConfig({ ...config, enable_resume_customization: e.target.checked })}
                    className="w-4 h-4 rounded border-input"
                  />
                  <span className="text-sm">Use resume for question customization</span>
                </label>

                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={config.enable_conflict_probing}
                    onChange={(e) => setConfig({ ...config, enable_conflict_probing: e.target.checked })}
                    className="w-4 h-4 rounded border-input"
                  />
                  <span className="text-sm">Enable conflict scenario probing</span>
                </label>

                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={config.require_reflection}
                    onChange={(e) => setConfig({ ...config, require_reflection: e.target.checked })}
                    className="w-4 h-4 rounded border-input"
                  />
                  <span className="text-sm">Require reflection questions</span>
                </label>
              </div>
            </CardContent>
          </Card>

          {/* Start button */}
          <Button
            className="w-full"
            size="lg"
            onClick={handleStart}
            disabled={selectedTraitIds.length === 0 || isStarting}
          >
            {isStarting ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Starting Interview...
              </>
            ) : (
              <>
                <Play className="mr-2 h-5 w-5" />
                Start Interview
              </>
            )}
          </Button>

          <p className="text-xs text-muted-foreground text-center">
            {selectedTraitIds.length} trait{selectedTraitIds.length !== 1 ? 's' : ''} selected
          </p>
        </div>

        {/* Right column - Trait selection */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5" />
                Select Traits to Assess
              </CardTitle>
              <CardDescription>
                Choose which traits to evaluate during this interview. We recommend 4-8 traits for a comprehensive assessment.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {Object.entries(traitsByCategory).map(([category, categoryTraits]) => (
                  <div key={category}>
                    <h3 className="font-medium text-sm text-muted-foreground mb-3 uppercase tracking-wide">
                      {category}
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {categoryTraits.map((trait) => {
                        const isSelected = selectedTraitIds.includes(trait.id);
                        return (
                          <button
                            key={trait.id}
                            onClick={() => toggleTrait(trait.id)}
                            className={`flex items-center gap-3 p-3 rounded-lg border text-left transition-colors ${
                              isSelected
                                ? 'bg-primary/5 border-primary ring-1 ring-primary'
                                : 'hover:bg-muted/50 border-border'
                            }`}
                          >
                            <div className={`flex-shrink-0 w-5 h-5 rounded border flex items-center justify-center ${
                              isSelected ? 'bg-primary border-primary' : 'border-input'
                            }`}>
                              {isSelected && <CheckCircle2 className="h-4 w-4 text-primary-foreground" />}
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="font-medium truncate">{trait.name}</div>
                              <div className="text-xs text-muted-foreground truncate">
                                {trait.definition?.substring(0, 60)}...
                              </div>
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>

              {/* Selection actions */}
              <div className="flex items-center gap-2 mt-6 pt-4 border-t">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSelectedTraitIds(traits.slice(0, 6).map(t => t.id))}
                >
                  Select First 6
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSelectedTraitIds(traits.map(t => t.id))}
                >
                  Select All
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSelectedTraitIds([])}
                >
                  Clear All
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Rubric selection (if available) */}
          {rubrics.length > 0 && (
            <Card className="mt-6">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Scoring Rubric (Optional)
                </CardTitle>
                <CardDescription>
                  Select a custom rubric or use the default behavioral anchors
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <button
                    onClick={() => setSelectedRubricId(null)}
                    className={`w-full flex items-center gap-3 p-3 rounded-lg border text-left transition-colors ${
                      selectedRubricId === null
                        ? 'bg-primary/5 border-primary ring-1 ring-primary'
                        : 'hover:bg-muted/50 border-border'
                    }`}
                  >
                    <div className={`flex-shrink-0 w-4 h-4 rounded-full border ${
                      selectedRubricId === null ? 'bg-primary border-primary' : 'border-input'
                    }`} />
                    <span className="font-medium">Use Default Rubrics</span>
                  </button>
                  {rubrics.map((rubric) => (
                    <button
                      key={rubric.id}
                      onClick={() => setSelectedRubricId(rubric.id)}
                      className={`w-full flex items-center gap-3 p-3 rounded-lg border text-left transition-colors ${
                        selectedRubricId === rubric.id
                          ? 'bg-primary/5 border-primary ring-1 ring-primary'
                          : 'hover:bg-muted/50 border-border'
                      }`}
                    >
                      <div className={`flex-shrink-0 w-4 h-4 rounded-full border ${
                        selectedRubricId === rubric.id ? 'bg-primary border-primary' : 'border-input'
                      }`} />
                      <div>
                        <div className="font-medium">{rubric.name}</div>
                        {rubric.description && (
                          <div className="text-xs text-muted-foreground">{rubric.description}</div>
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
