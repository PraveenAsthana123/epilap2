// PhaseDashboard.jsx — RAG dashboard of the 13 model-lifecycle phase gates.
import React, { useMemo } from 'react'
import { parseCSV } from './csv.js'

const CLS = { Green: 'sev1', Amber: 'sev2', Red: 'sev4' }

export default function PhaseDashboard({ datasets }) {
  const ds = datasets.find((x) => x.name === 'phase_scorecard.csv')
  const { rows } = useMemo(() => (ds ? parseCSV(ds.text) : { rows: [] }), [ds])
  if (!rows.length) return <div className="content"><div className="crumb">phase_scorecard.csv not found — run mlops/phase_gates.py</div></div>

  const overall = Math.round(rows.reduce((a, r) => a + Number(r.score), 0) / rows.length)
  return (
    <main className="content">
      <div className="crumb">Model lifecycle · phase gates</div>
      <h1 className="home-h1">Phase-Gate Dashboard — {overall}/100</h1>
      <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(210px,1fr))' }}>
        {rows.map((r) => (
          <div className={'composite ' + (CLS[r.status] || 'sev2')} key={r.phase} style={{ margin: 0, minHeight: 96 }}>
            <div>
              <div className="comp-label">{r.phase}</div>
              <div className="comp-band" style={{ fontSize: 20 }}>{r.status}</div>
              <div className="comp-sub">{r.quality_checks} checks · {r.monitoring}</div>
            </div>
            <div className="comp-num" style={{ fontSize: 30 }}>{r.score}</div>
          </div>
        ))}
      </div>
    </main>
  )
}
