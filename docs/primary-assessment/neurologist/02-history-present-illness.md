# Neurologist Assessment — Section 2: History of Present Illness (EP001)

> **Why (this doc):** The history of present illness (HPI) captures the onset, evolution, and current trajectory of the seizure disorder, which anchors every downstream diagnostic and treatment decision for patient EP001 (29M, focal impaired awareness, left-temporal). **How:** The neurologist elicits structured onset, frequency, and modifier data during the clinical interview and records it as discrete key-value fields for the epilepsy data pipeline.

**Problem:** Focal epilepsy trajectories are only interpretable when onset and course are captured consistently; free-text narratives lose the structured signals needed for longitudinal modeling.

**Research Objective:** Encode the HPI as machine-readable fields so seizure onset, frequency change, and treatment-response markers can feed reproducible epilepsy phenotyping and outcome analysis.

**Role:** Neurologist · **Type:** Primary (clinical) data

*Caption - Structured HPI fields for EP001 documenting first-seizure timing, initial semiology, and current disease-course modifiers used to classify severity and treatment responsiveness.*

| Question | Answer |
|---|---|
| First seizure date | 2024-01-14 |
| Age at first seizure | 27 |
| Initial presentation | Sudden loss of awareness followed by right arm jerking |
| Frequency increasing | Yes |
| Breakthrough seizures | Yes |
| Recent infection | No |
| Medication recently changed | Yes |

## Questionnaire (Enterprise Form)

*Caption - The patient-facing questions the neurologist asks to capture this section, with response type, validation, EP001's example answer, and the derived AI feature.*

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0201 | When did your very first seizure happen? | Date | ISO-8601 date | 2024-01-14 | first_seizure_date |
| NEU-0202 | How old were you when the first seizure occurred? | Number | 0-120 years | 27 | age_at_first_seizure |
| NEU-0203 | What happened during that first seizure? | Text | free-text, 3-300 chars | Sudden loss of awareness followed by right arm jerking | initial_presentation |
| NEU-0204 | Are your seizures becoming more frequent? | Yes-No | one-of[Yes|No|Occasionally] | Yes | frequency_increasing |
| NEU-0205 | Are you still having seizures despite treatment? | Yes-No | one-of[Yes|No|Rare] | Yes | breakthrough_seizures |
| NEU-0206 | Have you had any recent infection or illness? | Yes-No | one-of[Yes|No] | No | recent_infection |
| NEU-0207 | Has your medication been changed recently? | Yes-No | one-of[Yes|No] | Yes | medication_recently_changed |

## Severity Scenario Model — Neurologist View

*Caption - The same assessment answered across four epilepsy severity levels from the neurologist's point of view; each variable shifts with severity. EP001 corresponds to Level 3 (Severe). Level 4 is the operational emergency — status epilepticus with seizures recurring about every 5 minutes.*

### Level 1 — Mild (Well-Controlled)
| Question | Answer |
|---|---|
| First seizure date | 2024-01-14 |
| Age at first seizure | 27 |
| Initial presentation | Brief focal aware episode, no motor spread |
| Frequency increasing | No |
| Breakthrough seizures | No |
| Recent infection | No |
| Medication recently changed | No |

### Level 2 — Moderate (Intermediate)
| Question | Answer |
|---|---|
| First seizure date | 2024-01-14 |
| Age at first seizure | 27 |
| Initial presentation | Loss of awareness with brief automatisms |
| Frequency increasing | Occasionally |
| Breakthrough seizures | Rare |
| Recent infection | No |
| Medication recently changed | No |

### Level 3 — Severe (Poorly Controlled) — EP001
| Question | Answer |
|---|---|
| First seizure date | 2024-01-14 |
| Age at first seizure | 27 |
| Initial presentation | Sudden loss of awareness followed by right arm jerking |
| Frequency increasing | Yes |
| Breakthrough seizures | Yes |
| Recent infection | No |
| Medication recently changed | Yes |

### Level 4 — Refractory / Status Epilepticus (Operational Emergency)
| Question | Answer |
|---|---|
| First seizure date | 2024-01-14 |
| Age at first seizure | 27 |
| Initial presentation | Prolonged seizures evolving to convulsive status epilepticus |
| Frequency increasing | Yes, continuous (every ~5 min without recovery) |
| Breakthrough seizures | Yes, recurring every ~5 min |
| Recent infection | Yes (possible precipitant) |
| Medication recently changed | Yes (recent ASM lapse) |

### Severity Classification Logic
```mermaid
flowchart TD
    A[Neurologist assessment] --> B{Severity markers}
    B -->|rare, controlled| L1[Level 1 Mild]
    B -->|moderate burden| L2[Level 2 Moderate]
    B -->|breakthrough despite adherence| L3[Level 3 Severe]
    B -->|seizures every ~5 min / status| L4[Level 4 Status Emergency]
    L3 --> E[EP001]
```
**Reason:** The illness course is read as a trajectory along a severity ladder, not a single snapshot. **Why:** Onset and course markers set treatment intensity and escalation for EP001. **What is happening:** Frequency, breakthrough, and precipitant fields shift from stable control to continuous status. **How it is happening:** The neurologist maps interview responses onto level thresholds. **Reference:** Fisher et al. (2017).

## Pipeline and Context Diagrams

```mermaid
flowchart TD
    A[Patient Interview] --> B[HPI Field Capture]
    B --> C[Neurologist Assessment Record]
    C --> D[Epilepsy Data Pipeline]
    D --> E[Phenotype and Outcome Model]
```

**Reason:** Shows where HPI data enters the clinical pipeline. **Why:** Onset and course fields are foundational inputs, so their flow must be explicit. **What is happening:** Interview responses are captured as structured fields and routed into the assessment record and modeling stages. **How it is happening:** The neurologist transcribes discrete answers that the pipeline ingests as typed variables. **Reference:** Fisher et al., 2017.

```mermaid
sequenceDiagram
    participant P as Patient EP001
    participant N as Neurologist
    participant R as Assessment Record
    P->>N: Describes seizure onset and course
    N->>N: Elicits structured HPI fields
    N->>R: Records discrete values
    R-->>N: Confirms captured data
```

**Reason:** Identifies the role capturing the HPI. **Why:** Accountability for data provenance requires naming who elicits and records each field. **What is happening:** The neurologist interviews the patient and writes structured values to the record. **How it is happening:** A guided clinical interview maps narrative to key-value fields. **Reference:** Fisher et al., 2017.

```mermaid
graph LR
    HPI[History of Present Illness] --> SEM[Seizure Semiology]
    HPI --> MED[Medication History]
    HPI --> IMG[Neuroimaging Section]
    HPI --> VEC[Clinical Vector]
```

**Reason:** Shows how HPI links to other assessment sections. **Why:** Onset and course fields inform semiology, medication, and imaging interpretation. **What is happening:** The HPI feeds multiple downstream sections that compose the clinical vector. **How it is happening:** Shared patient identifiers join HPI fields to related assessment records. **Reference:** Topol, 2019.

```mermaid
journey
    title EP001 HPI Capture Experience
    section Interview
      Recall first seizure: 3: Patient
      Describe current course: 4: Patient
    section Recording
      Elicit structured fields: 5: Neurologist
      Confirm accuracy: 4: Neurologist, Patient
```

**Reason:** Depicts the patient and role experience for this item. **Why:** Data quality depends on how comfortably the patient recalls and confirms details. **What is happening:** The patient recounts onset and course while the neurologist structures and verifies it. **How it is happening:** Iterative question-and-confirm steps produce validated fields. **Reference:** Topol, 2019.

## Professor Readiness (Defense Q&A)

**Q1: Why capture the HPI as discrete fields rather than free text?**
Discrete fields make onset, frequency, and treatment-response signals machine-readable, enabling reproducible longitudinal analysis that free-text narratives cannot support.

**Q2: How do these HPI fields support the focal epilepsy classification for EP001?**
Fields such as initial presentation and breakthrough seizures document focal semiology and pharmacoresistance markers consistent with the ILAE operational classification.

**Q3: What is the significance of "Medication recently changed" being Yes alongside "Breakthrough seizures" Yes?**
Together they flag a possible treatment-response or adherence event, prompting review of drug levels and regimen adequacy before escalating to advanced workup.

## References

American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). American Psychological Association.

Fisher, R. S., Cross, J. H., French, J. A., Higurashi, N., Hirsch, E., Jansen, F. E., Lagae, L., Moshé, S. L., Peltola, J., Roulet Perez, E., Scheffer, I. E., & Zuberi, S. M. (2017). Operational classification of seizure types by the International League Against Epilepsy: Position paper of the ILAE Commission for Classification and Terminology. *Epilepsia, 58*(4), 522–530. https://doi.org/10.1111/epi.13670

Topol, E. J. (2019). *Deep medicine: How artificial intelligence can make healthcare human again*. Basic Books.
