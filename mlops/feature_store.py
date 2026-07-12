"""
feature_store.py — Minimal offline feature store (entity = patient_id)
======================================================================

Materialises engineered features into a governed, versioned offline store with
feature-group METADATA, and serves point-in-time feature vectors to training and
inference — the "feature store" the 23-step flow omitted.

    materialize()            build the offline feature table + metadata from the cohort
    get_features(ids, cols)  serve a feature vector for given patients
    list_features()          the feature catalogue (group, dtype, description)

Store: mlops/store/features.csv + feature_metadata.json
Run: python mlops/feature_store.py
"""
from __future__ import annotations
import os, json
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "analysis")
STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "store")
os.makedirs(STORE, exist_ok=True)

# Feature groups: which columns belong to which owning domain (data-mesh style).
GROUPS = {
    "clinical": ["neuro_seizure_freq_pm", "npsy_gad7", "npsy_moca", "pt_qolie31",
                 "pharm_adherence_pct", "care_zbi_burden"],
    "eeg": ["eeg_temporal_asym", "eeg_spike_rate_pm", "eeg_entropy", "eeg_paf_hz",
            "eeg_connectivity", "eeg_delta", "eeg_theta", "eeg_alpha"],
    "engineered": ["seizure_burden", "mood_load", "qol_deficit", "cognitive_deficit"],
    "target": ["severity_level", "drug_resistant"],
}


def materialize() -> pd.DataFrame:
    """Join the cohort + EEG + engineered features into one offline feature table."""
    prim = pd.read_csv(os.path.join(DATA, "primary_clean_features.csv"))
    eeg = pd.read_csv(os.path.join(DATA, "cohort_eeg.csv"))
    df = prim.merge(eeg, on="patient_id", how="left")
    cols = ["patient_id"] + [c for g in GROUPS.values() for c in g if c in df.columns]
    table = df[cols].drop_duplicates("patient_id")
    table.to_csv(os.path.join(STORE, "features.csv"), index=False)

    meta = []
    for group, feats in GROUPS.items():
        for f in feats:
            if f in table.columns:
                meta.append({"feature": f, "group": group,
                             "dtype": str(table[f].dtype),
                             "entity": "patient_id"})
    json.dump({"features": meta, "n_entities": int(len(table))},
              open(os.path.join(STORE, "feature_metadata.json"), "w"), indent=2)
    return table


def _load():
    p = os.path.join(STORE, "features.csv")
    if not os.path.exists(p):
        materialize()
    return pd.read_csv(p)


def get_features(entity_ids, cols=None) -> pd.DataFrame:
    """Serve a feature vector for the given patient ids (offline retrieval)."""
    t = _load()
    t = t[t["patient_id"].isin(entity_ids)]
    if cols:
        t = t[["patient_id"] + [c for c in cols if c in t.columns]]
    return t.reset_index(drop=True)


def list_features() -> pd.DataFrame:
    meta = json.load(open(os.path.join(STORE, "feature_metadata.json")))
    return pd.DataFrame(meta["features"])


def main():
    t = materialize()
    print(f"feature store materialised: {t.shape[0]} entities x {t.shape[1]-1} features")
    print("EP001 vector:", get_features(["EP001"], ["neuro_seizure_freq_pm", "eeg_temporal_asym"]).to_dict("records"))


if __name__ == "__main__":
    main()
