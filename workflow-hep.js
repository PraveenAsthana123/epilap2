export const meta = {
  name: 'epilepsy-dba-hep',
  description: 'Author Human Epilepsy Project (HEP) modules 1-5 + integration + reference architecture',
  phases: [{ title: 'HEP' }],
}

const BASE = 'c:/Aman_prod/Epi/docs/hep'

const PREAMBLE = `You are authoring ONE Markdown document for a DBA epilepsy project
"Enterprise AI Platform for Explainable Multimodal Epilepsy Intelligence". EPILEPSY ONLY.
Roles: Neurologist, EEG Technician (plus nurse/neuropsychologist where relevant).

This concerns Dataset 2 = HUMAN EPILEPSY PROJECT (HEP), the PRIMARY (clinical, longitudinal)
dataset that complements the EEG-focused EPILEPSIAE secondary dataset. HEP's example patient is
HEP001: 27-year-old female, focal impaired awareness seizures, suspected temporal lobe
epilepsy, aura = rising epigastric sensation, automatisms = lip smacking, on Levetiracetam,
adherence ~85-95%, left hippocampal sclerosis on MRI, left temporal spikes on EEG, left
temporal hypometabolism on PET, diagnostic confidence 96%. (Do NOT confuse with EP001.)

MANDATORY STANDARD (all required):
1. # H1 title + blockquote with **Why (this doc)** and **How**.
2. Numbered ## research spine IN ORDER: Problem -> Sub-Problems -> Research Problem ->
   Research Objective -> Flow -> Hypotheses -> Statistical Analysis. THEN the module content
   sections (as tables). THEN "Professor Readiness (Defense Q&A)". THEN "References".
3. Every ## and ### heading has a one-line "> **Why:** ... **How:** ..." note.
4. Data in Markdown tables. EVERY table preceded by an italic "*Caption -*" (1-2 lines) on why
   it is present.
5. Include ALL FOUR Mermaid diagrams (fenced \`\`\`mermaid): flowchart TD, sequenceDiagram,
   graph LR (network / integration with EPILEPSIAE), journey. Plain ASCII labels, NO
   parentheses/colons/brackets inside [] node labels.
6. Show how this module integrates with the EPILEPSIAE (EEG) secondary pipeline (fusion).
7. "Professor Readiness (Defense Q&A)": 4-5 examiner questions as ### with concise answers,
   incl. longitudinal-modeling rigor (mixed-effects, survival, leakage) where relevant.
8. "References": APA 7th edition (ILAE/Fisher et al. 2017, Topol 2019, APA 2020, plus
   longitudinal/survival/mixed-model sources where relevant).
AI is decision support only — never autonomous diagnosis/prescription/surgery.
Use the Write tool to save to the EXACT path. Then reply only: "WROTE <path>".`

const DOCS = [
  ['module-1-patient-registration', 'HEP Module 1 - Patient Registration', 'Patient identifier (HEP001), demographics (27F, BMI 22.7, Ontario, married, employed), contact, consent (research/data-sharing/imaging/EEG), insurance, family/social support, socioeconomic index, caregiver support score, access-to-care score, descriptive + inferential stats, feature engineering, feature selection, ML (predict loss-to-follow-up, medication adherence, high-risk patients). Comparison table vs EPILEPSIAE (HEP stronger on social/longitudinal). Note: structured data, deep learning starts after EEG.'],
  ['module-2-neurologist-assessment', 'HEP Module 2 - Comprehensive Neurologist Assessment', 'Visit info, chief complaint, history of present illness, seizure history (age at onset 26, frequency), seizure semiology (aura rising epigastric, automatisms lip smacking, head turning, postictal confusion), triggers (sleep deprivation, stress, non-adherence), past medical history, family history (father epilepsy), medication history (Levetiracetam), comorbidities, neurological examination, differential diagnosis, initial epilepsy classification (focal impaired awareness, temporal lobe epilepsy), management plan. Feature engineering (seizure severity index, trigger burden score, clinical complexity score), feature selection, ML (epilepsy subtype, drug response, recurrence).'],
  ['module-3-diagnostic-investigation', 'HEP Module 3 - Comprehensive Diagnostic Investigation', 'Diagnostic order summary, EEG investigation summary (left temporal spike waves, abnormal), MRI (left hippocampal sclerosis, mild left temporal atrophy, MRI risk index 0.82), CT, PET/SPECT (left temporal hypometabolism), blood investigations + anti-seizure drug monitoring (therapeutic), genetic testing (negative), neuropsychological assessment (mild memory deficit), integrated diagnostic summary, overall diagnostic confidence 96%, multimodal feature engineering (structural lesion score, functional imaging score, multimodal diagnostic score), feature selection, ML (drug-resistant epilepsy, temporal lobe epilepsy, surgical candidacy). This module is the bridge to the secondary EEG pipeline (multimodal transformer fusing clinical+MRI+PET+neuropsych+EEG embeddings).'],
  ['module-4-longitudinal-followup', 'HEP Module 4 - Longitudinal Treatment, Follow-up & Outcome Assessment', 'Follow-up visit info, seizure diary, treatment response (partial response, 75% reduction), medication monitoring (dose change, adherence 95%, therapeutic level), adverse effects, drug-resistance assessment, quality of life (78/100), cognitive progression, mental health, healthcare utilization, surgical evaluation, final outcome (favorable prognosis). Longitudinal example table (baseline->3->6->12 months: seizures 4->0.2, adherence 80->98, QOL 55->91). Time-series dataset, mixed-effects models, survival analysis (Kaplan-Meier, Cox), longitudinal feature engineering (seizure reduction rate, disease progression score), feature selection, ML/DL (LSTM/GRU/Transformer/TFT), predictions (recurrence, drug resistance, seizure freedom).'],
  ['module-5-statistical-predictive-ai', 'HEP Module 5 - Advanced Statistical Modeling, Time-Series & Predictive AI', 'Longitudinal data prep (patient timeline HEP001 visits), missing data analysis + imputation (mean/KNN/multiple imputation/LOCF), descriptive + inferential statistics, longitudinal mixed-effects models (fixed vs random effects), survival analysis (Kaplan-Meier, log-rank, Cox PH, time-dependent Cox), time-series feature engineering (seizure trend slope, QOL trend, adherence stability), feature selection (SHAP/Boruta/LASSO/RFE/MI), classical ML, deep learning (LSTM/GRU/Transformer/TFT/Neural ODE), explainable AI (SHAP/attention/integrated gradients), predictive models (drug resistance, seizure freedom, hospitalization, cognitive decline), model evaluation (ROC-AUC, calibration, Brier), clinical validation (Cohen kappa, ICC), MULTIMODAL FUSION merging HEP clinical timeline + EPILEPSIAE EEG embeddings via multimodal transformer.'],
  ['integration-framework', 'HEP + EPILEPSIAE Cross-Dataset Integration Framework', 'Cross-dataset variable mapping matrix (Age/Gender/Medication/MRI/EEG/Follow-up across EPILEPSIAE, HEP, TUH, PhysioNet, NINDS), gap analysis (HEP strong on longitudinal/medication/QOL; EPILEPSIAE strong on EEG signal), master epilepsy data dictionary (10 sections: demographics, clinical assessment, EEG metadata, signal processing, feature engineering, ML, deep learning, explainability, RAG, governance), unified variable dictionary, unified AI pipeline, external validation strategy (TUH large-scale, PhysioNet reproducibility). This becomes the dissertation core.'],
  ['reference-architecture-20-layers', 'Enterprise Healthcare AI Reference Architecture - 20 Layers', '20 integrated layers L1-L20: L1 Patient & Caregiver, L2 Clinical Assessment, L3 Diagnostic Investigations, L4 EEG Acquisition, L5 Signal Processing (DSP), L6 Feature Engineering, L7 Statistical Analysis, L8 Classical ML, L9 Deep Learning, L10 Multimodal AI, L11 Explainable AI, L12 Multi-Agent Orchestration, L13 RAG & Knowledge Intelligence, L14 MLOps/AIOps, L15 Cybersecurity & Privacy, L16 AI Governance & Compliance, L17 Business Intelligence/Executive Dashboard, L18 Population Health Intelligence, L19 Learning Health System, L20 Healthcare Ecosystem & Global Research. Each layer: focus + outputs. Map HEP + EPILEPSIAE into the layers.'],
].map(([slug, title, points]) => ({ path: `${BASE}/${slug}.md`, title, points }))

phase('HEP')
log(`Authoring ${DOCS.length} HEP docs (modules 1-5 + integration + reference architecture)...`)
const res = await parallel(
  DOCS.map((d) => () =>
    agent(
      `${PREAMBLE}\n\nDOCUMENT TO WRITE\nTitle: ${d.title}\nAbsolute path (Write tool, exact): ${d.path}\nSections/content to cover as tables + diagrams:\n${d.points}`,
      { label: d.path.split('/hep/')[1], phase: 'HEP', agentType: 'general-purpose' }
    )
  )
)
return { requested: DOCS.length, written: res.filter(Boolean).length }
