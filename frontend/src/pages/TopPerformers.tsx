import { useState, useEffect } from 'react';
import { api } from '@/api/client';
import { TopPerformer, Trait } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Plus, Users, Play, Loader2, X, Link2, Copy, Check } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

const STATUS_COLORS: Record<string, string> = {
  PENDING: 'bg-yellow-100 text-yellow-800',
  IN_PROGRESS: 'bg-blue-100 text-blue-800',
  COMPLETED: 'bg-green-100 text-green-800',
  ARCHIVED: 'bg-gray-100 text-gray-800',
};

export default function TopPerformers() {
  const [performers, setPerformers] = useState<TopPerformer[]>([]);
  const [traits, setTraits] = useState<Trait[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isProfilingOpen, setIsProfilingOpen] = useState(false);
  const [selectedPerformer, setSelectedPerformer] = useState<TopPerformer | null>(null);
  const [selectedTraits, setSelectedTraits] = useState<string[]>([]);
  const [creating, setCreating] = useState(false);
  const [startingProfiling, setStartingProfiling] = useState(false);

  // Invitation dialog state
  const [inviteDialogOpen, setInviteDialogOpen] = useState(false);
  const [invitePerformer, setInvitePerformer] = useState<TopPerformer | null>(null);
  const [inviteLink, setInviteLink] = useState<string | null>(null);
  const [inviteLoading, setInviteLoading] = useState(false);
  const [linkCopied, setLinkCopied] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    job_title: '',
    department: '',
    role_category: '',
    tenure_months: '',
    email: '',
    employee_id: '',
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [performersRes, traitsRes] = await Promise.all([
        api.getTopPerformers(),
        api.getTraits({ limit: 100 }),
      ]);
      setPerformers(performersRes.data.items);
      setTraits(traitsRes.data.items);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    setCreating(true);
    try {
      await api.createTopPerformer({
        name: formData.name || undefined,
        job_title: formData.job_title,
        department: formData.department || undefined,
        role_category: formData.role_category,
        tenure_months: formData.tenure_months ? parseInt(formData.tenure_months) : undefined,
        email: formData.email || undefined,
        employee_id: formData.employee_id || undefined,
      });
      setIsCreateOpen(false);
      setFormData({
        name: '',
        job_title: '',
        department: '',
        role_category: '',
        tenure_months: '',
        email: '',
        employee_id: '',
      });
      loadData();
    } catch (error) {
      console.error('Failed to create performer:', error);
    } finally {
      setCreating(false);
    }
  };

  const openProfilingDialog = (performer: TopPerformer) => {
    setSelectedPerformer(performer);
    setSelectedTraits([]);
    setIsProfilingOpen(true);
  };

  const startProfiling = async () => {
    if (!selectedPerformer || selectedTraits.length === 0) return;

    setStartingProfiling(true);
    try {
      const response = await api.startProfilingSession({
        top_performer_id: selectedPerformer.id,
        target_traits: selectedTraits,
      });
      // Store initial prompt and navigate
      localStorage.setItem(`profiling_${response.data.session_id}`, JSON.stringify(response.data));
      window.location.href = `/profiling/${response.data.session_id}`;
    } catch (error) {
      console.error('Failed to start profiling:', error);
      setStartingProfiling(false);
    }
  };

  const toggleTrait = (traitName: string) => {
    setSelectedTraits(prev =>
      prev.includes(traitName)
        ? prev.filter(t => t !== traitName)
        : [...prev, traitName]
    );
  };

  // Open invite dialog
  const handleOpenInviteDialog = (performer: TopPerformer) => {
    if (!performer.email) {
      alert('This performer does not have an email address. Please add one first.');
      return;
    }
    setInvitePerformer(performer);
    setInviteLink(null);
    setLinkCopied(false);
    setInviteDialogOpen(true);
  };

  // Create invitation
  const handleCreateInvitation = async () => {
    if (!invitePerformer || !invitePerformer.email) return;

    setInviteLoading(true);
    try {
      const response = await api.createTopPerformerInvitation({
        top_performer_id: invitePerformer.id,
        recipient_email: invitePerformer.email,
        recipient_name: invitePerformer.name || undefined,
        custom_message: `You've been invited to participate in a profile development session.`,
      });
      // Build full link from token
      const baseUrl = window.location.origin;
      setInviteLink(`${baseUrl}/invite/${response.data.token}`);
    } catch (err) {
      console.error('Failed to create invitation:', err);
    } finally {
      setInviteLoading(false);
    }
  };

  // Copy link to clipboard
  const handleCopyLink = async () => {
    if (!inviteLink) return;
    try {
      await navigator.clipboard.writeText(inviteLink);
      setLinkCopied(true);
      setTimeout(() => setLinkCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Top Performers</h1>
          <p className="text-muted-foreground">
            Profile high performers to build organization-specific rubrics
          </p>
        </div>
        <Button onClick={() => setIsCreateOpen(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Add Top Performer
        </Button>
      </div>

      {/* Create Dialog */}
      {isCreateOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center">
          <Card className="w-full max-w-md">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Add Top Performer</CardTitle>
                <Button variant="ghost" size="icon" onClick={() => setIsCreateOpen(false)}>
                  <X className="h-4 w-4" />
                </Button>
              </div>
              <CardDescription>
                Add a high-performing employee to profile their traits.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Name (optional)</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="John Smith"
                  autoComplete="off"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="job_title">Job Title *</Label>
                <Input
                  id="job_title"
                  value={formData.job_title}
                  onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
                  placeholder="Senior Software Engineer"
                  autoComplete="off"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="department">Department</Label>
                  <Input
                    id="department"
                    value={formData.department}
                    onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                    placeholder="Engineering"
                    autoComplete="off"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="role_category">Role Category *</Label>
                  <Input
                    id="role_category"
                    value={formData.role_category}
                    onChange={(e) => setFormData({ ...formData, role_category: e.target.value })}
                    placeholder="Software Development"
                    autoComplete="off"
                    required
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="tenure_months">Tenure (months)</Label>
                  <Input
                    id="tenure_months"
                    type="number"
                    min="0"
                    value={formData.tenure_months}
                    onChange={(e) => setFormData({ ...formData, tenure_months: e.target.value })}
                    placeholder="24"
                    autoComplete="off"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    placeholder="john@company.com"
                    autoComplete="off"
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2 pt-4">
                <Button variant="outline" onClick={() => setIsCreateOpen(false)}>
                  Cancel
                </Button>
                <Button
                  onClick={handleCreate}
                  disabled={creating || !formData.job_title || !formData.role_category}
                >
                  {creating ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                  Add Performer
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Profiling Dialog */}
      {isProfilingOpen && selectedPerformer && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center">
          <Card className="w-full max-w-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Start Profiling Session</CardTitle>
                <Button variant="ghost" size="icon" onClick={() => setIsProfilingOpen(false)}>
                  <X className="h-4 w-4" />
                </Button>
              </div>
              <CardDescription>
                Select which traits to explore with {selectedPerformer.name || 'this performer'}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label className="text-sm font-medium">Selected Traits ({selectedTraits.length})</Label>
                <p className="text-sm text-muted-foreground mb-3">
                  Click traits to select them for this profiling session
                </p>
                <div className="flex flex-wrap gap-2 max-h-64 overflow-y-auto">
                  {traits.map((trait) => (
                    <Badge
                      key={trait.id}
                      variant={selectedTraits.includes(trait.name) ? 'default' : 'outline'}
                      className="cursor-pointer"
                      onClick={() => toggleTrait(trait.name)}
                    >
                      {trait.name}
                    </Badge>
                  ))}
                </div>
              </div>
              <div className="flex justify-end gap-2 pt-4">
                <Button variant="outline" onClick={() => setIsProfilingOpen(false)}>
                  Cancel
                </Button>
                <Button
                  onClick={startProfiling}
                  disabled={startingProfiling || selectedTraits.length === 0}
                >
                  {startingProfiling ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                  Start Profiling ({selectedTraits.length} traits)
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {performers.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Users className="h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">No top performers yet</h3>
            <p className="text-muted-foreground text-center mb-4">
              Add your high-performing employees to start profiling their traits.
            </p>
            <Button onClick={() => setIsCreateOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Add Your First Top Performer
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Top Performers ({performers.length})</CardTitle>
            <CardDescription>
              Profile these employees to extract trait patterns for your rubrics
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4 font-medium">Name / Title</th>
                    <th className="text-left py-3 px-4 font-medium">Role Category</th>
                    <th className="text-left py-3 px-4 font-medium">Department</th>
                    <th className="text-left py-3 px-4 font-medium">Status</th>
                    <th className="text-left py-3 px-4 font-medium">Profile</th>
                    <th className="text-right py-3 px-4 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {performers.map((performer) => (
                    <tr key={performer.id} className="border-b last:border-b-0">
                      <td className="py-3 px-4">
                        <div>
                          <div className="font-medium">
                            {performer.name || 'Anonymous'}
                          </div>
                          <div className="text-sm text-muted-foreground">
                            {performer.job_title}
                          </div>
                        </div>
                      </td>
                      <td className="py-3 px-4">{performer.role_category}</td>
                      <td className="py-3 px-4">{performer.department || '-'}</td>
                      <td className="py-3 px-4">
                        <Badge className={STATUS_COLORS[performer.profiling_status]}>
                          {performer.profiling_status}
                        </Badge>
                      </td>
                      <td className="py-3 px-4">
                        {performer.trait_profile
                          ? Object.keys(performer.trait_profile).length
                          : 0} traits
                      </td>
                      <td className="py-3 px-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => openProfilingDialog(performer)}
                          >
                            <Play className="h-4 w-4 mr-1" />
                            Profile
                          </Button>
                          {performer.email && (
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => handleOpenInviteDialog(performer)}
                            >
                              <Link2 className="h-4 w-4 mr-1" />
                              Invite
                            </Button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Invitation Dialog */}
      <Dialog open={inviteDialogOpen} onOpenChange={setInviteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Send Profiling Invitation</DialogTitle>
            <DialogDescription>
              Generate a self-service profiling link for {invitePerformer?.name || 'this performer'}.
            </DialogDescription>
          </DialogHeader>

          <div className="py-4">
            {!inviteLink ? (
              <div className="text-center">
                <p className="text-sm text-muted-foreground mb-4">
                  Click the button below to generate a unique profiling session link that will
                  be sent to <strong>{invitePerformer?.email}</strong>.
                </p>
                <p className="text-xs text-muted-foreground">
                  The link will expire in 14 days.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="p-3 bg-muted rounded-lg">
                  <p className="text-sm font-medium mb-2">Invitation Link:</p>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 text-xs bg-background p-2 rounded border overflow-x-auto">
                      {inviteLink}
                    </code>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleCopyLink}
                    >
                      {linkCopied ? (
                        <Check className="h-4 w-4 text-green-600" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground">
                  Share this link with the employee. They will be guided through a conversational
                  session to explore their work experiences and extract trait patterns.
                </p>
              </div>
            )}
          </div>

          <DialogFooter>
            {!inviteLink ? (
              <>
                <Button variant="outline" onClick={() => setInviteDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleCreateInvitation} disabled={inviteLoading}>
                  {inviteLoading ? 'Generating...' : 'Generate Link'}
                </Button>
              </>
            ) : (
              <Button onClick={() => setInviteDialogOpen(false)}>
                Done
              </Button>
            )}
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
