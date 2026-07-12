// Scenarios.jsx — browse the 57 seizure/epilepsy scenarios with category + severity filters.
import React, { useMemo, useState } from 'react'
import { parseCSV } from './csv.js'

const SEVCLS = { '1': 'sev1', '2': 'sev2', '3': 'sev3', '4': 'sev4' }

export default function Scenarios({ datasets }) {
  const ds = datasets.find((x) => x.name === 'epilepsy_scenarios.csv')
  const { rows } = useMemo(() => (ds ? parseCSV(ds.text) : { rows: [] }), [ds])
  const [cat, setCat] = useState('All')
  const [q, setQ] = useState('')
  if (!rows.length) return <div className="content"><div className="crumb">epilepsy_scenarios.csv not found — run analysis/build_scenarios.py</div></div>

  const cats = ['All', ...Array.from(new Set(rows.map((r) => r.category)))]
  const filtered = rows.filter((r) =>
    (cat === 'All' || r.category === cat) &&
    (!q || (r.scenario + r.key_features).toLowerCase().includes(q.toLowerCase())))

  return (
    <main className="content home">
      <h1 className="home-h1">Seizure & Epilepsy Scenarios ({rows.length})</h1>
      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', margin: '0 0 16px' }}>
        <select className="search" style={{ maxWidth: 240 }} value={cat} onChange={(e) => setCat(e.target.value)}>
          {cats.map((c) => <option key={c}>{c}</option>)}
        </select>
        <input className="search" style={{ maxWidth: 280 }} placeholder="Search scenarios…" value={q} onChange={(e) => setQ(e.target.value)} />
        <span className="sc-hint">{filtered.length} shown</span>
      </div>
      <div className="cards">
        {filtered.map((r) => (
          <div className="card" key={r.id}>
            <div className="card-foot" style={{ marginBottom: 8 }}>
              <span className="card-meta">{r.id}</span>
              <span className={'pill ' + (SEVCLS[r.severity_level] || 'sevnone')}>L{r.severity_level}</span>
            </div>
            <div className="card-title" style={{ fontSize: 14 }}>{r.scenario}</div>
            <div className="card-blurb">{r.key_features}</div>
            <div className="card-meta">{r.category} · {r.onset} · w={r.clinical_weight}</div>
          </div>
        ))}
      </div>
    </main>
  )
}
