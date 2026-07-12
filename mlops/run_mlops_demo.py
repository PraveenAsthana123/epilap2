"""
run_mlops_demo.py — End-to-end MLOps demo tying the data-engineering layer together
===================================================================================

Demonstrates the full MLOps loop the 23-step flow omitted:
  1. DATA CONTRACT   validate the cohort before use
  2. FEATURE STORE   materialise + serve features
  3. TRAIN + TRACK   train two model versions, log experiments
  4. REGISTRY        register both, promote the best
  5. ROLLBACK        roll production back to the previous version

Run: python mlops/run_mlops_demo.py   (needs primary_analysis + cohort artefacts)
"""
from __future__ import annotations
import os, sys
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import data_contract, feature_store, experiment_tracker as et, model_registry as mr

TARGET = "drug_resistant"


def main():
    print("=" * 70, "\nMLOps demo — contract -> feature store -> track -> registry -> rollback\n", "=" * 70)

    # 1. Data contract
    df0 = pd.read_csv(os.path.join(ROOT, "data", "analysis", "cohort_primary.csv"))
    viol = data_contract.validate(df0)
    print(f"1. DATA CONTRACT: {'PASS' if not viol else viol}")

    # 2. Feature store
    feature_store.materialize()
    feats = feature_store.list_features()
    num_feats = [f for f in feats["feature"] if f not in ("severity_level", "drug_resistant")]
    store = feature_store.get_features(df0["patient_id"].tolist(), num_feats)
    data = store.merge(df0[["patient_id", TARGET]], on="patient_id").dropna()
    X, y = data[[c for c in num_feats if c in data]].values, data[TARGET].values
    print(f"2. FEATURE STORE: {X.shape[1]} features x {X.shape[0]} entities")

    # 3. Train two versions + track experiments
    models = {"logreg_v1": LogisticRegression(max_iter=1000, random_state=42),
              "rf_v2": RandomForestClassifier(n_estimators=300, random_state=42)}
    trained = {}
    for name, clf in models.items():
        auc = float(cross_val_score(clf, X, y, cv=5, scoring="roc_auc").mean())
        clf.fit(X, y)
        trained[name] = (clf, auc)
        et.log_run("drug_resistance", {"model": name}, {"auc": round(auc, 4)}, {"stage": "demo"})
        print(f"3. TRACK: {name} auc={auc:.3f}")
    best = et.best_run("auc", "drug_resistance", maximize=True)
    print(f"   best run: {best['p.model']} (auc {best['m.auc']})")

    # 4. Register both, promote v1 then the best
    v_lr = mr.register("drug_resistance", trained["logreg_v1"][0],
                       {"auc": round(trained["logreg_v1"][1], 4)}, {"model": "logreg"})
    mr.promote("drug_resistance", v_lr)
    v_rf = mr.register("drug_resistance", trained["rf_v2"][0],
                       {"auc": round(trained["rf_v2"][1], 4)}, {"model": "rf"})
    mr.promote("drug_resistance", v_rf)
    print(f"4. REGISTRY: registered v{v_lr}(logreg) + v{v_rf}(rf); production=v{mr.production_version('drug_resistance')}")

    # 5. Rollback production to the previous version
    prev = mr.rollback("drug_resistance")
    print(f"5. ROLLBACK: production rolled back to v{prev} (now {mr.production_version('drug_resistance')})")
    print("   loaded production model:", type(mr.load('drug_resistance')).__name__)


if __name__ == "__main__":
    main()
