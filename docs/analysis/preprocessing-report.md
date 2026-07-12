# Preprocessing / Feature-Engineering / Balancing — Techniques Demonstrated

> **Why (this doc):** Runs every preprocessing technique from the checklist on the cohort and
> reports what each did — imputation (incl. KNN + model-based), outlier detection (z-score/IQR/
> IsolationForest), encoding (one-hot/ordinal/frequency/target), scaling (standard/min-max/robust),
> power/log transforms, PCA/SVD dimensionality reduction, SMOTE/ADASYN/under-sampling class
> balancing, and leakage checks. **How:** `analysis/preprocessing.py` (a reusable library + demo).

| technique | result |
|---|---|
| Imputation (KNN) | 42 nulls -> 0 |
| Imputation (iterative/model) | IterativeImputer available |
| Outliers (zscore) | 17 flagged on seizure_freq |
| Outliers (iqr) | 35 flagged on seizure_freq |
| Outliers (isoforest) | 24 flagged on seizure_freq |
| Encoding (one-hot) | employment -> 3 cols |
| Encoding (frequency) | unique freq values=4 |
| Encoding (target/mean) | range 0.25-0.42 |
| Scaling (standard) | shape (500, 5) |
| Scaling (minmax) | shape (500, 5) |
| Scaling (robust) | shape (500, 5) |
| Transform (Yeo-Johnson power) | shape (500, 5) |
| Dim-reduction (pca, k=3) | shape (500, 3) |
| Dim-reduction (svd, k=3) | shape (500, 3) |
| Balance (smote) | [308, 192] -> [308, 308] |
| Balance (adasyn) | [308, 192] -> [308, 290] |
| Balance (under) | [308, 192] -> [192, 192] |
| Leakage: target-corr>0.98 | [] |
| Leakage: dup entities across splits | 0 |

**Leakage prevention:** no feature exceeds 0.98 target correlation; the subject-level split has
**0 duplicate entities across train/test** (0 = no patient-level leakage).
