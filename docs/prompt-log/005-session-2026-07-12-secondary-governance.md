# Prompt Log 005 — Session 2026‑07‑11/12: Secondary EEG pipeline + Governance + UI

Per [GLOBAL‑POLICY.md](../GLOBAL-POLICY.md) rules 9 & 24 — verbatim (lightly de‑duplicated) record of
user inputs and the response actions taken.

## Inputs (user prompts, chronological)
1. 23‑step "Schizophrenia EEG → AI → RAG" complete flow — *"for secondary data set … have you implemented these in detail for each phase, category, add all missing point … with monitoring, pipeline, dashboard, report."* (translated to epilepsy per policy)
2. "create data section where each data … must get visualized before process and after process; for synthetic data … also create UI/tab to see the data visualization"
3. "survey section … where from patient to capture all his pain or question for neurologist and EEG technician"
4. "dashboard section … list of all the dashboard, report for each role"
5. "report section: list of summary report for each type of epilepsy, seizure"
6. "simulation section UI: each analysis by each role"
7. "AI form section UI: all form must be created for each role, question"
8. "continuous monitoring section … update, notification, alert, tracking, report, monitoring, update by each role"
9. "these must be top 1%"; "secondary data analysis"; "all the UI for each scenario"
10. "check the brutal feedback in anything missing"; "add them for each phase"
11. "statistical analysis, machine learning analysis, subjective analysis, list of analysis"
12. "sensitivity analysis"; "list of filter, transformation, Fourier, 1d to 2d conversion, computer vision approach, ml approach, statistical model approach"; "each pipeline must explain in detail"
13. "for secondary model … each accuracy, hypothesis"; "loss function"
14. "precision recall, data balance, unbalance, EDA, SMOTE, feature engineering, feature selection, visualization, hyperparameter tuning, present on UI"
15. "list of all the accuracy matrix must present"
16. "model drift, concept drift, model training, continuous monitoring, scoring, tracking, logging"
17. "make all these part of global policy"; "all the data must be present top 1%, production grade"; "security grade"; "encryption, HIPAA grade"; "NIST grade"; "OWASP grade"
18. "take patient consent … EULA grade"; "for taking their data for analysis"; "IRB board related document prepare"
19. "save all the input in md file"
20. "LIMS, SHAP … must be implemented in each section"

## Response actions taken
| Input | Action | Artefact |
|---|---|---|
| 1, 6, 9–16 | Built full 23‑phase secondary EEG pipeline on **real CHB‑MIT** | `analysis/secondary_eeg_full.py`; `docs/analysis/secondary-eeg-full.md` |
| 11–15 | Statistical (Mann‑Whitney), sensitivity (ablation + threshold sweep), subjective, EDA + class balance, SMOTE, GridSearchCV HPO, full accuracy matrix (AUC/AP/log‑loss), loss curve, methods catalog | same pipeline + exported `data/analysis/eeg_*.csv` |
| 2 | Before/after preprocessing export | `data/analysis/eeg_before_after.csv` |
| 17 | Security/compliance governance | `docs/governance/00-security-compliance.md` (HIPAA/NIST/OWASP/encryption) |
| 18 | IRB + patient consent (EULA) | `docs/governance/01-irb-submission.md`, `02-patient-consent-eula.md` |
| 17 | Global policy update | `docs/GLOBAL-POLICY.md` (new rules 26–31) + memory |
| 19 | This prompt log | `docs/prompt-log/005-...md` |
| 2–8 | UI sections (Data Viz, Survey, Dashboards, Reports, Simulation, AI Forms, Continuous Monitoring) | `viewer/src/*.jsx` (in progress) |
| 20 | SHAP present in Responsible‑AI (`docs/responsible-ai/05-explainable-ai.md`) + permutation importance in secondary pipeline; LIMS documented in data‑engineering governance | cross‑referenced |

## Notes / honest scope
- Deep models (EEGNet/CNN/ViT) remain an **MLP stand‑in** (no GPU/torch); RAG is a keyword stand‑in — interfaces are in place.
- All statistics/figures are **real computed numbers** on the real EEG (best AUC ≈ 0.92, log‑loss ≈ 0.08).
- Governance docs are dissertation‑grade artefacts; they describe controls, not a certified production deployment.
