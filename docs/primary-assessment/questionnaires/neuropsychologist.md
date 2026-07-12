# Neuropsychologist — Patient Questionnaire (Consolidated, EP001)

> **Why (this doc):** The complete set of questions the Neuropsychologist asks the patient, aggregated from every Neuropsychologist assessment section into one enterprise form for intake, EMR entry, and AI feature extraction. **How:** auto-generated from the section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.

**Role:** Neuropsychologist · **Sections:** 8 · **Total questions:** 96 · **ID prefix:** `NPS`


## Neuropsychologist Assessment — Section 1: Global Cognitive Screening

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NPS-0101 | Which standardized screening instrument was administered? | Dropdown[MoCA, MMSE, ACE-III] | Instrument name | MoCA (v8.1) | screening_instrument |
| NPS-0102 | What was the total screening score? | Score | MoCA 0-30 | 26/30 | moca_total_score |
| NPS-0103 | Was an education adjustment applied? | Dropdown[Yes, No] | +1 pt if ≤12 yrs education | No (16 yrs, not required) | education_adjustment_flag |
| NPS-0104 | Score on the visuospatial/executive items? | Score | 0-5 | 5/5 | visuospatial_executive_score |
| NPS-0105 | Score on the naming items? | Score | 0-3 | 2/3 (lion missed) | naming_subscore |
| NPS-0106 | Score on the attention items? | Score | 0-6 | 5/6 | attention_subscore |
| NPS-0107 | Score on language repetition/fluency? | Score | 0-3 | 2/3 | language_subscore |
| NPS-0108 | Score on the abstraction items? | Score | 0-2 | 2/2 | abstraction_subscore |
| NPS-0109 | Score on delayed recall? | Score | 0-5 | 3/5 (2 with cue) | delayed_recall_subscore |
| NPS-0110 | Score on the orientation items? | Score | 0-6 | 6/6 | orientation_subscore |
| NPS-0111 | Confirmatory MMSE total score? | Score | MMSE 0-30 | 28/30 | mmse_total_score |
| NPS-0112 | Rate the patient's effort/engagement. | Dropdown[Adequate, Suboptimal, Poor] | Categorical | Adequate | effort_engagement_rating |
| NPS-0113 | Clinical interpretation of the screen? | Text | Free-text summary | Borderline-normal; recall & naming soft signs | screening_interpretation |

## Neuropsychologist Assessment — Section 2: Verbal & Visual Memory Assessment

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NPS-0201 | Which memory battery was administered? | Dropdown[WMS-IV, WMS-III, RBANS] | Battery name | WMS-IV (Adult) | memory_battery |
| NPS-0202 | Auditory (verbal) memory index? | Score | Index 40-160 | 84 (Low Average) | auditory_verbal_memory_index |
| NPS-0203 | Logical Memory I (immediate) scaled score? | Score | Scaled 1-19 | Scaled 6 | logical_memory_i_scaled |
| NPS-0204 | Logical Memory II (delayed) scaled score? | Score | Scaled 1-19 | Scaled 5 | logical_memory_ii_scaled |
| NPS-0205 | Verbal Paired Associates II scaled score? | Score | Scaled 1-19 | Scaled 6 | verbal_paired_associates_ii_scaled |
| NPS-0206 | Verbal recognition score? | Score | 0-30 | 22/30 | verbal_recognition_score |
| NPS-0207 | Visual memory index? | Score | Index 40-160 | 102 (Average) | visual_memory_index |
| NPS-0208 | Designs I / II scaled scores? | Score | Scaled 1-19 each | Scaled 10 / 10 | designs_scaled |
| NPS-0209 | Visual Reproduction II scaled score? | Score | Scaled 1-19 | Scaled 11 | visual_reproduction_ii_scaled |
| NPS-0210 | Visual recognition score? | Score | 0-30 | 27/30 | visual_recognition_score |
| NPS-0211 | Verbal–visual discrepancy? | Read-only(Auto) | Index-point difference | 18 pts (verbal < visual) | verbal_visual_discrepancy |
| NPS-0212 | Percent verbal information retained? | Number | 0-100% | 74% | verbal_retention_pct |
| NPS-0213 | Clinical interpretation of the memory profile? | Text | Free-text summary | Selective verbal-memory weakness, visuospatial preserved | memory_interpretation |

## Neuropsychologist Assessment — Section 3: Attention & Processing Speed

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NPS-0301 | Digit Span Forward raw/scaled score? | Score | Scaled 1-19 | 6 (Scaled 9) | digit_span_forward |
| NPS-0302 | Digit Span Backward raw/scaled score? | Score | Scaled 1-19 | 4 (Scaled 8) | digit_span_backward |
| NPS-0303 | Digit Span Sequencing scaled score? | Score | Scaled 1-19 | Scaled 8 | digit_span_sequencing |
| NPS-0304 | Spatial Span scaled score? | Score | Scaled 1-19 | Scaled 10 | spatial_span |
| NPS-0305 | Symbol Search scaled score (WAIS-IV)? | Score | Scaled 1-19 | Scaled 8 | symbol_search |
| NPS-0306 | Coding / Digit Symbol scaled score? | Score | Scaled 1-19 | Scaled 7 | coding_digit_symbol |
| NPS-0307 | Processing Speed Index? | Score | Index 40-160 | 88 (Low Average) | processing_speed_index |
| NPS-0308 | Continuous Performance omission errors? | Number | Count | 6 (mild) | cpt_omissions |
| NPS-0309 | Continuous Performance commission errors? | Number | Count | 4 (WNL) | cpt_commissions |
| NPS-0310 | Mean reaction time? | Number | ms | 412 ms (mildly slowed) | reaction_time_mean_ms |
| NPS-0311 | Sustained attention lapses observed? | Dropdown[None, Occasional, Mild late-block, Frequent] | Categorical | Mild, late-block | sustained_attention_lapses |
| NPS-0312 | Clinical interpretation of attention/speed? | Text | Free-text summary | Mild slowing; likely ASM + sleep-deficit related | attention_speed_interpretation |

## Neuropsychologist Assessment — Section 4: Executive Function

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NPS-0401 | Trail Making A completion time? | Number | seconds | 28 sec (Scaled 10) | trail_making_a_time |
| NPS-0402 | Trail Making B completion time? | Number | seconds | 78 sec (Scaled 8) | trail_making_b_time |
| NPS-0403 | Trail B–A difference? | Read-only(Auto) | seconds | 50 sec (mildly elevated) | trail_b_minus_a |
| NPS-0404 | Stroop Word T-score? | Score | T 20-80 | T = 52 | stroop_word_t |
| NPS-0405 | Stroop Color T-score? | Score | T 20-80 | T = 49 | stroop_color_t |
| NPS-0406 | Stroop Color-Word interference T-score? | Score | T 20-80 | T = 43 (mild) | stroop_interference_t |
| NPS-0407 | WCST categories completed? | Score | 0-6 | 5/6 | wcst_categories_completed |
| NPS-0408 | WCST perseverative errors T-score? | Score | T 20-80 | T = 41 (mild) | wcst_perseverative_errors_t |
| NPS-0409 | WCST failures to maintain set? | Number | Count | 1 | wcst_failure_maintain_set |
| NPS-0410 | Verbal Fluency (FAS) total? | Number | raw count | 34 (Low Average) | verbal_fluency_fas |
| NPS-0411 | Category Fluency (Animals) total? | Number | raw count | 16 (Low Average) | category_fluency_animals |
| NPS-0412 | Clinical interpretation of executive function? | Text | Free-text summary | Mild shifting/inhibition weakness; concept formation intact | executive_interpretation |

## Neuropsychologist Assessment — Section 5: Language & Confrontation Naming

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NPS-0501 | Handedness / language dominance? | Dropdown[Right/left-dominant, Left/right-dominant, Mixed] | Categorical | Right-handed / left-dominant (presumed) | handedness_dominance |
| NPS-0502 | Boston Naming Test score (/60)? | Score | 0-60 | 48 (mildly reduced) | bnt_score |
| NPS-0503 | BNT phonemic cue benefit? | Number | items gained | +6 items | bnt_phonemic_cue_benefit |
| NPS-0504 | BNT semantic cue benefit? | Number | items gained | +1 item | bnt_semantic_cue_benefit |
| NPS-0505 | Tip-of-the-tongue frequency? | Dropdown[Normal, Mildly elevated, Elevated, Frequent] | Categorical | Elevated | tip_of_tongue_frequency |
| NPS-0506 | Auditory comprehension (Token Test) score? | Score | 0-44 | 42/44 (WNL) | token_test_score |
| NPS-0507 | Repetition status? | Dropdown[Intact, Impaired] | Categorical | Intact | repetition_status |
| NPS-0508 | Category Fluency (Animals) total? | Number | raw count | 16 (Low Average) | category_fluency_animals |
| NPS-0509 | Letter Fluency (FAS) total? | Number | raw count | 34 (Low Average) | letter_fluency_fas |
| NPS-0510 | Reading / writing status? | Dropdown[Intact, Functionally intact, Impaired] | Categorical | Functionally intact | reading_writing_status |
| NPS-0511 | Clinical interpretation of language/naming? | Text | Free-text summary | Anomia with phonemic-cue responsiveness; comprehension spared | language_naming_interpretation |

## Neuropsychologist Assessment — Section 6: Mood & Anxiety

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NPS-0601 | NDDI-E total score (/24)? | Score | NDDI-E 6-24 | 14 (screen positive threshold ≥15 → borderline) | nddie_total |
| NPS-0602 | NDDI-E suicidality item response? | Dropdown[Denies ideation, Passive ideation, Active ideation] | Escalate if positive | Denies active ideation | nddie_suicidality_item |
| NPS-0603 | GAD-7 total score (/21)? | Score | GAD-7 0-21 | 9 (mild–moderate anxiety) | gad7_total |
| NPS-0604 | BDI-II total score (/63)? | Score | BDI-II 0-63 | 17 (mild depression) | bdi_ii_total |
| NPS-0605 | BDI-II cognitive subscale level? | Dropdown[WNL, Slightly elevated, Mildly elevated, Elevated] | Categorical | Mildly elevated | bdi_cognitive_subscale |
| NPS-0606 | BDI-II somatic subscale level? | Dropdown[WNL, Mildly elevated, Elevated] | Categorical | Elevated (sleep/fatigue driven) | bdi_somatic_subscale |
| NPS-0607 | Self-reported irritability? | Dropdown[Absent, Occasional, Present] | Categorical | Present, ASM-linked | irritability_self_report |
| NPS-0608 | Average sleep (hrs/day)? | Number | hours 0-24 | 5.2 (poor) | sleep_hours_per_day |
| NPS-0609 | Suspected ASM contributor? | Text | Medication name | Levetiracetam (mood/irritability) | suspected_asm_contributor |
| NPS-0610 | Perceived stigma level? | Dropdown[None, Minimal, Mild, Moderate, Severe] | Categorical | Mild | perceived_stigma |
| NPS-0611 | Clinical interpretation of mood/anxiety? | Text | Free-text summary | Mild-moderate anxiety + mild depression; monitor & refer | mood_anxiety_interpretation |

## Neuropsychologist Assessment — Section 7: Quality of Life & Psychosocial Function

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NPS-0701 | QOLIE-31 overall T-score? | Score | T 0-100 | 58 (moderately reduced) | qolie31_overall_t |
| NPS-0702 | Seizure worry subscale? | Score | T 0-100 | 44 (reduced) | seizure_worry_subscale |
| NPS-0703 | Overall quality of life subscale? | Score | T 0-100 | 60 | overall_qol_subscale |
| NPS-0704 | Emotional wellbeing subscale? | Score | T 0-100 | 55 | emotional_wellbeing_subscale |
| NPS-0705 | Energy/fatigue subscale? | Score | T 0-100 | 48 (reduced) | energy_fatigue_subscale |
| NPS-0706 | Cognitive function (self-rated) subscale? | Score | T 0-100 | 50 | cognitive_function_subscale |
| NPS-0707 | Medication effects subscale? | Score | T 0-100 | 52 | medication_effects_subscale |
| NPS-0708 | Social function subscale? | Score | T 0-100 | 56 | social_function_subscale |
| NPS-0709 | Employment status? | Dropdown[Employed unrestricted, Employed with accommodations, Medical leave, Unemployed] | Categorical | Employed (software engineer) | employment_status |
| NPS-0710 | Driving status? | Dropdown[Unrestricted, Conditional, Restricted, Prohibited] | Categorical | Restricted per seizure control | driving_status |
| NPS-0711 | Marital/social support? | Text | Free-text | Married, supportive spouse | marital_social_support |
| NPS-0712 | Clinical interpretation of QoL/psychosocial function? | Text | Free-text summary | Moderate QoL reduction; seizure worry & fatigue dominant | qol_interpretation |

## Neuropsychologist Assessment — Section 8: Integrated Neuropsychological Impression

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NPS-0801 | Global screen (MoCA) summary? | Read-only(Auto) | MoCA 0-30 | 26/30 (borderline) | global_screen_moca |
| NPS-0802 | Verbal memory summary? | Dropdown[Impaired, Low Average, Average, Above Average] | Categorical | Low Average (selectively weak) | verbal_memory_summary |
| NPS-0803 | Visual memory summary? | Dropdown[Impaired, Low Average, Average, Above Average] | Categorical | Average (preserved) | visual_memory_summary |
| NPS-0804 | Verbal–visual dissociation present? | Dropdown[Absent, Emerging, Present] | Categorical | Present (verbal < visual) | verbal_visual_dissociation |
| NPS-0805 | Attention/processing speed summary? | Dropdown[Impaired, Low Average, Average, Above Average] | Categorical | Low Average (ASM/sleep related) | attention_speed_summary |
| NPS-0806 | Executive function summary? | Text | Free-text summary | Mild shifting/inhibition weakness | executive_summary |
| NPS-0807 | Confrontation naming (BNT) summary? | Read-only(Auto) | 0-60 | 48/60 (mild anomia) | confrontation_naming_summary |
| NPS-0808 | Mood/anxiety composite summary? | Read-only(Auto) | Composite scores | GAD-7 = 9; BDI-II = 17; NDDI-E borderline | mood_anxiety_summary |
| NPS-0809 | Quality of life (QOLIE-31) summary? | Dropdown[Good, Mildly reduced, Moderately reduced, Severely reduced] | Categorical | Moderately reduced | qol_summary |
| NPS-0810 | Lateralizing formulation? | Dropdown[No lateralizing deficit, Possible left-temporal, Left temporal, Right temporal] | Categorical | Left (dominant) temporal profile | lateralizing_formulation |
| NPS-0811 | Confidence in the formulation? | Dropdown[Low, Moderate, Moderate–High, High] | Categorical | Moderate–High (convergent) | formulation_confidence |
| NPS-0812 | Primary recommendations? | Text | Free-text list | Verbal memory strategy training; mood referral; sleep/ASM review | primary_recommendations |
