"""
model_registry.py — Model registry with versioning, promotion & ROLLBACK
=========================================================================

Registers trained models with immutable versions + metadata, tracks which version
is in "production", and supports promotion and ROLLBACK to a previous version — the
model-rollback / registry capability the 23-step flow omitted.

    register(name, model, metrics, params)  -> new version number (saved via joblib)
    promote(name, version)                   set the production pointer
    rollback(name)                           revert production to the previous version
    production_version(name)                 current production version
    load(name, version=None)                 load a version (default: production)

Store: mlops/store/models/<name>/v<N>.joblib + registry.json
"""
from __future__ import annotations
import os, json, time
import joblib

STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "store", "models")
os.makedirs(STORE, exist_ok=True)
REG = os.path.join(STORE, "registry.json")


def _load_reg() -> dict:
    return json.load(open(REG)) if os.path.exists(REG) else {}


def _save_reg(reg: dict):
    json.dump(reg, open(REG, "w"), indent=2)


def register(name: str, model, metrics: dict, params: dict | None = None) -> int:
    reg = _load_reg()
    entry = reg.setdefault(name, {"versions": [], "production": None, "history": []})
    version = (max([v["version"] for v in entry["versions"]], default=0) + 1)
    d = os.path.join(STORE, name)
    os.makedirs(d, exist_ok=True)
    joblib.dump(model, os.path.join(d, f"v{version}.joblib"))
    entry["versions"].append({"version": version, "metrics": metrics,
                              "params": params or {}, "ts": time.time()})
    _save_reg(reg)
    return version


def promote(name: str, version: int):
    reg = _load_reg()
    e = reg[name]
    assert any(v["version"] == version for v in e["versions"]), f"no version {version}"
    e["history"].append({"from": e["production"], "to": version, "ts": time.time(), "action": "promote"})
    e["production"] = version
    _save_reg(reg)


def rollback(name: str) -> int | None:
    """Revert production to the previous production version in history."""
    reg = _load_reg()
    e = reg[name]
    prev = None
    for h in reversed(e["history"]):
        if h["action"] in ("promote", "rollback") and h["from"] is not None and h["from"] != e["production"]:
            prev = h["from"]
            break
    if prev is None:
        # Fall back to the highest version below current.
        vers = sorted(v["version"] for v in e["versions"])
        below = [v for v in vers if v < (e["production"] or 0)]
        prev = below[-1] if below else None
    if prev is None:
        return None
    e["history"].append({"from": e["production"], "to": prev, "ts": time.time(), "action": "rollback"})
    e["production"] = prev
    _save_reg(reg)
    return prev


def production_version(name: str):
    return _load_reg().get(name, {}).get("production")


def load(name: str, version: int | None = None):
    v = version or production_version(name)
    if v is None:
        raise ValueError(f"no production version for {name}")
    return joblib.load(os.path.join(STORE, name, f"v{v}.joblib"))
