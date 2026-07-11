import React, { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'

mermaid.initialize({
  startOnLoad: false,
  securityLevel: 'loose',
  theme: 'base',
  themeVariables: {
    fontFamily: 'inherit',
    primaryColor: '#eef0fe',
    primaryBorderColor: '#4f46e5',
    primaryTextColor: '#1a1f2b',
    lineColor: '#8891a5',
  },
})

let SEQ = 0

export default function Mermaid({ code }) {
  const ref = useRef(null)
  const [err, setErr] = useState(null)

  useEffect(() => {
    let cancelled = false
    const id = 'mmd-' + (SEQ++)
    mermaid
      .render(id, code)
      .then(({ svg }) => {
        if (!cancelled && ref.current) ref.current.innerHTML = svg
      })
      .catch((e) => {
        if (!cancelled) setErr(String(e?.message || e))
      })
    return () => {
      cancelled = true
    }
  }, [code])

  if (err) {
    return (
      <pre className="mermaid-error">Diagram error: {err}
{code}</pre>
    )
  }
  return <div className="mermaid-diagram" ref={ref} />
}
