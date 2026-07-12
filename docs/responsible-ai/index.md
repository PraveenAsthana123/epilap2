# Responsible AI Framework (Epilepsy Intelligence Platform)

> **Why (this section):** A clinical AI platform for epilepsy is only adoptable if it is
> trustworthy end-to-end — explainable, fair, accountable, secure, compliant, and kept
> under human control. This section consolidates the platform's Responsible-AI pillars
> into one governed framework, each pillar anchored on patient **EP001** and mapped to a
> concrete, often already-implemented, mechanism in this repo. **How:** one policy-compliant
> doc per pillar (definition, mechanisms/controls, metrics with thresholds, where-implemented,
> the four Mermaid diagrams + a C4 model, Defense Q&A, APA-7 references).

## The pillars

| # | Pillar | Doc | Core question it answers |
|---|---|---|---|
| 1 | **Responsible AI** | [01-responsible-ai.md](01-responsible-ai.md) | What principles bind the whole platform? |
| 2 | **Accountable AI** | [02-accountable-ai.md](02-accountable-ai.md) | Who owns each decision; what is logged? |
| 3 | **Fairness AI** | [03-fairness-ai.md](03-fairness-ai.md) | Is the model equitable across groups? |
| 4 | **Bias AI** | [04-bias-ai.md](04-bias-ai.md) | What biases exist and how are they detected? |
| 5 | **Explainable AI** | [05-explainable-ai.md](05-explainable-ai.md) | Why did the model produce this output? |
| 6 | **Governance AI** | [06-governance-ai.md](06-governance-ai.md) | How is the model lifecycle governed? |
| 7 | **Interpretable AI** | [07-interpretable-ai.md](07-interpretable-ai.md) | Are the models glass-box where they can be? |
| 8 | **Portable AI** | [08-portable-ai.md](08-portable-ai.md) | Does it interoperate and deploy across sites? |
| 9 | **Performance AI** | [09-performance-ai.md](09-performance-ai.md) | How well does it perform and stay calibrated? |
| 10 | **Ethical AI** | [10-ethical-ai.md](10-ethical-ai.md) | Is it beneficent, just, and consent-based? |
| 11 | **Secure AI** | [11-secure-ai.md](11-secure-ai.md) | Is PHI protected and the model robust? |
| 12 | **Risk AI** | [12-risk-ai.md](12-risk-ai.md) | What clinical/model risks, and their controls? |
| 13 | **AI Control Tower** | [13-ai-control-tower.md](13-ai-control-tower.md) | How is everything monitored centrally? |
| 14 | **AI Federation** | [14-ai-federation.md](14-ai-federation.md) | How do sites train without sharing PHI? |
| 15 | **Compliance AI** | [15-compliance-ai.md](15-compliance-ai.md) | Which regulations, and how are they met? |
| 16 | **Decision AI** | [16-decision-ai.md](16-decision-ai.md) | Decision support vs decision making; who decides? |

## Already live in this repo

| Pillar | Concrete implementation |
|---|---|
| Fairness / Bias | `analysis/primary_analysis.py` → `bias_check()` reports demographic-parity + equal-opportunity gaps across sex and age band (thresholds < 0.10) |
| Explainable / Interpretable | ordinal logistic odds ratios + feature-selection ranking in `analysis/`; [pipeline-a/phase-11](../pipeline-a/phase-11-explainable-ai.md) |
| Performance | cross-validated AUCs (primary 0.969, EEG focus 0.93, fusion 0.976) in [analysis](../analysis/index.md) |
| Governance / Compliance | [pipeline-a/phase-16](../pipeline-a/phase-16-governance-compliance.md); reproducible seeds + audit trail |
| Decision / Human-in-the-loop | fusion CDSS keeps the neurologist as the authority ([fusion-analysis](../analysis/fusion-analysis.md)) |

See the platform vision in [research-vision](../research-vision.md).
