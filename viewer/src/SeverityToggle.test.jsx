// SeverityToggle.test.jsx — real component/button test (render + click) with jsdom.
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import SeverityToggle from './SeverityToggle.jsx'

describe('SeverityToggle (button/frontend test)', () => {
  it('renders four level buttons', () => {
    render(<SeverityToggle value={null} onSelect={() => {}} />)
    expect(screen.getByRole('button', { name: /L1 Mild/ })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /L4 Refractory/ })).toBeInTheDocument()
  })

  it('fires onSelect with the clicked level (positive)', () => {
    const onSelect = vi.fn()
    render(<SeverityToggle value={null} onSelect={onSelect} />)
    fireEvent.click(screen.getByRole('button', { name: /L3 Severe/ }))
    expect(onSelect).toHaveBeenCalledWith(3)
  })

  it('marks the selected button pressed, others not (negative)', () => {
    render(<SeverityToggle value={2} onSelect={() => {}} />)
    expect(screen.getByRole('button', { name: /L2 Moderate/ })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('button', { name: /L1 Mild/ })).toHaveAttribute('aria-pressed', 'false')
  })
})
