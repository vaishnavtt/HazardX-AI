import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api, formatApiError } from '../api/client';
import type { AlertItem, AlertSummaryResponse, AlertAuditLogItem } from '../types/hazard';
import { GlassCard } from '../components/glass/GlassCard';
import { GlassPanel } from '../components/glass/GlassPanel';
import { GlassModal } from '../components/glass/GlassModal';
import { LiquidButton } from '../components/ui/LiquidButton';
import { LiquidIconButton } from '../components/ui/LiquidIconButton';
import { LiquidSegmentedControl } from '../components/ui/LiquidSegmentedControl';
import { LoadingState } from '../components/common/LoadingState';
import { ErrorState } from '../components/common/ErrorState';
import {
  Bell,
  AlertTriangle,
  ShieldCheck,
  Clock,
  Filter,
  CheckCircle,
  RefreshCw,
  MapPin,
  Globe2,
  ChevronRight,
  Info,
  Droplets,
  Mountain,
  Activity,
  Wind,
  Flame,
  CheckCircle2,
  XCircle,
  Mail,
} from 'lucide-react';

export const AlertManagementPage: React.FC = () => {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [summary, setSummary] = useState<AlertSummaryResponse | null>(null);
  const [selectedAlert, setSelectedAlert] = useState<AlertItem | null>(null);
  const [alertAuditLogs, setAlertAuditLogs] = useState<AlertAuditLogItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState(false);

  // Filters
  const [hazardFilter, setHazardFilter] = useState<string>('ALL');
  const [severityFilter, setSeverityFilter] = useState<string>('ALL');
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [page, setPage] = useState<number>(1);
  const [totalCount, setTotalCount] = useState<number>(0);

  // Resolution modal
  const [showResolveModal, setShowResolveModal] = useState(false);
  const [resolutionNotes, setResolutionNotes] = useState('');
  const [operatorName, setOperatorName] = useState('Duty Incident Officer');

  const hazardColors: Record<string, string> = {
    floods: '#2196F3',
    landslides: '#FF9800',
    earthquakes: '#9C27B0',
    cyclones: '#00BCD4',
    wildfires: '#F44336',
  };

  const hazardIcons: Record<string, any> = {
    floods: Droplets,
    landslides: Mountain,
    earthquakes: Activity,
    cyclones: Wind,
    wildfires: Flame,
  };

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [sumRes, alertsRes] = await Promise.all([
        api.getAlertSummary(),
        api.getAlerts({
          hazard_type: hazardFilter !== 'ALL' ? hazardFilter : undefined,
          severity: severityFilter !== 'ALL' ? severityFilter : undefined,
          status: statusFilter !== 'ALL' ? statusFilter : undefined,
          page,
          page_size: 15,
        }),
      ]);
      setSummary(sumRes);
      setAlerts(alertsRes.items);
      setTotalCount(alertsRes.total);

      if (selectedAlert) {
        const refreshed = alertsRes.items.find((a: AlertItem) => a.alert_id === selectedAlert.alert_id);
        if (refreshed) setSelectedAlert(refreshed);
      }
    } catch (e) {
      setError(formatApiError(e));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [hazardFilter, severityFilter, statusFilter, page]);

  const handleSelectAlert = async (alert: AlertItem) => {
    setSelectedAlert(alert);
    try {
      const logs = await api.getAlertHistory(alert.alert_id);
      setAlertAuditLogs(logs);
    } catch (e) {
      console.error('Error fetching audit logs:', e);
    }
  };

  const handleAcknowledge = async () => {
    if (!selectedAlert) return;
    setActionLoading(true);
    try {
      const updated = await api.acknowledgeAlert(
        selectedAlert.alert_id,
        'Public Duty Officer',
        'Alert acknowledged via public intelligence console.'
      );
      setSelectedAlert(updated);
      fetchData();
    } catch (e) {
      alert(`Acknowledgement error: ${formatApiError(e)}`);
    } finally {
      setActionLoading(false);
    }
  };

  const handleResolve = async () => {
    if (!selectedAlert) return;
    setActionLoading(true);
    try {
      const updated = await api.resolveAlert(
        selectedAlert.alert_id,
        operatorName,
        resolutionNotes || 'Hazard level subsided. Threat cleared.'
      );
      setSelectedAlert(updated);
      setShowResolveModal(false);
      fetchData();
    } catch (e) {
      alert(`Resolution error: ${formatApiError(e)}`);
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-10 max-w-6xl mx-auto pb-16">
      {/* 1. Header Banner */}
      <div className="relative rounded-3xl glass-panel p-8 md:p-10 overflow-hidden border border-slate-200/80 shadow-sm bg-white/80">
        <span className="glass-specular-sheen" />
        <div className="max-w-3xl space-y-3 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold">
            <Bell className="w-3.5 h-3.5" />
            Active Warning Management
          </div>

          <h1 className="text-3xl md:text-5xl font-black text-slate-900 tracking-tight">
            Multi-Hazard <span className="text-rose-600">Alert Center</span>
          </h1>

          <p className="text-slate-600 text-sm md:text-base leading-relaxed">
            Live multi-hazard operational alerts generated by automated rule engines and machine learning inference.
            All alerts include physical telemetry factors, verified sources, and audit histories.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3">
            <LiquidButton
              variant="secondary"
              size="sm"
              onClick={fetchData}
              leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
            >
              Refresh Active Alerts
            </LiquidButton>

            <span className="text-xs text-slate-500 flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-slate-400" />
              Email Dispatch: <span className="text-amber-700 font-medium">Local Mock Mode (SMTP Unconfigured)</span>
            </span>
          </div>
        </div>
      </div>

      {/* 2. Stat Counts */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl glass-card flex flex-col justify-between bg-white/85 border border-slate-200/80 shadow-sm">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Active Alerts</span>
            <span className="text-3xl font-bold text-slate-900 mt-2">{summary.total_active}</span>
          </div>
          <div className="p-5 rounded-2xl glass-card flex flex-col justify-between border-l-4 border-rose-500 bg-white/85 shadow-sm border-slate-200/80">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Critical Threats</span>
            <span className="text-3xl font-bold text-rose-600 mt-2">{summary.total_severe_red}</span>
          </div>
          <div className="p-5 rounded-2xl glass-card flex flex-col justify-between border-l-4 border-amber-500 bg-white/85 shadow-sm border-slate-200/80">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">High Alerts</span>
            <span className="text-3xl font-bold text-amber-600 mt-2">{summary.total_high_orange || 0}</span>
          </div>
          <div className="p-5 rounded-2xl glass-card flex flex-col justify-between border-l-4 border-yellow-500 bg-white/85 shadow-sm border-slate-200/80">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Moderate Advisories</span>
            <span className="text-3xl font-bold text-yellow-600 mt-2">{summary.total_moderate_yellow || 0}</span>
          </div>
        </div>
      )}

      {/* 3. Filters Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl glass-panel bg-white/80 border border-slate-200/80 shadow-sm">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold text-slate-600 uppercase tracking-wider mr-2 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5" /> Hazard:
          </span>
          {['ALL', 'floods', 'landslides', 'earthquakes', 'cyclones', 'wildfires'].map((hz) => (
            <button
              key={hz}
              type="button"
              onClick={() => { setHazardFilter(hz); setPage(1); }}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold capitalize transition-all ${hazardFilter === hz
                ? 'bg-sky-100 text-sky-800 border border-sky-300 shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200/50'
                }`}
            >
              {hz}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-500">Severity:</span>
          {['ALL', 'RED', 'ORANGE', 'YELLOW'].map((sev) => (
            <button
              key={sev}
              type="button"
              onClick={() => { setSeverityFilter(sev); setPage(1); }}
              className={`px-2.5 py-1 rounded-full text-xs font-bold transition-all ${severityFilter === sev
                ? 'bg-slate-800 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:text-slate-900 border border-slate-200/50'
                }`}
            >
              {sev}
            </button>
          ))}
        </div>
      </div>

      {/* 4. Alert List and Details Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: List of Alerts */}
        <div className="lg:col-span-2 space-y-3">
          {loading ? (
            <div className="p-8 glass-panel rounded-2xl text-center text-slate-500 text-sm bg-white/80 border border-slate-200/80">
              Loading active operational alerts...
            </div>
          ) : alerts.length > 0 ? (
            alerts.map((alt) => {
              const hColor = hazardColors[alt.hazard_type] || '#0284C7';
              const isSelected = selectedAlert?.alert_id === alt.alert_id;

              return (
                <div
                  key={alt.alert_id}
                  onClick={() => handleSelectAlert(alt)}
                  className={`p-4 rounded-2xl glass-card transition-all cursor-pointer bg-white/85 border ${isSelected ? 'border-sky-500 bg-sky-50/50 shadow-md ring-2 ring-sky-400/20' : 'border-slate-200/80 hover:bg-slate-50/80 shadow-sm'
                    }`}
                  style={{ borderLeft: `4px solid ${hColor}` }}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span
                          className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full"
                          style={{ background: `${hColor}18`, color: hColor }}
                        >
                          {alt.hazard_type}
                        </span>

                        <span
                          className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${alt.severity === 'RED'
                            ? 'bg-rose-100 text-rose-700'
                            : alt.severity === 'ORANGE'
                              ? 'bg-amber-100 text-amber-700'
                              : 'bg-yellow-100 text-yellow-700'
                            }`}
                        >
                          {alt.severity}
                        </span>

                        <span className="text-[11px] font-mono text-slate-500">
                          {alt.status}
                        </span>
                      </div>

                      <h4 className="text-sm font-bold text-slate-900 tracking-tight">{alt.title}</h4>
                      <p className="text-xs text-slate-500 flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-sky-600" />
                        {alt.location_name}
                      </p>
                    </div>

                    <div className="text-right shrink-0">
                      <span className="text-[11px] font-mono text-slate-500 block">
                        {alt.created_at ? alt.created_at.split('T')[0] : 'Today'}
                      </span>
                      <span className="text-xs text-sky-600 font-semibold flex items-center gap-0.5 mt-2 justify-end">
                        Inspect <ChevronRight className="w-3.5 h-3.5" />
                      </span>
                    </div>
                  </div>
                </div>
              );
            })
          ) : (
            <div className="p-12 glass-panel rounded-2xl text-center text-slate-500 bg-white/80 border border-slate-200/80">
              No alerts match the selected hazard or severity criteria.
            </div>
          )}
        </div>

        {/* Right Column: Selected Alert Detailed Dossier */}
        <div className="space-y-4">
          {selectedAlert ? (
            <div className="glass-panel rounded-3xl p-6 space-y-4 border border-slate-200/80 bg-white/85 shadow-sm">
              <div>
                <span
                  className="text-xs font-bold uppercase tracking-wider"
                  style={{ color: hazardColors[selectedAlert.hazard_type] || '#0284C7' }}
                >
                  {selectedAlert.hazard_type} &bull; {selectedAlert.severity} PRIORITY
                </span>
                <h3 className="text-lg font-bold text-slate-900 mt-1 leading-snug">
                  {selectedAlert.title}
                </h3>
                <p className="text-xs text-slate-500 mt-1 flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-sky-600" />
                  {selectedAlert.location_name} ({selectedAlert.latitude.toFixed(2)}, {selectedAlert.longitude.toFixed(2)})
                </p>
              </div>

              <div className="p-3.5 rounded-2xl bg-slate-50/80 border border-slate-200/70 space-y-1">
                <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold">
                  Official Guidance & Instructions
                </span>
                <p className="text-xs text-slate-700 leading-relaxed font-medium">
                  {selectedAlert.guidance || 'Adhere strictly to civil protection instructions and local directives.'}
                </p>
              </div>

              <div className="space-y-1 text-xs text-slate-600">
                <div className="flex justify-between py-1 border-b border-slate-200/60">
                  <span>Source Feeds</span>
                  <span className="text-slate-900 font-medium">{selectedAlert.source}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-200/60">
                  <span>Confidence Score</span>
                  <span className="text-slate-900 font-mono font-semibold">{((selectedAlert.confidence_score || 0.7) * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between py-1">
                  <span>Current State</span>
                  <span className="text-sky-700 font-semibold">{selectedAlert.status}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-2 flex flex-col gap-2">
                <Link to={`/map?lat=${selectedAlert.latitude}&lon=${selectedAlert.longitude}&zoom=8`}>
                  <LiquidButton variant="secondary" size="sm" className="w-full" rightIcon={<Globe2 className="w-4 h-4" />}>
                    View on Live Map
                  </LiquidButton>
                </Link>

                {selectedAlert.status === 'ACTIVE' && (
                  <LiquidButton
                    variant="primary"
                    size="sm"
                    className="w-full"
                    onClick={handleAcknowledge}
                    isLoading={actionLoading}
                    leftIcon={<CheckCircle2 className="w-4 h-4" />}
                  >
                    Acknowledge Alert
                  </LiquidButton>
                )}

                {selectedAlert.status !== 'RESOLVED' && (
                  <LiquidButton
                    variant="ghost"
                    size="sm"
                    className="w-full text-slate-600 hover:text-slate-900"
                    onClick={() => setShowResolveModal(true)}
                  >
                    Resolve Alert
                  </LiquidButton>
                )}
              </div>

              {/* Statutory Disclaimer */}
              <p className="text-[10px] text-slate-400 italic border-t border-slate-200/60 pt-3">
                Automated advisory decision support. This does not supersede official civil protection directives.
              </p>
            </div>
          ) : (
            <div className="glass-panel rounded-3xl p-8 text-center text-slate-500 text-sm bg-white/80 border border-slate-200/80 shadow-sm">
              Select an alert from the list to view its complete operational dossier, metrics, and actions.
            </div>
          )}
        </div>
      </div>

      {/* Resolution Modal */}
      <GlassModal
        isOpen={showResolveModal}
        onClose={() => setShowResolveModal(false)}
        title="Resolve Active Alert"
        subtitle={`Closing alert: ${selectedAlert?.title}`}
        footer={
          <>
            <LiquidButton variant="ghost" size="sm" onClick={() => setShowResolveModal(false)}>
              Cancel
            </LiquidButton>
            <LiquidButton variant="primary" size="sm" onClick={handleResolve} isLoading={actionLoading}>
              Confirm Resolution
            </LiquidButton>
          </>
        }
      >
        <div className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-700 font-semibold mb-1">Incident Officer Name</label>
            <input
              type="text"
              value={operatorName}
              onChange={(e) => setOperatorName(e.target.value)}
              className="w-full p-2.5 rounded-xl bg-white border border-slate-300 text-slate-800 focus:outline-none focus:border-sky-500 shadow-sm"
            />
          </div>

          <div>
            <label className="block text-slate-700 font-semibold mb-1">Resolution Summary Notes</label>
            <textarea
              rows={3}
              value={resolutionNotes}
              onChange={(e) => setResolutionNotes(e.target.value)}
              placeholder="e.g. Flood discharge returned below critical thresholds; hazard cleared."
              className="w-full p-2.5 rounded-xl bg-white border border-slate-300 text-slate-800 focus:outline-none focus:border-sky-500 shadow-sm"
            />
          </div>
        </div>
      </GlassModal>
    </div>
  );
};

export default AlertManagementPage;
