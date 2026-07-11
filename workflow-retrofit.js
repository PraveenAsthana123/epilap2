export const meta = {
  name: 'epilepsy-dba-retrofit',
  description: 'Retrofit existing blueprint docs to the 18-rule canonical standard',
  phases: [{ title: 'Retrofit' }],
}

const BASE = 'c:/Aman_prod/Epi/docs'

const PREAMBLE = `You are upgrading ONE existing Markdown doc for a DBA epilepsy project
"Enterprise AI Platform for Explainable Multimodal Epilepsy Intelligence". EPILEPSY ONLY
(never schizophrenia/PANSS). Roles: Neurologist, EEG Technician. Test patient EP001.

TASK: Read the existing file at the given path, PRESERVE its factual content/tables, and
REWRITE it to meet this mandatory standard, then save with the Write tool to the SAME path.

STANDARD:
1. Keep the existing H1 title and all real content/tables.
2. Add, near the top, a blockquote with **Why (this doc)** and **How**.
3. Add a research-spine framing where sensible: short Problem / Research Objective notes.
4. Under every ## and ### heading add a one-line "> **Why:** ... **How:** ..." note.
5. Precede EVERY table with an italic "*Caption -*" line (1-2 lines) on why it is present.
6. Add ALL FOUR Mermaid diagrams (fenced \`\`\`mermaid): flowchart TD, sequenceDiagram,
   graph LR (network), journey. Plain ASCII node labels, no parentheses/colons inside [].
7. Add a "Professor Readiness (Defense Q&A)" section: 3-4 examiner questions as ### with
   concise answers.
8. Add a "References" section with APA 7th edition entries (ILAE/Fisher et al. 2017, Topol
   2019, APA 2020, plus topic-appropriate).
After writing reply only: "RETROFIT <path>".`

const FILES = [
  ['00-overview.md', 'Overview / three contributions / five pillars'],
  ['part1-business-problem.md', 'Business problem, research questions, gap, conceptual framework'],
  ['part2-methodology.md', 'Research design, data, variables, hypotheses'],
  ['pipeline-a-primary-assessment.md', 'Primary assessment AI 16-phase summary'],
  ['pipeline-b-eeg.md', 'Secondary EEG AI 16-phase summary'],
  ['pipeline-c-multimodal.md', 'Multimodal fusion (the novel contribution)'],
  ['pipeline-d-enterprise-platform.md', 'Enterprise platform 12 layers + multi-agent'],
  ['pipeline-e-evaluation.md', 'Enterprise evaluation 15 layers + scorecard'],
  ['part4-implementation.md', 'Azure/hybrid architecture, multi-agent, implementation'],
  ['part5-8-results-conclusion.md', 'Evaluation chapters, results, discussion, conclusion'],
  ['appendix.md', 'Instruments, risk register, model registry'],
  ['publication-strategy.md', 'Six-paper Q1 output plan'],
]

phase('Retrofit')
log(`Retrofitting ${FILES.length} blueprint docs to canonical standard...`)
const res = await parallel(
  FILES.map(([f, desc]) => () =>
    agent(
      `${PREAMBLE}\n\nFILE: ${BASE}/${f}\nWHAT IT COVERS: ${desc}`,
      { label: f, phase: 'Retrofit', agentType: 'general-purpose' }
    )
  )
)
return { requested: FILES.length, done: res.filter(Boolean).length }
