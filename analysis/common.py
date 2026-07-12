"""
common.py — Shared configuration, reproducibility controls, and reporting helpers
=================================================================================

This module is the single source of truth for every path, random seed, clinical
threshold, and output helper used across the three analysis pipelines:

    primary_analysis.py    (clinical assessment / primary data)
    secondary_analysis.py  (EEG / secondary data)
    fusion_analysis.py     (multimodal fusion for one patient, EP001)

Design goals (production-grade, DBA-defensible):
  * DETERMINISM  — one global SEED so every table/figure is byte-reproducible.
  * TRACEABILITY — every artefact is written under analysis/outputs/<stage>/ and
                   every dataset under data/analysis/, so a reviewer can rebuild
                   the whole dissertation from `python analysis/run_all.py`.
  * SEPARATION   — validation (find problems) is kept distinct from cleaning
                   (fix problems); encoding/scaling are distinct from feature
                   engineering. Each concern lives in its own function.

Scope: EPILEPSY ONLY. Patient EP001 (EP-2026-001) is the canonical index case.
All data generated here is SYNTHETIC but clinically plausible and internally
consistent with EP001's documented profile.
"""

from __future__ import annotations
import os
import textwrap
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Reproducibility
# ---------------------------------------------------------------------------
# A single seed drives every stochastic step. We expose a factory so each script
# can obtain an independent-but-deterministic generator stream if it wants one,
# while `SEED` remains the master value quoted in the methods section.
SEED: int = 42


def rng(offset: int = 0) -> np.random.Generator:
    """Return a NumPy Generator seeded from the master SEED (+ optional offset).

    Using an offset lets separate stages draw independent streams that are still
    fully reproducible (e.g. cohort=rng(0), bootstrap=rng(1)).
    """
    return np.random.default_rng(SEED + offset)


# ---------------------------------------------------------------------------
# 2. Paths — everything is relative to the repo root (this file's grandparent).
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))          # .../Epi/analysis
ROOT = os.path.dirname(HERE)                                # .../Epi
DATA_DIR = os.path.join(ROOT, "data", "analysis")          # generated cohorts
OUT_DIR = os.path.join(HERE, "outputs")                    # tables + figures
DOCS_DIR = os.path.join(ROOT, "docs", "analysis")          # generated report md

for _d in (DATA_DIR, OUT_DIR, DOCS_DIR):
    os.makedirs(_d, exist_ok=True)


def out_path(stage: str, name: str) -> str:
    """Absolute path for an output artefact, creating analysis/outputs/<stage>/."""
    d = os.path.join(OUT_DIR, stage)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


# ---------------------------------------------------------------------------
# 3. Cohort size + clinical constants
# ---------------------------------------------------------------------------
N_PATIENTS: int = 500          # EP001 .. EP500 (subject-level unit of analysis)

# The 4-level epilepsy severity ladder used throughout the project. It is the
# supervised TARGET for the primary pipeline and the stratifier everywhere else.
SEVERITY_LEVELS = {
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Refractory/Status",
}
# Population prevalence of each level (roughly reflects a tertiary epilepsy clinic
# skewed toward harder cases; ~30% drug-resistant across L3/L4 combined).
SEVERITY_PREVALENCE = np.array([0.28, 0.34, 0.24, 0.14])

# Mean-score -> band thresholds, IDENTICAL to the viewer's scoring engine so the
# statistics and the interactive UI agree.
def band_from_mean(mean: float) -> int:
    """Map a mean severity score (1..4) to an ordinal level 1..4 (viewer-consistent)."""
    if mean < 1.75:
        return 1
    if mean < 2.5:
        return 2
    if mean < 3.25:
        return 3
    return 4


def pid(i: int) -> str:
    """Canonical patient id: EP001, EP002, ..."""
    return f"EP{i:03d}"


# ---------------------------------------------------------------------------
# 4. Reporting helpers — markdown tables, figure saving, and Mermaid/C4 blocks
#    so a single `python` run emits a policy-compliant report (tables + all four
#    Mermaid diagram types + a C4 model) with REAL computed numbers.
# ---------------------------------------------------------------------------
def df_to_md(df: pd.DataFrame, floatfmt: str = "{:.3f}", index: bool = False,
             max_rows: int | None = None) -> str:
    """Render a DataFrame as a GitHub-flavoured markdown table.

    We hand-roll this (instead of df.to_markdown, which needs `tabulate`) to keep
    the dependency surface minimal and the formatting fully under our control.
    """
    d = df.copy()
    if max_rows is not None and len(d) > max_rows:
        d = d.head(max_rows)

    def fmt(v):
        if isinstance(v, (float, np.floating)):
            if np.isnan(v):
                return ""
            return floatfmt.format(v)
        return str(v)

    cols = ([d.index.name or ""] if index else []) + [str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "|".join(["---"] * len(cols)) + "|"]
    for idx, row in d.iterrows():
        cells = ([str(idx)] if index else []) + [fmt(v) for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def save_fig(fig, stage: str, name: str) -> str:
    """Save a matplotlib figure as PNG under outputs/<stage>/ and return a
    repo-relative path suitable for referencing from the report markdown."""
    p = out_path(stage, name)
    fig.savefig(p, dpi=130, bbox_inches="tight")
    import matplotlib.pyplot as plt
    plt.close(fig)
    return os.path.relpath(p, ROOT).replace("\\", "/")


def explain(reason: str, why: str, what: str, how: str, ref: str) -> str:
    """Emit the mandatory per-diagram explanation block (global policy rule 21)."""
    return (f"**Reason:** {reason} **Why:** {why} **What is happening:** {what} "
            f"**How it is happening:** {how} **Reference:** {ref}")


def caption(text: str) -> str:
    """Emit a table caption (global policy rule 17)."""
    return f"*Caption - {text}*"


def write_report(filename: str, sections: list[str]) -> str:
    """Concatenate report sections and write to docs/analysis/<filename>."""
    p = os.path.join(DOCS_DIR, filename)
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n\n".join(s.strip("\n") for s in sections) + "\n")
    return p


def banner(msg: str) -> None:
    """Console section banner for the CLI run log."""
    print("\n" + "=" * 74 + f"\n{msg}\n" + "=" * 74)
