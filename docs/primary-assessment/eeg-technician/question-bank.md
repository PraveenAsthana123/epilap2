# EEG Technologist — Hospital-Grade Question Bank (EEG001–EEG080)

> **Why (this doc):** The full 80‑item EEG‑technologist acquisition questionnaire (8 sections:
> verification → technical report) — the hospital‑grade expansion behind the EEG‑Technician role's
> enterprise questionnaire. **How:** one table per section with the exact IDs; these items feed the
> acquisition/QC feature set used by the [secondary EEG analysis](../../analysis/secondary-analysis.md).

## Section 1 — Patient Verification

*Caption - Identity, order, and start‑of‑recording checks completed before acquisition.*

| ID | Question |
|---|---|
| EEG001 | Confirm patient identity using two identifiers |
| EEG002 | Confirm physician order |
| EEG003 | Confirm test type requested |
| EEG004 | Date and time of recording |
| EEG005 | Patient fasting? (if relevant to protocol) |
| EEG006 | Hair clean and free of oils/products? |
| EEG007 | Patient cooperative? |
| EEG008 | Interpreter required? |
| EEG009 | Consent confirmed (per site protocol) |
| EEG010 | Recording started successfully |

## Section 2 — Test Preparation

*Caption - Sleep, medication, and clinical‑state factors that condition the recording.*

| ID | Question |
|---|---|
| EEG011 | Sleep deprivation requested? |
| EEG012 | Approximate sleep last night (hours) |
| EEG013 | Last meal time |
| EEG014 | Last anti‑seizure medication taken |
| EEG015 | Recent seizure before test? |
| EEG016 | Time since last seizure |
| EEG017 | Fever or acute illness today? |
| EEG018 | Pregnancy status (if applicable and relevant) |
| EEG019 | Any scalp wounds or skin issues? |
| EEG020 | Metal hair accessories removed? |

## Section 3 — Electrode Placement

*Caption - Montage, impedance, and setup‑quality documentation.*

| ID | Question |
|---|---|
| EEG021 | Electrode placement system used |
| EEG022 | Electrode cap or individual electrodes? |
| EEG023 | Electrode impedance acceptable? |
| EEG024 | Maximum impedance value |
| EEG025 | Any electrode replaced during setup? |
| EEG026 | Missing electrodes? |
| EEG027 | Reference electrode used |
| EEG028 | Ground electrode verified |
| EEG029 | Electrode placement documented |
| EEG030 | Overall setup quality |

## Section 4 — Recording Quality

*Caption - Duration, completeness, and signal‑quality of the acquisition.*

| ID | Question |
|---|---|
| EEG031 | Recording duration |
| EEG032 | Recording completed as ordered? |
| EEG033 | Background activity adequate? |
| EEG034 | Excessive electrical noise? |
| EEG035 | Baseline stable? |
| EEG036 | Technical interruptions? |
| EEG037 | Video synchronized (if Video EEG)? |
| EEG038 | Audio synchronized? |
| EEG039 | Data loss during recording? |
| EEG040 | Overall recording quality |

## Section 5 — Artifact Documentation

*Caption - Artifact types observed — critical for downstream automated analysis.*

| ID | Question |
|---|---|
| EEG041 | Eye blink artifact observed? |
| EEG042 | Eye movement artifact observed? |
| EEG043 | Muscle artifact observed? |
| EEG044 | ECG artifact observed? |
| EEG045 | Electrode pop artifact observed? |
| EEG046 | Sweat artifact observed? |
| EEG047 | Motion artifact observed? |
| EEG048 | Chewing artifact observed? |
| EEG049 | Respiratory artifact observed? |
| EEG050 | Other artifact (describe) |

## Section 6 — Activation Procedures

*Caption - Hyperventilation, photic, and sleep activation to elicit epileptiform activity.*

| ID | Question |
|---|---|
| EEG051 | Hyperventilation performed? |
| EEG052 | Hyperventilation duration |
| EEG053 | Hyperventilation completed safely? |
| EEG054 | Photic stimulation performed? |
| EEG055 | Flash frequencies completed |
| EEG056 | Response observed during photic stimulation? |
| EEG057 | Sleep recorded? |
| EEG058 | Drowsiness recorded? |
| EEG059 | Any activation procedure stopped early? |
| EEG060 | Reason procedure stopped |

## Section 7 — Event Documentation

*Caption - Clinical events captured during the recording (ictal documentation).*

| ID | Question |
|---|---|
| EEG061 | Clinical event observed during recording? |
| EEG062 | Number of events observed |
| EEG063 | Event start time |
| EEG064 | Event end time |
| EEG065 | Patient behavior during event |
| EEG066 | Body movements observed |
| EEG067 | Consciousness appeared altered? |
| EEG068 | Event marker inserted? |
| EEG069 | Video annotation completed? |
| EEG070 | Family/caregiver observations documented (if present)? |

## Section 8 — Technical Report

*Caption - Adequacy, export, archival, and sign‑off of the study.*

| ID | Question |
|---|---|
| EEG071 | Recording technically adequate? |
| EEG072 | Major technical limitations |
| EEG073 | Repeat study recommended due to technical issues? |
| EEG074 | Recording exported successfully |
| EEG075 | Recording transferred to neurologist |
| EEG076 | Raw EEG file archived |
| EEG077 | Video archived (if applicable) |
| EEG078 | Technical summary |
| EEG079 | EEG technologist name |
| EEG080 | Electronic signature |

---
Feeds: the EEG‑Technician role sections in [primary‑assessment](../index.md) and the acquisition/QC
features of the [secondary EEG pipeline](../../analysis/secondary-analysis.md). Real EEG acquisition
(CHB‑MIT) analysed in [chbmit‑real‑analysis](../../analysis/chbmit-real-analysis.md).
