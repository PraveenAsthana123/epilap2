# Literature — Primary (Clinical) Data Analysis in Epilepsy AI

> **Why (this doc):** A curated set of **real, verifiable** papers that analyse **primary
> clinical data** (demographics, history, seizure semiology, medications, EHR/claims, clinical
> notes) — as opposed to raw EEG signal — to predict epilepsy outcomes (drug-resistance, seizure
> recurrence, surgical outcome, treatment response). Sources were retrieved via web search
> (July 2026); URLs are included so each can be verified and read in full.
>
> **Honesty note:** entries summarise titles/abstracts from search results; verify specifics against
> the full text before citing in the dissertation.

## Drug-resistant epilepsy — clinical/EHR/claims features

| # | Study (what it addresses) | Data (primary) | Link |
|---|---|---|---|
| 1 | Predicting drug-resistant epilepsy — ML on **administrative claims** (RF AUC 0.764 vs 0.657 age/sex baseline) | claims records | [PubMed 30412924](https://pubmed.ncbi.nlm.nih.gov/30412924/) |
| 2 | Interpretable ML for drug-resistant epilepsy in children with **tuberous sclerosis** (multimodal + clinical) | clinical + EEG/MRI/genetic | [Frontiers Neurology 2025](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2025.1623212/full) |
| 3 | ML to predict **treatment success** in children with drug-resistant epilepsy (clinical + history) | clinical + medication history | [PMC12708293](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12708293/) |
| 4 | ML for **therapeutic response** in drug-resistant epilepsy — **bivariate diagnostic meta-analysis** (pooled sens/spec 0.84) | mixed clinical | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S092012112500124X) |
| 5 | **Early prediction** of drug-resistant epilepsy using **clinical + EEG features** (CNN) | clinical + EEG | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1059131123003242) |
| 6 | Drug-resistance prediction in **newly diagnosed temporal lobe epilepsy** (clinical) | clinical baseline | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1388245725000185) |

## Seizure recurrence & post-insult seizures — clinical cohorts / EHR

| # | Study | Data (primary) | Link |
|---|---|---|---|
| 7 | **EHR** predict seizures after **ischemic stroke** (ML) | EHR | [medRxiv 2024](https://www.medrxiv.org/content/10.1101/2024.01.24.24301755.full.pdf) |
| 8 | Can ML predict **late seizures after intracerebral haemorrhage**? Real-world data | EHR/real-world | [PubMed 38820686](https://pubmed.ncbi.nlm.nih.gov/38820686/) |
| 9 | Predicting **seizure recurrence** from **routine clinical notes** using **LLMs** (retrospective cohort) | clinical notes (NLP) | [PMC10695164](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10695164/) |
| 10 | Risk of recurrence after a **first unprovoked seizure** — 10-year **prospective cohort** | clinical predictors | [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0920121124001724) |
| 11 | **Prediction begins with diagnosis** — recurrence risk in the First Seizure Clinic | clinical | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1059131124002620) |
| 12 | Predictors of **early recurrent seizure** after first ED presentation (retrospective cohort) | clinical/ED | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1059131120300480) |

## Surgical / localisation using clinical + imaging concordance

| # | Study | Data (primary) | Link |
|---|---|---|---|
| 13 | Predicting **seizure outcome after epilepsy surgery** — do we need complex models, larger samples, or better data? (LR/MLP/XGBoost) | clinical predictors | [PMC10952307](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10952307/) |
| 14 | ML for **localising the epileptogenic zone** — value of **clinical-semiology + imaging concordance** | semiology + imaging | [PMC8521800](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8521800/) |

## How these map to this project
- **Drug-resistance** studies (1–6) ↔ `analysis/primary_analysis.py` `drug_resistant` target + `fusion`.
- **Recurrence** studies (7–12) ↔ `analysis/recurrence.py` (survival) — matching their cohort/time-to-event framing.
- **Surgical / concordance** (13–14) ↔ `docs/surgical-recommendation.md` + `governance.py` concordance engine.
- Common finding echoed by our pipeline: **nocturnal + focal semiology + EEG epileptiform + poor early
  response** raise risk — the exact features weighted in the primary model.

## Sources
- [Predicting DRE from claims (PubMed 30412924)](https://pubmed.ncbi.nlm.nih.gov/30412924/)
- [Interpretable ML DRE in TSC (Frontiers 2025)](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2025.1623212/full)
- [Treatment success in pediatric DRE (PMC12708293)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12708293/)
- [Therapeutic-response meta-analysis (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S092012112500124X)
- [Early DRE prediction clinical+EEG CNN (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S1059131123003242)
- [DRE in newly diagnosed TLE (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S1388245725000185)
- [EHR seizures after ischemic stroke (medRxiv)](https://www.medrxiv.org/content/10.1101/2024.01.24.24301755.full.pdf)
- [Late seizures after ICH (PubMed 38820686)](https://pubmed.ncbi.nlm.nih.gov/38820686/)
- [Seizure recurrence from notes via LLM (PMC10695164)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10695164/)
- [First unprovoked seizure 10-yr cohort (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0920121124001724)
- [First Seizure Clinic recurrence (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S1059131124002620)
- [Early recurrent seizure after ED (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S1059131120300480)
- [Seizure outcome after surgery (PMC10952307)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10952307/)
- [Epileptogenic-zone localisation concordance (PMC8521800)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8521800/)
