// Simulation.jsx — patient picker over the 60 filled records; shows answers + predicted category.
import React, { useMemo, useState } from 'react'
import { parseCSV } from './csv.js'

const CARE_CLS = { 'No-Disease': 'sev1', 'Basic-Mild': 'sev1', Moderate: 'sev2', Severe: 'sev3', Surgical: 'sev4' }

function find(datasets, name) {
  const d = datasets.find((x) => x.name === name)
  return d ? parseCSV(d.text) : { headers: [], rows: [] }
}

export default function Simulation({ datasets }) {
  const neuro = useMemo(() => find(datasets, 'neurologist_answers.csv'), [datasets])
  const eeg = useMemo(() => find(datasets, 'eeg_technician_answers.csv'), [datasets])
  const ids = neuro.rows.map((r) => r.patient_id)
  const [pid, setPid] = useState(ids[0])
  if (!ids.length) return <div className="content"><div className="crumb">neurologist_answers.csv not found — run analysis/generate_qbank_dataset.py</div></div>

  const n = neuro.rows.find((r) => r.patient_id === pid) || neuro.rows[0]
  const e = eeg.rows.find((r) => r.patient_id === pid) || {}
  const nq = neuro.headers.filter((h) => !['patient_id', 'seizure_type', 'epilepsy_type', 'care_category'].includes(h))
  const eegKeys = ['montage', 'n_channels', 'band_delta', 'band_theta', 'band_alpha', 'band_beta', 'band_gamma',
    'peak_alpha_hz', 'spike_rate_pm', 'focus_lobe', 'focus_channel']

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">Simulation<small>60 filled patient records → predicted category</small></div>
        <div className="navlabel">Patients ({ids.length})</div>
        <div style={{ maxHeight: '70vh', overflowY: 'auto' }}>
          {neuro.rows.map((r) => (
            <button key={r.patient_id} className={'navitem' + (r.patient_id === pid ? ' active' : '')}
                    onClick={() => setPid(r.patient_id)}>
              {r.patient_id} <span className={'dot ' + (CARE_CLS[r.care_category] || '')} />
            </button>
          ))}
        </div>
      </aside>
      <main className="content">
        <div className="crumb">Simulation · {pid}</div>
        <h1 className="md-inline-h1">Patient {pid}</h1>

        <div className="cards" style={{ gridTemplateColumns: 'repeat(3,1fr)', marginBottom: 18 }}>
          <div className={'composite ' + (CARE_CLS[n.care_category] || 'sev2')} style={{ margin: 0 }}>
            <div><div className="comp-label">Care category</div><div className="comp-band">{n.care_category}</div></div>
          </div>
          <div className="card"><div className="card-title">Epilepsy type</div><div className="card-meta">{n.epilepsy_type}</div></div>
          <div className="card"><div className="card-title">Seizure type</div><div className="card-meta">{n.seizure_type}</div></div>
        </div>

        <h2 className="dash-h2">Neurologist answers</h2>
        <table className="dash"><tbody>
          {nq.map((h) => (<tr key={h}><td style={{ width: '55%' }}>{h}</td><td><b>{n[h]}</b></td></tr>))}
        </tbody></table>

        <h2 className="dash-h2">EEG technologist — quantitative</h2>
        <table className="dash"><tbody>
          {eegKeys.map((k) => (<tr key={k}><td>{k}</td><td><b>{e[k]}</b></td></tr>))}
        </tbody></table>
      </main>
    </div>
  )
}
