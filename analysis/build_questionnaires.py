"""
build_questionnaires.py — Extract, validate & consolidate the per-role patient questionnaires
==============================================================================================

Every assessment section carries a "## Questionnaire (Enterprise Form)" table
(ID | Question | Response Type | Validation | EP001 (Example) | AI Feature). This
script:

  1. CHECKS every role/section for the questionnaire block.
  2. VALIDATES each table (required columns present, >=1 row, IDs prefixed by role).
  3. VERIFIES id uniqueness within a role.
  4. CREATES one consolidated patient questionnaire per role under
     docs/primary-assessment/questionnaires/<role>.md, plus an index and a
     validation report.

Run: python analysis/build_questionnaires.py
"""
from __future__ import annotations
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PA = os.path.join(ROOT, "docs", "primary-assessment")
OUT = os.path.join(PA, "questionnaires")
os.makedirs(OUT, exist_ok=True)

# role folder -> (display name, expected ID prefix)
ROLES = [
    ("neurologist", "Neurologist", "NEU"),
    ("eeg-technician", "EEG Technician", "EEG"),
    ("nurse", "Nurse", "NUR"),
    ("neuropsychologist", "Neuropsychologist", "NPS"),
    ("pharmacist", "Pharmacist", "PHA"),
    ("caregiver", "Caregiver", "CAR"),
    ("patient", "Patient", "PAT"),
    ("administrator", "Administrator", "ADM"),
    ("occupational-therapist", "Occupational Therapist", "OT"),
]
REQUIRED_COLS = ["ID", "Question", "Response Type", "Validation", "AI Feature"]


def h1_title(md: str, fallback: str) -> str:
    m = re.search(r"^\s*#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else fallback


def extract_questionnaire(md: str):
    """Return (header_cells, [row_cells,...]) for the first table after the
    '## Questionnaire (Enterprise Form)' heading, or None if absent."""
    idx = md.find("## Questionnaire (Enterprise Form)")
    if idx < 0:
        return None
    tail = md[idx:]
    rows = []
    header = None
    for line in tail.splitlines():
        t = line.strip()
        if t.startswith("|"):
            cells = [c.strip() for c in t.split("|")[1:-1]]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue  # separator
            if header is None:
                header = cells
            else:
                rows.append(cells)
        elif header is not None and not t.startswith("|"):
            if rows:
                break  # table ended
    return (header, rows) if header else None


def main() -> None:
    report = []          # (role, sections, questions, issues)
    index_rows = []
    total_q = 0

    for folder, name, prefix in ROLES:
        rdir = os.path.join(PA, folder)
        if not os.path.isdir(rdir):
            report.append((name, 0, 0, "MISSING FOLDER"))
            continue
        sections = sorted(f for f in os.listdir(rdir) if re.match(r"\d", f) and f.endswith(".md"))
        issues = []
        seen_ids = set()
        q_count = 0
        blocks = []  # (section_title, header, rows)

        for sec in sections:
            md = open(os.path.join(rdir, sec), encoding="utf-8").read()
            title = h1_title(md, sec)
            ex = extract_questionnaire(md)
            if ex is None:
                issues.append(f"{sec}: no questionnaire block")
                continue
            header, rows = ex
            missing = [c for c in REQUIRED_COLS if c not in header]
            if missing:
                issues.append(f"{sec}: missing cols {missing}")
            if not rows:
                issues.append(f"{sec}: zero rows")
            for r in rows:
                rid = r[0] if r else ""
                if not rid.upper().startswith(prefix):
                    issues.append(f"{sec}: id '{rid}' not prefixed {prefix}")
                if rid in seen_ids:
                    issues.append(f"{sec}: duplicate id '{rid}'")
                seen_ids.add(rid)
            q_count += len(rows)
            blocks.append((title, header, rows))

        total_q += q_count
        report.append((name, len(sections), q_count, "; ".join(issues) if issues else "OK"))
        index_rows.append((name, folder, len(sections), q_count))

        # --- write the consolidated per-role questionnaire ---
        out = [f"# {name} — Patient Questionnaire (Consolidated, EP001)\n",
               f"> **Why (this doc):** The complete set of questions the {name} asks the patient, "
               f"aggregated from every {name} assessment section into one enterprise form for "
               f"intake, EMR entry, and AI feature extraction. **How:** auto-generated from the "
               f"section questionnaires by `analysis/build_questionnaires.py`; do not edit by hand.\n",
               f"**Role:** {name} · **Sections:** {len(blocks)} · **Total questions:** {q_count} · "
               f"**ID prefix:** `{prefix}`\n"]
        for title, header, rows in blocks:
            short = re.sub(r"\s*\(EP001\)\s*$", "", title)
            out.append(f"\n## {short}\n")
            out.append("| " + " | ".join(header) + " |")
            out.append("|" + "|".join(["---"] * len(header)) + "|")
            for r in rows:
                r = (r + [""] * len(header))[:len(header)]
                out.append("| " + " | ".join(r) + " |")
        with open(os.path.join(OUT, f"{folder}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(out) + "\n")

    # --- index ---
    idx = ["# Patient Questionnaires — All Roles (Consolidated)\n",
           "> **Why (this doc):** One consolidated patient-facing questionnaire per role, "
           "aggregated from the section-level enterprise forms. **How:** generated + validated "
           "by `analysis/build_questionnaires.py`.\n",
           f"**Roles:** {len(index_rows)} · **Total questions across all roles:** {total_q}\n",
           "| Role | Questionnaire | Sections | Questions |", "|---|---|---|---|"]
    for nm, folder, ns, nq in index_rows:
        idx.append(f"| {nm} | [{folder}.md]({folder}.md) | {ns} | {nq} |")
    open(os.path.join(OUT, "index.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")

    # --- validation report ---
    rep = ["# Questionnaire Validation Report\n",
           "> Automated check that every role/section has a valid enterprise questionnaire "
           "(required columns, >=1 row, role-prefixed unique IDs).\n",
           "| Role | Sections | Questions | Status |", "|---|---|---|---|"]
    all_ok = True
    for nm, ns, nq, st in report:
        rep.append(f"| {nm} | {ns} | {nq} | {'✅ ' + st if st == 'OK' else '⚠️ ' + st} |")
        if st != "OK":
            all_ok = False
    rep.append(f"\n**Overall:** {'✅ ALL ROLES VALID' if all_ok else '⚠️ ISSUES FOUND (see above)'} "
               f"· total questions = {total_q}.")
    open(os.path.join(OUT, "validation-report.md"), "w", encoding="utf-8").write("\n".join(rep) + "\n")

    print(f"roles={len(index_rows)} total_questions={total_q} all_ok={all_ok}")
    for nm, ns, nq, st in report:
        print(f"  {nm:22s} sections={ns:2d} questions={nq:3d}  {st}")


if __name__ == "__main__":
    main()
