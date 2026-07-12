# Governance Runtime — Confidence/Uncertainty (C5) & Concordance (C6)

> **Why (this doc):** The two governance-core capabilities that define the DBA contribution,
> executed as real code on the epilepsy drug-resistance model. C5 tells the platform **when to
> defer to the clinician**; C6 tells it **when the evidence sources disagree** (mandatory human
> review). **How:** every number/figure is computed by `analysis/governance.py`.

## C5 — Confidence & Uncertainty Estimation (with abstention)

*Caption - Calibration, uncertainty, and the abstention value proposition — accuracy is higher on the confident subset.*

| metric | value |
|---|---|
| Brier (raw) | 0.072 |
| Brier (calibrated) | 0.075 |
| Accuracy (all) | 0.907 |
| Accuracy (confident 80%) | 0.942 |
| Accuracy (deferred 20%) | 0.759 |
| Abstention rate | 0.193 |
| Mean entropy | 0.175 |
| Mean ensemble variance | 0.121 |

![Reliability](analysis/outputs/governance/reliability.png)

**Human-oversight value:** deferring the least-confident 20% of cases raises accuracy from
**0.907** (all) to **0.942** (confident subset) —
the deferred cases go to the clinician. EP001 predicted p = 0.911
(margin 0.411).

**Reason:** Estimate confidence and abstain when uncertain. **Why:** Safe clinical AI must know when NOT to answer and defer to a human. **What is happening:** Calibrated probabilities + margin/entropy/ensemble-variance gate an abstention rule. **How it is happening:** The confident subset is more accurate; uncertain cases route to the neurologist. **Reference:** Guo et al. (2017); Kompa, Snoek & Beam (2021).

## C6 — Clinical Evidence Concordance Engine

*Caption - Per-patient agreement across three INDEPENDENT high-severity signals (clinical rule, EEG rule, model).*

| concordance | patients |
|---|---|
| Concordant | 242 |
| Discordant | 152 |
| Partial | 106 |

**Discordant patients flagged for mandatory human review:** 152.
**EP001:** clinical_high=1, eeg_high=1,
model_high=1 → **Concordant**.

**Reason:** Detect agreement/conflict across evidence sources. **Why:** Trust requires knowing when EEG, clinical, and model evidence disagree. **What is happening:** Three independent signals are compared; discordant cases are escalated. **How it is happening:** Agreement of 3/3 = concordant, 2/3 = partial, lone dissenter = discordant -> human review. **Reference:** Rosenow & Luders (2001).

## Role in the framework (sequence)

```mermaid
sequenceDiagram
    participant F as Fusion model
    participant C5 as Confidence engine
    participant C6 as Concordance engine
    participant N as Neurologist
    F->>C5: prediction + probability
    C5->>C6: confident? (else defer)
    C6->>N: concordant -> recommend; discordant/uncertain -> mandatory review
    N-->>F: decision + feedback
```

**Reason:** Show how C5 + C6 gate the recommendation. **Why:** Governance means the AI recommends only when confident AND concordant. **What is happening:** Low confidence or discordant evidence routes to the clinician. **How it is happening:** Two gates sit between the model and any recommendation. **Reference:** NIST (2023).

## Professor Readiness (Defense Q&A)

**Q1: Why abstain instead of always predicting?** Because deferring uncertain cases to the
clinician raises reliability where it matters and is the operational meaning of "human oversight."

**Q2: Are the concordance signals independent of the target?** Yes — the clinical and EEG rules
are derived from raw features, not the label, so agreement is informative rather than circular.

**Q3: What happens to discordant patients?** They are flagged for mandatory human review — the
platform does not issue an autonomous recommendation when evidence conflicts.

## References

Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. *ICML*.

Kompa, B., Snoek, J., & Beam, A. L. (2021). Second opinion needed: communicating uncertainty in medical ML. *npj Digital Medicine, 4*(4).

NIST. (2023). *AI Risk Management Framework (AI RMF 1.0)*.

Rosenow, F., & Luders, H. (2001). Presurgical evaluation of epilepsy. *Brain, 124*(9), 1683-1700.
