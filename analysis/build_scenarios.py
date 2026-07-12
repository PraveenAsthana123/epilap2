"""
build_scenarios.py — Seizure / epilepsy scenario database + weightage & scoring
===============================================================================

Builds a structured database of seizure and epilepsy scenarios (ILAE 2017 seizure
types, epilepsy syndromes, and clinical scenarios), each mapped to the platform's
4-level severity ladder and a clinical weight. Also emits the domain WEIGHTAGE
table used to turn a filled questionnaire into a weighted patient severity SCORE.

Outputs:
  data/analysis/epilepsy_scenarios.csv     — one row per scenario
  data/analysis/domain_weightage.csv       — role/domain weights for scoring
  docs/scenarios/index.md                   — human-readable scenario catalogue
  docs/scenarios/scoring-weightage.md       — weightage + scoring model

Run: python analysis/build_scenarios.py
"""
from __future__ import annotations
import os, csv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "analysis")
DOCS = os.path.join(ROOT, "docs", "scenarios")
os.makedirs(DATA, exist_ok=True); os.makedirs(DOCS, exist_ok=True)

# (id, category, scenario, onset, awareness, ILAE class, severity(1-4), weight, key features)
SCENARIOS = [
    # ---- ILAE 2017 seizure types: focal onset ----
    ("SZ-F01","Seizure Type","Focal aware seizure","Focal","Aware","Focal aware (simple partial)",2,0.6,"Preserved awareness; motor/sensory/autonomic aura"),
    ("SZ-F02","Seizure Type","Focal impaired awareness seizure","Focal","Impaired","Focal impaired awareness (complex partial)",3,1.0,"Behavioural arrest, automatisms, amnesia — EP001 type"),
    ("SZ-F03","Seizure Type","Focal motor — automatisms","Focal","Variable","Focal motor onset",2,0.7,"Lip-smacking, fumbling"),
    ("SZ-F04","Seizure Type","Focal motor — clonic","Focal","Variable","Focal motor onset",2,0.7,"Rhythmic jerking of one limb"),
    ("SZ-F05","Seizure Type","Focal motor — tonic","Focal","Variable","Focal motor onset",2,0.7,"Sustained stiffening"),
    ("SZ-F06","Seizure Type","Focal motor — hyperkinetic","Focal","Variable","Focal motor onset",3,0.8,"Vigorous limb/trunk movements (frontal)"),
    ("SZ-F07","Seizure Type","Focal motor — epileptic spasms","Focal","Variable","Focal motor onset",3,0.9,"Brief axial flexion/extension"),
    ("SZ-F08","Seizure Type","Focal non-motor — autonomic","Focal","Variable","Focal non-motor onset",2,0.7,"Epigastric rising, pallor, flushing"),
    ("SZ-F09","Seizure Type","Focal non-motor — behaviour arrest","Focal","Variable","Focal non-motor onset",2,0.6,"Sudden cessation of activity"),
    ("SZ-F10","Seizure Type","Focal non-motor — cognitive","Focal","Variable","Focal non-motor onset",2,0.7,"Deja vu, dysphasia, forced thinking"),
    ("SZ-F11","Seizure Type","Focal non-motor — emotional","Focal","Variable","Focal non-motor onset",2,0.7,"Fear, anxiety, ictal laughter"),
    ("SZ-F12","Seizure Type","Focal non-motor — sensory","Focal","Variable","Focal non-motor onset",2,0.7,"Somatosensory, visual, auditory, olfactory"),
    ("SZ-F13","Seizure Type","Focal to bilateral tonic-clonic","Focal","Lost","Focal to bilateral tonic-clonic",4,1.2,"Secondary generalisation; injury/SUDEP risk"),
    # ---- generalized onset ----
    ("SZ-G01","Seizure Type","Generalized tonic-clonic","Generalized","Lost","Generalized motor",4,1.2,"Bilateral stiffening then jerking; tongue-bite, incontinence"),
    ("SZ-G02","Seizure Type","Generalized clonic","Generalized","Lost","Generalized motor",3,0.9,"Rhythmic bilateral jerking"),
    ("SZ-G03","Seizure Type","Generalized tonic","Generalized","Lost","Generalized motor",3,0.9,"Bilateral stiffening"),
    ("SZ-G04","Seizure Type","Generalized myoclonic","Generalized","Aware","Generalized motor",2,0.7,"Brief shock-like jerks"),
    ("SZ-G05","Seizure Type","Myoclonic-tonic-clonic","Generalized","Lost","Generalized motor",3,0.9,"Jerks preceding GTC (JME)"),
    ("SZ-G06","Seizure Type","Myoclonic-atonic","Generalized","Lost","Generalized motor",3,0.9,"Jerk then drop (Doose)"),
    ("SZ-G07","Seizure Type","Atonic (drop attack)","Generalized","Lost","Generalized motor",3,1.0,"Sudden loss of tone; fall/injury"),
    ("SZ-G08","Seizure Type","Epileptic spasms","Generalized","Variable","Generalized motor",4,1.0,"Clusters of axial spasms (West)"),
    ("SZ-G09","Seizure Type","Typical absence","Generalized","Impaired","Generalized non-motor (absence)",2,0.6,"Brief blank stare, 3 Hz spike-wave"),
    ("SZ-G10","Seizure Type","Atypical absence","Generalized","Impaired","Generalized non-motor (absence)",3,0.8,"Slower onset/offset, tone change (LGS)"),
    ("SZ-G11","Seizure Type","Myoclonic absence","Generalized","Impaired","Generalized non-motor (absence)",3,0.8,"Absence with rhythmic myoclonia"),
    ("SZ-G12","Seizure Type","Eyelid myoclonia","Generalized","Variable","Generalized non-motor (absence)",2,0.7,"Eyelid jerks + upward eye deviation"),
    # ---- unknown onset ----
    ("SZ-U01","Seizure Type","Unknown-onset tonic-clonic","Unknown","Lost","Unknown motor",4,1.1,"GTC, onset unwitnessed"),
    ("SZ-U02","Seizure Type","Unknown-onset behaviour arrest","Unknown","Variable","Unknown non-motor",2,0.6,"Arrest, onset unclear"),
    ("SZ-U03","Seizure Type","Unclassified seizure","Unknown","Variable","Unclassified",2,0.6,"Insufficient information"),
    # ---- epilepsy syndromes / etiologies ----
    ("EP-S01","Epilepsy Syndrome","Mesial temporal lobe epilepsy (MTS)","Focal","Impaired","Focal, structural",3,1.0,"Hippocampal sclerosis; drug-resistant tendency — EP001"),
    ("EP-S02","Epilepsy Syndrome","Frontal lobe epilepsy","Focal","Variable","Focal, structural/unknown",3,0.9,"Nocturnal, hyperkinetic, brief"),
    ("EP-S03","Epilepsy Syndrome","Juvenile myoclonic epilepsy","Generalized","Aware","Idiopathic generalized",2,0.7,"Morning myoclonus, photosensitive"),
    ("EP-S04","Epilepsy Syndrome","Childhood absence epilepsy","Generalized","Impaired","Idiopathic generalized",2,0.6,"Frequent absences, 3 Hz"),
    ("EP-S05","Epilepsy Syndrome","Lennox-Gastaut syndrome","Generalized","Variable","Developmental/epileptic encephalopathy",4,1.3,"Multiple seizure types, cognitive impairment"),
    ("EP-S06","Epilepsy Syndrome","Dravet syndrome","Generalized","Variable","Developmental/epileptic encephalopathy",4,1.3,"SCN1A, febrile-triggered, refractory"),
    ("EP-S07","Epilepsy Syndrome","West syndrome (infantile spasms)","Generalized","Variable","Developmental/epileptic encephalopathy",4,1.2,"Spasms, hypsarrhythmia, regression"),
    ("EP-S08","Epilepsy Syndrome","Self-limited epilepsy w/ centrotemporal spikes","Focal","Aware","Self-limited focal",1,0.4,"Benign rolandic; nocturnal, remits"),
    ("EP-S09","Epilepsy Syndrome","Post-traumatic epilepsy","Focal","Variable","Focal, structural",3,0.9,"After TBI; latency months-years"),
    ("EP-S10","Epilepsy Syndrome","Post-stroke epilepsy","Focal","Variable","Focal, structural",3,0.9,"Cortical infarct; older patients"),
    # ---- clinical scenarios ----
    ("CL-01","Clinical Scenario","First unprovoked seizure","Any","Variable","Any",2,0.6,"Single event; recurrence-risk stratification"),
    ("CL-02","Clinical Scenario","Breakthrough seizure despite adherence","Focal","Impaired","Focal",3,1.0,"Recurrence on adequate ASM — EP001"),
    ("CL-03","Clinical Scenario","Drug-resistant (refractory) epilepsy","Any","Variable","Any",4,1.3,"Failed >=2 appropriate ASMs; surgery work-up"),
    ("CL-04","Clinical Scenario","Seizure cluster (acute repetitive)","Any","Variable","Any",4,1.1,"Multiple seizures/day; rescue meds"),
    ("CL-05","Clinical Scenario","Convulsive status epilepticus","Generalized","Lost","Generalized motor",4,1.5,"Seizure >5 min / recurring ~every 5 min — emergency"),
    ("CL-06","Clinical Scenario","Non-convulsive status epilepticus","Any","Impaired","Any",4,1.4,"Altered awareness, EEG-confirmed; ICU cEEG"),
    ("CL-07","Clinical Scenario","Nocturnal seizures","Focal","Variable","Focal",3,0.9,"Sleep-related; SUDEP relevance — EP001 has these"),
    ("CL-08","Clinical Scenario","Catamenial epilepsy","Focal","Variable","Any",3,0.8,"Perimenstrual exacerbation"),
    ("CL-09","Clinical Scenario","Febrile seizure","Generalized","Lost","Provoked",1,0.4,"Child + fever; usually benign"),
    ("CL-10","Clinical Scenario","Acute symptomatic / provoked seizure","Any","Variable","Provoked",2,0.6,"Metabolic, alcohol withdrawal, toxic"),
    ("CL-11","Clinical Scenario","SUDEP risk scenario","Any","Variable","Any",4,1.2,"GTC + nocturnal + poor control; counselling"),
    ("CL-12","Clinical Scenario","Psychogenic non-epileptic seizure (differential)","N/A","Variable","Non-epileptic (differential)",2,0.5,"vEEG normal; not epilepsy — rule out"),
    ("CL-13","Clinical Scenario","Epilepsy in pregnancy","Any","Variable","Any",3,0.9,"ASM teratogenicity, level changes, folate"),
    ("CL-14","Clinical Scenario","Epilepsy surgery candidate","Focal","Impaired","Focal, structural",3,1.0,"Drug-resistant focal + concordant work-up"),
    ("CL-15","Clinical Scenario","Well-controlled epilepsy (seizure-free)","Any","Variable","Any",1,0.3,"Seizure-free >=1 yr on ASM; driving eligible"),
    # ---- platform severity ladder ----
    ("SEV-1","Severity Level","Mild (well-controlled)","-","-","-",1,0.3,"Rare/absent seizures, monotherapy, no restriction"),
    ("SEV-2","Severity Level","Moderate (intermediate)","-","-","-",2,0.6,"~Monthly seizures, minor impact, mild QoL reduction"),
    ("SEV-3","Severity Level","Severe (poorly controlled)","-","-","-",3,1.0,"Several/month, breakthrough, restrictions — EP001"),
    ("SEV-4","Severity Level","Refractory / Status (operational emergency)","-","-","-",4,1.5,"Seizures ~every 5 min / drug-resistant; emergency"),
]

# Domain (role) weightage for the composite weighted severity score.
DOMAIN_WEIGHTS = [
    ("Neurologist", 0.22, "Seizure classification, burden, diagnosis — primary driver"),
    ("EEG Technician", 0.10, "Objective electrophysiology / focus evidence"),
    ("Neuropsychologist", 0.12, "Cognitive & mood comorbidity load"),
    ("Pharmacist", 0.12, "Regimen complexity, drug resistance, levels"),
    ("Nurse", 0.10, "Observed events, vitals, acute safety"),
    ("Caregiver", 0.10, "Witnessed burden, home management"),
    ("Patient", 0.12, "Patient-reported outcomes, QoL, adherence"),
    ("Occupational Therapist", 0.08, "Functional independence, participation, safety"),
    ("Administrator", 0.04, "Encounter acuity / utilisation signal"),
]


def main() -> None:
    # CSV: scenarios
    sp = os.path.join(DATA, "epilepsy_scenarios.csv")
    with open(sp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id","category","scenario","onset","awareness","ilae_class",
                    "severity_level","clinical_weight","key_features"])
        w.writerows(SCENARIOS)

    # CSV: domain weightage
    wp = os.path.join(DATA, "domain_weightage.csv")
    with open(wp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["domain","weight","rationale"]); w.writerows(DOMAIN_WEIGHTS)

    # Doc: scenario catalogue grouped by category
    cats = ["Seizure Type","Epilepsy Syndrome","Clinical Scenario","Severity Level"]
    out = ["# Epilepsy & Seizure Scenario Database\n",
           "> **Why (this doc):** A single controlled catalogue of every seizure type (ILAE 2017), "
           "epilepsy syndrome, and clinical scenario the platform reasons about, each mapped to the "
           "4-level severity ladder and a clinical weight for scoring. **How:** generated from "
           "`analysis/build_scenarios.py`; source of truth is `data/analysis/epilepsy_scenarios.csv`.\n",
           f"**Total scenarios:** {len(SCENARIOS)} · **Categories:** {len(cats)} · "
           "Severity 1=Mild 2=Moderate 3=Severe 4=Refractory/Status. EP001 = Severe focal "
           "impaired-awareness, left temporal.\n"]
    for cat in cats:
        rows = [s for s in SCENARIOS if s[1] == cat]
        out.append(f"\n## {cat} ({len(rows)})\n")
        out.append("| ID | Scenario | Onset | Awareness | ILAE Class | Severity | Weight | Key features |")
        out.append("|---|---|---|---|---|---|---|---|")
        for s in rows:
            out.append(f"| {s[0]} | {s[2]} | {s[3]} | {s[4]} | {s[5]} | {s[6]} | {s[7]} | {s[8]} |")
    out.append("\nSee [scoring-weightage.md](scoring-weightage.md) for how scenarios/weights drive the patient score.")
    open(os.path.join(DOCS, "index.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")

    # Doc: weightage + scoring model
    sc = ["# Questionnaire Weightage & Scoring Model\n",
          "> **Why (this doc):** Turns a filled role questionnaire into a weighted patient "
          "severity score, so the form is not just data capture but a graded assessment. "
          "**How:** each item maps to a severity level (1-4) via the section's Severity Scenario "
          "Model; items are weighted, averaged per role, then combined across roles by domain weight.\n",
          "## Item-level scoring\n",
          "*Caption - Each questionnaire item scores 1-4 by the answer's severity level; item weight scales its contribution.*\n",
          "| Step | Rule |","|---|---|",
          "| 1 | Map each answered item to its severity level L (1=Mild … 4=Refractory/Status) |",
          "| 2 | Item weight w = clinical_weight of the matching scenario (default 1.0) |",
          "| 3 | Section score = Σ(L·w) / Σ(w) over answered items |",
          "| 4 | Role score = mean of that role's section scores |",
          "| 5 | Patient composite = Σ(role_score · domain_weight) |",
          "| 6 | Band: <1.75 Mild · <2.5 Moderate · <3.25 Severe · else Refractory/Status |\n",
          "## Domain weightage\n",
          "*Caption - Relative weight of each role in the composite patient severity score (sums to 1.0).*\n",
          "| Domain | Weight | Rationale |","|---|---|---|"]
    for d,wt,r in DOMAIN_WEIGHTS:
        sc.append(f"| {d} | {wt} | {r} |")
    sc.append(f"\n**Total:** {sum(x[1] for x in DOMAIN_WEIGHTS):.2f}. EP001 → domain scores skew to "
              "Severe (Level 3), composite ≈ Severe. Source CSVs: `data/analysis/domain_weightage.csv`, "
              "`data/analysis/epilepsy_scenarios.csv`.")
    open(os.path.join(DOCS, "scoring-weightage.md"), "w", encoding="utf-8").write("\n".join(sc) + "\n")

    print(f"scenarios={len(SCENARIOS)} -> {sp}")
    for cat in cats:
        print(f"  {cat}: {sum(1 for s in SCENARIOS if s[1]==cat)}")
    print(f"domain_weights sum={sum(x[1] for x in DOMAIN_WEIGHTS):.2f}")


if __name__ == "__main__":
    main()
