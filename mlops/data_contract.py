"""
data_contract.py — Data contract for the primary cohort (schema + quality guarantees)
=====================================================================================

A data contract is the enforceable agreement between the data PRODUCER (make_cohort)
and CONSUMERS (analytics, models, feature store): expected columns, types, ranges, and
required/nullability. Validating against it BEFORE downstream use is the data-engineering
control the 23-step flow omitted.

Run: python mlops/data_contract.py   (validates data/analysis/cohort_primary.csv)
"""
from __future__ import annotations
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Contract: column -> constraints. `req`=required (no nulls), range = (min,max) for numeric,
# allowed = permitted categorical values.
CONTRACT = {
    "patient_id": {"dtype": "str", "req": True},
    "age": {"dtype": "int", "req": True, "range": (0, 120)},
    "sex": {"dtype": "str", "req": True, "allowed": ["M", "F", "Intersex"]},
    "neuro_seizure_freq_pm": {"dtype": "float", "req": True, "range": (0, 300)},
    "npsy_gad7": {"dtype": "int", "req": True, "range": (0, 21)},
    "pt_qolie31": {"dtype": "int", "req": True, "range": (0, 100)},
    "pharm_adherence_pct": {"dtype": "int", "req": True, "range": (0, 100)},
    "severity_level": {"dtype": "int", "req": True, "allowed": [1, 2, 3, 4]},
    "drug_resistant": {"dtype": "int", "req": True, "allowed": [0, 1]},
}


def validate(df: pd.DataFrame) -> list[str]:
    """Return a list of contract violations (empty list = the data passes the contract)."""
    v = []
    for col, c in CONTRACT.items():
        if col not in df.columns:
            v.append(f"missing column: {col}")
            continue
        s = df[col]
        if c.get("req") and s.isna().any():
            v.append(f"{col}: {int(s.isna().sum())} null(s) but required")
        if "range" in c:
            lo, hi = c["range"]
            bad = pd.to_numeric(s, errors="coerce")
            n = int(((bad < lo) | (bad > hi)).sum())
            if n:
                v.append(f"{col}: {n} value(s) outside [{lo},{hi}]")
        if "allowed" in c:
            n = int((~s.isin(c["allowed"])).sum())
            if n:
                v.append(f"{col}: {n} value(s) not in {c['allowed']}")
    return v


def main():
    df = pd.read_csv(os.path.join(ROOT, "data", "analysis", "cohort_primary.csv"))
    viol = validate(df)
    print(f"contract check on cohort_primary.csv ({len(df)} rows): "
          + ("PASS" if not viol else f"{len(viol)} VIOLATION(S)"))
    for x in viol:
        print("  -", x)
    return viol


if __name__ == "__main__":
    main()
