// Retrofit the early primary-assessment raw-data files (and the scorecard) to the full
// canonical standard. These were authored before the diagram/APA7 standard existed.
// Each agent reads the file, PRESERVES its data table, and adds the mandatory elements.
export const meta = {
  name: 'epilepsy-dba-retrofit-primary',
  description: 'Upgrade 26 primary-assessment/scorecard docs to the full canonical standard',
  phases: [{ title: 'Retrofit primary' }],
}

const D = 'c:/Aman_prod/Epi/docs'

const PREAMBLE = `You are upgrading ONE existing small Markdown data-capture doc for a DBA
epilepsy project. EPILEPSY ONLY. Canonical patient EP001 (29M, focal impaired awareness,
left-temporal). Read the file at the given path, PRESERVE its existing data table(s) and
values verbatim, and REWRITE it to meet this standard, then Write back to the SAME path.

STANDARD:
1. Keep the existing H1 and the data table(s) unchanged.
2. Add a top blockquote: **Why (this doc):** ... **How:** ...
3. Add short **Problem** and **Research Objective** lines (research spine, kept brief for a
   data-capture doc).
4. Precede every table with an italic "*Caption -*" (1-2 lines) on why it is present.
5. Add ALL FOUR Mermaid diagrams (fenced \`\`\`mermaid): flowchart TD (where this data flows
   in the pipeline), sequenceDiagram (role capturing it), graph LR (how it links to other
   assessment sections / the clinical vector), journey (patient/role experience for this item).
   Plain ASCII labels, NO parentheses/colons/brackets inside [] node labels. After each diagram
   add: **Reason:** ... **Why:** ... **What is happening:** ... **How it is happening:** ...
   **Reference:** ...
6. Add a "Professor Readiness (Defense Q&A)" section: 3 short examiner questions + answers.
7. Add a "References" section: APA 7th edition (ILAE/Fisher et al. 2017; Topol 2019; APA 2020).
Keep it concise but fully compliant. Then reply only: "RETROFIT <path>".`

const NEURO = ['01-chief-complaint','02-history-present-illness','03-seizure-history','04-aura',
  '05-during-seizure','06-post-ictal','07-trigger-assessment','08-medication-history',
  '09-past-medical-history','10-family-history','11-lifestyle','12-neurological-examination',
  '13-functional-assessment','14-quality-of-life','15-impression']
  .map(s => `${D}/primary-assessment/neurologist/${s}.md`)

const TECH = ['01-patient-preparation','02-eeg-setup','03-electrode-quality',
  '04-recording-conditions','05-artifact-risk','06-technician-notes']
  .map(s => `${D}/primary-assessment/eeg-technician/${s}.md`)

const OTHER = [
  `${D}/primary-assessment/00-patient-summary.md`,
  `${D}/primary-assessment/ai-derived-features.md`,
  `${D}/primary-assessment/roles-neurologist.md`,
  `${D}/primary-assessment/roles-eeg-technician.md`,
  `${D}/dataset-scorecard.md`,
]

const FILES = [...NEURO, ...TECH, ...OTHER]

phase('Retrofit primary')
log(`Retrofitting ${FILES.length} primary-assessment/scorecard docs to full standard...`)
const res = await parallel(
  FILES.map((p) => () =>
    agent(`${PREAMBLE}\n\nFILE: ${p}`,
      { label: p.split('/docs/')[1], phase: 'Retrofit primary', agentType: 'general-purpose' })
  )
)
return { requested: FILES.length, done: res.filter(Boolean).length }
