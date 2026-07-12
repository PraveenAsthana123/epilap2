// SeverityToggle.jsx — a small, self-contained interactive control:
// four severity-level buttons (L1..L4). Selecting one highlights it and fires
// onSelect(level). Extracted as a testable unit for button/component tests.
import React from 'react'

const LEVELS = [
  { level: 1, label: 'Mild' },
  { level: 2, label: 'Moderate' },
  { level: 3, label: 'Severe' },
  { level: 4, label: 'Refractory/Status' },
]

export default function SeverityToggle({ value, onSelect }) {
  return (
    <div className="sevtoggle" role="group" aria-label="Severity level">
      {LEVELS.map((l) => (
        <button
          key={l.level}
          type="button"
          aria-pressed={value === l.level}
          className={'opt' + (value === l.level ? ' sel sev' + l.level : '')}
          onClick={() => onSelect(l.level)}
        >
          <b>L{l.level}</b> {l.label}
        </button>
      ))}
    </div>
  )
}
