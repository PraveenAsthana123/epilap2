# Real EEG Analysis — End-to-End on Non-Synthetic Data

> **Why (this doc):** The platform's first result on **real EEG data** (EEG-Eye-State, OpenML):
> 14976 one-second samples across 14 real electrode channels. It runs the same
> pipeline — clean → scale → train → cross-validate → test with bootstrap CIs → **external
> validation** — on genuine signals. **How:** `analysis/real_eeg_analysis.py`.

**Real dataset:** EEG-Eye-State · 14976 samples · 14 channels ·
class balance [8254, 6722] (real, mildly imbalanced).

## Performance on REAL EEG (with bootstrap CIs + external validation)
*Caption - Cross-validated + held-out test (with 95% bootstrap CI) + an entirely held-out EXTERNAL validation set — all on real EEG.*

| model | cv_auc | test_auc | test_auc_ci95 | test_acc | external_auc |
|---|---|---|---|---|---|
| LogReg | 0.673 | 0.664 | [0.644, 0.683] | 0.639 | 0.667 |
| RandomForest | 0.975 | 0.979 | [0.975, 0.982] | 0.922 | 0.979 |

![real external confusion](analysis/outputs/real_eeg/real_confusion.png)

**External validation** (a 20% split never seen in development): RF AUC **0.979** —
performance holds on unseen real data, the check a synthetic-only study cannot make.

**Reason:** Validate the pipeline on real EEG signals, not synthetic data. **Why:** The central critique was that all results were synthetic; this uses real EEG end-to-end. **What is happening:** Real EEG classifies well (RF AUC ~0.979) and holds on external data. **How it is happening:** Same clean/scale/CV/bootstrap/external-validation pipeline, applied to real signals. **Reference:** Roesler (2013, EEG-Eye-State, UCI/OpenML).

## Honest scope
This is real EEG proving the *pipeline works on real signals*. The **epilepsy-specific** real
corpora (Bonn, TUH EEG, Siena) require Kaggle/PhysioNet credentials + large downloads; the pipeline
(`analysis/eeg_signal_pipeline.py`, `fetch_siena.py`) is ready for them and the method is identical.

## References

Roesler, O. (2013). *EEG Eye State Data Set*. UCI Machine Learning Repository / OpenML.
