"""
run_all.py — One-command reproduction of the entire analytics deliverable
=========================================================================

Runs the four stages in dependency order so a reviewer can regenerate every dataset,
figure, and report from a clean checkout:

    1. make_cohort         build the linked primary + EEG cohort (deterministic)
    2. primary_analysis    end-to-end primary (clinical) statistical pipeline
    3. secondary_analysis  end-to-end EEG pipeline
    4. fusion_analysis      multimodal fusion + EP001 end-to-end case

Usage:  python analysis/run_all.py
"""
from __future__ import annotations
import make_cohort, primary_analysis, secondary_analysis, fusion_analysis
from common import banner


def main() -> None:
    banner("RUN ALL — epilepsy primary + secondary + fusion analytics")
    make_cohort.main()
    primary_analysis.main()
    secondary_analysis.main()
    fusion_analysis.main()
    banner("DONE — see docs/analysis/*.md and analysis/outputs/")


if __name__ == "__main__":
    main()
