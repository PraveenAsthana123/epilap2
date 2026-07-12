// Survey.jsx — Patient survey: capture the patient's pain points / questions for the
// Neurologist and EEG Technician. Consent-gated (per governance policy), then a structured
// questionnaire whose answers are summarised into a hand-off note for each clinician.
import React, { useState } from 'react'

// Questions the patient answers, tagged by the clinician who needs the answer.
const QUESTIONS = [
  { id: 'seizure_freq', to: 'Neurologist', q: 'How often are you having seizures now?', type: 'choice',
    opts: ['None', 'Less than monthly', 'Weekly', 'Daily or more'] },
  { id: 'aura', to: 'Neurologist', q: 'Do you get a warning (aura) before a seizure?', type: 'choice',
    opts: ['No', 'Sometimes', 'Always'] },
  { id: 'triggers', to: 'Neurologist', q: 'What seems to trigger your seizures?', type: 'text' },
  { id: 'meds', to: 'Neurologist', q: 'Are you having side effects from your medication?', type: 'choice',
    opts: ['None', 'Mild', 'Bothersome', 'Severe'] },
  { id: 'mood', to: 'Neurologist', q: 'How has your mood / memory been?', type: 'text' },
  { id: 'concerns', to: 'Neurologist', q: 'Your main question for the neurologist:', type: 'text' },
  { id: 'scalp', to: 'EEG Technician', q: 'Any scalp sensitivity, cuts, or hair products today?', type: 'text' },
  { id: 'sleep', to: 'EEG Technician', q: 'How much did you sleep before this EEG?', type: 'choice',
    opts: ['Normal', 'Sleep-deprived on purpose', 'Poor sleep'] },
  { id: 'comfort', to: 'EEG Technician', q: 'Anything that would make the recording more comfortable?', type: 'text' },
  { id: 'eeg_q', to: 'EEG Technician', q: 'Your question for the EEG technician:', type: 'text' },
]

export default function Survey() {
  const [consent, setConsent] = useState(false)
  const [ans, setAns] = useState({})
  const [submitted, setSubmitted] = useState(false)
  const set = (id, v) => setAns((a) => ({ ...a, [id]: v }))
  const answered = Object.values(ans).filter((v) => v && String(v).trim()).length

  if (!consent) {
    return (
      <main className="content home">
        <h1 className="home-h1">🗣️ Patient Survey — consent first</h1>
        <p className="home-sub">
          Before we capture your answers for the care team, please agree to how your data is used
          (informed consent + data-use terms). Your care is <strong>not</strong> affected by declining.
        </p>
        <div className="composite sev2" style={{ display: 'block' }}>
          <ul style={{ margin: '4px 0 12px 18px', lineHeight: 1.6 }}>
            <li>Your answers help your neurologist and EEG technician prepare.</li>
            <li>Data is de-identified (replaced with a code) before any AI analysis.</li>
            <li>AI is decision-support only — a neurologist reviews everything.</li>
            <li>You may withdraw at any time.</li>
          </ul>
          <button className="btn" onClick={() => setConsent(true)}>✔ I understand &amp; consent</button>
        </div>
      </main>
    )
  }

  if (submitted) {
    const byRole = ['Neurologist', 'EEG Technician'].map((role) => ({
      role, items: QUESTIONS.filter((q) => q.to === role).map((q) => ({ q: q.q, a: ans[q.id] || '—' })),
    }))
    return (
      <main className="content home">
        <h1 className="home-h1">✅ Survey captured — hand-off notes</h1>
        <p className="home-sub">These structured notes are routed to each clinician (de-identified, EP001).</p>
        {byRole.map((b) => (
          <section key={b.role} style={{ marginBottom: 18 }}>
            <h2 className="dash-h2">For the {b.role}</h2>
            <table className="dash">
              <thead><tr><th>Question</th><th>Patient answer</th></tr></thead>
              <tbody>{b.items.map((it, i) => <tr key={i}><td>{it.q}</td><td>{it.a}</td></tr>)}</tbody>
            </table>
          </section>
        ))}
        <button className="btn ghost" onClick={() => { setSubmitted(false); setAns({}); }}>Start over</button>
      </main>
    )
  }

  return (
    <main className="content home">
      <h1 className="home-h1">🗣️ Patient Survey — tell your care team</h1>
      <p className="home-sub">Answer what you can ({answered}/{QUESTIONS.length}). Your answers go to the right clinician.</p>
      {['Neurologist', 'EEG Technician'].map((role) => (
        <section key={role} style={{ marginBottom: 18 }}>
          <h2 className="dash-h2">Questions for the {role}</h2>
          {QUESTIONS.filter((q) => q.to === role).map((q) => (
            <div className="q" key={q.id} style={{ display: 'block' }}>
              <div className="q-key" style={{ marginBottom: 6 }}>{q.q}</div>
              {q.type === 'choice' ? (
                <div className="q-opts">
                  {q.opts.map((o) => (
                    <button key={o} className={'opt' + (ans[q.id] === o ? ' sel sev2' : '')} onClick={() => set(q.id, o)}>{o}</button>
                  ))}
                </div>
              ) : (
                <input className="search" style={{ maxWidth: 520 }} value={ans[q.id] || ''}
                       placeholder="Type your answer…" onChange={(e) => set(q.id, e.target.value)} />
              )}
            </div>
          ))}
        </section>
      ))}
      <button className="btn" onClick={() => setSubmitted(true)}>Submit to care team →</button>
    </main>
  )
}
