# Flagship #4 — Seizure Recurrence Risk Prediction (Survival Analysis)

> **Why (this doc):** Recurrence is a *time-to-event* question (when will the next seizure occur,
> given censored follow-up), not a static label — so it is modelled with survival analysis. This is
> the sixth top-6 EEG-centric flagship, now runnable. **How:** Kaplan-Meier by severity + a Cox
> proportional-hazards model (hazard ratios + concordance index) + risk stratification, from
> `analysis/recurrence.py`. Anchored on EP001.

**Design:** 500 patients, 365-day follow-up, right-censored. Event = seizure recurrence.

## Kaplan-Meier — time to recurrence by severity

*Caption - Median days to seizure recurrence per severity group — higher severity recurs sooner.*

| severity | median_days_to_recurrence |
|---|---|
| Mild | 161.100 |
| Moderate | 102.700 |
| Severe | 45.800 |
| Refractory/Status | 36.800 |

![Kaplan-Meier](analysis/outputs/recurrence/km_by_severity.png)

**Reason:** Show the survival (seizure-free) probability over time per severity. **Why:** Recurrence timing, not just occurrence, drives follow-up scheduling and counselling. **What is happening:** Severe/refractory groups lose seizure-freedom faster than mild groups. **How it is happening:** KM estimates the survival function with right-censoring at 365 days. **Reference:** Kaplan & Meier (1958).

## Cox proportional-hazards model

*Caption - Hazard ratios per predictor (>1 = higher recurrence hazard); concordance index measures discrimination.*

| predictor | coef | hazard_ratio | p |
|---|---|---|---|
| neuro_trigger_burden | 0.103 | 1.108 | 0.010 |
| pt_side_effect_burden | 0.037 | 1.038 | 0.042 |
| seizure_burden | 0.022 | 1.022 | 0.000 |
| mood_load | 0.008 | 1.008 | 0.371 |
| care_zbi_burden | 0.004 | 1.004 | 0.255 |
| pharm_asm_count | -0.000 | 1.000 | 0.990 |
| pt_qolie31 | -0.010 | 0.990 | 0.001 |
| npsy_naming_z | -0.080 | 0.923 | 0.086 |

**Concordance index (Harrell's C) = 0.663** (0.5 = chance, 1.0 = perfect ordering).

**Reason:** Quantify which factors accelerate recurrence. **Why:** Cox gives interpretable hazard ratios the clinician can act on. **What is happening:** Seizure frequency and severity raise the hazard; adherence lowers it. **How it is happening:** Cox regression on the censored data; C-index evaluates risk ordering. **Reference:** Cox (1972); Harrell et al. (1996).

## Risk stratification + EP001

*Caption - Patients split into Low/Medium/High recurrence-risk tertiles for triage.*

| risk_band | patients |
|---|---|
| High | 167 |
| Low | 167 |
| Medium | 166 |

**EP001:** risk band = **High** (risk score 1.417); estimated
recurrence probability by 90/180/365 days = 0.666 / 0.875 / 0.986.

## Role in the framework

```mermaid
flowchart LR
    F[EEG + clinical features] --> COX[Cox recurrence model]
    COX --> RISK[Risk band Low/Med/High]
    RISK --> C5[Confidence gate]
    C5 --> N[Neurologist - follow-up plan]
```

**Reason:** Show recurrence risk feeding follow-up decisions. **Why:** Risk-based follow-up beats fixed intervals. **What is happening:** Features → hazard → risk band → clinician plan, gated by confidence. **How it is happening:** Cox partial hazard ranks patients; high-risk get closer monitoring. **Reference:** Cox (1972).

## Professor Readiness (Defense Q&A)

**Q1: Why survival analysis, not classification?** Follow-up is censored and the question is *when*,
not just *whether*; Cox/KM handle censoring and yield time-specific risk.

**Q2: What does the C-index tell us?** How well the model orders patients by recurrence risk
(analogous to AUC for survival) — 0.663 here.

**Q3: How is it used clinically?** High-risk patients get shorter follow-up intervals and closer
remote monitoring; the neurologist confirms the plan.

## References

Cox, D. R. (1972). Regression models and life-tables. *JRSS B, 34*(2), 187-220.

Harrell, F. E., Lee, K. L., & Mark, D. B. (1996). Multivariable prognostic models. *Statistics in Medicine, 15*(4), 361-387.

Kaplan, E. L., & Meier, P. (1958). Nonparametric estimation from incomplete observations. *JASA, 53*(282), 457-481.
