// KnowledgeGraph.jsx — Semantic layer: visualize the epilepsy RDF knowledge graph
// (kg_nodes.csv + kg_edges.csv), plus the MCP tool servers and the multi-agent roster.
import React, { useMemo, useState } from 'react'
import { parseCSV } from './csv.js'

const TYPECOLOR = {
  Patient: '#dc2626', SeizureType: '#7c3aed', EEGFeature: '#2563eb', ASM: '#059669',
  Assessment: '#d97706', Outcome: '#db2777', Guideline: '#0891b2', Severity: '#9333ea', BrainRegion: '#65a30d',
}

const MCP = [
  ['kg-query', 'read graph', 'low', 'all agents'],
  ['guideline-retrieval', 'vector search', 'low', 'read-only'],
  ['patient-context', 'de-id features', 'high', 'consent + purpose'],
  ['eeg-analysis', 'run signal model', 'medium', 'approved agents'],
  ['risk-score', '90d seizure risk', 'medium', 'approved agents'],
  ['write-note', 'append note', 'high', 'human approval'],
  ['send-alert', 'patient/clinician alert', 'high', 'clinical authorization'],
]
const AGENTS = [
  ['Intake', 'context + consent', 'patient-context, kg-query'],
  ['Assessment', 'structure assessments', 'kg-query, guideline'],
  ['EEG-analysis', 'signal model', 'eeg-analysis'],
  ['Risk-scoring', 'compute risk', 'risk-score'],
  ['Guideline', 'retrieve evidence', 'guideline, kg-query'],
  ['Explainability', 'SHAP/graph reasons', 'kg-query'],
  ['Safety', 'clinical rules / abstain', 'read-only'],
  ['Compliance', 'consent/PII/audit', 'read-only'],
  ['Report', 'assemble report', 'guideline'],
  ['Human-approval', 'route to neurologist', 'write-note*, send-alert* (gated)'],
]
const RISKCLS = { low: 'sev1', medium: 'sev2', high: 'sev4' }

export default function KnowledgeGraph({ datasets }) {
  const nodesDs = datasets.find((d) => d.name === 'kg_nodes.csv')
  const edgesDs = datasets.find((d) => d.name === 'kg_edges.csv')
  const nodes = useMemo(() => (nodesDs ? parseCSV(nodesDs.text).rows : []), [nodesDs])
  const edges = useMemo(() => (edgesDs ? parseCSV(edgesDs.text).rows : []), [edgesDs])
  const [hover, setHover] = useState(null)

  const layout = useMemo(() => {
    const W = 760, H = 520, cx = W / 2, cy = H / 2, R = 210
    const pos = {}
    nodes.forEach((n, i) => {
      const a = (i / nodes.length) * 2 * Math.PI - Math.PI / 2
      pos[n.id] = { x: cx + R * Math.cos(a), y: cy + R * Math.sin(a), ...n }
    })
    return { W, H, pos }
  }, [nodes])

  if (!nodes.length) return <div className="content"><div className="crumb">kg_nodes.csv not found — run analysis/knowledge_graph_export.py</div></div>

  const { W, H, pos } = layout
  const activeEdges = hover ? edges.filter((e) => e.source === hover || e.target === hover) : edges
  const types = [...new Set(nodes.map((n) => n.type))]

  return (
    <main className="content home">
      <h1 className="home-h1">🕸️ Knowledge Graph (RDF) + MCP + Multi-Agent</h1>
      <p className="home-sub">
        The semantic backbone the RAG/agent layer reasons over: {nodes.length} nodes, {edges.length} relations.
        Exported as <strong>RDF Turtle</strong> (epilepsy-kg.ttl — load into a triple store / graph DB) and node/edge CSVs.
        Hover a node to isolate its relationships.
      </p>

      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 10 }}>
        {types.map((t) => (
          <span key={t} className="sev" style={{ background: TYPECOLOR[t] || '#64748b', color: '#fff', padding: '2px 8px', borderRadius: 10, fontSize: 11 }}>{t}</span>
        ))}
      </div>

      <div className="chartbox" style={{ maxWidth: '100%', overflowX: 'auto' }}>
        <svg viewBox={`0 0 ${W} ${H}`} width="100%">
          {activeEdges.map((e, i) => {
            const a = pos[e.source], b = pos[e.target]
            if (!a || !b) return null
            const dim = hover && e.source !== hover && e.target !== hover
            return (
              <g key={i} opacity={dim ? 0.08 : 0.5}>
                <line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke="#94a3b8" strokeWidth="1" />
                <text x={(a.x + b.x) / 2} y={(a.y + b.y) / 2} fontSize="8" fill="#64748b">{e.relation}</text>
              </g>
            )
          })}
          {nodes.map((n) => {
            const p = pos[n.id]
            const on = !hover || hover === n.id || edges.some((e) => (e.source === hover && e.target === n.id) || (e.target === hover && e.source === n.id))
            return (
              <g key={n.id} opacity={on ? 1 : 0.25} onMouseEnter={() => setHover(n.id)} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }}>
                <circle cx={p.x} cy={p.y} r={hover === n.id ? 9 : 6} fill={TYPECOLOR[n.type] || '#64748b'} />
                <text x={p.x + 9} y={p.y + 3} fontSize="9" fill="currentColor">{n.label}</text>
              </g>
            )
          })}
        </svg>
      </div>

      <h2 className="dash-h2" style={{ marginTop: 18 }}>MCP tool servers (Model Context Protocol)</h2>
      <div className="chartbox" style={{ overflowX: 'auto' }}>
        <table className="dash">
          <thead><tr><th>Server</th><th>Exposes</th><th>Risk</th><th>Access rule</th></tr></thead>
          <tbody>{MCP.map((m) => (
            <tr key={m[0]}><td><strong>{m[0]}</strong></td><td>{m[1]}</td>
              <td><span className={'pill ' + RISKCLS[m[2]]}>{m[2]}</span></td><td>{m[3]}</td></tr>
          ))}</tbody>
        </table>
      </div>

      <h2 className="dash-h2" style={{ marginTop: 18 }}>Multi-agent roster (least-privilege)</h2>
      <div className="chartbox" style={{ overflowX: 'auto' }}>
        <table className="dash">
          <thead><tr><th>Agent</th><th>Job</th><th>Allowed MCP tools</th></tr></thead>
          <tbody>{AGENTS.map((a) => (
            <tr key={a[0]}><td><strong>{a[0]}</strong></td><td>{a[1]}</td><td>{a[2]}</td></tr>
          ))}</tbody>
        </table>
      </div>
      <div className="crumb" style={{ marginTop: 12 }}>* high-risk tools require the human-approval gate (neurologist). Full spec: docs/enterprise-flow/mcp-multiagent-knowledge-graph.md</div>
    </main>
  )
}
