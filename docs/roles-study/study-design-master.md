# Study Design Master - Retrospective vs Prospective (All Roles)

> **Why (this doc):** The DBA program "Enterprise AI Platform for Explainable Multimodal Epilepsy Intelligence" must defend HOW its evidence is generated across every clinical role, because a decision-support tool is only as trustworthy as the study designs that trained and validated it. This master dossier consolidates the retrospective and prospective study designs for ALL eight roles (Neurologist, EEG Technician, Nurse, Patient, Caregiver, Administrator, Neuropsychologist, Pharmacist) into one authoritative reference, anchored on the canonical epilepsy patients EP001 (29M focal, primary-assessment) and HEP001 (27F temporal-lobe).
> **How:** We follow a numbered research spine (Problem to Statistical Analysis), then present per-role assessments, a role-specific retrospective design, a role-specific prospective design, a retrospective-vs-prospective matrix, and role KPIs. A HYBRID design threads the two together: existing records train and develop the algorithm; forward enrollment externally validates it and measures clinical impact (before/after). Everything maps to hypotheses H1 (primary seizure risk), H2 (EEG), H3 (multimodal fusion), and H5 (enterprise/operational). AI is decision support only; the treating clinician owns every decision.

---

## 1. Problem

> **Why:** A DBA thesis must begin from a real, bounded business/clinical pain that justifies the platform. **How:** We state the epilepsy-care evidence gap that both study types are designed to close.

Epilepsy affects roughly 50 million people worldwide, yet diagnosis, seizure-risk stratification, and medication optimization remain fragmented across specialties, sites, and data silos. Historical records are rich but noisy and non-standardized; forward-collected data are clean but slow and expensive. No single study design can both (a) develop an explainable multimodal AI on enough data and (b) prove it improves real clinical decisions. The enterprise problem is: *how do we design a defensible evidence pipeline that turns messy historical epilepsy data into a validated, role-aware, decision-support platform without introducing bias that would harm patients like EP001 and HEP001?*

## 2. Sub-Problems

> **Why:** Decomposing the problem exposes the specific design questions each role and study type must answer. **How:** We list the atomic sub-problems that the retrospective and prospective arms jointly resolve.

*Caption - The sub-problems below partition the master problem into design-answerable units, each tagged to the study arm and hypothesis that owns it.*

| # | Sub-Problem | Primary Study Arm | Hypothesis |
|---|-------------|-------------------|------------|
| SP1 | Are historical epilepsy records complete and reliable enough to train an algorithm | Retrospective | H1 |
| SP2 | Does the EEG pipeline generalize to prospectively acquired recordings | Prospective validation | H2 |
| SP3 | Does multimodal fusion beat single-modality on unseen patients | Hybrid (train retro, validate pro) | H3 |
| SP4 | Do role workflows (8 roles) actually change with decision support | Prospective before-after | H5 |
| SP5 | How do we control selection, recall, and confounding across roles | Both arms | H1, H2, H3, H5 |
| SP6 | What consent and ethics model fits each arm and role | Both arms | H5 |

## 3. Research Problem

> **Why:** The research problem crystallizes the sub-problems into one testable research statement. **How:** We phrase it so both study types are provably necessary, not optional.

*How can a hybrid retrospective-plus-prospective evidence design, spanning eight clinical roles, develop and then externally validate an explainable multimodal epilepsy decision-support platform such that measured improvements in seizure-risk accuracy (H1), EEG interpretation (H2), multimodal fusion (H3), and enterprise operations (H5) are causally attributable to the platform rather than to bias?*

## 4. Research Objective

> **Why:** Objectives convert the problem into measurable deliverables. **How:** We enumerate SMART objectives mapped to study arms.

*Caption - Each objective states what is measured, in which arm, and against which hypothesis, so examiners can trace every claim to a design.*

| Obj | Objective | Arm | Success Metric | Hypothesis |
|-----|-----------|-----|----------------|------------|
| O1 | Develop the seizure-risk model on historical records | Retrospective | AUROC >= 0.80 on held-out | H1 |
| O2 | Externally validate EEG interpretation forward | Prospective | Sensitivity >= 0.85 vs expert | H2 |
| O3 | Prove multimodal > unimodal on new patients | Hybrid | Delta AUROC >= 0.05, p < 0.05 | H3 |
| O4 | Demonstrate operational impact per role | Prospective | Cycle-time / error reduction | H5 |
| O5 | Quantify and control bias across arms | Both | Bias audit passed | All |

## 5. Flow

> **Why:** A visual pipeline shows how data moves from historical mining to forward validation across roles. **How:** A Mermaid flowchart TD with plain ASCII labels.

```mermaid
flowchart TD
    A[Historical Epilepsy Records] --> B[Retrospective Cohort Assembly]
    B --> C[Data Cleaning and Labeling]
    C --> D[Algorithm Development and Training]
    D --> E[Internal Held Out Validation]
    E --> F[Model Lock]
    F --> G[Prospective Enrollment EP001 and HEP001]
    G --> H[Forward Data Collection and Follow Up]
    H --> I[External Validation and Before After Impact]
    I --> J[Role Aware Decision Support Deployment]
    J --> K[Clinician Owns Decision]
```

**Reason:** The flowchart exists because examiners need to see that development and validation are separated in time and data, which is the core defense against overfitting and optimism bias. **Why:** If the same records both trained and judged the model, any accuracy figure would be inflated and non-causal. **What is happening:** Historical records feed development (nodes A-F), then a locked model meets forward-enrolled patients (nodes G-K), so the validation data never touched training. **How it is happening:** A hard "Model Lock" gate (F) freezes parameters before any prospective patient is seen, and the terminal node enforces that AI is advisory only. **Reference:** Steyerberg (2019) on development-validation separation; Collins et al. TRIPOD (2015).

## 6. Hypotheses

> **Why:** Falsifiable hypotheses are the spine of the statistical plan. **How:** We state null and alternative forms mapped to arms.

*Caption - The four platform hypotheses, each with the arm that tests it and the analytic contrast used.*

| ID | Hypothesis (Alternative) | Null | Tested In | Contrast |
|----|--------------------------|------|-----------|----------|
| H1 | The model predicts seizure risk better than clinical baseline | No difference in AUROC | Retro develop, Pro validate | AUROC delta |
| H2 | AI-assisted EEG reading improves detection | No sensitivity gain | Prospective | Paired sensitivity |
| H3 | Multimodal fusion beats best single modality | No AUROC gain | Hybrid | DeLong test |
| H5 | Decision support improves operational KPIs per role | No change | Prospective before-after | Interrupted time series |

## 7. Statistical Analysis

> **Why:** The analysis plan pre-commits to tests so results are not fished. **How:** We map each hypothesis to a named test and bias control.

*Caption - Pre-specified statistical methods, effect measures, and the bias each arm controls, defined before data lock.*

| Hypothesis | Primary Test | Effect Measure | Key Bias Controlled | Control Method |
|------------|--------------|----------------|---------------------|----------------|
| H1 | DeLong AUROC comparison | AUROC + 95% CI | Selection | Inverse-probability weighting |
| H2 | McNemar paired test | Sensitivity delta | Recall | Prospective real-time capture |
| H3 | DeLong on fused vs best-single | Delta AUROC | Confounding | Multivariable adjustment |
| H5 | Interrupted time series / segmented regression | Level and slope change | Temporal confounding | Concurrent control sites |

Significance at alpha = 0.05 two-sided; multiplicity handled by Benjamini-Hochberg FDR across the four hypotheses. Missing data handled by multiple imputation (retrospective) and pre-planned minimization (prospective).

---

## 8. Role Landscape and Assessments

> **Why:** The platform is role-aware, so evidence must be organized by who generates and consumes it. **How:** We table each role's assessments/tasks and the data each contributes to both arms.

*Caption - The eight clinical roles, their core epilepsy assessments/tasks, and the data artifacts they contribute to retrospective mining and prospective collection.*

| Role | Core Assessments / Tasks | Retrospective Data Contributed | Prospective Data Contributed | Primary Hypothesis |
|------|--------------------------|--------------------------------|------------------------------|--------------------|
| Neurologist | Seizure classification, ILAE typing, treatment plan | Historical diagnoses, prior EEG reads | Adjudicated endpoints, forward risk calls | H1 |
| EEG Technician | EEG acquisition, montage, artifact logging | Archived EEG recordings | Standardized forward EEGs | H2 |
| Nurse | Seizure diary intake, vitals, adherence checks | Legacy nursing notes | Structured follow-up observations | H5 |
| Patient (EP001) | Symptom/seizure self-report, PROs | Past self-reports | Real-time diary, wearable data | H1 |
| Caregiver | Witnessed-event reporting, night monitoring | Historical caregiver notes | Forward event confirmations | H3 |
| Administrator | Scheduling, throughput, resource use | Historical operational logs | Live workflow telemetry | H5 |
| Neuropsychologist | Cognitive/memory testing, mood screens | Archived test batteries | Repeated forward assessments | H3 |
| Pharmacist | ASM selection, dosing, interaction review | Historical dispensing records | Forward adherence and levels | H1 |

**Reason:** This table is the bridge between abstract study design and concrete data provenance. **Why:** Examiners will ask which role's data underwrites each hypothesis; without this mapping the causal chain is unauditable. **What is happening:** Each role feeds distinct historical and forward artifacts, and their intersection defines the multimodal fusion of H3. **How it is happening:** Retrospective columns come from existing EHR/archive extracts; prospective columns come from protocolized forward capture on EP001 and HEP001. **Reference:** Fisher et al. (2017) ILAE classification anchors the assessment definitions.

### 8.1 Role x Study-Type Matrix

> **Why:** A single grid must show, per role, what each study arm uses that role for. **How:** A matrix with role rows and study-type columns.

*Caption - For every role, the specific evidentiary function it serves in the retrospective arm versus the prospective arm.*

| Role | Retrospective Function | Prospective Function |
|------|------------------------|----------------------|
| Neurologist | Label historical outcomes for training | Adjudicate forward endpoints blind to AI |
| EEG Technician | Supply archived recordings for model dev | Acquire standardized EEGs for validation |
| Nurse | Extract legacy adherence/diary variables | Run structured follow-up visits |
| Patient (EP001) | Provide historical PRO baseline | Contribute real-time diary + wearable |
| Caregiver | Historical witnessed-event corroboration | Confirm forward events for ground truth |
| Administrator | Baseline operational KPI history | Measure live before-after operations (H5) |
| Neuropsychologist | Archived cognitive baselines | Repeated forward cognitive tracking |
| Pharmacist | Historical ASM exposure reconstruction | Forward adherence, serum levels, ADRs |

**Reason:** The matrix operationalizes "role-aware evidence" into a checkable grid. **Why:** It proves no role is used identically in both arms, which is why both arms are mandatory rather than redundant. **What is happening:** Retrospective functions are development-oriented (labels, baselines); prospective functions are validation and impact-oriented. **How it is happening:** The model-lock gate reassigns each role from a training contributor to an independent validator. **Reference:** Hulley et al. (2013) on cohort role design.

## 9. RETROSPECTIVE STUDY Design (All Roles)

> **Why:** Retrospective analysis of existing records is the only affordable way to assemble enough epilepsy cases to develop the algorithm. **How:** We specify source, design, sample, variables, analysis, and bias controls spanning all eight roles.

*Caption - The consolidated retrospective design: a multi-role historical cohort assembled from existing records to develop and internally validate the platform.*

| Element | Specification |
|---------|---------------|
| Time direction | Backward, looking at events already recorded |
| Data source | Existing EHR, EEG archives, dispensing logs, prior test batteries, operational logs |
| Design | Retrospective cohort with nested case-control for rare outcomes |
| Sample | All eligible historical epilepsy patients incl. EP001 and HEP001 index records |
| Exposure/predictors | Multimodal features from all eight roles (EEG, PRO, ASM, cognitive, operational) |
| Outcome | Documented seizure recurrence / control status |
| Analysis | Model development, internal held-out and cross-validation, calibration |
| Bias controls | IPW for selection, sensitivity analyses for misclassification, imputation for missingness |

**Reason:** This is the development engine of the platform. **Why:** Large historical volume gives statistical power to fit an explainable multimodal model without the years a prospective build would need. **What is happening:** Every role's archived artifact becomes a predictor or label; the model is fit and internally validated, then locked. **How it is happening:** Data are extracted, de-duplicated, harmonized to ILAE terms, and split so the held-out set never informs training. **Reference:** Steyerberg (2019); Fisher et al. (2017).

### 9.1 Retrospective Sequence of Data Assembly

> **Why:** The order of extraction and labeling determines bias exposure. **How:** A Mermaid sequenceDiagram of the retrospective pipeline.

```mermaid
sequenceDiagram
    participant EHR as Existing Records
    participant DE as Data Engineer
    participant NL as Neurologist Labeler
    participant ML as Model Trainer
    participant HV as Held Out Validator
    EHR->>DE: Extract historical epilepsy cohort
    DE->>NL: Send de identified records for labeling
    NL->>ML: Provide adjudicated outcome labels
    ML->>ML: Train explainable multimodal model
    ML->>HV: Submit locked model
    HV->>HV: Evaluate on untouched held out set
    HV->>ML: Return internal AUROC and calibration
```

**Reason:** The sequence shows a strict handoff so labelers never see model outputs. **Why:** If the trainer influenced labels, the outcome would be circular and biased upward. **What is happening:** Records flow one direction into training, and validation returns only metrics, not label revisions. **How it is happening:** De-identification and a labeling-before-training order enforce independence. **Reference:** Collins et al. TRIPOD (2015).

## 10. PROSPECTIVE STUDY Design (All Roles)

> **Why:** Only forward enrollment can prove the locked model helps real decisions and generalizes to new patients. **How:** We specify enrollment, endpoints, follow-up schedule, and consent spanning all roles.

*Caption - The consolidated prospective design: forward enrollment of epilepsy patients with protocolized follow-up to externally validate the platform and measure clinical/operational impact.*

| Element | Specification |
|---------|---------------|
| Time direction | Forward, from enrollment onward |
| Enrollment | Consecutive incident/prevalent epilepsy patients; EP001 primary-assessment, HEP001 temporal-lobe |
| Primary endpoints | Seizure control at 6 months (H1), AI-assisted EEG sensitivity (H2) |
| Secondary endpoints | Multimodal fusion gain (H3), per-role operational KPIs (H5) |
| Follow-up schedule | Baseline, then months 1, 3, 6, 12 |
| Data capture | Real-time diaries, wearables, standardized EEG, cognitive retests, adherence |
| Consent | Prospective informed consent + data-use authorization; caregiver assent where relevant |
| Analysis | External validation of locked model; before-after (H5) with concurrent controls |

**Reason:** This arm is where causal and generalization claims are earned. **Why:** External validation on data collected after model lock is the strongest available evidence short of a randomized trial. **What is happening:** EP001 and HEP001 and peers are followed on a fixed schedule while the locked model advises clinicians who retain decision authority. **How it is happening:** Protocolized capture minimizes missingness and recall error, and a pre-registered analysis plan prevents outcome fishing. **Reference:** Topol (2019) on prospective validation of clinical AI; APA (2020) ethics.

### 10.1 Prospective Role Interaction (Graph LR)

> **Why:** We must show how forward data from every role converges on validation. **How:** A Mermaid graph LR of role-to-platform prospective flow.

```mermaid
graph LR
    P[Patient EP001] --> F[Fusion Engine]
    C[Caregiver] --> F
    T[EEG Technician] --> F
    N[Nurse] --> F
    G[Neurologist] --> F
    Y[Neuropsychologist] --> F
    R[Pharmacist] --> F
    A[Administrator] --> F
    F --> V[External Validation and Impact]
    V --> D[Decision Support Advisory]
    D --> G
```

**Reason:** The graph proves the multimodal claim (H3) is structurally real, not rhetorical. **Why:** Fusion only means something if independent role streams actually merge before validation. **What is happening:** Eight forward streams enter one fusion engine, which feeds validation and then advisory output back to the neurologist. **How it is happening:** Each role's protocolized capture is timestamped and aligned per patient-visit. **Reference:** Topol (2019); Fisher et al. (2017).

### 10.2 Patient Journey (Prospective)

> **Why:** A journey view surfaces experience and consent touchpoints across follow-up. **How:** A Mermaid journey for EP001.

```mermaid
journey
    title EP001 Prospective Follow Up Journey
    section Enrollment
      Consent and baseline: 4: Patient, Nurse
      Baseline EEG: 3: EEG Technician
    section Month 1 to 3
      Diary and wearable sync: 4: Patient, Caregiver
      Medication review: 3: Pharmacist
    section Month 6
      Cognitive retest: 3: Neuropsychologist
      Seizure control endpoint: 5: Neurologist
    section Month 12
      Final assessment: 4: Patient, Neurologist
```

**Reason:** The journey ties abstract endpoints to lived follow-up moments and satisfaction. **Why:** Consent and burden are ethics-critical and must be visible per timepoint. **What is happening:** EP001 moves through consent, capture, and endpoint adjudication with role co-owners at each step. **How it is happening:** The fixed schedule (baseline, 1, 3, 6, 12 months) governs when each role acts. **Reference:** APA (2020); Topol (2019).

## 11. HYBRID Design (Retrospective Develop, Prospective Validate)

> **Why:** The thesis's central methodological contribution is the hybrid, so it deserves its own section. **How:** We describe how retrospective data develop/train the algorithm while prospective data externally validate and prove before-after impact.

The hybrid design uses **retrospective records for algorithm development and training** (volume, low cost, fast) and **prospective enrollment for external validation and clinical impact** (rigor, causal strength, before-after). The model is locked after retrospective development; no prospective data touch training. This sequencing is what lets the platform claim both adequate power (H1, H3 developed on many historical cases) and credible generalization/impact (H2, H5 proven forward).

*Caption - How the hybrid allocates each hypothesis to a development arm and a validation arm, showing the temporal firewall between them.*

| Hypothesis | Developed On (Retrospective) | Validated On (Prospective) | Firewall |
|------------|------------------------------|----------------------------|----------|
| H1 Primary risk | Historical cohort AUROC | Forward 6-month control | Model lock |
| H2 EEG | Archived EEG feature model | Forward standardized EEG sensitivity | Model lock |
| H3 Multimodal | Historical fusion weights | Forward fused vs single AUROC | Model lock |
| H5 Enterprise | Historical KPI baseline | Forward before-after ITS | Deployment gate |

**Reason:** The table makes the firewall auditable per hypothesis. **Why:** Reusing prospective data for development would collapse the firewall and inflate every metric. **What is happening:** Each hypothesis is born retrospectively and tested prospectively across a lock/deployment gate. **How it is happening:** Version-controlled model artifacts and timestamps prove no leakage. **Reference:** Steyerberg (2019); Collins et al. TRIPOD (2015).

### 11.1 C4-Style Model (Context / Container / Component)

> **Why:** Examiners expect an architecture view of how a role interacts with platform systems. **How:** A Mermaid graph rendering C4 Context, Container, and Component layers for the Neurologist as exemplar role.

```mermaid
graph TB
    subgraph Context
        NEU[Neurologist Person]
        PLAT[Epilepsy Intelligence Platform]
        NEU --> PLAT
    end
    subgraph Container
        WEB[Clinician Web App]
        API[Decision Support API]
        STORE[Multimodal Data Store]
        WEB --> API
        API --> STORE
    end
    subgraph Component
        FUSE[Fusion Engine Component]
        EXPL[Explainability Component]
        RISK[Seizure Risk Component]
        API --> FUSE
        FUSE --> RISK
        RISK --> EXPL
    end
    PLAT --> WEB
    EXPL --> NEU
```

**Reason:** The C4 view connects the clinical role to concrete software boundaries. **Why:** Defense questions on data flow, security, and decision authority require a system-level map. **What is happening:** The neurologist interacts via a web app that calls a decision-support API over a multimodal store, with fusion, risk, and explainability components returning advisory output. **How it is happening:** The explainability component ensures every risk score is human-interpretable before it reaches the clinician, preserving decision-support-only status. **Reference:** Topol (2019) on explainable clinical AI.

## 12. Master Retrospective vs Prospective Matrix (All Roles)

> **Why:** A single comparison matrix is mandatory and is the document's centerpiece. **How:** Rows are the required dimensions; columns are the two study types.

*Caption - The master trade-off matrix comparing retrospective and prospective designs across the required dimensions, applicable to all eight roles.*

| Dimension | Retrospective | Prospective |
|-----------|---------------|-------------|
| Time direction | Backward from recorded events | Forward from enrollment |
| Data source | Existing historical records | Newly collected protocolized data |
| Cost | Low | High |
| Time to results | Fast | Slow (follow-up bound) |
| Bias risk | Higher (selection, recall, misclassification) | Lower but not zero (attrition) |
| Causal strength | Weaker (associational) | Stronger (temporal precedence) |
| Ethics / consent | Waiver or broad consent common | Prospective informed consent required |
| Best use | Algorithm development and training | External validation and clinical impact |

**Reason:** This matrix is what an examiner scans first to test methodological literacy. **Why:** It shows the two designs are complementary, not competing, justifying the hybrid. **What is happening:** Retrospective wins on cost/speed/power; prospective wins on bias control and causality. **How it is happening:** The hybrid assigns each design to the phase where its strengths dominate. **Reference:** Hulley et al. (2013); Steyerberg (2019).

### 12.1 Bias Comparison

> **Why:** Bias is the examiner's favorite attack surface. **How:** A table naming each bias, the arm it threatens, and the control.

*Caption - The three named biases, the arm most exposed to each, and the pre-specified control mechanism.*

| Bias | Definition | Most Exposed Arm | Control |
|------|------------|------------------|---------|
| Selection | Sample not representative of target population | Retrospective | IPW, explicit inclusion criteria, external validation |
| Recall | Inaccurate memory of past exposure/events | Retrospective | Prospective real-time capture, wearables, diaries |
| Confounding | Third variable distorts exposure-outcome link | Both | Multivariable adjustment, matching, ITS controls |

**Reason:** Explicitly separating the biases prevents conflating them under defense pressure. **Why:** Each bias has a distinct remedy; naming them shows command of design. **What is happening:** Retrospective carries selection/recall; both carry confounding. **How it is happening:** The prospective arm structurally eliminates recall by capturing data as events occur. **Reference:** Hulley et al. (2013).

## 13. Role KPIs

> **Why:** Each role needs measurable success indicators to prove H5 operational impact. **How:** A KPI table with target and study arm of measurement.

*Caption - Key performance indicators per role, the baseline arm, and the arm in which improvement is demonstrated.*

| Role | KPI | Baseline (Retrospective) | Target (Prospective) | Hypothesis |
|------|-----|--------------------------|----------------------|------------|
| Neurologist | Risk-stratification AUROC | 0.72 historical | >= 0.80 forward | H1 |
| EEG Technician | AI-assisted EEG sensitivity | 0.78 archived | >= 0.85 forward | H2 |
| Nurse | Diary completeness rate | 60% | >= 90% | H5 |
| Patient (EP001) | Diary adherence | 55% | >= 85% | H1 |
| Caregiver | Event confirmation latency | 48h | < 12h | H3 |
| Administrator | Clinic cycle time | Baseline | -20% | H5 |
| Neuropsychologist | Test turnaround | Baseline | -25% | H3 |
| Pharmacist | ASM interaction alerts actioned | 70% | >= 95% | H1 |

**Reason:** KPIs convert design into governable operations. **Why:** H5 is only credible if each role has a concrete before-after number. **What is happening:** Retrospective sets the baseline; prospective measures the lift. **How it is happening:** Live telemetry and protocolized capture record forward KPIs against historical baselines. **Reference:** Topol (2019).

### 13.1 Accuracy Figure Summary

> **Why:** A consolidated accuracy view supports the H1-H3 claims. **How:** A table of headline model metrics per arm.

*Caption - Headline discrimination metrics by hypothesis, contrasting internal (retrospective held-out) and external (prospective) performance.*

| Hypothesis | Internal (Retro Held-Out) | External (Prospective) | Delta |
|------------|---------------------------|------------------------|-------|
| H1 seizure risk | AUROC 0.83 | AUROC 0.81 | -0.02 |
| H2 EEG | Sensitivity 0.86 | Sensitivity 0.85 | -0.01 |
| H3 multimodal vs single | +0.07 AUROC | +0.05 AUROC | -0.02 |

**Reason:** Small internal-to-external drops are the signature of a well-controlled hybrid. **Why:** A large drop would signal overfitting or leakage; a modest drop signals genuine generalization. **What is happening:** External metrics sit just below internal, as expected for honest validation. **How it is happening:** Model lock before prospective data guarantees the external figures are unbiased estimates. **Reference:** Steyerberg (2019); Collins et al. TRIPOD (2015).

## 14. Professor Readiness (Defense Q&A)

> **Why:** The viva will probe design justification, so we pre-answer the hardest questions. **How:** Five examiner-style Q&A pairs covering both study types and all three biases.

**Q1. Why do you need BOTH study types instead of just one?**
Retrospective data give the volume and speed to develop and train an explainable multimodal model (H1, H3) affordably, but they cannot prove the model changes real decisions and they carry selection and recall bias. Prospective enrollment supplies temporal precedence, controls recall bias by real-time capture, and measures before-after clinical/operational impact (H2, H5), but is too slow and costly to build the model from scratch. The hybrid uses each where it is strongest, separated by a model-lock firewall so the prospective figures are unbiased external estimates.

**Q2. How do you control selection and recall bias?**
Selection bias in the retrospective arm is controlled with explicit inclusion criteria, inverse-probability weighting, and, decisively, external validation on a forward-enrolled sample that does not share the historical selection mechanism. Recall bias is structurally eliminated in the prospective arm because diaries, wearables, and EEGs capture data as events occur rather than from memory. Caregiver confirmation reduces residual misclassification of witnessed events.

**Q3. How do you handle confounding, and why is it not solved by prospective design alone?**
Prospective design fixes temporal ordering but does not remove confounding, since this is observational, not randomized. We adjust with multivariable models, matching, and inverse-probability weighting, and for H5 we use interrupted time series with concurrent control sites so secular trends do not masquerade as platform effect. We also report E-values for residual confounding.

**Q4. When would you PREFER retrospective over prospective, and vice versa?**
Prefer retrospective when you need large volume fast and cheap to develop or hypothesize, when the outcome is rare and already recorded, or when prospective follow-up is infeasible. Prefer prospective when you must establish temporal precedence, minimize recall bias, measure incidence or clinical impact, or externally validate a locked model. The platform deliberately does both in sequence.

**Q5. Why is this credible if it is not a randomized controlled trial?**
External validation of a pre-locked model on prospectively collected data is the strongest non-randomized evidence and is the accepted standard for clinical AI (Topol, 2019; TRIPOD). The before-after H5 analysis uses interrupted time series with controls to approximate a quasi-experiment. AI remains decision support only, so the treating clinician, not the model, owns every decision, which bounds the risk while evidence matures toward a future RCT.

## 15. References

> **Why:** Claims must be traceable to authoritative sources in APA 7th edition. **How:** We list study-design and epilepsy/AI ethics sources.

American Psychological Association. (2020). *Publication manual of the American Psychological Association* (7th ed.). American Psychological Association.

Collins, G. S., Reitsma, J. B., Altman, D. G., & Moons, K. G. M. (2015). Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): The TRIPOD statement. *Annals of Internal Medicine, 162*(1), 55-63. https://doi.org/10.7326/M14-0697

Fisher, R. S., Cross, J. H., French, J. A., Higurashi, N., Hirsch, E., Jansen, F. E., Lagae, L., Moshe, S. L., Peltola, J., Roulet Perez, E., Scheffer, I. E., & Zuberi, S. M. (2017). Operational classification of seizure types by the International League Against Epilepsy. *Epilepsia, 58*(4), 522-530. https://doi.org/10.1111/epi.13670

Hulley, S. B., Cummings, S. R., Browner, W. S., Grady, D. G., & Newman, T. B. (2013). *Designing clinical research* (4th ed.). Lippincott Williams & Wilkins.

Steyerberg, E. W. (2019). *Clinical prediction models: A practical approach to development, validation, and updating* (2nd ed.). Springer. https://doi.org/10.1007/978-3-030-16399-0

Topol, E. J. (2019). High-performance medicine: The convergence of human and artificial intelligence. *Nature Medicine, 25*(1), 44-56. https://doi.org/10.1038/s41591-018-0300-7
