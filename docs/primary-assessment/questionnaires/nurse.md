# Nurse — Patient Questionnaire (Consolidated, EP001)

> **Why (this doc):** The complete set of questions the Nurse asks the patient, aggregated from every Nurse assessment section into one enterprise form for intake, EMR entry, and AI feature extraction. **How:** auto-generated from the section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.

**Role:** Nurse · **Sections:** 7 · **Total questions:** 96 · **ID prefix:** `NUR`


## Nurse Assessment — Section 1: Vital Signs & Baseline Observations

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NUR-0101 | What is the patient's blood pressure? | Text | Format ###/## mmHg (systolic 70-220 / diastolic 40-130) | 124/78 mmHg | blood_pressure_reading |
| NUR-0102 | What is the patient's heart rate? | Number | 30-220 bpm | 72 bpm | heart_rate_bpm |
| NUR-0103 | What is the patient's temperature? | Number | 34.0-42.0 C | 36.7 C | body_temperature_c |
| NUR-0104 | What is the patient's oxygen saturation (SpO2)? | Number | 50-100 % | 98% | oxygen_saturation_pct |
| NUR-0105 | What is the patient's respiratory rate? | Number | 4-60 /min | 16 /min | respiratory_rate |
| NUR-0106 | What is the NEWS2 aggregate score? | Read-only (Auto) | 0-20 (derived from vitals) | 0 (Low) | news2_aggregate_score |
| NUR-0107 | What is the patient's weight? | Number | 20-300 kg | 78 kg | body_weight_kg |
| NUR-0108 | What is the patient's height? | Number | 100-250 cm | 178 cm | body_height_cm |
| NUR-0109 | What is the patient's BMI? | Read-only (Auto) | 10.0-70.0 (weight/height derived) | 24.6 (Normal) | body_mass_index |
| NUR-0110 | What is the patient's pain score? | Severity(0-10) | Integer 0-10 | 2 (post-ictal headache) | pain_score_0_10 |
| NUR-0111 | What is the patient's level of consciousness (ACVPU)? | Dropdown[Alert, Confusion, Voice, Pain, Unresponsive] | Allowed set only | Alert | acvpu_consciousness_level |
| NUR-0112 | What is the capillary blood glucose? | Number | 1.0-30.0 mmol/L | 5.4 mmol/L | capillary_blood_glucose |

## Nurse Assessment — Section 2: Seizure Observation Chart

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NUR-0201 | When did the observed seizure event occur (date/time)? | Date | ISO datetime YYYY-MM-DD HH:MM | 2026-07-10 03:14 | event_datetime |
| NUR-0202 | What seizure type was observed? | Dropdown[Focal Aware, Focal Impaired Awareness, Focal to Bilateral Tonic-Clonic, Generalized, Not observed] | Allowed set only | Focal Impaired Awareness | observed_seizure_type |
| NUR-0203 | What onset lateralization signs were seen? | Text | Free text (<=120 chars) | Left temporal (right-hand automatisms) | onset_lateralization_signs |
| NUR-0204 | What was the observed seizure duration? | Number | 1-3600 sec | 85 sec | seizure_duration_sec |
| NUR-0205 | Was an aura reported before the event? | Text | Free text or "None" | Metallic taste, déjà vu | pre_ictal_aura |
| NUR-0206 | What motor features were observed? | Text | Free text or "None observed" | Lip-smacking, right-hand fumbling | motor_features |
| NUR-0207 | What was the awareness level during the event? | Dropdown[Preserved, Partially preserved, Impaired, Absent] | Allowed set only | Impaired (unresponsive to voice) | ictal_awareness_level |
| NUR-0208 | Was there head or eye deviation, and which way? | Dropdown[None, Rightward, Leftward, Sustained rightward, Sustained leftward] | Allowed set only | Rightward | head_eye_deviation |
| NUR-0209 | Was there incontinence during the seizure? | Yes-No | Yes or No | No | ictal_incontinence |
| NUR-0210 | Was there tongue or cheek biting? | Dropdown[No, Lateral (minor), Deep lateral] | Allowed set only | Lateral (minor) | tongue_biting |
| NUR-0211 | What was the post-ictal recovery duration? | Number | 0-1440 min (or "No return to baseline") | 12 min | post_ictal_duration_min |
| NUR-0212 | What was the lowest peri-ictal SpO2? | Number | 50-100 % | 93% | peri_ictal_spo2_lowest |
| NUR-0213 | Was the recovery position applied? | Yes-No | Yes or No / Not required | Yes | recovery_position_applied |
| NUR-0214 | Who witnessed the event? | Text | Free text (role/name) | Night-shift nurse | witnessed_by |

## Nurse Assessment — Section 3: Medication Administration & Adherence Check

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NUR-0301 | What is the first ASM and dose? | Text | Drug name + dose + frequency | Carbamazepine 400 mg BID | asm_1_regimen |
| NUR-0302 | What is the second ASM and dose? | Text | Drug name + dose + frequency, or "None" | Levetiracetam 500 mg BID | asm_2_regimen |
| NUR-0303 | What is the administration route? | Dropdown[Oral, IV, Buccal, IV / buccal] | Allowed set only | Oral | administration_route |
| NUR-0304 | Was the morning dose given (and when)? | Yes-No | Yes/No + time HH:MM (or Withheld) | Yes (08:00) | morning_dose_given |
| NUR-0305 | Was the evening dose given (and when)? | Yes-No | Yes/No + time HH:MM (or Withheld) | Yes (20:00) | evening_dose_given |
| NUR-0306 | How many doses were missed in the last 30 days? | Number | 0-60 | 7 | doses_missed_30d |
| NUR-0307 | What is the measured adherence percentage? | Number | 0-100 % | 88% | measured_adherence_pct |
| NUR-0308 | What method was used to assess adherence? | Dropdown[Self-report, Pill count + self-report, Self-report + app reminder, Emergency medication chart] | Allowed set only | Pill count + self-report | adherence_method |
| NUR-0309 | What was the last serum ASM level check? | Text | Drug + level (mg/L) + interpretation | Carbamazepine 7.2 mg/L (therapeutic) | last_serum_level |
| NUR-0310 | What side effects were reported? | Text | Free text or "None" | Dizziness, mild drowsiness | reported_side_effects |
| NUR-0311 | What PRN/rescue medication is in place? | Text | Drug + status (available/given) | Buccal midazolam (available, not used) | prn_rescue_medication |
| NUR-0312 | What are the barriers to adherence? | Text | Free text or "None" | Shift work, forgetfulness | adherence_barriers |
| NUR-0313 | Is the patient capable of self-administration? | Dropdown[Yes (independent), Yes (supervised), No (fully dependent)] | Allowed set only | Yes (supervised) | self_admin_capable |

## Nurse Assessment — Section 4: Injury & Safety Screen

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NUR-0401 | How many falls occurred in the last 12 months? | Number | 0-100 | 1 | falls_12m_count |
| NUR-0402 | What was the severity of fall injury? | Dropdown[None, Moderate, High] | Allowed set only | Moderate (bruising, no fracture) | fall_injury_severity |
| NUR-0403 | Is there tongue or cheek biting? | Dropdown[No, Occasional (minor), Yes (lateral, minor), Deep lateral] | Allowed set only | Yes (lateral, minor) | tongue_cheek_biting |
| NUR-0404 | Is there incontinence during seizures? | Yes-No | Yes or No | No | seizure_incontinence |
| NUR-0405 | Is there a history of burns or scalds? | Yes-No | Yes / No / Under review | No | burns_scalds_history |
| NUR-0406 | Has there been a head injury from a seizure? | Yes-No | Yes or No | No | seizure_head_injury |
| NUR-0407 | What is the overall injury risk rating? | Dropdown[Low, Low-Moderate, Moderate, Very High] | Allowed set only | Moderate | injury_risk_rating |
| NUR-0408 | What is the Morse Fall Scale score? | Number | 0-125 | 45 (Moderate) | morse_fall_scale_score |
| NUR-0409 | What bed rails or padding are in place? | Text | Free text | Padded rails in place | bed_rails_padding |
| NUR-0410 | What supervision level is assigned? | Dropdown[Routine, Standard, Intermittent (15-min checks), Continuous 1:1] | Allowed set only | Intermittent (15-min checks) | supervision_level |
| NUR-0411 | What is the patient's driving status? | Dropdown[Permitted, Conditional, Restricted, Prohibited] | Allowed set only | Restricted | driving_status |
| NUR-0412 | Is bathing supervision advised? | Yes-No | Yes/No + note (shower vs bath) | Yes (shower, not bath) | bathing_supervision_advised |
| NUR-0413 | Was SUDEP risk discussed? | Yes-No | Yes or No | Yes | sudep_risk_discussed |
| NUR-0414 | Was the safe-environment checklist completed? | Dropdown[Completed, Emergency safety measures active] | Allowed set only | Completed | safe_environment_checklist |

## Nurse Assessment — Section 5: Patient Education

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NUR-0501 | Was seizure first-aid taught? | Yes-No | Yes/No + detail | Yes (recovery position, timing, when to call) | seizure_first_aid_taught |
| NUR-0502 | Was trigger avoidance discussed? | Yes-No | Yes/No + detail | Yes (sleep, stress, missed meds) | trigger_avoidance_discussed |
| NUR-0503 | Was sleep hygiene education given? | Yes-No | Yes/No + target vs current hrs | Yes (target 7-8 hrs; currently 5.2 hrs) | sleep_hygiene_education |
| NUR-0504 | Was medication adherence coaching provided? | Yes-No | Yes/No + method | Yes (alarms, pill organizer) | adherence_coaching |
| NUR-0505 | Was rescue medication training delivered? | Text | Drug + method, or "Not required" | Buccal midazolam demonstrated | rescue_medication_training |
| NUR-0506 | Were driving regulations explained? | Yes-No | Yes/No + status | Yes (restriction understood) | driving_regulations_explained |
| NUR-0507 | Was seizure diary training provided? | Text | Method (app/paper), or "Optional" | Mobile app reinforced | seizure_diary_training |
| NUR-0508 | Was aura recognition education given? | Text | Free text or "Not applicable" | Metallic taste, déjà vu as warning | aura_recognition_education |
| NUR-0509 | Was alcohol/caffeine advice provided? | Yes-No | Provided / Deferred | Provided | alcohol_caffeine_advice |
| NUR-0510 | What teaching method was used? | Dropdown[Verbal + leaflet, Verbal + written leaflet, Verbal + written leaflet + teach-back, Family briefing + emergency instruction] | Allowed set only | Verbal + written leaflet + teach-back | teaching_method |
| NUR-0511 | What was the teach-back comprehension level? | Dropdown[Good, Adequate, Caregiver confirms emergency steps] | Allowed set only | Adequate | teach_back_comprehension |
| NUR-0512 | What educational materials were given? | Text | Free text | Epilepsy self-management booklet | educational_materials_given |
| NUR-0513 | Was the caregiver/spouse included? | Yes-No | Yes / No / Optional | Yes (wife present) | caregiver_included |
| NUR-0514 | What follow-up education is needed? | Text | Free text | Sleep and stress management | follow_up_education_needed |

## Nurse Assessment — Section 6: Psychosocial Support Screen

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NUR-0601 | What is the PHQ-2 mood screen score? | Number | 0-6 | 2 (mild low mood) | phq2_mood_score |
| NUR-0602 | What is the GAD-2 anxiety screen score? | Number | 0-6 | 3 (mild anxiety) | gad2_anxiety_score |
| NUR-0603 | What is the reported stress level? | Dropdown[Low, Moderate, High] | Allowed set only | High (work + seizure worry) | reported_stress_level |
| NUR-0604 | What is the patient's coping style? | Text | Free text | Problem-focused, some avoidance | coping_style |
| NUR-0605 | What is the employment impact? | Text | Free text or "None" | Software engineer; concentration concerns | employment_impact |
| NUR-0606 | What is the marital/social support status? | Text | Free text | Married; supportive spouse | marital_social_support |
| NUR-0607 | What is the level of perceived stigma? | Dropdown[Low, Mild, Moderate, High] | Allowed set only | Moderate (discloses selectively) | perceived_stigma |
| NUR-0608 | What is the impact of driving loss? | Dropdown[None, Moderate, Significant, Prohibited] | Allowed set only | Significant (independence, commute) | driving_loss_impact |
| NUR-0609 | Is there sleep-related distress? | Yes-No | Yes/No + detail | Yes (5.2 hrs, worry-driven) | sleep_related_distress |
| NUR-0610 | What is the level of social isolation? | Dropdown[None, Low, Moderate, High] | Allowed set only | Low | social_isolation |
| NUR-0611 | What was the suicidal ideation screen result? | Dropdown[Negative, Positive, Deferred] | Allowed set only | Negative | suicidal_ideation_screen |
| NUR-0612 | Was a support group referral offered? | Yes-No | Offered / Not required / Planned | Offered (epilepsy peer group) | support_group_referral |
| NUR-0613 | Is a psychology referral needed? | Dropdown[No, Monitor, Consider, Yes] | Allowed set only | Consider (mood + stress) | psychology_referral_needed |
| NUR-0614 | Was QOLIE-31 referenced? | Yes-No | Yes / Deferred | Yes | qolie31_referenced |

## Nurse Assessment — Section 7: Care Plan & Shift Handover

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NUR-0701 | What handover format is used? | Dropdown[SBAR, SBAR + emergency escalation] | Allowed set only | SBAR | handover_format |
| NUR-0702 | What is the Situation summary? | Text | Free text (<=160 chars) | 29M, focal impaired-awareness epilepsy, breakthrough seizures | sbar_situation |
| NUR-0703 | What is the Background summary? | Text | Free text (<=160 chars) | Left-temporal onset; CBZ + LEV; 88% adherence | sbar_background |
| NUR-0704 | What is the Assessment this shift? | Text | Free text (<=160 chars) | 1 observed seizure this shift; vitals stable | sbar_assessment |
| NUR-0705 | What is the Recommendation? | Text | Free text (<=160 chars) | Continue 15-min checks; monitor SpO2 | sbar_recommendation |
| NUR-0706 | What are the active nursing diagnoses? | Text | Free text | Risk of injury; risk of ineffective coping | active_nursing_diagnoses |
| NUR-0707 | What seizure precautions are in place? | Text | Free text | Padded rails, recovery position, suction ready | seizure_precautions |
| NUR-0708 | What is the monitoring frequency? | Text | Free text | 15-min visual + hourly vitals overnight | monitoring_frequency |
| NUR-0709 | What medications are due next shift? | Text | Drug + dose + time | CBZ 400 mg + LEV 500 mg at 20:00 | medications_due_next_shift |
| NUR-0710 | What is the rescue plan? | Text | Free text | Buccal midazolam if seizure > 5 min | rescue_plan |
| NUR-0711 | What outstanding tasks remain? | Text | Free text | Sleep-hygiene follow-up; psychology referral | outstanding_tasks |
| NUR-0712 | What falls precaution is in place? | Text | Morse score + measure | Morse 45; call bell in reach | falls_precaution |
| NUR-0713 | What are the escalation criteria? | Text | Free text | NEWS2 >= 3, cluster, or status | escalation_criteria |
| NUR-0714 | Was the family updated? | Yes-No | Yes or No + who | Yes (spouse) | family_updated |
| NUR-0715 | Was the care plan reviewed this shift? | Yes-No | Yes / Emergency care plan active | Yes (this shift) | care_plan_reviewed |
