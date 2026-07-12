# Caregiver — Patient Questionnaire (Consolidated, EP001)

> **Why (this doc):** The complete set of questions the Caregiver asks the patient, aggregated from every Caregiver assessment section into one enterprise form for intake, EMR entry, and AI feature extraction. **How:** auto-generated from the section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.

**Role:** Caregiver · **Sections:** 7 · **Total questions:** 84 · **ID prefix:** `CAR`


## Caregiver Assessment — Section 1: Witnessed Seizure Semiology Description

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| CAR-101 | What is your relationship to the patient? | Dropdown[Spouse/Parent/Sibling/Child/Friend/Other] | Allowed set | Spouse (lives with patient) | observer_relationship |
| CAR-102 | How many of the patient's seizures have you personally witnessed? | Dropdown[None/Some/Yes (majority)/All] | Allowed set | Yes (majority) | witnessed_event_proportion |
| CAR-103 | What does the patient do at the very start of a seizure? | Text | Free text ≤200 chars | Sudden behavioral arrest / staring | onset_behavior_pattern |
| CAR-104 | What repetitive movements do you see during the event? | Text | Free text ≤200 chars | Lip-smacking, hand fumbling | automatism_detection |
| CAR-105 | Is the patient aware or responsive during the event? | Dropdown[Retained/Partially impaired/Impaired] | Allowed set | Impaired (unresponsive to name) | awareness_impairment_level |
| CAR-106 | How do you test whether the patient responds during an event? | Text | Free text ≤200 chars | Calls name, touches arm — no response | responsiveness_test_method |
| CAR-107 | How long does a typical seizure last (seconds)? | Number | 0–600 sec | ~90 sec | typical_duration_seconds |
| CAR-108 | Does the event ever spread to whole-body jerking? | Dropdown[Never/Rare/Occasional/Frequent] | Allowed set | Occasional (bilateral jerking) | secondary_generalization_flag |
| CAR-109 | Do the eyes or head turn to one side during the event? | Dropdown[None/Occasional/Frequent] | Allowed set | Head turns to right at times | head_eye_deviation |
| CAR-110 | Does the patient make any sounds during the event? | Dropdown[None/Occasional/Frequent] | Allowed set | Occasional low mumbling | vocalization_pattern |
| CAR-111 | How does the patient behave after the event, and for how long? | Text | Free text ≤200 chars | Confusion and fatigue ~10–20 min | postictal_state_profile |
| CAR-112 | How many injuries or falls have occurred during events? | Number | 0–99 | 1 fall to date | event_injury_count |

## Caregiver Assessment — Section 2: Home Seizure Frequency & Diary

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| CAR-201 | How do you record seizure events? | Dropdown[Mobile app/Notebook/App + notebook/Occasional note] | Allowed set | Shared mobile app + bedside notebook | diary_capture_method |
| CAR-202 | How soon after an event do you log it? | Dropdown[Per event same day/Per event/As needed/Weekly] | Allowed set | Per event, same day | logging_latency |
| CAR-203 | On average, how many seizures occur per month? | Number | 0–100 | 5/month | monthly_seizure_count |
| CAR-204 | How many daytime events are logged per month? | Number | 0–100 | ~2/month | daytime_event_count |
| CAR-205 | How many nocturnal events are logged per month? | Number | 0–100 | ~3/month | nocturnal_event_count |
| CAR-206 | What is the longest seizure-free gap (days)? | Number | 0–3650 | 11 days | longest_seizure_free_gap |
| CAR-207 | How often do seizures cluster on a single day? | Dropdown[None/Rare/Occasional/Frequent] | Allowed set | Rare (1 in last 3 months) | cluster_day_frequency |
| CAR-208 | At what time of day do events most often occur? | Text | Free text ≤200 chars | Often early morning / on waking | event_time_pattern |
| CAR-209 | How often is a missed dose linked to an event? | Text | Free text ≤200 chars | Noted on 2 of last 5 events | missed_dose_correlation |
| CAR-210 | What percentage of events do you manage to log? | Number | 0–100 % | High (≈95% of events) | diary_adherence_rate |
| CAR-211 | What is the date of the most recent logged event? | Date | YYYY-MM-DD | 2026-06-18 | last_event_date |
| CAR-212 | Who do you share the diary with? | Dropdown[Neurologist/GP/Emergency services/None] | Allowed set | Neurologist at visits | diary_sharing_target |

## Caregiver Assessment — Section 3: Nocturnal / Suspected Unwitnessed Events

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| CAR-301 | Does the patient have seizures during sleep? | Yes-No | Yes/No | Yes | nocturnal_seizure_present |
| CAR-302 | Do you wake to witness night-time seizures, and how often? | Dropdown[None/Occasionally/Yes (some)/Yes (most)] | Allowed set | Yes (spouse wakes to some) | nocturnal_witness_rate |
| CAR-303 | Do you suspect seizures you did not directly see? | Yes-No | Yes/No | Yes (indirect signs) | unwitnessed_event_suspected |
| CAR-304 | What morning signs suggest a night-time seizure? | Text | Free text ≤200 chars | Bitten tongue, sore muscles, wet pillow | indirect_morning_signs |
| CAR-305 | What bedding disturbance do you notice after an event? | Text | Free text ≤200 chars | Displaced sheets, moved pillow | bedding_disruption_signs |
| CAR-306 | Is the patient confused on waking? | Dropdown[No/Rare/Intermittent/Frequent] | Allowed set | Yes, intermittent | waking_confusion_level |
| CAR-307 | How often does the patient wake unusually fatigued? | Dropdown[No/Occasional/Frequent] | Allowed set | Frequent | morning_fatigue_frequency |
| CAR-308 | Does the patient wet the bed after a suspected event? | Dropdown[No/Occasional/Frequent] | Allowed set | Occasional | nocturnal_enuresis_flag |
| CAR-309 | How many nocturnal events do you estimate per month? | Number | 0–100 | ~3/month | estimated_nocturnal_count |
| CAR-310 | What monitoring do you use at night? | Text | Free text ≤200 chars | Baseline audio via phone, no device yet | nocturnal_monitoring_aid |
| CAR-311 | Do you share a bed with the patient? | Yes-No | Yes/No | Yes (spouse in same bed) | bed_sharing_flag |
| CAR-312 | Have you discussed SUDEP risk with the clinician? | Yes-No | Yes/No | Yes, with neurologist | sudep_discussion_flag |

## Caregiver Assessment — Section 4: Observed Triggers at Home

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| CAR-401 | How many hours does the patient sleep per day? | Number | 0–24 hrs | 5.2 hrs/day (short) | observed_sleep_duration |
| CAR-402 | How would you rate the patient's sleep quality? | Dropdown[Good/Fair/Poor] | Allowed set | Poor, fragmented | observed_sleep_quality |
| CAR-403 | How often does the patient work late into the night? | Dropdown[Rare/Sometimes/Frequent] | Allowed set | Frequent | late_night_work_frequency |
| CAR-404 | How much work stress do you observe? | Dropdown[Low/Moderate/High] | Allowed set | High during deadlines | observed_work_stress |
| CAR-405 | How often do you observe missed medication doses? | Dropdown[None/Rare/Occasional/Frequent] | Allowed set | Occasional (mainly evening) | observed_missed_doses |
| CAR-406 | How much alcohol does the patient consume? | Dropdown[None/Rare, low/Moderate/High] | Allowed set | Rare, low | observed_alcohol_use |
| CAR-407 | How much caffeine does the patient consume? | Dropdown[Low/Moderate/High] | Allowed set | High (late-day coffee) | observed_caffeine_use |
| CAR-408 | How much screen time before bed do you observe? | Dropdown[Low/Moderate/High] | Allowed set | High | pre_bed_screen_time |
| CAR-409 | How often does the patient skip meals? | Dropdown[None/Rare/Occasional/Frequent] | Allowed set | Occasional under deadlines | observed_meal_skipping |
| CAR-410 | What is the strongest trigger you observe? | Text | Free text ≤200 chars | Sleep deficit | strongest_observed_trigger |
| CAR-411 | What pattern links triggers to the patient's seizures? | Text | Free text ≤200 chars | Poor sleep precedes most events | trigger_event_correlation |
| CAR-412 | Overall, how heavy is the trigger burden? | Dropdown[Low/Low–Moderate/Moderate–High/Critical] | Allowed set | Moderate–High | observed_trigger_burden |

## Caregiver Assessment — Section 5: Home Medication Support & Reminders

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| CAR-501 | What is the first anti-seizure medication and dose? | Text | Drug name + dose | Carbamazepine 400 mg BID | asm1_regimen |
| CAR-502 | What is the second anti-seizure medication and dose? | Text | Drug name + dose | Levetiracetam 500 mg BID | asm2_regimen |
| CAR-503 | Who provides medication reminders? | Dropdown[Self-managed/Spouse/Shared/Carer] | Allowed set | Spouse (verbal + phone alarm) | reminder_provider |
| CAR-504 | How often are reminders given? | Dropdown[Not needed/As needed/Once daily/Twice daily] | Allowed set | Twice daily | reminder_frequency |
| CAR-505 | Is a pill organizer used? | Yes-No | Yes/No | Yes (weekly, spouse-filled) | pill_organizer_used |
| CAR-506 | What percentage of doses do you observe taken? | Number | 0–100 % | 88% | observed_adherence_rate |
| CAR-507 | Which dose is most often missed? | Dropdown[None/Morning/Afternoon/Evening] | Allowed set | Evening (late work) | most_missed_dose |
| CAR-508 | Who manages prescription refills? | Dropdown[Patient/Spouse/Shared/Pharmacy] | Allowed set | Spouse tracks and reorders | refill_management |
| CAR-509 | What medication side effects do you observe? | Text | Free text ≤200 chars | Mild drowsiness, occasional irritability | observed_side_effects |
| CAR-510 | What behavior or mood changes do you observe? | Text | Free text ≤200 chars | Mood dip noted with Levetiracetam | observed_behavior_change |
| CAR-511 | How many doses do you personally witness taken? | Dropdown[Rarely/Some/Majority/All] | Allowed set | Majority (morning most reliable) | doses_witnessed_taken |
| CAR-512 | What is the main barrier to adherence? | Text | Free text ≤200 chars | Irregular schedule / deadlines | adherence_barrier |

## Caregiver Assessment — Section 6: Safety, Supervision & First-Aid Readiness

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| CAR-601 | What is the patient's current driving status? | Dropdown[Permitted/Conditional/Restricted/Prohibited] | Allowed set | Restricted (not driving) | driving_status |
| CAR-602 | How many falls have occurred in the last year? | Number | 0–99 | 1 | falls_last_year |
| CAR-603 | How severe was the worst injury? | Dropdown[None/Minor/Moderate/High] | Allowed set | Moderate (bruising, no fracture) | injury_severity |
| CAR-604 | Which high-risk activities do you supervise? | Text | Free text ≤200 chars | Bathing, cooking, stairs | supervised_activities |
| CAR-605 | What bathroom adaptations are in place? | Text | Free text ≤200 chars | Shower preferred over bath | bathroom_adaptation |
| CAR-606 | What kitchen precautions are in place? | Text | Free text ≤200 chars | Back burners, reduced solo cooking | kitchen_precautions |
| CAR-607 | Are you trained in seizure first aid? | Dropdown[No/Basic awareness/Yes (basic)/Yes (advanced)] | Allowed set | Yes (basic) | first_aid_training_level |
| CAR-608 | Do you know the recovery position? | Yes-No | Yes/No | Yes | recovery_position_known |
| CAR-609 | Do you know when to call emergency services? | Yes-No | Yes/No | Knows >5 min rule | emergency_timing_knowledge |
| CAR-610 | Is rescue medication available at home? | Yes-No | Yes/No | Not prescribed | rescue_medication_available |
| CAR-611 | What supervision is in place at night? | Text | Free text ≤200 chars | Bed sharing, phone nearby | nocturnal_supervision |
| CAR-612 | Is there a documented emergency plan? | Dropdown[None/Informal/Partial/Formal] | Allowed set | Partial (informal) | emergency_plan_status |

## Caregiver Assessment — Section 7: Caregiver Burden & Wellbeing (ZBI)

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| CAR-701 | Which burden instrument was used? | Read-only(Auto) | Fixed value | Zarit Burden Interview (ZBI-22) | burden_instrument |
| CAR-702 | What is your total ZBI burden score? | Number | 0–88 | 32 (mild–moderate burden) | zbi_total_score |
| CAR-703 | How often is your own sleep disrupted by caregiving? | Dropdown[None/Occasional/Frequent/Constant] | Allowed set | Frequent (nocturnal vigilance) | caregiver_sleep_disruption |
| CAR-704 | How anxious are you about the patient's seizures? | Dropdown[Minimal/Mild/Moderate/Severe] | Allowed set | Moderate | seizure_anxiety_level |
| CAR-705 | How much has caregiving affected your work or career? | Dropdown[None/Mild/Moderate/Major] | Allowed set | Mild (some flexibility used) | work_impact_level |
| CAR-706 | How restricted is your social life? | Dropdown[None/Mild/Moderate/Severe] | Allowed set | Moderate | social_restriction_level |
| CAR-707 | How much financial strain do you experience? | Dropdown[None/Mild/Moderate/Significant] | Allowed set | Mild | financial_strain_level |
| CAR-708 | How much relationship strain do you experience? | Dropdown[None/Mild/Moderate/High] | Allowed set | Mild | relationship_strain_level |
| CAR-709 | How often do you neglect your own health? | Dropdown[No/Occasional/Frequent] | Allowed set | Occasional | self_health_neglect |
| CAR-710 | How much respite or support is available to you? | Dropdown[Not needed/Some/Limited/Overwhelmed] | Allowed set | Limited (family nearby) | respite_availability |
| CAR-711 | How well do you feel you are coping? | Dropdown[Good/Fair to good/Fair/Crisis] | Allowed set | Fair to good | perceived_coping_level |
| CAR-712 | Are you engaged with a caregiver support group? | Dropdown[Not needed/Aware/Not yet, interested/Engaged] | Allowed set | Not yet, interested | support_group_engagement |
