// EEGWaveform.jsx — plot the REAL EEG snippet (CHB-MIT, around the seizure at 2996s).
import React, { useMemo } from 'react'
import { parseCSV } from './csv.js'

export default function EEGWaveform({ datasets }) {
  const ds = datasets.find((x) => x.name === 'eeg_snippet.csv')
  const parsed = useMemo(() => (ds ? parseCSV(ds.text) : { headers: [], rows: [] }), [ds])
  if (!parsed.rows.length) return <div className="content"><div className="crumb">eeg_snippet.csv not found — export from analysis/chbmit_analysis.py</div></div>

  const chans = parsed.headers.filter((h) => h !== 't')
  const rows = parsed.rows
  const t0 = Number(rows[0].t), t1 = Number(rows[rows.length - 1].t)
  const W = 900, rowH = 90, pad = 46
  const H = chans.length * rowH + 30
  const x = (t) => pad + ((t - t0) / (t1 - t0)) * (W - pad - 10)
  const seizureX = x(2996)

  return (
    <main className="content">
      <div className="crumb">Real EEG · CHB-MIT chb01_03 · {t0.toFixed(0)}–{t1.toFixed(0)}s</div>
      <h1 className="home-h1">Real EEG waveform (around seizure @ 2996s)</h1>
      <p className="home-sub">Genuine pediatric epilepsy EEG (PhysioNet). The red line marks the annotated seizure onset; note the amplitude/frequency change after it.</p>
      <div className="chartbox" style={{ maxWidth: '100%', overflowX: 'auto' }}>
        <svg viewBox={`0 0 ${W} ${H}`} width="100%">
          {chans.map((ch, ci) => {
            const vals = rows.map((r) => Number(r[ch]))
            const mn = Math.min(...vals), mx = Math.max(...vals), rng = (mx - mn) || 1
            const yBase = 20 + ci * rowH + rowH / 2
            const pts = rows.map((r, i) => {
              const px = x(Number(r.t))
              const py = yBase - ((Number(r[ch]) - (mn + mx) / 2) / rng) * (rowH * 0.8)
              return `${px.toFixed(1)},${py.toFixed(1)}`
            }).join(' ')
            return (
              <g key={ch}>
                <text x="4" y={yBase - rowH / 2 + 12} fontSize="10" fill="currentColor">{ch}</text>
                <polyline points={pts} fill="none" stroke="#4f46e5" strokeWidth="0.6" />
              </g>
            )
          })}
          <line x1={seizureX} y1="10" x2={seizureX} y2={H - 6} stroke="#dc2626" strokeWidth="1.2" />
          <text x={seizureX + 3} y="16" fontSize="10" fill="#dc2626">seizure 2996s</text>
        </svg>
      </div>
    </main>
  )
}
