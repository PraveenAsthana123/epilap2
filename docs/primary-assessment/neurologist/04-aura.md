# Neurologist Assessment — Section 4: Aura (EP001)

> **Why (this doc):** The aura is the patient-reported warning phase of a focal seizure and, in focal impaired awareness epilepsy, offers direct localizing evidence about seizure onset before consciousness is lost. **How:** The neurologist structures the reported pre-ictal symptoms of EP001 (29M, focal impaired awareness, left-temporal) into discrete, machine-readable variables so they can feed the downstream localization and classification pipeline.

**Problem:** Aura symptoms are often described in free narrative, making them hard to compare across visits or link to an anatomical onset zone.

**Research Objective:** Capture EP001's aura semiology as standardized variables that support ILAE-consistent focal seizure classification and left-temporal localization.

**Role:** Neurologist · **Type:** Primary (clinical) data

*Caption - Structured aura semiology for EP001. The metallic taste, déjà vu, mild speech difficulty, and left-hand numbness together form a semiological signature consistent with a left (dominant) temporal onset with early perisylvian and mesial-temporal involvement.*

| Variable | Value |
|---|---|
| Aura Present | Yes |
| Metallic Taste | Yes |
| Déjà vu | Yes |
| Fear | No |
| Visual Aura | No |
| Auditory Aura | No |
| Speech Difficulty | Mild |
| Numbness | Left Hand |

## Questionnaire (Enterprise Form)

*Caption - The patient-facing questions the neurologist asks to capture this section, with response type, validation, EP001's example answer, and the derived AI feature.*

| ID | Question | Response Type | Validation | EP001 (Example) | AI Feature |
|---|---|---|---|---|---|
| NEU-0401 | Do you get any warning before a seizure? | Dropdown[Yes|No|Occasional] | one-of[...] | Yes | aura_present |
| NEU-0402 | Do you notice a metallic or unusual taste? | Dropdown[Yes|No|Occasional] | one-of[...] | Yes | aura_metallic_taste |
| NEU-0403 | Do you get a feeling of deja vu beforehand? | Yes-No | one-of[Yes|No] | Yes | aura_deja_vu |
| NEU-0404 | Do you feel a sudden sense of fear? | Yes-No | one-of[Yes|No] | No | aura_fear |
| NEU-0405 | Do you see any visual changes or lights? | Yes-No | one-of[Yes|No] | No | aura_visual |
| NEU-0406 | Do you hear any unusual sounds? | Yes-No | one-of[Yes|No] | No | aura_auditory |
| NEU-0407 | Do you have any trouble speaking beforehand? | Dropdown[None|Mild|Moderate|Global] | one-of[...] | Mild | aura_speech_difficulty |
| NEU-0408 | Do you feel any numbness or tingling, and where? | Dropdown[None|Left Hand|Right Hand|Face|Other] | one-of[...] | Left Hand | aura_numbness_location |

## Severity Scenario Model — Neurologist View

*Caption - The same assessment answered across four epilepsy severity levels from the neurologist's point of view; each variable shifts with severity. EP001 corresponds to Level 3 (Severe). Level 4 is the operational emergency — status epilepticus with seizures recurring about every 5 minutes.*

### Level 1 — Mild (Well-Controlled)
| Variable | Value |
|---|---|
| Aura Present | Yes |
| Metallic Taste | Occasional |
| Déjà vu | Yes |
| Fear | No |
| Visual Aura | No |
| Auditory Aura | No |
| Speech Difficulty | None |
| Numbness | None |

### Level 2 — Moderate (Intermediate)
| Variable | Value |
|---|---|
| Aura Present | Yes |
| Metallic Taste | Yes |
| Déjà vu | Yes |
| Fear | No |
| Visual Aura | No |
| Auditory Aura | No |
| Speech Difficulty | Mild |
| Numbness | None |

### Level 3 — Severe (Poorly Controlled) — EP001
| Variable | Value |
|---|---|
| Aura Present | Yes |
| Metallic Taste | Yes |
| Déjà vu | Yes |
| Fear | No |
| Visual Aura | No |
| Auditory Aura | No |
| Speech Difficulty | Mild |
| Numbness | Left Hand |

### Level 4 — Refractory / Status Epilepticus (Operational Emergency)
| Variable | Value |
|---|---|
| Aura Present | No (no warning; lost in status) |
| Metallic Taste | Not reportable |
| Déjà vu | Not reportable |
| Fear | Not reportable |
| Visual Aura | Not reportable |
| Auditory Aura | Not reportable |
| Speech Difficulty | Global (unresponsive) |
| Numbness | Not assessable |

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
**Reason:** The warning phase itself grades along a severity ladder. **Why:** A reliable aura permits abortive action, while loss of aura in status removes that safety margin. **What is happening:** Aura reliability degrades from a protective warning to no reportable warning in status. **How it is happening:** The neurologist reads pre-ictal symptom fields against level thresholds. **Reference:** Fisher et al. (2017).

## Data Flow and Context Diagrams

```mermaid
flowchart TD
    A[Patient Reported Warning] --> B[Neurologist Aura Interview]
    B --> C[Structured Aura Variables]
    C --> D[Focal Seizure Semiology Layer]
    D --> E[Left Temporal Localization Hypothesis]
    E --> F[Clinical Feature Vector EP001]
```

**Reason:** Shows where aura data enters the assessment pipeline. **Why:** Aura is the earliest evidence in the ictal timeline and anchors later localization. **What is happening:** Narrative warning symptoms are converted into structured variables that flow toward a localization hypothesis. **How it is happening:** The interview normalizes each symptom into a named field that joins the patient feature vector. **Reference:** Fisher et al. (2017).

```mermaid
sequenceDiagram
    participant P as Patient EP001
    participant N as Neurologist
    participant R as Data Record
    P->>N: Describes pre seizure sensations
    N->>P: Probes taste memory fear vision speech
    P->>N: Confirms metallic taste and deja vu
    N->>R: Records structured aura variables
    R-->>N: Confirms captured values
```

**Reason:** Documents the role that captures the aura. **Why:** Accurate elicitation depends on targeted probing by the neurologist. **What is happening:** The clinician queries each symptom domain and records confirmed responses. **How it is happening:** A structured question set maps patient replies to discrete fields. **Reference:** Fisher et al. (2017).

```mermaid
graph LR
    AU[Aura Section] --> SEM[Seizure Semiology]
    AU --> LOC[Localization Zone]
    AU --> LANG[Language Dominance Signal]
    SEM --> VEC[Clinical Vector]
    LOC --> VEC
    LANG --> VEC
```

**Reason:** Shows how aura links to other assessment sections. **Why:** Aura variables are not isolated and reinforce semiology, localization, and language findings. **What is happening:** The aura node fans out into related clinical dimensions that all converge on the vector. **How it is happening:** Shared variables cross-reference the aura record with adjacent sections. **Reference:** Fisher et al. (2017).

```mermaid
journey
    title EP001 Aura Experience
    section Warning Onset
      Notices metallic taste: 3: Patient
      Feels familiar deja vu: 3: Patient
    section Reporting
      Explains sensations to clinician: 4: Patient, Neurologist
      Answers targeted probes: 4: Patient, Neurologist
    section Documentation
      Sees symptoms recorded: 5: Neurologist
```

**Reason:** Captures the lived experience of the aura item. **Why:** Understanding the patient perspective improves elicitation fidelity. **What is happening:** EP001 moves from noticing warning signs to seeing them documented. **How it is happening:** The clinician guides the patient through recall and confirmation. **Reference:** Topol (2019).

## Professor Readiness (Defense Q&A)

**Q1: Why does the aura matter for localization in EP001?**
A: The aura reflects the seizure onset zone before spread. Metallic taste and déjà vu point to mesial and perisylvian temporal structures, consistent with a left-temporal focus.

**Q2: Why is mild speech difficulty significant here?**
A: Early ictal language disturbance suggests involvement of the dominant (left) hemisphere, supporting left-temporal lateralization rather than right.

**Q3: Why record negatives such as no visual or auditory aura?**
A: Documented negatives narrow the differential, arguing against occipital or lateral-temporal onset and strengthening the mesial left-temporal hypothesis.

## References

American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). American Psychological Association.

Fisher, R. S., Cross, J. H., French, J. A., Higurashi, N., Hirsch, E., Jansen, F. E., Lagae, L., Moshé, S. L., Peltola, J., Roulet Perez, E., Scheffer, I. E., & Zuberi, S. M. (2017). Operational classification of seizure types by the International League Against Epilepsy. *Epilepsia, 58*(4), 522-530. https://doi.org/10.1111/epi.13670

Topol, E. J. (2019). *Deep medicine: How artificial intelligence can make healthcare human again*. Basic Books.
