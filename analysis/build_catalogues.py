"""
build_catalogues.py — Pain-point register/matrix + visualization catalogue
===========================================================================

Scans the repo docs to generate two auto-maintained catalogues:
  docs/primary-assessment/pain-points-register.md  — every role's pain points as a matrix
  docs/analysis/visualization-catalogue.md         — every diagram/chart type + counts

Run: python analysis/build_catalogues.py
"""
from __future__ import annotations
import os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PA = os.path.join(ROOT, "docs", "primary-assessment")
DOCS = os.path.join(ROOT, "docs")


def _table_after(md: str, heading_regex: str):
    """Return rows of the first markdown table following a heading matching regex."""
    m = re.search(heading_regex, md, re.I)
    if not m:
        return None
    rows, header, started = [], None, False
    for line in md[m.end():].splitlines():
        t = line.strip()
        if t.startswith("|"):
            started = True
            cells = [c.strip() for c in t.split("|")[1:-1]]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue
            if header is None:
                header = cells
            else:
                rows.append(cells)
        elif started:
            break
    return rows


def pain_register():
    roles = sorted(glob.glob(os.path.join(PA, "roles-*.md")))
    out = ["# Pain-Point Register & Matrix (All Roles)\n",
           "> **Why (this doc):** A consolidated matrix of every role/stakeholder's pain points "
           "and the EP001 evidence/impact behind each — the problem space the platform addresses. "
           "**How:** auto-extracted from each `roles-*.md` landing page by "
           "`analysis/build_catalogues.py`.\n",
           "| Role | Pain Point | Evidence / Impact (EP001) |", "|---|---|---|"]
    total = 0
    for rp in roles:
        role = os.path.basename(rp).replace("roles-", "").replace(".md", "").replace("-", " ").title()
        md = open(rp, encoding="utf-8").read()
        rows = _table_after(md, r"##[^\n]*(Concern|Pain Point|Pain-Point)")
        if not rows:
            continue
        for r in rows:
            pain = r[0] if r else ""
            ev = r[1] if len(r) > 1 else ""
            out.append(f"| {role} | {pain} | {ev} |")
            total += 1
    out.insert(3, f"**Roles covered:** {len(roles)} · **Pain points:** {total}\n")
    open(os.path.join(PA, "pain-points-register.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    return len(roles), total


def viz_catalogue():
    files = glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True)
    kinds = {"flowchart TD/TB (flowchart)": r"```mermaid\s*\n\s*flowchart",
             "sequenceDiagram": r"```mermaid\s*\n\s*sequenceDiagram",
             "graph LR (network)": r"```mermaid\s*\n\s*graph\s+LR",
             "journey map": r"```mermaid\s*\n\s*journey",
             "C4 / container (flowchart TB subgraph)": r"subgraph\s+\w*\[?(System Context|Container|Ctx|Plat)",
             "PNG figures (matplotlib)": r"!\[[^\]]*\]\([^)]+\.png\)"}
    counts = {k: 0 for k in kinds}
    total_mermaid = 0
    for f in files:
        md = open(f, encoding="utf-8", errors="ignore").read()
        total_mermaid += len(re.findall(r"```mermaid", md))
        for k, rx in kinds.items():
            counts[k] += len(re.findall(rx, md, re.I))
    out = ["# Visualization & Diagram Catalogue\n",
           "> **Why (this doc):** Confirms the mandated visual types (flowchart, sequence, "
           "network, journey, C4) and computed charts are present across the documentation. "
           "**How:** auto-counted across all `docs/**/*.md` by `analysis/build_catalogues.py`.\n",
           f"**Markdown files scanned:** {len(files)} · **Total Mermaid diagrams:** {total_mermaid}.\n",
           "| Visualization type | Occurrences |", "|---|---|"]
    for k, v in counts.items():
        out.append(f"| {k} | {v} |")
    out.append("\n**Diagram standard (per GLOBAL-POLICY rule 5 & 21):** every substantive doc "
               "carries a flowchart, a sequence diagram, a network (graph LR) diagram, and a "
               "journey map; architecture docs add a C4 model. Analytics reports add computed "
               "PNG charts (correlation heatmap, severity boxplot, SHAP importance, EEG asymmetry).")
    open(os.path.join(DOCS, "analysis", "visualization-catalogue.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    return len(files), total_mermaid, counts


def main():
    nr, npain = pain_register()
    nf, nm, counts = viz_catalogue()
    print(f"pain register: roles={nr} pain_points={npain}")
    print(f"viz catalogue: files={nf} mermaid={nm}")
    for k, v in counts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
