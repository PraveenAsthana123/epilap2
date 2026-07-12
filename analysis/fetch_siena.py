"""
fetch_siena.py — Download & batch-process real Siena Scalp EEG (PhysioNet)
=========================================================================

Fixes the "no real data" gap operationally: this downloads Siena Scalp EEG EDF
recordings from PhysioNet and runs each through the REAL DSP pipeline
(`eeg_signal_pipeline.py`), producing a real EEG biomarker table that can replace
the synthetic `cohort_eeg.csv`.

Siena Scalp EEG Database v1.0.0:  https://physionet.org/content/siena-scalp-eeg/1.0.0/
(open access; ~20 GB full, individual EDFs are large — fetch a subset).

Usage:
    python analysis/fetch_siena.py --subjects PN00 --limit 1     # download + process 1 EDF
    python analysis/fetch_siena.py --process-only data/siena-sample   # process EDFs already present

Notes:
  * EDFs are gitignored (large). This script is the reproducible fetch/process path.
  * Requires `mne` or `pyedflib` to read EDF; `requests` to download.
"""
from __future__ import annotations
import os, argparse, glob
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SIENA_BASE = "https://physionet.org/files/siena-scalp-eeg/1.0.0"
DEST = os.path.join(ROOT, "data", "siena-sample")


def download(subject: str, limit: int) -> list[str]:
    """Download up to `limit` EDF files for a subject from PhysioNet."""
    import requests
    os.makedirs(os.path.join(DEST, subject), exist_ok=True)
    # RECORDS lists the EDF paths; fetch it then pull the first `limit` EDFs.
    rec_url = f"{SIENA_BASE}/{subject}/RECORDS"
    try:
        recs = requests.get(rec_url, timeout=30).text.split()
    except Exception as e:  # pragma: no cover - network dependent
        print(f"  could not fetch RECORDS ({e}); is PhysioNet reachable?")
        return []
    got = []
    for rel in recs[:limit]:
        url = f"{SIENA_BASE}/{rel}"
        out = os.path.join(DEST, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        print(f"  downloading {rel} ...")
        with requests.get(url, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(out, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
        got.append(out)
    return got


def process(edf_dir: str) -> pd.DataFrame:
    """Run every EDF under `edf_dir` through the real DSP feature extractor."""
    import eeg_signal_pipeline as eeg
    rows = []
    for path in sorted(glob.glob(os.path.join(edf_dir, "**", "*.edf"), recursive=True)):
        try:
            sig, fs, ch = eeg.load_edf(path)
            sig = eeg.preprocess(sig, fs)
            feats, *_ = eeg.extract_features(sig, fs, ch)
            feats["source_edf"] = os.path.basename(path)
            rows.append(feats)
            print(f"  processed {os.path.basename(path)} ({len(ch)} ch @ {fs:.0f} Hz)")
        except Exception as e:
            print(f"  skipped {os.path.basename(path)}: {e}")
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subjects", nargs="*", default=["PN00"])
    ap.add_argument("--limit", type=int, default=1)
    ap.add_argument("--process-only", default=None,
                    help="skip download; process EDFs under this directory")
    args = ap.parse_args()

    if not args.process_only:
        for s in args.subjects:
            download(s, args.limit)
    edf_dir = args.process_only or DEST
    df = process(edf_dir)
    if len(df):
        out = os.path.join(ROOT, "data", "analysis", "eeg_real_features.csv")
        df.to_csv(out, index=False)
        print(f"wrote {out}  ({len(df)} recordings)")
    else:
        print("no EDFs processed — download a Siena recording first (see module docstring).")


if __name__ == "__main__":
    main()
