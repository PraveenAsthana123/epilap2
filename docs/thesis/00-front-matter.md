# An Enterprise-Grade Explainable Multimodal AI Platform for Remote Epilepsy Care: Design, Implementation, and Evaluation

**A dissertation submitted in partial fulfilment of the requirements for the degree of Doctor of Business Administration (DBA)**

*Reference index case: Patient EP001 · Scope: Epilepsy*

> **Compiled PDF:** this dissertation is compiled to [DBA-Epilepsy-Thesis.pdf](../DBA-Epilepsy-Thesis.pdf)
> (52 pp) via `python analysis/build_thesis_pdf.py`. The companion technical deliverable is
> [DBA-Epilepsy-Deliverable.pdf](../DBA-Epilepsy-Deliverable.pdf).

---

## Abstract

Epilepsy affects approximately fifty million people worldwide, yet its diagnosis and ongoing
management remain slow, fragmented, and unevenly explained. Clinical history captured by neurologists
and electrophysiological evidence captured by electroencephalography (EEG) technicians are rarely fused
within a single, governed, enterprise workflow, and the machine-learning models that could assist are
too often delivered as isolated artefacts without the data-engineering, deployment, monitoring, and
governance scaffolding that a healthcare organisation requires. This dissertation addresses that
organisational gap. Adopting a Design Science Research paradigm combined with a mixed-methods
evaluation, it designs, implements, and evaluates an enterprise-grade, explainable, multimodal
artificial-intelligence platform for remote epilepsy care, structured as seven connected operating
pipelines spanning research protocol, data engineering, feature engineering, statistical and machine
learning modelling, machine-learning operations, retrieval-augmented generation with a knowledge graph,
and clinical safety with responsible-AI governance.

The empirical core of the work is a reproducible analysis of **real scalp EEG** from the CHB-MIT
database. Using signal preprocessing, time-frequency transforms (short-time Fourier and continuous
wavelet), one-dimensional-to-two-dimensional image representations, and a set of interpretable
biomarkers (spectral band power, Hjorth parameters, Higuchi fractal dimension, spectral entropy,
phase-locking value, and line-length), a hyperparameter-tuned, class-balanced classifier discriminates
ictal from interictal states with a cross-validated area under the receiver-operating-characteristic
curve (ROC-AUC) of approximately 0.92, rising to approximately 0.97 for ictal-versus-interictal
separation, and generalises to an external EEG benchmark (EEG-Eye-State) at a ROC-AUC of approximately
0.979. Explainability via SHAP and permutation importance converges on line-length, gamma-band power,
and phase-locking value as the dominant discriminators, and non-parametric hypothesis testing confirms
their significance. Clinical severity, seizure-recurrence, and longitudinal models are demonstrated on
a clearly labelled synthetic 500-patient cohort pending institutional-review-board-approved clinical
data. The platform is delivered as running code, an interactive viewer with fifteen analytical views,
a knowledge graph exported as Resource Description Framework triples, and a compiled dissertation.

The contribution is fourfold: a theoretical operating model for governed multimodal epilepsy
intelligence; a methodological pipeline demonstrating real-EEG, explainable, reproducible analysis; a
practical deployable artefact; and an honest account of the boundary between what is implemented and
what remains specified. The work argues that the decisive gap in clinical AI is not algorithmic but
operational, and that value accrues when models are embedded in owned, governed, monitored pipelines
with human oversight throughout.

**Keywords:** epilepsy, electroencephalography, explainable AI, multimodal fusion, MLOps, responsible
AI, knowledge graph, retrieval-augmented generation, design science, clinical decision support.

---

## Declaration

I declare that this dissertation is my own work and that all sources have been acknowledged in
accordance with APA 7th-edition conventions. The empirical EEG analyses use publicly available,
de-identified datasets (CHB-MIT via PhysioNet; EEG-Eye-State via OpenML). Clinical cohort data used for
the severity and recurrence demonstrations are synthetic and are labelled as such throughout. The
platform is a research and decision-support artefact; it is not a certified medical device and does not
provide autonomous diagnosis.

## Acknowledgements

The author acknowledges the PhysioNet and OpenML communities for open datasets, the maintainers of the
open-source scientific Python and JavaScript ecosystems on which the artefact is built, and the
clinical framing provided by the International League Against Epilepsy classification.

---

## Table of Contents

*Caption — the dissertation structure; each chapter carries a flowchart, sequence diagram, network
diagram, and C4 model, with supporting tables and figures.*

| Chapter | Title |
|---|---|
| Front matter | Title · Abstract · Declaration · Acknowledgements · Contents · Figures/Tables · Abbreviations |
| 1 | Introduction |
| 2 | Literature Review |
| 3 | Research Methodology |
| 4 | System Design & Architecture |
| 5 | Implementation |
| 6 | Results & Evaluation |
| 7 | Discussion |
| 8 | Conclusion, Limitations & Future Work |
| References | Consolidated APA-7 references (per chapter) |
| Appendices | Governance pack, enterprise-flow specifications, knowledge-graph ontology |

## List of Abbreviations

*Caption — abbreviations used throughout the dissertation.*

| Abbrev. | Meaning |
|---|---|
| AI | Artificial Intelligence |
| ASM | Anti-Seizure Medication |
| AUC | Area Under the ROC Curve |
| CWT | Continuous Wavelet Transform |
| DBA | Doctor of Business Administration |
| DSR | Design Science Research |
| EEG | Electroencephalography |
| HIPAA | Health Insurance Portability and Accountability Act |
| ILAE | International League Against Epilepsy |
| KG | Knowledge Graph |
| MCP | Model Context Protocol |
| MLOps | Machine-Learning Operations |
| NIST | National Institute of Standards and Technology |
| PLV | Phase-Locking Value |
| PR-AUC | Area Under the Precision-Recall Curve |
| RAG | Retrieval-Augmented Generation |
| RDF | Resource Description Framework |
| ROC | Receiver Operating Characteristic |
| SHAP | SHapley Additive exPlanations |
| SMOTE | Synthetic Minority Over-sampling Technique |
| STFT | Short-Time Fourier Transform |
