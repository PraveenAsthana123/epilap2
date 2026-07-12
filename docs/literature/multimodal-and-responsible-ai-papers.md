# Literature — Multimodal (Primary + Secondary) & Responsible / Explainable / Governance AI

> **Why (this doc):** Real papers for (a) **multimodal** analysis fusing primary clinical data with
> secondary EEG/imaging, and (b) **Responsible / Explainable / Governance AI** in clinical decision
> support — the two pillars of this project. Retrieved via web search (July 2026); verify full text
> before citing.

## Multimodal — primary (clinical) + secondary (EEG/imaging) fusion

| # | Study | Modalities fused | Link |
|---|---|---|---|
| 1 | Predicting **antiseizure-medication outcomes** in early-diagnosed epilepsy — multimodal framework | **EEG + MRI + clinical** | [medRxiv 2025](https://www.medrxiv.org/content/10.1101/2025.03.12.25323644.full.pdf) |
| 2 | ML model for **post-stroke epilepsy risk** integrating multimodal signals (365 patients) | **EEG-fMRI + clinical biomarkers** | [Frontiers Neurology 2026](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2026.1722475/abstract) |
| 3 | **MultiEpilepsyNet** — hybrid deep-learning multimodal seizure detection | **EEG + MRI** | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0361923025004575) |
| 4 | Advanced **Multimodal Learning** for seizure detection & prediction (review) | EEG + multimodal | [arXiv 2601.05095](https://arxiv.org/html/2601.05095v1) |
| 5 | Patient-specific **data fusion + adversarial training** for seizure prediction | multimodal EEG | [PMC10192566](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10192566/) |
| 6 | Interpretable ML for drug-resistant epilepsy in TSC | **clinical + EEG + MRI + genetic** | [Frontiers 2025](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2025.1623212/full) |

→ Maps to this repo's `analysis/fusion_analysis.py` + `decision_support.py` (primary + EEG fusion).

## Explainable AI (XAI) in clinical decision support

| # | Study | Link |
|---|---|---|
| 7 | Survey of **explainable AI in healthcare** — concepts, applications, challenges | [ScienceDirect 2024](https://www.sciencedirect.com/science/article/pii/S2352914824001448) |
| 8 | **XAI in CDSS — meta-analysis** of 62 studies (2018–2025) | [MDPI Healthcare](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12427955/) |
| 9 | **XAI applications in healthcare — systematic review** (76 studies) | [MDPI Algorithms](https://doi.org/10.3390/a19060488) |
| 10 | **To explain or not to explain?** — AI explainability in CDSS | [PMC9931364](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9931364/) |
| 11 | Communication gap between AI models & clinicians (explainability, trust) | [PMC7618637](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7618637/) |

→ Maps to `analysis/responsible_ai_runtime.py` (SHAP + LIME) + `docs/responsible-ai/05-explainable-ai.md`.

## Responsible AI & Governance in clinical AI

| # | Study | Link |
|---|---|---|
| 12 | Reinforcing CDSS through **multi-agent systems + ethical AI governance** | [arXiv 2504.03699](https://arxiv.org/html/2504.03699v1) |
| 13 | AI-driven CDSS — governance & implementation | [arXiv 2501.09628](https://arxiv.org/pdf/2501.09628) |

### Foundational (canonical, widely cited)
- Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions (**SHAP**). *NeurIPS*.
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?" (**LIME**). *KDD*.
- Rudin, C. (2019). Stop explaining black-box models for high-stakes decisions. *Nature Machine Intelligence, 1*, 206–215.
- Ghassemi, M., Oakden-Rayner, L., & Beam, A. L. (2021). The false hope of current approaches to explainable AI in health care. *Lancet Digital Health, 3*(11), e745–e750.
- Amann, J., et al. (2020). Explainability for AI in medicine. *BMC Medical Informatics and Decision Making, 20*, 310.
- Mitchell, M., et al. (2019). **Model cards** for model reporting. *FAT\**.
- Barocas, S., Hardt, M., & Narayanan, A. (2019). *Fairness and machine learning*. fairmlbook.org.
- NIST. (2023). *AI Risk Management Framework (AI RMF 1.0)*.
- European Union. (2024). *EU Artificial Intelligence Act*.

→ Maps to the 16-pillar [Responsible AI framework](../responsible-ai/index.md) + governance runtime (`mlops/`).

## Sources
- [Multimodal ASM outcomes (medRxiv)](https://www.medrxiv.org/content/10.1101/2025.03.12.25323644.full.pdf) ·
  [Post-stroke epilepsy multimodal (Frontiers)](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2026.1722475/abstract) ·
  [MultiEpilepsyNet (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S0361923025004575) ·
  [Multimodal review (arXiv)](https://arxiv.org/html/2601.05095v1) ·
  [Data-fusion seizure prediction (PMC10192566)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10192566/) ·
  [XAI healthcare survey (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S2352914824001448) ·
  [XAI CDSS meta-analysis (PMC12427955)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12427955/) ·
  [XAI healthcare review (MDPI)](https://doi.org/10.3390/a19060488) ·
  [To explain or not (PMC9931364)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9931364/) ·
  [Ethical AI governance CDSS (arXiv)](https://arxiv.org/html/2504.03699v1)
