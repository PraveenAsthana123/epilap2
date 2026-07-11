# Brutal Gap Analysis — What's Missing for Top 1%

Honest audit of the current artifact set against a top-1% DBA standard. No sugar-coating.

## Scorecard

| Area | Now | Top-1% bar | Gap |
|---|---|---|---|
| Blueprint coverage | ✅ Parts I–VIII, Pipelines A–E | Same | Minor — needs diagrams + APA7 |
| Primary assessment data (EP001) | ✅ 21 MD files, tables | Multi-patient cohort | Only 1 patient; need EP002+ |
| Diagrams | 🟡 Flowchart on 2 phases | 4 diagram types in **every** doc | Most docs have none yet |
| APA7 references | ❌ none | Every doc | Missing everywhere |
| Literature review | ❌ placeholder | 60–100 cited sources, synthesis matrix | Not written |
| Methodology rigor | 🟡 outline | Sample size/power, ethics, consent, validity/reliability | Thin |
| Statistical plan | 🟡 named tests | Assumptions, effect sizes, CIs, multiple-testing correction, worked numbers | Not worked |
| ML rigor | 🟡 listed models | Subject-level CV, external validation, calibration, fairness, leakage checks | Described, not evidenced |
| Explainability | 🟡 listed methods | SHAP/Grad-CAM worked examples + clinician-agreement study | Not worked |
| Brain localization | ❌ | Channel→region mapping (frontal/temporal/parietal/occipital), focus + confidence | Missing (clinically vital) |
| Remote monitoring | 🟡 mentioned | Wearable/mobile data model, alert thresholds, relapse warning | Not specified |
| RAG evaluation | 🟡 named frameworks | RAGAS/DeepEval metrics with targets + hallucination policy | Not evidenced |
| Governance | 🟡 lists | Risk register (done), bias/drift dashboards, human-override audit, versioning | Partial |
| Business/ROI | 🟡 example KPIs | NPV/IRR/payback model with assumptions | Illustrative only |
| Datasets | ❌ | TUH, Siena, EPILEPSIAE, HEP scored for fit + access path | Not documented |
| Viewer UX | 🟡 good | Diagram rendering (done), heading hierarchy (done), TOC, dark/light, print/PDF export | TOC + export missing |
| Reproducibility | ❌ | Feature dictionary, model cards, data lineage, env/versioning | Missing |
| Ethics/regulatory | 🟡 mentioned | Consent, de-identification, "decision support not diagnosis" framing, IRB note | Thin |

## Top-10 Priorities (ordered)

| # | Fix | Why it matters |
|---|---|---|
| 1 | Mandatory 4 diagrams + APA7 in every doc | Policy compliance; readability |
| 2 | Brain-localization module (channel→region, focus, confidence) | Highest clinical value; differentiates from EEG-classification papers |
| 3 | Literature review with synthesis matrix + gap table | Core of any doctorate |
| 4 | Worked statistics + ML rigor (leakage, subject-level CV, calibration, fairness) | Scientific defensibility |
| 5 | Remote-monitoring spec (wearables, thresholds, relapse alerts) | Broadens contribution beyond EEG |
| 6 | Dataset dossier (TUH/Siena/EPILEPSIAE/HEP scored) + hybrid design | Feasibility |
| 7 | RAG evaluation metrics + hallucination policy | Trust/safety |
| 8 | ROI model with explicit assumptions (NPV/IRR/payback) | DBA business core |
| 9 | Model cards + feature dictionary + data lineage | Reproducibility |
| 10 | Viewer: TOC, PDF export, per-role dashboards | Presentation polish |

## References

American Psychological Association. (2020). *Publication manual of the American Psychological
Association* (7th ed.). https://doi.org/10.1037/0000165-000
