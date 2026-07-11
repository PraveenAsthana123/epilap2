# Project Plan

Living plan for the DBA epilepsy docs + viewer. Governed by [GLOBAL-POLICY.md](GLOBAL-POLICY.md).

## Status Legend
✅ done · 🟡 in progress · ⬜ pending

## Milestones

| # | Milestone | Status |
|---|---|---|
| 1 | Blueprint docs (Parts I–VIII, Pipelines A–E, appendix, publication strategy) | ✅ |
| 2 | Primary Assessment EP001 (Neurologist 15, EEG Technician 6, roles/tasks, AI features, index) | ✅ |
| 3 | React viewer (Vite, auto-load MD, nav, search, GFM tables) running at localhost:5173 | ✅ |
| 4 | Global policy persisted (memory + GLOBAL-POLICY.md) | ✅ |
| 5 | Prompt log started (`docs/prompt-log/`) | 🟡 |
| 6 | Mermaid diagrams in viewer (flowchart, sequence, network, journey) | ✅ |
| 7 | Pipeline A phases 1–16 (epilepsy, EP001, tables, 4 diagrams each, APA7) | ✅ |
| 8 | Retrofit blueprint docs (12) with mandatory diagrams + APA7 | ✅ |
| 9 | Pipeline B (EEG) 1–16 phase docs to full standard | ✅ |
| 10 | Stakeholder sims (Neurologist, EEG Tech, Nurse, Patient, Caregiver, Administrator) | ✅ |
| 11 | Top-1% gap docs (brain-localization, remote-monitoring, literature review, dataset dossier) | ✅ |
| 12 | Global approvals in user settings.json | ✅ |
| 13 | Viewer UI/UX polish pass (TOC, PDF export) | ⬜ optional |

**Totals:** 87 Markdown docs · 38 auto-generated with all 4 diagram types · build passes · viewer live at localhost:5173.

## Notes / Requests Parked

| Request | Decision |
|---|---|
| Cron job to auto-complete tasks | Not created yet — needs confirmation of exact schedule/action before I set up a recurring agent. |
| "All approvals" | Treated as standing approval to install tooling and write files in this repo. |
