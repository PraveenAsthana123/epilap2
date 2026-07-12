// AIForms.jsx — AI Form section: the intake/assessment form for every role, with its
// questions. Selecting a role shows its form; fields are the AI model's input features.
import React, { useState } from 'react'

// Per-role assessment form. Each field feeds the primary/fusion model as an input feature.
const FORMS = {
  'Neurologist': ['Seizure type (focal/generalized/unknown)', 'Seizure frequency (per month)',
    'Age at onset', 'Aura present?', 'Duration (seconds)', 'Post-ictal state', 'MRI lesion?',
    'Prior status epilepticus?', 'Current ASMs', 'Response to first ASM'],
  'EEG Technician': ['Electrode montage (10-20)', 'Impedance (kΩ)', 'Sampling rate (Hz)',
    'Interictal spikes?', 'Focus lobe/channel', 'Photic response', 'Sleep-deprived?', 'Artefact level'],
  'Nurse': ['Vitals (BP/HR/SpO2)', 'Seizures observed this shift', 'Injury/tongue bite?',
    'Rescue medication given?', 'Fall risk', 'Care-plan adherence'],
  'Neuropsychologist': ['Memory score', 'Attention/processing speed', 'Mood (PHQ-style)',
    'Anxiety', 'Quality of life', 'Cognitive side effects'],
  'Pharmacist': ['ASM regimen', 'Serum drug level', 'Drug interactions', 'Adherence %',
    'Adverse effects', 'Renal/hepatic adjustment'],
  'Caregiver': ['Witnessed seizure count', 'Typical semiology', 'Night-time events?',
    'Home safety hazards', 'Caregiver burden', 'Emergency plan in place?'],
  'Patient': ['Self-reported seizures', 'Aura description', 'Triggers', 'Sleep quality',
    'Medication side effects', 'Main concern / question'],
  'Administrator': ['Registration complete?', 'Diagnosis coding (ICD)', 'Consent + IRB on file?',
    'Scheduling', 'Insurance/authorization', 'Data-governance flags'],
  'Occupational Therapist': ['ADL independence', 'IADL', 'Driving status', 'Return-to-work',
    'Home safety adaptations', 'Participation/roles'],
  'Radiologist': ['Modality (MRI/CT/PET)', 'Lesion present?', 'Location', 'Epileptogenic zone concordance',
    'Hippocampal sclerosis?', 'Recommendation'],
}
const ICONS = { Neurologist: '🧠', 'EEG Technician': '📈', Nurse: '🩺', Neuropsychologist: '🧩',
  Pharmacist: '💊', Caregiver: '🤝', Patient: '🧍', Administrator: '🗂️', 'Occupational Therapist': '🧰', Radiologist: '🩻' }

export default function AIForms() {
  const roles = Object.keys(FORMS)
  const [role, setRole] = useState(roles[0])
  const [vals, setVals] = useState({})
  const fields = FORMS[role]
  const done = fields.filter((f) => (vals[role]?.[f] || '').trim()).length
  const set = (f, v) => setVals((s) => ({ ...s, [role]: { ...(s[role] || {}), [f]: v } }))

  return (
    <main className="content home">
      <h1 className="home-h1">📝 AI Assessment Forms — all roles</h1>
      <p className="home-sub">
        Every role's intake/assessment form. Each field is an <strong>input feature</strong> for the AI
        severity/seizure model. Fill a form to see it captured ({done}/{fields.length} for {role}).
      </p>
      <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(140px,1fr))', marginBottom: 16 }}>
        {roles.map((r) => (
          <button key={r} className={'card' + (r === role ? ' active' : '')} onClick={() => setRole(r)}
                  style={r === role ? { outline: '2px solid #6366f1' } : {}}>
            <div className="card-icon">{ICONS[r]}</div>
            <div className="card-title" style={{ fontSize: 12 }}>{r}</div>
            <div className="card-meta">{FORMS[r].length} fields</div>
          </button>
        ))}
      </div>
      <h2 className="dash-h2">{ICONS[role]} {role} — assessment form</h2>
      {fields.map((f) => (
        <div className="q" key={f} style={{ display: 'block' }}>
          <div className="q-key" style={{ marginBottom: 6 }}>{f}</div>
          <input className="search" style={{ maxWidth: 480 }} value={vals[role]?.[f] || ''}
                 placeholder="Enter value…" onChange={(e) => set(f, e.target.value)} />
        </div>
      ))}
      <div className="crumb" style={{ marginTop: 12 }}>Captured values are the model's feature vector (de-identified, EP001). Consent required before submission.</div>
    </main>
  )
}
