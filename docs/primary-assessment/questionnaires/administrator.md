# Administrator — Patient Questionnaire (Consolidated, EP001)

> **Why (this doc):** The complete set of questions the Administrator asks the patient, aggregated from every Administrator assessment section into one enterprise form for intake, EMR entry, and AI feature extraction. **How:** auto-generated from the section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.

**Role:** Administrator · **Sections:** 6 · **Total questions:** 117 · **ID prefix:** `ADM`


## Administrator Assessment — Section 1: Patient Registration & Demographics

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| ADM-0101 | What is the patient's assigned Patient ID? | Read-only(Auto) | Format EP### | EP001 | patient_id_resolution |
| ADM-0102 | What is the patient's Medical Record Number? | Read-only(Auto) | Format EP-YYYY-### | EP-2026-001 | mrn_deduplication |
| ADM-0103 | What is the de-identified Study ID? | Read-only(Auto) | Format DBA-EP-### | DBA-EP-001 | study_id_mapping |
| ADM-0104 | What is the patient's full legal name? | Text | Non-empty; HIPAA-protected | [Redacted per HIPAA] | identity_verification |
| ADM-0105 | What is the patient's date of birth? | Date | ISO date (YYYY-MM-DD) | 1997-03-14 | age_derivation |
| ADM-0106 | What is the patient's age? | Read-only(Auto) | Derived integer 0-120 years | 29 years | age_band_stratification |
| ADM-0107 | What is the patient's sex? | Dropdown[Male/Female/Other] | Allowed set | Male | demographic_cohorting |
| ADM-0108 | What is the patient's handedness? | Dropdown[Right/Left/Ambidextrous] | Allowed set | Right | lateralization_flag |
| ADM-0109 | What is the patient's marital status? | Dropdown[Single/Married/Divorced/Widowed] | Allowed set | Married | support_context_tagging |
| ADM-0110 | What is the patient's occupation? | Text | Free text | Software Engineer | functional_safety_context |
| ADM-0111 | What is the patient's highest education level? | Dropdown[High School/Bachelor's/Master's/Doctorate] | Allowed set | Bachelor's Degree | health_literacy_estimate |
| ADM-0112 | What is the patient's preferred language? | Dropdown[English/Spanish/Other] | Allowed set | English | interpreter_need_prediction |
| ADM-0113 | Is the patient's contact phone on file and verified? | Yes-No | Verified boolean | On file (verified) | reachability_scoring |
| ADM-0114 | Is the patient's email on file and verified? | Yes-No | Verified boolean; email format | On file (verified) | reminder_channel_selection |
| ADM-0115 | Is the patient's address on file and verified? | Yes-No | Verified boolean | On file (verified) | geolocation_access_analysis |
| ADM-0116 | Who is the patient's emergency contact? | Text | Non-empty relationship | Spouse (on file) | emergency_contact_activation |
| ADM-0117 | What is the registration date? | Date | ISO date (YYYY-MM-DD) | 2026-07-11 | encounter_timeline_anchor |
| ADM-0118 | What is the visit type? | Dropdown[New Patient/Established/Emergency] | Allowed set | New Patient | visit_type_classification |
| ADM-0119 | What is the registration status? | Dropdown[Active/Inactive/Pending] | Allowed set | Active | record_status_monitoring |

## Administrator Assessment — Section 2: Insurance, Billing Eligibility & Consent

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| ADM-0201 | What is the patient's assigned Patient ID? | Read-only(Auto) | Format EP### | EP001 | patient_id_resolution |
| ADM-0202 | What is the de-identified Study ID? | Read-only(Auto) | Format DBA-EP-### | DBA-EP-001 | study_id_mapping |
| ADM-0203 | What is the patient's insurance type? | Dropdown[Commercial/Medicare/Medicaid/Self-Pay] | Allowed set | Commercial (Employer-Sponsored PPO) | payer_mix_classification |
| ADM-0204 | Is the payer name on file and verified? | Yes-No | Verified boolean | On file (verified) | payer_identification |
| ADM-0205 | Is the policy number on file and verified? | Yes-No | Verified boolean; policy format | On file (verified) | coverage_validation |
| ADM-0206 | Is the group number on file and verified? | Yes-No | Verified boolean | On file (verified) | group_plan_matching |
| ADM-0207 | What is the subscriber relationship? | Dropdown[Self/Spouse/Child/Other] | Allowed set | Self | subscriber_link_resolution |
| ADM-0208 | What is the eligibility status? | Dropdown[Active/Inactive/Pending] | Allowed set | Active / Verified | eligibility_verification |
| ADM-0209 | What is the eligibility verification date? | Date | ISO date (YYYY-MM-DD) | 2026-07-10 | verification_recency_check |
| ADM-0210 | Is prior authorization required? | Yes-No | Boolean with procedure list | Yes (EEG, MRI) | prior_auth_prediction |
| ADM-0211 | What is the prior authorization status? | Dropdown[Approved/Pending/Denied/N/A] | Allowed set | Approved | auth_status_tracking |
| ADM-0212 | What is the specialist copay amount? | Number | Currency >= 0 (USD) | $40 (Specialist) | out_of_pocket_estimation |
| ADM-0213 | What is the deductible-met status? | Dropdown[Met/Partial/Not Met] | Allowed set | Partial | deductible_progress_tracking |
| ADM-0214 | What is the coordination of benefits status? | Dropdown[None/Primary/Secondary] | Allowed set | None (single payer) | cob_resolution |
| ADM-0215 | Is consent to treat signed? | Yes-No | Signed with ISO date | Signed 2026-07-11 | consent_status_tracking |
| ADM-0216 | Is the HIPAA privacy acknowledgement signed? | Yes-No | Signed with ISO date | Signed 2026-07-11 | privacy_acknowledgement_check |
| ADM-0217 | Is de-identified research consent signed? | Yes-No | Signed with ISO date | Signed 2026-07-11 | research_consent_scope |
| ADM-0218 | What is the GDPR data-use lawful basis? | Dropdown[Explicit consent/Vital interests/Legal obligation] | Allowed set | Explicit consent | lawful_basis_classification |
| ADM-0219 | Is the financial responsibility agreement signed? | Yes-No | Signed with ISO date | Signed 2026-07-11 | financial_agreement_tracking |

## Administrator Assessment — Section 3: Appointment & Clinic Scheduling

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| ADM-0301 | What is the patient's assigned Patient ID? | Read-only(Auto) | Format EP### | EP001 | patient_id_resolution |
| ADM-0302 | What is the de-identified Study ID? | Read-only(Auto) | Format DBA-EP-### | DBA-EP-001 | study_id_mapping |
| ADM-0303 | What is the visit type? | Dropdown[New Patient/Established/Emergency] | Allowed set | New Patient | visit_type_classification |
| ADM-0304 | What is the appointment type? | Dropdown[Consult/Follow-up/Urgent/Emergency] | Allowed set | Outpatient Neurology Consult | appointment_type_routing |
| ADM-0305 | What is the scheduled appointment date? | Date | ISO date (YYYY-MM-DD) | 2026-07-14 | calendar_slot_optimization |
| ADM-0306 | What is the scheduled appointment time? | Text | 24h time (HH:MM) | 09:30 | slot_time_allocation |
| ADM-0307 | What is the appointment duration? | Number | Minutes > 0 | 45 min | duration_estimation |
| ADM-0308 | What is the clinic location? | Text | Non-empty facility/suite | Neurology Outpatient, Suite 3 | resource_location_assignment |
| ADM-0309 | Who is the assigned provider? | Text | Non-empty provider | Attending Neurologist | provider_matching |
| ADM-0310 | What is the referral source? | Text | Non-empty source | Family Physician | referral_source_attribution |
| ADM-0311 | What is the booking channel? | Dropdown[Referral Intake/Patient Portal/Clinic Triage/ED Triage] | Allowed set | Referral Intake | channel_utilization_analysis |
| ADM-0312 | Is an interpreter required? | Yes-No | Boolean | No | interpreter_need_prediction |
| ADM-0313 | Is transport assistance required? | Yes-No | Boolean | No | transport_need_prediction |
| ADM-0314 | When is the EEG scheduled? | Date | ISO date-time or Not required | 2026-07-21 10:00 | diagnostic_sequencing |
| ADM-0315 | When is the MRI scheduled? | Date | ISO date-time or Not required | 2026-07-23 14:00 | imaging_sequencing |
| ADM-0316 | When is the follow-up appointment? | Date | ISO date with interval | 2026-10-14 (3 months) | followup_interval_planning |
| ADM-0317 | What is the reminder method? | Dropdown[SMS/Email/SMS + Email/Call] | Allowed set | SMS + Email | reminder_channel_selection |
| ADM-0318 | What is the referral-to-consult wait time? | Number | Days >= 0 | 3 days | access_wait_time_metric |
| ADM-0319 | What is the appointment status? | Dropdown[Confirmed/Pending/Admitted/Cancelled] | Allowed set | Confirmed | appointment_status_tracking |
| ADM-0320 | What is the no-show risk flag? | Dropdown[Low/Medium/High/N/A] | Allowed set | Low | no_show_risk_prediction |

## Administrator Assessment — Section 4: Encounter, ICD-10/CPT Coding

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| ADM-0401 | What is the patient's assigned Patient ID? | Read-only(Auto) | Format EP### | EP001 | patient_id_resolution |
| ADM-0402 | What is the de-identified Study ID? | Read-only(Auto) | Format DBA-EP-### | DBA-EP-001 | study_id_mapping |
| ADM-0403 | What is the encounter type? | Dropdown[Consult/Follow-up/Urgent/Emergency] | Allowed set | Outpatient Neurology Consult | encounter_type_classification |
| ADM-0404 | What is the encounter date? | Date | ISO date (YYYY-MM-DD) | 2026-07-14 | encounter_timeline_anchor |
| ADM-0405 | What is the place of service code? | Dropdown[11/21/23] | CMS POS code set | 11 (Office) | place_of_service_validation |
| ADM-0406 | What is the primary diagnosis (ICD-10)? | Text | ICD-10 code format | G40.209 | icd10_code_assignment |
| ADM-0407 | What is the diagnosis description? | Text | Non-empty | Localization-related focal epilepsy with complex partial seizures, not intractable, without status epilepticus | diagnosis_text_mapping |
| ADM-0408 | What is the alternate diagnosis (ICD-10)? | Text | ICD-10 code format | G40.109 | alternate_code_suggestion |
| ADM-0409 | What is the laterality note? | Text | Non-empty | Left-temporal focus | laterality_extraction |
| ADM-0410 | What is the E/M service (CPT)? | Text | CPT code format | 99204 (New patient, moderate complexity) | em_level_recommendation |
| ADM-0411 | What is the EEG procedure (CPT)? | Text | CPT code or Not performed | 95816 (EEG, awake and drowsy) | procedure_code_assignment |
| ADM-0412 | What is the MRI procedure (CPT)? | Text | CPT code or Not performed | 70553 (MRI brain w/ and w/o contrast) | imaging_code_assignment |
| ADM-0413 | What modifier applies? | Text | CPT modifier or None | None | modifier_suggestion |
| ADM-0414 | Who is the rendering provider? | Text | Non-empty provider | Attending Neurologist | provider_attribution |
| ADM-0415 | Is medical necessity documented? | Yes-No | Documented with rationale | Documented (new-onset focal seizures) | medical_necessity_validation |
| ADM-0416 | What is the charge capture status? | Dropdown[Complete/Incomplete/Expedited] | Allowed set | Complete | charge_capture_tracking |
| ADM-0417 | What is the claim status? | Dropdown[Ready to Submit/Held/Submitted/Denied] | Allowed set | Ready to Submit | claim_status_prediction |
| ADM-0418 | What is the coding audit flag? | Dropdown[Passed/Priority review/Failed] | Allowed set | Passed | coding_audit_flagging |
| ADM-0419 | What are the patient's height, weight, and BMI? | Number | cm / kg / BMI numeric | 175 cm / 72 kg / 23.5 | anthropometric_capture |

## Administrator Assessment — Section 5: Records Management & Data Governance

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| ADM-0501 | What is the patient's assigned Patient ID? | Read-only(Auto) | Format EP### | EP001 | patient_id_resolution |
| ADM-0502 | What is the de-identified Study ID? | Read-only(Auto) | Format DBA-EP-### | DBA-EP-001 | study_id_mapping |
| ADM-0503 | What record system holds the data? | Dropdown[EHR/EHR + PACS/EHR + Critical Care] | Allowed set | Electronic Health Record (EHR) | system_of_record_tagging |
| ADM-0504 | What interoperability standard is used? | Dropdown[HL7 FHIR R4/HL7 v2/DICOM] | Allowed set | HL7 FHIR R4 | interoperability_compliance |
| ADM-0505 | What is the data classification? | Dropdown[Public/Sensitive/PHI/PHI-Critical] | Allowed set | Sensitive / Protected Health Information | data_classification_tagging |
| ADM-0506 | What access control model is enforced? | Dropdown[RBAC/ABAC/Break-glass] | Allowed set | Role-Based (RBAC) | access_model_enforcement |
| ADM-0507 | Is the minimum necessary policy enforced? | Yes-No | Boolean | Enforced | minimum_necessary_audit |
| ADM-0508 | Is audit logging enabled? | Yes-No | Immutable boolean | Enabled (immutable) | audit_log_monitoring |
| ADM-0509 | What is the encryption-at-rest standard? | Dropdown[AES-256/AES-128/None] | Allowed set | AES-256 | encryption_compliance_check |
| ADM-0510 | What is the encryption-in-transit standard? | Dropdown[TLS 1.3/TLS 1.2/None] | Allowed set | TLS 1.3 | transit_security_check |
| ADM-0511 | What de-identification method is applied? | Dropdown[Safe Harbor/Expert Determination/None] | Allowed set | Safe Harbor (18 identifiers removed) | deidentification_validation |
| ADM-0512 | Who holds the re-identification key custody? | Text | Restricted role | Restricted (data custodian) | key_custody_control |
| ADM-0513 | What is the consent scope on file? | Dropdown[Treatment/Treatment + Research/Emergency] | Allowed set | Treatment + De-identified Research | consent_scope_enforcement |
| ADM-0514 | What is the GDPR lawful basis? | Dropdown[Explicit consent/Vital interests/Legal obligation] | Allowed set | Explicit consent | lawful_basis_classification |
| ADM-0515 | Which data subject rights are enabled? | Dropdown[Access/Rectification/Erasure] | Allowed set (multi) | Access, Rectification, Erasure | data_rights_management |
| ADM-0516 | What is the retention period? | Number | Years >= 0 | 10 years (post last encounter) | retention_policy_enforcement |
| ADM-0517 | What is the breach notification SLA? | Number | Hours > 0 | 72 hours | breach_sla_monitoring |
| ADM-0518 | What is the backup frequency? | Dropdown[Daily/Continuous/Weekly] | Allowed set | Daily (encrypted) | backup_integrity_check |
| ADM-0519 | Is a data sharing agreement in place? | Yes-No | Boolean with scope | In place (research use) | data_sharing_compliance |
| ADM-0520 | What is the governance review date? | Date | ISO date (YYYY-MM-DD) | 2026-07-11 | governance_review_scheduling |

## Administrator Assessment — Section 6: Referral Intake & Care Coordination

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| ADM-0601 | What is the patient's assigned Patient ID? | Read-only(Auto) | Format EP### | EP001 | patient_id_resolution |
| ADM-0602 | What is the de-identified Study ID? | Read-only(Auto) | Format DBA-EP-### | DBA-EP-001 | study_id_mapping |
| ADM-0603 | What is the referral source? | Text | Non-empty source | Family Physician | referral_source_attribution |
| ADM-0604 | What is the referral reason? | Text | Non-empty clinical reason | New-onset focal seizures | referral_reason_classification |
| ADM-0605 | What is the referral received date? | Date | ISO date (YYYY-MM-DD) | 2026-07-08 | intake_timeline_anchor |
| ADM-0606 | What is the referral type? | Dropdown[Consult/Follow-up/Urgent/Emergency Transfer] | Allowed set | Outpatient Neurology Consult | referral_type_routing |
| ADM-0607 | What is the triage priority? | Dropdown[Routine/Urgent/Emergent] | Allowed set | Routine (fast-tracked) | triage_priority_prediction |
| ADM-0608 | Is the referral complete? | Dropdown[Complete/Incomplete] | Allowed set | Complete (notes + labs attached) | referral_completeness_check |
| ADM-0609 | What supporting documents are attached? | Text | Non-empty document list | GP notes, basic metabolic panel | document_completeness_analysis |
| ADM-0610 | Did the insurance pre-check pass? | Dropdown[Passed/Failed/Deferred] | Allowed set | Passed | eligibility_precheck |
| ADM-0611 | When is the consult booked? | Date | ISO date or Immediate | 2026-07-14 | consult_scheduling_link |
| ADM-0612 | What diagnostics are coordinated? | Text | Non-empty diagnostic list | EEG + MRI | diagnostic_coordination |
| ADM-0613 | What is the interdisciplinary loop? | Text | Non-empty team list | Neurology, EEG Tech, Neuropsychology | care_team_composition |
| ADM-0614 | When was the referral acknowledgement sent? | Date | ISO date or Immediate | 2026-07-08 | acknowledgement_tracking |
| ADM-0615 | When is the outcome letter to the referrer due? | Text | Scheduled milestone | Scheduled post-consult | loop_closure_scheduling |
| ADM-0616 | Is a care coordinator assigned? | Yes-No | Boolean | Assigned | coordinator_assignment |
| ADM-0617 | What is the referral tracking ID? | Read-only(Auto) | Format REF-EP###-#### | REF-EP001-0708 | referral_tracking_id |
| ADM-0618 | What is the loop closure status? | Dropdown[In Progress/Closed/Emergent handoff] | Allowed set | In Progress | loop_closure_monitoring |
| ADM-0619 | What is the escalation flag? | Dropdown[None/Watch/Activated] | Allowed set | None | escalation_flag_prediction |
| ADM-0620 | What is the referral status? | Dropdown[Accepted/Pending/Admitted/Declined] | Allowed set | Accepted | referral_status_tracking |
