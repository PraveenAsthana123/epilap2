"""
decision_support.py — Integrated Multimodal Clinical Decision Support (flagship #6)
===================================================================================

The capstone that UNIFIES every flagship + governance module into one governed
decision per patient (the "shared multimodal engine"):

    inputs  -> severity/type (primary) · drug-resistance risk (fusion)
               · recurrence risk band (survival) · EEG focus (DSP)
    gates   -> C5 confidence (defer if uncertain) · C6 concordance (defer if conflict)
    output  -> a governed recommendation OR "mandatory clinician review"

It reads the artefacts produced by the other pipelines (recurrence.csv, concordance.csv,
cohort_*.csv) and emits an EP001 decision card + a cohort auto-vs-defer summary.

Run: python analysis/decision_support.py
  (first run: make_cohort, primary_analysis, governance, recurrence)
"""
from __future__ import annotations
import os, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV

from common import DATA_DIR, df_to_md, explain, caption, write_report, banner, SEED

TARGET = "drug_resistant"
CONF_MARGIN = 0.15  # |p-0.5| below this -> low confidence -> defer


def load():
    prim = pd.read_csv(os.path.join(DATA_DIR, "primary_clean_features.csv"))
    feats = pd.read_csv(os.path.join(DATA_DIR, "primary_selected_features.csv")).iloc[:, 0].tolist()
    feats = [f for f in feats if f in prim.columns]
    eeg = pd.read_csv(os.path.join(DATA_DIR, "cohort_eeg.csv"))[["patient_id", "focus_side", "eeg_focus_channel"]]
    rec = pd.read_csv(os.path.join(DATA_DIR, "recurrence.csv"))[["patient_id", "risk_band"]]
    conc = pd.read_csv(os.path.join(DATA_DIR, "concordance.csv"))[["patient_id", "concordance"]]
    df = prim.merge(eeg, on="patient_id").merge(rec, on="patient_id").merge(conc, on="patient_id")
    return df, feats


def assemble(df, feats):
    """Compute the per-patient integrated decision with confidence + concordance gates."""
    X, y = df[feats].values, df[TARGET].values
    cal = CalibratedClassifierCV(LogisticRegression(max_iter=1000, random_state=SEED),
                                 method="isotonic", cv=3).fit(X, y)
    p = cal.predict_proba(X)[:, 1]
    margin = np.abs(p - 0.5)
    confident = margin >= CONF_MARGIN
    concordant = df["concordance"].values == "Concordant"

    rows = []
    for i, r in df.reset_index(drop=True).iterrows():
        gated = bool(confident[i] and concordant[i])
        if not gated:
            rec = "MANDATORY CLINICIAN REVIEW (low confidence or discordant evidence)"
        elif p[i] >= 0.5 and r["risk_band"] == "High":
            rec = (f"Refer to epilepsy centre / expedite: high drug-resistance risk + high recurrence; "
                   f"consider presurgical evaluation ({r['focus_side']} focus, {r['eeg_focus_channel']}).")
        elif p[i] >= 0.5:
            rec = "Specialist review + regimen optimisation; closer follow-up."
        else:
            rec = "Continue current management with routine follow-up + remote monitoring."
        rows.append({"patient_id": r["patient_id"], "severity": int(r["severity_level"]),
                     "drug_resist_p": round(float(p[i]), 3), "recurrence": r["risk_band"],
                     "focus": r["focus_side"], "confident": gated and bool(confident[i]),
                     "concordance": r["concordance"], "auto_recommendable": gated,
                     "recommendation": rec})
    out = pd.DataFrame(rows)
    return out


def build_report(v):
    ep = v["ep"]
    S = [f"""# Integrated Multimodal Clinical Decision Support (Flagship #6)

> **Why (this doc):** The capstone engine that fuses every flagship output — severity
> classification, drug-resistance risk, recurrence risk, and EEG focus — behind the two
> governance gates (C5 confidence, C6 concordance), producing ONE governed decision per patient
> under human oversight. **How:** `analysis/decision_support.py` reads the other pipelines'
> artefacts and assembles the decision; the neurologist retains final authority.

## Cohort: auto-recommendable vs mandatory review

{caption("How many patients pass BOTH governance gates (auto-recommendable) versus routed to the clinician.")}

{df_to_md(v['summary'])}

**{v['auto_pct']}%** of patients are auto-recommendable (confident + concordant); the rest are
routed to mandatory clinician review — the operational meaning of human oversight.

## EP001 — integrated decision card

{caption("Every flagship output for EP001, the governance gates, and the resulting governed recommendation.")}

| Field | Value |
|---|---|
| Severity (classification) | Level {ep['severity']} |
| Drug-resistance risk (fusion) | {ep['drug_resist_p']} |
| Recurrence risk (survival) | {ep['recurrence']} |
| EEG focus (DSP) | {ep['focus']} |
| Confidence gate (C5) | {'PASS' if ep['confident'] else 'DEFER'} |
| Concordance gate (C6) | {ep['concordance']} |
| Auto-recommendable | {ep['auto_recommendable']} |
| **Recommendation** | {ep['recommendation']} |

## Governed decision flow

```mermaid
flowchart TD
    C[Classification] --> ENG[Multimodal Engine]
    DR[Drug-resistance risk] --> ENG
    RC[Recurrence risk] --> ENG
    FO[EEG focus] --> ENG
    ENG --> G5{{C5 confident?}}
    G5 -->|no| REV[Mandatory clinician review]
    G5 -->|yes| G6{{C6 concordant?}}
    G6 -->|no| REV
    G6 -->|yes| REC[Governed recommendation]
    REC --> N[Neurologist confirms]
    REV --> N
```

**Reason:** Show how all flagships fuse behind the governance gates. **Why:** A recommendation is issued only when the AI is BOTH confident AND the evidence agrees. **What is happening:** Four flagship signals feed one engine; two gates decide recommend-vs-defer; the clinician confirms. **How it is happening:** Calibrated probability margin (C5) + source agreement (C6) gate the output. **Reference:** NIST (2023); Topol (2019).

## Professor Readiness (Defense Q&A)

**Q1: What is the contribution here?** A single governed engine that fuses multiple EEG-based
flagships and only recommends when confident and concordant — the Responsible-AI thesis in action.

**Q2: Why defer some patients?** Low confidence or conflicting evidence means the safe action is
human review, not an autonomous recommendation.

**Q3: How does EP001 flow through it?** Severe + high drug-resistance + high recurrence + concordant
left-temporal focus → passes both gates → expedite/presurgical recommendation, clinician-confirmed.

## References

NIST. (2023). *AI Risk Management Framework (AI RMF 1.0)*.

Topol, E. J. (2019). *Deep medicine*. Basic Books.
"""]
    return write_report("integrated-decision-support.md", S)


def main():
    banner("decision_support — integrated multimodal CDSS (flagship #6)")
    df, feats = load()
    dec = assemble(df, feats)
    dec.to_csv(os.path.join(DATA_DIR, "decisions.csv"), index=False)
    summary = dec["auto_recommendable"].value_counts().rename_axis("auto_recommendable").reset_index(name="patients")
    auto_pct = round(100 * dec["auto_recommendable"].mean(), 1)
    ep = dec[dec.patient_id == "EP001"].iloc[0].to_dict()
    path = build_report(dict(summary=summary, auto_pct=auto_pct, ep=ep))
    print(f"  auto-recommendable={auto_pct}%  deferred={100-auto_pct}%")
    print(f"  EP001: sev L{ep['severity']} DRp={ep['drug_resist_p']} rec={ep['recurrence']} "
          f"focus={ep['focus']} auto={ep['auto_recommendable']}")
    print(f"  report -> {path}")


if __name__ == "__main__":
    main()
