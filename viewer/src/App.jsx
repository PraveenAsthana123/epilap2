import React, { useMemo, useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import Mermaid from './Mermaid.jsx'

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
  'Start', 'Part I–III', 'Pipelines', 'Part IV–VIII', 'Primary Assessment',
  'Roles & Stakeholders', 'HEP Dataset', 'Source Datasets', 'Dataset Dossiers', 'Reference',
]

// Extract the first H1 as the doc title; fall back to the path.
function titleFromMarkdown(md, fallback) {
  const m = md.match(/^\s*#\s+(.+)$/m)
  return m ? m[1].trim() : fallback
}

// Map a doc path to an "All Docs" nav group. Order of checks matters (most specific first).
function classify(rel) {
  const parts = rel.split('/')
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

// Section docs belonging to one role (numbered files inside its folder), sorted.
function sectionsFor(role) {
  return DOCS
    .filter((d) => d.path.startsWith(role.dir))
    .sort((a, b) => a.path.localeCompare(b.path, undefined, { numeric: true }))
}
// Precompute per-role doc lists once.
const ROLE_DOCS = Object.fromEntries(
  ROLES.map((r) => [r.key, { overview: BY_ID[r.overview] || null, sections: sectionsFor(r) }])
)

// "All Docs" = everything that is NOT a per-role assessment section or role overview.
const ALL_DOCS = DOCS.filter(
  (d) => !ROLES.some((r) => d.path.startsWith(r.dir)) && !ROLE_OVERVIEWS.has(d.path)
)

export default function App() {
  // view is 'home' | 'all' | a role key.
  const [view, setView] = useState('home')
  const [activeId, setActiveId] = useState(null)
  const [query, setQuery] = useState('')
  const [navOpen, setNavOpen] = useState(false)

  const role = ROLES.find((r) => r.key === view) || null
  const active = activeId ? BY_ID[activeId] : null

  // Switch portal, picking a sensible default document for the destination.
  function enter(v) {
    setView(v)
    setNavOpen(false)
    setQuery('')
    if (v === 'home') { setActiveId(null); return }
    if (v === 'all') { setActiveId(ALL_DOCS[0]?.id ?? null); return }
    const rd = ROLE_DOCS[v]
    setActiveId((rd.overview || rd.sections[0])?.id ?? null)
  }

  const go = (id) => { setActiveId(id); setNavOpen(false) }

  useEffect(() => { window.scrollTo(0, 0) }, [activeId, view])

  // Grouped nav for the "All Docs" portal, filtered by the search box.
  const allGroups = useMemo(() => {
    const map = new Map()
    for (const d of ALL_DOCS) {
      const hit =
        !query ||
        d.title.toLowerCase().includes(query.toLowerCase()) ||
        d.md.toLowerCase().includes(query.toLowerCase())
      if (!hit) continue
      if (!map.has(d.group)) map.set(d.group, [])
      map.get(d.group).push(d)
    }
    return [...map.entries()].sort(
      (a, b) => GROUP_ORDER.indexOf(a[0]) - GROUP_ORDER.indexOf(b[0])
    )
  }, [query])

  // ---- Top tab bar (shared across all views) --------------------------------
  const topbar = (
    <header className="topbar">
      <button className="logo" onClick={() => enter('home')} title="Role portals home">
        <span className="logo-mark">◈</span> DBA Blueprint
      </button>
      <nav className="tabs">
        {ROLES.map((r) => (
          <button
            key={r.key}
            className={'tab' + (view === r.key ? ' active' : '')}
            onClick={() => enter(r.key)}
          >
            <span className="tab-ic">{r.icon}</span>{r.label}
          </button>
        ))}
        <button
          className={'tab tab-all' + (view === 'all' ? ' active' : '')}
          onClick={() => enter('all')}
        >
          All Docs
        </button>
      </nav>
    </header>
  )

  // ---- Home: role portal landing cards -------------------------------------
  if (view === 'home') {
    return (
      <div className="app">
        {topbar}
        <main className="content home">
          <h1 className="home-h1">Epilepsy Primary Assessment — Role Portals</h1>
          <p className="home-sub">
            Patient <strong>EP001</strong> · Each role has its own workspace. Open a portal to see
            that role's assessment questions, captured from its point of view, with a four-level
            severity model (Mild → Moderate → Severe → Refractory/Status) on every section.
          </p>
          <div className="cards">
            {ROLES.map((r) => (
              <button className="card" key={r.key} onClick={() => enter(r.key)}>
                <div className="card-icon">{r.icon}</div>
                <div className="card-title">{r.label}</div>
                <div className="card-blurb">{r.blurb}</div>
                <div className="card-meta">{ROLE_DOCS[r.key].sections.length} assessments →</div>
              </button>
            ))}
          </div>
        </main>
      </div>
    )
  }

  // ---- Role portal OR All Docs (both use the sidebar + content shell) -------
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
                {SEVERITY.map((s) => (
                  <span className={'sev ' + s.cls} key={s.k}>{s.k} {s.label}</span>
                ))}
              </div>
              {ROLE_DOCS[role.key].overview && (
                <div className="navgroup">
                  <div className="navlabel">Overview</div>
                  <button
                    className={'navitem' + (active?.id === ROLE_DOCS[role.key].overview.id ? ' active' : '')}
                    onClick={() => go(ROLE_DOCS[role.key].overview.id)}
                  >
                    Role Overview · Concerns · Tasks
                  </button>
                </div>
              )}
              <div className="navgroup">
                <div className="navlabel">Assessments ({ROLE_DOCS[role.key].sections.length})</div>
                {ROLE_DOCS[role.key].sections.map((d, i) => (
                  <button
                    key={d.id}
                    className={'navitem' + (d.id === active?.id ? ' active' : '')}
                    onClick={() => go(d.id)}
                    title={d.path}
                  >
                    <span className="numdot">{i + 1}</span>{d.title.replace(/\s*\(EP001\)\s*$/, '')}
                  </button>
                ))}
              </div>
            </>
          ) : (
            <>
              <div className="brand">
                All Documents
                <small>Full DBA blueprint · pipelines, datasets, HEP & reference</small>
              </div>
              <input
                className="search"
                placeholder="Search all docs…"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
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
          {active ? (
            <>
              <div className="crumb">
                {role ? `${role.label} portal` : active.group} · {active.path}
              </div>
              <article className="md">
                <ReactMarkdown remarkPlugins={[remarkGfm]} components={MD_COMPONENTS}>
                  {active.md}
                </ReactMarkdown>
              </article>
            </>
          ) : (
            <div className="crumb">Select an item from the menu.</div>
          )}
        </main>
      </div>
    </div>
  )
}
