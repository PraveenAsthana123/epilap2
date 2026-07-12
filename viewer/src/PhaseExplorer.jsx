// PhaseExplorer.jsx — Per-phase detail for a pipeline (primary clinical | secondary EEG).
// For EVERY phase it shows, as TABLES: input · process · output, plus a governance strip
// (visualization · score · quality-check · score-check · trust · Governance/Responsible/Explainable AI).
// Data comes from data/analysis/phase_explorer.csv + phase_explorer_io.csv (python phase_io_export.py).
import React, { useMemo, useState } from 'react'
import { parseCSV } from './csv.js'

function IOTable({ title, rows, accent }) {
  return (
    <div style={{ flex: 1, minWidth: 240 }}>
      <div className="navlabel" style={{ color: accent }}>{title} data table</div>
      <table className="dash">
        <thead><tr><th>field</th><th>value</th></tr></thead>
        <tbody>
          {rows.length ? rows.map((r, i) => (
            <tr key={i}><td><strong>{r.field}</strong></td><td>{r.value}</td></tr>
          )) : <tr><td colSpan={2}>—</td></tr>}
        </tbody>
      </table>
    </div>
  )
}

function scoreCls(s) { const n = Number(s); return n >= 85 ? 'sev1' : n >= 70 ? 'sev2' : n >= 50 ? 'sev3' : 'sev4' }

export default function PhaseExplorer({ datasets, pipeline, title, icon }) {
  const metaDs = datasets.find((d) => d.name === 'phase_explorer.csv')
  const ioDs = datasets.find((d) => d.name === 'phase_explorer_io.csv')
  const meta = useMemo(() => (metaDs ? parseCSV(metaDs.text).rows : []).filter((r) => r.pipeline === pipeline)
    .sort((a, b) => Number(a.phase_no) - Number(b.phase_no)), [metaDs, pipeline])
  const io = useMemo(() => (ioDs ? parseCSV(ioDs.text).rows : []).filter((r) => r.pipeline === pipeline), [ioDs, pipeline])
  const [sel, setSel] = useState(0)

  if (!meta.length) return <div className="content"><div className="crumb">phase_explorer.csv not found — run analysis/phase_io_export.py</div></div>

  const p = meta[sel]
  const rowsFor = (t) => io.filter((r) => r.phase_no === p.phase_no && r.io === t)
  const avg = Math.round(meta.reduce((a, r) => a + Number(r.score || 0), 0) / meta.length)
  const gov = [
    ['🖼️ Visualization', p.visualization], ['✅ Quality check', p.quality_check],
    ['🎯 Score check', p.score_check], ['🔒 Trust', p.trust],
    ['🏛️ Governance AI', p.governance_ai], ['⚖️ Responsible AI', p.responsible_ai],
    ['💡 Explainable AI', p.explainable_ai],
  ]

  return (
    <main className="content home">
      <h1 className="home-h1">{icon} {title} — phase-by-phase detail</h1>
      <p className="home-sub">
        Every phase of the {pipeline} pipeline with its <strong>input → process → output</strong> tables plus
        visualization, score, quality &amp; score checks, trust, and Governance / Responsible / Explainable AI.
        Coverage score (mean): <strong>{avg}/100</strong> across {meta.length} phases.
      </p>

      {/* Phase stepper */}
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', margin: '0 0 16px' }}>
        {meta.map((m, i) => (
          <button key={m.phase_no} onClick={() => setSel(i)}
            className={'opt' + (i === sel ? ' sel ' + scoreCls(m.score) : '')}
            title={m.phase} style={{ fontSize: 12 }}>
            <b>{m.phase_no}</b> {m.phase}
          </button>
        ))}
      </div>

      {/* Selected phase header + score */}
      <div className={'scorecard ' + scoreCls(p.score)} style={{ marginBottom: 14 }}>
        <div className="sc-left">
          <div className="sc-answered">Phase {p.phase_no} of {meta.length}</div>
          <div className="sc-band">{p.phase}</div>
        </div>
        <div className="sc-num">{p.score}<span>/100</span></div>
      </div>

      {/* Input / Process / Output tables */}
      <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', marginBottom: 16 }}>
        <IOTable title="① Input" rows={rowsFor('input')} accent="#2563eb" />
        <IOTable title="② Process" rows={rowsFor('process')} accent="#7c3aed" />
        <IOTable title="③ Output" rows={rowsFor('output')} accent="#059669" />
      </div>

      {/* Governance / trust strip */}
      <div className="navlabel">Quality · Trust · Governance / Responsible / Explainable AI</div>
      <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(220px,1fr))' }}>
        {gov.map(([k, v]) => (
          <div className="composite sev2" key={k} style={{ margin: 0, minHeight: 74 }}>
            <div><div className="comp-label">{k}</div><div className="comp-sub" style={{ fontSize: 13 }}>{v}</div></div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: 10, marginTop: 16 }}>
        <button className="btn ghost" disabled={sel === 0} onClick={() => setSel((s) => Math.max(0, s - 1))}>← Prev phase</button>
        <button className="btn" disabled={sel === meta.length - 1} onClick={() => setSel((s) => Math.min(meta.length - 1, s + 1))}>Next phase →</button>
      </div>
    </main>
  )
}
