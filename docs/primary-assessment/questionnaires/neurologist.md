# Neurologist — Patient Questionnaire (Consolidated, EP001)

> **Why (this doc):** The complete set of questions the Neurologist asks the patient, aggregated from every Neurologist assessment section into one enterprise form for intake, EMR entry, and AI feature extraction. **How:** auto-generated from the section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.

**Role:** Neurologist · **Sections:** 15 · **Total questions:** 103 · **ID prefix:** `NEU`


## Neurologist Assessment — Section 1: Chief Complaint

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0101 | What brings you in to see us today? | Text | free-text, 3-300 chars | Recurrent seizures over the last 18 months | chief_complaint_text |
| NEU-0102 | What is your single biggest concern right now? | Text | free-text, 3-200 chars | Increasing seizure frequency | primary_concern |
| NEU-0103 | How long has this problem been going on? | Number | 0-600 months | 18 months | problem_duration_months |
| NEU-0104 | On a scale of 0 to 10, how severe does this feel? | Severity(0-10) | 0-10 | 8/10 | severity_self_report |
| NEU-0105 | How many emergency visits have you had for this? | Number | 0-100 | 2 | emergency_visit_count |
| NEU-0106 | How many times have you been admitted to hospital? | Number | 0-100 | 1 | hospital_admission_count |
| NEU-0107 | What are you hoping we can achieve today? | Text | free-text, 3-200 chars | Better seizure control | patient_expectation |

## Neurologist Assessment — Section 2: History of Present Illness

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0201 | When did your very first seizure happen? | Date | ISO-8601 date | 2024-01-14 | first_seizure_date |
| NEU-0202 | How old were you when the first seizure occurred? | Number | 0-120 years | 27 | age_at_first_seizure |
| NEU-0203 | What happened during that first seizure? | Text | free-text, 3-300 chars | Sudden loss of awareness followed by right arm jerking | initial_presentation |
| NEU-0204 | Are your seizures becoming more frequent? | Yes-No | one-of[Yes | No | Occasionally] |
| NEU-0205 | Are you still having seizures despite treatment? | Yes-No | one-of[Yes | No | Rare] |
| NEU-0206 | Have you had any recent infection or illness? | Yes-No | one-of[Yes | No] | No |
| NEU-0207 | Has your medication been changed recently? | Yes-No | one-of[Yes | No] | Yes |

## Neurologist Assessment — Section 3: Seizure History

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0301 | What type of epilepsy have you been told you have? | Dropdown[Focal Epilepsy | Generalized Epilepsy | Combined | Unknown] |
| NEU-0302 | What type of seizures do you experience? | Dropdown[Focal Aware | Focal Impaired Awareness | Focal to Bilateral Tonic-Clonic | Generalized] |
| NEU-0303 | How often do your seizures happen? | Number | 0-300 per month | 5/month | seizure_freq_pm |
| NEU-0304 | How long does a typical seizure last? | Number | 0-3600 sec | 90 sec | avg_seizure_duration_sec |
| NEU-0305 | What is the longest seizure you have had? | Number | 0-3600 sec | 3 min | longest_seizure_sec |
| NEU-0306 | When was your most recent seizure? | Date | ISO-8601 date | 2026-06-18 | last_seizure_date |
| NEU-0307 | Do your seizures ever come in clusters? | Yes-No | one-of[Yes | No] | No |
| NEU-0308 | Have you ever had a seizure that would not stop? | Yes-No | one-of[Yes | No] | No |
| NEU-0309 | Do you have seizures during sleep or at night? | Dropdown[Yes | No | Occasional] | one-of[...] |
| NEU-0310 | Are your seizures usually seen by someone else? | Yes-No | one-of[Yes | No] | Yes |
| NEU-0311 | How do you keep track of your seizures? | Dropdown[Mobile App | Paper Diary | None | Inpatient EEG telemetry] |

## Neurologist Assessment — Section 4: Aura

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0401 | Do you get any warning before a seizure? | Dropdown[Yes | No | Occasional] | one-of[...] |
| NEU-0402 | Do you notice a metallic or unusual taste? | Dropdown[Yes | No | Occasional] | one-of[...] |
| NEU-0403 | Do you get a feeling of deja vu beforehand? | Yes-No | one-of[Yes | No] | Yes |
| NEU-0404 | Do you feel a sudden sense of fear? | Yes-No | one-of[Yes | No] | No |
| NEU-0405 | Do you see any visual changes or lights? | Yes-No | one-of[Yes | No] | No |
| NEU-0406 | Do you hear any unusual sounds? | Yes-No | one-of[Yes | No] | No |
| NEU-0407 | Do you have any trouble speaking beforehand? | Dropdown[None | Mild | Moderate | Global] |
| NEU-0408 | Do you feel any numbness or tingling, and where? | Dropdown[None | Left Hand | Right Hand | Face |

## Neurologist Assessment — Section 5: During Seizure

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0501 | Do you lose awareness during a seizure? | Yes-No | one-of[Yes | No] | Yes |
| NEU-0502 | Do you ever bite your tongue during a seizure? | Yes-No | one-of[Yes | No] | Yes |
| NEU-0503 | Do you lose control of your bladder during a seizure? | Yes-No | one-of[Yes | No] | No |
| NEU-0504 | Do your eyes turn to one side, and which way? | Dropdown[None | Left | Right] | one-of[...] |
| NEU-0505 | Which limb jerks or stiffens during a seizure? | Dropdown[None | Right Arm | Left Arm | Bilateral convulsive] |
| NEU-0506 | Does the seizure ever spread to a full-body convulsion? | Yes-No | one-of[Yes | No] | No |

## Neurologist Assessment — Section 6: Post-Ictal

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0601 | How long are you confused after a seizure? | Number | 0-1440 min | 20 min | postictal_confusion_min |
| NEU-0602 | Do you get a headache afterwards, and how bad? | Dropdown[None | Mild | Moderate | Severe] |
| NEU-0603 | How tired do you feel afterwards? | Dropdown[None | Mild | Moderate | Severe |
| NEU-0604 | Do you have any memory loss after a seizure? | Dropdown[None | Brief | Temporary | Prolonged] |
| NEU-0605 | How long until you feel back to normal? | Number | 0-1440 min | 45 min | recovery_time_min |

## Neurologist Assessment — Section 7: Trigger Assessment

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0701 | Do your seizures get worse when you lack sleep? | Yes-No | one-of[Yes | No] | Yes |
| NEU-0702 | Does general stress bring on your seizures? | Yes-No | one-of[Yes | No] | Yes |
| NEU-0703 | Do flashing or flickering lights trigger seizures? | Yes-No | one-of[Yes | No] | No |
| NEU-0704 | Does having a fever trigger your seizures? | Yes-No | one-of[Yes | No] | No |
| NEU-0705 | Does drinking alcohol trigger your seizures? | Dropdown[Yes | No | Occasionally] | one-of[...] |
| NEU-0706 | Do missed medication doses trigger seizures? | Yes-No | one-of[Yes | No] | Yes |
| NEU-0707 | Does emotional upset bring on your seizures? | Yes-No | one-of[Yes | No] | Yes |
| NEU-0708 | Does going without food (fasting) trigger seizures? | Yes-No | one-of[Yes | No] | No |

## Neurologist Assessment — Section 8: Medication History

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0801 | Which seizure medication are you taking now? | Text | free-text drug name, 2-100 chars | Levetiracetam | current_medication |
| NEU-0802 | What dose do you take and how often? | Text | dose + frequency, 2-50 chars | 1000 mg BID | medication_dose |
| NEU-0803 | How long have you been on this medication? | Number | 0-600 months | 12 months | medication_duration_months |
| NEU-0804 | What percentage of doses do you manage to take? | Percentage | 0-100% | 88% | adherence_pct |
| NEU-0805 | How many doses do you miss in a typical month? | Number | 0-100 per month | 3/month | missed_doses_pm |
| NEU-0806 | Do you notice any side effects from the medication? | Text | free-text, 0-200 chars | Irritability | side_effects |
| NEU-0807 | Do you have a rescue medication for emergencies? | Text | free-text drug name, 0-100 chars | Midazolam Nasal Spray | rescue_medication |
| NEU-0808 | Have any seizure medications failed you before? | Text | free-text drug name, 0-100 chars | Carbamazepine | previous_drug_failure |

## Neurologist Assessment — Section 9: Past Medical History

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0901 | Have you ever had a head injury or concussion? If so, when? | Dropdown[None, Mild concussion, Moderate TBI, Severe TBI] + Date | Allowed set; year 1900-present | Mild concussion (2019) | head_injury_history |
| NEU-0902 | Have you ever been told you had a stroke? | Yes-No | Yes/No | No | prior_stroke_flag |
| NEU-0903 | Have you ever been diagnosed with a brain tumor? | Yes-No | Yes/No | No | brain_tumor_flag |
| NEU-0904 | Have you had any infection of the brain or spinal cord (e.g., meningitis, encephalitis)? | Yes-No | Yes/No | No | cns_infection_flag |
| NEU-0905 | As a child, did you have seizures with fever (febrile seizures)? | Dropdown[No, Simple, Complex/prolonged] | Allowed set | No | febrile_seizure_history |
| NEU-0906 | Were you ever told you had developmental delay as a child? | Yes-No | Yes/No | No | developmental_delay_flag |

## Neurologist Assessment — Section 10: Family History

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-1001 | Does anyone in your family have epilepsy or seizures? If so, which relative? | Dropdown[None, First-degree, Second-degree, Distant] + Text | Allowed set; relative label | Maternal Uncle | family_epilepsy_relative |
| NEU-1002 | Does any close relative have migraines? | Dropdown[None, Mother, Father, Sibling, Other] | Allowed set | Mother | family_migraine_relative |
| NEU-1003 | Has any family member had a stroke? | Dropdown[None, First-degree, Second-degree, Grandparent] | Allowed set | None | family_stroke_relative |
| NEU-1004 | Is there any family history of dementia? | Dropdown[None, First-degree, Second-degree, Grandparent] | Allowed set | None | family_dementia_relative |

## Neurologist Assessment — Section 11: Lifestyle

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-1101 | On average, how many hours do you sleep per day? | Number | 0-24 hrs, 1 decimal | 5.2 hrs/day | sleep_hours_per_day |
| NEU-1102 | How would you rate your sleep quality? | Dropdown[Good, Fair, Poor, Very poor] | Allowed set | Poor | sleep_quality_rating |
| NEU-1103 | Do you smoke? | Yes-No | Yes/No | No | smoking_status |
| NEU-1104 | How often do you drink alcohol? | Dropdown[None, Occasional, Social, Heavy] | Allowed set | Social | alcohol_use_level |
| NEU-1105 | How often do you exercise? | Dropdown[None, Weekly, Twice/week, Daily] | Allowed set | Twice/week | exercise_frequency |
| NEU-1106 | How many cups of caffeinated drinks do you have per day? | Number | 0-20 cups/day | 4 cups/day | caffeine_cups_per_day |
| NEU-1107 | How would you rate your stress level at work? | Dropdown[Low, Moderate, High, Severe] | Allowed set | High | occupational_stress_level |

## Neurologist Assessment — Section 12: Neurological Examination

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-1201 | Mental status testing — are orientation, memory, and attention intact? | Dropdown[Normal, Abnormal, Post-ictal confusion/obtunded] | Allowed set | Normal | mental_status_exam |
| NEU-1202 | Cranial nerve examination — any deficit (e.g., gaze deviation)? | Dropdown[Normal, Abnormal, Gaze deviation] | Allowed set | Normal | cranial_nerve_exam |
| NEU-1203 | Motor examination — any weakness or paresis? | Dropdown[Normal, Abnormal, Todd's paresis] | Allowed set | Normal | motor_exam_result |
| NEU-1204 | Sensory examination — any sensory loss? | Dropdown[Normal, Reduced, Absent] | Allowed set | Normal | sensory_exam_result |
| NEU-1205 | Reflexes — are deep tendon reflexes normal and symmetric? | Dropdown[Normal, Mildly brisk, Asymmetric brisk] | Allowed set | Normal | reflex_exam_result |
| NEU-1206 | Coordination testing — any dysmetria or incoordination? | Dropdown[Normal, Impaired] | Allowed set | Normal | coordination_exam_result |
| NEU-1207 | Gait assessment — is walking steady and normal? | Dropdown[Normal, Unsteady, Unable] | Allowed set | Normal | gait_exam_result |
| NEU-1208 | Romberg test — does the patient sway or fall with eyes closed? | Dropdown[Negative, Positive, Untestable] | Allowed set | Negative | romberg_test_result |

## Neurologist Assessment — Section 13: Functional Assessment

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-1301 | What is your current driving status given your seizures? | Dropdown[Permitted, Conditional, Restricted, Prohibited] | Allowed set | Restricted | driving_status |
| NEU-1302 | How much has epilepsy affected your work or employment? | Dropdown[None, Mild, Moderate, Severe/unable to work] | Allowed set | Moderate | employment_impact_level |
| NEU-1303 | Can you manage basic daily self-care (bathing, dressing, eating) independently? | Dropdown[Independent, Assisted, Dependent] | Allowed set | Independent | adl_status |
| NEU-1304 | Can you manage complex daily tasks (finances, shopping, medication) independently? | Dropdown[Independent, Assisted, Dependent] | Allowed set | Independent | iadl_status |
| NEU-1305 | Has your productivity at work been affected? | Dropdown[Normal, Slightly reduced, Reduced, Severely impaired] | Allowed set | Reduced | work_productivity_level |
| NEU-1306 | How many falls have you had in the recent period? | Number | Integer 0-99 | 1 | fall_count |
| NEU-1307 | What is your overall risk of injury from seizures? | Dropdown[Low, Low-Moderate, Moderate, High] | Allowed set | Moderate | injury_risk_level |

## Neurologist Assessment — Section 14: Quality of Life

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-1401 | Based on the QOLIE-31 questionnaire, what is your overall quality-of-life score? | Number | Integer 0-100 | 56/100 | qolie31_composite_score |
| NEU-1402 | How would you rate your level of anxiety? | Dropdown[None, Mild, Moderate, Severe] | Allowed set | Mild | anxiety_level |
| NEU-1403 | How would you rate your level of depression or low mood? | Dropdown[None, Minimal, Mild, Moderate, Severe] | Allowed set | Mild | depression_level |
| NEU-1404 | How much does epilepsy limit your social activities? | Dropdown[None, Mild, Moderate, Severe] | Allowed set | Moderate | social_limitation_level |
| NEU-1405 | How would you rate your fatigue or energy levels? | Dropdown[Low, Moderate, High, Very high] | Allowed set | High | fatigue_level |

## Neurologist Assessment — Neurologist Impression

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-1501 | What is the integrated epilepsy diagnosis for this patient? | Text | Free text, clinician-entered | Drug-responsive focal epilepsy with breakthrough seizures | epilepsy_diagnosis |
| NEU-1502 | Is the patient a candidate for epilepsy surgery? | Dropdown[No, Yes (referral)] | Allowed set | No | surgical_candidate_flag |
| NEU-1503 | Is a brain MRI recommended? | Dropdown[No, Yes (3T epilepsy protocol)] | Allowed set | No | mri_recommended_flag |
| NEU-1504 | Is a repeat EEG required? | Dropdown[No, Optional, Yes, Yes (continuous video-EEG)] | Allowed set | Yes | repeat_eeg_flag |
| NEU-1505 | What medication adjustment is planned? | Text | Free text, clinician-entered | Increase Levetiracetam | medication_adjustment |
| NEU-1506 | When should the patient return for follow-up? | Dropdown[12 months, 6 months, 3 months, Emergency admission (days)] | Allowed set | 3 months | followup_interval |
