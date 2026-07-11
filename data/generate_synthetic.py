"""Generate synthetic epilepsy sample datasets matching the dossier schemas.
Deterministic (seeded). EP001 = the canonical patient profile. Data is SYNTHETIC.
"""
import csv, os, random

random.seed(42)
ROOT = os.path.join(os.path.dirname(__file__), "synthetic")
N = 100  # patients EP001..EP100

def pid(i): return f"EP{i:03d}"

def w(rel, header, rows):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)

SEIZURE_TYPES = ["Focal Impaired Awareness", "Focal Aware", "Generalized Tonic-Clonic",
                 "Absence", "Myoclonic"]
EPILEPSY_CLASS = ["Focal", "Generalized", "Combined", "Unknown"]
ASMS = ["Levetiracetam", "Carbamazepine", "Valproate", "Lamotrigine", "Lacosamide"]
REGIONS = ["Left Temporal", "Right Temporal", "Left Frontal", "Right Frontal",
           "Parietal", "Occipital", "Generalized"]

def maybe(p): return random.random() < p

# ---------- Dataset 25: Population registry core files ----------
def demographics():
    rows = []
    for i in range(1, N+1):
        if i == 1:
            rows.append([pid(i), 29, "Male", "Software Engineer", "Urban", "Insured", "Ontario"])
        else:
            rows.append([pid(i), random.randint(6, 78),
                         random.choice(["Male", "Female"]),
                         random.choice(["Student", "Teacher", "Retired", "Engineer", "Unemployed"]),
                         random.choice(["Urban", "Rural"]),
                         random.choice(["Insured", "Uninsured"]),
                         random.choice(["Ontario", "Quebec", "BC", "Alberta"])])
    return w("dataset-25-population/demographics.csv",
             ["Patient_ID", "Age", "Gender", "Occupation", "Urban_Rural", "Insurance", "Province"], rows)

def epidemiology():
    rows = []
    for i in range(1, N+1):
        age = 29 if i == 1 else random.randint(6, 78)
        rows.append([pid(i), random.choice(EPILEPSY_CLASS),
                     age, "Childhood" if age < 18 else ("Elderly" if age > 65 else "Adult"),
                     "Yes" if (i == 1 or maybe(0.3)) else "No",  # drug resistant
                     "Alive" if maybe(0.97) else "Deceased"])
    return w("dataset-25-population/epidemiology.csv",
             ["Patient_ID", "Epilepsy_Class", "Age_at_Diagnosis", "Age_Group",
              "Drug_Resistant", "Status"], rows)

def seizure_registry():
    rows = []
    for i in range(1, N+1):
        freq = 5 if i == 1 else random.randint(0, 18)
        rows.append([pid(i), random.choice(SEIZURE_TYPES), freq,
                     freq*4, random.randint(0, 5), random.randint(0, 3)])
    return w("dataset-25-population/seizure_registry.csv",
             ["Patient_ID", "Seizure_Type", "Monthly_Frequency", "Weekly_Frequency_x4",
              "Emergency_Visits", "Hospitalizations"], rows)

def medication_registry():
    rows = []
    for i in range(1, N+1):
        if i == 1:
            rows.append([pid(i), "Levetiracetam", "First Line", "No", "Yes", 88])
        else:
            rows.append([pid(i), random.choice(ASMS),
                         random.choice(["First Line", "Second Line"]),
                         "Yes" if maybe(0.3) else "No",
                         "Yes" if maybe(0.3) else "No",
                         random.randint(50, 100)])
    return w("dataset-25-population/medication_registry.csv",
             ["Patient_ID", "ASM_Name", "Line", "Polytherapy", "Drug_Resistant", "Adherence_Pct"], rows)

# ---------- Dataset 18: Remote monitoring ----------
def remote_monitoring():
    rows = []
    for i in range(1, N+1):
        risk = random.randint(30, 95)
        rows.append([pid(i), f"DEV{i:03d}", random.randint(20, 120),
                     random.randint(0, 12), f"{random.randint(85, 99)}%",
                     random.choice(REGIONS), risk,
                     "High" if risk > 75 else ("Moderate" if risk > 50 else "Low")])
    return w("dataset-18-remote-monitoring/remote_monitoring.csv",
             ["Patient_ID", "Device_ID", "Monitoring_Days", "Seizures_Detected",
              "Signal_Quality", "Localization", "Risk_Score", "Risk_Level"], rows)

# ---------- Dataset 19: Wearable digital biomarker ----------
def wearable():
    rows = []
    for i in range(1, N+1):
        rows.append([pid(i), random.randint(55, 100), random.randint(20, 80),
                     random.randint(90, 99), 8 if i == 1 else random.randint(3, 9),
                     random.randint(40, 95), random.randint(30, 95)])
    return w("dataset-19-wearable/digital_biomarkers.csv",
             ["Patient_ID", "Heart_Rate", "HRV_ms", "SpO2_Pct", "Sleep_Hours",
              "Sleep_Score", "Overall_Risk"], rows)

# ---------- Dataset 20: Neuroimaging ----------
def neuroimaging():
    rows = []
    for i in range(1, N+1):
        les = "Yes" if (i == 1 or maybe(0.4)) else "No"
        rows.append([pid(i), random.choice(["1.5T", "3T"]), les,
                     random.choice(["Cortical Dysplasia", "Hippocampal Sclerosis", "None", "Cavernoma"]),
                     round(random.uniform(2.5, 3.5), 2),
                     "Left Temporal" if i == 1 else random.choice(REGIONS),
                     92 if i == 1 else random.randint(10, 90)])
    return w("dataset-20-neuroimaging/mri_findings.csv",
             ["Patient_ID", "Field_Strength", "Lesion_Present", "Lesion_Type",
              "Hippocampal_Vol_cm3", "Localization", "AI_Localization_Pct"], rows)

# ---------- Dataset 21: Neuropsychology ----------
def neuropsych():
    rows = []
    for i in range(1, N+1):
        rows.append([pid(i), random.randint(70, 120), random.randint(60, 130),
                     random.randint(0, 27), random.randint(0, 21),
                     56 if i == 1 else random.randint(30, 90)])
    return w("dataset-21-neuropsychology/cognition_scores.csv",
             ["Patient_ID", "Full_Scale_IQ", "Memory_Index", "PHQ9", "GAD7", "QOLIE31"], rows)

# ---------- Dataset 22: Genomics ----------
def genomics():
    genes = ["SCN1A", "SCN2A", "KCNQ2", "DEPDC5", "STXBP1", "CDKL5", "None"]
    acmg = ["Pathogenic", "Likely Pathogenic", "VUS", "Benign"]
    rows = []
    for i in range(1, N+1):
        g = random.choice(genes)
        rows.append([pid(i), g, "N/A" if g == "None" else random.choice(acmg),
                     random.choice(["HLA-B*15:02", "CYP2C9*3", "POLG", "None"]),
                     random.choice(["Sensitive", "Resistant", "Partial"])])
    return w("dataset-22-genomics/gene_panel.csv",
             ["Patient_ID", "Gene", "ACMG_Class", "Pharmacogenomic_Variant", "Drug_Response"], rows)

# ---------- Dataset 23: Surgery ----------
def surgery():
    procs = ["Temporal Lobectomy", "Lesionectomy", "LITT", "VNS", "RNS", "None"]
    engel = ["I", "II", "III", "IV"]
    rows = []
    for i in range(1, N+1):
        if maybe(0.25):
            rows.append([pid(i), "Yes", random.choice(procs[:-1]),
                         random.choice(engel), random.randint(50, 100)])
        else:
            rows.append([pid(i), "No", "None", "N/A", 0])
    return w("dataset-23-surgery/surgical_outcomes.csv",
             ["Patient_ID", "Surgical_Candidate", "Procedure", "Engel_Class", "Seizure_Reduction_Pct"], rows)

# ---------- Dataset 24: ICU ----------
def icu():
    rows = []
    for i in range(1, N+1):
        if maybe(0.15):
            rows.append([pid(i), random.randint(8, 30), random.randint(3, 15),
                         random.choice(["Convulsive", "Non-convulsive", "Refractory", "None"]),
                         random.randint(0, 100),
                         random.choice(["Survived", "Deceased"])])
    return w("dataset-24-icu/icu_monitoring.csv",
             ["Patient_ID", "APACHE_II", "GCS", "Status_Epilepticus_Type",
              "Seizure_Burden_Pct", "ICU_Outcome"], rows)

if __name__ == "__main__":
    results = {
        "demographics.csv": demographics(),
        "epidemiology.csv": epidemiology(),
        "seizure_registry.csv": seizure_registry(),
        "medication_registry.csv": medication_registry(),
        "remote_monitoring.csv": remote_monitoring(),
        "digital_biomarkers.csv": wearable(),
        "mri_findings.csv": neuroimaging(),
        "cognition_scores.csv": neuropsych(),
        "gene_panel.csv": genomics(),
        "surgical_outcomes.csv": surgery(),
        "icu_monitoring.csv": icu(),
    }
    print("Generated synthetic CSVs (SYNTHETIC DATA — not real patients):")
    for k, v in results.items():
        print(f"  {k}: {v} rows")
    print(f"Output dir: {ROOT}")
