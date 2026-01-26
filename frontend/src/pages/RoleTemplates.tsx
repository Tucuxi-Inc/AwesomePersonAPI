import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '@/api/client';
import { RoleTemplatesByCategory, RoleProfile, Trait } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

export default function RoleTemplates() {
  const navigate = useNavigate();
  const [templateData, setTemplateData] = useState<RoleTemplatesByCategory | null>(null);
  const [traits, setTraits] = useState<Record<string, Trait>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<RoleProfile | null>(null);
  const [cloneDialogOpen, setCloneDialogOpen] = useState(false);
  const [cloneName, setCloneName] = useState('');
  const [cloneDescription, setCloneDescription] = useState('');
  const [cloning, setCloning] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [templatesRes, traitsRes] = await Promise.all([
        api.getRoleTemplates(),
        api.getTraits({ limit: 100 }),
      ]);

      setTemplateData(templatesRes.data);

      // Build trait lookup map
      const traitMap: Record<string, Trait> = {};
      for (const trait of traitsRes.data.items) {
        traitMap[trait.id] = trait;
      }
      setTraits(traitMap);
    } catch (err) {
      setError('Failed to load role templates');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleClone = async () => {
    if (!selectedTemplate || !cloneName.trim()) return;

    try {
      setCloning(true);
      const response = await api.cloneRoleProfile(selectedTemplate.id, {
        name: cloneName.trim(),
        description: cloneDescription.trim() || undefined,
      });
      setCloneDialogOpen(false);
      setCloneName('');
      setCloneDescription('');
      setSelectedTemplate(null);
      // Navigate to the new role profile
      navigate(`/roles/${response.data.id}`);
    } catch (err) {
      console.error('Failed to clone template:', err);
    } finally {
      setCloning(false);
    }
  };

  const openCloneDialog = (template: RoleProfile) => {
    setSelectedTemplate(template);
    setCloneName(`${template.name} (Copy)`);
    setCloneDescription(template.description || '');
    setCloneDialogOpen(true);
  };

  const getTraitName = (traitId: string): string => {
    return traits[traitId]?.name || 'Unknown Trait';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">{error}</p>
        <Button onClick={loadData} className="mt-4">
          Retry
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Role Templates</h1>
        <p className="text-muted-foreground mt-2">
          Browse pre-configured role templates with recommended traits. Clone a template to customize it for your organization.
        </p>
      </div>

      <div className="text-sm text-muted-foreground">
        {templateData?.total} templates across {templateData?.categories.length} categories
      </div>

      <Accordion type="multiple" defaultValue={templateData?.categories.map(c => c.name) || []}>
        {templateData?.categories.map((category) => (
          <AccordionItem key={category.name} value={category.name}>
            <AccordionTrigger className="text-lg font-semibold">
              {category.name}
              <Badge variant="secondary" className="ml-2">
                {category.templates.length}
              </Badge>
            </AccordionTrigger>
            <AccordionContent>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 pt-2">
                {category.templates.map((template) => (
                  <Card key={template.id} className="flex flex-col">
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div>
                          <CardTitle className="text-lg">{template.name}</CardTitle>
                          {template.level && (
                            <Badge variant="outline" className="mt-1">
                              {template.level}
                            </Badge>
                          )}
                        </div>
                      </div>
                      {template.description && (
                        <CardDescription className="mt-2 line-clamp-2">
                          {template.description}
                        </CardDescription>
                      )}
                    </CardHeader>
                    <CardContent className="flex-1 space-y-4">
                      {template.critical_traits.length > 0 && (
                        <div>
                          <h4 className="text-sm font-medium mb-2">Critical Traits</h4>
                          <div className="flex flex-wrap gap-1">
                            {template.critical_traits.map((req, idx) => (
                              <Badge key={idx} variant="destructive" className="text-xs">
                                {getTraitName(req.trait_id)}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}
                      {template.positive_traits.length > 0 && (
                        <div>
                          <h4 className="text-sm font-medium mb-2">Positive Traits</h4>
                          <div className="flex flex-wrap gap-1">
                            {template.positive_traits.slice(0, 4).map((req, idx) => (
                              <Badge key={idx} variant="secondary" className="text-xs">
                                {getTraitName(req.trait_id)}
                              </Badge>
                            ))}
                            {template.positive_traits.length > 4 && (
                              <Badge variant="outline" className="text-xs">
                                +{template.positive_traits.length - 4} more
                              </Badge>
                            )}
                          </div>
                        </div>
                      )}
                      {template.counter_indicators.length > 0 && (
                        <div>
                          <h4 className="text-sm font-medium mb-2">Counter-Indicators</h4>
                          <div className="flex flex-wrap gap-1">
                            {template.counter_indicators.map((ci, idx) => (
                              <Badge key={idx} variant="outline" className="text-xs border-orange-500 text-orange-600">
                                {getTraitName(ci.trait_id)} ({ci.threshold})
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}
                      <div className="pt-2">
                        <Button
                          onClick={() => openCloneDialog(template)}
                          variant="outline"
                          className="w-full"
                        >
                          Clone Template
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>

      {/* Clone Dialog */}
      <Dialog open={cloneDialogOpen} onOpenChange={setCloneDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Clone Role Template</DialogTitle>
            <DialogDescription>
              Create a copy of "{selectedTemplate?.name}" that you can customize for your organization.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="clone-name">Role Name</Label>
              <Input
                id="clone-name"
                value={cloneName}
                onChange={(e) => setCloneName(e.target.value)}
                placeholder="Enter a name for this role"
                autoComplete="off"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="clone-description">Description (optional)</Label>
              <Textarea
                id="clone-description"
                value={cloneDescription}
                onChange={(e) => setCloneDescription(e.target.value)}
                placeholder="Describe this role and how it differs from the template"
                rows={3}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setCloneDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleClone} disabled={!cloneName.trim() || cloning}>
              {cloning ? 'Cloning...' : 'Clone Template'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
