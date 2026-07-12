// api.test.js — frontend API-client tests with a mocked fetch (positive + negative).
import { describe, it, expect, vi, afterEach } from 'vitest'
import { getScenarios, postScore, apiHealthy } from './api.js'

afterEach(() => { vi.restoreAllMocks() })

describe('api client', () => {
  it('parses scenarios (positive)', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true, json: async () => ({ count: 2, scenarios: [{ id: 'SZ-F02' }] }),
    })
    const r = await getScenarios('Seizure Type')
    expect(r.count).toBe(2)
    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/scenarios?category='))
  })

  it('throws on non-ok score (negative)', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: false, status: 401 })
    await expect(postScore([{ items: [{ level: 3, weight: 1 }] }], 'neurologist'))
      .rejects.toThrow(/401/)
  })

  it('apiHealthy returns false when fetch rejects (negative)', async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error('no server'))
    expect(await apiHealthy()).toBe(false)
  })
})
