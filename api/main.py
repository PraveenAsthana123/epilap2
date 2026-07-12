"""
main.py — Epilepsy Intelligence Platform API (FastAPI)
======================================================

A thin, runnable REST API over the platform's artefacts: roles, the seizure/epilepsy
scenario catalogue, and the weighted severity SCORING model. It is deliberately
stateless and file/DB-backed so it runs from a clean checkout.

Endpoints
    GET  /health                     liveness
    GET  /roles                      the 9 roles + domain weights
    GET  /scenarios                  full scenario catalogue (optional ?category=)
    GET  /scenarios/{scenario_id}    one scenario
    GET  /severity                   the 4-level ladder
    POST /score                      weighted severity score from submitted answers
    GET  /patient/{patient_id}       patient + stored composite (from SQLite)

Run:  cd api && pip install -r requirements.txt && uvicorn main:app --reload
Docs: http://127.0.0.1:8000/docs  (auto OpenAPI/Swagger)
"""
from __future__ import annotations
import os, csv, sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "analysis")
DB = os.path.join(ROOT, "db", "epilepsy.db")

app = FastAPI(title="Epilepsy Intelligence Platform API", version="1.0.0",
              description="Roles, seizure/epilepsy scenarios, and weighted severity scoring.")


# --------------------------------------------------------------------------- helpers
def _read_csv(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _band(mean: Optional[float]) -> dict:
    """Map a mean severity score (1..4) to its band — identical to the viewer + docs."""
    if mean is None:
        return {"level": 0, "label": "—"}
    if mean < 1.75:
        return {"level": 1, "label": "Mild"}
    if mean < 2.5:
        return {"level": 2, "label": "Moderate"}
    if mean < 3.25:
        return {"level": 3, "label": "Severe"}
    return {"level": 4, "label": "Refractory/Status"}


# --------------------------------------------------------------------------- models
class Item(BaseModel):
    level: int = Field(..., ge=1, le=4, description="Answer's severity level 1-4")
    weight: float = Field(1.0, gt=0, description="Item clinical weight")


class Section(BaseModel):
    name: Optional[str] = None
    items: list[Item]


class ScoreRequest(BaseModel):
    role: Optional[str] = None
    sections: list[Section]


# --------------------------------------------------------------------------- endpoints
@app.get("/health")
def health():
    return {"status": "ok", "service": "epilepsy-platform-api"}


@app.get("/roles")
def roles():
    """The 9 roles and their composite-score domain weights."""
    try:
        rows = _read_csv(os.path.join(DATA, "domain_weightage.csv"))
    except FileNotFoundError:
        raise HTTPException(500, "domain_weightage.csv missing — run analysis/build_scenarios.py")
    return {"roles": rows, "total_weight": round(sum(float(r["weight"]) for r in rows), 3)}


@app.get("/severity")
def severity():
    return {"levels": [
        {"level": 1, "name": "Mild"}, {"level": 2, "name": "Moderate"},
        {"level": 3, "name": "Severe (EP001)"}, {"level": 4, "name": "Refractory/Status"}]}


@app.get("/scenarios")
def scenarios(category: Optional[str] = None):
    """Full seizure/epilepsy scenario catalogue; filter with ?category=."""
    rows = _read_csv(os.path.join(DATA, "epilepsy_scenarios.csv"))
    if category:
        rows = [r for r in rows if r["category"].lower() == category.lower()]
    return {"count": len(rows), "scenarios": rows}


@app.get("/scenarios/{scenario_id}")
def scenario(scenario_id: str):
    rows = _read_csv(os.path.join(DATA, "epilepsy_scenarios.csv"))
    for r in rows:
        if r["id"].lower() == scenario_id.lower():
            return r
    raise HTTPException(404, f"scenario {scenario_id} not found")


@app.post("/score")
def score(req: ScoreRequest):
    """Weighted severity score: item -> section (Σ L·w / Σ w) -> role (mean of sections) -> band."""
    section_scores = []
    for sec in req.sections:
        num = sum(it.level * it.weight for it in sec.items)
        den = sum(it.weight for it in sec.items)
        s = round(num / den, 3) if den else None
        section_scores.append({"name": sec.name, "score": s, "band": _band(s)})
    means = [s["score"] for s in section_scores if s["score"] is not None]
    role_mean = round(sum(means) / len(means), 3) if means else None
    return {"role": req.role, "sections": section_scores,
            "role_score": role_mean, "role_band": _band(role_mean)}


@app.get("/patient/{patient_id}")
def patient(patient_id: str):
    """Patient record + stored composite severity (from the SQLite DB)."""
    if not os.path.exists(DB):
        raise HTTPException(500, "epilepsy.db missing — run db/build_sqlite.py")
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    p = con.execute("SELECT * FROM patient WHERE patient_id=?", (patient_id,)).fetchone()
    if not p:
        con.close()
        raise HTTPException(404, f"patient {patient_id} not found")
    ps = con.execute("SELECT composite_score, band FROM patient_score WHERE patient_id=?",
                     (patient_id,)).fetchone()
    con.close()
    out = dict(p)
    if ps:
        out["composite_score"] = ps["composite_score"]
        out["band"] = _band(ps["composite_score"])
    return out
