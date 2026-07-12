# Primary Assessment — Index (Epilepsy, Patient EP001)

Epilepsy Primary Assessment dataset (pre-EEG), split into one MD file per assessment.
All data in table format. **Eight roles**, each with its own question set captured from that
role's point of view: **Neurologist**, **EEG Technician**, **Nurse**, **Neuropsychologist**,
**Pharmacist**, **Caregiver**, **Patient**, and **Administrator**.

Every assessment section also carries a **Severity Scenario Model** — the same questions
answered across four epilepsy severity levels from that role's perspective:

| Level | Name | Picture | Maps to |
|---|---|---|---|
| 1 | Mild | Well-controlled, rare seizures, monotherapy, no restrictions | — |
| 2 | Moderate | ~Monthly seizures, minor impact, mild QoL reduction | — |
| 3 | Severe | Several/month, breakthrough despite adherence, restrictions | **EP001** |
| 4 | Refractory / Status | Seizures every ~5 min (status epilepticus) — operational emergency | — |

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

## Nurse Assessment (Nursing / Observation)
| # | File | Section |
|---|---|---|
| 1 | [01-vital-signs-baseline.md](nurse/01-vital-signs-baseline.md) | Vital Signs & Baseline Observations |
| 2 | [02-seizure-observation-chart.md](nurse/02-seizure-observation-chart.md) | Seizure Observation Chart |
| 3 | [03-medication-administration.md](nurse/03-medication-administration.md) | Medication Administration & Adherence |
| 4 | [04-injury-safety-screen.md](nurse/04-injury-safety-screen.md) | Injury & Safety Screen |
| 5 | [05-patient-education.md](nurse/05-patient-education.md) | Patient Education & Self-Management |
| 6 | [06-psychosocial-support-screen.md](nurse/06-psychosocial-support-screen.md) | Psychosocial & Support Screen |
| 7 | [07-care-plan-handover.md](nurse/07-care-plan-handover.md) | Care Plan & Handover Notes |

## Neuropsychologist Assessment (Cognitive)
| # | File | Section |
|---|---|---|
| 1 | [01-cognitive-screening.md](neuropsychologist/01-cognitive-screening.md) | Cognitive Screening |
| 2 | [02-memory-assessment.md](neuropsychologist/02-memory-assessment.md) | Memory Assessment |
| 3 | [03-attention-processing-speed.md](neuropsychologist/03-attention-processing-speed.md) | Attention & Processing Speed |
| 4 | [04-executive-function.md](neuropsychologist/04-executive-function.md) | Executive Function |
| 5 | [05-language-naming.md](neuropsychologist/05-language-naming.md) | Language & Naming |
| 6 | [06-mood-anxiety.md](neuropsychologist/06-mood-anxiety.md) | Mood & Anxiety |
| 7 | [07-quality-of-life-psychosocial.md](neuropsychologist/07-quality-of-life-psychosocial.md) | Quality of Life & Psychosocial |
| 8 | [08-neuropsychological-impression.md](neuropsychologist/08-neuropsychological-impression.md) | Neuropsychological Impression |

## Pharmacist Assessment (Medication)
| # | File | Section |
|---|---|---|
| 1 | [01-medication-reconciliation.md](pharmacist/01-medication-reconciliation.md) | Medication Reconciliation |
| 2 | [02-asm-regimen-review.md](pharmacist/02-asm-regimen-review.md) | ASM Regimen Review |
| 3 | [03-adherence-assessment.md](pharmacist/03-adherence-assessment.md) | Adherence Assessment |
| 4 | [04-drug-interaction-screen.md](pharmacist/04-drug-interaction-screen.md) | Drug Interaction Screen |
| 5 | [05-adverse-effect-review.md](pharmacist/05-adverse-effect-review.md) | Adverse-Effect Review |
| 6 | [06-therapeutic-drug-monitoring.md](pharmacist/06-therapeutic-drug-monitoring.md) | Therapeutic Drug Monitoring |
| 7 | [07-counselling-care-plan.md](pharmacist/07-counselling-care-plan.md) | Counselling & Care Plan |

## Caregiver Assessment (Observer-Reported)
| # | File | Section |
|---|---|---|
| 1 | [01-witnessed-seizure-description.md](caregiver/01-witnessed-seizure-description.md) | Witnessed Seizure Description |
| 2 | [02-seizure-frequency-diary.md](caregiver/02-seizure-frequency-diary.md) | Seizure Frequency & Diary |
| 3 | [03-nocturnal-unwitnessed-events.md](caregiver/03-nocturnal-unwitnessed-events.md) | Nocturnal / Unwitnessed Events |
| 4 | [04-trigger-observations.md](caregiver/04-trigger-observations.md) | Trigger Observations |
| 5 | [05-medication-support.md](caregiver/05-medication-support.md) | Medication Support at Home |
| 6 | [06-safety-supervision.md](caregiver/06-safety-supervision.md) | Safety & Supervision |
| 7 | [07-caregiver-burden-wellbeing.md](caregiver/07-caregiver-burden-wellbeing.md) | Caregiver Burden & Wellbeing |

## Patient Self-Report (Patient-Reported Outcomes)
| # | File | Section |
|---|---|---|
| 1 | [01-symptom-self-report.md](patient/01-symptom-self-report.md) | Symptom Self-Report |
| 2 | [02-seizure-diary-self.md](patient/02-seizure-diary-self.md) | Seizure Diary (Self) |
| 3 | [03-medication-adherence-self.md](patient/03-medication-adherence-self.md) | Medication Adherence Self-Report |
| 4 | [04-trigger-lifestyle-self.md](patient/04-trigger-lifestyle-self.md) | Trigger & Lifestyle Self-Report |
| 5 | [05-side-effect-self-report.md](patient/05-side-effect-self-report.md) | Side-Effect Self-Report |
| 6 | [06-quality-of-life-qolie31.md](patient/06-quality-of-life-qolie31.md) | Quality of Life (QOLIE-31) |
| 7 | [07-mood-anxiety-self.md](patient/07-mood-anxiety-self.md) | Mood & Anxiety Self-Report |
| 8 | [08-goals-concerns.md](patient/08-goals-concerns.md) | Goals & Concerns |

## Administrator Assessment (Administrative)
| # | File | Section |
|---|---|---|
| 1 | [01-registration-demographics.md](administrator/01-registration-demographics.md) | Registration & Demographics |
| 2 | [02-insurance-consent.md](administrator/02-insurance-consent.md) | Insurance & Consent |
| 3 | [03-appointment-scheduling.md](administrator/03-appointment-scheduling.md) | Appointment Scheduling |
| 4 | [04-encounter-coding.md](administrator/04-encounter-coding.md) | Encounter & Coding |
| 5 | [05-records-data-governance.md](administrator/05-records-data-governance.md) | Records & Data Governance |
| 6 | [06-referral-management.md](administrator/06-referral-management.md) | Referral Management |

## Occupational Therapist Assessment (Functional / Rehabilitation)
| # | File | Section |
|---|---|---|
| 1 | [01-referral-information.md](occupational-therapist/01-referral-information.md) | Referral Information (OT001–010) |
| 2 | [02-occupational-profile.md](occupational-therapist/02-occupational-profile.md) | Occupational Profile (OT011–020) |
| 3 | [03-patient-priorities.md](occupational-therapist/03-patient-priorities.md) | Patient Priorities (OT021–030) |
| 4 | [04-functional-concerns.md](occupational-therapist/04-functional-concerns.md) | Functional Concerns (OT031–040) |
| 5 | [05-seizure-impact.md](occupational-therapist/05-seizure-impact.md) | Seizure Impact on Daily Life (OT041–050) |
| 6 | [06-safety-screening.md](occupational-therapist/06-safety-screening.md) | Initial Safety Screening (OT051–060) |
| 7 | [07-clinical-impression.md](occupational-therapist/07-clinical-impression.md) | Initial Clinical Impression (OT061–070) |

## Radiologist Assessment (Imaging / Secondary)
| # | File | Section |
|---|---|---|
| 1 | [01-imaging-referral.md](radiologist/01-imaging-referral.md) | Imaging Referral (RAD001) |
| 2 | [02-mri-brain.md](radiologist/02-mri-brain.md) | MRI Brain |
| 3 | [03-ct-brain.md](radiologist/03-ct-brain.md) | CT Brain |
| 4 | [04-advanced-imaging.md](radiologist/04-advanced-imaging.md) | Advanced Imaging (PET/SPECT/fMRI/MEG) |
| 5 | [05-lesion-localization.md](radiologist/05-lesion-localization.md) | Lesion → Epileptogenic-Zone Concordance |
| 6 | [06-radiology-impression.md](radiologist/06-radiology-impression.md) | Radiology Impression |

## Derived / Roles
| File | Contents |
|---|---|
| [ai-derived-features.md](ai-derived-features.md) | AI features derived before EEG |
| [roles-radiologist.md](roles-radiologist.md) | Radiologist: imaging assessments, pain points, tasks |
| [roles-neurologist.md](roles-neurologist.md) | Neurologist: assessments, concerns, tasks |
| [roles-eeg-technician.md](roles-eeg-technician.md) | EEG Technician: assessments, concerns, tasks |
| [roles-nurse.md](roles-nurse.md) | Nurse: assessments, concerns, tasks |
| [roles-neuropsychologist.md](roles-neuropsychologist.md) | Neuropsychologist: assessments, concerns, tasks |
| [roles-pharmacist.md](roles-pharmacist.md) | Pharmacist: assessments, concerns, tasks |
| [roles-caregiver.md](roles-caregiver.md) | Caregiver: observations, concerns, tasks |
| [roles-patient.md](roles-patient.md) | Patient: self-reports, concerns, tasks |
| [roles-administrator.md](roles-administrator.md) | Administrator: tasks, concerns, workflow |
| [roles-occupational-therapist.md](roles-occupational-therapist.md) | Occupational Therapist: assessments, participation map, tasks |
