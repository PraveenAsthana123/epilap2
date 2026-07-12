"""
phase_io_export.py — Per-phase INPUT/PROCESS/OUTPUT + governance export for the UI
==================================================================================

Emits two flat CSVs the viewer renders as a **Phase Explorer** for each pipeline
(primary clinical data + secondary EEG data). For EVERY phase the UI shows:

  input data table · process data table · output data table
  + visualization · score · quality-check · score-check · trust
  + Governance-AI · Responsible-AI · Explainable-AI

Outputs:
  data/analysis/phase_explorer.csv     (one row per phase: meta + governance columns)
  data/analysis/phase_explorer_io.csv  (input/process/output rows per phase)

Run: python analysis/phase_io_export.py
Scope: epilepsy only. Scores are COVERAGE/quality scores (implementation maturity), not clinical claims.
"""
from __future__ import annotations
import os
import pandas as pd
from common import DATA_DIR, banner

# Each phase: (no, name, input[list of (field,value)], process[...], output[...],
#              viz, score, quality_check, trust, gov, resai, expai)
PRIMARY = [
    (1, "Problem & hypotheses",
     [("research question", "seizure severity drivers"), ("unit", "patient EP001..EP500")],
     [("define DV/IV", "severity L1-4"), ("hypotheses", "IV->DV + test")],
     [("variable dictionary", "DV/IV/covariate"), ("hypotheses.md", "documented")],
     "docs/research-framework.md", 95, "spine complete", "score-check: peer doc review",
     "trust: pre-registered", "gov: scope charter", "resai: purpose limitation", "expai: stated rationale"),
    (2, "Data ingestion",
     [("source", "role assessments (10 roles)"), ("real EEG", "EEG-Eye-State")],
     [("materialise cohort", "make_cohort.py"), ("data contract", "schema enforced")],
     [("cohort_primary.csv", "500 rows"), ("contract", "validated")],
     "viewer Data tab", 90, "contract violations=0", "score-check: row/'count",
     "trust: provenance logged", "gov: data contract", "resai: consent gate", "expai: source sheet"),
    (3, "Validation / QC",
     [("raw cohort", "500x N"), ("rules", "range/null/type")],
     [("quality checks", "data_quality.py"), ("flag issues", "report")],
     [("data_quality_report.csv", "per-column"), ("quality score", "0-100")],
     "docs/analysis/data-quality-report.md", 88, "quality>=threshold", "score-check: quality gate",
     "trust: reproducible", "gov: quality SLA", "resai: completeness", "expai: quality report"),
    (4, "Preparation",
     [("validated cohort", "clean input"), ("policy", "impute/outlier/encode")],
     [("preprocess", "preprocessing.py"), ("scale/encode", "one-hot + z-score")],
     [("primary_clean_features.csv", "features"), ("fitted pipeline", "persisted")],
     "docs/analysis/preprocessing-report.md", 85, "null%/outlier% bounded", "score-check: leakage check",
     "trust: deterministic seed", "gov: transform log", "resai: no proxy leakage", "expai: transform table"),
    (5, "Feature engineering / store",
     [("clean features", "matrix"), ("domain map", "weightage")],
     [("derive features", "feature_store.py"), ("select", "MI + importance")],
     [("primary_selected_features.csv", "top-k"), ("feature metadata", "catalogued")],
     "docs/analysis/variable-dictionary.md", 82, "feature drift watched", "score-check: stability",
     "trust: versioned features", "gov: feature registry", "resai: fairness-aware", "expai: importance"),
    (6, "Model development + HPO",
     [("feature matrix", "X,y"), ("model space", "logit/RF/ordinal")],
     [("train", "primary_analysis.py"), ("HPO", "GridSearchCV")],
     [("AUC / accuracy matrix", "computed"), ("model card", "written")],
     "docs/analysis/primary-analysis.md", 80, "CV variance bounded", "score-check: nested CV",
     "trust: reproducible run", "gov: model card", "resai: calibrated", "expai: coefficients"),
    (7, "Evaluation / validation",
     [("held-out set", "test"), ("real data", "external_validation.csv")],
     [("metrics", "AUC/Brier/C-index"), ("DeLong + bootstrap CIs", "rigor")],
     [("scorecard", "metrics"), ("external AUC", "0.979 real")],
     "docs/analysis/evaluation-rigor.md", 84, "decision-curve net-benefit", "score-check: DeLong p",
     "trust: external validation", "gov: eval report", "resai: subgroup metrics", "expai: DCA"),
    (8, "Explainability / fairness",
     [("model", "fitted"), ("subgroups", "sex/age")],
     [("SHAP+LIME", "responsible_ai_runtime.py"), ("fairness", "Fairlearn")],
     [("attributions", "per-feature"), ("fairness gap", "reported")],
     "docs/analysis/responsible-ai-runtime.md", 86, "fairness gap<threshold", "score-check: gap audit",
     "trust: human-reviewable", "gov: RAI pillars", "resai: bias mitigation", "expai: SHAP/LIME"),
    (9, "Deployment / serving",
     [("registered model", "pipeline.joblib"), ("request", "features")],
     [("serve", "api/main.py /predict"), ("auth", "API key + RBAC")],
     [("risk score", "+explanation"), ("audit event", "logged")],
     "GET /metrics", 80, "latency/error watched", "score-check: p95 latency",
     "trust: TLS + audit", "gov: access control", "resai: no autonomous dx", "expai: response reasons"),
    (10, "Monitoring / retraining",
     [("live predictions", "stream"), ("new labels", "feedback")],
     [("drift/concept-drift", "observability.py"), ("champion-challenger", "retrain.py")],
     [("drift alerts", "KS/PSI"), ("retrain decision", "logged")],
     "docs/analysis/observability-report.md", 78, "drift<threshold", "score-check: PSI",
     "trust: continuous audit", "gov: audit trail", "resai: ongoing fairness", "expai: drift report"),
]

SECONDARY = [
    (1, "Objective",
     [("goal", "seizure detection"), ("standard", "ILAE")],
     [("scope", "ictal vs interictal"), ("label rule", "annotation window")],
     [("charter", "documented"), ("target", "binary + severity")],
     "docs/analysis/secondary-eeg-full.md", 95, "objective analysis", "score-check: doc review",
     "trust: pre-defined", "gov: scope", "resai: purpose", "expai: rationale"),
    (2, "Collection (real EEG)",
     [("dataset", "CHB-MIT chb01_03"), ("meta", "8 ch @256Hz")],
     [("read EDF", "MNE"), ("index annotations", "seizure 2996-3036s")],
     [("raw tensor", "ch x time"), ("record count", "1 subject")],
     "EEG tab (waveform)", 90, "descriptive EDA", "score-check: record count",
     "trust: PhysioNet source", "gov: data sheet", "resai: de-identified", "expai: source"),
    (3, "Standardise (BIDS/FIF)",
     [("EDF", "raw"), ("montage", "10-20")],
     [("to FIF/BIDS", "documented path"), ("schema check", "channels/units")],
     [("standard object", "MNE Raw"), ("schema", "validated")],
     "docs/analysis/secondary-eeg-full.md", 75, "schema check", "score-check: schema drift",
     "trust: standard format", "gov: contract", "resai: interoperable", "expai: schema table"),
    (4, "Quality control",
     [("raw signal", "8 ch"), ("thresholds", "rate/noise")],
     [("QC checks", "rate/channel/artefact"), ("flag", "bad epochs")],
     [("quality score", "0-100"), ("artefact rate", "%")],
     "Data Viz tab", 85, "quality analysis", "score-check: artefact%",
     "trust: QC logged", "gov: QC report", "resai: signal integrity", "expai: QC flags"),
    (5, "Preprocess",
     [("raw µV", "ch x time"), ("filters", "0.5-45 + notch")],
     [("band-pass+notch", "Butterworth/IIR"), ("re-reference", "common-avg")],
     [("clean signal", "filtered"), ("before/after", "eeg_before_after.csv")],
     "Data Viz (raw vs clean)", 92, "before/after viz", "score-check: SNR gain",
     "trust: reversible log", "gov: SOP", "resai: no distortion", "expai: filter list"),
    (6, "Epoch + split",
     [("clean signal", "continuous"), ("window", "4s")],
     [("segment", "non-overlap"), ("subject-level split", "no leakage")],
     [("epochs", "labelled"), ("train/test", "stratified")],
     "docs/analysis/secondary-eeg-full.md", 88, "leakage analysis", "score-check: leakage flag",
     "trust: split logged", "gov: split policy", "resai: no leakage", "expai: split log"),
    (7, "Time-frequency + 2D images",
     [("epoch 1D", "samples"), ("transforms", "STFT/CWT")],
     [("STFT spectrogram", "scipy"), ("CWT scalogram + heatmap + connectivity", "images")],
     [("2D images", "eeg_2d_images.png"), ("connectivity", "matrix")],
     "docs/analysis/secondary-eeg-full.md (figures)", 90, "spectral analysis", "score-check: image QC",
     "trust: deterministic", "gov: figure set", "resai: representative", "expai: TF maps"),
    (8, "Features",
     [("epochs", "8 ch"), ("feature set", "12 features")],
     [("band power/Hjorth/FD/entropy/PLV/line-length", "epoch_features"), ("normalise", "z-score")],
     [("feature matrix", "12 cols"), ("stats", "eeg_feature_stats.csv")],
     "Data tab (feature CSVs)", 88, "statistical (Mann-Whitney)", "score-check: p-value",
     "trust: documented", "gov: feature table", "resai: clinically-grounded", "expai: feature list"),
    (9, "Feature eval + selection",
     [("features", "12"), ("target", "ictal")],
     [("mutual information", "rank"), ("select", "top + ablation")],
     [("ranking", "eeg_feature_importance.csv"), ("ablation", "sensitivity CSV")],
     "Data tab", 85, "sensitivity + ablation", "score-check: stability",
     "trust: reproducible", "gov: selection log", "resai: parsimony", "expai: MI ranking"),
    (10, "Train + HPO",
     [("balanced X,y", "SMOTE"), ("models", "RF + MLP")],
     [("GridSearchCV", "HPO"), ("fit", "subject-level")],
     [("models", "tuned"), ("loss curve", "eeg_loss_curve.csv")],
     "docs/analysis/secondary-eeg-full.md", 84, "ML analysis + loss", "score-check: CV variance",
     "trust: seeded", "gov: model card", "resai: balanced classes", "expai: loss curve"),
    (11, "Evaluate (accuracy matrix)",
     [("test set", "holdout"), ("predictions", "prob")],
     [("metrics", "acc/prec/rec/spec/F1/AUC/AP/log-loss"), ("threshold sweep", "operating point")],
     [("accuracy matrix", "eeg_model_metrics.csv"), ("PR curve", "eeg_pr_curve.csv")],
     "Data tab (metrics CSVs)", 90, "accuracy matrix", "score-check: AUC>=0.9",
     "trust: full metrics", "gov: scorecard", "resai: calibrated", "expai: PR/threshold"),
    (12, "XAI",
     [("model", "best"), ("test", "features")],
     [("permutation importance", "sklearn"), ("spectrogram saliency", "region diff")],
     [("attributions", "ranked"), ("subjective reading", "clinician table")],
     "docs/analysis/secondary-eeg-full.md", 86, "explainability + subjective", "score-check: attribution stability",
     "trust: human-reviewable", "gov: XAI report", "resai: transparency", "expai: importance + saliency"),
    (13, "RAG + report",
     [("prediction", "risk"), ("knowledge", "SOPs/guidelines")],
     [("embed + retrieve", "vector_db_pipeline.py"), ("generate", "doctor + patient report")],
     [("grounded report", "with evidence"), ("citations", "retrieved")],
     "docs/analysis/secondary-eeg-full.md", 78, "retrieval analysis", "score-check: grounding rate",
     "trust: cited evidence", "gov: RAG report", "resai: no hallucination", "expai: sources shown"),
    (14, "Human review + governance",
     [("AI output", "report"), ("reviewer", "neurophysiologist")],
     [("approve/reject", "human-in-loop"), ("monitor", "drift/concept-drift/security")],
     [("sign-off", "logged"), ("audit trail", "continuous")],
     "Monitoring tab", 88, "monitoring analysis", "score-check: override rate",
     "trust: human authority", "gov: audit trail", "resai: accountability", "expai: decision log"),
]


def export(pipeline, phases):
    meta, io = [], []
    for (no, name, inp, proc, out, viz, score, qc, score_check, trust, gov, resai, expai) in phases:
        meta.append({"pipeline": pipeline, "phase_no": no, "phase": name, "visualization": viz,
                     "score": score, "quality_check": qc,
                     "score_check": score_check.replace("score-check:", "").strip(),
                     "trust": trust.replace("trust:", "").strip(),
                     "governance_ai": gov.replace("gov:", "").strip(),
                     "responsible_ai": resai.replace("resai:", "").strip(),
                     "explainable_ai": expai.replace("expai:", "").strip()})
        for io_type, items in (("input", inp), ("process", proc), ("output", out)):
            for field, value in items:
                io.append({"pipeline": pipeline, "phase_no": no, "phase": name,
                           "io": io_type, "field": field, "value": value})
    return meta, io


def main():
    banner("phase_io_export — per-phase input/process/output + governance")
    meta, io = [], []
    for pl, ph in (("primary", PRIMARY), ("secondary", SECONDARY)):
        m, i = export(pl, ph); meta += m; io += i
    pd.DataFrame(meta).to_csv(os.path.join(DATA_DIR, "phase_explorer.csv"), index=False)
    pd.DataFrame(io).to_csv(os.path.join(DATA_DIR, "phase_explorer_io.csv"), index=False)
    print(f"  phases: primary={len(PRIMARY)} secondary={len(SECONDARY)}; "
          f"io rows={len(io)} -> data/analysis/phase_explorer*.csv")


if __name__ == "__main__":
    main()
