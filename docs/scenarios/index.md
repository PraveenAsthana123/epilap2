# Epilepsy & Seizure Scenario Database

> **Why (this doc):** A single controlled catalogue of every seizure type (ILAE 2017), epilepsy syndrome, and clinical scenario the platform reasons about, each mapped to the 4-level severity ladder and a clinical weight for scoring. **How:** generated from `analysis/build_scenarios.py`; source of truth is `data/analysis/epilepsy_scenarios.csv`.

**Total scenarios:** 57 · **Categories:** 4 · Severity 1=Mild 2=Moderate 3=Severe 4=Refractory/Status. EP001 = Severe focal impaired-awareness, left temporal.


## Seizure Type (28)

| ID | Scenario | Onset | Awareness | ILAE Class | Severity | Weight | Key features |
|---|---|---|---|---|---|---|---|
| SZ-F01 | Focal aware seizure | Focal | Aware | Focal aware (simple partial) | 2 | 0.6 | Preserved awareness; motor/sensory/autonomic aura |
| SZ-F02 | Focal impaired awareness seizure | Focal | Impaired | Focal impaired awareness (complex partial) | 3 | 1.0 | Behavioural arrest, automatisms, amnesia — EP001 type |
| SZ-F03 | Focal motor — automatisms | Focal | Variable | Focal motor onset | 2 | 0.7 | Lip-smacking, fumbling |
| SZ-F04 | Focal motor — clonic | Focal | Variable | Focal motor onset | 2 | 0.7 | Rhythmic jerking of one limb |
| SZ-F05 | Focal motor — tonic | Focal | Variable | Focal motor onset | 2 | 0.7 | Sustained stiffening |
| SZ-F06 | Focal motor — hyperkinetic | Focal | Variable | Focal motor onset | 3 | 0.8 | Vigorous limb/trunk movements (frontal) |
| SZ-F07 | Focal motor — epileptic spasms | Focal | Variable | Focal motor onset | 3 | 0.9 | Brief axial flexion/extension |
| SZ-F08 | Focal non-motor — autonomic | Focal | Variable | Focal non-motor onset | 2 | 0.7 | Epigastric rising, pallor, flushing |
| SZ-F09 | Focal non-motor — behaviour arrest | Focal | Variable | Focal non-motor onset | 2 | 0.6 | Sudden cessation of activity |
| SZ-F10 | Focal non-motor — cognitive | Focal | Variable | Focal non-motor onset | 2 | 0.7 | Deja vu, dysphasia, forced thinking |
| SZ-F11 | Focal non-motor — emotional | Focal | Variable | Focal non-motor onset | 2 | 0.7 | Fear, anxiety, ictal laughter |
| SZ-F12 | Focal non-motor — sensory | Focal | Variable | Focal non-motor onset | 2 | 0.7 | Somatosensory, visual, auditory, olfactory |
| SZ-F13 | Focal to bilateral tonic-clonic | Focal | Lost | Focal to bilateral tonic-clonic | 4 | 1.2 | Secondary generalisation; injury/SUDEP risk |
| SZ-G01 | Generalized tonic-clonic | Generalized | Lost | Generalized motor | 4 | 1.2 | Bilateral stiffening then jerking; tongue-bite, incontinence |
| SZ-G02 | Generalized clonic | Generalized | Lost | Generalized motor | 3 | 0.9 | Rhythmic bilateral jerking |
| SZ-G03 | Generalized tonic | Generalized | Lost | Generalized motor | 3 | 0.9 | Bilateral stiffening |
| SZ-G04 | Generalized myoclonic | Generalized | Aware | Generalized motor | 2 | 0.7 | Brief shock-like jerks |
| SZ-G05 | Myoclonic-tonic-clonic | Generalized | Lost | Generalized motor | 3 | 0.9 | Jerks preceding GTC (JME) |
| SZ-G06 | Myoclonic-atonic | Generalized | Lost | Generalized motor | 3 | 0.9 | Jerk then drop (Doose) |
| SZ-G07 | Atonic (drop attack) | Generalized | Lost | Generalized motor | 3 | 1.0 | Sudden loss of tone; fall/injury |
| SZ-G08 | Epileptic spasms | Generalized | Variable | Generalized motor | 4 | 1.0 | Clusters of axial spasms (West) |
| SZ-G09 | Typical absence | Generalized | Impaired | Generalized non-motor (absence) | 2 | 0.6 | Brief blank stare, 3 Hz spike-wave |
| SZ-G10 | Atypical absence | Generalized | Impaired | Generalized non-motor (absence) | 3 | 0.8 | Slower onset/offset, tone change (LGS) |
| SZ-G11 | Myoclonic absence | Generalized | Impaired | Generalized non-motor (absence) | 3 | 0.8 | Absence with rhythmic myoclonia |
| SZ-G12 | Eyelid myoclonia | Generalized | Variable | Generalized non-motor (absence) | 2 | 0.7 | Eyelid jerks + upward eye deviation |
| SZ-U01 | Unknown-onset tonic-clonic | Unknown | Lost | Unknown motor | 4 | 1.1 | GTC, onset unwitnessed |
| SZ-U02 | Unknown-onset behaviour arrest | Unknown | Variable | Unknown non-motor | 2 | 0.6 | Arrest, onset unclear |
| SZ-U03 | Unclassified seizure | Unknown | Variable | Unclassified | 2 | 0.6 | Insufficient information |

## Epilepsy Syndrome (10)

| ID | Scenario | Onset | Awareness | ILAE Class | Severity | Weight | Key features |
|---|---|---|---|---|---|---|---|
| EP-S01 | Mesial temporal lobe epilepsy (MTS) | Focal | Impaired | Focal, structural | 3 | 1.0 | Hippocampal sclerosis; drug-resistant tendency — EP001 |
| EP-S02 | Frontal lobe epilepsy | Focal | Variable | Focal, structural/unknown | 3 | 0.9 | Nocturnal, hyperkinetic, brief |
| EP-S03 | Juvenile myoclonic epilepsy | Generalized | Aware | Idiopathic generalized | 2 | 0.7 | Morning myoclonus, photosensitive |
| EP-S04 | Childhood absence epilepsy | Generalized | Impaired | Idiopathic generalized | 2 | 0.6 | Frequent absences, 3 Hz |
| EP-S05 | Lennox-Gastaut syndrome | Generalized | Variable | Developmental/epileptic encephalopathy | 4 | 1.3 | Multiple seizure types, cognitive impairment |
| EP-S06 | Dravet syndrome | Generalized | Variable | Developmental/epileptic encephalopathy | 4 | 1.3 | SCN1A, febrile-triggered, refractory |
| EP-S07 | West syndrome (infantile spasms) | Generalized | Variable | Developmental/epileptic encephalopathy | 4 | 1.2 | Spasms, hypsarrhythmia, regression |
| EP-S08 | Self-limited epilepsy w/ centrotemporal spikes | Focal | Aware | Self-limited focal | 1 | 0.4 | Benign rolandic; nocturnal, remits |
| EP-S09 | Post-traumatic epilepsy | Focal | Variable | Focal, structural | 3 | 0.9 | After TBI; latency months-years |
| EP-S10 | Post-stroke epilepsy | Focal | Variable | Focal, structural | 3 | 0.9 | Cortical infarct; older patients |

## Clinical Scenario (15)

| ID | Scenario | Onset | Awareness | ILAE Class | Severity | Weight | Key features |
|---|---|---|---|---|---|---|---|
| CL-01 | First unprovoked seizure | Any | Variable | Any | 2 | 0.6 | Single event; recurrence-risk stratification |
| CL-02 | Breakthrough seizure despite adherence | Focal | Impaired | Focal | 3 | 1.0 | Recurrence on adequate ASM — EP001 |
| CL-03 | Drug-resistant (refractory) epilepsy | Any | Variable | Any | 4 | 1.3 | Failed >=2 appropriate ASMs; surgery work-up |
| CL-04 | Seizure cluster (acute repetitive) | Any | Variable | Any | 4 | 1.1 | Multiple seizures/day; rescue meds |
| CL-05 | Convulsive status epilepticus | Generalized | Lost | Generalized motor | 4 | 1.5 | Seizure >5 min / recurring ~every 5 min — emergency |
| CL-06 | Non-convulsive status epilepticus | Any | Impaired | Any | 4 | 1.4 | Altered awareness, EEG-confirmed; ICU cEEG |
| CL-07 | Nocturnal seizures | Focal | Variable | Focal | 3 | 0.9 | Sleep-related; SUDEP relevance — EP001 has these |
| CL-08 | Catamenial epilepsy | Focal | Variable | Any | 3 | 0.8 | Perimenstrual exacerbation |
| CL-09 | Febrile seizure | Generalized | Lost | Provoked | 1 | 0.4 | Child + fever; usually benign |
| CL-10 | Acute symptomatic / provoked seizure | Any | Variable | Provoked | 2 | 0.6 | Metabolic, alcohol withdrawal, toxic |
| CL-11 | SUDEP risk scenario | Any | Variable | Any | 4 | 1.2 | GTC + nocturnal + poor control; counselling |
| CL-12 | Psychogenic non-epileptic seizure (differential) | N/A | Variable | Non-epileptic (differential) | 2 | 0.5 | vEEG normal; not epilepsy — rule out |
| CL-13 | Epilepsy in pregnancy | Any | Variable | Any | 3 | 0.9 | ASM teratogenicity, level changes, folate |
| CL-14 | Epilepsy surgery candidate | Focal | Impaired | Focal, structural | 3 | 1.0 | Drug-resistant focal + concordant work-up |
| CL-15 | Well-controlled epilepsy (seizure-free) | Any | Variable | Any | 1 | 0.3 | Seizure-free >=1 yr on ASM; driving eligible |

## Severity Level (4)

| ID | Scenario | Onset | Awareness | ILAE Class | Severity | Weight | Key features |
|---|---|---|---|---|---|---|---|
| SEV-1 | Mild (well-controlled) | - | - | - | 1 | 0.3 | Rare/absent seizures, monotherapy, no restriction |
| SEV-2 | Moderate (intermediate) | - | - | - | 2 | 0.6 | ~Monthly seizures, minor impact, mild QoL reduction |
| SEV-3 | Severe (poorly controlled) | - | - | - | 3 | 1.0 | Several/month, breakthrough, restrictions — EP001 |
| SEV-4 | Refractory / Status (operational emergency) | - | - | - | 4 | 1.5 | Seizures ~every 5 min / drug-resistant; emergency |

See [scoring-weightage.md](scoring-weightage.md) for how scenarios/weights drive the patient score.
