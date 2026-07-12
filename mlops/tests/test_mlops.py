"""Tests for the MLOps layer: data contract, feature store, experiment tracker, registry+rollback."""
import os, sys
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

HERE = os.path.dirname(os.path.abspath(__file__))
MLOPS = os.path.dirname(HERE)
ROOT = os.path.dirname(MLOPS)
sys.path.insert(0, MLOPS)
import data_contract, feature_store, experiment_tracker as et, model_registry as mr


# ---- data contract ----
def test_contract_passes_clean_data():
    df = pd.DataFrame({"patient_id": ["EP001"], "age": [29], "sex": ["M"],
                       "neuro_seizure_freq_pm": [5.0], "npsy_gad7": [9], "pt_qolie31": [55],
                       "pharm_adherence_pct": [88], "severity_level": [3], "drug_resistant": [1]})
    assert data_contract.validate(df) == []                       # positive


def test_contract_catches_violations():
    df = pd.DataFrame({"patient_id": ["X"], "age": [500], "sex": ["Z"],
                       "neuro_seizure_freq_pm": [5.0], "npsy_gad7": [9], "pt_qolie31": [55],
                       "pharm_adherence_pct": [88], "severity_level": [9], "drug_resistant": [1]})
    v = data_contract.validate(df)
    assert any("age" in x for x in v)                             # negative: bad age
    assert any("sex" in x for x in v)                            # bad category
    assert any("severity_level" in x for x in v)                 # bad level


# ---- feature store ----
def test_feature_store_serves_ep001():
    feature_store.materialize()
    fv = feature_store.get_features(["EP001"], ["neuro_seizure_freq_pm"])
    assert len(fv) == 1 and fv.iloc[0]["patient_id"] == "EP001"   # positive
    assert feature_store.get_features(["NOPE"]).empty             # negative


# ---- experiment tracker ----
def test_experiment_tracker_logs_and_ranks():
    exp = "unit_test_exp"
    et.log_run(exp, {"model": "a"}, {"auc": 0.80})
    et.log_run(exp, {"model": "b"}, {"auc": 0.90})
    best = et.best_run("auc", exp, maximize=True)
    assert best["p.model"] == "b"                                 # positive
    assert best["m.auc"] == 0.90


# ---- model registry + rollback ----
def test_registry_register_promote_rollback():
    name = "unit_test_model"
    v1 = mr.register(name, LogisticRegression(), {"auc": 0.90})
    mr.promote(name, v1)
    v2 = mr.register(name, RandomForestClassifier(n_estimators=5), {"auc": 0.95})
    mr.promote(name, v2)
    assert mr.production_version(name) == v2                      # positive: promoted
    prev = mr.rollback(name)
    assert prev == v1                                            # negative-path: rolled back
    assert mr.production_version(name) == v1
    assert type(mr.load(name)).__name__ == "LogisticRegression"  # loads the rolled-back model
