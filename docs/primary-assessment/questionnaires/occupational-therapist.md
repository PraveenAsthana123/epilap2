# Occupational Therapist — Patient Questionnaire (Consolidated, EP001)

> **Why (this doc):** The complete set of questions the Occupational Therapist asks the patient, aggregated from every Occupational Therapist assessment section into one enterprise form for intake, EMR entry, and AI feature extraction. **How:** auto-generated from the section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.

**Role:** Occupational Therapist · **Sections:** 7 · **Total questions:** 70 · **ID prefix:** `OT`


## Occupational Therapist Assessment — Section 1: Referral Information

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| OT001 | Who referred the patient for occupational therapy? | Dropdown[Neurologist/Nurse/Self/Other] | Epilepsy-care referrer only (never psychiatry) | Neurologist | referral_source_class |
| OT002 | What is the reason for this OT referral? | Text | Free text, 10-300 chars | Functional decline and safety concerns limiting daily occupations | referral_reason_intent |
| OT003 | What is the primary epilepsy diagnosis? | Dropdown[Focal/Generalized/Combined/Unknown Epilepsy] | Must be an epilepsy diagnosis | Focal Epilepsy (left-temporal) | epilepsy_diagnosis_code |
| OT004 | When was epilepsy diagnosed? | Date | ISO-8601, not in future | 2024-03-12 | diagnosis_recency_index |
| OT005 | What is the current seizure classification? | Dropdown[Focal Aware/Focal Impaired Awareness/Focal to Bilateral Tonic-Clonic] | ILAE 2017 allowed set | Focal Impaired Awareness (from neurologist) | seizure_classification_code |
| OT006 | How urgent is this referral? | Dropdown[Routine/Priority/Urgent] | One of allowed set | Priority | referral_urgency_level |
| OT007 | Is a previous OT assessment available? | Yes-No | Yes or No | No | prior_ot_episode_flag |
| OT008 | Were previous OT records reviewed? | Dropdown[Yes/No/Not applicable] | One of allowed set | Not applicable (no prior records) | prior_records_reviewed_flag |
| OT009 | Summarize the referral in the patient's context. | Text | Free text, 20-500 chars | 29M with poorly controlled focal impaired-awareness seizures (~5/month), on medical leave, needing assistance with meal preparation; referred for functional and safety assessment | referral_summary_embedding |
| OT010 | OT electronic signature confirming referral capture. | Signature | Signed name + date | Signed — OT, 2026-07-11 | signature_verified_flag |

## Occupational Therapist Assessment — Section 2: Occupational Profile

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| OT011 | What is the patient's current living arrangement? | Dropdown[Lives with spouse/Lives with family/Lives alone/Supervised/Inpatient] | One of allowed set | Lives with spouse | living_arrangement_class |
| OT012 | What is the patient's marital/relationship status? | Dropdown[Single/Married/Partnered/Divorced/Widowed] | One of allowed set | Married | relationship_status_class |
| OT013 | Who is the patient's primary caregiver? | Dropdown[None required/Spouse/Family/Clinical staff] | One of allowed set | Spouse | caregiver_support_class |
| OT014 | What is the patient's current employment status? | Dropdown[Employed full-time/Employed with adjustments/On medical leave/Unable to work] | One of allowed set | On medical leave (affected) | employment_status_class |
| OT015 | What is the patient's student status? | Dropdown[Not a student/Part-time student/Full-time student] | One of allowed set | Not a student | student_status_flag |
| OT016 | Describe the patient's typical daily routine. | Text | Free text, 10-400 chars | Structured mornings, rests midday after fatigue, limited outings due to seizure fear | daily_routine_structure_index |
| OT017 | What hobbies and leisure activities does the patient value? | Checklist | One or more activities | Cooking, reading, walking with spouse | leisure_engagement_profile |
| OT018 | Which roles are most important to the patient? | Checklist | One or more roles | Spouse, worker, home contributor | valued_roles_profile |
| OT019 | Summarize the patient's occupational profile. | Text | Free text, 20-500 chars | 29M married, living with supportive spouse; valued worker role interrupted by medical leave; routines and community outings curtailed by ~5 seizures/month | occupational_profile_embedding |
| OT020 | Occupational participation score for the patient. | Read-only(Auto) | 0-100, system-derived | 40/100 (reduced; ~80% occupational impact) | occupational_participation_index |

## Occupational Therapist Assessment — Section 3: Patient Priorities

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| OT021 | How high a priority is improving self-care for the patient? | Dropdown[Low/Medium/High priority/Not applicable] | One of allowed set | Medium priority — mostly independent | selfcare_priority_weight |
| OT022 | How high a priority is improving household activities? | Dropdown[Low/Medium/High priority/Not applicable] | One of allowed set | High priority — safer meal preparation wanted | household_priority_weight |
| OT023 | How high a priority is returning to work? | Dropdown[Low/Medium/High priority/Not applicable] | One of allowed set | High priority — return to work is top goal | work_priority_weight |
| OT024 | How high a priority is school participation? | Dropdown[Low/Medium/High priority/Not applicable] | One of allowed set | Not applicable | school_priority_weight |
| OT025 | How high a priority is driving/transportation? | Dropdown[Low/Medium/High priority/Not applicable] | One of allowed set | Medium priority — currently not driving | transport_priority_weight |
| OT026 | How high a priority is social participation? | Dropdown[Low/Medium/High priority/Not applicable] | One of allowed set | Medium priority — limited by seizure fear | social_priority_weight |
| OT027 | How high a priority is leisure? | Dropdown[Low/Medium/High priority/Not applicable] | One of allowed set | Low priority — maintained with spouse | leisure_priority_weight |
| OT028 | How high a priority is community participation? | Dropdown[Low/Medium/High priority/Not applicable] | One of allowed set | Medium priority — outings curtailed | community_priority_weight |
| OT029 | What other priorities does the patient identify? | Text | Free text, 5-300 chars | Improve overall independence | other_priorities_intent |
| OT030 | Ranked top priorities for the patient. | Read-only(Auto) | System-derived top 3 | Top 3: Return to Work, Improve Independence, Safer Meal Preparation | priority_ranking_score |

## Occupational Therapist Assessment — Section 4: Functional Concerns

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| OT031 | What level of difficulty does the patient have with dressing? | Dropdown[Independent/Independent — minor difficulty/Requires assistance/Dependent] | One of allowed set | Independent — minor difficulty | dressing_difficulty_level |
| OT032 | What level of difficulty does the patient have with bathing? | Dropdown[Independent/Independent — minor difficulty/Requires assistance/Dependent] | One of allowed set | Independent — minor difficulty (seizure-safety aware) | bathing_difficulty_level |
| OT033 | What level of difficulty does the patient have with cooking? | Dropdown[Independent/Independent — minor difficulty/Requires assistance/Dependent] | One of allowed set | Requires assistance (burn/seizure risk at stove) | cooking_difficulty_level |
| OT034 | What level of difficulty does the patient have with shopping? | Dropdown[Independent/Independent — minor difficulty/Requires assistance/Dependent] | One of allowed set | Requires assistance (fatigue, crowds, transport) | shopping_difficulty_level |
| OT035 | What level of difficulty does the patient have managing medications? | Dropdown[Independent/Independent — minor difficulty/Requires assistance/Dependent] | One of allowed set | Independent — minor difficulty (88% adherence) | medication_management_difficulty_level |
| OT036 | What level of difficulty does the patient have using technology? | Dropdown[Independent/Independent — minor difficulty/Requires assistance/Dependent] | One of allowed set | Independent | technology_use_difficulty_level |
| OT037 | What level of difficulty does the patient have remembering appointments? | Dropdown[Independent/Independent — minor difficulty/Requires assistance/Dependent] | One of allowed set | Independent — minor difficulty (post-ictal memory) | appointment_recall_difficulty_level |
| OT038 | What level of difficulty does the patient have completing tasks? | Dropdown[Independent/Independent — minor difficulty/Requires assistance/Dependent] | One of allowed set | Independent — minor difficulty (fatigue interrupts) | task_completion_difficulty_level |
| OT039 | Summarize the patient's functional concerns. | Text | Free text, 20-500 chars | Independent with minor difficulty across most ADL; requires assistance with cooking and shopping due to seizure and safety risk | functional_concern_embedding |
| OT040 | Aggregate functional concern score for the patient. | Read-only(Auto) | 0-100, system-derived | 62/100 (moderate-high concern; assistance needed in 2 IADL domains) | functional_concern_score |

## Occupational Therapist Assessment — Section 5: Seizure Impact on Daily Life

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| OT041 | Do seizures interfere with the patient's work? | Dropdown[Yes/No/N/A] | One of allowed set | Yes — on medical leave | work_interference_flag |
| OT042 | Do seizures interfere with the patient's school participation? | Dropdown[Yes/No/N/A] | One of allowed set | N/A — not a student | school_interference_flag |
| OT043 | Do seizures interfere with driving/transportation? | Dropdown[Yes/No/N/A] | One of allowed set | Yes — driving restricted, uses public transport/lifts | transport_interference_flag |
| OT044 | Do seizures interfere with household activities? | Dropdown[Yes/No/N/A] | One of allowed set | Yes — cooking/meal-prep affected | household_interference_flag |
| OT045 | Do seizures interfere with social participation? | Dropdown[Yes/No/N/A] | One of allowed set | Yes — reduced community participation | social_interference_flag |
| OT046 | Do seizures interfere with the patient's sleep? | Dropdown[Yes/No/N/A] | One of allowed set | Yes — nocturnal seizures affect sleep | sleep_interference_flag |
| OT047 | Does fear of seizures limit the patient's activities? | Yes-No | Yes or No | Yes | seizure_fear_limitation_flag |
| OT048 | Does the patient avoid activities due to seizure concerns? | Yes-No | Yes or No | Yes — avoids solo cooking and swimming | activity_avoidance_flag |
| OT049 | Summarize the occupational impact of seizures. | Text | Free text, 20-500 chars | Major interference across work, transport, and home occupations; fear-driven avoidance present | seizure_impact_embedding |
| OT050 | Occupational impact score for the patient. | Read-only(Auto) | 0-100%, system-derived | 80% (High) | occupational_impact_score |

## Occupational Therapist Assessment — Section 6: Initial Safety Screening

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| OT051 | Has the patient had any falls in the past 12 months? | Yes-No | Yes or No (record count) | Yes — 1 fall | fall_history_flag |
| OT052 | Has the patient had any burns or kitchen accidents? | Yes-No | Yes or No | Yes — minor burn during cooking | burn_incident_flag |
| OT053 | Are there bathroom safety concerns? | Yes-No | Yes or No | Yes — no grab rails, uses bathtub | bathroom_hazard_flag |
| OT054 | Are stairs present at the patient's home? | Yes-No | Yes or No | Yes | stairs_present_flag |
| OT055 | Does the patient live alone? | Yes-No | Yes or No | No — lives with spouse | lives_alone_flag |
| OT056 | Does the patient use mobility aids? | Yes-No | Yes or No | No | mobility_aid_flag |
| OT057 | Is an emergency response plan available? | Dropdown[Yes/No/Partial] | One of allowed set | Partial — informal plan, not documented | emergency_plan_status |
| OT058 | Is immediate OT intervention required? | Yes-No | Yes or No | Yes — kitchen safety | immediate_intervention_flag |
| OT059 | Record safety notes and recommended modifications. | Text | Free text, 20-500 chars | Priority hazard is unsupervised cooking; recommend hob guards, kettle/meal-prep modification, bathroom grab rails | safety_notes_embedding |
| OT060 | Aggregate safety risk score for the patient. | Read-only(Auto) | 0-100%, system-derived | 70% (High) | safety_risk_score |

## Occupational Therapist Assessment — Section 7: Initial Clinical Impression

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| OT061 | Were major occupational problems identified? | Yes-No | Yes or No | Yes — work participation, meal-prep safety, community mobility | occupational_problem_flag |
| OT062 | What is the highest-priority OT issue? | Text | Free text, 5-300 chars | Safe return to work + meal-prep (kitchen) safety | priority_issue_intent |
| OT063 | Which immediate interventions are recommended? | Checklist | One or more interventions | Kitchen-safety modifications, energy/seizure-aware meal prep, graded return-to-work plan | recommended_intervention_set |
| OT064 | What additional assessments are required? | Checklist | Zero or more assessments | Home safety assessment, driving/transport review | additional_assessment_set |
| OT065 | Is referral to another MDT member recommended? | Yes-No | Yes or No | Yes — neurologist (driving), social worker (work) | mdt_referral_flag |
| OT066 | Does the patient agree with the assessment priorities? | Yes-No | Yes or No | Yes | patient_agreement_flag |
| OT067 | What is the baseline functional independence level? | Dropdown[Fully independent/Independent with minor difficulty/Requires assistance/Dependent] | One of allowed set | Independent with minor difficulty; needs assistance with cooking | baseline_independence_level |
| OT068 | Summarize the initial OT clinical impression. | Text | Free text, 20-500 chars | Focal impaired-awareness epilepsy with high occupational impact and high safety risk; kitchen safety and return-to-work are lead goals | clinical_impression_embedding |
| OT069 | Is the assessment complete? | Yes-No | Yes or No | Yes | assessment_complete_flag |
| OT070 | OT electronic signature closing the assessment. | Signature | Signed name + date | Signed — OT, 2026-07-11 | signature_verified_flag |
