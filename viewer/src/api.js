// api.js — thin client for the Epilepsy Platform API.
// Base URL comes from VITE_API_URL, else "/api" (dev proxy -> localhost:8000).
// Every call falls back gracefully so the viewer works even with no API running.

const BASE = import.meta.env?.VITE_API_URL || '/api'

async function get(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`API ${path} -> ${res.status}`)
  return res.json()
}

export async function getScenarios(category) {
  const q = category ? `?category=${encodeURIComponent(category)}` : ''
  return get(`/scenarios${q}`)
}

export async function getRoles() {
  return get('/roles')
}

// Weighted severity score via the API (mirrors the local scorer).
export async function postScore(sections, role, apiKey) {
  const res = await fetch(`${BASE}/score`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(apiKey ? { 'X-API-Key': apiKey } : {}) },
    body: JSON.stringify({ role, sections }),
  })
  if (!res.ok) throw new Error(`score -> ${res.status}`)
  return res.json()
}

// Convenience: is the API reachable? (used to decide local vs API scoring)
export async function apiHealthy() {
  try {
    const r = await fetch(`${BASE}/health`)
    return r.ok
  } catch {
    return false
  }
}
