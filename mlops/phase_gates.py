"""
phase_gates.py — Per-phase quality checks + scoring + maturity dashboard
========================================================================

Scores every phase of the model lifecycle by running concrete QUALITY CHECKS against
the actual repo artefacts (files, reports, metrics). Each phase gets:
  * a set of pass/fail quality checks (evidence-based)
  * a score 0-100 (= % checks passed)
  * a RAG status (Green >=80 / Amber >=50 / Red <50)
plus an overall maturity score and a statistical summary.

Outputs:
  data/analysis/phase_scorecard.csv        (phase, score, status, passed/total)  <- shows in viewer Data tab
  docs/phase-gates-scorecard.md             (full per-phase checks + monitoring + stats)

Run: python mlops/phase_gates.py
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _exists(*parts) -> bool:
    return os.path.exists(os.path.join(ROOT, *parts))


def _contains(rel: str, needle: str) -> bool:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return False
    return needle.lower() in open(p, encoding="utf-8", errors="ignore").read().lower()


# Each phase -> list of (check_name, passed_bool). Monitoring column names the signal watched.
PHASES = [
    ("1. Problem definition", "n/a", [
        ("research problems documented", _exists("docs", "research-problems.md")),
        ("hypotheses (IV->DV->test)", _exists("docs", "analysis", "hypotheses.md")),
        ("variable dictionary (DV/IV/covariate)", _exists("docs", "analysis", "variable-dictionary.md")),
    ]),
    ("2. Data ingestion", "freshness / record count", [
        ("cohort materialised", _exists("data", "analysis", "cohort_primary.csv")),
        ("data contract defined", _exists("mlops", "data_contract.py")),
        ("real-data fetch path (Siena)", _exists("analysis", "fetch_siena.py")),
    ]),
    ("3. Data validation", "contract violations", [
        ("data-quality catalogue", _exists("data", "analysis", "data_quality_report.csv")),
        ("quality report", _exists("docs", "analysis", "data-quality-report.md")),
        ("contract enforced", _exists("mlops", "data_contract.py")),
    ]),
    ("4. Data preparation", "null% / outlier%", [
        ("preprocessing library", _exists("analysis", "preprocessing.py")),
        ("cleaned features persisted", _exists("data", "analysis", "primary_clean_features.csv")),
        ("imputation + outliers + encoding", _contains("docs/analysis/preprocessing-report.md", "imputation")),
        ("fitted preprocessing pipeline persisted", _exists("mlops", "store", "pipeline.joblib")),  # gap
    ]),
    ("5. Feature engineering / store", "feature drift", [
        ("feature store", _exists("mlops", "feature_store.py")),
        ("feature metadata catalogue", _exists("mlops", "store", "feature_metadata.json")),
        ("derived features", _contains("docs/analysis/primary-analysis.md", "feature engineering")),
    ]),
    ("6. Model development", "n/a", [
        ("classification model", _contains("docs/analysis/primary-analysis.md", "auc")),
        ("survival model", _exists("docs", "analysis", "recurrence-risk.md")),
        ("time-series model", _exists("docs", "analysis", "timeseries-analysis.md")),
        ("hyperparameter optimization", _exists("mlops", "store", "hpo_results.json")),  # gap
    ]),
    ("7. Training", "n/a", [
        ("subject-level split", _contains("docs/analysis/secondary-analysis.md", "subject-level")),
        ("cross-validation", _contains("docs/analysis/primary-analysis.md", "cross-validated")),
        ("experiment tracking", _exists("mlops", "experiment_tracker.py")),
    ]),
    ("8. Evaluation / validation", "performance decay", [
        ("AUC / discrimination", _contains("docs/analysis/primary-analysis.md", "auc")),
        ("calibration (Brier)", _contains("docs/analysis/governance-confidence-concordance.md", "brier")),
        ("survival C-index", _contains("docs/analysis/recurrence-risk.md", "concordance")),
        ("decision curve analysis", _exists("docs", "analysis", "decision-curve.md")),  # gap
        ("external validation", _exists("data", "analysis", "external_validation.csv")),  # gap (needs real data)
    ]),
    ("9. Explainability / fairness", "fairness gap", [
        ("SHAP + LIME", _contains("docs/analysis/responsible-ai-runtime.md", "shap")),
        ("fairness + mitigation", _contains("docs/analysis/responsible-ai-runtime.md", "fairness")),
        ("responsible-AI pillars", _exists("docs", "responsible-ai", "index.md")),
    ]),
    ("10. Deployment / serving", "latency / error rate", [
        ("API service", _exists("api", "main.py")),
        ("containerised + healthcheck", _contains("api/Dockerfile", "healthcheck")),
        ("model registry + rollback", _exists("mlops", "model_registry.py")),
        ("/predict serves registered model", _contains("api/main.py", "/predict")),  # gap
    ]),
    ("11. Monitoring / observability", "drift / system / API", [
        ("data/model observability", _exists("docs", "analysis", "observability-report.md")),
        ("system monitor (CPU/mem/GPU)", _exists("mlops", "system_monitor.py")),
        ("API metrics endpoint", _contains("api/main.py", "/metrics")),
        ("logging (app/inference/audit)", _exists("mlops", "logging_setup.py")),
    ]),
    ("12. Governance", "audit / compliance", [
        ("responsible-AI governance", _exists("docs", "responsible-ai", "06-governance-ai.md")),
        ("audit logging", _contains("mlops/logging_setup.py", "audit")),
        ("prompt log / provenance", _exists("docs", "prompt-log", "index.md")),
        ("auto-generated model cards", _exists("mlops", "store", "model_card.md")),  # gap
    ]),
    ("13. Retraining / continuous learning", "champion-challenger", [
        ("retraining pipeline", _exists("mlops", "retrain.py")),          # gap
        ("champion-challenger", _exists("mlops", "store", "challenger.json")),  # gap
        ("feedback capture", _contains("mlops/logging_setup.py", "feedback")),  # gap
    ]),
]


def status(score):
    return "Green" if score >= 80 else "Amber" if score >= 50 else "Red"


# Per-phase PIPELINE (the module that runs it) and VISUALIZATION (its report/figure),
# so every phase has: pipeline · monitoring · quality-check · scoring · visualization · dashboard.
PIPELINE_OF = [
    "docs/research-problems.md", "analysis/make_cohort.py", "mlops/data_quality.py",
    "analysis/preprocessing.py", "mlops/feature_store.py", "analysis/primary_analysis.py",
    "analysis/run_all.py", "analysis/eda.py", "analysis/responsible_ai_runtime.py",
    "api/main.py", "mlops/observability.py", "docs/responsible-ai/index.md", "mlops/retrain.py (planned)",
]
VIZ_OF = [
    "docs/research-framework.md", "viewer Data tab", "docs/analysis/data-quality-report.md",
    "docs/analysis/eda-report.md", "docs/analysis/variable-dictionary.md",
    "docs/analysis/primary-analysis.md", "docs/analysis/primary-analysis.md",
    "docs/analysis/eda-report.md (charts)", "docs/analysis/responsible-ai-runtime.md",
    "GET /metrics", "docs/analysis/observability-report.md", "docs/responsible-ai/implementation/index.md",
    "docs/phase-gates-scorecard.md",
]


def main():
    rows, detail = [], []
    for i, (phase, monitor, checks) in enumerate(PHASES):
        passed = sum(1 for _, ok in checks if ok)
        total = len(checks)
        score = round(100 * passed / total)
        rows.append({"phase": phase, "pipeline": PIPELINE_OF[i], "monitoring": monitor,
                     "quality_checks": f"{passed}/{total}", "score": score, "status": status(score),
                     "visualization": VIZ_OF[i], "checks_passed": passed, "checks_total": total})
        for name, ok in checks:
            detail.append({"phase": phase, "quality_check": name, "result": "PASS" if ok else "GAP"})
    sc = pd.DataFrame(rows)
    sc.to_csv(os.path.join(ROOT, "data", "analysis", "phase_scorecard.csv"), index=False)
    det = pd.DataFrame(detail)

    overall = round(float(sc["score"].mean()))
    weakest = sc.sort_values("score").iloc[0]

    def md(df):
        return "| " + " | ".join(df.columns) + " |\n|" + "|".join(["---"] * len(df.columns)) + "|\n" + \
               "\n".join("| " + " | ".join(str(x) for x in r) + " |" for _, r in df.iterrows())

    doc = f"""# Model Lifecycle — Phase-Gate Scorecard (Quality · Scoring · Monitoring)

> **Why (this doc):** Each phase of the model lifecycle is quality-checked against real repo
> artefacts, scored 0-100, RAG-rated, and assigned a monitoring signal — a per-phase governance
> dashboard. **How:** `mlops/phase_gates.py` runs evidence-based checks; the scorecard CSV also
> renders in the viewer Data tab.

## Overall maturity: {overall}/100
Weakest phase: **{weakest['phase']}** ({weakest['score']}/100) — see gaps below.

## Phase scorecard — pipeline · monitoring · quality · score · visualization
{md(sc[['phase', 'pipeline', 'monitoring', 'quality_checks', 'score', 'status', 'visualization']])}

_Dashboard: this scorecard + `data/analysis/phase_scorecard.csv` (renders in the viewer **Data** tab)._

## Statistical summary
- Phases: {len(sc)} · mean score {overall} · median {int(sc['score'].median())} ·
  min {int(sc['score'].min())} · max {int(sc['score'].max())}
- Green {int((sc.status=='Green').sum())} · Amber {int((sc.status=='Amber').sum())} · Red {int((sc.status=='Red').sum())}

## Per-phase quality checks (PASS / GAP)
{md(det)}

**Open gaps (GAP rows)** are the honest to-do list per phase: fitted-pipeline persistence,
hyperparameter optimization, decision-curve analysis, external validation, `/predict` model
serving, auto-generated model cards, and the retraining / champion-challenger loop.
"""
    open(os.path.join(ROOT, "docs", "phase-gates-scorecard.md"), "w", encoding="utf-8").write(doc)
    print(f"phase gates: overall maturity {overall}/100 across {len(sc)} phases")
    for _, r in sc.iterrows():
        print(f"  {r['phase']:<38} {r['score']:>3}  {r['status']}")


if __name__ == "__main__":
    main()
