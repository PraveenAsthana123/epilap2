// TabMeta.jsx — Standard Input/Process/Output/Visualization/Report (IPOVR) descriptor for
// every data-driven tab, so each UI states what it consumes, does, produces, shows, and reports.
import React, { useState } from 'react'

// Per-tab IPOVR metadata. Keyed by the App `view` key.
export const TAB_META = {
  opmodel: { title: 'Operating Model',
    input: 'enterprise_pipelines.csv, enterprise_stages.csv', process: 'map 40 stages to 7 pipelines + status',
    output: 'coverage %, per-pipeline stage list, prediction object', visualization: 'pipeline cards + status table',
    report: 'docs/enterprise-flow/00-operating-model.md' },
  pphases: { title: 'Primary Pipeline',
    input: 'phase_explorer.csv (primary)', process: 'per-phase input→process→output + governance',
    output: '10 phases with coverage score', visualization: 'stepper + I/P/O tables + gov strip',
    report: 'docs/enterprise-flow/pipeline-1-research-clinical-protocol.md' },
  sphases: { title: 'Secondary (EEG) Pipeline',
    input: 'phase_explorer.csv (secondary)', process: 'per-phase input→process→output + governance',
    output: '14 EEG phases with coverage score', visualization: 'stepper + I/P/O tables + gov strip',
    report: 'docs/analysis/secondary-eeg-full.md' },
  dataviz: { title: 'Data Visualization',
    input: 'eeg_before_after.csv, eeg_class_balance.csv, all CSVs', process: 'raw vs filtered, before/after SMOTE, histograms',
    output: 'signal overlays, balance cards, dataset gallery', visualization: 'SVG line/hist charts',
    report: 'docs/analysis/secondary-eeg-full.md' },
  survey: { title: 'Patient Survey',
    input: 'patient answers (consent-gated)', process: 'capture pain/questions by target clinician',
    output: 'hand-off notes (de-identified)', visualization: 'grouped answer tables',
    report: 'docs/governance/02-patient-consent-eula.md' },
  forms: { title: 'AI Forms',
    input: 'per-role field values', process: 'assemble model feature vector', output: 'captured role form',
    visualization: 'role cards + form fields', report: 'docs/primary-assessment/*question-bank.md' },
  dashboards: { title: 'Dashboards Index',
    input: 'role catalog', process: 'index dashboards/reports per role', output: 'catalog by role',
    visualization: 'role sections + kind pills', report: 'this catalog' },
  reports: { title: 'Reports',
    input: 'seizure/epilepsy type catalog', process: 'map type → severity + care category + pathway',
    output: 'summary report per type', visualization: 'filterable table + category cards',
    report: 'docs/scenarios/ + this tab' },
  monitoring: { title: 'Continuous Monitoring',
    input: 'phase_scorecard.csv + signals', process: 'watch drift/perf/security/fairness, per-role duties',
    output: 'health %, alert feed, per-role duties', visualization: 'alert cards + signal tables',
    report: 'docs/monitoring-observability.md' },
  kg: { title: 'Knowledge Graph',
    input: 'kg_nodes.csv, kg_edges.csv', process: 'render RDF graph + MCP/agent policy',
    output: 'node/edge graph, MCP + agent tables', visualization: 'interactive SVG graph',
    report: 'docs/enterprise-flow/mcp-multiagent-knowledge-graph.md' },
  sim: { title: 'Simulation',
    input: 'scenario + role', process: 'simulate per-role analysis flow', output: 'simulated run',
    visualization: 'flow + result cards', report: 'docs/scenarios/' },
  scenarios: { title: 'Scenarios',
    input: 'epilepsy_scenarios.csv', process: 'filter by category/severity', output: 'scenario cards',
    visualization: 'cards + severity pills', report: 'docs/scenarios/' },
  phases: { title: 'Phase Gates',
    input: 'phase_scorecard.csv', process: 'quality-gate each lifecycle phase', output: 'RAG scorecard',
    visualization: 'phase cards', report: 'docs/phase-gates-scorecard.md' },
  eeg: { title: 'EEG Waveform',
    input: 'eeg_snippet.csv (real CHB-MIT)', process: 'plot channels + seizure marker', output: 'waveform',
    visualization: 'multi-channel SVG', report: 'docs/analysis/chbmit-real-analysis.md' },
  data: { title: 'Data',
    input: '35 data/analysis CSVs', process: 'profile + preview each dataset', output: 'tables + profiles',
    visualization: 'data tables', report: 'docs/analysis/' },
}

const STEPS = [
  ['① Input', 'input', '#2563eb'], ['② Process', 'process', '#7c3aed'], ['③ Output', 'output', '#059669'],
  ['④ Visualization', 'visualization', '#d97706'], ['⑤ Report', 'report', '#db2777'],
]

// Collapsible IPOVR band shown at the top of every data-driven tab.
export default function IPOVR({ view }) {
  const meta = TAB_META[view]
  const [open, setOpen] = useState(false)
  if (!meta) return null
  return (
    <div style={{ borderBottom: '1px solid #e2e8f0', background: 'var(--panel,#f8fafc)' }}>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap', padding: '8px 20px' }}>
        <strong style={{ fontSize: 12, color: '#475569' }}>IPOVR:</strong>
        {STEPS.map(([label, key, color]) => (
          <span key={key} title={meta[key]} onClick={() => setOpen((o) => !o)}
                style={{ fontSize: 11, background: color, color: '#fff', padding: '2px 8px', borderRadius: 10, cursor: 'pointer' }}>
            {label}
          </span>
        ))}
        <button className="btn ghost" style={{ padding: '2px 8px', fontSize: 11 }} onClick={() => setOpen((o) => !o)}>{open ? 'hide' : 'details'}</button>
      </div>
      {open && (
        <div style={{ padding: '0 20px 10px', overflowX: 'auto' }}>
          <table className="dash" style={{ fontSize: 12 }}>
            <tbody>
              {STEPS.map(([label, key]) => (
                <tr key={key}><td style={{ fontWeight: 600, whiteSpace: 'nowrap' }}>{label}</td><td>{meta[key]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
