# Enterprise AI Platform for Explainable Multimodal Epilepsy Intelligence

> A **DBA dissertation deliverable**: a navigable, research-grade documentation set plus a
> React viewer for an explainable, multimodal, enterprise AI platform for epilepsy care.
> **Reason:** epilepsy care is fragmented across clinical assessment and EEG. **Why:** a DBA
> must link technical innovation to organizational value. **What:** 100+ canonical Markdown
> docs + a Vite/React viewer. **How:** docs authored to an 18+-rule standard, rendered with
> Mermaid diagrams. **Reference:** see `docs/00-overview.md`.

## 1. What this is

A structured blueprint + reference documentation for a healthcare AI platform, organized so an
examiner can trace the argument from business problem → data → models → explainability →
deployment → governance → business value.

## 2. Repository structure

| Path | Contents |
|---|---|
| `docs/` | All documentation (100+ Markdown files) — see index below |
| `docs/pipeline-a/` | Primary Clinical Assessment AI — 16 phase docs (EP001) |
| `docs/pipeline-b/` | Secondary EEG AI — 16 phase docs |
| `docs/stakeholders/` | Role simulations (Neurologist, EEG Tech, Nurse, Patient, Caregiver, Administrator) |
| `docs/roles-study/` | Per-role retrospective + prospective study designs |
| `docs/datasets/` | Modality dossiers 18–25 (remote monitoring, wearable, imaging, genomics, surgery, ICU, population) |
| `docs/source-datasets/` | Named datasets: EPILEPSIAE, TUH, PhysioNet, NINDS + comparison matrix |
| `docs/hep/` | Human Epilepsy Project primary dataset (modules 1–5 + integration + 20-layer architecture) |
| `docs/primary-assessment/` | EP001 raw assessment data (Neurologist 15 + EEG Technician 6) |
| `docs/prompt-log/` | Record of every user input/prompt (policy 24) |
| `viewer/` | Vite + React app that auto-loads and renders all docs with Mermaid diagrams |
| `data/synthetic/` | Synthetic sample CSVs (11 schemas, EP001 canonical) |
| `data/siena-sample/` | Real Siena EEG metadata (git-friendly; EDF fetched locally) |
| `workflow-*.js` | Multi-agent authoring scripts (documented, re-runnable) |

## 3. Governing standard

Every substantive doc follows **`docs/GLOBAL-POLICY.md`** (25 mandatory rules). Highlights:

| Rule area | Requirement |
|---|---|
| Scope | Epilepsy only |
| Format | Markdown tables, one MD file per unit, captions on every table |
| Diagrams | flowchart + sequence + network + journey + **C4 model** per doc |
| Explainability | Per-heading Why/How; per-diagram Reason/Why/What/How/Reference |
| Rigor | Research spine (Problem→…→Statistical Analysis), APA7 references, Professor-Readiness Q&A |
| Ops | Terminal task tracking, ~5-min progress updates, prompt logging, auto-resume after limits |

## 4. How to run the viewer

```bash
cd viewer
npm install        # first time only (installs React, Vite, Mermaid, react-markdown)
npm run dev        # serves at http://localhost:5173
# or
npm run build      # production build to viewer/dist
```

The viewer auto-discovers every `docs/**/*.md` via `import.meta.glob`, renders GitHub-flavored
tables, and turns ` ```mermaid ` blocks into diagrams. Sidebar navigation + full-text search.

## 5. Data

- **Synthetic CSVs** (`data/synthetic/`) — regenerate with `python data/generate_synthetic.py`.
- **Real EEG** — access-controlled or large; see `data/README.md` and `docs/dataset-scorecard.md`.
  Fetch one open Siena record locally (kept out of git):
  ```bash
  curl -o data/siena-sample/PN00/PN00-4.edf \
    https://physionet.org/files/siena-scalp-eeg/1.0.0/PN00/PN00-4.edf
  ```

## 6. Canonical example patients

| ID | Profile | Used in |
|---|---|---|
| **EP001** | 29M, focal impaired awareness, left-temporal | Pipeline A/B, primary-assessment, datasets |
| **HEP001** | 27F, temporal lobe epilepsy | HEP modules |

## 7. Key entry docs

- `docs/00-overview.md` — dissertation entry point
- `docs/GLOBAL-POLICY.md` — the mandatory standard
- `docs/PLAN.md` — milestones
- `docs/COVERAGE-MATRIX.md` — traceability + missing-checks
- `docs/GAP-ANALYSIS.md` — brutal top-1% gaps
- `docs/dataset-scorecard.md` — which dataset to use

## 8. Caveat

Clinical numbers (accuracies, KPIs, confidences) are **illustrative placeholders**; replace
with real data and citations before submission.
