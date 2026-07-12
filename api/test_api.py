"""
test_api.py — Positive + negative API tests (FastAPI TestClient)
================================================================
Run:  cd api && python -m pytest -q   (requires the DB + CSVs to exist)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fastapi.testclient import TestClient
from main import app

c = TestClient(app)


def test_health():
    assert c.get("/health").json()["status"] == "ok"


def test_roles_weights_sum_to_one():
    assert abs(c.get("/roles").json()["total_weight"] - 1.0) < 1e-6   # positive


def test_scenarios_count():
    assert c.get("/scenarios").json()["count"] >= 50                  # positive


def test_scenario_lookup_and_404():
    assert c.get("/scenarios/SZ-F02").json()["scenario"].startswith("Focal")  # positive
    assert c.get("/scenarios/DOES-NOT-EXIST").status_code == 404              # negative


def test_score_weighted_band():
    r = c.post("/score", json={"role": "neurologist", "sections": [
        {"items": [{"level": 3, "weight": 1.0}, {"level": 4, "weight": 1.2}]}]})
    assert r.status_code == 200
    assert r.json()["role_band"]["label"] in ("Severe", "Refractory/Status")  # positive


def test_score_rejects_bad_level():
    # NEGATIVE: level outside 1-4 must be a 422 validation error.
    assert c.post("/score", json={"sections": [{"items": [{"level": 9}]}]}).status_code == 422


def test_patient_ep001_and_missing():
    assert c.get("/patient/EP001").json()["band"]["label"] == "Severe"   # positive
    assert c.get("/patient/NOPE").status_code == 404                     # negative


def test_api_key_enforced_when_set(monkeypatch):
    # With EPI_API_KEY set, protected endpoints require the header.
    monkeypatch.setenv("EPI_API_KEY", "secret123")
    body = {"sections": [{"items": [{"level": 3, "weight": 1.0}]}]}
    assert c.post("/score", json=body).status_code == 401                        # negative: missing key
    assert c.post("/score", json=body, headers={"X-API-Key": "wrong"}).status_code == 401
    assert c.post("/score", json=body, headers={"X-API-Key": "secret123"}).status_code == 200  # positive
    # Open (no key configured) still works for dev.
    monkeypatch.delenv("EPI_API_KEY", raising=False)
    assert c.post("/score", json=body).status_code == 200
