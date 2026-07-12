# Observability & Monitoring Report

> **Why (this doc):** Continuous monitoring of model and data health — performance, prediction
> distribution/confidence, data drift (KS), concept drift, and data quality — the observability
> layer the checklist requires. **How:** `mlops/observability.py`; in production this runs on a
> schedule and alerts on breaches.

## Model performance (holdout)
accuracy 0.84 · precision 0.827 · recall 0.741 · F1 0.782

## Prediction monitoring
predicted-positive rate 0.347 · mean confidence 0.762 ·
class distribution actual [92, 58] vs predicted [98, 52]

## Data drift (Kolmogorov-Smirnov, reference vs current window)
| feature | ks_stat | p | drift |
|---|---|---|---|
| neuro_seizure_freq_pm | 0.0 | 1.0 | stable |
| npsy_gad7 | 0.0 | 1.0 | stable |
| pt_qolie31 | 0.33 | <0.001 | DRIFT |
| pharm_adherence_pct | 0.0 | 1.0 | stable |
| npsy_moca | 0.0 | 1.0 | stable |
| age | 0.35 | <0.001 | DRIFT |

_(The two simulated-drift features (age, pt_qolie31) are correctly flagged DRIFT; unshifted features stay stable — the detector works.)_

## Concept drift (feature<->target relation change)
| feature | corr_window1 | corr_window2 | relation_drift | flag |
|---|---|---|---|---|
| neuro_seizure_freq_pm | 0.481 | 0.391 | 0.089 | ok |
| npsy_gad7 | 0.433 | 0.538 | 0.106 | ok |
| pt_qolie31 | -0.524 | -0.492 | 0.032 | ok |
| pharm_adherence_pct | -0.226 | 0.026 | 0.252 | review |
| npsy_moca | -0.406 | -0.51 | 0.104 | ok |
| age | 0.027 | 0.063 | 0.036 | ok |

## Data quality
rows 500 · duplicate rows 0 · overall null% 0.38 ·
contract violations 4 ['age: 3 value(s) outside [0,120]', 'pt_qolie31: 9 null(s) but required', 'pharm_adherence_pct: 19 null(s) but required', 'pharm_adherence_pct: 2 value(s) outside [0,100]']

**Alerting policy:** any KS drift p<0.05, relation-drift>0.15, calibration decay, or contract
violation raises a monitoring alert routed to the ML/clinical owner (human override retained).
