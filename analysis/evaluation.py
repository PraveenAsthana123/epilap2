"""
evaluation.py — Rigorous model evaluation (DCA · bootstrap CIs · DeLong · nested CV)
====================================================================================

Closes the evaluation-phase gaps a top-tier review demands:
  * Decision Curve Analysis (net clinical benefit vs treat-all / treat-none)
  * Bootstrap confidence intervals on ROC-AUC
  * DeLong test comparing two correlated ROC-AUCs (is model A really > B?)
  * Nested cross-validation (unbiased performance with inner hyperparameter search)

Output: docs/analysis/evaluation-rigor.md + figures.
Run: python analysis/evaluation.py
"""
from __future__ import annotations
import os, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
from sklearn.metrics import roc_auc_score

from common import DATA_DIR, df_to_md, save_fig, explain, caption, write_report, banner, SEED

STAGE = "evaluation"
TARGET = "drug_resistant"
FEATS = ["neuro_seizure_freq_pm", "npsy_gad7", "pt_qolie31", "pharm_adherence_pct", "npsy_moca",
         "care_zbi_burden", "neuro_trigger_burden"]


# ---- bootstrap CI on AUC --------------------------------------------------
def bootstrap_auc_ci(y, p, n=1000):
    rng = np.random.default_rng(SEED)
    aucs = []
    idx = np.arange(len(y))
    for _ in range(n):
        b = rng.choice(idx, len(idx), replace=True)
        if len(np.unique(y[b])) < 2:
            continue
        aucs.append(roc_auc_score(y[b], p[b]))
    lo, hi = np.percentile(aucs, [2.5, 97.5])
    return round(float(np.mean(aucs)), 3), round(float(lo), 3), round(float(hi), 3)


# ---- DeLong test (fast algorithm, Sun & Xu 2014) --------------------------
def _midrank(x):
    J = np.argsort(x); Z = x[J]; N = len(x); T = np.zeros(N)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5 * (i + j - 1) + 1
        i = j
    T2 = np.empty(N); T2[J] = T
    return T2


def delong_test(y, p1, p2):
    """Return the two-sided p-value for AUC(p1) == AUC(p2) on the same labels."""
    order = (-np.array([p1, p2])).argsort(axis=1)  # not used; keep structure explicit
    y = np.asarray(y)
    pos = y == 1
    m, n = int(pos.sum()), int((~pos).sum())
    preds = np.vstack([p1, p2])
    pos_p = preds[:, pos]; neg_p = preds[:, ~pos]
    k = 2
    tx = np.array([_midrank(pos_p[r]) for r in range(k)])
    ty = np.array([_midrank(neg_p[r]) for r in range(k)])
    tz = np.array([_midrank(np.concatenate([pos_p[r], neg_p[r]])) for r in range(k)])
    aucs = tz[:, :m].sum(axis=1) / m / n - (m + 1) / 2 / n
    v01 = (tz[:, :m] - tx) / n
    v10 = 1 - (tz[:, m:] - ty) / m
    s01 = np.cov(v01); s10 = np.cov(v10)
    S = s01 / m + s10 / n
    d = aucs[0] - aucs[1]
    var = S[0, 0] + S[1, 1] - 2 * S[0, 1]
    z = d / np.sqrt(var) if var > 0 else 0.0
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return round(float(aucs[0]), 3), round(float(aucs[1]), 3), round(float(p), 4)


# ---- decision curve analysis ---------------------------------------------
def decision_curve(y, p):
    ts = np.linspace(0.01, 0.6, 30)
    n = len(y)
    rows = []
    for pt in ts:
        pred = p >= pt
        tp = np.sum((pred == 1) & (y == 1)); fp = np.sum((pred == 1) & (y == 0))
        nb = tp / n - fp / n * (pt / (1 - pt))
        nb_all = y.mean() - (1 - y.mean()) * (pt / (1 - pt))
        rows.append({"pt": pt, "model": nb, "treat_all": nb_all, "treat_none": 0.0})
    d = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(d.pt, d.model, label="model", color="#4f46e5")
    ax.plot(d.pt, d.treat_all, label="treat all", color="#94a3b8", ls="--")
    ax.plot(d.pt, d.treat_none, label="treat none", color="#111827", ls=":")
    ax.set_xlabel("threshold probability"); ax.set_ylabel("net benefit")
    ax.set_ylim(-0.05, max(0.05, d.model.max() * 1.1)); ax.legend()
    ax.set_title("Decision Curve Analysis")
    return save_fig(fig, STAGE, "dca.png")


# ---- nested CV with inner HPO ---------------------------------------------
def nested_cv(X, y):
    grid = {"n_estimators": [200, 400], "max_depth": [None, 6]}
    inner = StratifiedKFold(3, shuffle=True, random_state=SEED)
    outer = StratifiedKFold(5, shuffle=True, random_state=SEED)
    clf = GridSearchCV(RandomForestClassifier(random_state=SEED), grid, cv=inner, scoring="roc_auc")
    scores = cross_val_score(clf, X, y, cv=outer, scoring="roc_auc")
    return round(float(scores.mean()), 3), round(float(scores.std()), 3)


def main():
    banner("evaluation — DCA, bootstrap CIs, DeLong, nested CV")
    df = pd.read_csv(os.path.join(DATA_DIR, "primary_clean_features.csv"))
    X = df[FEATS].fillna(df[FEATS].median()).values
    y = df[TARGET].values
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)

    lr = LogisticRegression(max_iter=1000, random_state=SEED).fit(Xtr, ytr)
    rf = RandomForestClassifier(n_estimators=300, random_state=SEED).fit(Xtr, ytr)
    p_lr = lr.predict_proba(Xte)[:, 1]
    p_rf = rf.predict_proba(Xte)[:, 1]

    ci_lr = bootstrap_auc_ci(yte, p_lr)
    ci_rf = bootstrap_auc_ci(yte, p_rf)
    a1, a2, p_delong = delong_test(yte, p_lr, p_rf)
    dca_png = decision_curve(yte, p_rf)
    nested_mean, nested_sd = nested_cv(X, y)

    ci_tab = pd.DataFrame([
        {"model": "LogReg", "auc": ci_lr[0], "ci95": f"[{ci_lr[1]}, {ci_lr[2]}]"},
        {"model": "RandomForest", "auc": ci_rf[0], "ci95": f"[{ci_rf[1]}, {ci_rf[2]}]"}])

    doc = f"""# Evaluation Rigor — DCA · Bootstrap CIs · DeLong · Nested CV

> **Why (this doc):** Point estimates are not enough for a defensible model; this adds clinical
> net-benefit, uncertainty on the metric, a formal model-comparison test, and unbiased nested
> performance. **How:** `analysis/evaluation.py`.

## ROC-AUC with bootstrap 95% CIs
{caption("AUC with 1000-sample bootstrap confidence intervals — the metric's uncertainty, not just a point.")}

{df_to_md(ci_tab)}

## Model comparison — DeLong test
AUC(LogReg) = {a1} vs AUC(RF) = {a2}; **DeLong p = {p_delong}**
({'no significant difference' if p_delong >= 0.05 else 'significant difference'} at α=0.05).

## Decision Curve Analysis (clinical net benefit)
![DCA]({dca_png})

The model curve above *treat-all* and *treat-none* across the plausible threshold range means it
adds net clinical benefit (fewer unnecessary actions than treating everyone).

## Nested cross-validation (unbiased, inner HPO)
Nested CV ROC-AUC = **{nested_mean} ± {nested_sd}** (5 outer × 3 inner folds; inner grid over
`n_estimators` × `max_depth`) — removes the optimistic bias of tuning and testing on the same folds.

{explain("Evaluate models the way a top journal / doctoral panel expects.",
         "CIs, formal comparison, net benefit, and nested CV are table-stakes for rigour.",
         "AUC uncertainty is quantified; models are compared formally; clinical utility is shown.",
         "Bootstrap CIs, DeLong test, DCA, and nested CV are computed from the data.",
         "DeLong et al. (1988); Vickers & Elkin (2006); Cawley & Talbot (2010).")}

## References

Cawley, G. C., & Talbot, N. L. C. (2010). On over-fitting in model selection and subsequent selection bias. *JMLR, 11*, 2079-2107.

DeLong, E. R., DeLong, D. M., & Clarke-Pearson, D. L. (1988). Comparing the areas under two or more correlated ROC curves. *Biometrics, 44*(3), 837-845.

Vickers, A. J., & Elkin, E. B. (2006). Decision curve analysis. *Medical Decision Making, 26*(6), 565-574.
"""
    path = write_report("evaluation-rigor.md", [doc])
    print(f"  AUC CIs: LR {ci_lr} RF {ci_rf}; DeLong p={p_delong}; nested CV {nested_mean}+/-{nested_sd}")
    print(f"  report -> {path}")


if __name__ == "__main__":
    main()
