"""
eda.py — Exploratory Data Analysis of EACH dataset (+ class balance + accuracy matrix)
======================================================================================

For every generated dataset: shape, missingness, duplicates, descriptive statistics,
class balance, correlations, and distributions. For the labelled cohort it also fits a
baseline model and reports the ACCURACY MATRIX (confusion matrix + per-class
precision/recall/F1) and detailed per-feature statistics vs the target.

Outputs: docs/analysis/eda-report.md + figures under analysis/outputs/eda/.
Run: python analysis/eda.py
"""
from __future__ import annotations
import os, warnings, glob
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score

from common import DATA_DIR, df_to_md, save_fig, caption, explain, write_report, banner, SEED

STAGE = "eda"
TARGET = "drug_resistant"


def dataset_eda(name, df):
    """Per-dataset EDA block: shape, missing, dup, numeric summary, class balance."""
    num = df.select_dtypes(include=[np.number])
    desc = num.describe().T[["mean", "std", "min", "50%", "max"]].round(2).reset_index() \
        .rename(columns={"index": "feature", "50%": "median"}) if len(num.columns) else pd.DataFrame()
    # Class balance for low-cardinality columns.
    bal = []
    for c in df.columns:
        if df[c].nunique() <= 6:
            vc = df[c].value_counts(normalize=True).round(3)
            bal.append({"column": c, "distribution": ", ".join(f"{k}:{v}" for k, v in vc.items())})
    return {"shape": f"{df.shape[0]} x {df.shape[1]}",
            "missing_pct": round(100 * df.isna().mean().mean(), 2),
            "duplicates": int(df.duplicated().sum()),
            "desc": desc, "balance": pd.DataFrame(bal)}


def accuracy_matrix(df):
    """Confusion matrix + per-class metrics for the drug-resistance target."""
    feats = ["neuro_seizure_freq_pm", "npsy_gad7", "pt_qolie31", "pharm_adherence_pct", "npsy_moca"]
    X = df[feats].fillna(df[feats].median()).values
    y = df[TARGET].values
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)
    clf = LogisticRegression(max_iter=1000, random_state=SEED).fit(Xtr, ytr)
    p = clf.predict_proba(Xte)[:, 1]
    pred = (p >= 0.5).astype(int)
    cm = confusion_matrix(yte, pred)
    rep = classification_report(yte, pred, output_dict=True, zero_division=0)
    auc = roc_auc_score(yte, p)

    fig, ax = plt.subplots(figsize=(4, 3.4))
    im = ax.imshow(cm, cmap="Blues")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black", fontsize=13)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["pred 0", "pred 1"]); ax.set_yticklabels(["true 0", "true 1"])
    ax.set_title("Confusion matrix (drug-resistance)")
    png = save_fig(fig, STAGE, "confusion.png")

    metrics = pd.DataFrame([
        {"class": "Not-resistant (0)", "precision": round(rep["0"]["precision"], 3),
         "recall": round(rep["0"]["recall"], 3), "f1": round(rep["0"]["f1-score"], 3),
         "support": int(rep["0"]["support"])},
        {"class": "Drug-resistant (1)", "precision": round(rep["1"]["precision"], 3),
         "recall": round(rep["1"]["recall"], 3), "f1": round(rep["1"]["f1-score"], 3),
         "support": int(rep["1"]["support"])},
    ])
    return metrics, png, round(rep["accuracy"], 3), round(auc, 3), cm.tolist()


def detailed_stats(df):
    """Per-feature: mean by target group + Mann-Whitney p + effect size (rank-biserial)."""
    feats = ["neuro_seizure_freq_pm", "npsy_gad7", "pt_qolie31", "pharm_adherence_pct",
             "npsy_moca", "care_zbi_burden"]
    rows = []
    g0 = df[df[TARGET] == 0]; g1 = df[df[TARGET] == 1]
    for f in feats:
        a, b = g0[f].dropna(), g1[f].dropna()
        u, p = stats.mannwhitneyu(a, b)
        rbc = 1 - 2 * u / (len(a) * len(b))     # rank-biserial effect size
        rows.append({"feature": f, "mean_not_resistant": round(a.mean(), 2),
                     "mean_resistant": round(b.mean(), 2),
                     "mannwhitney_p": ("<0.001" if p < 1e-3 else round(p, 3)),
                     "effect_size_rbc": round(rbc, 3)})
    return pd.DataFrame(rows)


def main():
    banner("eda — exploratory data analysis of each dataset")
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))
    keep = ["cohort_primary", "cohort_eeg", "recurrence", "decisions", "epilepsy_scenarios"]
    blocks = []
    for p in files:
        name = os.path.basename(p).replace(".csv", "")
        if name not in keep:
            continue
        df = pd.read_csv(p)
        e = dataset_eda(name, df)
        block = f"### {name}\n\nshape {e['shape']} · missing {e['missing_pct']}% · duplicates {e['duplicates']}\n"
        if len(e["desc"]):
            block += "\n" + df_to_md(e["desc"].head(12)) + "\n"
        if len(e["balance"]):
            block += "\n**Class balance / low-cardinality columns:**\n\n" + df_to_md(e["balance"].head(10)) + "\n"
        blocks.append(block)

    prim = pd.read_csv(os.path.join(DATA_DIR, "cohort_primary.csv"))
    # Correlation heatmap.
    key = ["neuro_seizure_freq_pm", "npsy_moca", "npsy_gad7", "pt_qolie31",
           "pharm_adherence_pct", "care_zbi_burden", "severity_level"]
    corr = prim[key].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr))); ax.set_xticklabels(corr.columns, rotation=90, fontsize=7)
    ax.set_yticks(range(len(corr))); ax.set_yticklabels(corr.columns, fontsize=7)
    fig.colorbar(im, fraction=0.046); ax.set_title("Spearman correlation")
    corr_png = save_fig(fig, STAGE, "correlation.png")

    # Class-balance figure for the targets.
    fig, axes = plt.subplots(1, 2, figsize=(7, 3))
    prim["severity_level"].value_counts().sort_index().plot.bar(ax=axes[0], color="#4f46e5")
    axes[0].set_title("severity_level")
    prim[TARGET].value_counts().sort_index().plot.bar(ax=axes[1], color="#0ea5e9")
    axes[1].set_title("drug_resistant (imbalanced)")
    bal_png = save_fig(fig, STAGE, "class_balance.png")

    acc_tab, cm_png, acc, auc, cm = accuracy_matrix(prim)
    stats_tab = detailed_stats(prim)
    imbalance = prim[TARGET].value_counts(normalize=True).round(3).to_dict()

    doc = f"""# Exploratory Data Analysis (Each Dataset) + Class Balance + Accuracy Matrix

> **Why (this doc):** EDA of every generated dataset — shape, missingness, distributions, class
> balance, correlations — plus the accuracy matrix (confusion + per-class metrics) and detailed
> per-feature statistics vs the target. **How:** `analysis/eda.py`.

## Per-dataset EDA
{''.join(blocks)}

## Correlation (primary cohort)
![correlation]({corr_png})

## Class balance
![class balance]({bal_png})

Target imbalance (`drug_resistant`): {imbalance} — handled by SMOTE/ADASYN/class-weight in
`analysis/preprocessing.py` and the primary pipeline's balancing stage.

## Accuracy matrix (drug-resistance, holdout)
Accuracy **{acc}** · ROC-AUC **{auc}** · confusion matrix {cm}

![confusion]({cm_png})

{df_to_md(acc_tab)}

## Detailed statistics — features vs target
{caption("Group means by drug-resistance with Mann-Whitney U p-values and rank-biserial effect sizes.")}

{df_to_md(stats_tab)}

{explain("Characterise every dataset and quantify feature-target relationships.",
         "EDA + balance + accuracy-matrix + effect sizes are prerequisites to trustworthy modelling.",
         "Targets are imbalanced; key clinical features differ significantly by drug-resistance.",
         "Descriptives + Spearman + Mann-Whitney + confusion matrix computed from the data.",
         "Tukey (1977); Field (2018).")}

## References

Field, A. (2018). *Discovering statistics using IBM SPSS statistics* (5th ed.). Sage.

Tukey, J. W. (1977). *Exploratory data analysis*. Addison-Wesley.
"""
    path = write_report("eda-report.md", [doc])
    print(f"  datasets EDA'd: {len(blocks)}; accuracy={acc} auc={auc}; imbalance={imbalance}")
    print(f"  report -> {path}")


if __name__ == "__main__":
    main()
