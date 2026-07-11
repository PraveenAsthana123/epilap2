export const meta = {
  name: 'epilepsy-dba-roles-study',
  description: 'Per-role docs covering retrospective + prospective study design, with matrices',
  phases: [{ title: 'Roles' }],
}

const BASE = 'c:/Aman_prod/Epi/docs/roles-study'

const PREAMBLE = `You are authoring ONE Markdown document for a DBA epilepsy project
"Enterprise AI Platform for Explainable Multimodal Epilepsy Intelligence". EPILEPSY ONLY.
Canonical patients: EP001 (29M focal, primary-assessment) and HEP001 (27F temporal-lobe).

This doc is a ROLE dossier: for ONE clinical role, document their assessments/tasks and how
their data participates in BOTH a RETROSPECTIVE study (analyze existing historical records)
and a PROSPECTIVE study (forward enrollment + follow-up data collection). Both study types are
MANDATORY and must each have their own section plus a comparison matrix.

MANDATORY STANDARD (all required):
1. # H1 title + blockquote with **Why (this doc)** and **How**.
2. Numbered ## research spine IN ORDER: Problem -> Sub-Problems -> Research Problem ->
   Research Objective -> Flow -> Hypotheses -> Statistical Analysis. THEN role content. THEN
   "Professor Readiness (Defense Q&A)". THEN "References".
3. Every ## and ### heading has a one-line "> **Why:** ... **How:** ..." note.
4. Data in Markdown tables. EVERY table preceded by an italic "*Caption -*" (1-2 lines).
5. Include ALL FOUR Mermaid diagrams (fenced \`\`\`mermaid): flowchart TD, sequenceDiagram,
   graph LR, journey. Plain ASCII labels, NO parentheses/colons/brackets inside [] labels.
   ALSO include a C4-style model (Context/Container/Component) as a Mermaid \`graph\` showing
   how this role interacts with the platform systems. AND after EVERY diagram/matrix/accuracy
   figure, add a detailed prose explanation with these labeled lines: **Reason:** ...
   **Why:** ... **What is happening:** ... **How it is happening:** ... **Reference:** ...
6. REQUIRED role sections: (a) Role assessments & tasks table; (b) RETROSPECTIVE STUDY design
   for this role (data source = existing records, design, sample, variables, analysis, bias
   controls); (c) PROSPECTIVE STUDY design (forward enrollment, endpoints, follow-up schedule,
   consent); (d) a RETROSPECTIVE vs PROSPECTIVE MATRIX for this role (rows: time direction,
   data source, cost, bias risk, causal strength, ethics/consent, best use); (e) role KPIs.
7. "Professor Readiness (Defense Q&A)": 4-5 examiner questions (incl. why both study types,
   selection/recall bias, confounding, when to prefer each).
8. "References": APA 7th edition (study-design sources + ILAE/Fisher 2017, Topol 2019, APA 2020).
AI is decision support only. Use the Write tool to save to the EXACT path. Reply only:
"WROTE <path>".`

const ROLES = [
  ['neurologist', 'Neurologist', 'Clinical assessment, diagnosis, medication decisions, follow-up. Retrospective: chart review of prior neurologist assessments to model risk. Prospective: enroll new patients, standardized structured intake, follow seizure outcomes.'],
  ['eeg-technician', 'EEG Technician', 'EEG acquisition, impedance/QC, artifact management. Retrospective: analyze archived EEG QC metadata. Prospective: standardized acquisition protocol with real-time QC capture.'],
  ['nurse', 'Epilepsy Nurse', 'Medication adherence, safety counselling, follow-up coordination. Retrospective: adherence records review. Prospective: adherence intervention with follow-up.'],
  ['patient', 'Patient', 'Symptoms, seizure diary, PROs, app engagement. Retrospective: historical diary/PRO data. Prospective: app-based daily monitoring cohort. No diagnosis claims.'],
  ['caregiver', 'Caregiver', 'Seizure observation, emergency response, adherence support. Retrospective: caregiver-reported event logs. Prospective: caregiver alerting cohort.'],
  ['administrator', 'Administrator', 'Operational KPIs (onboarding time, throughput, cost). Retrospective: historical operational data. Prospective: before/after AI-deployment operational study.'],
  ['neuropsychologist', 'Neuropsychologist', 'Cognition, memory, mood, QoL assessment. Retrospective: archived neuropsych scores. Prospective: longitudinal cognitive follow-up cohort.'],
  ['pharmacist', 'Pharmacist', 'ASM review, interactions, therapeutic drug monitoring, pharmacogenomics. Retrospective: dispensing + drug-level records. Prospective: medication-optimization cohort.'],
].map(([slug, role, points]) => ({ path: `${BASE}/role-${slug}-study.md`, title: `Role Study - ${role} (Retrospective + Prospective)`, points }))

const MASTER = {
  path: `${BASE}/study-design-master.md`,
  title: 'Study Design Master - Retrospective vs Prospective (All Roles)',
  points: 'Master comparison of retrospective vs prospective study designs across ALL roles (Neurologist, EEG Technician, Nurse, Patient, Caregiver, Administrator, Neuropsychologist, Pharmacist). Include a ROLE x STUDY-TYPE matrix. Explain the HYBRID design: retrospective data for algorithm development/training, prospective data for external validation and clinical impact (before/after). Map to hypotheses H1 (primary), H2 (EEG), H3 (multimodal), H5 (enterprise/operational). Cover bias (selection, recall, confounding), ethics/consent differences, cost/time trade-offs, and when to prefer each.',
}

const ALL = [MASTER, ...ROLES]

phase('Roles')
log(`Authoring ${ALL.length} role/study docs (retrospective + prospective)...`)
const res = await parallel(
  ALL.map((d) => () =>
    agent(
      `${PREAMBLE}\n\nDOCUMENT TO WRITE\nTitle: ${d.title}\nAbsolute path (Write tool, exact): ${d.path}\nContent to cover as tables + diagrams:\n${d.points}`,
      { label: d.path.split('/roles-study/')[1], phase: 'Roles', agentType: 'general-purpose' }
    )
  )
)
return { requested: ALL.length, written: res.filter(Boolean).length }
