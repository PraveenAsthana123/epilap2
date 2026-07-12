"""
build_sqlite.py — Materialise a runnable SQLite database from the repo artefacts
================================================================================

Creates db/epilepsy.db with a SQLite-compatible version of schema.sql and loads:
  * the 4-level severity ladder
  * the 9 roles + their domain weights (from data/analysis/domain_weightage.csv)
  * the 57-scenario catalogue (from data/analysis/epilepsy_scenarios.csv)
  * patient EP001

This gives a real, queryable database for the API and for demos, reproducible from
`python db/build_sqlite.py`.
"""
from __future__ import annotations
import os, sqlite3, csv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "analysis")
DB = os.path.join(HERE, "epilepsy.db")

ROLE_META = [  # code, name, prefix (order matches the platform)
    ("neurologist", "Neurologist", "NEU"), ("eeg-technician", "EEG Technician", "EEG"),
    ("nurse", "Nurse", "NUR"), ("neuropsychologist", "Neuropsychologist", "NPS"),
    ("pharmacist", "Pharmacist", "PHA"), ("caregiver", "Caregiver", "CAR"),
    ("patient", "Patient", "PAT"), ("administrator", "Administrator", "ADM"),
    ("occupational-therapist", "Occupational Therapist", "OT"),
]

DDL = """
CREATE TABLE severity_level(level INTEGER PRIMARY KEY, name TEXT, description TEXT);
CREATE TABLE role(role_id INTEGER PRIMARY KEY, code TEXT UNIQUE, name TEXT, id_prefix TEXT, domain_weight REAL);
CREATE TABLE scenario(scenario_id TEXT PRIMARY KEY, category TEXT, name TEXT, onset TEXT, awareness TEXT,
    ilae_class TEXT, severity_level INTEGER, clinical_weight REAL, key_features TEXT);
CREATE TABLE patient(patient_id TEXT PRIMARY KEY, study_id TEXT, age INTEGER, sex TEXT, focus_side TEXT);
CREATE TABLE patient_score(id INTEGER PRIMARY KEY, patient_id TEXT, composite_score REAL, band INTEGER);
"""


def main() -> None:
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.executescript(DDL)

    con.executemany("INSERT INTO severity_level VALUES (?,?,?)", [
        (1, "Mild", "Well-controlled"), (2, "Moderate", "Intermediate"),
        (3, "Severe", "Poorly controlled (EP001)"), (4, "Refractory/Status", "Emergency")])

    # roles + domain weights
    weights = {r[0]: float(r[1]) for r in _csv(os.path.join(DATA, "domain_weightage.csv"))[1:]}
    for i, (code, name, prefix) in enumerate(ROLE_META, 1):
        w = weights.get(name, 0.0)
        con.execute("INSERT INTO role VALUES (?,?,?,?,?)", (i, code, name, prefix, w))

    # scenarios
    rows = _csv(os.path.join(DATA, "epilepsy_scenarios.csv"))[1:]
    con.executemany("INSERT INTO scenario VALUES (?,?,?,?,?,?,?,?,?)", rows)

    # EP001
    con.execute("INSERT INTO patient VALUES (?,?,?,?,?)", ("EP001", "DBA-EP-001", 29, "M", "Left"))
    con.execute("INSERT INTO patient_score VALUES (?,?,?,?)", (1, "EP001", 3.0, 3))
    con.commit()

    n_sc = con.execute("SELECT count(*) FROM scenario").fetchone()[0]
    n_role = con.execute("SELECT count(*) FROM role").fetchone()[0]
    print(f"built {DB}  roles={n_role} scenarios={n_sc}")
    con.close()


def _csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.reader(f))


if __name__ == "__main__":
    main()
