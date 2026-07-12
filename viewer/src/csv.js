// csv.js — tiny robust CSV parser (handles quoted fields with commas/newlines)
// and lightweight column profiling for the data viewer.

export function parseCSV(text) {
  const rows = []
  let field = '', row = [], inQ = false
  const pushField = () => { row.push(field); field = '' }
  const pushRow = () => { rows.push(row); row = [] }
  text = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n')
  for (let i = 0; i < text.length; i++) {
    const ch = text[i]
    if (inQ) {
      if (ch === '"') {
        if (text[i + 1] === '"') { field += '"'; i++ } else inQ = false
      } else field += ch
    } else if (ch === '"') inQ = true
    else if (ch === ',') pushField()
    else if (ch === '\n') { pushField(); pushRow() }
    else field += ch
  }
  if (field.length || row.length) { pushField(); pushRow() }
  const nonEmpty = rows.filter((r) => r.length > 1 || (r.length === 1 && r[0] !== ''))
  const headers = nonEmpty.shift() || []
  const objs = nonEmpty.map((r) => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ''])))
  return { headers, rows: objs }
}

const NUMRE = /^-?\d+(\.\d+)?$/

// Per-column profile: type, missing, and numeric summary or top categories.
export function profile(headers, rows) {
  return headers.map((h) => {
    const vals = rows.map((r) => r[h])
    const present = vals.filter((v) => v !== '' && v != null)
    const nums = present.filter((v) => NUMRE.test(v)).map(Number)
    const numeric = present.length > 0 && nums.length >= present.length * 0.8
    const col = { name: h, missing: rows.length - present.length, numeric }
    if (numeric && nums.length) {
      const s = [...nums].sort((a, b) => a - b)
      col.min = s[0]; col.max = s[s.length - 1]
      col.mean = nums.reduce((a, b) => a + b, 0) / nums.length
      col.median = s[Math.floor(s.length / 2)]
    } else {
      const counts = {}
      for (const v of present) counts[v] = (counts[v] || 0) + 1
      col.top = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 8)
      col.unique = Object.keys(counts).length
    }
    return col
  })
}
