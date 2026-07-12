# Pharmacist — Patient Questionnaire (Consolidated, EP001)

> **Why (this doc):** The complete set of questions the Pharmacist asks the patient, aggregated from every Pharmacist assessment section into one enterprise form for intake, EMR entry, and AI feature extraction. **How:** auto-generated from the section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.

**Role:** Pharmacist · **Sections:** 7 · **Total questions:** 85 · **ID prefix:** `PHA`


## Pharmacist Assessment — Section 1: Medication Reconciliation

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PHA-0101 | What is the patient's unique identifier? | Read-only(Auto) | Format EP-YYYY-NNN | EP001 (EP-2026-001) | patient_identity_link |
| PHA-0102 | What is the patient's current body weight? | Number | 30–200 kg | 72 kg | weight_based_dosing |
| PHA-0103 | On what date was this reconciliation performed? | Date | ISO 8601 (YYYY-MM-DD) | 2026-07-11 | reconciliation_recency_flag |
| PHA-0104 | Which sources did you use to verify the medication list? | Dropdown[Prescriber orders/Pharmacy dispensing log/Patient interview/ED-ICU chart] (multi-select) | At least 1 required | Prescriber orders, pharmacy dispensing log, patient interview | source_completeness_score |
| PHA-0105 | What is the first antiseizure medication, dose, and frequency? | Text | Drug name + dose + frequency | Carbamazepine (CBZ) 400 mg BID | primary_asm_encoding |
| PHA-0106 | What is the second antiseizure medication, dose, and frequency? | Text | Drug name + dose + frequency, or None | Levetiracetam (LEV) 500 mg BID | secondary_asm_encoding |
| PHA-0107 | Is any PRN or rescue medication prescribed? | Text | Drug + route, or None | None currently prescribed | rescue_medication_flag |
| PHA-0108 | What OTC medications or supplements does the patient take? | Text | Free text, or None | Occasional ibuprofen; vitamin D 1000 IU | otc_interaction_input |
| PHA-0109 | Does the patient have any known drug allergies? | Text | NKDA or allergen list | No known drug allergies (NKDA) | allergy_alert_flag |
| PHA-0110 | How many discrepancies were found between sources? | Number | Integer ≥ 0 | 1 (CBZ evening dose taken late/variably) | discrepancy_count |
| PHA-0111 | Were the identified discrepancies resolved? | Yes-No | Yes / No / Not applicable | Yes — timing counselling flagged | discrepancy_resolution_status |
| PHA-0112 | How many total active medications are on the reconciled list? | Read-only(Auto) | Auto-count from list | 2 ASMs + 1 supplement | medication_burden_index |

## Pharmacist Assessment — Section 2: ASM Regimen Review

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PHA-0201 | What is the first antiseizure medication? | Text | Drug name | Carbamazepine (CBZ) | primary_asm_identity |
| PHA-0202 | What is the carbamazepine dose and total daily amount? | Text | mg BID; max 1600 mg/day | 400 mg BID (800 mg/day) | cbz_daily_dose_mg |
| PHA-0203 | What is carbamazepine's mechanism of action? | Read-only(Auto) | Drug-class lookup | Sodium-channel blockade | mechanism_class_tag |
| PHA-0204 | What is carbamazepine's enzyme-induction status? | Read-only(Auto) | Inducer / inhibitor / neutral | Strong CYP3A4 inducer (auto-inducer) | enzyme_induction_flag |
| PHA-0205 | What is the second antiseizure medication? | Text | Drug name, or None | Levetiracetam (LEV) | secondary_asm_identity |
| PHA-0206 | What is the levetiracetam dose and total daily amount? | Text | mg BID; 500–3000 mg/day | 500 mg BID (1000 mg/day) | lev_daily_dose_mg |
| PHA-0207 | What is levetiracetam's mechanism of action? | Read-only(Auto) | Drug-class lookup | SV2A synaptic-vesicle binding | mechanism_class_tag |
| PHA-0208 | What is the rationale for this drug combination? | Text | Free text | Complementary mechanisms; no shared metabolism target | combination_rationality_score |
| PHA-0209 | Is the carbamazepine dose adequate relative to the ceiling? | Dropdown[Subtherapeutic/Low/Low-moderate/Adequate/At-ceiling] | Single select | Low–moderate; below weight-based ceiling | cbz_dose_adequacy |
| PHA-0210 | Is the levetiracetam dose adequate relative to headroom? | Dropdown[Subtherapeutic/Low/Low-moderate/Adequate/At-ceiling] | Single select | Low; titration headroom to 1500–3000 mg/day | lev_dose_adequacy |
| PHA-0211 | What is the current seizure-control status? | Dropdown[Controlled/Mostly controlled/Inadequate/Status] | Single select | Inadequate — ~5/month, breakthrough | seizure_control_status |
| PHA-0212 | What is the regimen recommendation? | Text | Free text | Optimize LEV titration; reassess CBZ trough | regimen_optimization_action |

## Pharmacist Assessment — Section 3: Adherence Assessment

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PHA-0301 | Which methods were used to assess adherence? | Dropdown[Pill count/MPR/Self-report/Inpatient MAR review] (multi-select) | At least 1 required | Pill count + MPR + self-report | adherence_method_set |
| PHA-0302 | How many days of refill records were reviewed? | Number | 30–365 days | 90 days | refill_window_days |
| PHA-0303 | What is the medication possession ratio (MPR)? | Number | 0.00–1.00 | 0.88 | medication_possession_ratio |
| PHA-0304 | What is the pill-count adherence percentage? | Percentage | 0–100% | 87% | pill_count_adherence_pct |
| PHA-0305 | What did the patient self-report about missed doses? | Text | Free text | Occasionally misses evening dose | self_report_adherence |
| PHA-0306 | How many doses are missed per week (estimated)? | Number | 0–14 | 1–2 (evening CBZ) | missed_doses_per_week |
| PHA-0307 | What is the overall adherence category? | Dropdown[Optimal/Good/Suboptimal/Critical] | Single select | Suboptimal (borderline) | adherence_category |
| PHA-0308 | What adherence barrier was identified? | Text | Free text, or None | Evening schedule / work shift timing | adherence_barrier_tag |
| PHA-0309 | What is the observed dosing pattern? | Text | Free text | Consistent morning, variable evening | dosing_pattern_profile |
| PHA-0310 | What is the likely impact of adherence on seizure control? | Dropdown[None/Minimal/Plausible contributor/Precipitant] | Single select | Plausible contributor to breakthrough | adherence_control_impact |
| PHA-0311 | What adherence intervention is planned? | Text | Free text | Dose-timing counselling, reminder app | adherence_intervention |
| PHA-0312 | When should adherence be reassessed? | Dropdown[4 weeks/3 months/6–12 months/Continuous] | Single select | 4 weeks | reassessment_interval |

## Pharmacist Assessment — Section 4: Drug–Drug Interaction Screen

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PHA-0401 | Which screening tool was used for the interaction check? | Read-only(Auto) | Tool name | CYP450 interaction matrix + clinical database | screening_tool_id |
| PHA-0402 | Which drug is the index enzyme inducer? | Text | Drug name, or None | Carbamazepine (strong CYP3A4 inducer) | index_inducer_flag |
| PHA-0403 | Does the index drug undergo auto-induction? | Yes-No | Yes / No | Yes — CBZ induces its own metabolism | auto_induction_flag |
| PHA-0404 | What is the severity of the CBZ × LEV interaction? | Dropdown[None/Minimal/Minor/Moderate/Major] | Single select | Minimal (LEV renally cleared, non-CYP) | cbz_lev_interaction_severity |
| PHA-0405 | What is the severity of the CBZ × oral contraceptives interaction? | Dropdown[None/Minimal/Minor/Moderate/Major] | Single select | Major — reduced contraceptive efficacy | cbz_oc_interaction_severity |
| PHA-0406 | What is the severity of the CBZ × warfarin interaction? | Dropdown[None/Minimal/Minor/Moderate/Major] | Single select | Major — reduced anticoagulant effect | cbz_warfarin_interaction_severity |
| PHA-0407 | What is the severity of the CBZ × ibuprofen (OTC) interaction? | Dropdown[None/Minimal/Minor/Moderate/Major] | Single select | Minor — monitor, no action | cbz_ibuprofen_interaction_severity |
| PHA-0408 | Is any enzyme inhibitor present in the regimen? | Yes-No | Yes / No | No | enzyme_inhibitor_flag |
| PHA-0409 | What is the highest interaction-severity flag overall? | Dropdown[None/Minor/Moderate/Major] | Single select | Major (contraceptive / anticoagulant class) | highest_interaction_severity |
| PHA-0410 | How many clinically active interactions are present now? | Number | Integer ≥ 0 | 0 current (no OC/warfarin now) | active_interaction_count |
| PHA-0411 | Is a counselling trigger raised for co-prescribing? | Yes-No | Yes / No / Low | Yes — future co-prescribing caution | counselling_trigger_flag |
| PHA-0412 | What is the interaction-screen recommendation? | Text | Free text | Document inducer status prominently in record | interaction_recommendation |

## Pharmacist Assessment — Section 5: Adverse-Effect / Tolerability Review

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PHA-0501 | Which tool was used for the adverse-effect review? | Read-only(Auto) | Tool name | ASM-specific adverse-effect checklist | review_tool_id |
| PHA-0502 | What is the severity of carbamazepine-related dizziness? | Dropdown[None/Mild/Moderate/Severe] | Single select | Mild, intermittent | cbz_dizziness_severity |
| PHA-0503 | What is the severity of carbamazepine-related diplopia? | Dropdown[None/Mild/Moderate/Severe] | Single select | Occasional, dose-related | cbz_diplopia_severity |
| PHA-0504 | What is the serum sodium (carbamazepine hyponatremia screen)? | Number | 120–145 mmol/L | Screen — Na 137 mmol/L (normal) | serum_sodium_mmol |
| PHA-0505 | Is there any history of carbamazepine rash? | Yes-No | Yes / No | None | cbz_rash_flag |
| PHA-0506 | What is the severity of levetiracetam-related mood/irritability? | Dropdown[None/Mild/Moderate/Severe] | Single select | Mild irritability reported | lev_mood_severity |
| PHA-0507 | What is the severity of levetiracetam-related somnolence? | Dropdown[None/Minimal/Mild/Moderate/Severe] | Single select | Minimal | lev_somnolence_severity |
| PHA-0508 | What is the overall tolerability rating? | Dropdown[Excellent/Good/Acceptable/Poor] | Single select | Acceptable — no dose-limiting toxicity | overall_tolerability |
| PHA-0509 | Is any dose-limiting effect present? | Text | Free text, or None | None currently | dose_limiting_effect_flag |
| PHA-0510 | Is any serious adverse drug reaction flagged? | Yes-No | Yes / No | None | serious_adr_flag |
| PHA-0511 | What is the sodium-monitoring plan? | Text | Free text | Continue periodic checks (CBZ) | sodium_monitoring_plan |
| PHA-0512 | What is the mood-monitoring plan? | Text | Free text | Track LEV irritability at follow-up | mood_monitoring_plan |
| PHA-0513 | Is upward dose titration feasible given tolerability? | Dropdown[None/Small/Available/IV only] | Single select | LEV headroom available with monitoring | titration_feasibility |

## Pharmacist Assessment — Section 6: Therapeutic Drug Monitoring

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PHA-0601 | What type of serum sample was taken? | Dropdown[Trough/Random/STAT/Serial] | Single select | Trough (pre-dose) | sample_type |
| PHA-0602 | What is the carbamazepine serum level? | Number | 0–20 mg/L (CBZ ref 4–12 mg/L) | 6.2 mg/L | cbz_serum_level_mgl |
| PHA-0603 | What is the carbamazepine reference range? | Read-only(Auto) | 4–12 mg/L | 4–12 mg/L | cbz_reference_range |
| PHA-0604 | How is the carbamazepine level interpreted? | Dropdown[Subtherapeutic/Low-therapeutic/Mid/High/Toxic] | Single select | Low-therapeutic | cbz_level_interpretation |
| PHA-0605 | What is the levetiracetam serum level? | Number | 0–60 mg/L (LEV ref 12–46 mg/L) | 18 mg/L (est.) | lev_serum_level_mgl |
| PHA-0606 | What is the levetiracetam reference range? | Read-only(Auto) | 12–46 mg/L | 12–46 mg/L | lev_reference_range |
| PHA-0607 | How is the levetiracetam level interpreted? | Dropdown[Subtherapeutic/Low-therapeutic/Mid/High/Toxic] | Single select | Low-therapeutic | lev_level_interpretation |
| PHA-0608 | What is the sampling context? | Text | Free text | Steady state, morning trough | sampling_context |
| PHA-0609 | What was the adherence level at the time of sampling? | Number | MPR 0.00–1.00 | MPR 0.88 (borderline) | adherence_at_sampling |
| PHA-0610 | What is the estimated auto-induction effect on the level? | Text | Free text | Likely lowering CBZ level | auto_induction_effect |
| PHA-0611 | Is titration headroom available on current levels? | Yes-No | Yes / No | Yes — both agents below mid-range | titration_headroom_flag |
| PHA-0612 | What is the therapeutic-drug-monitoring recommendation? | Text | Free text | Repeat trough after LEV titration | tdm_recommendation |

## Pharmacist Assessment — Section 7: Counselling & Pharmaceutical Care Plan

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| PHA-0701 | On what date was the care plan created? | Date | ISO 8601 (YYYY-MM-DD) | 2026-07-11 | care_plan_date |
| PHA-0702 | What is the primary goal of the care plan? | Text | Free text | Reduce seizure frequency toward control | primary_care_goal |
| PHA-0703 | What is the adherence counselling action? | Text | Free text | Fix evening CBZ timing; reminder app | adherence_counselling_item |
| PHA-0704 | What is the sleep counselling action? | Text | Free text | Address 5.2 hr sleep as trigger | sleep_counselling_item |
| PHA-0705 | What is the interaction counselling action? | Text | Free text | Warn on future OC / CYP3A4 co-meds | interaction_counselling_item |
| PHA-0706 | What is the adverse-effect counselling action? | Text | Free text | Report diplopia, mood, dizziness early | adverse_effect_counselling_item |
| PHA-0707 | What dosing action is recommended to the prescriber? | Text | Free text | Recommend LEV titration to prescriber | dosing_action |
| PHA-0708 | What is the monitoring plan? | Text | Free text | Repeat TDM + sodium at 4–6 weeks | monitoring_plan |
| PHA-0709 | What is the adherence (MPR) target? | Number | MPR target 0.00–1.00 | MPR greater than 0.95 | adherence_target_mpr |
| PHA-0710 | Was patient understanding confirmed? | Dropdown[Teach-back confirmed/Partial/Not confirmed] | Single select | Teach-back confirmed | teach_back_status |
| PHA-0711 | When is the follow-up scheduled? | Text | Date or interval | Pharmacist review in 4 weeks | follow_up_schedule |
| PHA-0712 | With whom is the care plan shared? | Dropdown[Neurologist/Patient/ICU/Emergency team] (multi-select) | At least 1 required | Neurologist, patient | care_plan_recipients |
