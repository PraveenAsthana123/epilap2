"""
experiment_tracker.py — Lightweight experiment tracking (params + metrics + lineage)
====================================================================================

Logs every training run (parameters, metrics, dataset version, timestamp) to an
append-only store so runs are comparable and reproducible — the experiment-tracking
capability the 23-step flow omitted. A dependency-free stand-in for MLflow/W&B.

    log_run(experiment, params, metrics, tags)   append a run, returns run_id
    list_runs(experiment)                          all runs (optionally filtered)
    best_run(metric, experiment, maximize)         the winning run

Store: mlops/store/experiments.jsonl
"""
from __future__ import annotations
import os, json, time, uuid
import pandas as pd

STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "store")
os.makedirs(STORE, exist_ok=True)
LOG = os.path.join(STORE, "experiments.jsonl")


def log_run(experiment: str, params: dict, metrics: dict, tags: dict | None = None) -> str:
    run_id = uuid.uuid4().hex[:12]
    rec = {"run_id": run_id, "experiment": experiment, "ts": time.time(),
           "params": params, "metrics": metrics, "tags": tags or {}}
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return run_id


def list_runs(experiment: str | None = None) -> pd.DataFrame:
    if not os.path.exists(LOG):
        return pd.DataFrame()
    rows = [json.loads(l) for l in open(LOG, encoding="utf-8") if l.strip()]
    if experiment:
        rows = [r for r in rows if r["experiment"] == experiment]
    flat = [{"run_id": r["run_id"], "experiment": r["experiment"],
             **{f"p.{k}": v for k, v in r["params"].items()},
             **{f"m.{k}": v for k, v in r["metrics"].items()}} for r in rows]
    return pd.DataFrame(flat)


def best_run(metric: str, experiment: str | None = None, maximize: bool = True):
    df = list_runs(experiment)
    col = f"m.{metric}"
    if df.empty or col not in df:
        return None
    idx = df[col].idxmax() if maximize else df[col].idxmin()
    return df.loc[idx].to_dict()
