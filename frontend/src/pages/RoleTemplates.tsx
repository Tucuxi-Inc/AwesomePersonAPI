import { useState, useEffect } from 'react';
import { api } from '@/api/client';
import { RoleTemplatesByCategory, RoleProfile, Trait } from '@/types';
import { useAuth } from '@/hooks/useAuth';
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Plus, Edit, Trash2, Copy, Loader2, AlertTriangle } from 'lucide-react';

const ROLE_CATEGORIES = [
  'Engineering',
  'Product',
  'Sales',
  'Customer Success',
  'Data & Analytics',
  'Marketing',
  'Operations',
  'Human Resources',
  'Finance',
  'Design',
  'Executive',
  'Other',
];

export default function RoleTemplates() {
  const { user } = useAuth();
  const [templateData, setTemplateData] = useState<RoleTemplatesByCategory | null>(null);
  const [traitMap, setTraitMap] = useState<Record<string, Trait>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<RoleProfile | null>(null);

  // Dialog states
  const [cloneDialogOpen, setCloneDialogOpen] = useState(false);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [dialogLoading, setDialogLoading] = useState(false);
  const [dialogError, setDialogError] = useState<string | null>(null);

  // Form state
  const [formName, setFormName] = useState('');
  const [formDescription, setFormDescription] = useState('');
  const [formCategory, setFormCategory] = useState('Engineering');

  const isAdmin = user?.role === 'ADMIN' || user?.is_superuser;

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
      const map: Record<string, Trait> = {};
      for (const trait of traitsRes.data.items) {
        map[trait.id] = trait;
      }
      setTraitMap(map);
    } catch (err) {
      setError('Failed to load role templates');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormName('');
    setFormDescription('');
    setFormCategory('Engineering');
    setDialogError(null);
  };

  // Open create dialog
  const handleOpenCreateDialog = () => {
    resetForm();
    setCreateDialogOpen(true);
  };

  // Open edit dialog
  const handleOpenEditDialog = (profile: RoleProfile) => {
    setSelectedTemplate(profile);
    setFormName(profile.name);
    setFormDescription(profile.description || '');
    setFormCategory(profile.role_category);
    setDialogError(null);
    setEditDialogOpen(true);
  };

  // Open clone dialog
  const openCloneDialog = (template: RoleProfile) => {
    setSelectedTemplate(template);
    setFormName(`${template.name} (Copy)`);
    setFormDescription(template.description || '');
    setCloneDialogOpen(true);
  };

  // Open delete dialog
  const handleOpenDeleteDialog = (profile: RoleProfile) => {
    setSelectedTemplate(profile);
    setDeleteDialogOpen(true);
  };

  // Create role profile
  const handleCreate = async () => {
    if (!formName.trim()) {
      setDialogError('Name is required');
      return;
    }

    setDialogLoading(true);
    setDialogError(null);

    try {
      await api.createRoleProfile({
        name: formName.trim(),
        description: formDescription.trim() || undefined,
        role_category: formCategory,
      });
      setCreateDialogOpen(false);
      loadData();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setDialogError(error.response?.data?.detail || 'Failed to create role profile');
    } finally {
      setDialogLoading(false);
    }
  };

  // Update role profile
  const handleUpdate = async () => {
    if (!selectedTemplate || !formName.trim()) {
      setDialogError('Name is required');
      return;
    }

    setDialogLoading(true);
    setDialogError(null);

    try {
      await api.updateRoleProfile(selectedTemplate.id, {
        name: formName.trim(),
        description: formDescription.trim() || undefined,
      });
      setEditDialogOpen(false);
      loadData();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setDialogError(error.response?.data?.detail || 'Failed to update role profile');
    } finally {
      setDialogLoading(false);
    }
  };

  // Clone role profile
  const handleClone = async () => {
    if (!selectedTemplate || !formName.trim()) return;

    setDialogLoading(true);
    try {
      await api.cloneRoleProfile(selectedTemplate.id, {
        name: formName.trim(),
        description: formDescription.trim() || undefined,
      });
      setCloneDialogOpen(false);
      setFormName('');
      setFormDescription('');
      setSelectedTemplate(null);
      loadData();
    } catch (err) {
      console.error('Failed to clone template:', err);
    } finally {
      setDialogLoading(false);
    }
  };

  // Delete role profile
  const handleDelete = async () => {
    if (!selectedTemplate) return;

    setDialogLoading(true);
    try {
      await api.deleteRoleProfile(selectedTemplate.id);
      setDeleteDialogOpen(false);
      setSelectedTemplate(null);
      loadData();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      alert(error.response?.data?.detail || 'Failed to delete role profile');
    } finally {
      setDialogLoading(false);
    }
  };

  const getTraitName = (traitId: string): string => {
    return traitMap[traitId]?.name || 'Unknown Trait';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="h-12 w-12 text-destructive mx-auto mb-4" />
        <p className="text-destructive">{error}</p>
        <Button onClick={loadData} className="mt-4">
          Retry
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Role Templates</h1>
          <p className="text-muted-foreground mt-2">
            Browse pre-configured role templates with recommended traits. Clone a template to customize it for your organization.
          </p>
        </div>
        {isAdmin && (
          <Button onClick={handleOpenCreateDialog}>
            <Plus className="mr-2 h-4 w-4" />
            Create Role
          </Button>
        )}
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
                          <div className="flex items-center gap-2 mt-1">
                            {template.level && (
                              <Badge variant="outline">
                                {template.level}
                              </Badge>
                            )}
                            {template.is_template && (
                              <Badge variant="secondary" className="text-xs">
                                Template
                              </Badge>
                            )}
                          </div>
                        </div>
                        {isAdmin && !template.is_template && (
                          <div className="flex items-center gap-1">
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-8 w-8 p-0"
                              onClick={() => handleOpenEditDialog(template)}
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-8 w-8 p-0 text-destructive hover:text-destructive"
                              onClick={() => handleOpenDeleteDialog(template)}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        )}
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
                      <div className="pt-2 flex gap-2">
                        <Button
                          onClick={() => openCloneDialog(template)}
                          variant="outline"
                          className="flex-1"
                        >
                          <Copy className="h-4 w-4 mr-1" />
                          Clone
                        </Button>
                        {isAdmin && !template.is_template && (
                          <Button
                            onClick={() => handleOpenEditDialog(template)}
                            variant="outline"
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>

      {/* Create Dialog */}
      <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Create Role Profile</DialogTitle>
            <DialogDescription>
              Create a new role profile for your organization.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="create-name">Role Name *</Label>
              <Input
                id="create-name"
                value={formName}
                onChange={(e) => setFormName(e.target.value)}
                placeholder="e.g., Senior Software Engineer"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="create-category">Category</Label>
              <Select value={formCategory} onValueChange={setFormCategory}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {ROLE_CATEGORIES.map((cat) => (
                    <SelectItem key={cat} value={cat}>
                      {cat}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="create-description">Description</Label>
              <Textarea
                id="create-description"
                value={formDescription}
                onChange={(e) => setFormDescription(e.target.value)}
                placeholder="Describe this role..."
                rows={3}
              />
            </div>
            {dialogError && (
              <div className="flex items-center gap-2 text-sm text-destructive">
                <AlertTriangle className="h-4 w-4" />
                {dialogError}
              </div>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setCreateDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreate} disabled={dialogLoading}>
              {dialogLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                'Create Role'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Edit Role Profile</DialogTitle>
            <DialogDescription>
              Update the role profile details.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="edit-name">Role Name *</Label>
              <Input
                id="edit-name"
                value={formName}
                onChange={(e) => setFormName(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-description">Description</Label>
              <Textarea
                id="edit-description"
                value={formDescription}
                onChange={(e) => setFormDescription(e.target.value)}
                rows={3}
              />
            </div>
            {dialogError && (
              <div className="flex items-center gap-2 text-sm text-destructive">
                <AlertTriangle className="h-4 w-4" />
                {dialogError}
              </div>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleUpdate} disabled={dialogLoading}>
              {dialogLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Saving...
                </>
              ) : (
                'Save Changes'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

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
                value={formName}
                onChange={(e) => setFormName(e.target.value)}
                placeholder="Enter a name for this role"
                autoComplete="off"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="clone-description">Description (optional)</Label>
              <Textarea
                id="clone-description"
                value={formDescription}
                onChange={(e) => setFormDescription(e.target.value)}
                placeholder="Describe this role and how it differs from the template"
                rows={3}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setCloneDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleClone} disabled={!formName.trim() || dialogLoading}>
              {dialogLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Cloning...
                </>
              ) : (
                'Clone Template'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Dialog */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Role Profile</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{selectedTemplate?.name}"? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteDialogOpen(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleDelete} disabled={dialogLoading}>
              {dialogLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Deleting...
                </>
              ) : (
                <>
                  <Trash2 className="h-4 w-4 mr-2" />
                  Delete Role
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
