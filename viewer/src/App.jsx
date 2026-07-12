import React, { useMemo, useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import Mermaid from './Mermaid.jsx'
import { parseSeverity, bandOf, scoreOf } from './scoring.js'
import DataView from './DataView.jsx'

// Load every generated dataset (data/analysis/*.csv) as raw text for the Data tab.
const CSV_MODULES = import.meta.glob('../../data/analysis/*.csv', {
  query: '?raw', import: 'default', eager: true,
})
const DATASETS = Object.entries(CSV_MODULES)
  .map(([path, text]) => ({ name: path.split('/').pop(), text }))
  .sort((a, b) => a.name.localeCompare(b.name))

// Custom renderers: code fences tagged ```mermaid become diagrams.
const MD_COMPONENTS = {
  code(props) {
    const { className, children } = props
    const text = String(children ?? '')
    if (/language-mermaid/.test(className || '')) {
      return <Mermaid code={text.replace(/\n$/, '')} />
    }
    return <code className={className}>{children}</code>
  },
}

// Eagerly load every markdown doc from ../docs as raw text.
const modules = import.meta.glob('../../docs/**/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
})

// ---------------------------------------------------------------------------
// Role portals. Each role is its own UI: a top tab + a dedicated left menu that
// lists ONLY that role's assessment sections (plus a role overview page).
// ---------------------------------------------------------------------------
const ROLES = [
  { key: 'neurologist',      label: 'Neurologist',      icon: '🧠', dir: 'primary-assessment/neurologist/',      overview: 'primary-assessment/roles-neurologist.md',      blurb: 'Clinical history, exam, seizure semiology & diagnosis' },
  { key: 'eeg-technician',   label: 'EEG Technician',   icon: '📈', dir: 'primary-assessment/eeg-technician/',   overview: 'primary-assessment/roles-eeg-technician.md',   blurb: 'EEG acquisition, impedance & signal quality control' },
  { key: 'nurse',            label: 'Nurse',            icon: '🩺', dir: 'primary-assessment/nurse/',            overview: 'primary-assessment/roles-nurse.md',            blurb: 'Vitals, seizure observation, safety & care plan' },
  { key: 'neuropsychologist',label: 'Neuropsychologist',icon: '🧩', dir: 'primary-assessment/neuropsychologist/',overview: 'primary-assessment/roles-neuropsychologist.md',blurb: 'Cognition, memory, mood & quality of life' },
  { key: 'pharmacist',       label: 'Pharmacist',       icon: '💊', dir: 'primary-assessment/pharmacist/',       overview: 'primary-assessment/roles-pharmacist.md',       blurb: 'ASM regimen, drug levels, interactions & adherence' },
  { key: 'caregiver',        label: 'Caregiver',        icon: '🤝', dir: 'primary-assessment/caregiver/',        overview: 'primary-assessment/roles-caregiver.md',        blurb: 'Witnessed seizures, home support & caregiver burden' },
  { key: 'patient',          label: 'Patient',          icon: '🧍', dir: 'primary-assessment/patient/',          overview: 'primary-assessment/roles-patient.md',          blurb: 'Self-reported symptoms, seizure diary & outcomes' },
  { key: 'administrator',    label: 'Administrator',    icon: '🗂️', dir: 'primary-assessment/administrator/',    overview: 'primary-assessment/roles-administrator.md',    blurb: 'Registration, coding, scheduling & governance' },
  { key: 'occupational-therapist', label: 'Occupational Therapist', icon: '🧰', dir: 'primary-assessment/occupational-therapist/', overview: 'primary-assessment/roles-occupational-therapist.md', blurb: 'Function, ADL/IADL, participation, home safety & return-to-work' },
  { key: 'radiologist', label: 'Radiologist', icon: '🩻', dir: 'primary-assessment/radiologist/', overview: 'primary-assessment/roles-radiologist.md', blurb: 'MRI/CT/PET imaging, lesion & epileptogenic-zone localization' },
]
const ROLE_OVERVIEWS = new Set(ROLES.map((r) => r.overview))

// Shared four-level severity ladder shown in every role portal header.
const SEVERITY = [
  { k: 'L1', label: 'Mild', cls: 'sev1' },
  { k: 'L2', label: 'Moderate', cls: 'sev2' },
  { k: 'L3', label: 'Severe · EP001', cls: 'sev3' },
  { k: 'L4', label: 'Refractory / Status', cls: 'sev4' },
]

// Human-friendly ordering for the "All Docs" nav sections (the rest of the blueprint).
const GROUP_ORDER = [
  'Start', 'Vision', 'Analytics', 'Responsible AI', 'Part I–III', 'Pipelines',
  'Part IV–VIII', 'Primary Assessment', 'Roles & Stakeholders', 'HEP Dataset',
  'Source Datasets', 'Dataset Dossiers', 'Reference',
]

// Extract the first H1 as the doc title; fall back to the path.
function titleFromMarkdown(md, fallback) {
  const m = md.match(/^\s*#\s+(.+)$/m)
  return m ? m[1].trim() : fallback
}

// Map a doc path to an "All Docs" nav group. Order of checks matters (most specific first).
function classify(rel) {
  const parts = rel.split('/')
  if (rel.startsWith('analysis/')) return 'Analytics'
  if (rel.startsWith('responsible-ai/')) return 'Responsible AI'
  if (rel === 'research-vision.md') return 'Vision'
  if (rel === 'patient-onboarding.md') return 'Vision'
  if (rel.startsWith('primary-assessment/')) return 'Primary Assessment'
  if (rel.startsWith('stakeholders/') || rel.startsWith('roles-study/')) return 'Roles & Stakeholders'
  if (rel.startsWith('hep/')) return 'HEP Dataset'
  if (rel.startsWith('source-datasets/')) return 'Source Datasets'
  if (rel.startsWith('datasets/')) return 'Dataset Dossiers'
  if (parts[0].startsWith('pipeline-')) return 'Pipelines'
  if (parts[0].startsWith('part1') || parts[0].startsWith('part2')) return 'Part I–III'
  if (parts[0].startsWith('part4') || parts[0].startsWith('part5')) return 'Part IV–VIII'
  if (parts[0].startsWith('00-overview')) return 'Start'
  return 'Reference'
}

// Severity-model parsing + scoring math live in scoring.js (pure, unit-tested).

function buildDocs() {
  const docs = Object.entries(modules).map(([path, md]) => {
    const rel = path.replace('../../docs/', '')
    return {
      id: rel,
      path: rel,
      md,
      group: classify(rel),
      title: titleFromMarkdown(md, rel),
      depth: rel.split('/').length,
    }
  })
  docs.sort((a, b) => a.path.localeCompare(b.path, undefined, { numeric: true }))
  return docs
}

const DOCS = buildDocs()
const BY_ID = Object.fromEntries(DOCS.map((d) => [d.id, d]))
// Precompute the scoring form for every doc that carries a severity model.
const QUESTIONS = Object.fromEntries(DOCS.map((d) => [d.id, parseSeverity(d.md)]))

function sectionsFor(role) {
  return DOCS
    .filter((d) => d.path.startsWith(role.dir))
    .sort((a, b) => a.path.localeCompare(b.path, undefined, { numeric: true }))
}
const ROLE_DOCS = Object.fromEntries(
  ROLES.map((r) => [r.key, { overview: BY_ID[r.overview] || null, sections: sectionsFor(r) }])
)

// "All Docs" = everything that is NOT a per-role assessment section or role overview.
const ALL_DOCS = DOCS.filter(
  (d) => !ROLES.some((r) => d.path.startsWith(r.dir)) && !ROLE_OVERVIEWS.has(d.path)
)

function Gauge({ level }) {
  return (
    <div className="gauge">
      {[1, 2, 3, 4].map((l) => (
        <span key={l} className={'seg sev' + l + (l === level ? ' on' : '')} />
      ))}
    </div>
  )
}

// ---- Interactive scoring form for one assessment --------------------------
function ScoreForm({ doc, ans, setAns, clear, prefill }) {
  const { questions } = QUESTIONS[doc.id]
  const s = scoreOf(ans, questions)
  return (
    <div className="scoreform">
      <div className={'scorecard ' + (s.band.cls || 'sevnone')}>
        <div className="sc-left">
          <div className="sc-answered">Answered {s.answered}/{s.total}</div>
          <div className="sc-band">{s.band.label}</div>
          <Gauge level={s.band.level} />
        </div>
        <div className="sc-num">
          {s.mean != null ? s.mean.toFixed(2) : '—'}<span>/4</span>
        </div>
      </div>
      <div className="sc-actions">
        <button className="btn" onClick={prefill}>Prefill EP001 (Level 3)</button>
        <button className="btn ghost" onClick={clear}>Clear answers</button>
        <span className="sc-hint">Pick the answer that best matches the patient for each item.</span>
      </div>
      {questions.map((q) => (
        <div className="q" key={q.key}>
          <div className="q-key">{q.key}</div>
          <div className="q-opts">
            {q.options.map((o) => (
              <button
                key={o.level}
                disabled={o.value === '—'}
                className={'opt' + (ans?.[q.key] === o.level ? ' sel sev' + o.level : '')}
                onClick={() => setAns(q.key, o.level)}
                title={o.value}
              >
                <b>L{o.level}</b> {o.value}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

export default function App() {
  const [view, setView] = useState('home') // 'home' | 'all' | role key
  const [activeId, setActiveId] = useState(null) // doc id, or 'DASH:<role>'
  const [query, setQuery] = useState('')
  const [navOpen, setNavOpen] = useState(false)
  const [scoreMode, setScoreMode] = useState(false)
  const [answers, setAnswers] = useState(() => {
    try { return JSON.parse(localStorage.getItem('ep-answers') || '{}') } catch { return {} }
  })
  useEffect(() => {
    try { localStorage.setItem('ep-answers', JSON.stringify(answers)) } catch {}
  }, [answers])

  const role = ROLES.find((r) => r.key === view) || null
  const isDash = typeof activeId === 'string' && activeId.startsWith('DASH:')
  const active = isDash ? null : (activeId ? BY_ID[activeId] : null)
  const activeHasScore = active && QUESTIONS[active.id]

  function enter(v) {
    setView(v); setNavOpen(false); setQuery(''); setScoreMode(false)
    if (v === 'home') { setActiveId(null); return }
    if (v === 'data') { setActiveId(null); return }
    if (v === 'all') { setActiveId(ALL_DOCS[0]?.id ?? null); return }
    const rd = ROLE_DOCS[v]
    setActiveId((rd.overview || rd.sections[0])?.id ?? null)
  }
  const go = (id) => { setActiveId(id); setNavOpen(false); setScoreMode(false) }

  // Answer setters (kept as stable-ish closures over `answers`).
  const setAns = (docId, key, level) =>
    setAnswers((a) => ({ ...a, [docId]: { ...(a[docId] || {}), [key]: level } }))
  const clearDoc = (docId) =>
    setAnswers((a) => { const n = { ...a }; delete n[docId]; return n })
  const prefillDoc = (docId) => {
    const q = QUESTIONS[docId]
    if (!q) return
    setAnswers((a) => ({ ...a, [docId]: Object.fromEntries(q.questions.map((x) => [x.key, 3])) }))
  }

  useEffect(() => { window.scrollTo(0, 0) }, [activeId, view])

  // ---- Aggregation: section -> role -> patient ----------------------------
  const roleAgg = (roleKey) => {
    const secs = ROLE_DOCS[roleKey].sections.filter((d) => QUESTIONS[d.id])
    const scored = secs
      .map((d) => ({ d, s: scoreOf(answers[d.id], QUESTIONS[d.id].questions) }))
      .filter((x) => x.s.answered > 0)
    const mean = scored.length ? scored.reduce((a, x) => a + x.s.mean, 0) / scored.length : null
    return { secs, scored, mean, band: bandOf(mean) }
  }
  const patientAgg = () => {
    const rs = ROLES.map((r) => ({ r, agg: roleAgg(r.key) })).filter((x) => x.agg.mean != null)
    const mean = rs.length ? rs.reduce((a, x) => a + x.agg.mean, 0) / rs.length : null
    return { rs, mean, band: bandOf(mean) }
  }

  const allGroups = useMemo(() => {
    const map = new Map()
    for (const d of ALL_DOCS) {
      const hit = !query ||
        d.title.toLowerCase().includes(query.toLowerCase()) ||
        d.md.toLowerCase().includes(query.toLowerCase())
      if (!hit) continue
      if (!map.has(d.group)) map.set(d.group, [])
      map.get(d.group).push(d)
    }
    return [...map.entries()].sort((a, b) => GROUP_ORDER.indexOf(a[0]) - GROUP_ORDER.indexOf(b[0]))
  }, [query])

  const topbar = (
    <header className="topbar">
      <button className="logo" onClick={() => enter('home')} title="Role portals home">
        <span className="logo-mark">◈</span> DBA Blueprint
      </button>
      <nav className="tabs">
        {ROLES.map((r) => (
          <button key={r.key} className={'tab' + (view === r.key ? ' active' : '')} onClick={() => enter(r.key)}>
            <span className="tab-ic">{r.icon}</span>{r.label}
          </button>
        ))}
        <button className={'tab tab-all' + (view === 'all' ? ' active' : '')} onClick={() => enter('all')}>
          All Docs
        </button>
        {DATASETS.length > 0 && (
          <button className={'tab tab-all' + (view === 'data' ? ' active' : '')} onClick={() => enter('data')}>
            📊 Data
          </button>
        )}
      </nav>
    </header>
  )

  // ---- Data tab: browse every generated CSV -------------------------------
  if (view === 'data') {
    return (
      <div className="app">
        {topbar}
        <DataView datasets={DATASETS} />
      </div>
    )
  }

  // ---- Home ----------------------------------------------------------------
  if (view === 'home') {
    const pa = patientAgg()
    return (
      <div className="app">
        {topbar}
        <main className="content home">
          <h1 className="home-h1">Epilepsy Primary Assessment — Role Portals</h1>
          <p className="home-sub">
            Patient <strong>EP001</strong> · Each role has its own workspace. Open a portal to see that
            role's assessment questions, then use <strong>Fill &amp; Score</strong> to enter answers and
            get a live severity score (Mild → Moderate → Severe → Refractory/Status).
          </p>
          {pa.mean != null && (
            <div className={'composite ' + pa.band.cls}>
              <div>
                <div className="comp-label">Current EP001 composite severity</div>
                <div className="comp-band">{pa.band.label}</div>
                <div className="comp-sub">{pa.rs.length} of {ROLES.length} roles scored</div>
              </div>
              <div className="comp-num">{pa.mean.toFixed(2)}<span>/4</span></div>
            </div>
          )}
          <div className="cards">
            {ROLES.map((r) => {
              const agg = roleAgg(r.key)
              return (
                <button className="card" key={r.key} onClick={() => enter(r.key)}>
                  <div className="card-icon">{r.icon}</div>
                  <div className="card-title">{r.label}</div>
                  <div className="card-blurb">{r.blurb}</div>
                  <div className="card-foot">
                    <span className="card-meta">{ROLE_DOCS[r.key].sections.length} assessments →</span>
                    {agg.mean != null && <span className={'pill ' + agg.band.cls}>{agg.band.label} {agg.mean.toFixed(1)}</span>}
                  </div>
                </button>
              )
            })}
          </div>
        </main>
      </div>
    )
  }

  // ---- Role portal / All Docs ---------------------------------------------
  return (
    <div className="app">
      {topbar}
      <button className="menubtn" onClick={() => setNavOpen((v) => !v)}>☰ Menu</button>
      <div className="shell">
        <aside className={'sidebar' + (navOpen ? ' open' : '')}>
          {role ? (
            <>
              <div className="rolehead">
                <span className="ricon">{role.icon}</span>
                <div>
                  <div className="rname">{role.label}</div>
                  <small>{role.blurb}</small>
                </div>
              </div>
              <div className="sevlegend" title="Every assessment section models these four severity levels">
                {SEVERITY.map((s) => (<span className={'sev ' + s.cls} key={s.k}>{s.k} {s.label}</span>))}
              </div>
              <div className="navgroup">
                <button
                  className={'navitem dashitem' + (activeId === 'DASH:' + role.key ? ' active' : '')}
                  onClick={() => go('DASH:' + role.key)}
                >
                  📊 Severity Dashboard
                </button>
                {ROLE_DOCS[role.key].overview && (
                  <button
                    className={'navitem' + (active?.id === ROLE_DOCS[role.key].overview.id ? ' active' : '')}
                    onClick={() => go(ROLE_DOCS[role.key].overview.id)}
                  >
                    📋 Role Overview · Concerns · Tasks
                  </button>
                )}
              </div>
              <div className="navgroup">
                <div className="navlabel">Assessments ({ROLE_DOCS[role.key].sections.length})</div>
                {ROLE_DOCS[role.key].sections.map((d, i) => {
                  const sc = QUESTIONS[d.id] ? scoreOf(answers[d.id], QUESTIONS[d.id].questions) : null
                  return (
                    <button
                      key={d.id}
                      className={'navitem' + (d.id === active?.id ? ' active' : '')}
                      onClick={() => go(d.id)}
                      title={d.path}
                    >
                      <span className="numdot">{i + 1}</span>
                      <span className="navtxt">{d.title.replace(/\s*\(EP001\)\s*$/, '')}</span>
                      {sc && sc.answered > 0 && <span className={'dot ' + sc.band.cls} title={sc.band.label} />}
                    </button>
                  )
                })}
              </div>
            </>
          ) : (
            <>
              <div className="brand">
                All Documents
                <small>Full DBA blueprint · pipelines, datasets, HEP & reference</small>
              </div>
              <input className="search" placeholder="Search all docs…" value={query} onChange={(e) => setQuery(e.target.value)} />
              {allGroups.map(([group, items]) => (
                <div className="navgroup" key={group}>
                  <div className="navlabel">{group}</div>
                  {items.map((d) => (
                    <button
                      key={d.id}
                      className={'navitem' + (d.id === active?.id ? ' active' : '') + (d.depth > 2 ? ' nested' : '')}
                      onClick={() => go(d.id)}
                      title={d.path}
                    >
                      {d.title}
                    </button>
                  ))}
                </div>
              ))}
              {allGroups.length === 0 && <div className="navlabel">No matches</div>}
              <div className="count">{ALL_DOCS.length} documents</div>
            </>
          )}
        </aside>

        <main className="content">
          {isDash && role ? (
            <Dashboard role={role} roleAgg={roleAgg} patientAgg={patientAgg} answers={answers} go={go} />
          ) : active ? (
            <>
              <div className="crumb">{role ? `${role.label} portal` : active.group} · {active.path}</div>
              {activeHasScore && (
                <div className="modetoggle">
                  <button className={!scoreMode ? 'on' : ''} onClick={() => setScoreMode(false)}>📖 Read</button>
                  <button className={scoreMode ? 'on' : ''} onClick={() => setScoreMode(true)}>✍️ Fill &amp; Score</button>
                </div>
              )}
              {activeHasScore && scoreMode ? (
                <>
                  <h1 className="md-inline-h1">{active.title.replace(/\s*\(EP001\)\s*$/, '')}</h1>
                  <ScoreForm
                    doc={active}
                    ans={answers[active.id]}
                    setAns={(k, l) => setAns(active.id, k, l)}
                    clear={() => clearDoc(active.id)}
                    prefill={() => prefillDoc(active.id)}
                  />
                </>
              ) : (
                <article className="md">
                  <ReactMarkdown remarkPlugins={[remarkGfm]} components={MD_COMPONENTS}>{active.md}</ReactMarkdown>
                </article>
              )}
            </>
          ) : (
            <div className="crumb">Select an item from the menu.</div>
          )}
        </main>
      </div>
    </div>
  )
}

// ---- Per-role severity dashboard -----------------------------------------
function Dashboard({ role, roleAgg, patientAgg, go }) {
  const agg = roleAgg(role.key)
  const pa = patientAgg()
  return (
    <>
      <div className="crumb">{role.label} portal · Severity Dashboard</div>
      <h1 className="home-h1">{role.icon} {role.label} — Severity Dashboard</h1>
      <p className="home-sub">
        Live scores from the answers you enter under <strong>Fill &amp; Score</strong>. Each assessment is
        scored as the mean of its answered items (Level 1–4), then averaged into this role's severity and,
        across all roles, into the overall EP001 composite.
      </p>

      <div className={'scorecard big ' + (agg.band.cls || 'sevnone')}>
        <div className="sc-left">
          <div className="sc-answered">{role.label} role severity · {agg.scored.length}/{agg.secs.length} assessments scored</div>
          <div className="sc-band">{agg.band.label}</div>
          <Gauge level={agg.band.level} />
        </div>
        <div className="sc-num">{agg.mean != null ? agg.mean.toFixed(2) : '—'}<span>/4</span></div>
      </div>

      <table className="dash">
        <thead><tr><th>Assessment</th><th>Answered</th><th>Score</th><th>Severity</th></tr></thead>
        <tbody>
          {agg.secs.map((d) => {
            const found = agg.scored.find((x) => x.d.id === d.id)
            const s = found?.s
            return (
              <tr key={d.id} onClick={() => go(d.id)} className="dash-row">
                <td>{d.title.replace(/\s*\(EP001\)\s*$/, '')}</td>
                <td>{s ? `${s.answered}/${s.total}` : '—'}</td>
                <td>{s?.mean != null ? s.mean.toFixed(2) : '—'}</td>
                <td>{s ? <span className={'pill ' + s.band.cls}>{s.band.label}</span> : <span className="pill sevnone">Not scored</span>}</td>
              </tr>
            )
          })}
        </tbody>
      </table>

      <h2 className="dash-h2">Patient EP001 — composite across all roles</h2>
      <div className={'scorecard big ' + (pa.band.cls || 'sevnone')}>
        <div className="sc-left">
          <div className="sc-answered">{pa.rs.length}/{ROLES.length} roles scored</div>
          <div className="sc-band">{pa.band.label}</div>
          <Gauge level={pa.band.level} />
        </div>
        <div className="sc-num">{pa.mean != null ? pa.mean.toFixed(2) : '—'}<span>/4</span></div>
      </div>
      <table className="dash">
        <thead><tr><th>Role</th><th>Assessments scored</th><th>Score</th><th>Severity</th></tr></thead>
        <tbody>
          {ROLES.map((r) => {
            const a = roleAgg(r.key)
            return (
              <tr key={r.key} className="dash-row" onClick={() => { }}>
                <td>{r.icon} {r.label}</td>
                <td>{a.scored.length}/{a.secs.length}</td>
                <td>{a.mean != null ? a.mean.toFixed(2) : '—'}</td>
                <td>{a.mean != null ? <span className={'pill ' + a.band.cls}>{a.band.label}</span> : <span className="pill sevnone">Not scored</span>}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </>
  )
}
