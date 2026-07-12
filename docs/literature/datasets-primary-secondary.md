# Datasets — Primary, Secondary & Same-Patient Multimodal (Epilepsy)

> **Why (this doc):** Real, mostly open-access datasets for the **primary** (clinical) and
> **secondary** (EEG/imaging) arms, plus **same-patient multimodal** datasets (one patient with both
> clinical + EEG + imaging) that suit the fusion work — with a shortlist of **3–4 to actually use**.
> Retrieved via web search (July 2026); verify licence + access before use.

## Secondary (EEG) — small → large

*Caption - Public EEG datasets, sorted small → large; the small ones are ideal to start.*

| Dataset | Size | Notes | Link |
|---|---|---|---|
| **Bonn University EEG** | very small (5 sets ×100 segments) | classic 2001 benchmark; interictal/ictal | [review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10235576/) |
| **UCI Epileptic Seizure Recognition** | 11,500 × 178 (tabular) | Bonn data reshaped to CSV; quick modelling | [Kaggle/UCI mirror] |
| **EEG-Eye-State** (used here) | 14,976 × 14 | real EEG, binary; used in `real_eeg_analysis.py` | OpenML |
| **Siena Scalp EEG** ⭐ | **14 patients**, 512 Hz, 47 seizures | small, real epilepsy, EDF; PhysioNet | [review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10235576/) |
| **CHB-MIT Scalp EEG** | 23 pediatric, 22 ch, 256 Hz | seizure-annotated; PhysioNet | [IEEE DataPort](https://ieee-dataport.org/open-access/preprocessed-chb-mit-scalp-eeg-database) |
| **Helsinki University Hospital** | 79 subjects | neonatal seizures | [review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10235576/) |
| **TUH EEG Seizure Corpus (TUSZ)** | 592+ subjects (10,874 pts total corpus) | largest free; requires registration | [review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10235576/) |

## Same-patient MULTIMODAL (clinical + EEG + imaging) — for fusion

*Caption - Datasets where the SAME patient has multiple modalities — exactly what multimodal fusion needs.*

| Dataset | Modalities per patient | N | Link |
|---|---|---|---|
| **Open Database of Epileptic EEG with MRI + post-op outcome** ⭐ | EEG + MRI + surgical outcome | 23 drug-resistant, operated | [PMC2974908](https://pmc.ncbi.nlm.nih.gov/articles/PMC2974908/) |
| **Paired 3T & 7T MRI + intracranial EEG** | T1/T2/FLAIR/rs-fMRI + iEEG (15 of 30) | 30 drug-resistant focal | [Nature Sci Data 2026](https://www.nature.com/articles/s41597-026-07540-5) |
| **Epilepsy-iEEG-Multicenter** (OpenNeuro ds003029) | iEEG (+ imaging via BIDS) | multi-centre | [OpenNeuro](https://openneuro.org/datasets/ds003029/versions/1.0.7) |
| **Simultaneous EEG-fMRI** | EEG + fMRI (same session) | large | [PMC10585622](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10585622/) |

## Primary (clinical) — honest note
Truly **open primary clinical** epilepsy datasets (demographics, history, meds, PROs) are **rare** —
they live in restricted EHR/registries needing a clinical collaborator + IRB. Accessible stand-ins:
the tabular UCI/EEG sets above, this repo's **synthetic cohort**, or a **retrospective linked hospital
extract** via a collaborator (the recommended route for the clinical-validation arm).

## ⭐ Recommended 3–4 to use

| Priority | Dataset | Arm | Why |
|---|---|---|---|
| 1 | **Siena Scalp EEG** | Secondary | Small, real epilepsy EDF → plugs straight into `analysis/eeg_signal_pipeline.py` via `fetch_siena.py` |
| 2 | **Open Database EEG + MRI + post-op** | **Same-patient multimodal** | 23 patients with EEG + MRI + outcome → matches the **fusion + presurgical** work |
| 3 | **CHB-MIT** | Secondary | Seizure-annotated → detection/validation |
| 4 | **UCI Epileptic Seizure Recognition** (+ EEG-Eye-State, already integrated) | Secondary (tabular) | Tiny + fast → quick real-data classification |

## Sources
- [EEG datasets review (Wong 2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10235576/) ·
  [CHB-MIT (IEEE DataPort)](https://ieee-dataport.org/open-access/preprocessed-chb-mit-scalp-eeg-database) ·
  [3T/7T MRI + iEEG (Nature 2026)](https://www.nature.com/articles/s41597-026-07540-5) ·
  [Epilepsy-iEEG-Multicenter (OpenNeuro)](https://openneuro.org/datasets/ds003029/versions/1.0.7) ·
  [EEG + MRI + post-op DB (PMC2974908)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2974908/) ·
  [Simultaneous EEG-fMRI (PMC10585622)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10585622/)
