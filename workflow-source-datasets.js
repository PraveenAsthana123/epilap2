export const meta = {
  name: 'epilepsy-dba-source-datasets',
  description: 'Author source-dataset dossiers: EPILEPSIAE, TUH, PhysioNet, NINDS',
  phases: [{ title: 'Source datasets' }],
}

const BASE = 'c:/Aman_prod/Epi/docs/source-datasets'

const PREAMBLE = `You are authoring ONE Markdown "source-dataset dossier" for a DBA epilepsy
project "Enterprise AI Platform for Explainable Multimodal Epilepsy Intelligence". EPILEPSY
ONLY. Roles: Neurologist, EEG Technician.

Context: the platform uses a MASTER cross-dataset framework. Dataset 1 = EPILEPSIAE (secondary
EEG master), Dataset 2 = Human Epilepsy Project / HEP (primary clinical, already documented in
docs/hep/). This dossier profiles ONE named source dataset and shows how it maps into the
master framework and unified variable dictionary. Be accurate and honest about ACCESS
(open vs registration/DUA vs paid/controlled) and about what is publicly known; do not invent
exact counts you are unsure of — describe scale qualitatively and flag uncertainty.

MANDATORY STANDARD (all required):
1. # H1 title + blockquote with **Why (this doc)** and **How**.
2. Numbered ## research spine IN ORDER: Problem -> Sub-Problems -> Research Problem ->
   Research Objective -> Flow -> Hypotheses -> Statistical Analysis. THEN dataset-profile
   content sections (as tables). THEN "Professor Readiness (Defense Q&A)". THEN "References".
3. Every ## and ### heading has a one-line "> **Why:** ... **How:** ..." note.
4. Data in Markdown tables. EVERY table preceded by an italic "*Caption -*" (1-2 lines).
5. Include ALL FOUR Mermaid diagrams (fenced \`\`\`mermaid): flowchart TD, sequenceDiagram,
   graph LR (integration / variable mapping), journey. Plain ASCII labels, NO
   parentheses/colons/brackets inside [] node labels.
6. Include: a Dataset Profile table (patients, EEG type, sampling rate, electrode system,
   clinical variables, follow-up, access), a Variable-Mapping row showing how it aligns with
   EPILEPSIAE/HEP/master dictionary, its ROLE in the research (master vs external validation
   vs reproducibility vs enrichment), and an Access & Ethics table (how to obtain, consent,
   de-identification).
7. "Professor Readiness (Defense Q&A)": 4-5 examiner questions as ### with concise answers,
   incl. external validity / generalizability / dataset-shift where relevant.
8. "References": APA 7th edition (dataset-appropriate + ILAE/Fisher 2017, Topol 2019, APA 2020,
   Goldberger et al. 2000 for PhysioNet).
AI is decision support only. Use the Write tool to save to the EXACT path. Then reply only:
"WROTE <path>".`

const DOCS = [
  ['dataset-01-epilepsiae', 'Dataset 1 - EPILEPSIAE (Best Overall - Primary+Secondary Master)', 'Overall rating: Primary 5/5, Secondary 5/5, Same-patient YES, Enterprise 5/5. PRIMARY DATA available: Patient ID, Age, Gender, Epilepsy diagnosis, Epilepsy syndrome, Seizure type, ILAE classification, Medication history, Anti-seizure drugs, Age of onset, Disease duration, MRI (some), CT (some), Surgery history (some), Neurologist diagnosis, Seizure diary, Clinical notes (limited), Hospital admission, Follow-up. SECONDARY DATA: Raw EEG, Long-term EEG, Video EEG, EDF files, EEG report, Seizure annotations, Electrode locations, Sampling frequency, Event markers, Artifact labels (some), Recording duration. EPILEPSIAE SAMPLE PATIENT (label it clearly as the EPILEPSIAE cohort example, NOT the platform canonical EP001): 28-year-old female, Temporal Lobe Epilepsy, Levetiracetam, 4 seizures/month, age of onset 19, MRI left hippocampal sclerosis; secondary = 72h Video EEG, 21 channels 512 Hz, sharp waves left temporal. ROLE = secondary EEG master reference AND best overall multimodal source. Access = controlled/paid research license.'],
  ['dataset-03-tuh-eeg', 'Dataset 3 - Temple University Hospital (TUH) EEG Corpus (Best EEG Signal Repository)', 'Rating: Primary 2/5, Secondary 5/5. PRIMARY DATA: Patient ID (de-identified) yes, Age yes, Gender yes, EEG indication yes, Neurologist EEG report yes, Clinical diagnosis limited, Medication rare, Questionnaire NO, Seizure diary NO, Follow-up limited. SECONDARY DATA: Raw EEG yes, EDF yes, EEG report yes, Event annotations (some subsets e.g. TUSZ seizure corpus), Channels yes, Sampling rate yes, Long recordings yes, EEG quality yes. Sub-corpora: seizure (TUSZ), abnormal/normal, artifact, events. Sample patient: 42yo male, EEG indication possible seizure, routine EEG, 21 channels, report normal. ROLE = large-scale external validation + EEG deep learning + explainable EEG. Access = free registration + signed DUA. Emphasize dataset-shift/generalizability.'],
  ['dataset-04-physionet', 'Dataset 4 - PhysioNet (Siena Scalp EEG & CHB-MIT) (Open Reproducibility)', 'Rating: Primary 2/5, Secondary 4/5. PRIMARY DATA: Patient ID yes, Age limited, Gender limited, Diagnosis limited, Clinical notes limited, Medication rare, Questionnaire NO, Neurologist assessment limited. SECONDARY DATA: EEG yes, EDF yes, Seizure annotations yes, Recording metadata yes, Event markers yes, EEG reports (some datasets), Long recordings yes. Siena = adult 512 Hz 10-20 annotated seizures; CHB-MIT = pediatric 256 Hz annotated seizures. Sample: 31yo, diagnosis epilepsy, EEG EDF seizure annotation 256 Hz. A real Siena PN00 metadata sample is already in data/siena-sample. ROLE = open reproducibility + benchmarking seizure-detection/signal-processing algorithms. Access = OPEN (PhysioNet).'],
  ['dataset-05-ninds', 'Dataset 5 - NINDS Repositories & Epilepsy Cohorts (Clinical/Multimodal Enrichment)', 'Rating: Primary 4/5, Secondary 4/5. PRIMARY DATA: Patient demographics yes, Age yes, Gender yes, Medical history yes, Family history some, Medication yes, Diagnosis yes, Neurologist assessment some, Clinical scales some, MRI some, Laboratory tests some. SECONDARY DATA: EEG yes, MRI yes, CT some, Genomics some, Biomarkers some, EEG reports some. Sample: 36yo, Carbamazepine, focal epilepsy, routine EEG, MRI, EDF, EEG report. ROLE = multimodal clinical research enrichment with additional imaging + biomarker + genomic data + additional external cohorts. Access = controlled application. Be honest about variable heterogeneity across cohorts.'],
  ['comparison-matrix', 'Cross-Dataset Comparison Matrix & DBA Selection Strategy', 'A full comparison matrix table across EPILEPSIAE, HEP, NINDS, TUH, PhysioNet for each data element (Age, Gender, Symptoms, Neurologist Assessment, Medication, Seizure History, Family History, MRI, Quality of Life, Depression/Anxiety, EEG, Video EEG, EDF Files, EEG Reports, Seizure Annotations, Longitudinal Follow-up) using values full/some/limited/rare/none. A DBA ranking table (1 EPILEPSIAE 5+5, 2 HEP 5+5, 3 NINDS 4+4, 4 TUH 2+5, 5 PhysioNet 2+4) with Best-Use column. The HYBRID DATASET STRATEGY: use EPILEPSIAE or HEP as primary multimodal source, TUH + PhysioNet for external validation of EEG models, and compare Primary-only vs EEG-only vs Multimodal to demonstrate fusion value (maps to hypotheses H1/H2/H3). Access-feasibility overlay. This is a dissertation chapter.'],
].map(([slug, title, points]) => ({ path: `${BASE}/${slug}.md`, title, points }))

phase('Source datasets')
log(`Authoring ${DOCS.length} source-dataset dossiers (EPILEPSIAE, TUH, PhysioNet, NINDS)...`)
const res = await parallel(
  DOCS.map((d) => () =>
    agent(
      `${PREAMBLE}\n\nDOCUMENT TO WRITE\nTitle: ${d.title}\nAbsolute path (Write tool, exact): ${d.path}\nContent to cover as tables + diagrams:\n${d.points}`,
      { label: d.path.split('/source-datasets/')[1], phase: 'Source datasets', agentType: 'general-purpose' }
    )
  )
)
return { requested: DOCS.length, written: res.filter(Boolean).length }
