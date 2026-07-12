# Checklist Coverage — Data Engineering, Preprocessing, MLOps & LLM-Ops

> **Why (this doc):** Maps every capability in the extended checklist to its status
> (✅ built · ➕ added this round · 📄 documented/planned) and where it lives. **How:** grouped by
> category with the implementing file. (Checklist referenced schizophrenia/PANSS; translated to
> epilepsy per policy.)

## Data-quality metadata (per column/dataset)
✅➕ `mlops/data_quality.py` → `data/analysis/data_quality_report.csv` + [report](analysis/data-quality-report.md)

feature_type · null_pct · missing_count · unique_count · **uniqueness_score** · **consistency_score** ·
mean/std/min/max · **skew/distribution** · **outlier_pct (IQR)** · **drift_threshold** · **anomaly_indicator** ·
record_count · **schema_version** · **feature_version** · **sensitive_classification** · **encryption_status** ·
**retention_policy** · **compliance_tag** · refresh_frequency · freshness · **duplicate_flag** ·
**referential_integrity** · date/region_partition · schema_changes — all emitted per column.

## Preprocessing
➕ `analysis/preprocessing.py` (+ existing `primary_analysis.py`)

| Item | Status |
|---|---|
| Imputation: mean/median | ✅ primary_analysis |
| Imputation: **KNN + model-based (iterative)** | ➕ preprocessing |
| Outliers: **z-score / IQR / IsolationForest** | ➕ preprocessing |
| Duplicates / invalid records / harmonisation | ✅ primary_analysis.clean + data_quality |
| Encoding: label / one-hot / ordinal | ✅ |
| Encoding: **frequency / target(mean)** | ➕ preprocessing |
| Scaling: standard / min-max / robust | ✅ + ➕ |
| Transforms: **power (Yeo-Johnson) / log** | ➕ preprocessing |
| Feature engineering: derived / aggregation / interaction / domain | ✅ + ➕ |

## Feature selection & dimensionality
| Item | Status |
|---|---|
| Correlation / LASSO / tree importance / RFE / MI / SelectKBest / SHAP-ranking | ✅ primary_analysis + RAI runtime |
| **PCA / TruncatedSVD** (UMAP optional) | ➕ preprocessing |
| Elastic Net / Boruta | 📄 (LASSO+RFE cover the need; can add) |

## Class imbalance & leakage
| Item | Status |
|---|---|
| **SMOTE / ADASYN / over / under / class-weight** | ➕ preprocessing (was: random oversample) |
| Leakage: target-corr check · **duplicate entities across splits** · subject-level split | ➕ preprocessing + all pipelines |

## MLOps / data engineering
| Item | Status |
|---|---|
| **Data contract** | ➕ `mlops/data_contract.py` |
| **Feature store + metadata** | ➕ `mlops/feature_store.py` |
| **Experiment tracking** | ➕ `mlops/experiment_tracker.py` |
| **Model registry + rollback** | ➕ `mlops/model_registry.py` |
| ETL / data mesh / fabric / partition / retention / lineage | ➕📄 [data-engineering-mlops](data-engineering-mlops.md) |
| Model / data **drift** | ✅ governance (confidence) + data_quality drift_threshold; 📄 scheduled drift job |

## LLM / Agent-Ops ("missing model" list)
➕ `mlops/llm_ops.py` + design in [responsible-ai/implementation](responsible-ai/implementation/index.md)

| Item | Status |
|---|---|
| **Prompt registry** (versioned) | ➕ |
| **Semantic caching** | ➕ (normalised key; embeddings in prod) |
| **Model routing** (by complexity/cost) | ➕ |
| **Response evaluation** (hallucination/grounding/PII) | ➕ |
| **Token / cost optimization** | ➕ CostTracker |
| Conversation memory · tool selection · agent planning · multi-agent orchestration | 📄 (Agent tool used in build; documented) |
| A/B testing · batch vs real-time inference · baseline selection | 📄 (experiment_tracker + model_registry provide the hooks) |
| Model-specific metrics (accuracy/precision/recall/AUC/PR-AUC/calibration/Brier/DCA) | ✅ primary/fusion/governance |

## Statistical / time-series (from the 23-step flow)
✅ descriptives, normality, correlation, chi-square, ANOVA, ordinal/logistic/Cox regression,
effect sizes, CIs, **survival analysis** (recurrence). 📄 MANOVA/ANCOVA/mixed-effects and deep
time-series (LSTM/Transformer/TFT) are documented as next-stage (need longitudinal real data).

## How to run everything added
```bash
python mlops/data_quality.py       # metadata catalogue
python analysis/preprocessing.py   # all preprocessing techniques
python mlops/llm_ops.py            # LLM/agent-ops demo
python mlops/run_mlops_demo.py     # contract->store->track->registry->rollback
# tests: analysis 25 · mlops 7 · API 8 · Vitest 19
```

**Legend:** ✅ already built · ➕ added this round · 📄 documented / planned (needs real longitudinal
data or a production tool swap: Feast / MLflow / Great Expectations / dbt / DataHub).
