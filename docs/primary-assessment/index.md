# Primary Assessment — Index (Epilepsy, Patient EP001)

Epilepsy Primary Assessment dataset (pre-EEG), split into one MD file per assessment.
All data in table format. Two roles: **Neurologist** (clinical/primary) and **EEG
Technician** (acquisition/QC).

## Patient
| File | Contents |
|---|---|
| [Patient Summary](00-patient-summary.md) | Demographics for EP001 |

## Neurologist Assessment (Primary / Clinical)
| # | File | Section |
|---|---|---|
| 1 | [01-chief-complaint.md](neurologist/01-chief-complaint.md) | Chief Complaint |
| 2 | [02-history-present-illness.md](neurologist/02-history-present-illness.md) | History of Present Illness |
| 3 | [03-seizure-history.md](neurologist/03-seizure-history.md) | Seizure History |
| 4 | [04-aura.md](neurologist/04-aura.md) | Aura |
| 5 | [05-during-seizure.md](neurologist/05-during-seizure.md) | During Seizure |
| 6 | [06-post-ictal.md](neurologist/06-post-ictal.md) | Post-Ictal |
| 7 | [07-trigger-assessment.md](neurologist/07-trigger-assessment.md) | Trigger Assessment |
| 8 | [08-medication-history.md](neurologist/08-medication-history.md) | Medication History |
| 9 | [09-past-medical-history.md](neurologist/09-past-medical-history.md) | Past Medical History |
| 10 | [10-family-history.md](neurologist/10-family-history.md) | Family History |
| 11 | [11-lifestyle.md](neurologist/11-lifestyle.md) | Lifestyle |
| 12 | [12-neurological-examination.md](neurologist/12-neurological-examination.md) | Neurological Examination |
| 13 | [13-functional-assessment.md](neurologist/13-functional-assessment.md) | Functional Assessment |
| 14 | [14-quality-of-life.md](neurologist/14-quality-of-life.md) | Quality of Life |
| 15 | [15-impression.md](neurologist/15-impression.md) | Neurologist Impression |

## EEG Technician Assessment (Acquisition / QC)
| # | File | Section |
|---|---|---|
| 1 | [01-patient-preparation.md](eeg-technician/01-patient-preparation.md) | Patient Preparation |
| 2 | [02-eeg-setup.md](eeg-technician/02-eeg-setup.md) | EEG Setup |
| 3 | [03-electrode-quality.md](eeg-technician/03-electrode-quality.md) | Electrode Quality |
| 4 | [04-recording-conditions.md](eeg-technician/04-recording-conditions.md) | Recording Conditions |
| 5 | [05-artifact-risk.md](eeg-technician/05-artifact-risk.md) | Artifact Risk |
| 6 | [06-technician-notes.md](eeg-technician/06-technician-notes.md) | Technician Notes |

## Derived / Roles
| File | Contents |
|---|---|
| [ai-derived-features.md](ai-derived-features.md) | AI features derived before EEG |
| [roles-neurologist.md](roles-neurologist.md) | Neurologist: assessments, concerns, tasks |
| [roles-eeg-technician.md](roles-eeg-technician.md) | EEG Technician: assessments, concerns, tasks |
