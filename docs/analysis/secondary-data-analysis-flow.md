# Secondary (EEG) Data Analysis — Flow

*Caption — the secondary pipeline (real CHB-MIT scalp EEG → seizure detection) as sequential steps, bullets, and diagrams. Real result: cross-validated ROC-AUC ≈ 0.92; external validation ≈ 0.979.*

## Sequential steps (input → process → output)

| # | Stage | Input | Process | Output | Tool |
|---|---|---|---|---|---|
| 1 | Load | CHB-MIT `chb01_03.edf` | read EDF (real EEG) | 8 ch @ 256 Hz | `MNE` |
| 2 | Preprocess | raw µV | band-pass 0.5–45 Hz + 50 Hz notch + re-reference | clean signal | `scipy.signal` |
| 3 | Epoch | clean signal | 4 s windows, **subject-level split** | labelled epochs | `numpy` |
| 4 | Time-frequency | epoch | STFT spectrogram + CWT scalogram | TF maps | `scipy` |
| 5 | 1D→2D images | TF maps | spectrogram / scalogram / connectivity / power-band heatmap | images | `matplotlib` |
| 6 | Features | epoch | band power, Hjorth, Higuchi FD, entropy, PLV, line-length | 12 features | custom |
| 7 | Normalise | features | z-score standardisation | scaled features | `scikit-learn` |
| 8 | Select | scaled features | mutual information + leave-one-band-out ablation | ranked features | `scikit-learn` |
| 9 | Balance | training fold | SMOTE (in-fold) | balanced train | `imbalanced-learn` |
| 10 | Train / HPO | balanced train | RandomForest + MLP, GridSearchCV | tuned models | `scikit-learn` |
| 11 | Evaluate | holdout | accuracy matrix (AUC/AP/log-loss) | metrics (**AUC ≈ 0.92**) | `scikit-learn` |
| 12 | Explain | best model | permutation + SHAP | top: line-length / gamma / PLV | `shap` |
| 13 | RAG report | prediction + KG | retrieve evidence + generate | clinician report | `vector_db_pipeline.py` |

## Key methods (bullets)

- **Data:** real pediatric scalp EEG (PhysioNet CHB-MIT); external validation on EEG-Eye-State.
- **Preprocess:** Butterworth band-pass + IIR notch + common-average reference.
- **Leakage control:** subject-level splits (no epoch from a subject in both train and test).
- **Time-frequency:** STFT (Fourier) + CWT (ricker/Mexican-hat wavelet).
- **1D→2D:** spectrogram, scalogram, channel-connectivity matrix, power-band heatmap.
- **Features:** spectral band power (δ/θ/α/β/γ), Hjorth (activity/mobility/complexity), Higuchi fractal dimension, spectral entropy, phase-locking value, line-length.
- **Significance:** Mann-Whitney U + rank-biserial effect (line-length, power, max-amplitude p < 0.001).
- **Imbalance:** SMOTE in-fold only.
- **Models:** RandomForest + MLP (lightweight stand-in for EEGNet/CNN), GridSearchCV-tuned.
- **Explainability:** permutation importance + SHAP → line-length, gamma power, PLV.

## Flowchart
```mermaid
flowchart TD
  A[1 Load EDF: CHB-MIT real EEG] --> B[2 Preprocess: bandpass+notch+re-ref]
  B --> C[3 Epoch 4s: subject-level split]
  C --> D[4 Time-frequency: STFT + CWT]
  D --> E[5 1D->2D images: spectrogram/scalogram/connectivity]
  C --> F[6 Features: band power/Hjorth/FD/entropy/PLV/line-length]
  F --> G[7 Normalise z-score]
  G --> H[8 Select: MI + band ablation]
  H --> I[9 Balance: SMOTE in-fold]
  I --> J[10 Train/HPO: RF + MLP]
  J --> K[11 Evaluate: accuracy matrix AUC~0.92]
  K --> L[12 Explain: permutation + SHAP]
  L --> M[13 RAG report: retrieve + generate]
```

## Sequence diagram
```mermaid
sequenceDiagram
  participant EEG as CHB-MIT EEG
  participant DSP as Preprocess + TF
  participant FE as Feature extraction
  participant Model
  participant RAG
  participant Neuro as Neurologist
  EEG->>DSP: raw 8ch @256Hz
  DSP->>DSP: bandpass + notch + STFT/CWT
  DSP->>FE: epochs (subject-level)
  FE->>Model: 12 features (SMOTE in-fold)
  Model-->>RAG: seizure risk + top biomarkers
  RAG->>RAG: retrieve guideline evidence + explain
  RAG->>Neuro: grounded report (AUC ~0.92)
  Neuro-->>RAG: confirm / override (logged)
```

## Network flow
```mermaid
graph LR
  EDF[CHB-MIT EDF] --> PRE[Preprocess]
  PRE --> EP[Epoch subject-level]
  EP --> TF[STFT / CWT]
  TF --> IMG[2D images]
  EP --> FEAT[12 features]
  FEAT --> SEL[Select MI + ablation]
  SEL --> BAL[SMOTE in-fold]
  BAL --> TRN[RF + MLP + HPO]
  TRN --> EVAL[Accuracy matrix]
  TRN --> XAI[Permutation + SHAP]
  EVAL & XAI --> RAG[RAG report + KG]
  RAG --> N[Neurologist]
```
