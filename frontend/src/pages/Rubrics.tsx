import { useState, useEffect, useCallback } from 'react';
import { api } from '@/api/client';
import { ScoringRubric, Trait, BehavioralAnchor } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
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
import {
  FileText,
  Search,
  Copy,
  Edit,
  Trash2,
  Loader2,
  AlertTriangle,
  CheckCircle,
  Star,
  ChevronDown,
  ChevronUp,
  Filter,
} from 'lucide-react';

export default function Rubrics() {
  // Data state
  const [rubrics, setRubrics] = useState<ScoringRubric[]>([]);
  const [traits, setTraits] = useState<Trait[]>([]);
  const [selectedRubric, setSelectedRubric] = useState<ScoringRubric | null>(null);

  // UI state
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterDefaultsOnly, setFilterDefaultsOnly] = useState(false);
  const [filterTraitId, setFilterTraitId] = useState<string>('');

  // Dialog state
  const [cloneDialogOpen, setCloneDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [dialogLoading, setDialogLoading] = useState(false);

  // Form state
  const [cloneName, setCloneName] = useState('');
  const [cloneDescription, setCloneDescription] = useState('');
  const [editName, setEditName] = useState('');
  const [editDescription, setEditDescription] = useState('');

  // Expanded anchors
  const [expandedAnchors, setExpandedAnchors] = useState<Record<string, boolean>>({});

  // Fetch rubrics
  const fetchRubrics = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await api.getRubrics({
        defaults_only: filterDefaultsOnly,
        trait_id: filterTraitId || undefined,
      });
      setRubrics(response.data.items || []);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setError(error.response?.data?.detail || 'Failed to load rubrics');
    } finally {
      setIsLoading(false);
    }
  }, [filterDefaultsOnly, filterTraitId]);

  // Fetch traits for filtering
  useEffect(() => {
    const fetchTraits = async () => {
      try {
        const response = await api.getTraits({ limit: 100 });
        setTraits(response.data.items || []);
      } catch (err) {
        console.error('Failed to fetch traits:', err);
      }
    };
    fetchTraits();
  }, []);

  useEffect(() => {
    fetchRubrics();
  }, [fetchRubrics]);

  // Get trait name by ID
  const getTraitName = (traitId: string) => {
    const trait = traits.find(t => t.id === traitId);
    return trait?.name || 'Unknown Trait';
  };

  // Filter rubrics by search
  const filteredRubrics = rubrics.filter(rubric => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return (
      rubric.name.toLowerCase().includes(query) ||
      getTraitName(rubric.trait_id).toLowerCase().includes(query) ||
      rubric.description?.toLowerCase().includes(query)
    );
  });

  // Handle clone
  const handleOpenCloneDialog = (rubric: ScoringRubric) => {
    setSelectedRubric(rubric);
    setCloneName(`${rubric.name} (Copy)`);
    setCloneDescription(rubric.description || '');
    setCloneDialogOpen(true);
  };

  const handleClone = async () => {
    if (!selectedRubric || !cloneName.trim()) return;

    setDialogLoading(true);
    try {
      await api.cloneRubric(selectedRubric.id, {
        name: cloneName.trim(),
        description: cloneDescription.trim() || undefined,
      });
      setCloneDialogOpen(false);
      fetchRubrics();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      alert(error.response?.data?.detail || 'Failed to clone rubric');
    } finally {
      setDialogLoading(false);
    }
  };

  // Handle edit
  const handleOpenEditDialog = (rubric: ScoringRubric) => {
    setSelectedRubric(rubric);
    setEditName(rubric.name);
    setEditDescription(rubric.description || '');
    setEditDialogOpen(true);
  };

  const handleEdit = async () => {
    if (!selectedRubric || !editName.trim()) return;

    setDialogLoading(true);
    try {
      await api.updateRubric(selectedRubric.id, {
        name: editName.trim(),
        description: editDescription.trim() || undefined,
      });
      setEditDialogOpen(false);
      fetchRubrics();
      // Update selected rubric if it's the one being edited
      if (selectedRubric) {
        setSelectedRubric({
          ...selectedRubric,
          name: editName.trim(),
          description: editDescription.trim(),
        });
      }
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      alert(error.response?.data?.detail || 'Failed to update rubric');
    } finally {
      setDialogLoading(false);
    }
  };

  // Handle delete
  const handleOpenDeleteDialog = (rubric: ScoringRubric) => {
    setSelectedRubric(rubric);
    setDeleteDialogOpen(true);
  };

  const handleDelete = async () => {
    if (!selectedRubric) return;

    setDialogLoading(true);
    try {
      await api.deleteRubric(selectedRubric.id);
      setDeleteDialogOpen(false);
      setSelectedRubric(null);
      fetchRubrics();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      alert(error.response?.data?.detail || 'Failed to delete rubric');
    } finally {
      setDialogLoading(false);
    }
  };

  // Toggle anchor expansion
  const toggleAnchor = (score: string) => {
    setExpandedAnchors(prev => ({
      ...prev,
      [score]: !prev[score],
    }));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Scoring Rubrics</h1>
          <p className="text-muted-foreground">
            Behavioral assessment criteria with anchors and probes
          </p>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="py-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search rubrics..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4 text-muted-foreground" />
              <Select
                value={filterTraitId}
                onValueChange={(value) => setFilterTraitId(value === 'all' ? '' : value)}
              >
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="All Traits" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Traits</SelectItem>
                  {traits.map((trait) => (
                    <SelectItem key={trait.id} value={trait.id}>
                      {trait.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button
                variant={filterDefaultsOnly ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilterDefaultsOnly(!filterDefaultsOnly)}
              >
                <Star className="h-4 w-4 mr-1" />
                Defaults Only
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Error state */}
      {error && (
        <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4 text-destructive">
          <div className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Loading state */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      )}

      {/* Main content */}
      {!isLoading && (
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Rubric list */}
          <div className="space-y-4">
            {filteredRubrics.length === 0 ? (
              <Card>
                <CardContent className="py-12 text-center">
                  <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No Rubrics Found</h3>
                  <p className="text-muted-foreground">
                    {searchQuery || filterTraitId
                      ? 'Try adjusting your search or filters.'
                      : 'No rubrics available.'}
                  </p>
                </CardContent>
              </Card>
            ) : (
              filteredRubrics.map((rubric) => (
                <Card
                  key={rubric.id}
                  className={`cursor-pointer transition-all hover:shadow-md ${
                    selectedRubric?.id === rubric.id ? 'ring-2 ring-primary' : ''
                  }`}
                  onClick={() => setSelectedRubric(rubric)}
                >
                  <CardHeader className="pb-2">
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <CardTitle className="text-base truncate">{rubric.name}</CardTitle>
                          {rubric.is_default && (
                            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                              <Star className="h-3 w-3 mr-1" />
                              Default
                            </span>
                          )}
                        </div>
                        <CardDescription className="mt-1">
                          {getTraitName(rubric.trait_id)}
                        </CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0">
                    {rubric.description && (
                      <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
                        {rubric.description}
                      </p>
                    )}
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-muted-foreground">
                        Version {rubric.version}
                      </span>
                      <div className="flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleOpenCloneDialog(rubric)}
                          title="Clone rubric"
                        >
                          <Copy className="h-4 w-4" />
                        </Button>
                        {!rubric.is_default && (
                          <>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleOpenEditDialog(rubric)}
                              title="Edit rubric"
                            >
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleOpenDeleteDialog(rubric)}
                              title="Delete rubric"
                              className="text-destructive hover:text-destructive"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>

          {/* Rubric detail */}
          <div className="lg:sticky lg:top-8">
            {selectedRubric ? (
              <Card>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle>{selectedRubric.name}</CardTitle>
                      <CardDescription className="mt-1">
                        {getTraitName(selectedRubric.trait_id)} | Version {selectedRubric.version}
                      </CardDescription>
                    </div>
                    {selectedRubric.is_default && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                        <Star className="h-3 w-3 mr-1" />
                        Default
                      </span>
                    )}
                  </div>
                  {selectedRubric.description && (
                    <p className="text-sm text-muted-foreground mt-2">
                      {selectedRubric.description}
                    </p>
                  )}
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* Behavioral Anchors */}
                  <div>
                    <h4 className="font-medium mb-3">Behavioral Anchors</h4>
                    <div className="space-y-2">
                      {Object.entries(selectedRubric.behavioral_anchors)
                        .sort(([a], [b]) => Number(b) - Number(a))
                        .map(([score, anchor]) => {
                          const anchorData = anchor as BehavioralAnchor;
                          const isExpanded = expandedAnchors[score];
                          return (
                            <div
                              key={score}
                              className="border rounded-lg overflow-hidden"
                            >
                              <button
                                className="w-full flex items-center justify-between p-3 hover:bg-accent text-left"
                                onClick={() => toggleAnchor(score)}
                              >
                                <div className="flex items-center gap-3">
                                  <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                                    Number(score) >= 4 ? 'bg-green-100 text-green-800' :
                                    Number(score) >= 3 ? 'bg-blue-100 text-blue-800' :
                                    Number(score) >= 2 ? 'bg-amber-100 text-amber-800' :
                                    'bg-red-100 text-red-800'
                                  }`}>
                                    {score}
                                  </span>
                                  <span className="font-medium">{anchorData.label}</span>
                                </div>
                                {isExpanded ? (
                                  <ChevronUp className="h-4 w-4 text-muted-foreground" />
                                ) : (
                                  <ChevronDown className="h-4 w-4 text-muted-foreground" />
                                )}
                              </button>
                              {isExpanded && (
                                <div className="px-3 pb-3 space-y-3 border-t bg-muted/30">
                                  <p className="text-sm text-muted-foreground pt-3">
                                    {anchorData.description}
                                  </p>
                                  {anchorData.indicators && anchorData.indicators.length > 0 && (
                                    <div>
                                      <p className="text-xs font-medium mb-1">Indicators:</p>
                                      <ul className="text-sm text-muted-foreground space-y-1">
                                        {anchorData.indicators.map((indicator, i) => (
                                          <li key={i} className="flex items-start gap-2">
                                            <CheckCircle className="h-3 w-3 mt-1 text-green-600 flex-shrink-0" />
                                            {indicator}
                                          </li>
                                        ))}
                                      </ul>
                                    </div>
                                  )}
                                </div>
                              )}
                            </div>
                          );
                        })}
                    </div>
                  </div>

                  {/* Primary Probes */}
                  {selectedRubric.primary_probes && selectedRubric.primary_probes.length > 0 && (
                    <div>
                      <h4 className="font-medium mb-3">Primary Probes</h4>
                      <div className="space-y-2">
                        {selectedRubric.primary_probes.map((probe, i) => (
                          <div key={i} className="p-3 bg-muted rounded-lg">
                            <p className="text-sm font-medium">{probe.question}</p>
                            <div className="flex items-center gap-2 mt-1 text-xs text-muted-foreground">
                              <span className="px-1.5 py-0.5 bg-background rounded">
                                {probe.star_focus}
                              </span>
                              <span>{probe.purpose}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Derivation info */}
                  {selectedRubric.derived_from && (
                    <div className="text-xs text-muted-foreground border-t pt-4">
                      <p>
                        <strong>Derived from:</strong> {selectedRubric.derivation_notes}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardContent className="flex items-center justify-center h-64 text-muted-foreground">
                  Select a rubric to view details
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      )}

      {/* Clone Dialog */}
      <Dialog open={cloneDialogOpen} onOpenChange={setCloneDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Clone Rubric</DialogTitle>
            <DialogDescription>
              Create a copy of this rubric that you can customize for your organization.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="clone-name">Name</Label>
              <Input
                id="clone-name"
                value={cloneName}
                onChange={(e) => setCloneName(e.target.value)}
                placeholder="Enter rubric name"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="clone-description">Description (optional)</Label>
              <Textarea
                id="clone-description"
                value={cloneDescription}
                onChange={(e) => setCloneDescription(e.target.value)}
                placeholder="Enter description"
                rows={3}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setCloneDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleClone} disabled={dialogLoading || !cloneName.trim()}>
              {dialogLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Cloning...
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4 mr-2" />
                  Clone Rubric
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Rubric</DialogTitle>
            <DialogDescription>
              Update the rubric name and description.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="edit-name">Name</Label>
              <Input
                id="edit-name"
                value={editName}
                onChange={(e) => setEditName(e.target.value)}
                placeholder="Enter rubric name"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="edit-description">Description (optional)</Label>
              <Textarea
                id="edit-description"
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                placeholder="Enter description"
                rows={3}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setEditDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleEdit} disabled={dialogLoading || !editName.trim()}>
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
            <DialogTitle>Delete Rubric</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{selectedRubric?.name}"? This action cannot be undone.
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
                  Delete Rubric
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
