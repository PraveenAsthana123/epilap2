"""
retrain.py — Champion-challenger retraining loop (continuous learning)
=====================================================================

Closes the retraining phase: trains a CHALLENGER, compares it to the current
CHAMPION (production) on a fresh holdout, and promotes the challenger only if it
wins by a margin — otherwise keeps the champion. Logs the decision as feedback +
audit. This is the continuous-learning control the lifecycle was missing.

Writes: mlops/store/challenger.json (+ registry update if promoted)
Run: python mlops/retrain.py
"""
from __future__ import annotations
import os, sys, json
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "analysis")
STORE = os.path.join(HERE, "store")
sys.path.insert(0, HERE)
import model_registry as mr, logging_setup as ls

NAME = "drug_resistance_pipeline"
MARGIN = 0.005
FEATS = ["neuro_seizure_freq_pm", "npsy_gad7", "pt_qolie31", "pharm_adherence_pct", "npsy_moca",
         "care_zbi_burden", "neuro_trigger_burden"]


def main():
    df = pd.read_csv(os.path.join(DATA, "primary_clean_features.csv"))
    X = df[FEATS].fillna(df[FEATS].median()); y = df["drug_resistant"].values
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=7, stratify=y)

    # Champion = current production pipeline (if any).
    champ_auc = None
    try:
        champ = mr.load(NAME)
        champ_auc = round(float(roc_auc_score(yte, champ.predict_proba(Xte)[:, 1])), 4)
    except Exception:
        champ = None

    # Challenger: a gradient-boosting pipeline.
    challenger = Pipeline([("scaler", StandardScaler()),
                           ("model", GradientBoostingClassifier(random_state=7))]).fit(Xtr, ytr)
    chall_auc = round(float(roc_auc_score(yte, challenger.predict_proba(Xte)[:, 1])), 4)

    promote = champ_auc is None or chall_auc > champ_auc + MARGIN
    decision = {"champion_auc": champ_auc, "challenger_auc": chall_auc,
                "margin": MARGIN, "promoted": promote}
    if promote:
        v = mr.register(NAME, challenger, {"auc": chall_auc}, {"model": "gbm_challenger"})
        mr.promote(NAME, v)
        decision["new_production_version"] = v
    json.dump(decision, open(os.path.join(STORE, "challenger.json"), "w"), indent=2)

    ls.log_feedback("retrain", {"champion_auc": champ_auc, "challenger_auc": chall_auc,
                                "promoted": promote})
    ls.log_audit("mlops", "retrain-decision", NAME, decision)
    print(f"champion_auc={champ_auc} challenger_auc={chall_auc} -> "
          + ("PROMOTED challenger" if promote else "KEPT champion"))


if __name__ == "__main__":
    main()
