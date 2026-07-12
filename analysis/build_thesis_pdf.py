"""
build_thesis_pdf.py — Compile the DBA dissertation (docs/thesis/) into one thesis PDF
=====================================================================================

Assembles the front matter and all eight chapters into a single, page-numbered PDF with a
formal title page. Reuses the markdown parser and styles from build_pdf.py (headings,
paragraphs, tables, bullet lists, code, embedded PNG figures; Mermaid blocks are shown as
labelled diagram placeholders — the interactive viewer renders them live).

Output: docs/DBA-Epilepsy-Thesis.pdf
Run:    python analysis/build_thesis_pdf.py
"""
from __future__ import annotations
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

# Reuse the parser + styles already written for the technical-deliverable PDF.
from build_pdf import parse_md, ROOT, ss, BODY

CHAPTERS = [
    ("Front matter", "docs/thesis/00-front-matter.md"),
    ("Chapter 1 — Introduction", "docs/thesis/ch1-introduction.md"),
    ("Chapter 2 — Literature Review", "docs/thesis/ch2-literature-review.md"),
    ("Chapter 3 — Research Methodology", "docs/thesis/ch3-methodology.md"),
    ("Chapter 4 — System Design & Architecture", "docs/thesis/ch4-system-design.md"),
    ("Chapter 5 — Implementation", "docs/thesis/ch5-implementation.md"),
    ("Chapter 6 — Results & Evaluation", "docs/thesis/ch6-results-evaluation.md"),
    ("Chapters 7–8 — Discussion & Conclusion", "docs/thesis/ch7-8-discussion-conclusion.md"),
]


def main():
    title = ParagraphStyle("TT", parent=ss["Title"], fontSize=22, alignment=TA_CENTER,
                           textColor=colors.HexColor("#1e293b"), leading=28)
    sub = ParagraphStyle("TS", parent=BODY, alignment=TA_CENTER, fontSize=12,
                         textColor=colors.HexColor("#475569"), leading=17)
    story = [Spacer(1, 45 * mm),
             Paragraph("An Enterprise-Grade Explainable Multimodal AI Platform for Remote Epilepsy Care", title),
             Spacer(1, 6 * mm),
             Paragraph("Design, Implementation, and Evaluation", sub),
             Spacer(1, 18 * mm),
             Paragraph("A dissertation submitted in partial fulfilment of the requirements for the degree of", sub),
             Paragraph("<b>Doctor of Business Administration (DBA)</b>", sub),
             Spacer(1, 14 * mm),
             Paragraph("Scope: Epilepsy · Reference index case: Patient EP001", sub),
             Paragraph("Empirical basis: real scalp EEG (CHB-MIT) + external validation (EEG-Eye-State)", sub),
             PageBreak()]

    n_missing = 0
    for _, rel in CHAPTERS:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            n_missing += 1
            continue
        md = open(p, encoding="utf-8").read()
        story += parse_md(md, os.path.dirname(p))
        story.append(PageBreak())

    out = os.path.join(ROOT, "docs", "DBA-Epilepsy-Thesis.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm,
                            title="DBA Epilepsy Dissertation", author="EP001 project")

    def footer(canvas, d):
        canvas.saveState(); canvas.setFont("Helvetica", 7); canvas.setFillColor(colors.HexColor("#94a3b8"))
        canvas.drawString(22 * mm, 11 * mm, "DBA Dissertation — Explainable Multimodal AI for Remote Epilepsy Care")
        canvas.drawRightString(A4[0] - 22 * mm, 11 * mm, f"Page {d.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Thesis PDF -> {out} ({os.path.getsize(out)//1024} KB, "
          f"{len(CHAPTERS)-n_missing}/{len(CHAPTERS)} sections)")


if __name__ == "__main__":
    main()
