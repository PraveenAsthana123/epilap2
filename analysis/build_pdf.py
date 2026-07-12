"""
build_pdf.py — Compile the DBA epilepsy deliverable into a single PDF
=====================================================================

Renders a curated set of the project's Markdown docs (headings, paragraphs, tables,
bullet lists, code, and real PNG figures) into one navigable PDF with a title page and
table of contents. Mermaid code fences are shown as labelled diagram placeholders (they
need a browser to render — the live viewer shows them interactively).

Output: docs/DBA-Epilepsy-Deliverable.pdf
Run:    python analysis/build_pdf.py
"""
from __future__ import annotations
import os, re, html
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, Image, ListFlowable, ListItem)
from reportlab.lib.enums import TA_CENTER

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Curated deliverable, in reading order.
DOCS = [
    ("Overview", "docs/00-overview.md"),
    ("Global Policy", "docs/GLOBAL-POLICY.md"),
    ("Secondary (EEG) — 23-Phase Pipeline on Real Data", "docs/analysis/secondary-eeg-full.md"),
    ("AIOps · DataOps · ModelOps · Fusion · Decision-AI", "docs/analysis/aiops-dataops-modelops-fusion.md"),
    ("Vector DB Pipeline for RAG", "docs/analysis/vector-db-rag.md"),
    ("Security & Compliance (HIPAA/NIST/OWASP)", "docs/governance/00-security-compliance.md"),
    ("IRB Submission", "docs/governance/01-irb-submission.md"),
    ("Patient Consent + EULA", "docs/governance/02-patient-consent-eula.md"),
    ("Model Lifecycle — Phase-Gate Scorecard", "docs/phase-gates-scorecard.md"),
]

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1x", parent=ss["Heading1"], fontSize=18, spaceBefore=6, spaceAfter=10, textColor=colors.HexColor("#3730a3"))
H2 = ParagraphStyle("H2x", parent=ss["Heading2"], fontSize=14, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#4f46e5"))
H3 = ParagraphStyle("H3x", parent=ss["Heading3"], fontSize=11.5, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#1f2937"))
BODY = ParagraphStyle("Bodyx", parent=ss["BodyText"], fontSize=9.5, leading=13)
QUOTE = ParagraphStyle("Quotex", parent=BODY, leftIndent=10, textColor=colors.HexColor("#475569"), fontName="Helvetica-Oblique")
CODE = ParagraphStyle("Codex", parent=BODY, fontName="Courier", fontSize=8, textColor=colors.HexColor("#334155"),
                      backColor=colors.HexColor("#f1f5f9"), borderPadding=4)
CAP = ParagraphStyle("Capx", parent=BODY, fontSize=8, textColor=colors.HexColor("#64748b"), fontName="Helvetica-Oblique")


def inline(t: str) -> str:
    t = html.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", t)          # strip md links -> text
    return t


def table_from(rows):
    cells = [[Paragraph(inline(c), BODY) for c in r] for r in rows]
    t = Table(cells, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0e7ff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def parse_md(md: str, base_dir: str):
    flow, i = [], 0
    lines = md.split("\n")
    bullets = []

    def flush_bullets():
        nonlocal bullets
        if bullets:
            flow.append(ListFlowable([ListItem(Paragraph(inline(b), BODY), leftIndent=8) for b in bullets],
                                     bulletType="bullet", start="•"))
            bullets = []

    while i < len(lines):
        ln = lines[i].rstrip()
        # code fence
        if ln.strip().startswith("```"):
            flush_bullets()
            lang = ln.strip()[3:].strip()
            buf, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            if lang == "mermaid":
                flow.append(Paragraph("◈ Diagram (Mermaid — interactive in the viewer): " +
                                      inline(buf[0] if buf else ""), CAP))
            else:
                text = html.escape("\n".join(buf)).replace(" ", "&nbsp;").replace("\n", "<br/>")
                flow.append(Paragraph(text, CODE))
            flow.append(Spacer(1, 4))
            continue
        # table
        if ln.startswith("|") and "|" in ln[1:]:
            flush_bullets()
            trows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not re.match(r"^-{2,}$", cells[0].replace(":", "") or "-") or any(c and not set(c) <= set("-: ") for c in cells):
                    if not all(set(c) <= set("-: ") for c in cells if c != ""):
                        trows.append(cells)
                i += 1
            if trows:
                flow.append(table_from(trows)); flow.append(Spacer(1, 6))
            continue
        # image
        m = re.match(r"!\[(.*?)\]\((.+?)\)", ln.strip())
        if m:
            flush_bullets()
            p = os.path.join(ROOT, m.group(2).replace("/", os.sep))
            if os.path.exists(p):
                try:
                    img = Image(p); img._restrictSize(150 * mm, 90 * mm)
                    flow.append(img); flow.append(Paragraph(inline(m.group(1)), CAP)); flow.append(Spacer(1, 6))
                except Exception:
                    pass
            i += 1; continue
        # headings
        if ln.startswith("### "):
            flush_bullets(); flow.append(Paragraph(inline(ln[4:]), H3))
        elif ln.startswith("## "):
            flush_bullets(); flow.append(Paragraph(inline(ln[3:]), H2))
        elif ln.startswith("# "):
            flush_bullets(); flow.append(Paragraph(inline(ln[2:]), H1))
        elif ln.startswith(">"):
            flush_bullets(); flow.append(Paragraph(inline(ln.lstrip(">").strip()), QUOTE))
        elif re.match(r"^\s*[-*] ", ln):
            bullets.append(re.sub(r"^\s*[-*] ", "", ln))
        elif ln.strip().startswith("*Caption"):
            flush_bullets(); flow.append(Paragraph(inline(ln.strip().strip("*")), CAP))
        elif ln.strip() == "":
            flush_bullets(); flow.append(Spacer(1, 4))
        else:
            flush_bullets(); flow.append(Paragraph(inline(ln), BODY))
        i += 1
    flush_bullets()
    return flow


def main():
    story = []
    title = ParagraphStyle("T", parent=ss["Title"], fontSize=24, alignment=TA_CENTER, textColor=colors.HexColor("#3730a3"))
    sub = ParagraphStyle("Sub", parent=BODY, alignment=TA_CENTER, fontSize=12, textColor=colors.HexColor("#475569"))
    story += [Spacer(1, 60 * mm),
              Paragraph("Explainable AI-Driven Remote Epilepsy Care Platform", title),
              Spacer(1, 8 * mm),
              Paragraph("DBA Deliverable — Real-Data EEG Pipeline, Governance, and Responsible AI", sub),
              Spacer(1, 4 * mm),
              Paragraph("Patient index case: EP001 · Compiled from the project documentation set", sub),
              PageBreak()]
    # Table of contents
    story += [Paragraph("Contents", H1)]
    story += [ListFlowable([ListItem(Paragraph(f"{n}. {t}", BODY)) for n, (t, _) in enumerate(DOCS, 1)],
                           bulletType="1"), PageBreak()]

    for t, rel in DOCS:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        md = open(p, encoding="utf-8").read()
        story += parse_md(md, os.path.dirname(p))
        story.append(PageBreak())

    out = os.path.join(ROOT, "docs", "DBA-Epilepsy-Deliverable.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=16 * mm, bottomMargin=16 * mm,
                            title="DBA Epilepsy Deliverable", author="EP001 project")

    def footer(canvas, d):
        canvas.saveState(); canvas.setFont("Helvetica", 7); canvas.setFillColor(colors.HexColor("#94a3b8"))
        canvas.drawString(18 * mm, 10 * mm, "Explainable AI-Driven Remote Epilepsy Care — DBA deliverable (epilepsy only)")
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {d.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"PDF written -> {out} ({os.path.getsize(out)//1024} KB, {len(DOCS)} sections)")


if __name__ == "__main__":
    main()
