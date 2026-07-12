# Variable Dictionary — Dependent / Independent / Covariate + Statistical Type

> **Why (this doc):** A DBA/statistical analysis must declare, for every variable, its role (dependent, independent, covariate, identifier) and its statistical data type (continuous, ordinal, nominal, binary, count) — this determines which tests are valid. **How:** generated from the cohort by `analysis/build_var_dictionary.py`; source of truth is `data/analysis/variable_dictionary.csv`.

**Total variables:** 58 · primary 42 · secondary 16.

## Dependent variables (outcomes)

| variable | modality | owning_role | analysis_role | statistical_type |
|---|---|---|---|---|
| severity_level | primary | Target | dependent | ordinal |
| severity_label | primary | Target | dependent | nominal |
| drug_resistant | primary | Target | dependent | binary |
| focus_side | secondary(EEG) | Target | dependent | nominal |

## Covariates (potential confounders)

| variable | modality | owning_role | analysis_role | statistical_type |
|---|---|---|---|---|
| age | primary | Demographics | covariate | continuous |
| sex | primary | Demographics | covariate | nominal |
| employment | primary | Demographics | covariate | nominal |
| education | primary | Demographics | covariate | nominal |
| marital | primary | Demographics | covariate | nominal |

## Independent variables (predictors) — primary

| variable | modality | owning_role | analysis_role | statistical_type |
|---|---|---|---|---|
| neuro_seizure_freq_pm | primary | Neurologist | independent | continuous |
| neuro_awareness_impaired | primary | Neurologist | independent | binary |
| neuro_nocturnal | primary | Neurologist | independent | binary |
| neuro_duration_sec | primary | Neurologist | independent | continuous |
| neuro_aura | primary | Neurologist | independent | binary |
| neuro_postictal_min | primary | Neurologist | independent | continuous |
| neuro_trigger_burden | primary | Neurologist | independent | ordinal |
| eegtech_impedance_kohm | primary | EEG Technician | independent | continuous |
| eegtech_artifact_grade | primary | EEG Technician | independent | ordinal |
| eegtech_sleep_deprived | primary | EEG Technician | independent | binary |
| nurse_seizure_obs_pm | primary | Nurse | independent | continuous |
| nurse_injury_events | primary | Nurse | independent | count |
| nurse_rescue_med | primary | Nurse | independent | binary |
| nurse_sbp | primary | Nurse | independent | continuous |
| nurse_hr | primary | Nurse | independent | continuous |
| npsy_moca | primary | Neuropsychologist | independent | ordinal |
| npsy_verbal_mem_z | primary | Neuropsychologist | independent | continuous |
| npsy_naming_z | primary | Neuropsychologist | independent | continuous |
| npsy_gad7 | primary | Neuropsychologist | independent | ordinal |
| npsy_nddi_e | primary | Neuropsychologist | independent | ordinal |
| pharm_asm_count | primary | Pharmacist | independent | count |
| pharm_cbz_level | primary | Pharmacist | independent | continuous |
| pharm_adherence_pct | primary | Pharmacist | independent | continuous |
| pharm_interaction_flags | primary | Pharmacist | independent | count |
| pharm_tdm_urgency | primary | Pharmacist | independent | ordinal |
| care_witnessed_freq_pm | primary | Caregiver | independent | continuous |
| care_supervision | primary | Caregiver | independent | ordinal |
| care_zbi_burden | primary | Caregiver | independent | continuous |
| pt_qolie31 | primary | Patient | independent | continuous |
| pt_selfreport_adherence_pct | primary | Patient | independent | continuous |
| pt_side_effect_burden | primary | Patient | independent | ordinal |
| admin_encounter_acuity | primary | Administrator | independent | ordinal |
| admin_prior_admissions | primary | Administrator | independent | count |

## Independent variables (predictors) — secondary (EEG)

| variable | modality | owning_role | analysis_role | statistical_type |
|---|---|---|---|---|
| eeg_delta | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_theta | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_alpha | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_beta | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_gamma | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_left_temporal_pow | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_right_temporal_pow | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_temporal_asym | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_spike_rate_pm | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_focal_slowing | secondary(EEG) | Radiology/EEG (secondary) | independent | binary |
| eeg_entropy | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_paf_hz | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_connectivity | secondary(EEG) | Radiology/EEG (secondary) | independent | continuous |
| eeg_qc_grade | secondary(EEG) | Radiology/EEG (secondary) | independent | ordinal |

## Identifiers

| variable | modality | owning_role | analysis_role | statistical_type |
|---|---|---|---|---|
| patient_id | primary | Demographics | identifier | identifier |
| eeg_focus_channel | secondary(EEG) | Radiology/EEG (secondary) | identifier | nominal |
