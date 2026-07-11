export const meta = {
  name: 'epilepsy-dba-docs',
  description: 'Fan out one agent per remaining DBA epilepsy doc, each to the 18-rule canonical standard',
  phases: [
    { title: 'Pipeline A' },
    { title: 'Pipeline B' },
    { title: 'Stakeholders' },
    { title: 'Gap docs' },
  ],
}

const BASE = 'c:/Aman_prod/Epi/docs'

// Shared standard every agent must follow.
const PREAMBLE = `You are authoring ONE Markdown document for a DBA dissertation project titled
"Enterprise AI Platform for Explainable Multimodal Epilepsy Intelligence".

TOPIC IS EPILEPSY ONLY. Never mention schizophrenia/PANSS/psychiatry. Roles are Neurologist
and EEG Technician. Test patient = EP001 (EP-2026-001): 29yo male, focal impaired awareness
epilepsy, 5 seizures/month, 90s duration, nocturnal, aura (metallic taste, deja vu), on
Levetiracetam 1000mg BID, adherence 88%, 3 missed doses/month, breakthrough seizures,
previous drug failure carbamazepine, sleep 5.2h poor, trigger burden 4 (high), driving
restricted, QOLIE-31 56/100; EEG pre-assessment 21 electrodes 10-20 system, 512 Hz, average
impedance 3.1 kOhm, low artifact risk, EEG readiness 98%.

MANDATORY STANDARD (all required, in this order where applicable):
1. Title (# H1) + a blockquote with **Why (this doc)** and **How**.
2. Research spine as numbered ## sections IN ORDER: Problem -> Sub-Problems -> Research
   Problem -> Research Objective -> Flow -> Hypotheses -> Statistical Analysis. Then topic
   content sections. Then "Professor Readiness (Defense Q&A)". Then "References".
3. Every ## and ### heading has a one-line "> **Why:** ... **How:** ..." note under it.
4. Data in Markdown tables. EVERY table is preceded by a 1-2 line caption in italics starting
   "*Caption -*" explaining why that table is present.
5. Every major step explained with BOTH a table AND a flowchart.
6. Include ALL FOUR Mermaid diagrams (each in a \`\`\`mermaid fenced block):
   - flowchart:  flowchart TD  (nodes: A[Text] --> B[Text]; decisions: X{Q?} -- Yes --> Y)
   - sequence:   sequenceDiagram  (participant X as Name; X->>Y: msg; Y-->>X: reply)
   - network:    graph LR  (A[Text] --> B[Text])
   - journey:    journey  (title ...; section Name;  Task: 4: Actor)
   Keep Mermaid node text plain ASCII, no parentheses/colons inside [] labels.
7. "Professor Readiness (Defense Q&A)": 4-5 hypothetical examiner questions as ### headings,
   each answered concisely with a short paragraph, table, or small flowchart.
8. "References": APA 7th edition entries (real, plausible epilepsy/AI sources: ILAE/Fisher
   et al. 2017, Topol 2019, APA 2020, plus topic-appropriate ones). Hanging-indent not needed.

Write clean, professional, defensible content. Be specific to EPILEPSY and EP001 where
relevant. Use the Write tool to save the file to the EXACT absolute path given. After writing,
reply with just: "WROTE <path> (<n> sections, 4 diagrams)".`

function spec(path, title, kind, points, phase) {
  return { path, title, kind, points, phase }
}

const PIPELINE_A = [
  spec(`${BASE}/pipeline-a/phase-03-data-cleaning.md`, 'Pipeline A Phase 3 - Data Cleaning (Epilepsy, EP001)', 'primary clinical', 'Fix invalid values (impossible age, adherence >100%), standardize medication names (Keppra->Levetiracetam), unit conversion (min->sec), missing-value decisions (never silently impute clinical fields), resolve logical conflicts (freq 0 but recent seizure), cleaning audit log table.'),
  spec(`${BASE}/pipeline-a/phase-04-clinical-standardization.md`, 'Pipeline A Phase 4 - Clinical Standardization (Epilepsy, EP001)', 'primary clinical', 'Coding standards (ICD-10 G40.x, SNOMED), controlled vocabularies for seizure type per ILAE 2017, unit normalization, reference ranges, data model / schema for standardized record.'),
  spec(`${BASE}/pipeline-a/phase-06-statistical-analysis.md`, 'Pipeline A Phase 6 - Statistical Analysis (Epilepsy, EP001)', 'primary clinical', 'Hypotheses & null/alt, normality (Shapiro-Wilk), t-test/Mann-Whitney, ANOVA/Kruskal-Wallis, chi-square, correlation Pearson/Spearman, regression predicting seizure frequency, effect size (Cohen d), 95% CI, multiple-testing correction (Benjamini-Hochberg), clinical interpretation.'),
  spec(`${BASE}/pipeline-a/phase-07-data-transformation.md`, 'Pipeline A Phase 7 - Data Transformation for ML (Epilepsy, EP001)', 'primary clinical', 'Define target (high seizure burden), train/test split BEFORE scaling (patient-level, no leakage), one-hot/ordinal encoding, normalization vs standardization, log-transform skewed seizure frequency, class imbalance (class weights/SMOTE), save transformation pipeline, leakage checks.'),
  spec(`${BASE}/pipeline-a/phase-08-feature-engineering.md`, 'Pipeline A Phase 8 - Feature Engineering (Epilepsy, EP001)', 'primary clinical', 'Derive clinical features: disease duration, seizure burden (freq x duration=450), trigger burden score, sleep deficit, medication features, functional/injury risk, EEG readiness index, time-since-last-seizure, composite seizure risk score, interaction features, feature dictionary.'),
  spec(`${BASE}/pipeline-a/phase-09-feature-selection.md`, 'Pipeline A Phase 9 - Feature Selection (Epilepsy, EP001)', 'primary clinical', 'Remove administrative/constant/near-zero-variance, correlation filter, chi-square/ANOVA/mutual information, RFE, embedded (LASSO/RF/XGBoost importance), SHAP ranking, neurologist human-in-the-loop review (keep aura, previous drug failure), 4-layer selection framework, final feature set.'),
  spec(`${BASE}/pipeline-a/phase-10-machine-learning.md`, 'Pipeline A Phase 10 - Machine Learning (Epilepsy, EP001)', 'primary clinical', 'Baseline logistic regression, classical models (RF/SVM/XGBoost/LightGBM/CatBoost), hyperparameter optimization, subject-level cross-validation, model comparison table with AUC, calibration, threshold optimization, external validation (TUH/Siena), error/fairness analysis, ensemble, model selection matrix, save production model. XGBoost wins ~92%.'),
  spec(`${BASE}/pipeline-a/phase-11-explainable-ai.md`, 'Pipeline A Phase 11 - Explainable AI (Epilepsy, EP001)', 'primary clinical', 'Global feature importance, local SHAP for EP001 (base 40% + seizure burden + trigger + sleep = high risk), counterfactual, confidence, neurologist + technician explanations, three levels (global/local/clinical explainability), human validation & agreement.'),
  spec(`${BASE}/pipeline-a/phase-12-clinical-evidence-rag.md`, 'Pipeline A Phase 12 - Clinical Evidence RAG (Epilepsy, EP001)', 'primary clinical', 'Dedicated indexes (ILAE/AAN/NICE guidelines, EEG SOP, medication, hospital SOP, research), query router, hybrid retrieval (vector+keyword+metadata), reranking, evidence validation, merge AI+evidence, neurologist/technician/patient reports, hallucination control, evidence confidence 93-97%.'),
  spec(`${BASE}/pipeline-a/phase-13-clinical-decision-support.md`, 'Pipeline A Phase 13 - Clinical Decision Support (Epilepsy, EP001)', 'primary clinical', 'Role-based dashboards (neurologist, EEG technician, nurse, patient, caregiver, administrator), risk stratification (low/moderate/high/critical), recommendation engine (recommend not diagnose), onboarding support, remote monitoring, alert engine, human-in-the-loop approve/modify/reject, outcome tracking KPIs before/after, final CDSS report for EP001 (high risk).'),
  spec(`${BASE}/pipeline-a/phase-14-enterprise-deployment.md`, 'Pipeline A Phase 14 - Enterprise Deployment & AI Operations (Epilepsy, EP001)', 'primary clinical', 'Enterprise flow patient->CDSS, inference service, EMR/FHIR integration, workflow automation, real-time & model monitoring, data/model/clinical drift, security & RBAC, audit trail, disaster recovery, six operational domains, deployment KPI targets.'),
  spec(`${BASE}/pipeline-a/phase-15-monitoring-continuous-learning.md`, 'Pipeline A Phase 15 - Monitoring & Continuous Learning (Epilepsy, EP001)', 'primary clinical', 'Monitor clinical/AI/operations metrics, data drift (age, adherence), model drift (accuracy drop triggers retrain), clinical drift (new guidelines->update RAG), human feedback loop, retraining policy, continuous improvement cycle, dashboards.'),
  spec(`${BASE}/pipeline-a/phase-16-governance-compliance.md`, 'Pipeline A Phase 16 - AI Governance, Responsible AI & Compliance (Epilepsy, EP001)', 'primary clinical', 'Governance board, Responsible AI principles (fairness/transparency/accountability/reliability/privacy/safety - AI never diagnoses autonomously), clinical & data & model governance, bias & drift monitoring, explainability audit, retraining policy, security governance, regulatory framing (decision support not medical device), KPI dashboard, risk register, continuous improvement.'),
]

const PIPELINE_B = [
  ['phase-01-eeg-acquisition', 'EEG Acquisition & Data Collection', 'Device integration (Nihon Kohden/Natus), EDF/BDF/FIF import, 21 channels 512 Hz, metadata, EP001 recording.'],
  ['phase-02-eeg-validation', 'EEG Validation & Quality Assessment', 'Sampling rate, missing channels, impedance (3.1 kOhm), artifact score, recording quality grade.'],
  ['phase-03-eeg-cleaning', 'EEG Signal Cleaning & Artifact Removal', 'Bandpass 0.5-45 Hz, notch 50/60, re-reference, ICA, eye/muscle artifact removal.'],
  ['phase-04-eeg-standardization', 'EEG Standardization & Harmonization', 'Montage, resample, BIDS/FIF, channel naming 10-20.'],
  ['phase-05-eeg-exploratory', 'Exploratory EEG Signal Analysis', 'Topomaps, power spectra, band power, visual review.'],
  ['phase-06-eeg-statistical', 'EEG Statistical Analysis', 'Band power stats, connectivity, asymmetry, hemispheric comparison.'],
  ['phase-07-eeg-transformation', 'EEG Signal Transformation', 'FFT, wavelet, time-frequency, spectrogram features.'],
  ['phase-08-eeg-feature-engineering', 'EEG Feature Engineering', 'Spike count, theta power, coherence, entropy, frontal/temporal biomarkers.'],
  ['phase-09-eeg-feature-selection', 'EEG Feature Selection', 'Discriminative biomarkers, mutual information, embedded importance.'],
  ['phase-10-eeg-classical-ml', 'EEG Classical Machine Learning', 'SVM/RF/XGBoost on biomarkers, subject-level CV to avoid leakage.'],
  ['phase-11-eeg-deep-learning', 'EEG Deep Learning', 'EEGNet/CNN/LSTM/Transformer, 1024-D embedding, subject-level split.'],
  ['phase-12-eeg-explainable-ai', 'EEG Explainable AI & Brain Localization', 'Grad-CAM, saliency, attention, channel importance, frequency-band importance, brain-region localization (left temporal focus for EP001, channels T7/P7/F7).'],
  ['phase-13-eeg-clinical-rag', 'EEG Clinical Evidence RAG', 'ILAE/AAN EEG reporting guidelines, evidence-based EEG report, confidence.'],
  ['phase-14-eeg-cdss', 'EEG Clinical Decision Support', 'Neurologist/neurophysiologist/technician views, decision rules, EP001 left temporal epileptiform activity 98%.'],
  ['phase-15-eeg-deployment', 'EEG Enterprise Deployment & AI Operations', 'Inference service, EMR, monitoring, drift, security, disaster recovery.'],
  ['phase-16-eeg-governance', 'EEG AI Governance & Continuous Improvement', 'Model registry, bias/drift, explainability audit, retraining, compliance.'],
].map(([slug, title, points]) =>
  spec(`${BASE}/pipeline-b/${slug}.md`, `Pipeline B ${title} (Epilepsy, EP001)`, 'secondary EEG', points))

const STAKEHOLDERS = [
  ['eeg-technician', 'EEG Technician', 'Uses EP001 pre-EEG data. Questions the technician asks (consent, identity, sleep deprivation, medication, prep), assessment (impedance 3.1 kOhm, artifact low, readiness 98%), tasks with simulated status, pain points (high impedance, artifacts, movement), complete flow.'],
  ['nurse', 'Epilepsy Nurse', 'Simulated (dummy answers). Medication review, adherence counselling, safety (driving/falls), education, follow-up coordination; questions, tasks with status, pain points, flow.'],
  ['patient', 'Patient', 'Simulated. Patient-facing questions/app tasks: medication reminders, sleep, seizure diary, questionnaire, appointment; experience, pain points, flow. No diagnosis claims.'],
  ['caregiver', 'Caregiver', 'Simulated. Emergency seizure response, medication support, appointment tracking, daily monitoring; questions, tasks, pain, flow.'],
  ['administrator', 'Administrator', 'Simulated. Operational KPIs: onboarding time, waiting time, throughput, AI adoption, cost per patient; questions, tasks, pain, flow.'],
].map(([slug, role, points]) =>
  spec(`${BASE}/stakeholders/${slug}-simulation.md`, `Stakeholder Simulation - ${role} (Epilepsy, EP001)`, 'stakeholder', `Role questions in detail with answers (real for EEG technician from EP001, dummy/simulated for others), assessment, tasks with simulated status, pain points, complete flow. ${points}`))

const GAP = [
  ['brain-localization', 'Brain Localization for Epilepsy (Channel-to-Region, Focus, Confidence)', 'Map 10-20 channels to lobes (frontal/temporal/parietal/occipital/central), localize seizure focus, output focus + confidence + affected electrodes (EP001: left temporal, F7/T7/P7, 92%), Grad-CAM/SHAP explainability, clinical value for treatment planning.'],
  ['remote-monitoring', 'Remote Epilepsy Monitoring (Wearables, Alerts, Relapse Warning)', 'Wearable EEG/smartwatch/mobile, daily seizure diary, sleep, medication adherence, activity; alert thresholds (adherence<60%, sleep<4h, seizure cluster), relapse warning, escalation to neurologist, KPIs.'],
  ['literature-review', 'Literature Review - Epilepsy AI (Synthesis Matrix)', 'Progression Healthcare->Epilepsy->EEG->ML->DL->XAI->RAG->Multi-Agent->CDSS->Responsible AI->Enterprise; synthesis matrix table (source, method, finding, gap); gap analysis; 15+ APA7 references.'],
  ['dataset-dossier', 'Dataset Dossier for Epilepsy Research', 'Score TUH EEG Corpus, Siena Scalp EEG, EPILEPSIAE, Human Epilepsy Project, PhysioNet, UK Biobank on patient-assessment/EEG/MRI/medication/longitudinal/access; hybrid design (public for algorithm validation + hospital retrospective for workflow); ethics/consent.'],
].map(([slug, title, points]) =>
  spec(`${BASE}/${slug}.md`, title, 'gap doc', points))

function buildPrompt(s) {
  return `${PREAMBLE}

DOCUMENT TO WRITE
Title: ${s.title}
Absolute path (use Write tool exactly): ${s.path}
Category: ${s.kind}
Required content points to cover (expand into full sections with tables + diagrams):
${s.points}`
}

async function authorAll(list, phase) {
  return parallel(
    list.map((s) => () =>
      agent(buildPrompt(s), {
        label: s.path.split('/docs/')[1],
        phase,
        agentType: 'general-purpose',
      })
    )
  )
}

phase('Pipeline A')
log(`Authoring ${PIPELINE_A.length} Pipeline A phase docs...`)
const a = await authorAll(PIPELINE_A, 'Pipeline A')

phase('Pipeline B')
log(`Authoring ${PIPELINE_B.length} Pipeline B (EEG) phase docs...`)
const b = await authorAll(PIPELINE_B, 'Pipeline B')

phase('Stakeholders')
log(`Authoring ${STAKEHOLDERS.length} stakeholder simulation docs...`)
const s = await authorAll(STAKEHOLDERS, 'Stakeholders')

phase('Gap docs')
log(`Authoring ${GAP.length} top-1% gap docs...`)
const g = await authorAll(GAP, 'Gap docs')

const all = [...a, ...b, ...s, ...g]
const done = all.filter(Boolean).length
return { requested: all.length, written: done, results: all }
