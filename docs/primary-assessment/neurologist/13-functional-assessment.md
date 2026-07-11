# Neurologist Assessment — Section 13: Functional Assessment (EP001)

> **Why (this doc):** Epilepsy affects daily life beyond seizure counts; functional status captures how focal impaired awareness seizures constrain driving, work, and safety for EP001. **How:** The neurologist records structured functional variables during the primary clinical visit, which feed the patient's composite clinical vector for downstream analysis.

**Problem:** Seizure frequency alone underrepresents the real-world burden of focal epilepsy, leaving functional impairment and injury risk poorly quantified.

**Research Objective:** Capture standardized functional-assessment variables for EP001 so that everyday-life impact and safety risk can be modeled alongside neurological findings.

**Role:** Neurologist · **Type:** Primary (clinical) data

*Caption - This table records EP001's functional status across driving, occupational impact, activities of daily living, and injury risk. It is present because these variables translate seizure burden into measurable real-world function.*

| Variable | Value |
|---|---|
| Driving | Restricted |
| Employment Impact | Moderate |
| ADL | Independent |
| IADL | Independent |
| Work Productivity | Reduced |
| Falls | 1 |
| Injury Risk | Moderate |

## Data Flow and Context Diagrams

```mermaid
flowchart TD
    A[Neurologist Visit] --> B[Functional Assessment Capture]
    B --> C[Driving and Employment Status]
    B --> D[ADL and IADL Status]
    B --> E[Falls and Injury Risk]
    C --> F[Clinical Vector EP001]
    D --> F
    E --> F
    F --> G[Analytics Pipeline]
```

**Reason:** To show where functional data enters the epilepsy data pipeline. **Why:** Readers must see that functional variables are not isolated but converge into the patient clinical vector. **What is happening:** Captured items flow from the visit into structured fields and then into the composite vector. **How it is happening:** The neurologist records each variable, which is normalized and merged with other sections. **Reference:** Fisher et al. (2017).

```mermaid
sequenceDiagram
    participant P as Patient EP001
    participant N as Neurologist
    participant R as Record System
    N->>P: Ask about driving and work impact
    P->>N: Report restrictions and reduced productivity
    N->>P: Ask about falls and daily activities
    P->>N: Report one fall and independent ADL
    N->>R: Enter functional assessment values
    R->>N: Confirm stored record
```

**Reason:** To document the role interaction that produces this data. **Why:** The reliability of functional data depends on the structured clinician-patient exchange. **What is happening:** The neurologist elicits functional status and records it. **How it is happening:** Through directed questioning during the primary assessment and entry into the record system. **Reference:** Topol (2019).

```mermaid
graph LR
    FA[Functional Assessment] --> SZ[Seizure History Section]
    FA --> QOL[Quality of Life Section]
    FA --> PSY[Psychosocial Section]
    FA --> CV[Clinical Vector]
    SZ --> CV
    QOL --> CV
    PSY --> CV
```

**Reason:** To map how functional data links to other assessment sections. **Why:** Functional impairment is interpreted in context with seizure and quality-of-life data. **What is happening:** This section cross-connects to related domains and the clinical vector. **How it is happening:** Shared patient identifiers link section outputs into one integrated vector. **Reference:** Fisher et al. (2017).

```mermaid
journey
    title EP001 Functional Assessment Experience
    section Discussion
      Discuss driving restriction: 2: Patient
      Discuss work productivity: 3: Patient
    section Safety
      Report recent fall: 2: Patient
      Confirm independent living: 4: Patient
    section Recording
      Review captured values: 4: Neurologist
```

**Reason:** To convey the lived experience of capturing this item. **Why:** Understanding patient sentiment highlights sensitive topics like driving loss. **What is happening:** EP001 moves through discussion, safety, and recording steps. **How it is happening:** The neurologist guides the patient through each functional topic and confirms values. **Reference:** APA (2020).

## Professor Readiness (Defense Q&A)

**Q1: Why capture functional status when seizure frequency is already recorded?**
A: Seizure counts do not reflect real-world impact; functional variables like driving restriction and injury risk quantify the everyday burden that drives clinical decisions.

**Q2: Why is EP001 listed as Independent for ADL but with Restricted driving?**
A: Basic self-care is preserved, but focal impaired awareness seizures create sudden risk during driving, so a safety-based restriction applies independent of self-care ability.

**Q3: How does one fall translate to Moderate injury risk?**
A: Injury risk integrates fall history with seizure type and awareness impairment; even a single fall in a patient with impaired-awareness seizures signals meaningful ongoing risk.

## References

American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). American Psychological Association.

Fisher, R. S., Cross, J. H., French, J. A., Higurashi, N., Hirsch, E., Jansen, F. E., Lagae, L., Moshé, S. L., Peltola, J., Roulet Perez, E., Scheffer, I. E., & Zuberi, S. M. (2017). Operational classification of seizure types by the International League Against Epilepsy. *Epilepsia, 58*(4), 522-530. https://doi.org/10.1111/epi.13670

Topol, E. J. (2019). *Deep medicine: How artificial intelligence can make healthcare human again*. Basic Books.
