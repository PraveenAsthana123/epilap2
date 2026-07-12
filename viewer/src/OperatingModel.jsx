// OperatingModel.jsx — Enterprise operating model: 7 connected pipelines, the 40-stage
// architecture (with implementation status), and the governed prediction-output object.
// Data: enterprise_pipelines.csv, enterprise_stages.csv, prediction_output_example.csv.
import React, { useMemo, useState } from 'react'
import { parseCSV } from './csv.js'

const STATUSCLS = { done: 'sev1', partial: 'sev2', gap: 'sev4' }
const STATUSLBL = { done: '✅ code', partial: '⚠️ partial', gap: '❌ documented' }

export default function OperatingModel({ datasets }) {
  const get = (n) => { const d = datasets.find((x) => x.name === n); return d ? parseCSV(d.text).rows : [] }
  const pipelines = useMemo(() => get('enterprise_pipelines.csv'), [datasets])
  const stages = useMemo(() => get('enterprise_stages.csv'), [datasets])
  const pred = useMemo(() => get('prediction_output_example.csv'), [datasets])
  const [filter, setFilter] = useState('All')

  if (!pipelines.length) return <div className="content"><div className="crumb">enterprise_pipelines.csv not found — run analysis/enterprise_flow_export.py</div></div>

  const counts = { done: 0, partial: 0, gap: 0 }
  stages.forEach((s) => { counts[s.status] = (counts[s.status] || 0) + 1 })
  const pct = Math.round((counts.done / stages.length) * 100)
  const shown = stages.filter((s) => filter === 'All' || s.pipeline === filter)

  return (
    <main className="content home">
      <h1 className="home-h1">🏛️ Enterprise Operating Model — 7 Pipelines · 40 Stages</h1>
      <p className="home-sub">
        The platform as seven owned, connected pipelines (research → data eng → features → modelling →
        MLOps → RAG/agents → safety). {counts.done} stages in code, {counts.partial} partial, {counts.gap} documented-design.
      </p>

      <div className={'composite ' + (pct >= 70 ? 'sev1' : 'sev2')} style={{ marginBottom: 18 }}>
        <div><div className="comp-label">Implementation coverage (stages in code)</div>
          <div className="comp-band">{counts.done}/{stages.length} stages</div>
          <div className="comp-sub">{counts.partial} partial · {counts.gap} documented</div></div>
        <div className="comp-num">{pct}<span>%</span></div>
      </div>

      <h2 className="dash-h2">The seven pipelines</h2>
      <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(280px,1fr))' }}>
        {pipelines.map((p) => (
          <button className={'card' + (filter === p.id ? ' active' : '')} key={p.id}
                  onClick={() => setFilter(filter === p.id ? 'All' : p.id)}
                  style={filter === p.id ? { outline: '2px solid #6366f1' } : {}}>
            <div className="card-foot" style={{ marginBottom: 6 }}><span className="pill sev2">{p.id}</span></div>
            <div className="card-title" style={{ fontSize: 14 }}>{p.pipeline}</div>
            <div className="card-blurb">{p.question}</div>
            <div className="card-meta">Owner: {p.owner}</div>
            <div className="card-meta">{p.artefacts}</div>
          </button>
        ))}
      </div>

      <h2 className="dash-h2" style={{ marginTop: 18 }}>
        40-stage architecture {filter !== 'All' && `— ${filter} only`}
        {filter !== 'All' && <button className="btn ghost" style={{ marginLeft: 10 }} onClick={() => setFilter('All')}>show all</button>}
      </h2>
      <div className="chartbox" style={{ overflowX: 'auto' }}>
        <table className="dash">
          <thead><tr><th>#</th><th>Stage</th><th>Pipeline</th><th>Status</th><th>Evidence / gap</th></tr></thead>
          <tbody>
            {shown.map((s) => (
              <tr key={s.stage_no}>
                <td>{s.stage_no}</td><td>{s.stage}</td><td>{s.pipeline}</td>
                <td><span className={'pill ' + (STATUSCLS[s.status] || 'sevnone')}>{STATUSLBL[s.status] || s.status}</span></td>
                <td>{s.evidence}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {pred.length > 0 && (
        <>
          <h2 className="dash-h2" style={{ marginTop: 18 }}>Governed prediction object (example — EP001)</h2>
          <p className="crumb">Every prediction carries provenance, calibration, uncertainty, explanation, fairness, evidence, and a safety gate — not just a risk score.</p>
          <div className="chartbox" style={{ overflowX: 'auto' }}>
            <table className="dash">
              <thead><tr><th>field</th><th>value</th></tr></thead>
              <tbody>{pred.map((r) => <tr key={r.field}><td><strong>{r.field}</strong></td><td>{r.value}</td></tr>)}</tbody>
            </table>
          </div>
        </>
      )}
    </main>
  )
}
