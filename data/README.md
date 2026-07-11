# Data Directory

> **Why:** Explain what data is committed to git vs fetched locally, and how to get the large
> EEG files without bloating the repo.

## What IS in git (small, safe)

*Caption — everything here is tiny and GitHub-friendly.*

| Path | Size | Contents |
|---|---|---|
| `synthetic/` | ~61 KB | Synthetic sample CSVs for all 8 dossier schemas (100 patients, EP001 canonical). **Not real patients.** |
| `siena-sample/subject_info.csv` | ~0.5 KB | Real Siena cohort metadata |
| `siena-sample/RECORDS` | ~0.6 KB | List of Siena EDF files |
| `siena-sample/PN00/Seizures-list-PN00.txt` | ~1.5 KB | Real seizure annotations (channels, timing) |

## What is NOT in git (fetch locally)

*Caption — large binary EEG; excluded via .gitignore, downloaded on demand.*

| File | Size | Why excluded |
|---|---|---|
| `siena-sample/PN00/*.edf` | 71–89 MB each | Binary EEG; GitHub warns >50 MB, hard limit 100 MB/file |

## GitHub size rules (why we split this way)

*Caption — the limits that drive the committed-vs-ignored decision.*

| Limit | Value |
|---|---|
| Hard per-file limit | 100 MB (push rejected above this) |
| Warning per-file | 50 MB |
| Recommended repo size | < 1 GB |
| Large binaries | Use Git LFS or keep out of git (we keep out) |

## Fetch a real EEG sample locally

```bash
# One Siena record (~71 MB) — runs outside git, ignored by .gitignore
curl -o data/siena-sample/PN00/PN00-4.edf \
  https://physionet.org/files/siena-scalp-eeg/1.0.0/PN00/PN00-4.edf
```

Full Siena dataset (~20 GB) and the access-controlled sets (TUH, EPILEPSIAE, UK Biobank) are
described in [../docs/dataset-scorecard.md](../docs/dataset-scorecard.md) and
[../docs/dataset-dossier.md](../docs/dataset-dossier.md).

## Regenerate synthetic data

```bash
python data/generate_synthetic.py
```
