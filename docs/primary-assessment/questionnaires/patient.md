# Patient — Patient Questionnaire (Consolidated, EP001)

> **Why (this doc):** The complete set of questions the Patient asks the patient, aggregated from every Patient assessment section into one enterprise form for intake, EMR entry, and AI feature extraction. **How:** auto-generated from the section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.

**Role:** Patient · **Sections:** 8 · **Total questions:** 96 · **ID prefix:** `PAT`


## Patient Self-Report — Section 1: Symptom Self-Report

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PAT-0101 | What do I feel just before a seizure? | Dropdown[Metallic taste/Déjà vu/Rising sensation/Fear/Visual change/None] | Free-text allowed; ≤200 chars | Metallic taste, then déjà vu | aura_symptom_profile |
| PAT-0102 | How much warning time do I get before a seizure? | Dropdown[None/<10 sec/10–30 sec/30–60 sec/>1 min] | Ordered category | About 10–20 seconds | aura_warning_window |
| PAT-0103 | What happens to my speech during the warning? | Dropdown[Normal/Slow/Words wrong/Cannot speak] | Ordered category | Words come out wrong or slow | ictal_speech_impairment |
| PAT-0104 | How aware am I during a seizure? | Dropdown[Fully aware/Partly aware/Lose track/Unconscious] | Ordered category | I lose track, cannot respond | awareness_impairment_level |
| PAT-0105 | How many seizures do I have per month (my count)? | Number | Integer 0–150/month | About 5 per month | self_reported_seizure_frequency |
| PAT-0106 | How long does a typical seizure last? | Dropdown[<1 min/1–2 min/2–5 min/>5 min] | Ordered category | Roughly a minute or two | typical_seizure_duration |
| PAT-0107 | How do I feel after a seizure? | Text | Free-text ≤200 chars | Confused, headache, very tired | postictal_symptom_profile |
| PAT-0108 | How long do I need to recover after a seizure? | Dropdown[<10 min/10–30 min/30–60 min/>1 hr] | Ordered category | 30–60 minutes before I feel normal | postictal_recovery_burden |
| PAT-0109 | Which symptom bothers me most? | Text | Free-text ≤120 chars | The confusion afterward | dominant_symptom_flag |
| PAT-0110 | Do I log every seizure event? | Yes-No | Boolean | Yes, in my phone diary | diary_logging_flag |
| PAT-0111 | How confident am I in my report? | Dropdown[Low/Medium/High/Mixed] | Ordered category | High for auras, medium for exact timing | self_report_confidence |

## Patient Self-Report — Section 2: Self-Logged Seizure Diary (Mobile App)

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PAT-0201 | What tool do I use to log my seizures? | Dropdown[Mobile App/Paper diary/Web portal/Wearable] | Fixed list | Mobile App (daily) | diary_tool_type |
| PAT-0202 | How do I record each event? | Dropdown[Self-entry after event/Proxy entry/Retrospective] | Fixed list | Self-entry after each event | logging_method |
| PAT-0203 | How many events did I log this month? | Number | Integer 0–150 | 5 | monthly_event_count |
| PAT-0204 | What is my average events per month over 3 months? | Number | Decimal 0–150 | 5.0 | rolling_3mo_frequency |
| PAT-0205 | When was my most recent seizure? | Date | ISO date ≤ today | 2026-07-08 | days_since_last_event |
| PAT-0206 | What time of day do my seizures usually happen? | Dropdown[Morning/Afternoon/Evening/Night/Variable] | Fixed list | Late evening / night | time_of_day_pattern |
| PAT-0207 | How many of my events were nocturnal? | Number | Integer 0–event count | 2 of 5 | nocturnal_event_ratio |
| PAT-0208 | How many events had an aura logged first? | Number | Integer 0–event count | 4 of 5 | aura_presence_ratio |
| PAT-0209 | How many events fell on a missed-dose day? | Number | Integer 0–event count | 1 of 5 | missed_dose_event_ratio |
| PAT-0210 | How quickly do I log an event after it happens? | Dropdown[<1 hr/Within 2 hr/Within 3 hr/Next day/Later] | Ordered category | Within 2 hours | logging_delay |
| PAT-0211 | How many days this month did I log in the diary? | Number | Integer 0–31 | 27 of 30 days | diary_adherence_rate |
| PAT-0212 | Do I have reminder notifications enabled? | Yes-No | Boolean | Enabled (nightly) | reminder_enabled_flag |

## Patient Self-Report — Section 3: Adherence Self-Report

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PAT-0301 | What is my main anti-seizure medication and dose? | Text | Free-text ≤120 chars | Carbamazepine 400 mg twice daily | primary_asm_regimen |
| PAT-0302 | What is my second anti-seizure medication and dose? | Text | Free-text ≤120 chars | Levetiracetam 500 mg twice daily | secondary_asm_regimen |
| PAT-0303 | What percentage of my doses do I take (my estimate)? | Percentage | 0–100% | 88% of doses | self_reported_adherence_rate |
| PAT-0304 | Which dose do I usually miss? | Dropdown[Morning/Midday/Evening/Night/None] | Fixed list | Evening dose | missed_dose_timing |
| PAT-0305 | What is the main reason I miss doses? | Dropdown[Forget/Busy/Travel/Side effects/Cost/Other] | Fixed list | Busy at work, forget | primary_nonadherence_reason |
| PAT-0306 | What is the second reason I miss doses? | Dropdown[Forget/Busy/Travel/Side effects/Cost/Other] | Fixed list | Away from home / travel | secondary_nonadherence_reason |
| PAT-0307 | Do I use reminders to take my medication? | Yes-No | Boolean | Phone alarm, sometimes ignore | reminder_use_flag |
| PAT-0308 | Do I use a pillbox or organizer? | Yes-No | Boolean | Yes, weekly organizer | pillbox_use_flag |
| PAT-0309 | How many doses did I miss in the last 2 weeks? | Number | Integer 0–56 | About 3 | recent_missed_dose_count |
| PAT-0310 | Do I ever stop medication when feeling well? | Yes-No | Boolean | No, I keep taking it | discontinuation_risk_flag |
| PAT-0311 | How confident am I that I take it correctly? | Dropdown[Low/Medium/High/Mixed] | Ordered category | High for morning, medium for evening | adherence_confidence |
| PAT-0312 | Do I refill my prescription on time? | Yes-No | Boolean | Yes, mail pharmacy | refill_timeliness_flag |

## Patient Self-Report — Section 4: Trigger & Lifestyle Self-Report

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PAT-0401 | How many hours of sleep do I usually get? | Number | Decimal 0–14 hrs/night | About 5.2 hours/night | average_sleep_hours |
| PAT-0402 | How would I rate my sleep quality? | Dropdown[Very poor/Poor/Fair/Good/Excellent] | Ordered category | Poor | sleep_quality_rating |
| PAT-0403 | How high is my work stress level? | Dropdown[None/Low/Moderate/High/Very high] | Ordered category | High (deadlines) | work_stress_level |
| PAT-0404 | How often do I drink alcohol? | Dropdown[Never/Occasionally/Weekly/Daily] | Ordered category | Occasionally, weekends | alcohol_frequency |
| PAT-0405 | Does a missed dose act as a trigger for me? | Dropdown[Never/Rarely/Sometimes/Often/Always] | Ordered category | Sometimes, evening dose | missed_dose_trigger_flag |
| PAT-0406 | How much caffeine do I consume daily? | Number | Integer 0–12 cups/day | 3–4 coffees/day | daily_caffeine_intake |
| PAT-0407 | How much screen time do I have before bed? | Dropdown[None/Low/Moderate/High] | Ordered category | High, late nights | pre_sleep_screen_time |
| PAT-0408 | Which trigger do I notice most? | Text | Free-text ≤120 chars | Poor sleep | primary_trigger |
| PAT-0409 | What is my second most noticed trigger? | Text | Free-text ≤120 chars | Work stress | secondary_trigger |
| PAT-0410 | How much do I exercise? | Dropdown[None/Light/Moderate/Regular] | Ordered category | Light, irregular | exercise_level |
| PAT-0411 | How would I rate my overall trigger burden? | Dropdown[Low/Moderate/High/Very high] | Ordered category | High | trigger_burden_score |
| PAT-0412 | What am I most willing to change? | Text | Free-text ≤120 chars | Sleep schedule first | modifiable_change_priority |

## Patient Self-Report — Section 5: ASM Side-Effect Self-Report (LAEP-style)

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PAT-0501 | How often do I feel dizzy or unsteady? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Sometimes | side_effect_dizziness |
| PAT-0502 | How often do I feel tired or fatigued? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Sometimes | side_effect_fatigue |
| PAT-0503 | How often do I feel irritable? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Rarely–Sometimes (mild) | side_effect_irritability |
| PAT-0504 | How often do I have difficulty concentrating? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Sometimes | side_effect_concentration |
| PAT-0505 | How often do I have memory problems? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Rarely | side_effect_memory |
| PAT-0506 | How often do I get headaches? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Rarely | side_effect_headache |
| PAT-0507 | How often do I feel sleepy? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Sometimes | side_effect_sleepiness |
| PAT-0508 | How often do I have shaky hands (tremor)? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Never | side_effect_tremor |
| PAT-0509 | How often do I have blurred or double vision? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Rarely | side_effect_vision |
| PAT-0510 | How often do I feel low in mood? | Dropdown[Never/Rarely/Sometimes/Always] | LAEP category | Rarely | side_effect_low_mood |
| PAT-0511 | How would I rate my overall side-effect burden? | Dropdown[None/Mild/Moderate/Severe] | Ordered category | Moderate | overall_side_effect_burden |
| PAT-0512 | Which side effect bothers me most? | Text | Free-text ≤120 chars | Dizziness | dominant_side_effect |
| PAT-0513 | Do side effects affect my medication adherence? | Yes-No | Boolean | Occasionally skip when very tired | side_effect_adherence_impact |

## Patient Self-Report — Section 6: Quality of Life (QOLIE-31)

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PAT-0601 | How much do I worry about having seizures? | Number | QOLIE-31 0–100 | 42 (frequent worry) | qolie_seizure_worry |
| PAT-0602 | How would I rate my overall quality of life? | Number | QOLIE-31 0–100 | 55 (moderately reduced) | qolie_overall_qol |
| PAT-0603 | How is my emotional well-being? | Number | QOLIE-31 0–100 | 58 | qolie_emotional_wellbeing |
| PAT-0604 | How are my energy and fatigue levels? | Number | QOLIE-31 0–100 | 48 | qolie_energy_fatigue |
| PAT-0605 | How is my cognitive functioning? | Number | QOLIE-31 0–100 | 52 | qolie_cognitive_function |
| PAT-0606 | How much do medication effects bother me? | Number | QOLIE-31 0–100 | 50 | qolie_medication_effects |
| PAT-0607 | How is my social functioning? | Number | QOLIE-31 0–100 | 60 | qolie_social_function |
| PAT-0608 | What is my QOLIE-31 total score? | Read-only(Auto) | QOLIE-31 0–100 | 53 (moderately reduced) | qolie_total_score |
| PAT-0609 | What has the biggest impact on my quality of life? | Text | Free-text ≤120 chars | Cannot drive independently | primary_qol_impact |
| PAT-0610 | What has the second biggest impact? | Text | Free-text ≤120 chars | Seizure worry at work | secondary_qol_impact |
| PAT-0611 | When did I complete this assessment? | Date | ISO date ≤ today | 2026-07-08 | assessment_date |
| PAT-0612 | How has my quality of life changed since last time? | Dropdown[Much better/Slightly better/Same/Slightly worse/Much worse] | Ordered category | Slightly worse | qol_change_trend |

## Patient Self-Report — Section 7: Mood & Anxiety Self-Report (NDDI-E, GAD-7)

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PAT-0701 | What is my total GAD-7 anxiety score? | Read-only(Auto) | GAD-7 0–21 | 9 (moderate anxiety) | gad7_total_score |
| PAT-0702 | How often have I felt nervous or anxious? | Dropdown[Not at all/Several days/More than half the days/Nearly every day] | GAD-7 item 0–3 | Several days | gad7_nervousness |
| PAT-0703 | How often do I worry about having seizures? | Dropdown[Not at all/Several days/More than half the days/Nearly every day] | GAD-7 item 0–3 | More than half the days | gad7_seizure_worry |
| PAT-0704 | How often do I have trouble relaxing? | Dropdown[Not at all/Several days/More than half the days/Nearly every day] | GAD-7 item 0–3 | Several days | gad7_trouble_relaxing |
| PAT-0705 | How often do I feel restless? | Dropdown[Not at all/Several days/More than half the days/Nearly every day] | GAD-7 item 0–3 | Several days | gad7_restlessness |
| PAT-0706 | What is my total NDDI-E depression score? | Read-only(Auto) | NDDI-E 6–24 | 14 (mildly elevated) | nddie_total_score |
| PAT-0707 | Am I above the NDDI-E screening cutoff (>15)? | Read-only(Auto) | Boolean (cutoff >15) | Below cutoff | nddie_cutoff_flag |
| PAT-0708 | How often does everything feel like a struggle? | Dropdown[Never/Rarely/Sometimes/Always] | NDDI-E item 1–4 | Sometimes | nddie_struggle |
| PAT-0709 | How often do I feel down or unhappy? | Dropdown[Never/Rarely/Sometimes/Always] | NDDI-E item 1–4 | Sometimes | nddie_feeling_down |
| PAT-0710 | Have I had thoughts of self-harm (NDDI-E)? | Yes-No | Boolean; triggers safety flag | Not endorsed | suicidality_safety_flag |
| PAT-0711 | What is my main emotional concern? | Text | Free-text ≤120 chars | Worry about next seizure | primary_emotional_concern |
| PAT-0712 | When did I complete this assessment? | Date | ISO date ≤ today | 2026-07-08 | assessment_date |

## Patient Self-Report — Section 8: Personal Goals & Concerns

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PAT-0801 | What is my top goal for treatment? | Text | Free-text ≤120 chars | Regain driving independence | primary_goal |
| PAT-0802 | What is my second goal? | Text | Free-text ≤120 chars | Fewer seizures per month | secondary_goal |
| PAT-0803 | What is my third goal? | Text | Free-text ≤120 chars | Sleep better and lower stress | tertiary_goal |
| PAT-0804 | What is my biggest concern? | Text | Free-text ≤120 chars | Losing my license affects my job | primary_concern |
| PAT-0805 | What is my second concern? | Text | Free-text ≤120 chars | Seizure at work in front of colleagues | secondary_concern |
| PAT-0806 | What is my third concern? | Text | Free-text ≤120 chars | Long-term medication side effects | tertiary_concern |
| PAT-0807 | How does epilepsy affect my work? | Text | Free-text ≤200 chars | Commute and confidence affected | work_impact |
| PAT-0808 | How does epilepsy affect my relationships? | Text | Free-text ≤200 chars | Wife worries; I feel dependent | relationship_impact |
| PAT-0809 | What does treatment success look like to me? | Text | Free-text ≤200 chars | 3 months seizure-free, driving again | success_definition |
| PAT-0810 | What support do I want? | Text | Free-text ≤200 chars | Clear plan and trigger coaching | desired_support |
| PAT-0811 | What am I willing to try? | Text | Free-text ≤200 chars | Sleep changes, better adherence | willingness_to_change |
| PAT-0812 | How confident am I in my care plan? | Dropdown[Low/Moderate/High] | Ordered category | Moderate, hopeful | plan_confidence |
