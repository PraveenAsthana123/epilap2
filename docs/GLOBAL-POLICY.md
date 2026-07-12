# GLOBAL POLICY (Mandatory)

These rules are **mandatory** for every document and code change in this project. They apply
automatically — no need to restate them per task.

| # | Policy | Rule |
|---|---|---|
| 1 | **Scope** | Epilepsy only. Exclude schizophrenia/PANSS/psychiatry; translate any such structure to epilepsy (Neurologist + EEG Technician). |
| 2 | **Order** | Docs first, then code. |
| 3 | **Format** | All data presented in Markdown tables. |
| 4 | **Granularity** | One MD file per unit of data (per assessment / phase / role). |
| 5 | **Diagrams** | Every doc must present: **flowchart**, **sequence diagram**, **network diagram**, **journey map** (Mermaid). |
| 6 | **Citations** | APA 7th edition formatting in every References section. |
| 7 | **UX** | Advanced readability, clear flow, polished UI/UX in the viewer. |
| 8 | **Tracking** | Terminal task list kept current every turn (done vs pending). |
| 9 | **Prompt log** | Save each prompt input + response output to `docs/prompt-log/`. |
| 10 | **Tooling** | Install any needed software (pre-approved). |
| 11 | **Top-1% bar** | Brutal self-review each pass: name what's missing for a top-1% DBA and close gaps. See [GAP-ANALYSIS.md](GAP-ANALYSIS.md). |
| 12 | **References** | Every substantive doc ends with an APA7 **References** section. |
| 13 | **Explainability / justification** | Every heading and subheading carries a short **Why** (reason it exists) and **How** (method), so each level is self-explaining. |
| 14 | **Professor readiness** | Every doc ends with a **Professor Readiness (Defense Q&A)** section: hypothetical examiner questions as sub-headings, each answered concisely via step/table/flowchart/1–3 lines. |
| 15 | **Research spine** | Every doc contains, in order: **Problem → Sub-problems → Research Problem → Research Objective → Flow → Hypotheses → Statistical Analysis**. |
| 16 | **Step duality** | Every step is explained with **both a table and a flowchart**. |
| 17 | **Table captions** | Every table is preceded by a 1–2 line note explaining *why that table is present*. |
| 18 | **Progress cadence** | Whenever a long-running background task (workflow/build) is active, post a status update to the user every ~5 minutes until it completes. |
| 19 | **Standing approval** | Do not pause to ask for approval. Proceed autonomously under this policy — install tooling, run workflows, write files, and complete every task. Only stop for genuinely destructive/irreversible actions. |
| 20 | **Auto-resume after session limit** | If a workflow agent fails with a session/usage limit, schedule a wakeup for just after the stated reset time and automatically resume the workflow (`resumeFromRunId`, which replays cached successes and re-runs only the failed agents). Report which items were deferred. |
| 21 | **C4 + detailed diagram explanation** | In addition to flowchart/sequence/network/journey, include a **C4-style model** (context/container/component) where architecture is discussed. Every diagram, model, matrix, and accuracy figure gets a detailed prose explanation: **Reason · Why · What is happening · How it is happening · Reference**. |
| 22 | **Code comments + docstrings** | All code (scripts, generators, React components, workflow scripts) must carry docstrings/header comments and inline comments explaining intent. |
| 23 | **README** | Maintain a detailed top-level `README.md` (purpose, structure, how to run, standards, data, index). |
| 24 | **Save all inputs** | Every user input/prompt is recorded in `docs/prompt-log/`. |
| 25 | **Missing-check** | On each verification pass, actively check for anything missing (files, diagrams, references, sections) and record it in `docs/COVERAGE-MATRIX.md` with a fix. |
| 26 | **Security-grade** | Every data path is security-grade by design: **HIPAA** Security/Privacy Rule, **NIST** CSF + 800-53 + AI RMF, **OWASP** Top-10 (web + LLM). See [governance/00-security-compliance.md](governance/00-security-compliance.md). |
| 27 | **Encryption** | PHI encrypted **at rest (AES-256)** and **in transit (TLS 1.2+)**; keys in KMS (rotated); de-identify (Safe-Harbor) before analysis; no secrets/raw EEG in the repo. |
| 28 | **Consent + EULA** | Before any patient data is used for analysis, capture **informed consent + EULA** (versioned, timestamped, revocable). See [governance/02-patient-consent-eula.md](governance/02-patient-consent-eula.md). |
| 29 | **IRB** | Human-subjects data use requires an **IRB** protocol/approval on file. See [governance/01-irb-submission.md](governance/01-irb-submission.md). |
| 30 | **Every phase = pipeline + analysis + monitoring + scoring + visualization + dashboard + report** | Each model/data phase must implement (or document) all seven: statistical + ML + subjective/sensitivity analysis, continuous monitoring (drift/concept-drift/alerts), scoring, a visualization, a dashboard, and a report. |
| 31 | **Full analysis set** | Each dataset/model carries: EDA + class-balance (with SMOTE), feature engineering + selection, HPO, full **accuracy matrix** (acc/precision/recall/specificity/F1/AUC/AP/log-loss), loss curve, hypothesis test, sensitivity/ablation, SHAP/permutation explainability, before/after data visualization — all presented in the viewer UI. |
| 34 | **APA-7 labelling + no-split rendering (mandatory)** | Apply **APA-7** style to every **heading, figure, table, chart, and graph**: figures/tables are numbered per chapter (Figure 1.1, Table 1.1) with an italic title caption; every References section is APA-7. In the compiled PDFs, a **table must not split across two pages** and a **figure + its caption must not split across two pages** (use `KeepTogether`). Each thesis chapter opens with an **"At a glance"** structured block (bullets + mini-table). |
| 33 | **Structured format over prose (mandatory)** | Prefer **tables, bullet points, sequential (numbered) steps, and diagrams** over paragraphs everywhere except the thesis chapters. Rules: (a) **no heading's body exceeds 2–3 lines of text** — convert the rest into a table, bullets, or a diagram; (b) if content has a **logical order → numbered sequential steps**; if not → **bullet points**; (c) **convert as many headings as possible into tables**; (d) every analysis/pipeline carries a **flowchart + sequence diagram + network flow** plus a step table. Install and use rich visual libraries in the viewer: **Mermaid** (flowchart/sequence/network/C4), **KaTeX/LaTeX** (math), **Recharts** (bar/pie/trend/line/radar/area). See [[format-preference-no-prose]]. |
| 32 | **Thesis framework (mandatory)** | The deliverable is a **doctoral (DBA) dissertation**, not a blueprint. Maintain `docs/thesis/` with the standard structure — **Front matter** (title, abstract, declaration, acknowledgements, table of contents, list of figures/tables, abbreviations) → **Ch1 Introduction** → **Ch2 Literature Review** → **Ch3 Methodology** → **Ch4 System Design & Architecture** → **Ch5 Implementation** → **Ch6 Results & Evaluation** → **Ch7 Discussion** → **Ch8 Conclusion, Limitations & Future Work** → **References (APA-7)** → **Appendices**. Write **flowing academic prose** (formal, third-person) — no "Why/How" markers or "Professor Q&A" inside thesis chapters. **Every chapter must contain all four diagram types — flowchart, sequenceDiagram, network (graph), and a C4 model — plus at least two tables and one chart/graph.** Use **real numbers only**; label synthetic vs real honestly. Compile to a thesis PDF (`analysis/build_thesis_pdf.py`). Keep quality high on every pass; track progress in the todo list. |

## Diagram Standard (Mermaid)

| Diagram | Mermaid type | Purpose |
|---|---|---|
| Flowchart | `flowchart TD` | Process/decision flow |
| Sequence | `sequenceDiagram` | Actor interactions over time |
| Network | `graph LR` | Component/data relationships |
| Journey map | `journey` | Patient/clinician experience |

## Test Patient

All worked examples use **EP001** (EP-2026-001) — see [primary-assessment/index.md](primary-assessment/index.md).
