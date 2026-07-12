# Visualization & Diagram Catalogue

> **Why (this doc):** Confirms the mandated visual types (flowchart, sequence, network, journey, C4) and computed charts are present across the documentation. **How:** auto-counted across all `docs/**/*.md` by `analysis/build_catalogues.py`.

**Markdown files scanned:** 233 · **Total Mermaid diagrams:** 1164.

| Visualization type | Occurrences |
|---|---|
| flowchart TD/TB (flowchart) | 551 |
| sequenceDiagram | 201 |
| graph LR (network) | 208 |
| journey map | 195 |
| C4 / container (flowchart TB subgraph) | 47 |
| PNG figures (matplotlib) | 5 |

**Diagram standard (per GLOBAL-POLICY rule 5 & 21):** every substantive doc carries a flowchart, a sequence diagram, a network (graph LR) diagram, and a journey map; architecture docs add a C4 model. Analytics reports add computed PNG charts (correlation heatmap, severity boxplot, SHAP importance, EEG asymmetry).
