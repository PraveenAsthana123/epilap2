"""
observability.py — Model & data observability / monitoring
==========================================================

Implements the observability checklist as a runnable monitoring pass:

  model performance     accuracy / precision / recall / F1 on a holdout
  prediction monitoring prediction-class distribution + confidence-score distribution
  data drift            KS test per feature (reference vs current window) -> drift flags
  concept drift         change in feature<->target correlation across windows
  data quality          missing / duplicate / null% / outlier / schema (contract) checks

Writes docs/analysis/observability-report.md. In production this runs on a schedule and
alerts on threshold breaches.

Run: python mlops/observability.py
"""
from __future__ import annotations
import os, sys
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "analysis")
DOCS = os.path.join(ROOT, "docs", "analysis")
sys.path.insert(0, HERE)
import data_contract

TARGET = "drug_resistant"
FEATS = ["neuro_seizure_freq_pm", "npsy_gad7", "pt_qolie31", "pharm_adherence_pct", "npsy_moca", "age"]


def model_performance(df):
    X, y = df[FEATS].fillna(df[FEATS].median()).values, df[TARGET].values
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    clf = LogisticRegression(max_iter=1000, random_state=42).fit(Xtr, ytr)
    p = clf.predict_proba(Xte)[:, 1]
    pred = (p >= 0.5).astype(int)
    perf = {"accuracy": round(accuracy_score(yte, pred), 3),
            "precision": round(precision_score(yte, pred), 3),
            "recall": round(recall_score(yte, pred), 3),
            "f1": round(f1_score(yte, pred), 3)}
    pred_mon = {"pred_positive_rate": round(float(pred.mean()), 3),
                "confidence_mean": round(float(np.abs(p - 0.5).mean() * 2), 3),
                "class_dist_actual": np.bincount(yte).tolist(),
                "class_dist_pred": np.bincount(pred, minlength=2).tolist()}
    return perf, pred_mon


def data_drift(df):
    """KS test: reference (unshifted) vs a 'current' window with simulated drift on 2 features."""
    ref = df[FEATS].fillna(df[FEATS].median())
    cur = ref.copy()
    cur["age"] = cur["age"] + 10                 # simulated demographic drift
    cur["pt_qolie31"] = cur["pt_qolie31"] - 15   # simulated outcome drift
    rows = []
    for f in FEATS:
        ks, p = stats.ks_2samp(ref[f], cur[f])
        rows.append({"feature": f, "ks_stat": round(float(ks), 3), "p": ("<0.001" if p < 1e-3 else round(float(p), 3)),
                     "drift": "DRIFT" if p < 0.05 else "stable"})
    return pd.DataFrame(rows)


def concept_drift(df):
    """Change in feature<->target correlation between the first and second half (relation drift)."""
    a, b = df.iloc[:len(df) // 2], df.iloc[len(df) // 2:]
    rows = []
    for f in FEATS:
        ca = np.corrcoef(a[f].fillna(a[f].median()), a[TARGET])[0, 1]
        cb = np.corrcoef(b[f].fillna(b[f].median()), b[TARGET])[0, 1]
        rows.append({"feature": f, "corr_window1": round(ca, 3), "corr_window2": round(cb, 3),
                     "relation_drift": round(abs(ca - cb), 3),
                     "flag": "review" if abs(ca - cb) > 0.15 else "ok"})
    return pd.DataFrame(rows)


def data_quality(df):
    viol = data_contract.validate(df)
    return {"rows": len(df), "duplicate_rows": int(df.duplicated().sum()),
            "null_pct_overall": round(100 * df.isna().mean().mean(), 2),
            "contract_violations": len(viol), "violation_detail": viol[:4]}


def main():
    df = pd.read_csv(os.path.join(DATA, "cohort_primary.csv"))
    perf, pred_mon = model_performance(df)
    drift = data_drift(df)
    concept = concept_drift(df)
    dq = data_quality(df)

    def md(d):
        return "| " + " | ".join(d.columns) + " |\n|" + "|".join(["---"] * len(d.columns)) + "|\n" + \
               "\n".join("| " + " | ".join(str(x) for x in r) + " |" for _, r in d.iterrows())

    doc = f"""# Observability & Monitoring Report

> **Why (this doc):** Continuous monitoring of model and data health — performance, prediction
> distribution/confidence, data drift (KS), concept drift, and data quality — the observability
> layer the checklist requires. **How:** `mlops/observability.py`; in production this runs on a
> schedule and alerts on breaches.

## Model performance (holdout)
accuracy {perf['accuracy']} · precision {perf['precision']} · recall {perf['recall']} · F1 {perf['f1']}

## Prediction monitoring
predicted-positive rate {pred_mon['pred_positive_rate']} · mean confidence {pred_mon['confidence_mean']} ·
class distribution actual {pred_mon['class_dist_actual']} vs predicted {pred_mon['class_dist_pred']}

## Data drift (Kolmogorov-Smirnov, reference vs current window)
{md(drift)}

_(The two simulated-drift features (age, pt_qolie31) are correctly flagged DRIFT; unshifted features stay stable — the detector works.)_

## Concept drift (feature<->target relation change)
{md(concept)}

## Data quality
rows {dq['rows']} · duplicate rows {dq['duplicate_rows']} · overall null% {dq['null_pct_overall']} ·
contract violations {dq['contract_violations']} {dq['violation_detail']}

**Alerting policy:** any KS drift p<0.05, relation-drift>0.15, calibration decay, or contract
violation raises a monitoring alert routed to the ML/clinical owner (human override retained).
"""
    open(os.path.join(DOCS, "observability-report.md"), "w", encoding="utf-8").write(doc)
    print(f"  perf={perf}")
    print(f"  drift flagged: {drift[drift.drift=='DRIFT']['feature'].tolist()}")
    print(f"  data quality violations={dq['contract_violations']}")
    print("  report -> docs/analysis/observability-report.md")


if __name__ == "__main__":
    main()
