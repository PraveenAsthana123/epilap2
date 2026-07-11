# Neurologist Assessment — Section 1: Chief Complaint (EP001)

> **Why (this doc):** The chief complaint is the patient's own reason for the encounter and the anchor for the entire epilepsy work-up; capturing it verbatim preserves the clinical starting point for EP001. **How:** A neurologist records the presenting concern, duration, severity, and prior acute utilisation in a structured question-answer table that feeds the downstream diagnostic pipeline.

**Role:** Neurologist · **Type:** Primary (clinical) data

**Problem:** Uncontrolled recurrent focal seizures in a 29-year-old male degrade quality of life, and the initial complaint is often unstructured and hard to compare across visits.

**Research Objective:** Capture the chief complaint as discrete, machine-readable fields so it can be linked to seizure semiology, EEG, imaging, and outcome data for reproducible analysis.

*Caption - The table below records EP001's chief complaint exactly as elicited by the neurologist; it is the primary intake record that seeds every later assessment section.*

| Question | Answer |
|---|---|
| Why are you here today? | Recurrent seizures over the last 18 months |
| Primary concern | Increasing seizure frequency |
| Duration of problem | 18 months |
| Severity | 8/10 |
| Emergency visits | 2 |
| Hospital admission | 1 |
| Patient expectation | Better seizure control |

## Data Flow and Context Diagrams

```mermaid
flowchart TD
    A[Patient EP001 arrives] --> B[Neurologist elicits chief complaint]
    B --> C[Structured intake table]
    C --> D[History and seizure semiology]
    D --> E[EEG and neuroimaging orders]
    E --> F[Clinical data vector]
    F --> G[Diagnosis and treatment plan]
```

**Reason:** To show where the chief complaint sits at the head of the epilepsy assessment pipeline. **Why:** Every later data point is interpreted against this presenting concern. **What is happening:** The verbal complaint is converted into a structured record that flows into history, EEG, and imaging. **How it is happening:** The neurologist captures fields at intake and passes them forward to downstream sections. **Reference:** Fisher et al. (2017) ILAE operational classification.

```mermaid
sequenceDiagram
    participant P as Patient EP001
    participant N as Neurologist
    participant R as Intake Record
    P->>N: States reason for visit
    N->>P: Asks about duration and severity
    P->>N: Reports 18 months and 8 of 10
    N->>R: Records structured chief complaint
    R-->>N: Confirms captured fields
```

**Reason:** To show the role and turn-taking that produces the captured complaint. **Why:** The neurologist is the accountable role for accurate first-line capture. **What is happening:** A structured dialogue extracts duration, severity, and expectation. **How it is happening:** Question-answer exchange is transcribed directly into the intake record. **Reference:** Topol (2019) on high-quality clinical data capture.

```mermaid
graph LR
    CC[Chief Complaint] --> HX[History and Semiology]
    CC --> EEG[EEG Findings]
    CC --> IMG[Neuroimaging]
    CC --> OUT[Outcome Tracking]
    HX --> CV[Clinical Vector]
    EEG --> CV
    IMG --> CV
    OUT --> CV
```

**Reason:** To show how the chief complaint links to other assessment sections. **Why:** The complaint provides the clinical thread that unifies separate modalities. **What is happening:** Each section contributes features to a shared clinical vector. **How it is happening:** Fields keyed to patient EP001 join across sections into one feature space. **Reference:** Fisher et al. (2017) framework for multimodal seizure characterisation.

```mermaid
journey
    title EP001 Chief Complaint Experience
    section Arrival
      Patient describes seizures: 3: Patient
      Neurologist listens: 4: Neurologist
    section Elicitation
      Duration and severity asked: 4: Neurologist
      Patient shares expectation: 3: Patient
    section Capture
      Structured record saved: 5: Neurologist
```

**Reason:** To depict the lived experience of capturing this item. **Why:** Understanding patient and clinician effort improves data quality and rapport. **What is happening:** The patient recounts a distressing history while the clinician structures it. **How it is happening:** Empathic questioning maps subjective concern into recorded fields. **Reference:** APA (2020) guidance on patient-centred documentation.

## Professor Readiness (Defense Q&A)

**Q1: Why capture the chief complaint verbatim rather than a diagnosis?**
The complaint is the patient's own framing and is diagnostically neutral; it preserves the raw signal before clinician interpretation, supporting reproducibility.

**Q2: How does an 8/10 severity rating add value if it is subjective?**
It provides a self-reported baseline that can be tracked longitudinally to measure treatment response, even though it is not an objective seizure count.

**Q3: Why record emergency visits and admissions in the chief complaint section?**
Acute utilisation quantifies disease burden and urgency, informing risk stratification and prioritisation of the work-up.

## References

American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). American Psychological Association.

Fisher, R. S., Cross, J. H., French, J. A., Higurashi, N., Hirsch, E., Jansen, F. E., Lagae, L., Moshé, S. L., Peltola, J., Roulet Perez, E., Scheffer, I. E., & Zuberi, S. M. (2017). Operational classification of seizure types by the International League Against Epilepsy: Position paper of the ILAE Commission for Classification and Terminology. *Epilepsia, 58*(4), 522–530. https://doi.org/10.1111/epi.13670

Topol, E. J. (2019). *Deep medicine: How artificial intelligence can make healthcare human again*. Basic Books.
