"""
governance.py — EXECUTABLE governance capabilities C5 + C6
=========================================================

The two governance-core problems that define the DBA contribution, as real code:

  C5  Confidence & Uncertainty Estimation
        * calibrated probabilities (isotonic) + Brier score before/after
        * uncertainty = probability margin + entropy + RF ensemble variance
        * ABSTENTION: defer low-confidence cases to the clinician, and show that
          accuracy on the confident subset > overall (the human-oversight value)

  C6  Clinical Evidence Concordance Engine
        * derives three INDEPENDENT high-severity signals per patient
          (clinical rule · EEG rule · model prediction)
        * scores agreement -> Concordant / Partial / Discordant
        * flags discordant patients for mandatory human review (governance)

Writes: docs/analysis/governance-confidence-concordance.md (+ figures).
Run: python analysis/governance.py   (needs make_cohort.py + primary_analysis.py first)
"""
from __future__ import annotations
import os, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.model_selection import train_test_split
from sklearn.metrics import brier_score_loss, accuracy_score

from common import DATA_DIR, df_to_md, save_fig, explain, caption, write_report, banner, SEED

STAGE = "governance"
TARGET = "drug_resistant"


def load():
    df = pd.read_csv(os.path.join(DATA_DIR, "primary_clean_features.csv"))
    feats = pd.read_csv(os.path.join(DATA_DIR, "primary_selected_features.csv")).iloc[:, 0].tolist()
    eeg = pd.read_csv(os.path.join(DATA_DIR, "cohort_eeg.csv"))
    df = df.merge(eeg, on="patient_id", how="left", suffixes=("", "_eeg"))
    feats = [f for f in feats if f in df.columns]
    return df, feats


# ---------------------------------------------------------------------------
# C5 — Confidence / uncertainty / abstention
# ---------------------------------------------------------------------------
def confidence(df, feats):
    X, y = df[feats].values, df[TARGET].values
    Xtr, Xte, ytr, yte, itr, ite = train_test_split(
        X, y, np.arange(len(y)), test_size=0.3, random_state=SEED, stratify=y)

    base = LogisticRegression(max_iter=1000, random_state=SEED).fit(Xtr, ytr)
    p_raw = base.predict_proba(Xte)[:, 1]
    brier_raw = brier_score_loss(yte, p_raw)

    # Calibrate probabilities (isotonic) on a held-out split.
    cal = CalibratedClassifierCV(LogisticRegression(max_iter=1000, random_state=SEED),
                                 method="isotonic", cv=3).fit(Xtr, ytr)
    p_cal = cal.predict_proba(Xte)[:, 1]
    brier_cal = brier_score_loss(yte, p_cal)

    # Uncertainty signals.
    margin = np.abs(p_cal - 0.5)                          # higher = more confident
    eps = 1e-9
    entropy = -(p_cal * np.log(p_cal + eps) + (1 - p_cal) * np.log(1 - p_cal + eps))
    rf = RandomForestClassifier(n_estimators=300, random_state=SEED).fit(Xtr, ytr)
    tree_p = np.stack([t.predict_proba(Xte)[:, 1] for t in rf.estimators_])
    ens_var = tree_p.var(0)                               # epistemic-ish variance

    # Abstention: defer the least-confident cases (bottom 20% by margin).
    thresh = np.quantile(margin, 0.20)
    confident = margin >= thresh
    pred = (p_cal >= 0.5).astype(int)
    acc_all = accuracy_score(yte, pred)
    acc_conf = accuracy_score(yte[confident], pred[confident])
    acc_defer = accuracy_score(yte[~confident], pred[~confident]) if (~confident).any() else float("nan")
    abstain_rate = float((~confident).mean())

    # Reliability curve.
    frac_pos, mean_pred = calibration_curve(yte, p_cal, n_bins=8, strategy="quantile")
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot([0, 1], [0, 1], "k--", lw=0.8, label="perfect")
    ax.plot(mean_pred, frac_pos, "o-", color="#4f46e5", label="calibrated")
    ax.set_xlabel("predicted probability"); ax.set_ylabel("observed frequency")
    ax.set_title("Reliability curve (calibrated)"); ax.legend()
    png = save_fig(fig, STAGE, "reliability.png")

    # EP001 confidence.
    ep = df.index[df["patient_id"] == "EP001"][0]
    ep_p = float(cal.predict_proba(df.loc[[ep], feats].values)[0, 1])
    ep_margin = abs(ep_p - 0.5)

    tab = pd.DataFrame({
        "metric": ["Brier (raw)", "Brier (calibrated)", "Accuracy (all)",
                   "Accuracy (confident 80%)", "Accuracy (deferred 20%)", "Abstention rate",
                   "Mean entropy", "Mean ensemble variance"],
        "value": [round(brier_raw, 4), round(brier_cal, 4), round(acc_all, 3),
                  round(acc_conf, 3), round(acc_defer, 3), round(abstain_rate, 3),
                  round(float(entropy.mean()), 3), round(float(ens_var.mean()), 4)],
    })
    return tab, png, {"ep_p": round(ep_p, 3), "ep_margin": round(ep_margin, 3),
                      "acc_all": round(acc_all, 3), "acc_conf": round(acc_conf, 3)}


# ---------------------------------------------------------------------------
# C6 — Concordance engine
# ---------------------------------------------------------------------------
def _rule_clinical(df):
    """Independent clinical high-severity signal (not the target)."""
    return ((df["neuro_seizure_freq_pm"] >= 4).astype(int)
            + (df["pt_qolie31"] <= 60).astype(int)
            + (df["npsy_gad7"] >= 8).astype(int)) >= 2


def _rule_eeg(df):
    """Independent EEG high-severity signal."""
    return ((df["eeg_spike_rate_pm"] >= 3).astype(int)
            + (df["eeg_temporal_asym"].abs() >= 0.10).astype(int)
            + (df["eeg_focal_slowing"] == 1).astype(int)) >= 2


def concordance(df, feats):
    clin = _rule_clinical(df).astype(int).values
    eeg = _rule_eeg(df).astype(int).values
    model = LogisticRegression(max_iter=1000, random_state=SEED) \
        .fit(df[feats].values, df[TARGET].values).predict(df[feats].values)
    agree = clin + eeg + model  # 0..3 sources indicating high severity
    label = np.where(np.isin(agree, [0, 3]), "Concordant",
                     np.where(agree == 2, "Partial", "Discordant"))
    # Concordant = all-3 agree (0 or 3); Partial = 2/3; Discordant = 1/3 (a lone dissenter).
    df2 = pd.DataFrame({"patient_id": df["patient_id"], "clinical_high": clin,
                        "eeg_high": eeg, "model_high": model, "sources_agree": agree,
                        "concordance": label})
    summary = df2["concordance"].value_counts().rename_axis("concordance").reset_index(name="patients")
    discordant = df2[df2["concordance"] == "Discordant"]
    ep = df2[df2["patient_id"] == "EP001"].iloc[0]
    return df2, summary, len(discordant), ep


def build_report(v):
    S = [f"""# Governance Runtime — Confidence/Uncertainty (C5) & Concordance (C6)

> **Why (this doc):** The two governance-core capabilities that define the DBA contribution,
> executed as real code on the epilepsy drug-resistance model. C5 tells the platform **when to
> defer to the clinician**; C6 tells it **when the evidence sources disagree** (mandatory human
> review). **How:** every number/figure is computed by `analysis/governance.py`.

## C5 — Confidence & Uncertainty Estimation (with abstention)

{caption("Calibration, uncertainty, and the abstention value proposition — accuracy is higher on the confident subset.")}

{df_to_md(v['conf_tab'])}

![Reliability]({v['conf_png']})

**Human-oversight value:** deferring the least-confident 20% of cases raises accuracy from
**{v['conf_meta']['acc_all']}** (all) to **{v['conf_meta']['acc_conf']}** (confident subset) —
the deferred cases go to the clinician. EP001 predicted p = {v['conf_meta']['ep_p']}
(margin {v['conf_meta']['ep_margin']}).

{explain("Estimate confidence and abstain when uncertain.",
         "Safe clinical AI must know when NOT to answer and defer to a human.",
         "Calibrated probabilities + margin/entropy/ensemble-variance gate an abstention rule.",
         "The confident subset is more accurate; uncertain cases route to the neurologist.",
         "Guo et al. (2017); Kompa, Snoek & Beam (2021).")}

## C6 — Clinical Evidence Concordance Engine

{caption("Per-patient agreement across three INDEPENDENT high-severity signals (clinical rule, EEG rule, model).")}

{df_to_md(v['conc_summary'])}

**Discordant patients flagged for mandatory human review:** {v['n_discordant']}.
**EP001:** clinical_high={v['ep']['clinical_high']}, eeg_high={v['ep']['eeg_high']},
model_high={v['ep']['model_high']} → **{v['ep']['concordance']}**.

{explain("Detect agreement/conflict across evidence sources.",
         "Trust requires knowing when EEG, clinical, and model evidence disagree.",
         "Three independent signals are compared; discordant cases are escalated.",
         "Agreement of 3/3 = concordant, 2/3 = partial, lone dissenter = discordant -> human review.",
         "Rosenow & Luders (2001).")}

## Role in the framework (sequence)

```mermaid
sequenceDiagram
    participant F as Fusion model
    participant C5 as Confidence engine
    participant C6 as Concordance engine
    participant N as Neurologist
    F->>C5: prediction + probability
    C5->>C6: confident? (else defer)
    C6->>N: concordant -> recommend; discordant/uncertain -> mandatory review
    N-->>F: decision + feedback
```

{explain("Show how C5 + C6 gate the recommendation.",
         "Governance means the AI recommends only when confident AND concordant.",
         "Low confidence or discordant evidence routes to the clinician.",
         "Two gates sit between the model and any recommendation.",
         "NIST (2023).")}

## Professor Readiness (Defense Q&A)

**Q1: Why abstain instead of always predicting?** Because deferring uncertain cases to the
clinician raises reliability where it matters and is the operational meaning of "human oversight."

**Q2: Are the concordance signals independent of the target?** Yes — the clinical and EEG rules
are derived from raw features, not the label, so agreement is informative rather than circular.

**Q3: What happens to discordant patients?** They are flagged for mandatory human review — the
platform does not issue an autonomous recommendation when evidence conflicts.

## References

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *ICML*.

Kompa, B., Snoek, J., & Beam, A. L. (2021). Second opinion needed: communicating uncertainty in medical ML. *npj Digital Medicine, 4*(4).

NIST. (2023). *AI Risk Management Framework (AI RMF 1.0)*.

Rosenow, F., & Luders, H. (2001). Presurgical evaluation of epilepsy. *Brain, 124*(9), 1683-1700.
"""]
    return write_report("governance-confidence-concordance.md", S)


def main():
    banner("governance — C5 confidence/uncertainty + C6 concordance")
    df, feats = load()
    conf_tab, conf_png, conf_meta = confidence(df, feats)
    conc_df, conc_summary, n_disc, ep = concordance(df, feats)
    conc_df.to_csv(os.path.join(DATA_DIR, "concordance.csv"), index=False)
    path = build_report(dict(conf_tab=conf_tab, conf_png=conf_png, conf_meta=conf_meta,
                             conc_summary=conc_summary, n_discordant=n_disc, ep=ep))
    print(f"  C5 accuracy all->confident: {conf_meta['acc_all']} -> {conf_meta['acc_conf']} "
          f"(abstain 20%); EP001 p={conf_meta['ep_p']}")
    print(f"  C6 concordance: {dict(zip(conc_summary['concordance'], conc_summary['patients']))}; "
          f"discordant={n_disc}; EP001={ep['concordance']}")
    print(f"  report -> {path}")
    return conf_meta, ep


if __name__ == "__main__":
    main()
