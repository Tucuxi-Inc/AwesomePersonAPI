import { useState, useEffect, useCallback } from 'react';
import { toast } from 'sonner';
import { api } from '@/api/client';
import { LLMSettings, LLMProvider } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Loader2,
  CheckCircle,
  AlertTriangle,
  Zap,
  Globe,
  Server,
  Cpu,
  Brain,
  Cloud,
  RefreshCw,
} from 'lucide-react';
import { cn } from '@/lib/utils';

// Provider icon mapping
const providerIcons: Record<string, React.ReactNode> = {
  anthropic: <Brain className="h-6 w-6" />,
  openai: <Zap className="h-6 w-6" />,
  google: <Globe className="h-6 w-6" />,
  groq: <Cpu className="h-6 w-6" />,
  openrouter: <Cloud className="h-6 w-6" />,
  ollama: <Server className="h-6 w-6" />,
};

interface LLMSettingsTabProps {
  organizationId: string;
}

export default function LLMSettingsTab({ organizationId }: LLMSettingsTabProps) {
  const [providers, setProviders] = useState<LLMProvider[]>([]);
  const [settings, setSettings] = useState<LLMSettings | null>(null);
  const [selectedProvider, setSelectedProvider] = useState<string>('anthropic');
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [modelsLoading, setModelsLoading] = useState(false);
  const [apiKey, setApiKey] = useState<string>('');
  const [baseUrl, setBaseUrl] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{
    success: boolean;
    message: string;
    preview?: string;
  } | null>(null);

  useEffect(() => {
    loadData();
  }, [organizationId]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [providersRes, settingsRes] = await Promise.all([
        api.getLLMProviders(),
        api.getLLMSettings(organizationId),
      ]);
      setProviders(providersRes.data);
      const s = settingsRes.data;
      setSettings(s);
      const provider = s.provider || 'anthropic';
      setSelectedProvider(provider);
      setSelectedModel(s.model || '');
      setBaseUrl(s.base_url || '');
      // Fetch models for the current provider
      fetchModels(provider);
    } catch (err) {
      console.error('Failed to load LLM settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchModels = useCallback(async (providerId: string, key?: string, url?: string) => {
    setModelsLoading(true);
    try {
      const response = await api.fetchLLMModels(providerId, key, url);
      const models: string[] = response.data || [];
      setAvailableModels(models);
      // Also update the provider in our local list
      setProviders((prev) =>
        prev.map((p) => (p.id === providerId ? { ...p, models } : p))
      );
    } catch {
      setAvailableModels([]);
    } finally {
      setModelsLoading(false);
    }
  }, []);

  const handleProviderSelect = (providerId: string) => {
    setSelectedProvider(providerId);
    setSelectedModel('');
    setApiKey('');
    setTestResult(null);
    setAvailableModels([]);
    const config = providers.find((p) => p.id === providerId);
    if (config?.default_base_url) {
      setBaseUrl(config.default_base_url);
    } else {
      setBaseUrl('');
    }
    // Fetch models for the new provider
    fetchModels(providerId);
  };

  const handleRefreshModels = () => {
    fetchModels(
      selectedProvider,
      apiKey || undefined,
      selectedProvider === 'ollama' ? baseUrl || undefined : undefined
    );
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const data: { provider: string; model: string; api_key?: string; base_url?: string } = {
        provider: selectedProvider,
        model: selectedModel || (availableModels[0] ?? ''),
      };
      if (apiKey) {
        data.api_key = apiKey;
      }
      if (selectedProvider === 'ollama' && baseUrl) {
        data.base_url = baseUrl;
      }
      const response = await api.updateLLMSettings(organizationId, data);
      setSettings(response.data);
      setApiKey('');
      toast.success('AI provider settings saved');
    } catch (err) {
      console.error('Failed to save LLM settings:', err);
      toast.error('Failed to save AI settings');
    } finally {
      setSaving(false);
    }
  };

  const handleTest = async () => {
    setTesting(true);
    setTestResult(null);
    try {
      const data: { provider: string; model: string; api_key?: string; base_url?: string } = {
        provider: selectedProvider,
        model: selectedModel || (availableModels[0] ?? ''),
      };
      if (apiKey) {
        data.api_key = apiKey;
      }
      if (selectedProvider === 'ollama' && baseUrl) {
        data.base_url = baseUrl;
      }
      const response = await api.testLLMSettings(organizationId, data);
      setTestResult({
        success: response.data.success,
        message: response.data.message,
        preview: response.data.response_preview,
      });
      if (response.data.success) {
        toast.success('Connection successful');
      } else {
        toast.error(response.data.message);
      }
    } catch (err) {
      console.error('LLM test failed:', err);
      toast.error('Connection test failed');
    } finally {
      setTesting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  const currentProviderConfig = providers.find((p) => p.id === selectedProvider);

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>AI Provider</CardTitle>
          <CardDescription>
            Select which AI provider to use for interviews and assessments.
            You can also set API keys via the <code className="text-xs bg-muted px-1 rounded">.env</code> file.
            Admin settings here take priority.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={(e) => { e.preventDefault(); handleSave(); }} className="space-y-6">
          {/* Provider Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {providers.map((provider) => (
              <button
                key={provider.id}
                type="button"
                onClick={() => handleProviderSelect(provider.id)}
                className={cn(
                  'flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-all cursor-pointer',
                  'hover:border-primary/50 hover:bg-accent/50',
                  selectedProvider === provider.id
                    ? 'border-primary bg-accent shadow-sm'
                    : 'border-border bg-card'
                )}
              >
                <div
                  className={cn(
                    'p-2 rounded-full',
                    selectedProvider === provider.id
                      ? 'bg-primary/10 text-primary'
                      : 'bg-muted text-muted-foreground'
                  )}
                >
                  {providerIcons[provider.id] || <Brain className="h-6 w-6" />}
                </div>
                <span
                  className={cn(
                    'text-sm font-medium',
                    selectedProvider === provider.id ? 'text-primary' : 'text-foreground'
                  )}
                >
                  {provider.name}
                </span>
                {!provider.requires_api_key && (
                  <span className="text-[10px] text-muted-foreground">No API key needed</span>
                )}
              </button>
            ))}
          </div>

          {/* Provider Configuration */}
          {currentProviderConfig && (
            <div className="space-y-4 pt-4 border-t">
              {/* API Key (shown first for cloud providers, hidden for Ollama) */}
              {currentProviderConfig.requires_api_key && (
                <div className="space-y-2">
                  <Label htmlFor="llm_api_key">API Key</Label>
                  <div className="flex gap-2">
                    <Input
                      id="llm_api_key"
                      type="password"
                      autoComplete="off"
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                      placeholder={
                        settings?.api_key_set && settings?.provider === selectedProvider
                          ? '••••••••'
                          : 'Enter API key'
                      }
                    />
                    <Button
                      type="button"
                      variant="outline"
                      size="icon"
                      onClick={handleRefreshModels}
                      disabled={modelsLoading}
                      title="Refresh model list"
                    >
                      <RefreshCw className={cn('h-4 w-4', modelsLoading && 'animate-spin')} />
                    </Button>
                  </div>
                  {settings?.api_key_set && settings?.provider === selectedProvider && (
                    <p className="text-xs text-muted-foreground">
                      API key is configured. Leave blank to keep existing. Click refresh to reload models.
                    </p>
                  )}
                </div>
              )}

              {/* Base URL (Ollama only) */}
              {selectedProvider === 'ollama' && (
                <div className="space-y-2">
                  <Label htmlFor="llm_base_url">Ollama Base URL</Label>
                  <div className="flex gap-2">
                    <Input
                      id="llm_base_url"
                      value={baseUrl}
                      onChange={(e) => setBaseUrl(e.target.value)}
                      placeholder="http://ollama:11434"
                    />
                    <Button
                      type="button"
                      variant="outline"
                      size="icon"
                      onClick={handleRefreshModels}
                      disabled={modelsLoading}
                      title="Refresh model list"
                    >
                      <RefreshCw className={cn('h-4 w-4', modelsLoading && 'animate-spin')} />
                    </Button>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Use <code className="bg-muted px-1 rounded">http://ollama:11434</code> for Docker,
                    or <code className="bg-muted px-1 rounded">http://localhost:11434</code> for host-installed Ollama.
                  </p>
                </div>
              )}

              {/* Model Selection */}
              <div className="space-y-2">
                <Label htmlFor="llm_model">
                  Model
                  {modelsLoading && <Loader2 className="inline h-3 w-3 ml-2 animate-spin" />}
                </Label>
                {availableModels.length > 0 ? (
                  <Select
                    value={selectedModel || undefined}
                    onValueChange={setSelectedModel}
                  >
                    <SelectTrigger id="llm_model">
                      <SelectValue placeholder="Select a model" />
                    </SelectTrigger>
                    <SelectContent>
                      {availableModels.map((model) => (
                        <SelectItem key={model} value={model}>
                          {model}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                ) : modelsLoading ? (
                  <div className="flex items-center gap-2 text-sm text-muted-foreground p-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Loading models...
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Input
                      id="llm_model_manual"
                      value={selectedModel}
                      onChange={(e) => setSelectedModel(e.target.value)}
                      placeholder="Enter model name (e.g., gpt-4o)"
                    />
                    <p className="text-xs text-muted-foreground">
                      {currentProviderConfig.requires_api_key
                        ? 'Enter an API key and click refresh to load available models, or type a model name.'
                        : 'No models found. Click refresh to reload, or type a model name.'}
                    </p>
                  </div>
                )}
              </div>

              {/* Source indicator */}
              {settings && (
                <div
                  className={cn(
                    'flex items-center gap-2 text-sm p-3 rounded-md',
                    settings.source === 'database'
                      ? 'bg-green-50 text-green-700'
                      : settings.source === 'env'
                        ? 'bg-blue-50 text-blue-700'
                        : 'bg-gray-50 text-gray-600'
                  )}
                >
                  {settings.source === 'database' ? (
                    <>
                      <CheckCircle className="h-4 w-4" />
                      Configured via admin settings
                      {settings.configured_at && (
                        <span className="text-muted-foreground">
                          (updated {new Date(settings.configured_at).toLocaleDateString()})
                        </span>
                      )}
                    </>
                  ) : settings.source === 'env' ? (
                    <>
                      <CheckCircle className="h-4 w-4" />
                      Using .env file configuration
                    </>
                  ) : (
                    <>
                      <AlertTriangle className="h-4 w-4" />
                      Using default settings — configure an API key to get started
                    </>
                  )}
                </div>
              )}

              {/* Test Result */}
              {testResult && (
                <div
                  className={cn(
                    'p-3 rounded-md text-sm',
                    testResult.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'
                  )}
                >
                  <div className="flex items-center gap-2 font-medium">
                    {testResult.success ? (
                      <CheckCircle className="h-4 w-4" />
                    ) : (
                      <AlertTriangle className="h-4 w-4" />
                    )}
                    {testResult.message}
                  </div>
                  {testResult.preview && (
                    <p className="mt-1 text-xs opacity-75 font-mono">
                      Response: {testResult.preview}
                    </p>
                  )}
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex gap-3">
                <Button type="submit" disabled={saving}>
                  {saving ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    'Save Settings'
                  )}
                </Button>
                <Button type="button" variant="outline" onClick={handleTest} disabled={testing}>
                  {testing ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Testing...
                    </>
                  ) : (
                    'Test Connection'
                  )}
                </Button>
              </div>
            </div>
          )}
          </form>
        </CardContent>
      </Card>
    </>
  );
}
