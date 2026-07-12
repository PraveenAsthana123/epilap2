# Prompt Log — Session 003 (2026-07-11): Role Assessments, Scoring, Analytics

> **Why (this doc):** Global policy rules 9 & 24 require every user prompt to be recorded for
> reference, reproducibility, and defense validation. **How:** Each user input this session is
> captured verbatim-in-substance with the resulting action and a validation checkpoint, so the
> work can be audited against the request.

**Session date:** 2026-07-11 · **Patient anchor:** EP001 · **Repo:** https://github.com/PraveenAsthana123/epilap2

## Prompt → Action → Validation Checkpoint

| # | User Prompt (substance) | Action Taken | Validation Checkpoint |
|---|---|---|---|
| 1 | Push the code to GitHub (`epilap2`) | `git init`, commit, push; fixed GH email-privacy block via noreply author | Repo live at `epilap2`, `main` pushed |
| 2 | Did you build each assessment / form for each role? | Reported only Neurologist + EEG Tech had forms; 6 roles missing | Gap table produced |
| 3 | Each role's questions must be present in the UI | Built assessment forms for all 6 missing roles (49 files) | Viewer auto-renders under Primary Assessment |
| 4 | Build the model / list of answer options; severity Mild/Intermediate/Severe (3–4 levels) | Added 4-level Severity Scenario Model to all 64 sections | `grep` verified severity block + Level 4 in all 64 |
| 5 | Operational case where attack happens every ~5 min | Level 4 = Refractory/Status (status epilepticus, seizures ~every 5 min) | Present in every section's L4 table |
| 6 | Each role must have separate UI; left menu per role; list of tabs | Rebuilt viewer as role-portal (top tabs + per-role left menu) | `npm run build` clean |
| 7 | Once user gives input for assessment, score them | Fill & Score mode: parse level tables → form → section/role/patient score | Parser verified on all 64 sections, 0 failures |
| 8 | Reposition research to AI-enabled epilepsy care platform (6 objectives, 3 pipelines, dataset strategy) | Built `research-vision.md` + `patient-onboarding.md`; crosswalk to existing docs | Objectives mapped to existing docs |
| 9 | Build end-to-end PRIMARY data analysis using statistical methods, top 1%, production-grade, nothing missing | Analytics package (this deliverable) | Runnable scripts + computed results |
| 10 | Similarly build SECONDARY (EEG) analysis end-to-end | Secondary pipeline | Runnable + results |
| 11 | Then COMBINE both for one patient (EP001) end-to-end | Fusion pipeline + EP001 case | Runnable + EP001 report |
| 12 | Save these input prompts in an md file for reference & validation | This file | — |
| 13 | If something missing, add it | Missing-check pass recorded in `COVERAGE-MATRIX.md` | Gap list closed |
| 14 | Each flowchart must present C4 model | C4 model added to analysis + vision docs | C4 block per architecture doc |
| 15 | Ensure each process designed at code level, very detailed, commented | Every pipeline stage = commented function + docstring | Code review |
| 16 | README in detail | `analysis/README.md` | — |
| 17 | Each role assessment matrix → feature engineering, evaluation, selection, one-hot, normalization, standardization, feature balance, bias check | Primary pipeline implements each step | Step outputs saved |

## Notes
- **Scope guard:** the user pasted material from a parallel schizophrenia/PANSS/DSM project; per
  global policy rule #1 all of it is translated to **epilepsy** (EP001, ILAE, QOLIE-31, GAD-7,
  NDDI-E, antiseizure medications) and no psychiatry content is introduced.
- See [[index]] for the full prompt-log index and [../COVERAGE-MATRIX.md](../COVERAGE-MATRIX.md)
  for the missing-item checklist.
