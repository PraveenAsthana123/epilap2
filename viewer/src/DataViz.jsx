// DataViz.jsx — Data section: visualize EVERY dataset BEFORE vs AFTER processing.
// Shows (1) real EEG raw-vs-filtered overlay, (2) class balance before/after SMOTE,
// (3) a gallery of all datasets (real + synthetic) with shape + a quick histogram.
import React, { useMemo, useState } from 'react'
import { parseCSV } from './csv.js'

// Simple inline SVG line chart overlaying two series.
function Overlay({ rows, xKey, aKey, bKey, aLabel, bLabel }) {
  const W = 860, H = 220, pad = 34
  const xs = rows.map((r) => Number(r[xKey]))
  const av = rows.map((r) => Number(r[aKey])), bv = rows.map((r) => Number(r[bKey]))
  const all = av.concat(bv)
  const mn = Math.min(...all), mx = Math.max(...all), rng = (mx - mn) || 1
  const x0 = Math.min(...xs), x1 = Math.max(...xs)
  const X = (v) => pad + ((v - x0) / ((x1 - x0) || 1)) * (W - pad - 8)
  const Y = (v) => H - pad - ((v - mn) / rng) * (H - pad - 12)
  const path = (vals) => vals.map((v, i) => `${X(xs[i]).toFixed(1)},${Y(v).toFixed(1)}`).join(' ')
  return (
    <div className="chartbox" style={{ maxWidth: '100%', overflowX: 'auto' }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%">
        <polyline points={path(av)} fill="none" stroke="#dc2626" strokeWidth="0.8" opacity="0.7" />
        <polyline points={path(bv)} fill="none" stroke="#4f46e5" strokeWidth="0.9" />
        <text x={pad} y="14" fontSize="11" fill="#dc2626">{aLabel}</text>
        <text x={pad + 120} y="14" fontSize="11" fill="#4f46e5">{bLabel}</text>
      </svg>
    </div>
  )
}

function Hist({ vals }) {
  const bins = 16
  const nums = vals.map(Number).filter((v) => Number.isFinite(v))
  if (nums.length < 3) return null
  const mn = Math.min(...nums), mx = Math.max(...nums), rng = (mx - mn) || 1
  const counts = new Array(bins).fill(0)
  nums.forEach((v) => { const i = Math.min(bins - 1, Math.floor(((v - mn) / rng) * bins)); counts[i]++ })
  const cmx = Math.max(...counts)
  return (
    <svg viewBox="0 0 160 44" width="160" height="44">
      {counts.map((c, i) => (
        <rect key={i} x={i * 10} y={44 - (c / cmx) * 40} width="9" height={(c / cmx) * 40} fill="#6366f1" />
      ))}
    </svg>
  )
}

export default function DataViz({ datasets }) {
  const ba = datasets.find((d) => d.name === 'eeg_before_after.csv')
  const bal = datasets.find((d) => d.name === 'eeg_class_balance.csv')
  const baP = useMemo(() => (ba ? parseCSV(ba.text) : null), [ba])
  const balP = useMemo(() => (bal ? parseCSV(bal.text) : null), [bal])
  const [sel, setSel] = useState(null)

  const gallery = useMemo(() => datasets.map((d) => {
    const p = parseCSV(d.text)
    const numCol = p.headers.find((h) => p.rows.slice(0, 20).every((r) => r[h] !== '' && Number.isFinite(Number(r[h]))))
    return { name: d.name, rows: p.rows.length, cols: p.headers.length, headers: p.headers, numCol, parsed: p,
             synthetic: /qbank|answers|cohort|scenario|fusion|primary/i.test(d.name) }
  }), [datasets])

  return (
    <main className="content home">
      <h1 className="home-h1">📊 Data Visualization — before vs after processing</h1>
      <p className="home-sub">
        Every dataset used in the platform, visualized. Real EEG (CHB-MIT) is shown <strong>raw vs filtered</strong>;
        the training set is shown <strong>before vs after SMOTE</strong> balancing. Synthetic cohorts are tagged.
      </p>

      {baP && baP.rows.length > 0 && (
        <section style={{ marginBottom: 22 }}>
          <h2 className="dash-h2">Real EEG — preprocessing (raw vs band-pass+notch+re-reference)</h2>
          <Overlay rows={baP.rows} xKey="t" aKey="raw_ch0" bKey="clean_ch0"
                   aLabel="raw µV" bLabel="preprocessed µV" />
          <div className="crumb">Channel 0 around the annotated seizure. Filtering removes drift + mains noise while preserving the ictal morphology.</div>
        </section>
      )}

      {balP && balP.rows.length > 0 && (
        <section style={{ marginBottom: 22 }}>
          <h2 className="dash-h2">Class balance — before vs after SMOTE</h2>
          <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(220px,1fr))' }}>
            {balP.rows.map((r) => (
              <div className="composite sev2" key={r.stage} style={{ margin: 0, minHeight: 88 }}>
                <div>
                  <div className="comp-label">{r.stage} · {r.method}</div>
                  <div className="comp-band" style={{ fontSize: 18 }}>ictal {r.ictal} / interictal {r.interictal}</div>
                  <div className="comp-sub">ratio {r.ratio}</div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      <h2 className="dash-h2">All datasets ({gallery.length})</h2>
      <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(240px,1fr))' }}>
        {gallery.map((g) => (
          <button className="card" key={g.name} onClick={() => setSel(sel === g.name ? null : g.name)}>
            <div className="card-title" style={{ fontSize: 13 }}>{g.name}</div>
            <div className="card-meta">{g.rows} rows · {g.cols} cols {g.synthetic ? '· synthetic' : '· real/derived'}</div>
            {g.numCol && <Hist vals={g.parsed.rows.map((r) => r[g.numCol])} />}
            {g.numCol && <div className="card-meta">hist: {g.numCol}</div>}
          </button>
        ))}
      </div>

      {sel && (() => {
        const g = gallery.find((x) => x.name === sel)
        return (
          <section style={{ marginTop: 18 }}>
            <h2 className="dash-h2">{sel} — first rows</h2>
            <div className="chartbox" style={{ overflowX: 'auto' }}>
              <table className="dash">
                <thead><tr>{g.headers.slice(0, 8).map((h) => <th key={h}>{h}</th>)}</tr></thead>
                <tbody>
                  {g.parsed.rows.slice(0, 8).map((r, i) => (
                    <tr key={i}>{g.headers.slice(0, 8).map((h) => <td key={h}>{r[h]}</td>)}</tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )
      })()}
    </main>
  )
}
