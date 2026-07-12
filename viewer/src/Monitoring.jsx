// Monitoring.jsx — Continuous Monitoring section: what must be monitored continuously across
// the platform and by each role — updates, notifications, alerts, tracking, reports. Includes
// a live-style alert feed and per-role monitoring responsibilities.
import React, { useMemo } from 'react'
import { parseCSV } from './csv.js'

// What is monitored continuously, by signal type. Thresholds are illustrative.
const SIGNALS = [
  { area: 'Model performance', metric: 'AUC / accuracy vs baseline', trigger: 'AUC drops >5%', action: 'alert + retrain', cadence: 'per batch' },
  { area: 'Data drift', metric: 'KS test on feature distributions', trigger: 'p<0.01 shift', action: 'notify data owner', cadence: 'daily' },
  { area: 'Concept drift', metric: 'label/prediction agreement over time', trigger: 'agreement falls', action: 'champion-challenger', cadence: 'weekly' },
  { area: 'Data quality', metric: 'nulls / range / schema', trigger: 'contract breach', action: 'block + alert', cadence: 'on ingest' },
  { area: 'EEG signal quality', metric: 'impedance / artefact ratio', trigger: 'artefact >20%', action: 'flag recording', cadence: 'per recording' },
  { area: 'API/system', metric: 'latency / error rate / CPU / memory', trigger: 'p95>1s or 5xx', action: 'page on-call', cadence: 'real-time' },
  { area: 'Security', metric: 'auth failures / anomalous access', trigger: 'spike / off-hours', action: 'lock + investigate', cadence: 'real-time' },
  { area: 'Fairness', metric: 'subgroup performance gap', trigger: 'gap >10%', action: 'bias review', cadence: 'monthly' },
  { area: 'Audit/logging', metric: 'append-only log integrity', trigger: 'gap/tamper', action: 'incident', cadence: 'continuous' },
]

// Per-role continuous-monitoring responsibilities: update / notify / alert / track / report.
const ROLE_MON = [
  { role: '🧠 Neurologist', update: 'review flagged seizures', notify: 'new high-risk EEG', alert: 'status epilepticus', track: 'seizure trend', report: 'weekly severity' },
  { role: '📈 EEG Technician', update: 're-check impedance', notify: 'poor signal quality', alert: 'electrode fault', track: 'artefact rate', report: 'recording QC' },
  { role: '🩺 Nurse', update: 'log observed seizures', notify: 'missed medication', alert: 'seizure cluster', track: 'vitals', report: 'shift summary' },
  { role: '💊 Pharmacist', update: 'reconcile ASMs', notify: 'interaction/level', alert: 'toxic drug level', track: 'adherence', report: 'medication review' },
  { role: '🤝 Caregiver', update: 'home diary entry', notify: 'reminder to log', alert: 'emergency event', track: 'night events', report: 'home summary' },
  { role: '🧍 Patient', update: 'self-report', notify: 'appointment/med reminder', alert: 'call-for-help (SOS)', track: 'symptoms', report: 'my trend' },
  { role: '🗂️ Administrator', update: 'governance status', notify: 'consent/IRB expiry', alert: 'compliance/security', track: 'phase gates', report: 'audit/compliance' },
]

function Bar({ pct, cls }) {
  return <div style={{ height: 8, background: '#e5e7eb', borderRadius: 4, overflow: 'hidden' }}>
    <div className={cls} style={{ height: '100%', width: pct + '%' }} /></div>
}

export default function Monitoring({ datasets }) {
  // Reuse the phase scorecard (if present) to show a live health strip.
  const sc = datasets.find((d) => d.name === 'phase_scorecard.csv')
  const scRows = useMemo(() => (sc ? parseCSV(sc.text).rows : []), [sc])
  const overall = scRows.length ? Math.round(scRows.reduce((a, r) => a + Number(r.score || 0), 0) / scRows.length) : null

  // Deterministic sample alert feed (illustrative of the live stream).
  const feed = [
    { t: 'now', sev: 'info', msg: 'Batch scored — AUC 0.92, within tolerance' },
    { t: '4m', sev: 'warn', msg: 'Data drift: gamma band KS p=0.03 (watch)' },
    { t: '18m', sev: 'info', msg: 'EEG QC passed for EP001 recording' },
    { t: '1h', sev: 'crit', msg: 'Security: 3 auth failures from new IP — locked' },
    { t: '3h', sev: 'info', msg: 'Weekly fairness check: max subgroup gap 4% (ok)' },
  ]
  const SEVCLS = { info: 'sev1', warn: 'sev2', crit: 'sev4' }

  return (
    <main className="content home">
      <h1 className="home-h1">📡 Continuous Monitoring</h1>
      <p className="home-sub">
        What runs continuously to keep the platform safe and accurate: updates, notifications, alerts,
        tracking, and reports — across the system and per role. Model drift, concept drift, data quality,
        security, and fairness are all watched.
      </p>

      {overall != null && (
        <div className={'composite ' + (overall >= 90 ? 'sev1' : overall >= 70 ? 'sev2' : 'sev4')} style={{ marginBottom: 18 }}>
          <div><div className="comp-label">Platform health (phase-gate mean)</div>
            <div className="comp-band">{overall >= 90 ? 'Healthy' : overall >= 70 ? 'Watch' : 'Action'}</div>
            <div className="comp-sub">{scRows.length} phases monitored</div></div>
          <div className="comp-num">{overall}<span>/100</span></div>
        </div>
      )}

      <h2 className="dash-h2">Live alert feed</h2>
      <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(280px,1fr))', marginBottom: 20 }}>
        {feed.map((f, i) => (
          <div className={'composite ' + SEVCLS[f.sev]} key={i} style={{ margin: 0, minHeight: 64 }}>
            <div><div className="comp-label">{f.sev.toUpperCase()} · {f.t}</div>
              <div className="comp-sub" style={{ fontSize: 13 }}>{f.msg}</div></div>
          </div>
        ))}
      </div>

      <h2 className="dash-h2">What is monitored continuously</h2>
      <div className="chartbox" style={{ overflowX: 'auto' }}>
        <table className="dash">
          <thead><tr><th>Area</th><th>Metric</th><th>Trigger</th><th>Action</th><th>Cadence</th></tr></thead>
          <tbody>{SIGNALS.map((s) => (
            <tr key={s.area}><td><strong>{s.area}</strong></td><td>{s.metric}</td><td>{s.trigger}</td><td>{s.action}</td><td>{s.cadence}</td></tr>
          ))}</tbody>
        </table>
      </div>

      <h2 className="dash-h2" style={{ marginTop: 18 }}>Per-role monitoring — update · notify · alert · track · report</h2>
      <div className="chartbox" style={{ overflowX: 'auto' }}>
        <table className="dash">
          <thead><tr><th>Role</th><th>Update</th><th>Notification</th><th>Alert</th><th>Tracking</th><th>Report</th></tr></thead>
          <tbody>{ROLE_MON.map((r) => (
            <tr key={r.role}><td>{r.role}</td><td>{r.update}</td><td>{r.notify}</td><td>{r.alert}</td><td>{r.track}</td><td>{r.report}</td></tr>
          ))}</tbody>
        </table>
      </div>
      <div className="crumb" style={{ marginTop: 12 }}>Alerts route to the responsible role; critical alerts page on-call and are audit-logged.</div>
    </main>
  )
}
