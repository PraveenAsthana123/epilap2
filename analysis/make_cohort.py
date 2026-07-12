"""
make_cohort.py — Synthetic epilepsy cohort generator (primary + secondary linked)
=================================================================================

Builds ONE internally-consistent synthetic cohort of N=500 epilepsy patients that
feeds all three pipelines. The design is deliberately *causal*: a latent per-patient
`severity_level` (1..4) and `focus_side` (Left/Right) generate BOTH the primary
clinical-assessment variables (each of the 8 role domains) AND the secondary EEG
biomarkers. Because the same latent state drives both modalities, the downstream
statistics show REAL, defensible relationships (correlation, ANOVA, regression,
and genuine multimodal incremental value) rather than noise.

Two linked matrices are written to data/analysis/:
    cohort_primary.csv  — patient x clinical-assessment features (role-tagged) + target
    cohort_eeg.csv      — patient x EEG-derived biomarkers + focus label
    data_dictionary.csv — variable | role/modality | type | unit | description

Patient EP001 (row 0) is overwritten with its documented canonical values so every
worked example in the dissertation ties back to the same index case.

A small, controlled amount of missingness and a few impossible values are injected
into the NON-EP001 rows so the validation and cleaning stages have real defects to
detect and repair (production realism). EP001 itself is always clean.

Run: python analysis/make_cohort.py
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from common import rng, DATA_DIR, N_PATIENTS, SEVERITY_PREVALENCE, pid, banner, df_to_md
import os


# ---------------------------------------------------------------------------
# Helpers to draw clinically-bounded values conditioned on severity.
# ---------------------------------------------------------------------------
def _clip(x, lo, hi):
    return np.clip(x, lo, hi)


def build_primary(sev: np.ndarray, g: np.random.Generator) -> pd.DataFrame:
    """Generate the primary clinical-assessment matrix, one column group per role.

    Every feature is a function of the latent severity `sev` (1..4) plus Gaussian
    noise, using clinically sensible directions of effect (e.g. seizure frequency
    and anxiety rise with severity; MoCA and quality-of-life fall with severity).
    """
    n = len(sev)
    s = sev.astype(float)  # convenience float view of severity

    df = pd.DataFrame({"patient_id": [pid(i + 1) for i in range(n)]})

    # ---- Demographics (weakly related to severity; used later for BIAS checks) --
    df["age"] = _clip(g.normal(34 + 2 * s, 11), 18, 85).round().astype(int)
    df["sex"] = g.choice(["M", "F"], size=n, p=[0.52, 0.48])
    df["employment"] = g.choice(["Employed", "Unemployed", "Student", "Retired"],
                                size=n, p=[0.55, 0.25, 0.12, 0.08])
    df["education"] = g.choice(["Secondary", "Bachelor", "Master", "PhD"],
                               size=n, p=[0.40, 0.40, 0.15, 0.05])
    df["marital"] = g.choice(["Single", "Married", "Divorced"], size=n, p=[0.45, 0.45, 0.10])

    # ---- Neurologist domain (seizure semiology) --------------------------------
    # Noise is deliberately generous so severity classes OVERLAP (realistic; avoids
    # near-deterministic "grade" features that would leak the label and inflate AUC).
    df["neuro_seizure_freq_pm"] = _clip(g.gamma(shape=2.0, scale=(s ** 1.3)) * g.normal(1, 0.35, n), 0, 300).round(1)
    df["neuro_awareness_impaired"] = (g.random(n) < (0.20 + 0.16 * s)).astype(int)
    df["neuro_nocturnal"] = (g.random(n) < (0.12 + 0.15 * s)).astype(int)
    df["neuro_duration_sec"] = _clip(g.normal(30 + 22 * s, 45), 5, 600).round().astype(int)
    df["neuro_aura"] = (g.random(n) < (0.30 + 0.10 * s)).astype(int)
    df["neuro_postictal_min"] = _clip(g.normal(3 + 6 * s, 12), 0, 180).round().astype(int)
    df["neuro_trigger_burden"] = _clip(g.normal(s, 1.3), 0, 4).round().astype(int)

    # ---- EEG Technician domain (acquisition QC, primary side) ------------------
    df["eegtech_impedance_kohm"] = _clip(g.normal(3.0 + 0.4 * s, 1.2), 0.5, 15).round(1)
    df["eegtech_artifact_grade"] = _clip(g.normal(0.6 + 0.5 * s, 1.1), 0, 3).round().astype(int)
    df["eegtech_sleep_deprived"] = (g.random(n) < 0.7).astype(int)

    # ---- Nurse domain (observation + vitals + safety) --------------------------
    df["nurse_seizure_obs_pm"] = _clip(df["neuro_seizure_freq_pm"] * g.normal(0.85, 0.1, n), 0, 300).round(1)
    df["nurse_injury_events"] = g.poisson(_clip(0.2 * s, 0, 4)).astype(int)
    df["nurse_rescue_med"] = (g.random(n) < (0.02 + 0.10 * (s >= 3))).astype(int)
    df["nurse_sbp"] = _clip(g.normal(122 + 2 * s, 12), 90, 190).round().astype(int)
    df["nurse_hr"] = _clip(g.normal(70 + 3 * s, 10), 45, 140).round().astype(int)

    # ---- Neuropsychologist domain (cognition + mood) ---------------------------
    df["npsy_moca"] = _clip(g.normal(30 - 1.6 * s, 2.9), 5, 30).round().astype(int)
    df["npsy_verbal_mem_z"] = _clip(g.normal(0.4 - 0.55 * s, 0.9), -4, 2).round(2)
    df["npsy_naming_z"] = _clip(g.normal(0.3 - 0.42 * s, 0.9), -4, 2).round(2)
    df["npsy_gad7"] = _clip(g.normal(2 + 2.3 * s, 3.6), 0, 21).round().astype(int)
    df["npsy_nddi_e"] = _clip(g.normal(8 + 1.6 * s, 3.4), 6, 24).round().astype(int)

    # ---- Pharmacist domain (regimen, levels, adherence) ------------------------
    df["pharm_asm_count"] = _clip(g.normal(0.6 + 0.7 * s, 1.1), 0, 5).round().astype(int)
    df["pharm_cbz_level"] = _clip(g.normal(8 - 0.3 * s, 2.5), 0, 15).round(1)
    df["pharm_adherence_pct"] = _clip(g.normal(96 - 3.2 * s, 9), 40, 100).round().astype(int)
    df["pharm_interaction_flags"] = g.poisson(_clip(0.3 * s, 0, 4)).astype(int)
    df["pharm_tdm_urgency"] = _clip(g.normal(0.4 + 0.55 * s, 1.1), 0, 3).round().astype(int)

    # ---- Caregiver domain (witnessed burden) -----------------------------------
    df["care_witnessed_freq_pm"] = _clip(df["neuro_seizure_freq_pm"] * g.normal(0.8, 0.2, n), 0, 300).round(1)
    df["care_supervision"] = _clip(g.normal(0.4 + 0.6 * s, 1.1), 0, 3).round().astype(int)
    df["care_zbi_burden"] = _clip(g.normal(6 + 8 * s, 13), 0, 88).round().astype(int)

    # ---- Patient domain (self-reported outcomes) -------------------------------
    df["pt_qolie31"] = _clip(g.normal(92 - 11 * s, 13), 0, 100).round().astype(int)
    df["pt_selfreport_adherence_pct"] = _clip(df["pharm_adherence_pct"] + g.normal(0, 6, n), 40, 100).round().astype(int)
    df["pt_side_effect_burden"] = _clip(g.normal(1 + 1.6 * s, 2.4), 0, 10).round().astype(int)

    # ---- Administrator domain (encounter acuity, utilisation) ------------------
    df["admin_encounter_acuity"] = _clip(g.normal(0.3 + 0.7 * s, 1.1), 0, 3).round().astype(int)
    df["admin_prior_admissions"] = g.poisson(_clip(0.25 * s, 0, 6)).astype(int)

    return df


def build_eeg(sev: np.ndarray, focus_side: np.ndarray, g: np.random.Generator) -> pd.DataFrame:
    """Generate the secondary EEG biomarker matrix from latent severity + focus side.

    Temporal asymmetry sign encodes the lateralised focus (Left => left-temporal
    power dominates => negative asymmetry index), and spike rate / slowing scale
    with severity. This gives the secondary pipeline a genuine laterality signal
    and a real severity gradient.
    """
    n = len(sev)
    s = sev.astype(float)
    left = (focus_side == "Left").astype(float)          # 1 if left focus
    lat_sign = np.where(focus_side == "Left", -1.0, 1.0)  # asymmetry direction

    df = pd.DataFrame({"patient_id": [pid(i + 1) for i in range(n)]})

    # Relative band powers (sum ~1); slowing (delta/theta) increases with severity.
    delta = _clip(g.normal(0.18 + 0.03 * s, 0.05), 0.05, 0.6)
    theta = _clip(g.normal(0.16 + 0.03 * s, 0.05), 0.05, 0.6)
    alpha = _clip(g.normal(0.34 - 0.03 * s, 0.06), 0.05, 0.6)
    beta = _clip(g.normal(0.20 - 0.01 * s, 0.05), 0.03, 0.5)
    gamma = _clip(g.normal(0.10, 0.03), 0.02, 0.3)
    tot = delta + theta + alpha + beta + gamma
    df["eeg_delta"] = (delta / tot).round(3)
    df["eeg_theta"] = (theta / tot).round(3)
    df["eeg_alpha"] = (alpha / tot).round(3)
    df["eeg_beta"] = (beta / tot).round(3)
    df["eeg_gamma"] = (gamma / tot).round(3)

    # Temporal region powers + asymmetry index (focus side lateralises this, but
    # imperfectly — realistic overlap so localisation AUC lands ~0.9, not 1.0).
    base_l = g.normal(1.0, 0.26, n)
    base_r = g.normal(1.0, 0.26, n)
    boost = 0.30 + 0.07 * s                                   # focal boost, grows w/ severity
    df["eeg_left_temporal_pow"] = _clip(base_l + left * boost, 0.2, 3).round(3)
    df["eeg_right_temporal_pow"] = _clip(base_r + (1 - left) * boost, 0.2, 3).round(3)
    # Asymmetry index in [-1,1]: (R-L)/(R+L), plus measurement noise. Negative =>
    # left-dominant focus (clinical convention). Imperfect => realistic ~0.88 AUC.
    L, R = df["eeg_left_temporal_pow"], df["eeg_right_temporal_pow"]
    df["eeg_temporal_asym"] = _clip((R - L) / (R + L) + g.normal(0, 0.07, n), -1, 1).round(3)

    # Interictal epileptiform activity + slowing + complexity.
    df["eeg_spike_rate_pm"] = _clip(g.normal(0.5 + 1.6 * s, 1.5), 0, 60).round(2)
    df["eeg_focal_slowing"] = (g.random(n) < (0.10 + 0.18 * s)).astype(int)
    df["eeg_entropy"] = _clip(g.normal(1.6 - 0.12 * s, 0.2), 0.3, 2.5).round(3)  # sample entropy, falls w/ severity
    df["eeg_paf_hz"] = _clip(g.normal(10.2 - 0.2 * s, 0.9), 6, 13).round(2)      # peak alpha freq
    df["eeg_connectivity"] = _clip(g.normal(0.45 + 0.05 * s, 0.1), 0.1, 0.9).round(3)
    df["eeg_qc_grade"] = _clip(g.normal(0.6 + 0.4 * s, 0.7), 0, 3).round().astype(int)

    # Discrete lateralising focus channel (10-20) — used for the localisation task.
    left_ch = g.choice(["F7", "T7", "P7"], size=n, p=[0.3, 0.45, 0.25])
    right_ch = g.choice(["F8", "T8", "P8"], size=n, p=[0.3, 0.45, 0.25])
    df["eeg_focus_channel"] = np.where(focus_side == "Left", left_ch, right_ch)
    df["focus_side"] = focus_side
    return df


def inject_defects(df: pd.DataFrame, g: np.random.Generator) -> pd.DataFrame:
    """Inject a controlled amount of missingness and a few impossible values into
    NON-EP001 rows, so the validation/cleaning stages have real work to do.

    Nothing here touches row 0 (EP001), which must stay pristine.
    """
    d = df.copy()
    idx = np.arange(1, len(d))  # exclude EP001 at index 0

    # ~4% missing in a handful of realistically-incomplete fields.
    for col, frac in [("pharm_adherence_pct", 0.04), ("npsy_moca", 0.03),
                      ("care_zbi_burden", 0.05), ("pt_qolie31", 0.02),
                      ("neuro_postictal_min", 0.03)]:
        miss = g.choice(idx, size=int(frac * len(idx)), replace=False)
        d.loc[miss, col] = np.nan

    # A few impossible values (data-entry errors) for the cleaning audit trail.
    bad_age = g.choice(idx, size=3, replace=False)
    d.loc[bad_age, "age"] = [500, -5, 240][:len(bad_age)]
    bad_adh = g.choice(idx, size=2, replace=False)
    d.loc[bad_adh, "pharm_adherence_pct"] = [130, 999][:len(bad_adh)]
    return d


def set_ep001(primary: pd.DataFrame, eeg: pd.DataFrame) -> None:
    """Overwrite row 0 with EP001's documented canonical values (in place)."""
    p = {
        "age": 29, "sex": "M", "employment": "Employed", "education": "Bachelor",
        "marital": "Married",
        "neuro_seizure_freq_pm": 5.0, "neuro_awareness_impaired": 1, "neuro_nocturnal": 1,
        "neuro_duration_sec": 90, "neuro_aura": 1, "neuro_postictal_min": 15,
        "neuro_trigger_burden": 4,
        "eegtech_impedance_kohm": 3.1, "eegtech_artifact_grade": 1, "eegtech_sleep_deprived": 1,
        "nurse_seizure_obs_pm": 4.0, "nurse_injury_events": 1, "nurse_rescue_med": 0,
        "nurse_sbp": 124, "nurse_hr": 72,
        "npsy_moca": 26, "npsy_verbal_mem_z": -1.2, "npsy_naming_z": -0.8, "npsy_gad7": 9,
        "npsy_nddi_e": 13,
        "pharm_asm_count": 2, "pharm_cbz_level": 6.2, "pharm_adherence_pct": 88,
        "pharm_interaction_flags": 1, "pharm_tdm_urgency": 2,
        "care_witnessed_freq_pm": 4.0, "care_supervision": 2, "care_zbi_burden": 34,
        "pt_qolie31": 55, "pt_selfreport_adherence_pct": 88, "pt_side_effect_burden": 4,
        "admin_encounter_acuity": 2, "admin_prior_admissions": 1,
    }
    for k, v in p.items():
        primary.loc[0, k] = v

    e = {
        "eeg_delta": 0.22, "eeg_theta": 0.20, "eeg_alpha": 0.28, "eeg_beta": 0.20,
        "eeg_gamma": 0.10, "eeg_left_temporal_pow": 1.62, "eeg_right_temporal_pow": 1.10,
        "eeg_temporal_asym": round((1.62 - 1.10) / (1.62 + 1.10), 3),  # +? see note
        "eeg_spike_rate_pm": 6.0, "eeg_focal_slowing": 1, "eeg_entropy": 1.15,
        "eeg_paf_hz": 9.4, "eeg_connectivity": 0.58, "eeg_qc_grade": 1,
        "eeg_focus_channel": "T7", "focus_side": "Left",
    }
    # EP001 is a LEFT focus => left temporal power dominates => asym should be
    # negative under an (R-L) convention. We store (L-R)/(L+R); left-dominant is
    # positive here, so we flip sign to keep "negative = left" clinical reading.
    e["eeg_temporal_asym"] = -abs(e["eeg_temporal_asym"])
    for k, v in e.items():
        eeg.loc[0, k] = v


def main() -> None:
    banner("make_cohort — generating linked primary + EEG cohort (N=%d)" % N_PATIENTS)
    g = rng(0)

    # 1) Latent severity (ordinal target) and lateralised focus side.
    sev = g.choice([1, 2, 3, 4], size=N_PATIENTS, p=SEVERITY_PREVALENCE)
    focus_side = g.choice(["Left", "Right"], size=N_PATIENTS, p=[0.58, 0.42])

    # 2) Build both modalities from the shared latent state.
    primary = build_primary(sev, g)
    eeg = build_eeg(sev, focus_side, g)

    # 3) Attach the supervised targets to the PRIMARY table.
    primary["severity_level"] = sev
    primary["severity_label"] = [ {1:"Mild",2:"Moderate",3:"Severe",4:"Refractory/Status"}[x] for x in sev ]
    primary["drug_resistant"] = (sev >= 3).astype(int)   # binary convenience target

    # 4) Pin EP001, then inject realistic defects into the rest.
    set_ep001(primary, eeg)
    primary = inject_defects(primary, g)

    # 5) Persist.
    p_path = os.path.join(DATA_DIR, "cohort_primary.csv")
    e_path = os.path.join(DATA_DIR, "cohort_eeg.csv")
    primary.to_csv(p_path, index=False)
    eeg.to_csv(e_path, index=False)

    # 6) Data dictionary (role/modality tagging is used by the report + bias checks).
    dd = build_dictionary(primary, eeg)
    dd.to_csv(os.path.join(DATA_DIR, "data_dictionary.csv"), index=False)

    print(f"  wrote {p_path}  ({primary.shape[0]} x {primary.shape[1]})")
    print(f"  wrote {e_path}  ({eeg.shape[0]} x {eeg.shape[1]})")
    print(f"  severity distribution: "
          + ", ".join(f"L{k}={int((sev==k).sum())}" for k in [1, 2, 3, 4]))
    print(f"  EP001 severity={primary.loc[0,'severity_level']} "
          f"focus={eeg.loc[0,'focus_side']} channel={eeg.loc[0,'eeg_focus_channel']}")


def build_dictionary(primary: pd.DataFrame, eeg: pd.DataFrame) -> pd.DataFrame:
    """Assemble a variable dictionary that tags each feature by its owning role /
    modality — this tagging is reused by the report and the bias analysis."""
    role_of = {
        "neuro_": "Neurologist", "eegtech_": "EEG Technician", "nurse_": "Nurse",
        "npsy_": "Neuropsychologist", "pharm_": "Pharmacist", "care_": "Caregiver",
        "pt_": "Patient", "admin_": "Administrator", "eeg_": "EEG (secondary)",
    }
    rows = []
    for col in list(primary.columns) + [c for c in eeg.columns if c not in primary.columns]:
        role = "Demographics"
        for pre, name in role_of.items():
            if col.startswith(pre):
                role = name
                break
        if col in ("severity_level", "severity_label", "drug_resistant"):
            role = "Target"
        if col in ("focus_side",):
            role = "Target (secondary)"
        rows.append({"variable": col, "role_modality": role})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    main()
