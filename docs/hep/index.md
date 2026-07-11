# Human Epilepsy Project (HEP) — Primary Dataset Index

> **Why (this doc):** One entry point to the HEP primary (clinical, longitudinal) dataset —
> the counterpart to the EEG-focused EPILEPSIAE secondary dataset.
> **How:** Links each HEP module + the cross-dataset integration framework and the 20-layer
> reference architecture. Example patient: **HEP001** (27F, temporal lobe epilepsy).

## Positioning

*Caption — why HEP and EPILEPSIAE are complementary, not duplicative.*

| Dataset | Role | Primary strength |
|---|---|---|
| EPILEPSIAE (≈ Pipelines A/B) | **Secondary** | EEG signal, seizure annotations |
| **Human Epilepsy Project** | **Primary** | Clinical assessment, longitudinal follow-up, outcomes |

## Modules

*Caption — the five HEP modules, each a canonical doc (spine + tables + 4 diagrams + Q&A + APA7).*

| # | Module | Focus |
|---|---|---|
| 1 | [Patient Registration](module-1-patient-registration.md) | Demographics, consent, social support (HEP001) |
| 2 | [Comprehensive Neurologist Assessment](module-2-neurologist-assessment.md) | Semiology, triggers, classification |
| 3 | [Comprehensive Diagnostic Investigation](module-3-diagnostic-investigation.md) | EEG+MRI+PET+neuropsych, 96% confidence |
| 4 | [Longitudinal Treatment & Follow-up](module-4-longitudinal-followup.md) | Seizure diary, survival analysis, outcomes |
| 5 | [Statistical Modeling & Predictive AI](module-5-statistical-predictive-ai.md) | Mixed-effects, survival, deep learning, fusion |

## Frameworks

*Caption — the integration and architecture docs that unify HEP with the rest of the platform.*

| Doc | Purpose |
|---|---|
| [HEP + EPILEPSIAE Integration Framework](integration-framework.md) | Variable-mapping matrix, gap analysis, master data dictionary |
| [20-Layer Reference Architecture](reference-architecture-20-layers.md) | Enterprise healthcare AI stack (L1–L20) |

## Cross-Dataset Roadmap

*Caption — how additional datasets are used (validate/extend, not rebuild).*

| Rank | Dataset | Purpose |
|---|---|---|
| 1 | EPILEPSIAE | Master EEG reference architecture (done conceptually) |
| 2 | **HEP** | Clinical + longitudinal complement (this set) |
| 3 | TUH EEG | Large-scale external validation |
| 4 | PhysioNet (Siena/CHB-MIT) | Open reproducibility |
| 5 | NINDS | Additional clinical/multimodal variables |

## References

American Psychological Association. (2020). *Publication manual of the American Psychological
Association* (7th ed.). https://doi.org/10.1037/0000165-000

Fisher, R. S., Cross, J. H., French, J. A., Higurashi, N., Hirsch, E., Jansen, F. E., Lagae,
L., Moshé, S. L., Peltola, J., Roulet Perez, E., Scheffer, I. E., & Zuberi, S. M. (2017).
Operational classification of seizure types by the International League Against Epilepsy.
*Epilepsia, 58*(4), 522–530. https://doi.org/10.1111/epi.13670
