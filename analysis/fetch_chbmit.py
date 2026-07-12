"""
fetch_chbmit.py — Download a REAL epilepsy EEG recording (CHB-MIT, PhysioNet)
============================================================================

Downloads CHB-MIT chb01_03.edf (~42 MB, pediatric scalp EEG with an annotated
seizure) + the summary, for analysis/chbmit_analysis.py. Open access (PhysioNet).
The .edf is gitignored (large); this script makes it reproducible.

Run: python analysis/fetch_chbmit.py
"""
from __future__ import annotations
import os, ssl, urllib.request
ssl._create_default_https_context = ssl._create_unverified_context

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "real", "chbmit")
BASE = "https://physionet.org/files/chbmit/1.0.0/chb01/"
FILES = ["chb01_03.edf", "chb01-summary.txt"]


def main():
    os.makedirs(OUT, exist_ok=True)
    for fn in FILES:
        dest = os.path.join(OUT, fn)
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            print("present:", fn); continue
        req = urllib.request.Request(BASE + fn, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=180).read()
        open(dest, "wb").write(data)
        print(f"downloaded {fn} ({len(data)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
