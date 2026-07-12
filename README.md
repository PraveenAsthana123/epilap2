# Epilepsy Intelligence Platform — DBA Blueprint

An **Explainable AI–Driven Remote Epilepsy Care Platform** for faster patient onboarding,
continuous monitoring, brain-focus localization, and clinical decision support under human
oversight. This repository is the full DBA deliverable: a docs-first clinical blueprint, an
interactive viewer, a reproducible analytics stack, a Responsible-AI framework (design +
runnable), a database schema, and a REST API. All worked examples use patient **EP001**.

> Scope: **epilepsy only.** Data is **synthetic** but clinically plausible and internally consistent.

## What's inside

| Area | Path | Highlights |
|---|---|---|
| **Clinical assessment** | `docs/primary-assessment/` | **9 roles**, 71 sections, **782 enterprise questionnaire items** (ID · Question · Response Type · Validation · EP001 · AI Feature), each with a 4-level severity model |
| **Interactive viewer** | `viewer/` | React role-portal: per-role left menu, markdown + Mermaid, **Fill & Score** with section→role→patient severity |
| **Analytics (runnable)** | `analysis/` | Primary + secondary (EEG) + fusion pipelines; questionnaire validator; scenario DB; **Responsible-AI runtime** (SHAP/LIME/fairness/guardrails) |
| **Responsible AI** | `docs/responsible-ai/` | 16 pillars + `implementation/` (accountable-AI, fairness, SHAP/LIME, guardrails/red-team, governance) |
| **Scenario database** | `data/analysis/`, `docs/scenarios/` | 57 seizure/epilepsy scenarios + weighted scoring model |
| **Database** | `db/` | PostgreSQL schema + runnable SQLite build |
| **API** | `api/` | FastAPI: roles, scenarios, weighted scoring, patient composite |
| **Vision** | `docs/research-vision.md`, `docs/patient-onboarding.md` | 6-objective platform vision + AI onboarding |

## Quick start

### Viewer
```bash
cd viewer && npm install && npm run dev      # http://localhost:5173
```

### Analytics (reproduces every table/figure)
```bash
cd analysis && pip install -r requirements.txt
python run_all.py                            # cohort -> primary -> secondary -> fusion
python responsible_ai_runtime.py             # SHAP + LIME + fairness + guardrails
python build_questionnaires.py               # validate + consolidate all 9 role forms
python build_scenarios.py                    # scenario DB + scoring model
python -m pytest -q                          # 19 tests (positive + negative)
```

### Database + API
```bash
python db/build_sqlite.py                    # db/epilepsy.db (roles, 57 scenarios, EP001)
cd api && pip install -r requirements.txt && uvicorn main:app --reload   # /docs for Swagger
python -m pytest -q                          # 7 API tests
```

## Headline results (from the committed run)

| Result | Value |
|---|---|
| Primary drug-resistance AUC | 0.969 |
| EEG focus-lateralisation AUC | 0.93 |
| Fusion AUC | 0.976 |
| Fairness demographic-parity gap (before -> after mitigation) | 0.175 -> 0.087 |
| Questionnaire items validated | 782 across 71 sections (9 roles) |
| Scenario catalogue | 57 (28 seizure types, 10 syndromes, 15 clinical, 4 severity) |
| EP001 | Severe · fused risk 0.59 · focus **Left Temporal** (conf 0.98) |

## The 9 roles

Neurologist · EEG Technician · Nurse · Neuropsychologist · Pharmacist · Caregiver · Patient ·
Administrator · Occupational Therapist — each a self-contained questionnaire + severity model,
scorable in the viewer and via the API.

## Model lifecycle — 13 phases (phase gates: 100/100)

Each phase has a pipeline, monitoring signal, quality checks, a score, and a visualization.
Scored by `mlops/phase_gates.py` → `docs/phase-gates-scorecard.md` (renders in the viewer **Data** tab).

| # | Phase | Pipeline | Report |
|---|---|---|---|
| 1 | Problem definition | research-problems | [research-framework](docs/research-framework.md) |
| 2 | Data ingestion | make_cohort · **fetch_real_eeg** | [data-quality](docs/analysis/data-quality-report.md) |
| 3 | Data validation | data_contract · data_quality | [data-quality](docs/analysis/data-quality-report.md) |
| 4 | Data preparation | preprocessing · **train_pipeline (persisted)** | [preprocessing](docs/analysis/preprocessing-report.md) |
| 5 | Feature engineering / store | feature_store | [variable-dictionary](docs/analysis/variable-dictionary.md) |
| 6 | Model development | primary/secondary/fusion · **HPO** | [primary](docs/analysis/primary-analysis.md) |
| 7 | Training | run_all · experiment_tracker | [fusion](docs/analysis/fusion-analysis.md) |
| 8 | Evaluation | **evaluation (DCA/CI/DeLong/nested)** · **real-EEG external** | [evaluation-rigor](docs/analysis/evaluation-rigor.md) · [real-eeg](docs/analysis/real-eeg-analysis.md) |
| 9 | Explainability / fairness | responsible_ai_runtime | [rai-runtime](docs/analysis/responsible-ai-runtime.md) |
| 10 | Deployment / serving | api (**/predict**) · registry+rollback | [monitoring](docs/monitoring-observability.md) |
| 11 | Monitoring | observability · system_monitor · /metrics | [observability](docs/analysis/observability-report.md) |
| 12 | Governance | responsible-ai · **model card** · audit log | [responsible-ai](docs/responsible-ai/index.md) |
| 13 | Retraining | **retrain (champion-challenger)** | [phase-gates](docs/phase-gates-scorecard.md) |

**Real data:** `analysis/real_eeg_analysis.py` runs the pipeline end-to-end on **real EEG**
(EEG-Eye-State, 14,976×14) with **external validation AUC 0.979** — the rest of the analytics use a
synthetic cohort (methodology demonstration); epilepsy-labelled real corpora (Siena/TUH) plug in via
`fetch_siena.py`.

## How it all works

See **[docs/ARCHITECTURE-INTERNALS.md](docs/ARCHITECTURE-INTERNALS.md)** for each component's
internal functionality, working approach, and implementation approach, and
**[docs/GLOBAL-POLICY.md](docs/GLOBAL-POLICY.md)** for the documentation standards.

## Standards

- Docs-first; one file per unit of data; every doc carries tables, four Mermaid diagram types
  (+ C4 where architecture is discussed), Why/How justifications, Professor-readiness Q&A, and
  APA-7 references.
- All analytics deterministic (seed 42) and reproducible from a clean checkout.
- Responsible AI: fairness/bias audited **and** mitigated; explainability via SHAP + LIME;
  guardrails on inputs; human-in-the-loop before any recommendation.

## Prompt log

Every user request driving this build is recorded under `docs/prompt-log/` for reference and
defense validation.
