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

// Human-friendly ordering for the top-level nav sections (rendered in this order).
const GROUP_ORDER = [
  'Start', 'Part I–III', 'Pipelines', 'Part IV–VIII', 'Primary Assessment',
  'Roles & Stakeholders', 'HEP Dataset', 'Source Datasets', 'Dataset Dossiers', 'Reference',
]

// Extract the first H1 as the doc title; fall back to the path.
function titleFromMarkdown(md, fallback) {
  const m = md.match(/^\s*#\s+(.+)$/m)
  return m ? m[1].trim() : fallback
}

// Map a doc path to a nav group. Order of checks matters (most specific first).
function classify(path) {
  // path like ../../docs/primary-assessment/neurologist/01-chief-complaint.md
  const rel = path.replace('../../docs/', '')
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
      group: classify(path),
      title: titleFromMarkdown(md, rel),
      depth: rel.split('/').length,
    }
  })
  docs.sort((a, b) => a.path.localeCompare(b.path, undefined, { numeric: true }))
  return docs
}

const DOCS = buildDocs()

export default function App() {
  const [activeId, setActiveId] = useState(DOCS[0]?.id)
  const [query, setQuery] = useState('')
  const [navOpen, setNavOpen] = useState(false)

  const groups = useMemo(() => {
    const map = new Map()
    for (const d of DOCS) {
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

  const active = DOCS.find((d) => d.id === activeId) || DOCS[0]

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [activeId])

  const go = (id) => {
    setActiveId(id)
    setNavOpen(false)
  }

  return (
    <div className="shell">
      <button className="menubtn" onClick={() => setNavOpen((v) => !v)}>
        ☰ Menu
      </button>

      <aside className={'sidebar' + (navOpen ? ' open' : '')}>
        <div className="brand">
          DBA Blueprint
          <small>Enterprise AI · Explainable Multimodal Epilepsy Intelligence</small>
        </div>
        <input
          className="search"
          placeholder="Search all docs…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        {groups.map(([group, items]) => (
          <div className="navgroup" key={group}>
            <div className="navlabel">{group}</div>
            {items.map((d) => (
              <button
                key={d.id}
                className={'navitem' + (d.id === active.id ? ' active' : '') + (d.depth > 2 ? ' nested' : '')}
                onClick={() => go(d.id)}
                title={d.path}
              >
                {d.title}
              </button>
            ))}
          </div>
        ))}
        {groups.length === 0 && <div className="navlabel">No matches</div>}
        <div className="count">{DOCS.length} documents</div>
      </aside>

      <main className="content">
        <div className="crumb">{active.group} · {active.path}</div>
        <article className="md">
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={MD_COMPONENTS}>
            {active.md}
          </ReactMarkdown>
        </article>
      </main>
    </div>
  )
}
