import { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { api } from '@/api/client';
import { Organization, EmailSettings } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Checkbox } from '@/components/ui/checkbox';
import {
  User,
  Building2,
  Key,
  Mail,
  Loader2,
  CheckCircle,
  AlertTriangle,
  Send,
} from 'lucide-react';

export default function Settings() {
  const { user, refreshUser } = useAuth();

  // Profile form state
  const [profileName, setProfileName] = useState('');
  const [profilePhone, setProfilePhone] = useState('');
  const [profileTitle, setProfileTitle] = useState('');
  const [profileBio, setProfileBio] = useState('');
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileSuccess, setProfileSuccess] = useState(false);
  const [profileError, setProfileError] = useState<string | null>(null);

  // Password form state
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordSuccess, setPasswordSuccess] = useState(false);
  const [passwordError, setPasswordError] = useState<string | null>(null);

  // Organization state
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [orgName, setOrgName] = useState('');
  const [orgDescription, setOrgDescription] = useState('');
  const [orgIndustry, setOrgIndustry] = useState('');
  const [orgWebsite, setOrgWebsite] = useState('');
  const [orgLoading, setOrgLoading] = useState(false);
  const [orgFetching, setOrgFetching] = useState(false);
  const [orgSuccess, setOrgSuccess] = useState(false);
  const [orgError, setOrgError] = useState<string | null>(null);

  // Email settings state
  const [emailSettings, setEmailSettings] = useState<EmailSettings | null>(null);
  const [smtpHost, setSmtpHost] = useState('');
  const [smtpPort, setSmtpPort] = useState(587);
  const [smtpUser, setSmtpUser] = useState('');
  const [smtpPassword, setSmtpPassword] = useState('');
  const [smtpFromEmail, setSmtpFromEmail] = useState('');
  const [smtpFromName, setSmtpFromName] = useState('');
  const [smtpUseTls, setSmtpUseTls] = useState(true);
  const [emailLoading, setEmailLoading] = useState(false);
  const [emailFetching, setEmailFetching] = useState(false);
  const [emailSuccess, setEmailSuccess] = useState(false);
  const [emailError, setEmailError] = useState<string | null>(null);

  // Test email state
  const [testEmail, setTestEmail] = useState('');
  const [testEmailLoading, setTestEmailLoading] = useState(false);
  const [testEmailSuccess, setTestEmailSuccess] = useState<string | null>(null);
  const [testEmailError, setTestEmailError] = useState<string | null>(null);

  // Initialize profile form with current user data
  useEffect(() => {
    if (user) {
      setProfileName(user.full_name || '');
      setProfilePhone(user.phone || '');
      setProfileTitle(user.title || '');
      setProfileBio(user.bio || '');
    }
  }, [user]);

  // Fetch organization data
  useEffect(() => {
    const fetchOrg = async () => {
      if (!user?.organization_id) return;

      setOrgFetching(true);
      try {
        const response = await api.getOrganization(user.organization_id);
        const org = response.data;
        setOrganization(org);
        setOrgName(org.name || '');
        setOrgDescription(org.description || '');
        setOrgIndustry(org.industry || '');
        setOrgWebsite(org.website || '');
      } catch (err) {
        console.error('Failed to fetch organization:', err);
      } finally {
        setOrgFetching(false);
      }
    };

    fetchOrg();
  }, [user?.organization_id]);

  const isAdmin = user?.role === 'ADMIN' || user?.is_superuser;

  // Fetch email settings
  useEffect(() => {
    const fetchEmailSettings = async () => {
      if (!user?.organization_id || !(user?.role === 'ADMIN' || user?.is_superuser)) return;

      setEmailFetching(true);
      try {
        const response = await api.getEmailSettings(user.organization_id);
        const settings = response.data;
        setEmailSettings(settings);
        setSmtpHost(settings.smtp_host || '');
        setSmtpPort(settings.smtp_port || 587);
        setSmtpUser(settings.smtp_user || '');
        setSmtpFromEmail(settings.smtp_from_email || '');
        setSmtpFromName(settings.smtp_from_name || '');
        setSmtpUseTls(settings.smtp_use_tls ?? true);
      } catch (err) {
        console.error('Failed to fetch email settings:', err);
      } finally {
        setEmailFetching(false);
      }
    };

    fetchEmailSettings();
  }, [user?.organization_id, user?.role, user?.is_superuser]);

  // Handle profile update
  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileLoading(true);
    setProfileError(null);
    setProfileSuccess(false);

    try {
      await api.updateMe({
        full_name: profileName.trim() || undefined,
        phone: profilePhone.trim() || undefined,
        title: profileTitle.trim() || undefined,
        bio: profileBio.trim() || undefined,
      });
      setProfileSuccess(true);
      if (refreshUser) {
        refreshUser();
      }
      setTimeout(() => setProfileSuccess(false), 3000);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setProfileError(error.response?.data?.detail || 'Failed to update profile');
    } finally {
      setProfileLoading(false);
    }
  };

  // Handle password change
  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError(null);
    setPasswordSuccess(false);

    if (newPassword !== confirmPassword) {
      setPasswordError('New passwords do not match');
      return;
    }

    if (newPassword.length < 8) {
      setPasswordError('Password must be at least 8 characters');
      return;
    }

    setPasswordLoading(true);

    try {
      await api.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });
      setPasswordSuccess(true);
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => setPasswordSuccess(false), 3000);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setPasswordError(error.response?.data?.detail || 'Failed to change password');
    } finally {
      setPasswordLoading(false);
    }
  };

  // Handle organization update
  const handleOrgUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!organization) return;

    setOrgLoading(true);
    setOrgError(null);
    setOrgSuccess(false);

    try {
      await api.updateOrganization(organization.id, {
        name: orgName.trim() || undefined,
        description: orgDescription.trim() || undefined,
      });
      setOrgSuccess(true);
      setTimeout(() => setOrgSuccess(false), 3000);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setOrgError(error.response?.data?.detail || 'Failed to update organization');
    } finally {
      setOrgLoading(false);
    }
  };

  // Handle email settings update
  const handleEmailSettingsUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user?.organization_id) return;

    setEmailLoading(true);
    setEmailError(null);
    setEmailSuccess(false);

    try {
      const response = await api.updateEmailSettings(user.organization_id, {
        smtp_host: smtpHost.trim(),
        smtp_port: smtpPort,
        smtp_user: smtpUser.trim(),
        smtp_password: smtpPassword || undefined,
        smtp_from_email: smtpFromEmail.trim(),
        smtp_from_name: smtpFromName.trim(),
        smtp_use_tls: smtpUseTls,
      });
      setEmailSettings(response.data);
      setSmtpPassword(''); // Clear password field after save
      setEmailSuccess(true);
      setTimeout(() => setEmailSuccess(false), 3000);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setEmailError(error.response?.data?.detail || 'Failed to update email settings');
    } finally {
      setEmailLoading(false);
    }
  };

  // Handle test email
  const handleTestEmail = async () => {
    if (!user?.organization_id || !testEmail) return;

    setTestEmailLoading(true);
    setTestEmailSuccess(null);
    setTestEmailError(null);

    try {
      const response = await api.testEmailSettings(user.organization_id, testEmail);
      if (response.data.success) {
        setTestEmailSuccess(response.data.message);
        setTimeout(() => setTestEmailSuccess(null), 5000);
      } else {
        setTestEmailError(response.data.error_detail || response.data.message);
      }
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setTestEmailError(error.response?.data?.detail || 'Failed to send test email');
    } finally {
      setTestEmailLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account and organization preferences
        </p>
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList>
          <TabsTrigger value="profile" className="flex items-center gap-2">
            <User className="h-4 w-4" />
            Profile
          </TabsTrigger>
          <TabsTrigger value="security" className="flex items-center gap-2">
            <Key className="h-4 w-4" />
            Security
          </TabsTrigger>
          {isAdmin && (
            <TabsTrigger value="organization" className="flex items-center gap-2">
              <Building2 className="h-4 w-4" />
              Organization
            </TabsTrigger>
          )}
          {isAdmin && (
            <TabsTrigger value="email" className="flex items-center gap-2">
              <Mail className="h-4 w-4" />
              Email
            </TabsTrigger>
          )}
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>Profile Information</CardTitle>
              <CardDescription>
                Update your personal information displayed across the platform.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleProfileUpdate} className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="full_name">Full Name</Label>
                    <Input
                      id="full_name"
                      value={profileName}
                      onChange={(e) => setProfileName(e.target.value)}
                      placeholder="Enter your full name"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      value={user?.email || ''}
                      disabled
                      className="bg-muted"
                    />
                    <p className="text-xs text-muted-foreground">
                      Contact support to change your email
                    </p>
                  </div>
                </div>

                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone</Label>
                    <Input
                      id="phone"
                      value={profilePhone}
                      onChange={(e) => setProfilePhone(e.target.value)}
                      placeholder="Enter your phone number"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="title">Job Title</Label>
                    <Input
                      id="title"
                      value={profileTitle}
                      onChange={(e) => setProfileTitle(e.target.value)}
                      placeholder="Enter your job title"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="bio">Bio</Label>
                  <Textarea
                    id="bio"
                    value={profileBio}
                    onChange={(e) => setProfileBio(e.target.value)}
                    placeholder="Tell us a bit about yourself"
                    rows={3}
                  />
                </div>

                {profileError && (
                  <div className="flex items-center gap-2 text-sm text-destructive">
                    <AlertTriangle className="h-4 w-4" />
                    {profileError}
                  </div>
                )}

                {profileSuccess && (
                  <div className="flex items-center gap-2 text-sm text-green-600">
                    <CheckCircle className="h-4 w-4" />
                    Profile updated successfully
                  </div>
                )}

                <Button type="submit" disabled={profileLoading}>
                  {profileLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    'Save Changes'
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Security Tab */}
        <TabsContent value="security">
          <Card>
            <CardHeader>
              <CardTitle>Change Password</CardTitle>
              <CardDescription>
                Update your password to keep your account secure.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handlePasswordChange} className="space-y-4 max-w-md">
                <div className="space-y-2">
                  <Label htmlFor="current_password">Current Password</Label>
                  <Input
                    id="current_password"
                    type="password"
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    placeholder="Enter current password"
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="new_password">New Password</Label>
                  <Input
                    id="new_password"
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="Enter new password"
                    required
                    minLength={8}
                  />
                  <p className="text-xs text-muted-foreground">
                    Must be at least 8 characters
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirm_password">Confirm New Password</Label>
                  <Input
                    id="confirm_password"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Confirm new password"
                    required
                  />
                </div>

                {passwordError && (
                  <div className="flex items-center gap-2 text-sm text-destructive">
                    <AlertTriangle className="h-4 w-4" />
                    {passwordError}
                  </div>
                )}

                {passwordSuccess && (
                  <div className="flex items-center gap-2 text-sm text-green-600">
                    <CheckCircle className="h-4 w-4" />
                    Password changed successfully
                  </div>
                )}

                <Button type="submit" disabled={passwordLoading}>
                  {passwordLoading ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Changing...
                    </>
                  ) : (
                    'Change Password'
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card className="mt-6">
            <CardHeader>
              <CardTitle>Account Information</CardTitle>
              <CardDescription>
                Your account details and permissions.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between py-2 border-b">
                  <span className="text-sm text-muted-foreground">User ID</span>
                  <span className="text-sm font-mono">{user?.id}</span>
                </div>
                <div className="flex items-center justify-between py-2 border-b">
                  <span className="text-sm text-muted-foreground">Role</span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary">
                    {user?.role}
                  </span>
                </div>
                <div className="flex items-center justify-between py-2 border-b">
                  <span className="text-sm text-muted-foreground">Status</span>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    user?.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {user?.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                {user?.is_superuser && (
                  <div className="flex items-center justify-between py-2 border-b">
                    <span className="text-sm text-muted-foreground">Superuser</span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                      Yes
                    </span>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Organization Tab (Admin only) */}
        {isAdmin && (
          <TabsContent value="organization">
            {orgFetching ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : !organization ? (
              <Card>
                <CardContent className="py-12 text-center">
                  <Building2 className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No Organization</h3>
                  <p className="text-muted-foreground">
                    You are not associated with any organization.
                  </p>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardHeader>
                  <CardTitle>Organization Settings</CardTitle>
                  <CardDescription>
                    Manage your organization's profile and preferences.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleOrgUpdate} className="space-y-4">
                    <div className="grid gap-4 sm:grid-cols-2">
                      <div className="space-y-2">
                        <Label htmlFor="org_name">Organization Name</Label>
                        <Input
                          id="org_name"
                          value={orgName}
                          onChange={(e) => setOrgName(e.target.value)}
                          placeholder="Enter organization name"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="org_slug">Slug</Label>
                        <Input
                          id="org_slug"
                          value={organization.slug}
                          disabled
                          className="bg-muted"
                        />
                        <p className="text-xs text-muted-foreground">
                          Unique identifier (cannot be changed)
                        </p>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="org_description">Description</Label>
                      <Textarea
                        id="org_description"
                        value={orgDescription}
                        onChange={(e) => setOrgDescription(e.target.value)}
                        placeholder="Describe your organization"
                        rows={3}
                      />
                    </div>

                    <div className="grid gap-4 sm:grid-cols-2">
                      <div className="space-y-2">
                        <Label htmlFor="org_industry">Industry</Label>
                        <Input
                          id="org_industry"
                          value={orgIndustry}
                          disabled
                          className="bg-muted"
                          placeholder="Not set"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="org_website">Website</Label>
                        <Input
                          id="org_website"
                          value={orgWebsite}
                          disabled
                          className="bg-muted"
                          placeholder="Not set"
                        />
                      </div>
                    </div>

                    {orgError && (
                      <div className="flex items-center gap-2 text-sm text-destructive">
                        <AlertTriangle className="h-4 w-4" />
                        {orgError}
                      </div>
                    )}

                    {orgSuccess && (
                      <div className="flex items-center gap-2 text-sm text-green-600">
                        <CheckCircle className="h-4 w-4" />
                        Organization updated successfully
                      </div>
                    )}

                    <Button type="submit" disabled={orgLoading}>
                      {orgLoading ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Saving...
                        </>
                      ) : (
                        'Save Changes'
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            )}

            {organization && (
              <Card className="mt-6">
                <CardHeader>
                  <CardTitle>Organization Details</CardTitle>
                  <CardDescription>
                    Additional information about your organization.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between py-2 border-b">
                      <span className="text-sm text-muted-foreground">Organization ID</span>
                      <span className="text-sm font-mono">{organization.id}</span>
                    </div>
                    <div className="flex items-center justify-between py-2 border-b">
                      <span className="text-sm text-muted-foreground">Status</span>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        organization.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {organization.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <div className="flex items-center justify-between py-2 border-b">
                      <span className="text-sm text-muted-foreground">Created</span>
                      <span className="text-sm">
                        {new Date(organization.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        )}

        {/* Email Settings Tab (Admin only) */}
        {isAdmin && (
          <TabsContent value="email">
            {emailFetching ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>Email Configuration</CardTitle>
                    <CardDescription>
                      Configure SMTP settings for sending interview invitations and notifications.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <form onSubmit={handleEmailSettingsUpdate} className="space-y-4">
                      <div className="grid gap-4 sm:grid-cols-2">
                        <div className="space-y-2">
                          <Label htmlFor="smtp_host">SMTP Host</Label>
                          <Input
                            id="smtp_host"
                            value={smtpHost}
                            onChange={(e) => setSmtpHost(e.target.value)}
                            placeholder="smtp.gmail.com"
                            required
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="smtp_port">SMTP Port</Label>
                          <Input
                            id="smtp_port"
                            type="number"
                            value={smtpPort}
                            onChange={(e) => setSmtpPort(parseInt(e.target.value) || 587)}
                            min={1}
                            max={65535}
                            required
                          />
                        </div>
                      </div>

                      <div className="grid gap-4 sm:grid-cols-2">
                        <div className="space-y-2">
                          <Label htmlFor="smtp_user">SMTP Username</Label>
                          <Input
                            id="smtp_user"
                            value={smtpUser}
                            onChange={(e) => setSmtpUser(e.target.value)}
                            placeholder="your-email@gmail.com"
                            required
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="smtp_password">SMTP Password</Label>
                          <Input
                            id="smtp_password"
                            type="password"
                            value={smtpPassword}
                            onChange={(e) => setSmtpPassword(e.target.value)}
                            placeholder={emailSettings?.smtp_password_set ? '••••••••' : 'Enter password'}
                          />
                          {emailSettings?.smtp_password_set && (
                            <p className="text-xs text-muted-foreground">
                              Password is configured. Leave blank to keep existing.
                            </p>
                          )}
                        </div>
                      </div>

                      <div className="grid gap-4 sm:grid-cols-2">
                        <div className="space-y-2">
                          <Label htmlFor="smtp_from_email">From Email</Label>
                          <Input
                            id="smtp_from_email"
                            type="email"
                            value={smtpFromEmail}
                            onChange={(e) => setSmtpFromEmail(e.target.value)}
                            placeholder="noreply@yourcompany.com"
                            required
                          />
                        </div>
                        <div className="space-y-2">
                          <Label htmlFor="smtp_from_name">From Name</Label>
                          <Input
                            id="smtp_from_name"
                            value={smtpFromName}
                            onChange={(e) => setSmtpFromName(e.target.value)}
                            placeholder="Your Company"
                            required
                          />
                        </div>
                      </div>

                      <div className="flex items-center space-x-2">
                        <Checkbox
                          id="smtp_use_tls"
                          checked={smtpUseTls}
                          onCheckedChange={(checked) => setSmtpUseTls(checked === true)}
                        />
                        <Label htmlFor="smtp_use_tls" className="text-sm font-normal">
                          Use TLS (recommended for secure email transmission)
                        </Label>
                      </div>

                      {emailSettings?.is_configured && (
                        <div className="flex items-center gap-2 text-sm text-green-600 bg-green-50 p-3 rounded-md">
                          <CheckCircle className="h-4 w-4" />
                          Email is configured
                          {emailSettings.configured_at && (
                            <span className="text-muted-foreground">
                              (Last updated: {new Date(emailSettings.configured_at).toLocaleDateString()})
                            </span>
                          )}
                        </div>
                      )}

                      {emailError && (
                        <div className="flex items-center gap-2 text-sm text-destructive">
                          <AlertTriangle className="h-4 w-4" />
                          {emailError}
                        </div>
                      )}

                      {emailSuccess && (
                        <div className="flex items-center gap-2 text-sm text-green-600">
                          <CheckCircle className="h-4 w-4" />
                          Email settings saved successfully
                        </div>
                      )}

                      <Button type="submit" disabled={emailLoading}>
                        {emailLoading ? (
                          <>
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                            Saving...
                          </>
                        ) : (
                          'Save Email Settings'
                        )}
                      </Button>
                    </form>
                  </CardContent>
                </Card>

                <Card className="mt-6">
                  <CardHeader>
                    <CardTitle>Test Configuration</CardTitle>
                    <CardDescription>
                      Send a test email to verify your SMTP settings are working correctly.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4 max-w-md">
                      <div className="space-y-2">
                        <Label htmlFor="test_email">Recipient Email</Label>
                        <Input
                          id="test_email"
                          type="email"
                          value={testEmail}
                          onChange={(e) => setTestEmail(e.target.value)}
                          placeholder="your-email@example.com"
                        />
                      </div>

                      {testEmailError && (
                        <div className="flex items-center gap-2 text-sm text-destructive">
                          <AlertTriangle className="h-4 w-4" />
                          {testEmailError}
                        </div>
                      )}

                      {testEmailSuccess && (
                        <div className="flex items-center gap-2 text-sm text-green-600">
                          <CheckCircle className="h-4 w-4" />
                          {testEmailSuccess}
                        </div>
                      )}

                      <Button
                        type="button"
                        variant="outline"
                        onClick={handleTestEmail}
                        disabled={testEmailLoading || !testEmail || !emailSettings?.is_configured}
                      >
                        {testEmailLoading ? (
                          <>
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                            Sending...
                          </>
                        ) : (
                          <>
                            <Send className="h-4 w-4 mr-2" />
                            Send Test Email
                          </>
                        )}
                      </Button>

                      {!emailSettings?.is_configured && (
                        <p className="text-xs text-muted-foreground">
                          Please save your email settings before sending a test email.
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>
        )}
      </Tabs>
    </div>
  );
}
