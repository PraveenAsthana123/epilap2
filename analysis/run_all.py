"""
run_all.py — One-command reproduction of the ENTIRE analytics deliverable
=========================================================================

Runs every pipeline in dependency order so a reviewer can regenerate all datasets,
figures, reports, and governance artefacts from a clean checkout. Grouped into the
data layer, the flagship analyses, the governance gates, the integrated engine, and
the catalogue/reference generators.

Usage:  python analysis/run_all.py
"""
from __future__ import annotations
from common import banner

# Each import is a self-contained, commented pipeline module (see its docstring).
import make_cohort            # synthetic linked cohort (primary + EEG)
import primary_analysis       # flagship 1/3: classification + drug-resistance
import secondary_analysis     # flagship 2/7: EEG QC + focus lateralisation
import fusion_analysis        # flagship 6: multimodal fusion + EP001 case
import governance             # C5 confidence/abstention + C6 concordance
import recurrence             # flagship 4: seizure recurrence survival
import decision_support       # flagship 6 (integrated): governed CDSS
import responsible_ai_runtime # explainability + fairness + guardrails (runtime)
import build_scenarios        # seizure/epilepsy scenario DB + weighting
import build_var_dictionary   # DV/IV/covariate dictionary + hypotheses
import build_questionnaires   # validate + consolidate the 10-role questionnaires
import build_catalogues       # pain-point register + visualization catalogue
import secondary_eeg_full      # full 23-phase EEG pipeline on real CHB-MIT (STFT/CWT/2D/SMOTE/HPO)
import phase_io_export         # per-phase input/process/output + governance (viewer Phase Explorer)
import vector_db_pipeline      # RAG vector DB (embed->index->retrieve) + scheduled jobs
import enterprise_flow_export  # 7-pipeline / 40-stage operating model + prediction-object CSVs
import knowledge_graph_export   # epilepsy RDF knowledge graph (Turtle) + node/edge CSVs


STAGES = [
    ("Data — cohort", make_cohort),
    ("Flagship — primary (classification/drug-resistance)", primary_analysis),
    ("Flagship — secondary EEG", secondary_analysis),
    ("Flagship — multimodal fusion", fusion_analysis),
    ("Governance — confidence (C5) + concordance (C6)", governance),
    ("Flagship — recurrence survival", recurrence),
    ("Integrated — multimodal decision support", decision_support),
    ("Runtime RAI — SHAP/LIME/fairness/guardrails", responsible_ai_runtime),
    ("Reference — scenario database", build_scenarios),
    ("Reference — variable dictionary + hypotheses", build_var_dictionary),
    ("Reference — questionnaire validation", build_questionnaires),
    ("Reference — pain + visualization catalogues", build_catalogues),
    ("Secondary — full 23-phase EEG (real CHB-MIT)", secondary_eeg_full),
    ("Phase Explorer — per-phase input/process/output export", phase_io_export),
    ("RAG — vector DB pipeline + scheduled jobs", vector_db_pipeline),
    ("Operating model — 7 pipelines / 40 stages / prediction object", enterprise_flow_export),
    ("Knowledge graph — epilepsy RDF/Turtle + node/edge CSVs", knowledge_graph_export),
]


def main() -> None:
    banner("RUN ALL — full epilepsy Responsible-AI analytics deliverable")
    for title, module in STAGES:
        banner(title)
        module.main()
    banner("DONE — see docs/analysis/*.md, docs/**, and analysis/outputs/")


if __name__ == "__main__":
    main()
