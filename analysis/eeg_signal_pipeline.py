"""
eeg_signal_pipeline.py — REAL EEG signal processing (not synthetic feature vectors)
===================================================================================

Addresses the "EEG is fake" gap: this computes EEG biomarkers from actual multi-channel
WAVEFORMS using real DSP (scipy) — band-pass + notch filtering, Welch power spectral
density, band powers, temporal asymmetry, peak alpha frequency, spectral-entropy
complexity, spike detection, and coherence connectivity.

It accepts a real EDF (Siena Scalp EEG / TUH EEG Corpus) via `load_edf()` when MNE or
pyedflib is installed; when no EDF is present it synthesises a physiologically-structured
multi-channel signal (pink noise + posterior alpha + focal temporal theta + interictal
spikes) so the pipeline is demonstrable end-to-end. Either way, the features come from
signal, not hand-assigned numbers.

To use real data:
    1. Download Siena Scalp EEG (PhysioNet) into data/siena-sample/  (EDFs are gitignored)
    2. python analysis/eeg_signal_pipeline.py --edf data/siena-sample/PN00/PN00-1.edf

Run (demo): python analysis/eeg_signal_pipeline.py
"""
from __future__ import annotations
import os, sys, argparse
import numpy as np
from scipy import signal as sps
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import rng, save_fig, df_to_md, explain, caption, write_report, banner, SEED
import pandas as pd

STAGE = "eeg"
CHANNELS = ["F7", "T7", "P7", "F3", "C3", "P3", "Fz", "Cz", "Pz",
            "F4", "C4", "P4", "F8", "T8", "P8"]
LEFT_TEMPORAL = ["F7", "T7", "P7"]
RIGHT_TEMPORAL = ["F8", "T8", "P8"]
BANDS = {"delta": (0.5, 4), "theta": (4, 8), "alpha": (8, 13), "beta": (13, 30), "gamma": (30, 45)}


# ---------------------------------------------------------------------------
# Signal source — real EDF loader (optional deps) or physiological synthesis
# ---------------------------------------------------------------------------
def load_edf(path: str):
    """Load a real EDF into (signals[n_ch,n], fs, ch_names). Uses MNE or pyedflib
    if available. Raises a clear error if neither is installed."""
    try:
        import mne
        raw = mne.io.read_raw_edf(path, preload=True, verbose="ERROR")
        return raw.get_data(), float(raw.info["sfreq"]), list(raw.ch_names)
    except ImportError:
        pass
    try:
        import pyedflib
        f = pyedflib.EdfReader(path)
        n = f.signals_in_file
        sig = np.vstack([f.readSignal(i) for i in range(n)])
        fs = float(f.getSampleFrequency(0))
        ch = f.getSignalLabels()
        f._close()
        return sig, fs, ch
    except ImportError:
        raise ImportError("Install `mne` or `pyedflib` to read real EDF files.")


def synth_eeg(fs=256, seconds=60, focus_side="Left"):
    """Synthesise a physiologically-structured multi-channel EEG (REAL time series that
    the DSP then analyses). Pink-noise background + posterior alpha + focal temporal
    theta slowing + interictal spikes lateralised to the focus side."""
    g = rng(7)
    n = int(fs * seconds)
    t = np.arange(n) / fs
    focal = LEFT_TEMPORAL if focus_side == "Left" else RIGHT_TEMPORAL
    sig = np.zeros((len(CHANNELS), n))
    for i, ch in enumerate(CHANNELS):
        # 1/f pink-ish background via filtered white noise.
        white = g.standard_normal(n)
        b, a = sps.butter(1, 40 / (fs / 2), btype="low")
        bg = sps.lfilter(b, a, white)
        x = bg
        # Posterior alpha (stronger at P/O).
        if ch.startswith(("P", "O")):
            x = x + 0.8 * np.sin(2 * np.pi * 10 * t)
        # Focal temporal theta slowing + interictal spikes on the focus side.
        if ch in focal:
            x = x + 0.6 * np.sin(2 * np.pi * 5.5 * t)          # theta slowing
            spikes = (g.random(n) < 1.2 / fs).astype(float)     # ~1.2 spikes/s
            spike_wave = sps.lfilter(*sps.butter(2, [10 / (fs / 2), 40 / (fs / 2)], btype="band"),
                                     spikes * g.uniform(10, 18, n))
            x = x + spike_wave
        sig[i] = x * 20e-6 + 10e-6 * g.standard_normal(n)       # scale to ~µV
    return sig, fs, list(CHANNELS)


# ---------------------------------------------------------------------------
# Preprocessing — real filters
# ---------------------------------------------------------------------------
def preprocess(sig, fs, notch=50.0):
    """Band-pass 0.5–45 Hz + notch + common-average reference (real DSP)."""
    b, a = sps.butter(4, [0.5 / (fs / 2), 45 / (fs / 2)], btype="band")
    x = sps.filtfilt(b, a, sig, axis=1)
    bn, an = sps.iirnotch(notch / (fs / 2), Q=30)
    x = sps.filtfilt(bn, an, x, axis=1)
    x = x - x.mean(axis=0, keepdims=True)                        # common-average reference
    return x


# ---------------------------------------------------------------------------
# Feature extraction — from the actual spectra
# ---------------------------------------------------------------------------
def _bandpower(psd, freqs, lo, hi):
    m = (freqs >= lo) & (freqs < hi)
    trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))  # numpy>=2 renamed trapz
    return trapz(psd[..., m], freqs[m], axis=-1)


def extract_features(sig, fs, ch_names):
    freqs, psd = sps.welch(sig, fs=fs, nperseg=int(fs * 2), axis=1)  # per-channel PSD
    total = _bandpower(psd, freqs, 0.5, 45) + 1e-20
    feats = {}
    for name, (lo, hi) in BANDS.items():
        feats[f"eeg_{name}"] = float((_bandpower(psd, freqs, lo, hi) / total).mean())

    def temporal_power(chs):
        idx = [ch_names.index(c) for c in chs if c in ch_names]
        return float(_bandpower(psd[idx], freqs, 0.5, 45).mean()) if idx else np.nan

    L = temporal_power(LEFT_TEMPORAL)
    R = temporal_power(RIGHT_TEMPORAL)
    feats["eeg_left_temporal_pow"] = round(L / (L + R), 3)
    feats["eeg_right_temporal_pow"] = round(R / (L + R), 3)
    feats["eeg_temporal_asym"] = round((R - L) / (R + L), 3)     # neg => left-dominant

    # Peak alpha frequency (dominant freq in 8–13 Hz, posterior mean).
    amask = (freqs >= 8) & (freqs <= 13)
    feats["eeg_paf_hz"] = round(float(freqs[amask][np.argmax(psd[:, amask].mean(0))]), 2)

    # Spectral entropy (complexity; falls with pathological slowing).
    p = psd.mean(0); p = p / p.sum()
    feats["eeg_entropy"] = round(float(-(p * np.log(p + 1e-20)).sum() / np.log(len(p))), 3)

    # Spike rate: threshold crossings on the temporal channels (per minute).
    tidx = [ch_names.index(c) for c in LEFT_TEMPORAL + RIGHT_TEMPORAL if c in ch_names]
    tsig = sig[tidx]
    thr = 4 * np.median(np.abs(tsig), axis=1, keepdims=True) / 0.6745  # robust sigma (Quiroga)
    spikes = (np.abs(tsig) > thr).sum(axis=1)
    minutes = sig.shape[1] / fs / 60
    feats["eeg_spike_rate_pm"] = round(float(spikes.mean() / minutes), 2)

    # Connectivity: mean magnitude-squared coherence across channel pairs (alpha band).
    coh = []
    for i in range(len(ch_names)):
        for j in range(i + 1, len(ch_names)):
            f, c = sps.coherence(sig[i], sig[j], fs=fs, nperseg=int(fs * 2))
            coh.append(c[(f >= 8) & (f <= 13)].mean())
    feats["eeg_connectivity"] = round(float(np.mean(coh)), 3)
    return feats, freqs, psd


def build_report(v):
    S = [f"""# Real EEG Signal Pipeline (DSP-based biomarkers)

> **Why (this doc):** The secondary-data critique was that EEG features were hand-assigned. This
> pipeline computes them from **actual multi-channel waveforms** using real DSP — filtering, Welch
> PSD, band powers, asymmetry, peak alpha frequency, spectral entropy, spike detection, and
> coherence connectivity. It accepts real **Siena/TUH EDF**; the demo runs on a physiologically
> synthesised signal. **How:** `analysis/eeg_signal_pipeline.py` (scipy).

**Source:** {v['source']} · channels {v['nch']} · fs {v['fs']} Hz · {v['secs']} s.

## Extracted biomarkers (computed from the spectra)

{caption("Biomarker features derived from the real PSD/coherence of the waveforms — Left vs Right focus demos show the asymmetry index flips sign, as expected.")}

{df_to_md(v['table'])}

![PSD]({v['psd_png']})

{explain("Compute EEG biomarkers from signal, not by assignment.",
         "Explainable EEG (flagship 2) requires features grounded in real spectra.",
         "Left-focus vs right-focus signals produce opposite-sign temporal asymmetry.",
         "Welch PSD band powers + coherence + robust spike detection on filtered waveforms.",
         "Nunez & Srinivasan (2006).")}

## Using real Siena/TUH data

```mermaid
flowchart LR
    EDF[Siena/TUH EDF] --> LD[load_edf via MNE/pyedflib]
    LD --> PP[Band-pass + notch + CAR]
    PP --> FE[Welch PSD -> band powers, asymmetry, PAF, entropy, spikes, coherence]
    FE --> VEC[Biomarker vector -> secondary pipeline]
```

**Reason:** Show the real-data path. **Why:** The pipeline must ingest genuine EDF for defensible results. **What is happening:** EDF → filters → spectral features → the secondary/fusion analytics. **How it is happening:** `load_edf()` reads EDF; the same `extract_features()` runs. **Reference:** Nunez & Srinivasan (2006).

## References

Nunez, P. L., & Srinivasan, R. (2006). *Electric fields of the brain* (2nd ed.). Oxford University Press.
"""]
    return write_report("eeg-signal-pipeline.md", S)


def run_one(edf, focus):
    if edf:
        sig, fs, ch = load_edf(edf); src = f"EDF {os.path.basename(edf)}"
    else:
        sig, fs, ch = synth_eeg(focus_side=focus); src = f"synthesised ({focus} focus)"
    sig = preprocess(sig, fs)
    feats, freqs, psd = extract_features(sig, fs, ch)
    return feats, freqs, psd, fs, ch, src


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edf", default=None)
    args = ap.parse_args()
    banner("eeg_signal_pipeline — real DSP EEG biomarkers")

    if args.edf:
        feats, freqs, psd, fs, ch, src = run_one(args.edf, "Left")
        rows = [{"biomarker": k, "value": v} for k, v in feats.items()]
        table = pd.DataFrame(rows)
        nch, secs = len(ch), "n/a"
    else:
        # Demo both focus sides to show the asymmetry index flips sign.
        fL, freqs, psdL, fs, ch, _ = run_one(None, "Left")
        fR, _, _, _, _, _ = run_one(None, "Right")
        table = pd.DataFrame({"biomarker": list(fL), "Left_focus": list(fL.values()),
                              "Right_focus": [fR[k] for k in fL]})
        psd = psdL; nch, secs, src = len(ch), 60, "synthesised (Left & Right focus)"

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(freqs, psd.mean(0), color="#4f46e5")
    ax.set_xlim(0, 45); ax.set_xlabel("Hz"); ax.set_ylabel("PSD"); ax.set_title("Mean power spectral density")
    psd_png = save_fig(fig, STAGE, "psd.png")

    path = build_report(dict(source=src, nch=nch, fs=fs, secs=secs, table=table, psd_png=psd_png))
    print(table.to_string(index=False))
    print(f"  report -> {path}")


if __name__ == "__main__":
    main()
