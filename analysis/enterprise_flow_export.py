"""
enterprise_flow_export.py — CSVs for the Operating-Model UI (7 pipelines / 40 stages)
=====================================================================================

Emits machine-readable versions of the enterprise operating model so the viewer can render
the seven pipelines, the 40-stage architecture (with status), and an example governed
prediction object.

Outputs:
  data/analysis/enterprise_pipelines.csv       (7 pipelines: owner, question, artefacts)
  data/analysis/enterprise_stages.csv          (40 stages: pipeline, status, evidence)
  data/analysis/prediction_output_example.csv  (governed prediction object, field/value)

Run: python analysis/enterprise_flow_export.py
Scope: epilepsy.
"""
from __future__ import annotations
import os
import pandas as pd
from common import DATA_DIR, banner

PIPELINES = [
    ("P1", "Research & Clinical Protocol", "DBA researcher + epileptologist + statistician",
     "What clinical problem, which population, what outcome?", "protocol, cohort def, target def, SAP, ethics"),
    ("P2", "Data Engineering & Governance", "Data architect + data steward",
     "How does data arrive, get contracted, governed, versioned?", "data contracts, lakehouse zones, catalog, lineage"),
    ("P3", "Data Prep & Feature Engineering", "ML/data engineer",
     "How is data cleaned, labelled, made leakage-safe, stored?", "feature registry, feature store, leakage review"),
    ("P4", "Statistical & ML Modelling", "ML architect + statistician",
     "What model, validated how, calibrated, fair?", "experiments, baselines, validation, calibration"),
    ("P5", "MLOps & Deployment", "ML platform engineer",
     "How is the model registered, served, rolled back, monitored?", "registry, serving, rollback, monitoring"),
    ("P6", "RAG, LLM & Agent Engineering", "GenAI engineer",
     "How is knowledge retrieved and generated safely?", "vector DB, prompt registry, agent policy, LLM eval"),
    ("P7", "Clinical Safety, Responsible-AI & Monitoring", "Clinical safety lead + privacy officer",
     "How is it kept safe, fair, private, overseen?", "safety layer, fairness, consent, audit"),
]

# (no, stage, pipeline, status, evidence)
STAGES = [
    (1, "Business & clinical problem definition", "P1", "done", "pipeline-1"),
    (2, "Research questions & hypotheses", "P1", "done", "pipeline-1 / hypotheses.md"),
    (3, "Outcome / target / horizon definition", "P1", "done", "seizure-recurrence-90d"),
    (4, "Study design & cohort protocol", "P1", "done", "pipeline-1"),
    (5, "Ethics, consent & data-use approval", "P1", "done", "governance/01,02"),
    (6, "Source-system identification", "P2", "partial", "pipelines-2-7 §2"),
    (7, "Data ownership & data contract", "P2", "partial", "mlops/data_contract.py"),
    (8, "Batch/stream/API/CDC ingestion", "P2", "partial", "§4 patterns"),
    (9, "Landing zone & raw immutable storage", "P2", "gap", "§5 lakehouse"),
    (10, "Schema & contract validation", "P2", "done", "mlops/data_contract.py"),
    (11, "Invalid-record quarantine", "P2", "partial", "§5"),
    (12, "Master patient index & entity resolution", "P2", "gap", "§7"),
    (13, "Cleaning & harmonisation", "P3", "done", "preprocessing.py"),
    (14, "Clinical terminology standardisation", "P2", "partial", "ILAE/SNOMED map"),
    (15, "Data-quality scoring", "P2", "done", "mlops/data_quality.py"),
    (16, "Metadata / catalog / lineage", "P2", "partial", "§8"),
    (17, "Sensitive-data classification & security", "P7", "done", "governance/00"),
    (18, "Curated clinical dataset", "P3", "done", "data/analysis/*clean*"),
    (19, "Annotation, labelling & adjudication", "P3", "partial", "§12"),
    (20, "Temporal alignment & cohort construction", "P3", "done", "make_cohort.py"),
    (21, "Exploratory & statistical analysis", "P4", "done", "analysis/eda.py"),
    (22, "Missing-data & outlier strategy", "P3", "done", "§11 taxonomy"),
    (23, "Encoding, scaling, transformation", "P3", "done", "preprocessing.py"),
    (24, "Feature engineering", "P3", "done", "feature_store.py"),
    (25, "Leakage review", "P3", "done", "§15 subject-level"),
    (26, "Feature validation & registry", "P3", "partial", "§13"),
    (27, "Offline & online feature store", "P3", "partial", "feature_store.py + §14"),
    (28, "Baseline model development", "P4", "done", "§18"),
    (29, "Classical / survival / time-series", "P4", "done", "recurrence, timeseries"),
    (30, "Experiment tracking & HPO", "P4", "done", "experiment_tracker.py"),
    (31, "Internal / temporal / external validation", "P4", "done", "external_validation.csv"),
    (32, "Calibration, fairness, explainability", "P4", "done", "responsible_ai_runtime.py"),
    (33, "Clinical utility & safety validation", "P7", "partial", "§30 safety layer"),
    (34, "Model registry & approval", "P5", "done", "model_registry.py"),
    (35, "Batch / real-time deployment", "P5", "done", "api/main.py"),
    (36, "RAG & agent integration", "P6", "partial", "vector_db_pipeline.py"),
    (37, "Human clinical oversight", "P7", "done", "human-in-the-loop"),
    (38, "Observability, drift, quality monitoring", "P5", "done", "observability.py"),
    (39, "Retraining, recalibration, rollback", "P5", "done", "retrain.py"),
    (40, "Retention, archival, deletion, retirement", "P2", "partial", "§35"),
]

PREDICTION = [
    ("patient_pseudonymous_id", "EP001"),
    ("prediction_timestamp", "2026-07-12T09:14:00-06:00"),
    ("prediction_horizon_days", "90"),
    ("model_name", "epi-recurrence-fusion"),
    ("model_version", "7.2.0"),
    ("feature_set_version", "5.1"),
    ("dataset_version", "3.2"),
    ("predicted_class", "breakthrough_seizure"),
    ("raw_probability", "0.72"),
    ("calibrated_probability", "0.64"),
    ("uncertainty_level", "moderate"),
    ("risk_category", "elevated"),
    ("top_contributing_factors", "line_length_up; asm_adherence_low; sleep_variability_high"),
    ("protective_factors", "stable_asm_regimen"),
    ("missing_critical_information", "recent_ambulatory_EEG"),
    ("out_of_distribution_indicator", "false"),
    ("fairness_warning", "none"),
    ("clinical_guideline_evidence", "ILAE ictal-EEG guidance; ASM-adherence evidence"),
    ("recommended_next_assessment", "neurologist review + repeat EEG within 2 weeks"),
    ("human_review_status", "pending"),
    ("clinician_override_status", "none"),
    ("override_reason", "none"),
    ("audit_id", "aud-2026-07-12-0009"),
]


def main():
    banner("enterprise_flow_export — 7 pipelines / 40 stages / prediction object")
    pd.DataFrame(PIPELINES, columns=["id", "pipeline", "owner", "question", "artefacts"]) \
        .to_csv(os.path.join(DATA_DIR, "enterprise_pipelines.csv"), index=False)
    pd.DataFrame(STAGES, columns=["stage_no", "stage", "pipeline", "status", "evidence"]) \
        .to_csv(os.path.join(DATA_DIR, "enterprise_stages.csv"), index=False)
    pd.DataFrame(PREDICTION, columns=["field", "value"]) \
        .to_csv(os.path.join(DATA_DIR, "prediction_output_example.csv"), index=False)
    done = sum(1 for s in STAGES if s[3] == "done")
    print(f"  pipelines={len(PIPELINES)} stages={len(STAGES)} (done={done}, "
          f"partial={sum(1 for s in STAGES if s[3]=='partial')}, gap={sum(1 for s in STAGES if s[3]=='gap')})")


if __name__ == "__main__":
    main()
