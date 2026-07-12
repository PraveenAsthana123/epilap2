// csv.test.js — parser + profiler tests (positive + negative).
import { describe, it, expect } from 'vitest'
import { parseCSV, profile } from './csv.js'

describe('parseCSV', () => {
  it('parses headers + rows (positive)', () => {
    const { headers, rows } = parseCSV('a,b\n1,x\n2,y\n')
    expect(headers).toEqual(['a', 'b'])
    expect(rows).toEqual([{ a: '1', b: 'x' }, { a: '2', b: 'y' }])
  })
  it('handles quoted fields with commas (negative: comma must not split)', () => {
    const { rows } = parseCSV('id,note\n1,"hello, world"\n')
    expect(rows[0].note).toBe('hello, world')
  })
})

describe('profile', () => {
  it('detects numeric vs categorical', () => {
    const { headers, rows } = parseCSV('age,sex\n29,M\n40,F\n')
    const cols = profile(headers, rows)
    const age = cols.find((c) => c.name === 'age')
    const sex = cols.find((c) => c.name === 'sex')
    expect(age.numeric).toBe(true)
    expect(age.min).toBe(29); expect(age.max).toBe(40)
    expect(sex.numeric).toBe(false)         // negative: not numeric
    expect(sex.unique).toBe(2)
  })
})
