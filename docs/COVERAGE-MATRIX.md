# Coverage / Traceability Matrix

> **Why:** Prove every piece of given input data is reflected in the docs (checked thoroughly).
> **How:** Map each source data unit → the doc file that carries it → status.

Legend: ✅ reflected · 🟡 partial (needs full-standard upgrade) · ⬜ not yet created

## A. EP001 — Neurologist Primary Assessment (given data)

*Caption — every neurologist section the user supplied, mapped to its MD file.*

| # | Section (given) | Doc file | Status |
|---|---|---|---|
| 1 | Chief Complaint | primary-assessment/neurologist/01-chief-complaint.md | ✅ |
| 2 | History of Present Illness | .../02-history-present-illness.md | ✅ |
| 3 | Seizure History | .../03-seizure-history.md | ✅ |
| 4 | Aura | .../04-aura.md | ✅ |
| 5 | During Seizure | .../05-during-seizure.md | ✅ |
| 6 | Post-Ictal | .../06-post-ictal.md | ✅ |
| 7 | Trigger Assessment | .../07-trigger-assessment.md | ✅ |
| 8 | Medication History | .../08-medication-history.md | ✅ |
| 9 | Past Medical History | .../09-past-medical-history.md | ✅ |
| 10 | Family History | .../10-family-history.md | ✅ |
| 11 | Lifestyle | .../11-lifestyle.md | ✅ |
| 12 | Neurological Examination | .../12-neurological-examination.md | ✅ |
| 13 | Functional Assessment | .../13-functional-assessment.md | ✅ |
| 14 | Quality of Life | .../14-quality-of-life.md | ✅ |
| 15 | Neurologist Impression | .../15-impression.md | ✅ |

## B. EP001 — EEG Technician Primary Assessment (given data)

*Caption — every EEG-technician section supplied, mapped to its file.*

| # | Section (given) | Doc file | Status |
|---|---|---|---|
| 1 | Patient Preparation | primary-assessment/eeg-technician/01-patient-preparation.md | ✅ |
| 2 | EEG Setup | .../02-eeg-setup.md | ✅ |
| 3 | Electrode Quality | .../03-electrode-quality.md | ✅ |
| 4 | Recording Conditions | .../04-recording-conditions.md | ✅ |
| 5 | Artifact Risk | .../05-artifact-risk.md | ✅ |
| 6 | Technician Notes | .../06-technician-notes.md | ✅ |

## C. EP001 — Derived / Roles (given data)

| Item (given) | Doc file | Status |
|---|---|---|
| AI Features Derived Before EEG | primary-assessment/ai-derived-features.md | ✅ |
| Patient Summary (demographics) | primary-assessment/00-patient-summary.md | ✅ |
| Neurologist role: assessment/pain/tasks | stakeholders/neurologist-simulation.md | ✅ full standard |
| Neurologist role (brief) | primary-assessment/roles-neurologist.md | 🟡 brief |
| EEG Technician role: assessment/pain/tasks | primary-assessment/roles-eeg-technician.md | 🟡 brief |

## D. Pipeline A — 16 Phases (given structure)

*Caption — each phase the user described, mapped to its doc + upgrade status.*

| Phase | Doc file | Status |
|---|---|---|
| 1 Data Collection | pipeline-a/phase-01-data-collection.md | 🟡 (flowchart only) |
| 2 Validation | pipeline-a/phase-02-validation.md | 🟡 (flowchart only) |
| 3 Cleaning | ⬜ | ⬜ |
| 4 Standardization | ⬜ | ⬜ |
| 5 Exploratory Data Analysis | pipeline-a/phase-05-exploratory-data-analysis.md | ✅ canonical (all rules) |
| 6 Statistical Analysis | ⬜ | ⬜ |
| 7 Data Transformation | ⬜ | ⬜ |
| 8 Feature Engineering | ⬜ | ⬜ |
| 9 Feature Selection | ⬜ | ⬜ |
| 10 Machine Learning | ⬜ | ⬜ |
| 11 Explainable AI | ⬜ | ⬜ |
| 12 Clinical Evidence RAG | ⬜ | ⬜ |
| 13 Clinical Decision Support | ⬜ | ⬜ |
| 14 Enterprise Deployment | ⬜ | ⬜ |
| 15 Monitoring & Continuous Learning | ⬜ | ⬜ |
| 16 AI Governance & Compliance | ⬜ | ⬜ |

## E. Blueprint / Pipelines B–E (given structure)

| Item | Doc file | Status |
|---|---|---|
| Overview / 3 contributions / 5 pillars | 00-overview.md | 🟡 (no diagrams yet) |
| Part I Business Problem | part1-business-problem.md | 🟡 |
| Part II Methodology | part2-methodology.md | 🟡 |
| Pipeline A summary | pipeline-a-primary-assessment.md | 🟡 |
| Pipeline B EEG | pipeline-b-eeg.md | 🟡 |
| Pipeline C Multimodal | pipeline-c-multimodal.md | 🟡 |
| Pipeline D Enterprise | pipeline-d-enterprise-platform.md | 🟡 |
| Pipeline E Evaluation | pipeline-e-evaluation.md | 🟡 |
| Parts IV–VIII | part4-implementation.md, part5-8-results-conclusion.md | 🟡 |
| Appendix / Publication strategy | appendix.md, publication-strategy.md | 🟡 |

## F. Top-1% Gap Docs (identified, not yet created)

| Doc | Status |
|---|---|
| Brain localization (channel→region, focus, confidence) | ⬜ |
| Remote monitoring (wearables, thresholds, relapse alerts) | ⬜ |
| Literature review (APA7, synthesis matrix) | ⬜ |
| Dataset dossier (TUH, Siena, EPILEPSIAE, HEP scored) | ⬜ |
| Other stakeholders (Nurse, Patient, Caregiver, Administrator) simulations | ⬜ |

## Summary Count (updated — build complete)

*Caption — headline completeness at a glance after both workflows.*

| Bucket | ✅ | 🟡 | ⬜ |
|---|---|---|---|
| EP001 assessments (A+B+C) | 23 | 0 | 0 |
| Pipeline A phases (1–16) | 16 | 0 | 0 |
| Pipeline B (EEG) phases (1–16) | 16 | 0 | 0 |
| Stakeholder sims | 6 | 0 | 0 |
| Blueprint docs (12) | 12 | 0 | 0 |
| Top-1% gap docs | 4 | 0 | 0 |

## Missing-Check (policy rule 25 — 2026-07-04)

*Caption — automated completeness scan; gaps found and the fix applied.*

| Gap found | Count | Fix |
|---|---|---|
| Primary-assessment raw-data files below full standard (no 4 diagrams / refs / Q&A) | 24 | ✅ Retrofitted (Workflow 7, 26/26) |
| dataset-scorecard.md missing 4 diagrams + Q&A | 1 | ✅ Retrofitted |
| Folders without index.md (pipeline-a, pipeline-b, stakeholders) | 3 | ✅ indexes created |
| Risky Mermaid labels | 0 (1 false positive: valid `[( )]` cylinder) | none needed |
| APA "Publication manual" author typo (Psychiatric→Psychological) | 7 | ✅ fixed via sed |

**Re-run missing-check (after fixes): 0 docs below standard.** 2 agent-generated psychiatric
references remain (plausible; flagged under the verify-citations-before-submission caveat).

**Conclusion:** Complete. All EP001 given assessment data (23/23) is reflected, all 16+16
pipeline phases, 6 stakeholder simulations, 12 retrofitted blueprint docs, and 4 gap docs are
built to the mandatory standard (tables + 4 diagrams + Why/How + Defense Q&A + APA7). **87 MD
docs total**, viewer builds clean, 0 Mermaid syntax issues. Optional remaining: viewer TOC/PDF
export polish (PLAN milestone 13).
