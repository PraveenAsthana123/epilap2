# EEG Technician — Patient Questionnaire (Consolidated, EP001)

> **Why (this doc):** The complete set of questions the EEG Technician asks the patient, aggregated from every EEG Technician assessment section into one enterprise form for intake, EMR entry, and AI feature extraction. **How:** auto-generated from the section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.

**Role:** EEG Technician · **Sections:** 6 · **Total questions:** 35 · **ID prefix:** `EEG`


## EEG Technician Assessment — Patient Preparation

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| EEG-0101 | Has the patient's identity been verified against wristband/records? | Yes-No | Yes/No; must be Yes to proceed | Yes | identity_verified |
| EEG-0102 | Has informed consent been signed for the EEG study? | Yes-No | Yes/No; must be Yes to proceed | Yes | consent_signed |
| EEG-0103 | Is this a sleep-deprived study? | Yes-No | Yes/No | Yes | sleep_deprived_study |
| EEG-0104 | Is the patient's hair clean and free of product? | Yes-No | Yes/No | Yes | hair_clean |
| EEG-0105 | Have all metal objects been removed? | Yes-No | Yes/No | Yes | metal_objects_removed |
| EEG-0106 | Has current anti-seizure medication been recorded? | Yes-No | Yes/No | Yes | medication_recorded |
| EEG-0107 | Has the date/time of last seizure been documented? | Yes-No | Yes/No | Yes | last_seizure_documented |
| EEG-0108 | What is the patient's pregnancy status? | Dropdown[Yes, No, N/A] | Allowed set: Yes/No/N/A | N/A | pregnancy_status |

## EEG Technician Assessment — EEG Setup

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| EEG-0201 | Which electrode placement system is used? | Dropdown[10–20 International, 10–10 Extended, High-density] | Allowed set | 10–20 International | electrode_system |
| EEG-0202 | How many electrodes are applied? | Number | Integer 19–256 | 21 | number_of_electrodes |
| EEG-0203 | What electrode cap size was fitted? | Dropdown[Small, Medium, Large] | Allowed set | Medium | electrode_cap_size |
| EEG-0204 | Which reference scheme is configured? | Dropdown[Linked Ears, Average, Cz, Bipolar] | Allowed set | Linked Ears | reference_scheme |
| EEG-0205 | What is the planned sampling rate? | Dropdown[256 Hz, 512 Hz, 1024 Hz] | Allowed set; ≥256 Hz | 512 Hz | sampling_rate_planned |
| EEG-0206 | What is the planned recording duration? | Number | Minutes; ≥20 min (or Continuous) | 30 min | recording_duration_min |

## EEG Technician Assessment — Electrode Quality

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| EEG-0301 | What is the measured impedance at Fp1? | Number | kΩ; target <5 kΩ | 3.2 kΩ | fp1_impedance_kohm |
| EEG-0302 | What is the measured impedance at Fp2? | Number | kΩ; target <5 kΩ | 3.1 kΩ | fp2_impedance_kohm |
| EEG-0303 | What is the measured impedance at F3? | Number | kΩ; target <5 kΩ | 2.9 kΩ | f3_impedance_kohm |
| EEG-0304 | What is the measured impedance at F4? | Number | kΩ; target <5 kΩ | 3.0 kΩ | f4_impedance_kohm |
| EEG-0305 | What is the average impedance across channels? | Read-only(Auto) | kΩ; mean of channels | 3.1 kΩ | average_impedance_kohm |
| EEG-0306 | Do all channels meet the <5 kΩ quality gate? | Yes-No | Yes/No; derived from channel values | Yes | all_channels_under_5kohm |

## EEG Technician Assessment — Recording Conditions

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| EEG-0401 | Is the patient awake at the start of recording? | Yes-No | Yes/No | Yes | awake_state |
| EEG-0402 | Is drowsiness expected during the recording? | Yes-No | Yes/No | Yes | drowsy_expected |
| EEG-0403 | Is sleep expected during the recording? | Yes-No | Yes/No | No | sleep_expected |
| EEG-0404 | Is hyperventilation planned as an activation procedure? | Yes-No | Yes/No | Yes | hyperventilation_planned |
| EEG-0405 | Is photic stimulation planned as an activation procedure? | Yes-No | Yes/No | Yes | photic_stimulation_planned |

## EEG Technician Assessment — Artifact Risk Assessment

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| EEG-0501 | What is the level of excess eye-blink artifact? | Dropdown[None, Mild, Moderate, Marked] | Allowed set | Mild | excess_eye_blink |
| EEG-0502 | What is the muscle artifact risk? | Dropdown[Low, Moderate, High] | Allowed set | Low | muscle_artifact_risk |
| EEG-0503 | Is sweating artifact present? | Yes-No | Yes/No | No | sweating_artifact |
| EEG-0504 | What is the level of electrode noise? | Dropdown[None, Low, Moderate, High] | Allowed set | None | electrode_noise |
| EEG-0505 | What is the movement artifact risk? | Dropdown[Low, Moderate, High] | Allowed set | Low | movement_risk |

## EEG Technician Assessment — Technician Notes

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| EEG-0601 | Was the patient cooperative during acquisition? | Text | Free text; ≤200 chars | Patient cooperative. | patient_cooperation_note |
| EEG-0602 | What was the electrode impedance quality? | Text | Free text; ≤200 chars | Good electrode impedance. | electrode_impedance_note |
| EEG-0603 | Was sleep deprivation status confirmed? | Text | Free text; ≤200 chars | Sleep deprivation confirmed. | sleep_deprivation_note |
| EEG-0604 | Were any technical issues anticipated? | Text | Free text; ≤200 chars | No technical issues anticipated. | technical_issues_note |
| EEG-0605 | What study type and activation procedures are the recording suitable for? | Text | Free text; ≤200 chars | Suitable for routine EEG with hyperventilation and photic stimulation. | study_suitability_note |
