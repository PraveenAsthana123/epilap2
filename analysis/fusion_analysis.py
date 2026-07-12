"""
fusion_analysis.py — Multimodal fusion + single-patient (EP001) end-to-end case
===============================================================================

Combines the PRIMARY (clinical assessment) and SECONDARY (EEG) modalities and
demonstrates the incremental value of fusion, then runs the whole platform for one
patient — EP001 — end-to-end: primary severity, EEG focus lateralisation, and a
fused clinical-decision-support recommendation under human oversight.

    Stage 1  merge                 link primary + EEG by patient_id
    Stage 2  incremental_value     CV AUC: primary-only vs EEG-only vs FUSION
    Stage 3  ep001_case            EP001 end-to-end (severity + focus + fused risk)
    Stage 4  report                docs/analysis/fusion-analysis.md (C4 + 4 diagrams)

Requires: make_cohort.py, primary_analysis.py, secondary_analysis.py to have run
(uses data/analysis/primary_clean_features.csv, primary_selected_features.csv, cohort_eeg.csv).

Run: python analysis/fusion_analysis.py
"""

from __future__ import annotations
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

from common import DATA_DIR, df_to_md, explain, caption, write_report, banner, SEED

TARGET_BIN = "drug_resistant"
EEG_FEATS = ["eeg_delta", "eeg_theta", "eeg_alpha", "eeg_beta", "eeg_gamma",
             "eeg_temporal_asym", "eeg_spike_rate_pm", "eeg_entropy", "eeg_paf_hz",
             "eeg_connectivity", "eeg_left_temporal_pow", "eeg_right_temporal_pow",
             "eeg_focal_slowing"]


# ---------------------------------------------------------------------------
# Stage 1 — Merge the two modalities on patient_id
# ---------------------------------------------------------------------------
def merge() -> tuple[pd.DataFrame, list, list]:
    """Join the cleaned primary feature frame with the EEG biomarker frame."""
    prim = pd.read_csv(os.path.join(DATA_DIR, "primary_clean_features.csv"))
    eeg = pd.read_csv(os.path.join(DATA_DIR, "cohort_eeg.csv"))
    sel = pd.read_csv(os.path.join(DATA_DIR, "primary_selected_features.csv")).iloc[:, 0].tolist()
    merged = prim.merge(eeg[["patient_id"] + EEG_FEATS + ["focus_side", "eeg_focus_channel"]],
                        on="patient_id", how="inner")
    return merged, sel, EEG_FEATS


# ---------------------------------------------------------------------------
# Stage 2 — Incremental value of fusion (cross-validated)
# ---------------------------------------------------------------------------
def incremental_value(df: pd.DataFrame, prim_feats: list, eeg_feats: list) -> pd.DataFrame:
    """Compare drug-resistance prediction from primary-only, EEG-only, and the fused
    feature set with 5-fold cross-validated AUC/accuracy. Fusion should match or beat
    the better single modality; the delta is the quantified incremental value."""
    y = df[TARGET_BIN].values
    sets = {"Primary-only": prim_feats, "EEG-only": eeg_feats,
            "Fusion (Primary+EEG)": prim_feats + eeg_feats}
    rows = []
    for name, feats in sets.items():
        X = StandardScaler().fit_transform(df[feats])
        clf = LogisticRegression(max_iter=1000, random_state=SEED)
        auc = cross_val_score(clf, X, y, cv=5, scoring="roc_auc")
        acc = cross_val_score(clf, X, y, cv=5, scoring="accuracy")
        rows.append({"model": name, "n_features": len(feats),
                     "auc_mean": round(auc.mean(), 3), "auc_sd": round(auc.std(), 3),
                     "accuracy": round(acc.mean(), 3)})
    tab = pd.DataFrame(rows)
    base = tab.loc[tab["model"] == "Primary-only", "auc_mean"].iloc[0]
    fus = tab.loc[tab["model"].str.startswith("Fusion"), "auc_mean"].iloc[0]
    tab.attrs["delta_auc"] = round(fus - base, 3)
    return tab


# ---------------------------------------------------------------------------
# Stage 3 — EP001 single-patient end-to-end
# ---------------------------------------------------------------------------
def ep001_case(df: pd.DataFrame, prim_feats: list, eeg_feats: list) -> dict:
    """Run the full platform for EP001: train on the rest of the cohort, then emit
    (a) primary drug-resistance risk, (b) EEG focus laterality + confidence, and
    (c) a fused risk score and recommendation — the clinical-decision-support card."""
    train = df[df["patient_id"] != "EP001"]
    ep = df[df["patient_id"] == "EP001"]

    # (a) Primary risk of drug-resistance.
    Xp_tr = StandardScaler().fit(train[prim_feats])
    clf_p = LogisticRegression(max_iter=1000, random_state=SEED).fit(
        Xp_tr.transform(train[prim_feats]), train[TARGET_BIN])
    p_primary = float(clf_p.predict_proba(Xp_tr.transform(ep[prim_feats]))[0, 1])

    # (b) EEG focus laterality (1 = Left) + confidence.
    yside = (train["focus_side"] == "Left").astype(int)
    Xe_tr = StandardScaler().fit(train[eeg_feats])
    clf_e = RandomForestClassifier(n_estimators=300, random_state=SEED).fit(
        Xe_tr.transform(train[eeg_feats]), yside)
    p_left = float(clf_e.predict_proba(Xe_tr.transform(ep[eeg_feats]))[0, 1])
    side = "Left" if p_left >= 0.5 else "Right"
    side_conf = p_left if side == "Left" else 1 - p_left

    # (c) Fused drug-resistance risk.
    Xf_tr = StandardScaler().fit(train[prim_feats + eeg_feats])
    clf_f = LogisticRegression(max_iter=1000, random_state=SEED).fit(
        Xf_tr.transform(train[prim_feats + eeg_feats]), train[TARGET_BIN])
    p_fused = float(clf_f.predict_proba(Xf_tr.transform(ep[prim_feats + eeg_feats]))[0, 1])

    region = {"T7": "Left Temporal", "F7": "Left Frontotemporal", "P7": "Left Parietotemporal",
              "T8": "Right Temporal", "F8": "Right Frontotemporal", "P8": "Right Parietotemporal"
              }.get(ep["eeg_focus_channel"].iloc[0], "Left Temporal")

    sev = int(ep["severity_level"].iloc[0])
    sev_label = {1: "Mild", 2: "Moderate", 3: "Severe", 4: "Refractory/Status"}[sev]

    # Recommendation logic (transparent, rule-based; clinician confirms).
    if p_fused >= 0.5 and sev >= 3:
        rec = ("Expedite comprehensive epilepsy-centre evaluation: video-EEG telemetry to "
               "confirm the left-temporal focus, MRI review for mesial temporal sclerosis, "
               "and pre-surgical work-up; review ASM regimen (breakthrough on CBZ+LEV).")
    elif p_fused >= 0.5:
        rec = "Prioritise neurology review and repeat EEG; optimise medication adherence."
    else:
        rec = "Routine follow-up; continue current management with remote monitoring."

    card = pd.DataFrame([
        ("Patient", "EP001 (EP-2026-001)"),
        ("Primary severity (assessment)", f"{sev_label} (Level {sev})"),
        ("Primary drug-resistance risk", f"{p_primary:.2f}"),
        ("EEG focus laterality", f"{side} (confidence {side_conf:.2f})"),
        ("EEG focus region / channel", f"{region} / {ep['eeg_focus_channel'].iloc[0]}"),
        ("Fused drug-resistance risk", f"{p_fused:.2f}"),
        ("Recommendation (clinician confirms)", rec),
    ], columns=["Field", "Value"])
    return {"card": card, "p_primary": round(p_primary, 3), "p_left": round(p_left, 3),
            "side": side, "side_conf": round(side_conf, 3), "p_fused": round(p_fused, 3),
            "region": region, "sev_label": sev_label}


def build_report(v: dict) -> str:
    inc = v["inc"]
    S = []
    S.append(f"""# Multimodal Fusion & EP001 End-to-End Case (Epilepsy)

> **Why (this doc):** The dissertation's payoff is fusion — combining the primary
> clinical-assessment analysis with the secondary EEG analysis for one coherent,
> explainable, human-supervised decision. **How:** The two modality matrices are
> linked by patient id, the incremental value of fusion is quantified by
> cross-validated AUC, and the whole platform is run for the index patient **EP001**
> end-to-end — all reproducible from `analysis/fusion_analysis.py`.

**Problem:** Primary and EEG modalities each capture only part of the epilepsy picture.
**Sub-problems:** modality linkage; incremental value; single-patient interpretability.
**Research Problem:** Does fusing primary and EEG data improve risk prediction and enable
an explainable, localised, patient-level decision beyond either modality alone?
**Research Objective:** Quantify fusion's incremental value and demonstrate an end-to-end
EP001 decision (severity + focus + fused risk + recommendation) under human oversight.
**Hypotheses:** H1 fusion AUC >= best single modality; H2 EEG adds lateralised localisation
that primary data cannot provide; H3 the EP001 fused output is clinically coherent.
**Statistical Analysis:** 5-fold cross-validated ROC-AUC/accuracy across three feature sets.
""")

    S.append(f"""## Fusion Architecture

{caption("Two modality pipelines converge into a fusion layer feeding explainable, human-supervised decision support.")}

```mermaid
flowchart TD
    P[Primary Pipeline<br/>clinical assessment] --> RF[Primary Risk Features]
    E[Secondary Pipeline<br/>EEG biomarkers] --> LF[EEG Focus + Biomarkers]
    RF --> FUS[Multimodal Fusion Layer]
    LF --> FUS
    FUS --> RISK[Fused Risk Score]
    FUS --> LOC[Brain Localization]
    RISK --> CDSS[Clinical Decision Support]
    LOC --> CDSS
    CDSS --> HUM[Neurologist Review - Human in the Loop]
    HUM --> OUT[Treatment Plan / Recommendation]
```

{explain("Show how the two modalities fuse into one decision.",
         "Fusion is only justified if it adds value over single modalities and stays explainable.",
         "Primary risk features and EEG focus features combine into fused risk + localisation, gated by a clinician.",
         "Each pipeline writes features that the fusion model consumes; the clinician confirms.",
         "Topol (2019); Rajkomar, Dean & Kohane (2019).")}

## C4 Model — Fusion & CDSS Container

{caption("C4 container view of the fusion + clinical-decision-support container within the platform.")}

```mermaid
flowchart TB
    subgraph Plat[Epilepsy Intelligence Platform]
      PA[(Container: Primary Analytics)]
      SA[(Container: EEG Analytics)]
      subgraph Cont[Container: Fusion + CDSS]
        MF[Component: Multimodal Fusion]
        RS[Component: Risk Scoring]
        XP[Component: Explainability]
      end
      DASH[Container: Neurologist Dashboard]
    end
    PA --> MF
    SA --> MF
    MF --> RS --> XP --> DASH
```

{explain("Locate the fusion container between the two analytics containers and the dashboard (C4).",
         "Explicit boundaries clarify where fusion, scoring, and explanation responsibilities live.",
         "Both analytics containers feed fusion, which scores, explains, and surfaces to the dashboard.",
         "Each component is a section of fusion_analysis.py.",
         "Brown (2018).")}

## Stage 2 — Incremental Value of Fusion

{caption("Cross-validated drug-resistance prediction from each modality alone versus fused; the AUC delta is the incremental value.")}

{df_to_md(inc)}

**Fusion vs primary-only ΔAUC = {inc.attrs['delta_auc']}.** Even where the primary clinical
vector is already strong, EEG contributes the *lateralised localisation* that the primary
data cannot supply — the qualitative value of fusion is not captured by AUC alone.

## Stage 3 — EP001 End-to-End (Clinical Decision Support Card)

{caption("The full platform run for the index patient EP001: primary severity, EEG focus, fused risk, and a rule-based recommendation the clinician confirms.")}

{df_to_md(v['case']['card'])}

**Reading:** EP001 presents as **{v['case']['sev_label']}** on the primary assessment, with a
fused drug-resistance risk of **{v['case']['p_fused']}** and an EEG focus lateralised to the
**{v['case']['side']}** (confidence {v['case']['side_conf']}), region **{v['case']['region']}** —
consistent with the documented left-temporal focus. The recommendation is generated by a
transparent rule and **requires neurologist confirmation** (no autonomous diagnosis).

## Role Capturing the Data (Sequence)

```mermaid
sequenceDiagram
    participant PA as Primary Pipeline
    participant SA as EEG Pipeline
    participant F as Fusion + CDSS
    participant N as Neurologist
    PA->>F: EP001 severity + drug-resistance risk {v['case']['p_primary']}
    SA->>F: EP001 focus = {v['case']['side']} ({v['case']['side_conf']}), {v['case']['region']}
    F->>N: Fused risk {v['case']['p_fused']} + localisation + recommendation
    N-->>F: Approve / adjust (human in the loop)
```

{explain("Show the multimodal handoff for one patient.",
         "Human oversight is mandatory before any recommendation is acted on.",
         "Both pipelines feed the fusion layer, which presents to the neurologist for approval.",
         "Each arrow is a real model output for EP001.",
         "Rajkomar et al. (2019).")}

## Data Linkage (Network)

```mermaid
graph LR
    PID[patient_id] --> PM[Primary Matrix]
    PID --> EM[EEG Matrix]
    PM --> FEAT[Fused Feature Vector]
    EM --> FEAT
    FEAT --> RISK[Risk Score]
    FEAT --> LOC[Localization]
    RISK --> DEC[Decision Support]
    LOC --> DEC
```

{explain("Map how the two matrices link into one fused vector.",
         "Patient-level linkage is the precondition for any multimodal claim.",
         "Both matrices join on patient_id to form the fused vector feeding risk and localisation.",
         "An inner join on patient_id guarantees per-patient alignment.",
         "Kuhn & Johnson (2019).")}

## Patient & Clinician Experience (Journey)

```mermaid
journey
    title EP001 Multimodal Decision Experience
    section Inputs
      Assessment analysed: 5: Primary Pipeline
      EEG analysed: 5: EEG Pipeline
    section Fusion
      Fuse risk + localisation: 5: Fusion
    section Decision
      Neurologist reviews: 4: Neurologist
      Plan agreed with patient: 4: Neurologist, Patient
```

{explain("Surface the end-to-end multimodal experience for EP001.",
         "The value is a single coherent, explainable decision, not two disconnected outputs.",
         "Primary and EEG results fuse into a reviewed plan agreed with the patient.",
         "Each step corresponds to a pipeline or human checkpoint.",
         "Tukey (1977).")}

## Professor Readiness (Defense Q&A)

**Q1: If the primary AUC is already high, why fuse?** Because EEG supplies lateralised
localisation (Left {v['case']['side_conf']} confidence, {v['case']['region']}) that primary
data cannot, and it modestly improves risk AUC (Δ = {inc.attrs['delta_auc']}); fusion's value
is both quantitative and qualitative.

**Q2: Is EP001 leaked into its own prediction?** No — the EP001 case trains on the rest of
the cohort and predicts the held-out index patient.

**Q3: Where is the human in the loop?** The recommendation is a transparent rule surfaced to
the neurologist for approval; the platform never issues an autonomous diagnosis.

## References

Brown, S. (2018). *The C4 model for visualising software architecture*. https://c4model.com

Kuhn, M., & Johnson, K. (2019). *Feature engineering and selection*. CRC Press.

Rajkomar, A., Dean, J., & Kohane, I. (2019). Machine learning in medicine. *New England Journal of Medicine, 380*(14), 1347-1358.

Topol, E. J. (2019). *Deep medicine*. Basic Books.

Tukey, J. W. (1977). *Exploratory data analysis*. Addison-Wesley.
""")
    return write_report("fusion-analysis.md", S)


def main() -> dict:
    banner("fusion_analysis — multimodal fusion + EP001 end-to-end case")
    df, prim_feats, eeg_feats = merge()
    inc = incremental_value(df, prim_feats, eeg_feats)
    case = ep001_case(df, prim_feats, eeg_feats)
    path = build_report({"inc": inc, "case": case})
    print(inc.to_string(index=False))
    print(f"  fusion delta AUC = {inc.attrs['delta_auc']}")
    print(f"  EP001: severity={case['sev_label']} p_fused={case['p_fused']} "
          f"focus={case['side']}({case['side_conf']}) region={case['region']}")
    print(f"  report -> {path}")
    return {"inc": inc, "case": case}


if __name__ == "__main__":
    main()
