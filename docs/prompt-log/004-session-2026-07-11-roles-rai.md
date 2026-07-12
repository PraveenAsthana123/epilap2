# Prompt Log — Session 004 (2026-07-11): OT Role, Enterprise Questionnaires & Responsible AI

> **Why (this doc):** Global policy rules 9 & 24 require every user input to be recorded for
> reference, reproducibility, and defense validation. **How:** Each user input in this stretch
> of the session is captured with its resulting action and a validation checkpoint, so the
> work can be audited against the request. Continues [003-session-2026-07-04-analysis](003-session-2026-07-11-analysis.md).

**Session date:** 2026-07-11 · **Patient anchor:** EP001 · **Repo:** https://github.com/PraveenAsthana123/epilap2

## Prompt → Action → Validation Checkpoint

| # | User Prompt (substance) | Action Taken | Validation Checkpoint |
|---|---|---|---|
| 1 | Responsible-AI pillar list (16: Responsible, Accountable, Fairness, Bias, Explainable, Governance, Interpretable, Portable, Performance, Ethical, Secure, Risk, AI Control Tower, AI Federation, Compliance, Decision) | Built `docs/responsible-ai/` — 16 pillar docs + index; new nav group | 16 pillar docs present; each with C4 + 4 diagrams |
| 2 | Begin Occupational Therapist (OT) module in enterprise format (Section 1, Categories A–G, OT001–OT070; participation map; smart logic; AI variables) | Built OT as the 9th role: 7 sections + landing; wired to role portal + scoring | OT sections have severity model; viewer builds |
| 3 | "Have these been addressed as form/survey/questionnaire to ask patient by each role?" | Assessed gap; confirmed enterprise questionnaire format needed | Gap acknowledged honestly |
| 4 | Use full enterprise questionnaire columns; apply to all 9 roles | Added `## Questionnaire (Enterprise Form)` (ID · Question · Response Type · Validation · EP001 · AI Feature) to all 71 sections | 71/71 sections verified; severity models intact |
| 5 | Responsible-AI IMPLEMENTATION spec — tools (LangSmith, WhyLabs, Fiddler, AIF360, Fairlearn, SHAP, LIME, InterpretML, NeMo Guardrails, Llama Guard, Counterfit, Langfuse, OpenTelemetry, ServiceNow, Evidently, NIST) + flows (Accountable-AI gateway pipeline, Fairness 6-step pipeline, SHAP/LIME flows, Governance registry) | Built `docs/responsible-ai/implementation/`: index (tooling landscape + master flow) + accountable-ai-architecture, governance-registry, fairness-bias-pipeline, guardrails-redteam, explainability-shap-lime | Implementation docs authored; mapped to real `bias_check()` / CDSS |
| 6 | Save the input data in an md file | This file | — |

## Responsible-AI implementation — captured tool → capability map

| Capability | Tools (as specified) |
|---|---|
| Accountability / Observability | LangSmith, WhyLabs, Fiddler AI, Langfuse, OpenTelemetry |
| Fairness | IBM AI Fairness 360 (AIF360), Fairlearn |
| Bias detection | Fairlearn, AIF360, Evidently AI |
| Explainable AI | SHAP, LIME, InterpretML |
| Guardrails | NVIDIA NeMo Guardrails, Llama Guard, Guardrails AI |
| Red Team | Microsoft Counterfit, PyRIT, Garak |
| Compliance / Risk | NIST AI RMF, risk scoring |
| Governance | Model / prompt / dataset registry, ServiceNow approval |
| Human-in-the-loop | ServiceNow approval task, neurologist sign-off |

## Captured reference flows
- **Accountable AI:** User → API Gateway → Authentication → Policy Engine → Guardrail → LLM/Model → Human-in-the-Loop → Risk Engine; cross-cut by audit log + distributed tracing (Langfuse + OpenTelemetry) + explainability store (model/prompt/RAG/confidence). Any flagged agent is fixable without stopping the pipeline.
- **Fairness/Bias:** collect balanced data → check imbalance/missing-demographics/sampling+label bias → validate → handle missing/outliers/protected/labels → detect (demographic parity, equal opportunity, equalised odds, statistical parity difference) → mitigate (pre: reweight/balance/remove biased features; in: fairness-aware learning + regularisation; post: threshold + calibration) → train/evaluate/deploy.
- **SHAP:** input → train → explainer → feature coalitions → per-feature contribution → SHAP values → base + approval probability.
- **LIME:** input → complex model → synthetic samples → predict → local linear model → local feature importance.
- **Governance:** define policy (approved-for-production, data classification, RAI + human-approval requirements) → register assets (model/prompt/dataset versions) → approval gates.

## Notes
- **Scope guard:** the user's pasted neurologist expansion (~220–420 Q) and any Psychiatrist role are treated per global policy #1 — epilepsy only; psychiatry translated, not introduced. The neurologist role remains 15 sections unless expansion is explicitly requested.
- See [index](index.md) and [../COVERAGE-MATRIX.md](../COVERAGE-MATRIX.md).
