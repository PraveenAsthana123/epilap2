// scoring.test.js — Vitest unit tests for the viewer scoring logic (positive + negative).
import { describe, it, expect } from 'vitest'
import { parseFirstTable, parseSeverity, bandOf, scoreOf } from './scoring.js'

const SAMPLE = `# Section 3

| Variable | Value |
|---|---|
| Frequency | 5/month |

## Severity Scenario Model — Neurologist View

### Level 1 — Mild
| Variable | Value |
|---|---|
| Frequency | <1/year |
| Awareness | Retained |

### Level 2 — Moderate
| Variable | Value |
|---|---|
| Frequency | 1/month |
| Awareness | Impaired |

### Level 3 — Severe — EP001
| Variable | Value |
|---|---|
| Frequency | 5/month |
| Awareness | Impaired |

### Level 4 — Refractory / Status
| Variable | Value |
|---|---|
| Frequency | every ~5 min |
| Awareness | Impaired |

### Severity Classification Logic
\`\`\`mermaid
flowchart TD
A --> B
\`\`\`
`

describe('bandOf', () => {
  it('maps means to the correct band (positive)', () => {
    expect(bandOf(1.0).level).toBe(1)
    expect(bandOf(2.0).level).toBe(2)
    expect(bandOf(3.0).level).toBe(3)
    expect(bandOf(4.0).level).toBe(4)
  })
  it('respects boundaries (negative: no round-up)', () => {
    expect(bandOf(2.49).level).toBe(2)   // must NOT be 3
    expect(bandOf(3.24).level).toBe(3)   // must NOT be 4
  })
  it('handles no answers', () => {
    expect(bandOf(null).level).toBe(0)
  })
})

describe('parseSeverity', () => {
  it('extracts questions with 4 level-options each (positive)', () => {
    const q = parseSeverity(SAMPLE)
    expect(q).not.toBeNull()
    expect(q.questions.length).toBe(2)
    const freq = q.questions.find((x) => x.key === 'Frequency')
    expect(freq.options.map((o) => o.level)).toEqual([1, 2, 3, 4])
    expect(freq.options[2].value).toContain('5/month')  // Level 3 = EP001
  })
  it('returns null when there is no severity model (negative)', () => {
    expect(parseSeverity('# Section\n\nno model here')).toBeNull()
  })
  it('does not parse the main table above the model', () => {
    const q = parseSeverity(SAMPLE)
    // Only the severity-model variables become questions, not stray rows.
    expect(q.questions.every((x) => ['Frequency', 'Awareness'].includes(x.key))).toBe(true)
  })
})

describe('scoreOf', () => {
  const questions = parseSeverity(SAMPLE).questions
  it('averages answered levels and bands them (positive)', () => {
    const s = scoreOf({ Frequency: 3, Awareness: 4 }, questions)
    expect(s.answered).toBe(2)
    expect(s.mean).toBeCloseTo(3.5)
    expect(s.band.level).toBe(4)
  })
  it('ignores unanswered items (negative / partial)', () => {
    const s = scoreOf({ Frequency: 1 }, questions)
    expect(s.answered).toBe(1)
    expect(s.band.level).toBe(1)
  })
  it('returns null mean for no answers', () => {
    expect(scoreOf({}, questions).mean).toBeNull()
  })
})

describe('parseFirstTable', () => {
  it('drops header + separator, keeps data rows', () => {
    const rows = parseFirstTable('| A | B |\n|---|---|\n| x | y |\n| p | q |\n')
    expect(rows).toEqual([['x', 'y'], ['p', 'q']])
  })
})
