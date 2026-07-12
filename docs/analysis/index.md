# Analytics — End-to-End Primary · Secondary · Fusion

> **Why (this section):** These are the executable, reproducible analyses that turn the
> project's clinical assessment data (primary) and EEG biomarkers (secondary) into an
> explainable, human-supervised, patient-level decision (fusion) for patient EP001.
> Every table and figure is computed by the code in [`analysis/`](../../analysis/README.md)
> and regenerated with `python analysis/run_all.py`. **How:** deterministic synthetic
> data, one commented function per pipeline stage, and self-writing reports.

## Reports

| Report | Scope | Headline result |
|---|---|---|
| [Primary Data Analysis](primary-analysis.md) | 8-role assessment matrix → validate, clean, feature-engineer, encode/scale, EDA, statistics, feature-select, balance, bias, model | Quality 0.998 · drug-resistance AUC 0.969 |
| [Secondary (EEG) Analysis](secondary-analysis.md) | EEG biomarkers → QC, preprocess, region-map, statistics, focus localisation | Focus-lateralisation AUC 0.93 |
| [Fusion & EP001 Case](fusion-analysis.md) | Merge modalities → incremental value → EP001 end-to-end decision | Fusion AUC 0.976 · EP001 Severe, Left-Temporal focus |

## How to reproduce

```bash
cd analysis && pip install -r requirements.txt && python run_all.py
```

## Method map

- Primary pipeline realises the phased methodology in [pipeline-a](../pipeline-a/index.md).
- Secondary pipeline realises [pipeline-b](../pipeline-b/index.md).
- Fusion realises [pipeline-c-multimodal](../pipeline-c-multimodal.md) and feeds
  [clinical decision support](../pipeline-a/phase-13-clinical-decision-support.md).
- The whole deliverable serves the platform vision in [research-vision](../research-vision.md).

See the code and full methodology in [`analysis/README.md`](../../analysis/README.md).
