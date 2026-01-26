import { useEffect, useState } from 'react';
import { api } from '@/api/client';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  ImpactDashboardResponse,
  ComplianceStatus,
  DisparateImpactReport,
} from '@/types';
import {
  AlertTriangle,
  CheckCircle,
  XCircle,
  Clock,
  FileText,
  TrendingDown,
  Shield,
} from 'lucide-react';

export function Compliance() {
  const [dashboard, setDashboard] = useState<ImpactDashboardResponse | null>(null);
  const [status, setStatus] = useState<ComplianceStatus | null>(null);
  const [reports, setReports] = useState<DisparateImpactReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [dashboardRes, statusRes, reportsRes] = await Promise.all([
        api.getImpactDashboard(),
        api.getComplianceStatus(),
        api.getImpactReports({ limit: 5 }),
      ]);
      setDashboard(dashboardRes.data);
      setStatus(statusRes.data);
      setReports(reportsRes.data);
    } catch (err) {
      setError('Failed to load compliance data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    if (!status?.organization_id) return;

    setGenerating(true);
    try {
      const now = new Date();
      const oneYearAgo = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());

      await api.generateImpactReport({
        organization_id: status.organization_id,
        period_start: oneYearAgo.toISOString(),
        period_end: now.toISOString(),
        report_type: 'ANNUAL',
      });

      // Refresh data
      fetchData();
    } catch (err) {
      setError('Failed to generate report');
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin h-8 w-8 border-2 border-foreground border-t-transparent rounded-full" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <XCircle className="h-12 w-12 text-destructive mx-auto mb-4" />
        <p className="text-muted-foreground">{error}</p>
        <Button onClick={fetchData} className="mt-4">
          Retry
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-serif font-semibold">Compliance & Bias Monitoring</h1>
          <p className="text-muted-foreground mt-1">
            Monitor assessment fairness and regulatory compliance
          </p>
        </div>
        <Button onClick={handleGenerateReport} disabled={generating}>
          {generating ? 'Generating...' : 'Generate Annual Report'}
        </Button>
      </div>

      {/* Compliance Status Card */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-lg font-medium flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Compliance Status
          </CardTitle>
          {status?.is_compliant ? (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-sm bg-green-100 text-green-800">
              <CheckCircle className="h-4 w-4" />
              Compliant
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-sm bg-yellow-100 text-yellow-800">
              <AlertTriangle className="h-4 w-4" />
              Action Required
            </span>
          )}
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-sm text-muted-foreground">Last Audit</p>
              <p className="text-lg font-medium">
                {status?.last_audit_date
                  ? new Date(status.last_audit_date).toLocaleDateString()
                  : 'Never'}
              </p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Next Audit Due</p>
              <p className="text-lg font-medium">
                {status?.next_audit_due
                  ? new Date(status.next_audit_due).toLocaleDateString()
                  : 'Immediately'}
              </p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Rubric Issues</p>
              <p className="text-lg font-medium">{status?.rubric_validation_issues || 0}</p>
            </div>
          </div>

          {/* Warnings */}
          {status?.warnings && status.warnings.length > 0 && (
            <div className="mt-6 border-t pt-4">
              <h4 className="text-sm font-medium mb-2">Warnings</h4>
              <ul className="space-y-2">
                {status.warnings.map((warning, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm">
                    <AlertTriangle className="h-4 w-4 text-yellow-600 mt-0.5 flex-shrink-0" />
                    <span>{warning}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Missing Documentation */}
          {status?.missing_documentation && status.missing_documentation.length > 0 && (
            <div className="mt-4 border-t pt-4">
              <h4 className="text-sm font-medium mb-2">Missing Documentation</h4>
              <ul className="space-y-1">
                {status.missing_documentation.map((doc, i) => (
                  <li key={i} className="text-sm text-muted-foreground">
                    - {doc.replace(/_/g, ' ')}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Disparate Impact Alerts */}
      {dashboard?.alerts && dashboard.alerts.length > 0 && (
        <Card className="border-yellow-200 bg-yellow-50">
          <CardHeader>
            <CardTitle className="text-lg font-medium flex items-center gap-2">
              <TrendingDown className="h-5 w-5 text-yellow-700" />
              Disparate Impact Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {dashboard.alerts.map((alert, i) => (
                <div
                  key={i}
                  className={`p-4 rounded-lg ${
                    alert.severity === 'HIGH'
                      ? 'bg-red-100 border border-red-200'
                      : 'bg-yellow-100 border border-yellow-200'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-medium">
                        {alert.protected_class.replace(/_/g, ' ')} - {alert.group}
                      </p>
                      <p className="text-sm text-muted-foreground mt-1">
                        Selection ratio: {(alert.current_ratio * 100).toFixed(1)}%
                        (threshold: {(alert.threshold * 100).toFixed(0)}%)
                      </p>
                    </div>
                    <span
                      className={`text-xs px-2 py-1 rounded ${
                        alert.severity === 'HIGH'
                          ? 'bg-red-200 text-red-800'
                          : 'bg-yellow-200 text-yellow-800'
                      }`}
                    >
                      {alert.severity}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Impact Ratios by Protected Class */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-medium">Selection Rate Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          {dashboard?.current_ratios && dashboard.current_ratios.length > 0 ? (
            <div className="space-y-6">
              {/* Group by protected class */}
              {['gender', 'race_ethnicity', 'age_group'].map((protectedClass) => {
                const ratios = dashboard.current_ratios.filter(
                  (r) => r.protected_class === protectedClass
                );
                if (ratios.length === 0) return null;

                return (
                  <div key={protectedClass}>
                    <h4 className="text-sm font-medium mb-3 capitalize">
                      {protectedClass.replace(/_/g, ' ')}
                    </h4>
                    <div className="space-y-2">
                      {ratios.map((ratio, i) => (
                        <div key={i} className="flex items-center gap-4">
                          <span className="w-32 text-sm truncate" title={ratio.group_a}>
                            {ratio.group_a.replace(/_/g, ' ')}
                          </span>
                          <div className="flex-1">
                            <div className="h-2 bg-muted rounded-full overflow-hidden">
                              <div
                                className={`h-full rounded-full ${
                                  ratio.passes_four_fifths
                                    ? 'bg-green-500'
                                    : 'bg-red-500'
                                }`}
                                style={{
                                  width: `${Math.min(ratio.impact_ratio * 100, 100)}%`,
                                }}
                              />
                            </div>
                          </div>
                          <span className="w-16 text-sm text-right">
                            {(ratio.impact_ratio * 100).toFixed(0)}%
                          </span>
                          <span className="w-6">
                            {ratio.passes_four_fifths ? (
                              <CheckCircle className="h-4 w-4 text-green-600" />
                            ) : (
                              <XCircle className="h-4 w-4 text-red-600" />
                            )}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-muted-foreground text-center py-8">
              No demographic data available for analysis. Demographic collection is voluntary
              and separate from hiring decisions.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Recent Reports */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-medium flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Recent Reports
          </CardTitle>
        </CardHeader>
        <CardContent>
          {reports.length > 0 ? (
            <div className="space-y-4">
              {reports.map((report) => (
                <div
                  key={report.id}
                  className="flex items-center justify-between p-4 border rounded-lg"
                >
                  <div>
                    <p className="font-medium">{report.report_type} Report</p>
                    <p className="text-sm text-muted-foreground">
                      {new Date(report.period_start).toLocaleDateString()} -{' '}
                      {new Date(report.period_end).toLocaleDateString()}
                    </p>
                    <p className="text-sm text-muted-foreground mt-1">
                      {report.total_assessments} assessments analyzed
                    </p>
                  </div>
                  <div className="flex items-center gap-4">
                    {report.has_disparate_impact ? (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-sm bg-red-100 text-red-800">
                        <AlertTriangle className="h-4 w-4" />
                        Impact Detected
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-sm bg-green-100 text-green-800">
                        <CheckCircle className="h-4 w-4" />
                        No Impact
                      </span>
                    )}
                    <span className="text-sm text-muted-foreground">
                      <Clock className="h-4 w-4 inline mr-1" />
                      {new Date(report.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-muted-foreground text-center py-8">
              No reports generated yet. Generate your first annual report to begin compliance
              tracking.
            </p>
          )}
        </CardContent>
      </Card>

      {/* Four-Fifths Rule Explanation */}
      <Card className="bg-muted/30">
        <CardHeader>
          <CardTitle className="text-lg font-medium">About the Four-Fifths Rule</CardTitle>
        </CardHeader>
        <CardContent className="prose prose-sm max-w-none">
          <p>
            The four-fifths (or 80%) rule is a guideline used by the EEOC to identify potential
            adverse impact in employment selection procedures. A selection rate for any
            protected group that is less than 80% of the rate for the group with the highest
            selection rate may indicate adverse impact.
          </p>
          <p className="mt-2">
            <strong>Important:</strong> The four-fifths rule is a guideline, not an absolute
            standard. Disparate impact analysis should be reviewed with employment counsel,
            considering sample sizes, statistical significance, and business necessity.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
