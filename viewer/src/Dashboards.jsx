// Dashboards.jsx — Dashboard section: a catalog of every dashboard + report available to
// each role, with where to find it. Data-driven so it stays in sync as tabs are added.
import React from 'react'

// Per-role catalog of dashboards and reports. `where` names the tab/portal that hosts it.
const CATALOG = [
  { role: '🧠 Neurologist', items: [
    { kind: 'Dashboard', name: 'Severity Dashboard (role + composite)', where: 'Neurologist portal → Severity Dashboard' },
    { kind: 'Dashboard', name: 'Model metrics (accuracy matrix)', where: 'Phases / Data tab (eeg_model_metrics.csv)' },
    { kind: 'Report', name: 'Seizure-type summary reports', where: 'Reports tab' },
    { kind: 'Report', name: 'EEG→AI→RAG generated report', where: 'docs/analysis/secondary-eeg-full.md' } ] },
  { role: '📈 EEG Technician', items: [
    { kind: 'Dashboard', name: 'Signal-quality / before-after', where: 'Data Viz tab' },
    { kind: 'Dashboard', name: 'Real EEG waveform + seizure marker', where: 'EEG tab' },
    { kind: 'Report', name: 'Time-frequency + 2D image set', where: 'docs/analysis/secondary-eeg-full.md' } ] },
  { role: '🩺 Nurse', items: [
    { kind: 'Dashboard', name: 'Severity + observation dashboard', where: 'Nurse portal' },
    { kind: 'Report', name: 'Seizure observation summary', where: 'Reports tab' } ] },
  { role: '💊 Pharmacist', items: [
    { kind: 'Dashboard', name: 'ASM regimen / adherence dashboard', where: 'Pharmacist portal' },
    { kind: 'Report', name: 'Drug-level & interaction report', where: 'Reports tab' } ] },
  { role: '🧩 Neuropsychologist', items: [
    { kind: 'Dashboard', name: 'Cognition / mood dashboard', where: 'Neuropsychologist portal' } ] },
  { role: '🤝 Caregiver', items: [
    { kind: 'Dashboard', name: 'Home seizure diary dashboard', where: 'Caregiver portal' },
    { kind: 'Report', name: 'Caregiver burden summary', where: 'Reports tab' } ] },
  { role: '🧍 Patient', items: [
    { kind: 'Form', name: 'Patient survey (pain / questions)', where: 'Survey tab' },
    { kind: 'Dashboard', name: 'My severity + trend', where: 'Patient portal' } ] },
  { role: '🗂️ Administrator', items: [
    { kind: 'Dashboard', name: 'Phase-gate governance dashboard', where: 'Phases tab' },
    { kind: 'Dashboard', name: 'Continuous monitoring board', where: 'Monitoring tab' },
    { kind: 'Report', name: 'Audit / compliance report', where: 'docs/governance/' } ] },
  { role: '🧰 Occupational Therapist', items: [
    { kind: 'Dashboard', name: 'Function / ADL dashboard', where: 'Occupational Therapist portal' } ] },
  { role: '🩻 Radiologist', items: [
    { kind: 'Dashboard', name: 'Imaging / localization dashboard', where: 'Radiologist portal' } ] },
]

const KINDCLS = { Dashboard: 'sev2', Report: 'sev1', Form: 'sev3' }

export default function Dashboards() {
  const totals = CATALOG.reduce((a, r) => a + r.items.length, 0)
  return (
    <main className="content home">
      <h1 className="home-h1">🧭 Dashboards &amp; Reports — by role</h1>
      <p className="home-sub">
        Every dashboard, report, and form in the platform, indexed by the role that owns it
        ({totals} items across {CATALOG.length} roles). Each entry names where to open it.
      </p>
      {CATALOG.map((r) => (
        <section key={r.role} style={{ marginBottom: 16 }}>
          <h2 className="dash-h2">{r.role}</h2>
          <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(260px,1fr))' }}>
            {r.items.map((it) => (
              <div className="card" key={it.name}>
                <div className="card-foot" style={{ marginBottom: 6 }}>
                  <span className={'pill ' + (KINDCLS[it.kind] || 'sevnone')}>{it.kind}</span>
                </div>
                <div className="card-title" style={{ fontSize: 14 }}>{it.name}</div>
                <div className="card-meta">{it.where}</div>
              </div>
            ))}
          </div>
        </section>
      ))}
    </main>
  )
}
