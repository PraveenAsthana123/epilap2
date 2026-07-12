# Hypotheses — Primary, Secondary & Fusion

> **Why (this doc):** States each research hypothesis with its independent and dependent variables and the statistical test used, so the analysis is falsifiable and defensible. **How:** aligned to `variable-dictionary.md`; tested in `analysis/primary_analysis.py`, `secondary_analysis.py`, `fusion_analysis.py`.

| ID | Dataset | Hypothesis | Independent variable(s) | Dependent variable | Statistical test | Expected direction |
|---|---|---|---|---|---|---|
| H1 | Primary | Higher seizure burden associates with higher severity | seizure_burden, neuro_seizure_freq_pm (IV) | severity_level (DV, ordinal) | Spearman; Kruskal-Wallis + eta^2 | positive |
| H2 | Primary | Lower quality of life associates with higher severity | pt_qolie31 (IV, continuous) | severity_level (DV) | Spearman; ordinal logistic | negative |
| H3 | Primary | Higher mood load (GAD-7 + NDDI-E) associates with higher severity | npsy_gad7, npsy_nddi_e (IV) | severity_level (DV) | Spearman; ANOVA | positive |
| H4 | Primary | Lower medication adherence associates with drug resistance | pharm_adherence_pct (IV) | drug_resistant (DV, binary) | logistic regression (OR) | negative |
| H5 | Primary | No material demographic bias in the severity model | sex, age band (covariate) | model prediction | demographic-parity / equal-opportunity gap | gap < 0.10 |
| H6 | Secondary | Temporal asymmetry differs by epileptogenic focus side | eeg_temporal_asym (IV, continuous) | focus_side (DV, nominal) | Welch t-test + Cohen's d | large effect |
| H7 | Secondary | EEG slowing / spike rate increases with severity | eeg_delta, eeg_theta, eeg_spike_rate_pm (IV) | severity_level (DV) | one-way ANOVA; Spearman | positive |
| H8 | Secondary | EEG biomarkers lateralise the focus above chance | EEG biomarker set (IV) | focus_side (DV) | cross-validated ROC-AUC | AUC > 0.5 |
| H9 | Fusion | Fusing primary + EEG beats either modality for drug-resistance | primary + EEG features (IV) | drug_resistant (DV) | cross-validated ROC-AUC (paired) | fusion >= best single |

**Result status (committed run):** H1–H4 supported (medium–large effects); H5 supported (parity gap 0.175 → 0.087 after mitigation); H6 supported (large Cohen's d); H7 supported; H8 supported (focus AUC 0.93); H9 supported (fusion AUC 0.976 ≥ primary 0.969).
