"""
fetch_real_eeg.py — Download a REAL public EEG dataset (EEG-Eye-State, OpenML)
=============================================================================

Fetches genuine EEG data (not synthetic) for real-data validation:
  EEG-Eye-State — 14,980 one-second samples, 14 real electrode channels, binary
  eye open/closed target (Roesler 2013). ~1.5 MB. Saved to data/real/.

For the epilepsy-specific real corpora use analysis/fetch_siena.py (PhysioNet).

Run: python analysis/fetch_real_eeg.py
"""
from __future__ import annotations
import os, ssl
ssl._create_default_https_context = ssl._create_unverified_context

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "real")
os.makedirs(OUT, exist_ok=True)


def main():
    from sklearn.datasets import fetch_openml
    path = os.path.join(OUT, "EEG-Eye-State.csv")
    if os.path.exists(path):
        print("already present:", path); return
    d = fetch_openml(name="EEG-Eye-State", version=1, as_frame=True, parser="auto")
    d.frame.to_csv(path, index=False)
    print(f"saved real EEG dataset: {path}  {d.frame.shape}")


if __name__ == "__main__":
    main()
