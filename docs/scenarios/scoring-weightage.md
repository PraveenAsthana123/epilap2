# Questionnaire Weightage & Scoring Model

> **Why (this doc):** Turns a filled role questionnaire into a weighted patient severity score, so the form is not just data capture but a graded assessment. **How:** each item maps to a severity level (1-4) via the section's Severity Scenario Model; items are weighted, averaged per role, then combined across roles by domain weight.

## Item-level scoring

*Caption - Each questionnaire item scores 1-4 by the answer's severity level; item weight scales its contribution.*

| Step | Rule |
|---|---|
| 1 | Map each answered item to its severity level L (1=Mild … 4=Refractory/Status) |
| 2 | Item weight w = clinical_weight of the matching scenario (default 1.0) |
| 3 | Section score = Σ(L·w) / Σ(w) over answered items |
| 4 | Role score = mean of that role's section scores |
| 5 | Patient composite = Σ(role_score · domain_weight) |
| 6 | Band: <1.75 Mild · <2.5 Moderate · <3.25 Severe · else Refractory/Status |

## Domain weightage

*Caption - Relative weight of each role in the composite patient severity score (sums to 1.0).*

| Domain | Weight | Rationale |
|---|---|---|
| Neurologist | 0.22 | Seizure classification, burden, diagnosis — primary driver |
| EEG Technician | 0.1 | Objective electrophysiology / focus evidence |
| Neuropsychologist | 0.12 | Cognitive & mood comorbidity load |
| Pharmacist | 0.12 | Regimen complexity, drug resistance, levels |
| Nurse | 0.1 | Observed events, vitals, acute safety |
| Caregiver | 0.1 | Witnessed burden, home management |
| Patient | 0.12 | Patient-reported outcomes, QoL, adherence |
| Occupational Therapist | 0.08 | Functional independence, participation, safety |
| Administrator | 0.04 | Encounter acuity / utilisation signal |

**Total:** 1.00. EP001 → domain scores skew to Severe (Level 3), composite ≈ Severe. Source CSVs: `data/analysis/domain_weightage.csv`, `data/analysis/epilepsy_scenarios.csv`.
