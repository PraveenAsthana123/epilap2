export const meta = {
  name: 'epilepsy-dba-datasets',
  description: 'Author dataset docs 18-25 to the 18-rule canonical standard',
  phases: [{ title: 'Datasets' }],
}

const BASE = 'c:/Aman_prod/Epi/docs/datasets'

const PREAMBLE = `You are authoring ONE Markdown "dataset dossier" document for a DBA epilepsy
project "Enterprise AI Platform for Explainable Multimodal Epilepsy Intelligence". EPILEPSY
ONLY (never schizophrenia/PANSS). Roles: Neurologist, EEG Technician. Reference test patient
EP001 in examples where natural (29yo male, focal impaired awareness, left-temporal focus).

The doc describes a DATA DICTIONARY / dataset schema for an epilepsy AI platform. Present the
dataset's sections as Markdown tables (Field | Description/Example rows). Also list the output
files and applicable AI models.

MANDATORY STANDARD (all required):
1. # H1 title + blockquote with **Why (this doc)** and **How**.
2. Numbered ## research spine sections IN ORDER: Problem -> Sub-Problems -> Research Problem ->
   Research Objective -> Flow -> Hypotheses -> Statistical Analysis. THEN the dataset content
   sections (as tables). THEN "Professor Readiness (Defense Q&A)". THEN "References".
3. Every ## and ### heading has a one-line "> **Why:** ... **How:** ..." note.
4. Data in Markdown tables. EVERY table preceded by an italic "*Caption -*" line (1-2 lines)
   on why that table is present.
5. Include ALL FOUR Mermaid diagrams (each fenced \`\`\`mermaid):
   - flowchart TD (data flow through the dataset)
   - sequenceDiagram (roles/systems interacting)
   - graph LR (network of dataset entities / integration with other datasets)
   - journey (patient or data journey)
   Plain ASCII node labels, NO parentheses/colons/brackets inside [] labels.
6. A "Dataset Integration" table showing how this dataset links to other platform datasets.
7. "Professor Readiness (Defense Q&A)": 4-5 examiner questions as ### with concise answers.
   Include ethics/privacy/consent and "decision support not autonomous decision" framing.
8. "References": APA 7th edition (ILAE/Fisher et al. 2017, Topol 2019, APA 2020, plus
   topic-appropriate genetics/imaging/ICU/public-health sources).
AI must never autonomously diagnose, prescribe, or recommend surgery — decision support only.
Use the Write tool to save to the EXACT absolute path given. Then reply only:
"WROTE <path>".`

const DATASETS = [
  ['dataset-18-remote-monitoring', 'Dataset 18 - Remote Monitoring & Clinical Recommendation', 'Patient monitoring profile, continuous EEG stream, seizure detection, seizure frequency & severity trends, brain localization (probability per region), surgical evaluation SUPPORT (never recommends surgery), medication monitoring, remote alerts, caregiver dashboard, neurologist dashboard, risk prediction/forecast with uncertainty, recommendation engine, AI safety rules (must not recommend removing a brain region or change dose autonomously), output files.'],
  ['dataset-19-wearable-digital-biomarker', 'Dataset 19 - Multimodal Wearable & Digital Biomarker', 'Wearable device info, EEG features, cardiac (HR/HRV/ECG), oxygen SpO2, respiration, movement (accelerometer/gyroscope/fall/tremor), sleep stages, circadian/seizure timing, medication adherence, lifestyle, environment, patient-reported outcomes, caregiver report, AI multimodal fusion, seizure risk prediction, personalized digital biomarker score, longitudinal trend, AI recommendations, dashboard, output files, AI models (multimodal/temporal fusion transformer, GNN, LSTM, survival, Bayesian).'],
  ['dataset-20-neuroimaging', 'Dataset 20 - Neuroimaging & Brain Mapping (MRI/fMRI/PET/CT/DTI)', 'Patient/study info, MRI metadata (T1/T2/FLAIR/SWI), brain regions (frontal/temporal/parietal/occipital/limbic/deep), lesion dataset & measurements, hippocampal volumes/sclerosis, cortical thickness, DTI (FA/MD), fMRI connectivity, PET FDG uptake/hypometabolism, brain connectivity metrics, brain atlas (AAL/Desikan), EEG-MRI fusion, surgical planning SUPPORT, AI localization probability per region (left temporal 92% for EP001), longitudinal imaging, AI models (3D CNN, U-Net/nnU-Net, ViT, GNN, multimodal transformer), output files.'],
  ['dataset-21-neuropsychology', 'Dataset 21 - Neuropsychology, Cognitive & Mental Health', 'Patient profile, cognition, intelligence (IQ indices), memory (immediate/delayed/verbal/visual/working), attention, executive function, language, processing speed, mood (depression/anxiety), sleep, quality of life (QOLIE-31), functional independence, behavior, medication cognitive impact, caregiver assessment, surgical neuropsychology (language dominance, memory risk), longitudinal cognitive trend, AI fusion/outputs (cognitive/memory/depression risk), standardized instruments table (MoCA, WMS, WCST, Trail Making, Boston Naming, PHQ-9, GAD-7, QOLIE-31), output files.'],
  ['dataset-22-genomics-precision-medicine', 'Dataset 22 - Genomics, Precision Medicine & Biomarker', 'Patient genetics, family history, whole genome/exome sequencing, epilepsy gene panel (SCN1A, SCN2A, KCNQ2, DEPDC5, STXBP1, CDKL5, PCDH19, TSC1/2), variant dataset (ACMG/ClinVar), copy number variants, pharmacogenomics (HLA-Carbamazepine, CYP2C9-Phenytoin, POLG-Valproate), drug response, blood/inflammatory/metabolic/CSF biomarkers, proteomics, metabolomics, transcriptomics, precision medicine score, multi-omics integration, AI biomarker discovery, personalized recommendation SUPPORT (genetics consult, not autonomous), output files, AI models (GNN, multimodal transformer, Bayesian, survival, multi-task).'],
  ['dataset-23-epilepsy-surgery', 'Dataset 23 - Epilepsy Surgery, Intraoperative Monitoring & Neuromodulation', 'Surgical candidate, drug-resistant epilepsy, presurgical evaluation, video EEG, stereo EEG (SEEG), electrocorticography (ECoG), functional brain mapping, electrical stimulation mapping, multimodal fusion, epileptogenic zone probability, surgical planning, neuromodulation (VNS/RNS/DBS), LITT, surgical procedures (temporal lobectomy, hemispherectomy, callosotomy), intraoperative monitoring (MEP/SSEP), complications, postoperative outcome, Engel classification, ILAE surgical outcome, AI surgical decision SUPPORT (summarize evidence, refer to MDT conference, never recommend surgery), AI outcome prediction with uncertainty, output files.'],
  ['dataset-24-icu-continuous-eeg', 'Dataset 24 - ICU, Continuous Video EEG (cEEG) & Critical Care', 'ICU admission (APACHE/SOFA/GCS), continuous EEG (24-120h, seizure burden, burst suppression), continuous video EEG, ICU vital signs (ICP/CPP), mechanical ventilation, sedation (BIS/suppression ratio), status epilepticus (convulsive/non-convulsive/refractory), acute stroke, TBI, intracranial hemorrhage, cardiac arrest monitoring, neonatal ICU (HIE), laboratory, ICU imaging, AI streaming/continuous monitoring, early warning events, alert prioritization (critical/high/medium/low), brain wave trends (alpha-delta ratio, spectral edge), medication response, ICU outcomes (GOS/mRS), AI risk scores, AI recommendation support, remote ICU dashboard, AI models (1D CNN, EEGNet, transformer, TFT, GNN, survival, Bayesian), output files.'],
  ['dataset-25-population-health-registry', 'Dataset 25 - Population Health, National Epilepsy Registry & Public Health', 'Registry info, population demographics, epidemiology (incidence/prevalence/drug-resistant/mortality), disease classification, seizure burden, healthcare utilization, medication registry, surgery registry, outcome registry, mortality (SUDEP), disability, quality indicators (time to diagnosis/EEG/MRI), AI registry (accuracy/override/fairness), wearable registry, public health surveillance, geographic analytics, AI population dashboard, quality improvement targets, international benchmarking, research registry, health economics (cost per patient, QALYs, ICER), AI population risk stratification, executive dashboards (Ministry of Health, Hospital), AI models (time-series forecasting, spatial analysis, survival, causal inference, GNN, foundation models), output files.'],
].map(([slug, title, points]) => ({ path: `${BASE}/${slug}.md`, title, points }))

phase('Datasets')
log(`Authoring ${DATASETS.length} dataset dossiers (18-25) to canonical standard...`)
const res = await parallel(
  DATASETS.map((d) => () =>
    agent(
      `${PREAMBLE}\n\nDOCUMENT TO WRITE\nTitle: ${d.title}\nAbsolute path (Write tool, exact): ${d.path}\nSections/content to cover as tables + diagrams:\n${d.points}`,
      { label: d.path.split('/datasets/')[1], phase: 'Datasets', agentType: 'general-purpose' }
    )
  )
)
return { requested: DATASETS.length, written: res.filter(Boolean).length }
