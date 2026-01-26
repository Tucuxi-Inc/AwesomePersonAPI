import { useEffect, useState } from 'react';
import { api } from '@/api/client';
import { Trait } from '@/types';
import { useAuth } from '@/hooks/useAuth';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Plus, Edit, Trash2, Loader2, AlertTriangle } from 'lucide-react';

interface TraitCategory {
  name: string;
  traits: Trait[];
}

const categoryLabels: Record<string, string> = {
  COGNITIVE: 'Cognitive Traits',
  INTERPERSONAL: 'Interpersonal Traits',
  EXECUTION: 'Execution Traits',
  STABILITY: 'Stability Traits',
  SELF_MANAGEMENT: 'Self-Management Traits',
  ORIENTATION: 'Orientation Traits',
};

const CATEGORIES = [
  'COGNITIVE',
  'INTERPERSONAL',
  'EXECUTION',
  'STABILITY',
  'SELF_MANAGEMENT',
  'ORIENTATION',
];

export function Traits() {
  const { user } = useAuth();
  const [categories, setCategories] = useState<TraitCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTrait, setSelectedTrait] = useState<Trait | null>(null);

  // Dialog states
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [dialogLoading, setDialogLoading] = useState(false);
  const [dialogError, setDialogError] = useState<string | null>(null);

  // Form state for create/edit
  const [formName, setFormName] = useState('');
  const [formCategory, setFormCategory] = useState('COGNITIVE');
  const [formDefinition, setFormDefinition] = useState('');
  const [formSpectrumLow, setFormSpectrumLow] = useState('');
  const [formSpectrumHigh, setFormSpectrumHigh] = useState('');
  const [formMarkersLow, setFormMarkersLow] = useState('');
  const [formMarkersHigh, setFormMarkersHigh] = useState('');
  const [formCounterIndicators, setFormCounterIndicators] = useState('');

  const isAdmin = user?.role === 'ADMIN' || user?.is_superuser;

  const fetchTraits = async () => {
    try {
      setLoading(true);
      const response = await api.getTraitCategories();
      setCategories(response.data);
    } catch (error) {
      console.error('Failed to fetch traits:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTraits();
  }, []);

  // Reset form
  const resetForm = () => {
    setFormName('');
    setFormCategory('COGNITIVE');
    setFormDefinition('');
    setFormSpectrumLow('');
    setFormSpectrumHigh('');
    setFormMarkersLow('');
    setFormMarkersHigh('');
    setFormCounterIndicators('');
    setDialogError(null);
  };

  // Open create dialog
  const handleOpenCreateDialog = () => {
    resetForm();
    setCreateDialogOpen(true);
  };

  // Open edit dialog
  const handleOpenEditDialog = (trait: Trait) => {
    setSelectedTrait(trait);
    setFormName(trait.name);
    setFormCategory(trait.category);
    setFormDefinition(trait.definition);
    setFormSpectrumLow(trait.spectrum_low_label);
    setFormSpectrumHigh(trait.spectrum_high_label);
    setFormMarkersLow(trait.behavioral_markers_low.join('\n'));
    setFormMarkersHigh(trait.behavioral_markers_high.join('\n'));
    setFormCounterIndicators(trait.counter_indicator_for.join('\n'));
    setDialogError(null);
    setEditDialogOpen(true);
  };

  // Open delete dialog
  const handleOpenDeleteDialog = (trait: Trait) => {
    setSelectedTrait(trait);
    setDeleteDialogOpen(true);
  };

  // Create trait
  const handleCreate = async () => {
    if (!formName.trim() || !formDefinition.trim()) {
      setDialogError('Name and definition are required');
      return;
    }

    setDialogLoading(true);
    setDialogError(null);

    try {
      await api.createTrait({
        name: formName.trim(),
        category: formCategory,
        definition: formDefinition.trim(),
        spectrum_low_label: formSpectrumLow.trim() || 'Low',
        spectrum_high_label: formSpectrumHigh.trim() || 'High',
        behavioral_markers_low: formMarkersLow.split('\n').map(s => s.trim()).filter(Boolean),
        behavioral_markers_high: formMarkersHigh.split('\n').map(s => s.trim()).filter(Boolean),
        counter_indicator_for: formCounterIndicators.split('\n').map(s => s.trim()).filter(Boolean),
      });
      setCreateDialogOpen(false);
      fetchTraits();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setDialogError(error.response?.data?.detail || 'Failed to create trait');
    } finally {
      setDialogLoading(false);
    }
  };

  // Update trait
  const handleUpdate = async () => {
    if (!selectedTrait || !formName.trim() || !formDefinition.trim()) {
      setDialogError('Name and definition are required');
      return;
    }

    setDialogLoading(true);
    setDialogError(null);

    try {
      const updatedTrait = await api.updateTrait(selectedTrait.id, {
        name: formName.trim(),
        category: formCategory,
        definition: formDefinition.trim(),
        spectrum_low_label: formSpectrumLow.trim() || 'Low',
        spectrum_high_label: formSpectrumHigh.trim() || 'High',
        behavioral_markers_low: formMarkersLow.split('\n').map(s => s.trim()).filter(Boolean),
        behavioral_markers_high: formMarkersHigh.split('\n').map(s => s.trim()).filter(Boolean),
        counter_indicator_for: formCounterIndicators.split('\n').map(s => s.trim()).filter(Boolean),
      });
      setEditDialogOpen(false);
      setSelectedTrait(updatedTrait.data);
      fetchTraits();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setDialogError(error.response?.data?.detail || 'Failed to update trait');
    } finally {
      setDialogLoading(false);
    }
  };

  // Delete trait
  const handleDelete = async () => {
    if (!selectedTrait) return;

    setDialogLoading(true);
    try {
      await api.deleteTrait(selectedTrait.id);
      setDeleteDialogOpen(false);
      setSelectedTrait(null);
      fetchTraits();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      alert(error.response?.data?.detail || 'Failed to delete trait');
    } finally {
      setDialogLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold">Trait Taxonomy</h1>
          <p className="text-muted-foreground mt-1">
            {categories.reduce((sum, cat) => sum + cat.traits.length, 0)} traits organized into {categories.length} categories with role-context valence mappings.
          </p>
        </div>
        {isAdmin && (
          <Button onClick={handleOpenCreateDialog}>
            <Plus className="mr-2 h-4 w-4" />
            Add Trait
          </Button>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Trait list by category */}
        <div className="space-y-6">
          {categories.map((category) => (
            <Card key={category.name}>
              <CardHeader>
                <CardTitle>{categoryLabels[category.name] || category.name}</CardTitle>
                <CardDescription>{category.traits.length} traits</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {category.traits.map((trait) => (
                    <div
                      key={trait.id}
                      className={`flex items-center justify-between px-3 py-2 rounded-md text-sm transition-colors cursor-pointer ${
                        selectedTrait?.id === trait.id
                          ? 'bg-primary text-primary-foreground'
                          : 'hover:bg-accent'
                      }`}
                      onClick={() => setSelectedTrait(trait)}
                    >
                      <span>{trait.name}</span>
                      {isAdmin && (
                        <div className="flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 w-6 p-0"
                            onClick={() => handleOpenEditDialog(trait)}
                          >
                            <Edit className="h-3 w-3" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 w-6 p-0 text-destructive hover:text-destructive"
                            onClick={() => handleOpenDeleteDialog(trait)}
                          >
                            <Trash2 className="h-3 w-3" />
                          </Button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Trait detail */}
        <div className="lg:sticky lg:top-8">
          {selectedTrait ? (
            <Card>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle>{selectedTrait.name}</CardTitle>
                    <CardDescription>{selectedTrait.category}</CardDescription>
                  </div>
                  {isAdmin && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleOpenEditDialog(selectedTrait)}
                    >
                      <Edit className="h-4 w-4 mr-1" />
                      Edit
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="font-medium mb-1">Definition</h4>
                  <p className="text-sm text-muted-foreground">{selectedTrait.definition}</p>
                </div>

                <div>
                  <h4 className="font-medium mb-2">Spectrum</h4>
                  <div className="flex items-center text-sm">
                    <span className="text-muted-foreground">{selectedTrait.spectrum_low_label}</span>
                    <div className="flex-1 mx-4 h-2 bg-muted rounded-full">
                      <div className="h-full w-1/2 bg-primary rounded-full"></div>
                    </div>
                    <span className="text-muted-foreground">{selectedTrait.spectrum_high_label}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium mb-2">Low Markers</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      {selectedTrait.behavioral_markers_low.map((marker, i) => (
                        <li key={i}>• {marker}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">High Markers</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      {selectedTrait.behavioral_markers_high.map((marker, i) => (
                        <li key={i}>• {marker}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {selectedTrait.counter_indicator_for.length > 0 && (
                  <div>
                    <h4 className="font-medium mb-2 text-destructive">Counter-Indicator For</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      {selectedTrait.counter_indicator_for.map((role, i) => (
                        <li key={i}>• {role}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="flex items-center justify-center h-64 text-muted-foreground">
                Select a trait to view details
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      {/* Create Dialog */}
      <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Create New Trait</DialogTitle>
            <DialogDescription>
              Add a new trait to the taxonomy.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="create-name">Name *</Label>
                <Input
                  id="create-name"
                  value={formName}
                  onChange={(e) => setFormName(e.target.value)}
                  placeholder="e.g., Resilience"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="create-category">Category</Label>
                <Select value={formCategory} onValueChange={setFormCategory}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {CATEGORIES.map((cat) => (
                      <SelectItem key={cat} value={cat}>
                        {categoryLabels[cat] || cat}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="create-definition">Definition *</Label>
              <Textarea
                id="create-definition"
                value={formDefinition}
                onChange={(e) => setFormDefinition(e.target.value)}
                placeholder="Define the trait..."
                rows={3}
              />
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="create-low">Spectrum Low Label</Label>
                <Input
                  id="create-low"
                  value={formSpectrumLow}
                  onChange={(e) => setFormSpectrumLow(e.target.value)}
                  placeholder="e.g., Brittle"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="create-high">Spectrum High Label</Label>
                <Input
                  id="create-high"
                  value={formSpectrumHigh}
                  onChange={(e) => setFormSpectrumHigh(e.target.value)}
                  placeholder="e.g., Resilient"
                />
              </div>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="create-markers-low">Low Markers (one per line)</Label>
                <Textarea
                  id="create-markers-low"
                  value={formMarkersLow}
                  onChange={(e) => setFormMarkersLow(e.target.value)}
                  placeholder="Enter behavioral markers..."
                  rows={4}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="create-markers-high">High Markers (one per line)</Label>
                <Textarea
                  id="create-markers-high"
                  value={formMarkersHigh}
                  onChange={(e) => setFormMarkersHigh(e.target.value)}
                  placeholder="Enter behavioral markers..."
                  rows={4}
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="create-counter">Counter-Indicator For (one per line)</Label>
              <Textarea
                id="create-counter"
                value={formCounterIndicators}
                onChange={(e) => setFormCounterIndicators(e.target.value)}
                placeholder="Enter role categories where high trait is negative..."
                rows={2}
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
                'Create Trait'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Edit Trait</DialogTitle>
            <DialogDescription>
              Update the trait details.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="edit-name">Name *</Label>
                <Input
                  id="edit-name"
                  value={formName}
                  onChange={(e) => setFormName(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-category">Category</Label>
                <Select value={formCategory} onValueChange={setFormCategory}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {CATEGORIES.map((cat) => (
                      <SelectItem key={cat} value={cat}>
                        {categoryLabels[cat] || cat}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-definition">Definition *</Label>
              <Textarea
                id="edit-definition"
                value={formDefinition}
                onChange={(e) => setFormDefinition(e.target.value)}
                rows={3}
              />
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="edit-low">Spectrum Low Label</Label>
                <Input
                  id="edit-low"
                  value={formSpectrumLow}
                  onChange={(e) => setFormSpectrumLow(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-high">Spectrum High Label</Label>
                <Input
                  id="edit-high"
                  value={formSpectrumHigh}
                  onChange={(e) => setFormSpectrumHigh(e.target.value)}
                />
              </div>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="edit-markers-low">Low Markers (one per line)</Label>
                <Textarea
                  id="edit-markers-low"
                  value={formMarkersLow}
                  onChange={(e) => setFormMarkersLow(e.target.value)}
                  rows={4}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-markers-high">High Markers (one per line)</Label>
                <Textarea
                  id="edit-markers-high"
                  value={formMarkersHigh}
                  onChange={(e) => setFormMarkersHigh(e.target.value)}
                  rows={4}
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-counter">Counter-Indicator For (one per line)</Label>
              <Textarea
                id="edit-counter"
                value={formCounterIndicators}
                onChange={(e) => setFormCounterIndicators(e.target.value)}
                rows={2}
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

      {/* Delete Dialog */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Trait</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{selectedTrait?.name}"? This action cannot be undone.
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
                  Delete Trait
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
