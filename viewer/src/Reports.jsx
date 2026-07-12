// Reports.jsx — Report section: summary report per epilepsy / seizure type, with the
// severity band, care category, key EEG signature, and recommended pathway. Filterable.
import React, { useMemo, useState } from 'react'

const SEVCLS = { 1: 'sev1', 2: 'sev2', 3: 'sev3', 4: 'sev4' }

// One summary report per seizure/epilepsy type (ILAE-aligned), mapped to the 4-level model
// and the care category (No-Disease / Basic-Mild / Moderate / Severe / Surgical).
const REPORTS = [
  { type: 'No epileptiform findings', cat: 'No-Disease', sev: 1, onset: '—',
    eeg: 'Normal background, no spikes', path: 'Reassure, review if events recur' },
  { type: 'Focal aware (simple partial)', cat: 'Basic-Mild', sev: 1, onset: 'Focal',
    eeg: 'Focal interictal spikes', path: 'First ASM (e.g., lamotrigine), seizure diary' },
  { type: 'Focal impaired awareness', cat: 'Moderate', sev: 2, onset: 'Focal',
    eeg: 'Temporal/frontal focal discharges', path: 'ASM optimization, MRI, neuropsych' },
  { type: 'Childhood absence', cat: 'Basic-Mild', sev: 2, onset: 'Generalized',
    eeg: '3 Hz spike-and-wave', path: 'Ethosuximide/valproate, avoid triggers' },
  { type: 'Juvenile myoclonic', cat: 'Moderate', sev: 2, onset: 'Generalized',
    eeg: '4–6 Hz polyspike-wave', path: 'Valproate/levetiracetam, sleep hygiene' },
  { type: 'Generalized tonic-clonic', cat: 'Moderate', sev: 3, onset: 'Generalized',
    eeg: 'Generalized polyspikes, ictal buildup', path: 'ASM, safety plan, driving counselling' },
  { type: 'Focal to bilateral tonic-clonic', cat: 'Severe', sev: 3, onset: 'Focal→bilateral',
    eeg: 'Focal onset with secondary generalization', path: 'MRI + video-EEG, surgical workup if refractory' },
  { type: 'Drug-resistant focal', cat: 'Surgical', sev: 4, onset: 'Focal',
    eeg: 'Consistent focal ictal onset zone', path: 'Pre-surgical evaluation, SEEG, resection/laser' },
  { type: 'Lennox-Gastaut', cat: 'Surgical', sev: 4, onset: 'Generalized',
    eeg: 'Slow spike-wave <2.5 Hz, paroxysmal fast', path: 'Multi-ASM, dietary, VNS/callosotomy' },
  { type: 'Status epilepticus', cat: 'Severe', sev: 4, onset: 'Any',
    eeg: 'Continuous/recurrent ictal activity', path: 'Emergency benzodiazepine + ICU protocol' },
]

export default function Reports() {
  const [cat, setCat] = useState('All')
  const cats = ['All', ...Array.from(new Set(REPORTS.map((r) => r.cat)))]
  const rows = useMemo(() => REPORTS.filter((r) => cat === 'All' || r.cat === cat), [cat])
  const counts = cats.slice(1).map((c) => ({ c, n: REPORTS.filter((r) => r.cat === c).length }))

  return (
    <main className="content home">
      <h1 className="home-h1">📄 Summary Reports — by epilepsy / seizure type</h1>
      <p className="home-sub">
        One summary report per seizure/epilepsy type, mapped to the 4-level severity model and the care
        category (No-Disease → Surgical), with the EEG signature and recommended pathway.
      </p>
      <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(150px,1fr))', marginBottom: 16 }}>
        {counts.map((x) => (
          <div className="composite sev2" key={x.c} style={{ margin: 0, minHeight: 70 }}>
            <div><div className="comp-label">{x.c}</div><div className="comp-band" style={{ fontSize: 16 }}>{x.n} types</div></div>
          </div>
        ))}
      </div>
      <select className="search" style={{ maxWidth: 240, marginBottom: 14 }} value={cat} onChange={(e) => setCat(e.target.value)}>
        {cats.map((c) => <option key={c}>{c}</option>)}
      </select>
      <div className="chartbox" style={{ overflowX: 'auto' }}>
        <table className="dash">
          <thead><tr><th>Type</th><th>Onset</th><th>EEG signature</th><th>Care category</th><th>Severity</th><th>Recommended pathway</th></tr></thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.type}>
                <td><strong>{r.type}</strong></td>
                <td>{r.onset}</td>
                <td>{r.eeg}</td>
                <td>{r.cat}</td>
                <td><span className={'pill ' + SEVCLS[r.sev]}>L{r.sev}</span></td>
                <td>{r.path}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="crumb" style={{ marginTop: 12 }}>Decision-support only — every report is confirmed by a neurologist. ILAE 2017 classification.</div>
    </main>
  )
}
