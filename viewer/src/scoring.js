// scoring.js — pure, testable scoring logic for the assessment viewer.
// Extracted from App.jsx so it can be unit-tested with Vitest independently of React.
// Parses each section's four "### Level N" severity tables into a scoring form,
// and computes the mean-of-levels score + severity band.

// Return [firstCol, lastCol] pairs for the first markdown table in `text`,
// dropping the header row and the |---| separator.
export function parseFirstTable(text) {
  const rows = []
  let inTable = false
  for (const line of text.split('\n')) {
    const t = line.trim()
    if (t.startsWith('|')) {
      inTable = true
      const cells = t.split('|').slice(1, -1).map((c) => c.trim())
      if (cells.every((c) => /^:?-{2,}:?$/.test(c))) continue // separator row
      rows.push([cells[0], cells[cells.length - 1]])
    } else if (inTable) {
      break // blank / non-pipe line ends the table
    }
  }
  return rows.slice(1) // drop header row
}

// Turn a section's "## Severity Scenario Model" into { questions:[{key, options}] }.
export function parseSeverity(md) {
  const start = md.indexOf('## Severity Scenario Model')
  if (start < 0) return null
  let end = md.indexOf('### Severity Classification Logic', start)
  if (end < 0) {
    const nextH2 = md.indexOf('\n## ', start + 3)
    end = nextH2 < 0 ? md.length : nextH2
  }
  const block = md.slice(start, end)
  const perLevel = {} // level number -> [ [key, value], ... ]
  const levelRe = /###\s*Level\s*([1-4])[^\n]*\n([\s\S]*?)(?=###\s*Level\s*[1-4]|$)/g
  let m
  while ((m = levelRe.exec(block))) {
    perLevel[Number(m[1])] = parseFirstTable(m[2])
  }
  const anchor = perLevel[1] || perLevel[3] || perLevel[2] || perLevel[4]
  if (!anchor || !anchor.length) return null
  const questions = anchor
    .map(([key]) => {
      const options = [1, 2, 3, 4].map((l) => {
        const row = (perLevel[l] || []).find((r) => r[0] === key)
        return { level: l, value: row ? row[1] : '—' }
      })
      return { key, options }
    })
    .filter((q) => q.options.filter((o) => o.value !== '—').length >= 2)
  return questions.length ? { questions } : null
}

// Map a mean severity score (1..4) to its band. Identical thresholds to the API + docs.
export function bandOf(mean) {
  if (mean == null) return { label: '—', cls: '', level: 0 }
  if (mean < 1.75) return { label: 'Mild', cls: 'sev1', level: 1 }
  if (mean < 2.5) return { label: 'Moderate', cls: 'sev2', level: 2 }
  if (mean < 3.25) return { label: 'Severe', cls: 'sev3', level: 3 }
  return { label: 'Refractory / Status', cls: 'sev4', level: 4 }
}

// Score a set of answers against a question list: mean of answered levels + band.
export function scoreOf(ans, questions) {
  const levels = questions.map((q) => ans?.[q.key]).filter(Boolean)
  const mean = levels.length ? levels.reduce((a, b) => a + b, 0) / levels.length : null
  return { answered: levels.length, total: questions.length, mean, band: bandOf(mean) }
}
