# Exploratory Data Analysis (Each Dataset) + Class Balance + Accuracy Matrix

> **Why (this doc):** EDA of every generated dataset — shape, missingness, distributions, class
> balance, correlations — plus the accuracy matrix (confusion + per-class metrics) and detailed
> per-feature statistics vs the target. **How:** `analysis/eda.py`.

## Per-dataset EDA
### cohort_eeg

shape 500 x 17 · missing 0.0% · duplicates 0

| feature | mean | std | min | median | max |
|---|---|---|---|---|---|
| eeg_delta | 0.250 | 0.050 | 0.080 | 0.250 | 0.390 |
| eeg_theta | 0.230 | 0.050 | 0.070 | 0.230 | 0.380 |
| eeg_alpha | 0.280 | 0.060 | 0.100 | 0.280 | 0.460 |
| eeg_beta | 0.180 | 0.050 | 0.050 | 0.180 | 0.350 |
| eeg_gamma | 0.060 | 0.010 | 0.050 | 0.060 | 0.100 |
| eeg_left_temporal_pow | 1.270 | 0.330 | 0.320 | 1.290 | 2.310 |
| eeg_right_temporal_pow | 1.210 | 0.340 | 0.280 | 1.190 | 2.140 |
| eeg_temporal_asym | -0.030 | 0.240 | -0.780 | -0.020 | 0.580 |
| eeg_spike_rate_pm | 4.150 | 2.140 | 0.000 | 4.000 | 9.810 |
| eeg_focal_slowing | 0.480 | 0.500 | 0.000 | 0.000 | 1.000 |
| eeg_entropy | 1.340 | 0.240 | 0.540 | 1.340 | 2.000 |
| eeg_paf_hz | 9.830 | 1.010 | 6.680 | 9.820 | 13.000 |

**Class balance / low-cardinality columns:**

| column | distribution |
|---|---|
| eeg_focal_slowing | 0:0.52, 1:0.48 |
| eeg_qc_grade | 1:0.416, 2:0.384, 0:0.116, 3:0.084 |
| eeg_focus_channel | T7:0.252, T8:0.192, F7:0.19, P7:0.14, F8:0.118, P8:0.108 |
| focus_side | Left:0.582, Right:0.418 |
### cohort_primary

shape 500 x 42 · missing 0.38% · duplicates 0

| feature | mean | std | min | median | max |
|---|---|---|---|---|---|
| age | 40.200 | 25.070 | -5.000 | 39.000 | 500.000 |
| neuro_seizure_freq_pm | 5.790 | 6.620 | 0.000 | 3.550 | 45.700 |
| neuro_awareness_impaired | 0.590 | 0.490 | 0.000 | 1.000 | 1.000 |
| neuro_nocturnal | 0.440 | 0.500 | 0.000 | 0.000 | 1.000 |
| neuro_duration_sec | 80.800 | 49.310 | 5.000 | 78.500 | 258.000 |
| neuro_aura | 0.520 | 0.500 | 0.000 | 1.000 | 1.000 |
| neuro_postictal_min | 17.130 | 11.790 | 0.000 | 16.000 | 67.000 |
| neuro_trigger_burden | 2.070 | 1.350 | 0.000 | 2.000 | 4.000 |
| eegtech_impedance_kohm | 3.910 | 1.260 | 0.500 | 3.900 | 8.200 |
| eegtech_artifact_grade | 1.700 | 1.020 | 0.000 | 2.000 | 3.000 |
| eegtech_sleep_deprived | 0.720 | 0.450 | 0.000 | 1.000 | 1.000 |
| nurse_seizure_obs_pm | 4.880 | 5.560 | 0.000 | 2.900 | 41.700 |

**Class balance / low-cardinality columns:**

| column | distribution |
|---|---|
| sex | M:0.516, F:0.484 |
| employment | Employed:0.584, Unemployed:0.228, Student:0.1, Retired:0.088 |
| education | Bachelor:0.412, Secondary:0.39, Master:0.148, PhD:0.05 |
| marital | Single:0.454, Married:0.442, Divorced:0.104 |
| neuro_awareness_impaired | 1:0.592, 0:0.408 |
| neuro_nocturnal | 0:0.556, 1:0.444 |
| neuro_aura | 1:0.522, 0:0.478 |
| neuro_trigger_burden | 2:0.236, 3:0.222, 1:0.192, 4:0.186, 0:0.164 |
| eegtech_artifact_grade | 2:0.314, 1:0.274, 3:0.266, 0:0.146 |
| eegtech_sleep_deprived | 1:0.716, 0:0.284 |
### decisions

shape 500 x 9 · missing 0.0% · duplicates 0

| feature | mean | std | min | median | max |
|---|---|---|---|---|---|
| severity | 2.220 | 0.990 | 1.000 | 2.000 | 4.000 |
| drug_resist_p | 0.380 | 0.410 | 0.000 | 0.200 | 1.000 |

**Class balance / low-cardinality columns:**

| column | distribution |
|---|---|
| severity | 2:0.332, 1:0.284, 3:0.266, 4:0.118 |
| recurrence | High:0.334, Low:0.334, Medium:0.332 |
| focus | Left:0.582, Right:0.418 |
| confident | False:0.534, True:0.466 |
| concordance | Concordant:0.484, Discordant:0.304, Partial:0.212 |
| auto_recommendable | False:0.534, True:0.466 |
### epilepsy_scenarios

shape 57 x 9 · missing 0.19% · duplicates 0

| feature | mean | std | min | median | max |
|---|---|---|---|---|---|
| severity_level | 2.740 | 0.900 | 1.000 | 3.000 | 4.000 |
| clinical_weight | 0.860 | 0.280 | 0.300 | 0.900 | 1.500 |

**Class balance / low-cardinality columns:**

| column | distribution |
|---|---|
| category | Seizure Type:0.491, Clinical Scenario:0.263, Epilepsy Syndrome:0.175, Severity Level:0.07 |
| onset | Focal:0.393, Generalized:0.339, Any:0.143, -:0.071, Unknown:0.054 |
| awareness | Variable:0.526, Lost:0.175, Impaired:0.158, Aware:0.07, -:0.07 |
| severity_level | 2:0.351, 3:0.351, 4:0.228, 1:0.07 |
### recurrence

shape 500 x 5 · missing 0.0% · duplicates 0

| feature | mean | std | min | median | max |
|---|---|---|---|---|---|
| time_days | 125.690 | 117.150 | 0.000 | 81.200 | 365.000 |
| recurred | 0.910 | 0.290 | 0.000 | 1.000 | 1.000 |
| risk_score | 1.250 | 1.330 | 0.360 | 0.910 | 16.870 |

**Class balance / low-cardinality columns:**

| column | distribution |
|---|---|
| recurred | 1:0.91, 0:0.09 |
| risk_band | High:0.334, Low:0.334, Medium:0.332 |


## Correlation (primary cohort)
![correlation](analysis/outputs/eda/correlation.png)

## Class balance
![class balance](analysis/outputs/eda/class_balance.png)

Target imbalance (`drug_resistant`): {0: 0.616, 1: 0.384} — handled by SMOTE/ADASYN/class-weight in
`analysis/preprocessing.py` and the primary pipeline's balancing stage.

## Accuracy matrix (drug-resistance, holdout)
Accuracy **0.84** · ROC-AUC **0.912** · confusion matrix [[83, 9], [15, 43]]

![confusion](analysis/outputs/eda/confusion.png)

| class | precision | recall | f1 | support |
|---|---|---|---|---|
| Not-resistant (0) | 0.847 | 0.902 | 0.874 | 92 |
| Drug-resistant (1) | 0.827 | 0.741 | 0.782 | 58 |

## Detailed statistics — features vs target
*Caption - Group means by drug-resistance with Mann-Whitney U p-values and rank-biserial effect sizes.*

| feature | mean_not_resistant | mean_resistant | mannwhitney_p | effect_size_rbc |
|---|---|---|---|---|
| neuro_seizure_freq_pm | 3.510 | 9.450 | <0.001 | 0.574 |
| npsy_gad7 | 5.840 | 9.970 | <0.001 | 0.566 |
| pt_qolie31 | 75.340 | 57.210 | <0.001 | -0.615 |
| pharm_adherence_pct | 90.500 | 90.010 | <0.001 | -0.340 |
| npsy_moca | 27.220 | 24.510 | <0.001 | -0.539 |
| care_zbi_burden | 19.540 | 32.270 | <0.001 | 0.499 |

**Reason:** Characterise every dataset and quantify feature-target relationships. **Why:** EDA + balance + accuracy-matrix + effect sizes are prerequisites to trustworthy modelling. **What is happening:** Targets are imbalanced; key clinical features differ significantly by drug-resistance. **How it is happening:** Descriptives + Spearman + Mann-Whitney + confusion matrix computed from the data. **Reference:** Tukey (1977); Field (2018).

## References

Field, A. (2018). *Discovering statistics using IBM SPSS statistics* (5th ed.). Sage.

Tukey, J. W. (1977). *Exploratory data analysis*. Addison-Wesley.
