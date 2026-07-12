# Epilepsy Analytics — Primary · Secondary · Fusion (End-to-End, Reproducible)

> **Why (this folder):** This is the executable, production-grade heart of the DBA:
> three connected analysis pipelines that turn the eight-role clinical assessment data
> (primary) and EEG biomarkers (secondary) into an explainable, human-supervised,
> patient-level decision (fusion) — for the index patient **EP001**. Every table and
> figure in the analysis report docs is computed here and is byte-reproducible from a
> single command. **How:** deterministic synthetic data (seeded), one commented
> function per pipeline stage, and self-writing policy-compliant reports.

Scope: **epilepsy only** (patient EP001 = EP-2026-001). Data is **synthetic** but
causally structured so the statistics show real, defensible relationships.

---

## 1. Quick start

```bash
cd analysis
pip install -r requirements.txt          # numpy pandas scipy statsmodels matplotlib scikit-learn
python run_all.py                         # regenerates cohort + all three analyses + reports
```

Individual stages (each is runnable on its own once the cohort exists):

```bash
python make_cohort.py          # -> data/analysis/cohort_primary.csv, cohort_eeg.csv, data_dictionary.csv
python primary_analysis.py     # -> docs/analysis/primary-analysis.md   + analysis/outputs/primary/*
python secondary_analysis.py   # -> docs/analysis/secondary-analysis.md + analysis/outputs/secondary/*
python fusion_analysis.py      # -> docs/analysis/fusion-analysis.md
```

---

## 2. What each script does

| Script | Role | Key stages (each = one commented function) |
|---|---|---|
| `common.py` | Shared config, seeds, paths, markdown/figure/diagram helpers | `rng`, `df_to_md`, `save_fig`, `write_report`, `band_from_mean` |
| `make_cohort.py` | Generate the linked cohort (N=500) from a latent severity + focus side | `build_primary`, `build_eeg`, `inject_defects`, `set_ep001` |
| `primary_analysis.py` | **Primary** clinical-assessment pipeline (11 stages) | validate → clean → feature-engineering → encode/scale → EDA → statistics → feature-eval/select → balance → bias → baseline-model |
| `secondary_analysis.py` | **Secondary** EEG pipeline | QC → preprocess → biomarkers/region-map → EDA → statistics → focus-localization |
| `fusion_analysis.py` | **Fusion** + EP001 case | merge → incremental-value → EP001 end-to-end decision card |
| `run_all.py` | One-command reproduction | runs the four in dependency order |

---

## 3. Primary pipeline — the eleven processes (as requested)

The primary data is the **role-assessment matrix**: each of the eight role portals
(Neurologist, EEG Technician, Nurse, Neuropsychologist, Pharmacist, Caregiver, Patient,
Administrator) contributes its variables as columns; each patient is a row.

1. **Load matrix** — patient × role-tagged feature matrix.
2. **Validate** (find problems, read-only) — completeness, missingness, range, type,
   duplicates, logical consistency, overall data-quality score.
3. **Clean** (fix problems) — impossible-value → NaN → median/mode imputation, dedup,
   full **audit trail** (EP001 stays pristine).
4. **Feature engineering** — derived clinical indices (seizure burden, adherence gap,
   mood load, cognitive deficit, polytherapy, QoL deficit).
5. **Encode + scale** — **one-hot** encoding of categoricals; **min-max normalization**
   and **z-score standardization** of numerics (both retained; documented which model
   uses which).
6. **EDA** — descriptives, Spearman correlation heatmap, severity boxplots.
7. **Statistics** — Shapiro–Wilk normality, Spearman correlation with severity,
   Kruskal–Wallis + one-way ANOVA + **eta-squared** effect size, chi-square + Cramer's V,
   and an **ordinal logistic regression** (odds ratios, 95% CI, p, pseudo-R²).
8. **Feature evaluation + selection** — mutual information + **LASSO** (L1 logistic) +
   **RFE**, combined into a consensus ranking; top-k selected.
9. **Balance** — class-balance report + deterministic random oversampling.
10. **Bias check** — fairness across **sex** and **age band**: per-group accuracy, TPR
    (equal opportunity) and selection rate (demographic parity), with gap verdicts.
11. **Baseline model** — 5-fold cross-validated AUC/accuracy (Logistic + Random Forest);
    the baseline the fusion must beat.

## 4. Secondary (EEG) pipeline

QC → preprocessing chain (band-pass, notch, re-reference, ICA, artifact reject, segment,
feature extract) → biomarker features + **10-20 channel → cortical region** mapping →
EDA → statistics (temporal-asymmetry Welch t-test + Cohen's d; band-power ANOVA by
severity; spike-rate Spearman) → **focus lateralisation** (Left vs Right) with a
**subject-level split** and cross-validated ROC-AUC.

## 5. Fusion + EP001 end-to-end

Links the two modalities by `patient_id`, quantifies the **incremental value** of fusion
(primary-only vs EEG-only vs fused CV-AUC), then runs the platform for **EP001**: primary
severity, EEG focus laterality + confidence, fused drug-resistance risk, and a transparent
rule-based recommendation **confirmed by the neurologist** (no autonomous diagnosis).

---

## 6. Headline results (from the committed run)

| Result | Value |
|---|---|
| Primary data-quality score | 0.998 |
| Primary drug-resistance AUC (baseline) | 0.969 |
| EEG focus-lateralisation AUC | 0.93 |
| Fusion AUC (primary + EEG) | 0.976 |
| EP001 | Severe · fused risk 0.59 · focus **Left Temporal** (conf 0.98) |

Numbers are regenerated on every `run_all.py`; the report docs embed them verbatim.

---

## 7. Outputs & mapping to the dissertation

- Datasets → `data/analysis/` (cohort + data dictionary + intermediate feature files).
- Figures → `analysis/outputs/<stage>/*.png`.
- Reports → `docs/analysis/primary-analysis.md`, `secondary-analysis.md`,
  `fusion-analysis.md` — each policy-compliant (captioned tables, four Mermaid diagram
  types, a **C4 model**, per-diagram Reason/Why/What/How/Reference, Defense Q&A, APA-7
  references).
- These map to the phased methodology in `docs/pipeline-a/` (primary) and
  `docs/pipeline-b/` (EEG), and to the platform vision in `docs/research-vision.md`.

## 8. Reproducibility & governance

- Single master seed (`common.SEED = 42`); every stochastic draw is seeded.
- Validation is kept separate from cleaning; every cleaning change is logged.
- Bias/fairness is audited before the model is reported.
- EP001 is predicted from a model trained on the **rest** of the cohort (no self-leakage).
