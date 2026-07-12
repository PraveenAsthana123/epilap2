"""
knowledge_graph_export.py — Epilepsy knowledge graph (RDF/Turtle) + graph DB export
====================================================================================

Builds a small, real **knowledge graph** for the epilepsy platform and exports it three ways:

  data/analysis/kg_nodes.csv   (id, label, type)          -> viewer graph
  data/analysis/kg_edges.csv   (source, relation, target) -> viewer graph
  docs/enterprise-flow/epilepsy-kg.ttl  (RDF Turtle)       -> load into a triple store / graph DB

The graph links patients, seizure types, EEG features/biomarkers, anti-seizure medications (ASM),
assessments/roles, outcomes, and guidelines — the semantic backbone a RAG/agent layer reasons over
(Model Context Protocol tools can query it; see docs/enterprise-flow/mcp-multiagent-knowledge-graph.md).

Run: python analysis/knowledge_graph_export.py
Scope: epilepsy.
"""
from __future__ import annotations
import os
import pandas as pd
from common import DATA_DIR, ROOT, banner

NS = "http://epilepsy.ai/kg#"

# Nodes: (id, label, type)
NODES = [
    ("EP001", "Patient EP001", "Patient"),
    ("focal", "Focal seizure", "SeizureType"),
    ("generalized", "Generalized seizure", "SeizureType"),
    ("absence", "Absence seizure", "SeizureType"),
    ("ftbtc", "Focal to bilateral tonic-clonic", "SeizureType"),
    ("line_length", "Line-length", "EEGFeature"),
    ("band_gamma", "Gamma band power", "EEGFeature"),
    ("plv", "Phase-locking value", "EEGFeature"),
    ("spike_rate", "Interictal spike rate", "EEGFeature"),
    ("levetiracetam", "Levetiracetam", "ASM"),
    ("lamotrigine", "Lamotrigine", "ASM"),
    ("valproate", "Valproate", "ASM"),
    ("neurologist", "Neurologist assessment", "Assessment"),
    ("eeg_tech", "EEG technician assessment", "Assessment"),
    ("breakthrough", "Breakthrough seizure (90d)", "Outcome"),
    ("status_epilepticus", "Status epilepticus", "Outcome"),
    ("ilae", "ILAE 2017 classification", "Guideline"),
    ("severity_l3", "Severity L3 (Severe)", "Severity"),
    ("temporal_lobe", "Temporal lobe focus", "BrainRegion"),
]

# Edges: (source, relation, target)
EDGES = [
    ("EP001", "hasSeizureType", "focal"),
    ("EP001", "hasSeverity", "severity_l3"),
    ("EP001", "treatedWith", "levetiracetam"),
    ("EP001", "assessedBy", "neurologist"),
    ("EP001", "assessedBy", "eeg_tech"),
    ("EP001", "atRiskOf", "breakthrough"),
    ("focal", "localizesTo", "temporal_lobe"),
    ("focal", "canEvolveTo", "ftbtc"),
    ("line_length", "predicts", "breakthrough"),
    ("band_gamma", "predicts", "breakthrough"),
    ("plv", "predicts", "breakthrough"),
    ("spike_rate", "indicates", "focal"),
    ("eeg_tech", "measures", "line_length"),
    ("eeg_tech", "measures", "band_gamma"),
    ("eeg_tech", "measures", "plv"),
    ("neurologist", "prescribes", "levetiracetam"),
    ("levetiracetam", "reduces", "breakthrough"),
    ("lamotrigine", "treats", "focal"),
    ("valproate", "treats", "generalized"),
    ("absence", "classifiedBy", "ilae"),
    ("generalized", "classifiedBy", "ilae"),
    ("breakthrough", "canEscalateTo", "status_epilepticus"),
    ("ilae", "grounds", "neurologist"),
]

TYPE_CLASS = {t for _, _, t in NODES}


def to_turtle():
    lines = [f"@prefix kg: <{NS}> .",
             "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
             "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .", ""]
    # class declarations
    for c in sorted(TYPE_CLASS):
        lines.append(f"kg:{c} a rdfs:Class .")
    lines.append("")
    # node instances
    for nid, label, typ in NODES:
        lines.append(f'kg:{nid} a kg:{typ} ; rdfs:label "{label}" .')
    lines.append("")
    # edges as triples
    for s, r, o in EDGES:
        lines.append(f"kg:{s} kg:{r} kg:{o} .")
    return "\n".join(lines) + "\n"


def main():
    banner("knowledge_graph_export — epilepsy RDF/Turtle + graph CSVs")
    pd.DataFrame(NODES, columns=["id", "label", "type"]).to_csv(os.path.join(DATA_DIR, "kg_nodes.csv"), index=False)
    pd.DataFrame(EDGES, columns=["source", "relation", "target"]).to_csv(os.path.join(DATA_DIR, "kg_edges.csv"), index=False)
    ttl_path = os.path.join(ROOT, "docs", "enterprise-flow", "epilepsy-kg.ttl")
    os.makedirs(os.path.dirname(ttl_path), exist_ok=True)
    open(ttl_path, "w", encoding="utf-8").write(to_turtle())
    print(f"  nodes={len(NODES)} edges={len(EDGES)} classes={len(TYPE_CLASS)}; "
          f"RDF -> docs/enterprise-flow/epilepsy-kg.ttl")


if __name__ == "__main__":
    main()
