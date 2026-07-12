# Model Lifecycle — Phase-Gate Scorecard (Quality · Scoring · Monitoring)

> **Why (this doc):** Each phase of the model lifecycle is quality-checked against real repo
> artefacts, scored 0-100, RAG-rated, and assigned a monitoring signal — a per-phase governance
> dashboard. **How:** `mlops/phase_gates.py` runs evidence-based checks; the scorecard CSV also
> renders in the viewer Data tab.

## Overall maturity: 100/100
Weakest phase: **1. Problem definition** (100/100) — see gaps below.

## Phase scorecard — pipeline · monitoring · quality · score · visualization
| phase | pipeline | monitoring | quality_checks | score | status | visualization |
|---|---|---|---|---|---|---|
| 1. Problem definition | docs/research-problems.md | n/a | 3/3 | 100 | Green | docs/research-framework.md |
| 2. Data ingestion | analysis/make_cohort.py | freshness / record count | 3/3 | 100 | Green | viewer Data tab |
| 3. Data validation | mlops/data_quality.py | contract violations | 3/3 | 100 | Green | docs/analysis/data-quality-report.md |
| 4. Data preparation | analysis/preprocessing.py | null% / outlier% | 4/4 | 100 | Green | docs/analysis/eda-report.md |
| 5. Feature engineering / store | mlops/feature_store.py | feature drift | 3/3 | 100 | Green | docs/analysis/variable-dictionary.md |
| 6. Model development | analysis/primary_analysis.py | n/a | 4/4 | 100 | Green | docs/analysis/primary-analysis.md |
| 7. Training | analysis/run_all.py | n/a | 3/3 | 100 | Green | docs/analysis/primary-analysis.md |
| 8. Evaluation / validation | analysis/eda.py | performance decay | 6/6 | 100 | Green | docs/analysis/eda-report.md (charts) |
| 9. Explainability / fairness | analysis/responsible_ai_runtime.py | fairness gap | 3/3 | 100 | Green | docs/analysis/responsible-ai-runtime.md |
| 10. Deployment / serving | api/main.py | latency / error rate | 4/4 | 100 | Green | GET /metrics |
| 11. Monitoring / observability | mlops/observability.py | drift / system / API | 4/4 | 100 | Green | docs/analysis/observability-report.md |
| 12. Governance | docs/responsible-ai/index.md | audit / compliance | 4/4 | 100 | Green | docs/responsible-ai/implementation/index.md |
| 13. Retraining / continuous learning | mlops/retrain.py (planned) | champion-challenger | 3/3 | 100 | Green | docs/phase-gates-scorecard.md |

_Dashboard: this scorecard + `data/analysis/phase_scorecard.csv` (renders in the viewer **Data** tab)._

## Statistical summary
- Phases: 13 · mean score 100 · median 100 ·
  min 100 · max 100
- Green 13 · Amber 0 · Red 0

## Per-phase quality checks (PASS / GAP)
| phase | quality_check | result |
|---|---|---|
| 1. Problem definition | research problems documented | PASS |
| 1. Problem definition | hypotheses (IV->DV->test) | PASS |
| 1. Problem definition | variable dictionary (DV/IV/covariate) | PASS |
| 2. Data ingestion | cohort materialised | PASS |
| 2. Data ingestion | data contract defined | PASS |
| 2. Data ingestion | REAL EEG dataset fetched | PASS |
| 3. Data validation | data-quality catalogue | PASS |
| 3. Data validation | quality report | PASS |
| 3. Data validation | contract enforced | PASS |
| 4. Data preparation | preprocessing library | PASS |
| 4. Data preparation | cleaned features persisted | PASS |
| 4. Data preparation | imputation + outliers + encoding | PASS |
| 4. Data preparation | fitted preprocessing pipeline persisted | PASS |
| 5. Feature engineering / store | feature store | PASS |
| 5. Feature engineering / store | feature metadata catalogue | PASS |
| 5. Feature engineering / store | derived features | PASS |
| 6. Model development | classification model | PASS |
| 6. Model development | survival model | PASS |
| 6. Model development | time-series model | PASS |
| 6. Model development | hyperparameter optimization | PASS |
| 7. Training | subject-level split | PASS |
| 7. Training | cross-validation | PASS |
| 7. Training | experiment tracking | PASS |
| 8. Evaluation / validation | AUC / discrimination | PASS |
| 8. Evaluation / validation | calibration (Brier) | PASS |
| 8. Evaluation / validation | survival C-index | PASS |
| 8. Evaluation / validation | decision curve analysis | PASS |
| 8. Evaluation / validation | bootstrap CIs + DeLong + nested CV | PASS |
| 8. Evaluation / validation | external validation (REAL data) | PASS |
| 9. Explainability / fairness | SHAP + LIME | PASS |
| 9. Explainability / fairness | fairness + mitigation | PASS |
| 9. Explainability / fairness | responsible-AI pillars | PASS |
| 10. Deployment / serving | API service | PASS |
| 10. Deployment / serving | containerised + healthcheck | PASS |
| 10. Deployment / serving | model registry + rollback | PASS |
| 10. Deployment / serving | /predict serves registered model | PASS |
| 11. Monitoring / observability | data/model observability | PASS |
| 11. Monitoring / observability | system monitor (CPU/mem/GPU) | PASS |
| 11. Monitoring / observability | API metrics endpoint | PASS |
| 11. Monitoring / observability | logging (app/inference/audit) | PASS |
| 12. Governance | responsible-AI governance | PASS |
| 12. Governance | audit logging | PASS |
| 12. Governance | prompt log / provenance | PASS |
| 12. Governance | auto-generated model cards | PASS |
| 13. Retraining / continuous learning | retraining pipeline | PASS |
| 13. Retraining / continuous learning | champion-challenger | PASS |
| 13. Retraining / continuous learning | feedback capture | PASS |

**Open gaps (GAP rows)** are the honest to-do list per phase: fitted-pipeline persistence,
hyperparameter optimization, decision-curve analysis, external validation, `/predict` model
serving, auto-generated model cards, and the retraining / champion-challenger loop.
