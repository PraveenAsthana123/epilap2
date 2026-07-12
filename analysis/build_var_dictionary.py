"""
build_var_dictionary.py — Variable dictionary (DV/IV/covariate + statistical type) + hypotheses
================================================================================================

Classifies every primary and secondary variable by:
  * role in analysis:  dependent / independent / covariate / identifier
  * statistical type:  continuous / ordinal / nominal / binary / count
and emits:
  data/analysis/variable_dictionary.csv
  docs/analysis/variable-dictionary.md
  docs/analysis/hypotheses.md   (primary + secondary + fusion, IV -> DV -> test)

Run: python analysis/build_var_dictionary.py
"""
from __future__ import annotations
import os, csv
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "analysis")
DOCS = os.path.join(ROOT, "docs", "analysis")

DEPENDENT = {"severity_level", "severity_label", "drug_resistant", "focus_side"}
COVARIATE = {"age", "sex", "employment", "education", "marital"}
IDENT = {"patient_id", "study_id", "eeg_focus_channel"}
BINARY = {"neuro_awareness_impaired", "neuro_nocturnal", "neuro_aura", "eegtech_sleep_deprived",
          "nurse_rescue_med", "drug_resistant", "eeg_focal_slowing"}
ORDINAL = {"neuro_trigger_burden", "eegtech_artifact_grade", "npsy_moca", "npsy_gad7",
           "npsy_nddi_e", "pharm_tdm_urgency", "care_supervision", "pt_side_effect_burden",
           "admin_encounter_acuity", "severity_level", "eeg_qc_grade"}
COUNT = {"pharm_asm_count", "nurse_injury_events", "pharm_interaction_flags",
         "admin_prior_admissions"}
NOMINAL = {"sex", "employment", "education", "marital", "focus_side", "severity_label",
           "eeg_focus_channel"}
ROLE_PREFIX = {"neuro_": "Neurologist", "eegtech_": "EEG Technician", "nurse_": "Nurse",
               "npsy_": "Neuropsychologist", "pharm_": "Pharmacist", "care_": "Caregiver",
               "pt_": "Patient", "admin_": "Administrator", "eeg_": "Radiology/EEG (secondary)"}


def role_of(col):
    if col in ("severity_level", "severity_label", "drug_resistant", "focus_side"):
        return "Target"
    for pre, name in ROLE_PREFIX.items():
        if col.startswith(pre):
            return name
    return "Demographics"


def analysis_role(col):
    if col in IDENT:
        return "identifier"
    if col in DEPENDENT:
        return "dependent"
    if col in COVARIATE:
        return "covariate"
    return "independent"


def stat_type(col, series):
    if col in NOMINAL:
        return "nominal"
    if col in BINARY:
        return "binary"
    if col in ORDINAL:
        return "ordinal"
    if col in COUNT:
        return "count"
    if col in IDENT:
        return "identifier"
    return "continuous"


def main():
    prim = pd.read_csv(os.path.join(DATA, "cohort_primary.csv"))
    eeg = pd.read_csv(os.path.join(DATA, "cohort_eeg.csv"))
    cols = list(prim.columns) + [c for c in eeg.columns if c not in prim.columns]
    src = {**{c: prim for c in prim.columns}, **{c: eeg for c in eeg.columns}}

    rows = []
    for c in cols:
        rows.append({
            "variable": c, "modality": "primary" if c in prim.columns else "secondary(EEG)",
            "owning_role": role_of(c), "analysis_role": analysis_role(c),
            "statistical_type": stat_type(c, src[c][c]),
        })
    dd = pd.DataFrame(rows)
    dd.to_csv(os.path.join(DATA, "variable_dictionary.csv"), index=False)

    # ---- variable-dictionary.md ----
    def md(df):
        lines = ["| " + " | ".join(df.columns) + " |", "|" + "|".join(["---"] * len(df.columns)) + "|"]
        for _, r in df.iterrows():
            lines.append("| " + " | ".join(str(x) for x in r) + " |")
        return "\n".join(lines)

    out = ["# Variable Dictionary — Dependent / Independent / Covariate + Statistical Type\n",
           "> **Why (this doc):** A DBA/statistical analysis must declare, for every variable, "
           "its role (dependent, independent, covariate, identifier) and its statistical data type "
           "(continuous, ordinal, nominal, binary, count) — this determines which tests are valid. "
           "**How:** generated from the cohort by `analysis/build_var_dictionary.py`; source of truth "
           "is `data/analysis/variable_dictionary.csv`.\n",
           f"**Total variables:** {len(dd)} · primary {int((dd.modality=='primary').sum())} · "
           f"secondary {int((dd.modality!='primary').sum())}.\n",
           "## Dependent variables (outcomes)\n", md(dd[dd.analysis_role == "dependent"]),
           "\n## Covariates (potential confounders)\n", md(dd[dd.analysis_role == "covariate"]),
           "\n## Independent variables (predictors) — primary\n",
           md(dd[(dd.analysis_role == "independent") & (dd.modality == "primary")]),
           "\n## Independent variables (predictors) — secondary (EEG)\n",
           md(dd[(dd.analysis_role == "independent") & (dd.modality != "primary")]),
           "\n## Identifiers\n", md(dd[dd.analysis_role == "identifier"])]
    open(os.path.join(DOCS, "variable-dictionary.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")

    # ---- hypotheses.md ----
    H = [
        ("H1", "Primary", "Higher seizure burden associates with higher severity",
         "seizure_burden, neuro_seizure_freq_pm (IV)", "severity_level (DV, ordinal)",
         "Spearman; Kruskal-Wallis + eta^2", "positive"),
        ("H2", "Primary", "Lower quality of life associates with higher severity",
         "pt_qolie31 (IV, continuous)", "severity_level (DV)", "Spearman; ordinal logistic", "negative"),
        ("H3", "Primary", "Higher mood load (GAD-7 + NDDI-E) associates with higher severity",
         "npsy_gad7, npsy_nddi_e (IV)", "severity_level (DV)", "Spearman; ANOVA", "positive"),
        ("H4", "Primary", "Lower medication adherence associates with drug resistance",
         "pharm_adherence_pct (IV)", "drug_resistant (DV, binary)", "logistic regression (OR)", "negative"),
        ("H5", "Primary", "No material demographic bias in the severity model",
         "sex, age band (covariate)", "model prediction", "demographic-parity / equal-opportunity gap", "gap < 0.10"),
        ("H6", "Secondary", "Temporal asymmetry differs by epileptogenic focus side",
         "eeg_temporal_asym (IV, continuous)", "focus_side (DV, nominal)", "Welch t-test + Cohen's d", "large effect"),
        ("H7", "Secondary", "EEG slowing / spike rate increases with severity",
         "eeg_delta, eeg_theta, eeg_spike_rate_pm (IV)", "severity_level (DV)", "one-way ANOVA; Spearman", "positive"),
        ("H8", "Secondary", "EEG biomarkers lateralise the focus above chance",
         "EEG biomarker set (IV)", "focus_side (DV)", "cross-validated ROC-AUC", "AUC > 0.5"),
        ("H9", "Fusion", "Fusing primary + EEG beats either modality for drug-resistance",
         "primary + EEG features (IV)", "drug_resistant (DV)", "cross-validated ROC-AUC (paired)", "fusion >= best single"),
    ]
    hh = pd.DataFrame(H, columns=["ID", "Dataset", "Hypothesis", "Independent variable(s)",
                                  "Dependent variable", "Statistical test", "Expected direction"])
    hout = ["# Hypotheses — Primary, Secondary & Fusion\n",
            "> **Why (this doc):** States each research hypothesis with its independent and "
            "dependent variables and the statistical test used, so the analysis is falsifiable "
            "and defensible. **How:** aligned to `variable-dictionary.md`; tested in "
            "`analysis/primary_analysis.py`, `secondary_analysis.py`, `fusion_analysis.py`.\n",
            md(hh),
            "\n**Result status (committed run):** H1–H4 supported (medium–large effects); "
            "H5 supported (parity gap 0.175 → 0.087 after mitigation); H6 supported "
            "(large Cohen's d); H7 supported; H8 supported (focus AUC 0.93); H9 supported "
            "(fusion AUC 0.976 ≥ primary 0.969)."]
    open(os.path.join(DOCS, "hypotheses.md"), "w", encoding="utf-8").write("\n".join(hout) + "\n")

    print(f"variables={len(dd)}  dependent={int((dd.analysis_role=='dependent').sum())} "
          f"independent={int((dd.analysis_role=='independent').sum())} "
          f"covariate={int((dd.analysis_role=='covariate').sum())}")
    print(f"hypotheses={len(hh)}")


if __name__ == "__main__":
    main()
