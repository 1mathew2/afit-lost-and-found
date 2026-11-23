"""Convert the docs/*.md documentation package to Word (.docx) files.

Usage: python md_to_docx.py
Output: docs/word/<name>.docx
"""
import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor, Inches

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "docs")
OUT = os.path.join(SRC, "word")
EMERALD = RGBColor(0x05, 0x96, 0x69)
NAVY = RGBColor(0x1F, 0x29, 0x37)

INLINE_RE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`)")


def add_inline(par, text):
    """Adds text to a paragraph, honouring **bold** and `code`."""
    for chunk in INLINE_RE.split(text):
        if not chunk:
            continue
        if chunk.startswith("**") and chunk.endswith("**"):
            run = par.add_run(chunk[2:-2])
            run.bold = True
        elif chunk.startswith("`") and chunk.endswith("`"):
            run = par.add_run(chunk[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(9.5)
        else:
            par.add_run(chunk)


def make_document(md_path, docx_path, title):
    doc = Document()

    # base styles
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    for i, size in ((1, 20), (2, 14), (3, 12), (4, 11.5)):
        try:
            st = doc.styles[f"Heading {i}"]
            st.font.size = Pt(size)
            st.font.color.rgb = EMERALD if i <= 2 else NAVY
        except KeyError:
            pass

    doc.core_properties.author = "Mathew Umama"
    doc.core_properties.title = title

    lines = open(md_path, encoding="utf-8").read().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # ---- fenced code block
        if line.startswith("```"):
            i += 1
            block = []
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.space_after = Pt(10)
            run = p.add_run("\n".join(block))
            run.font.name = "Consolas"
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            continue

        # ---- table
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1].strip()):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            table = doc.add_table(rows=1, cols=len(header))
            table.style = "Light Grid Accent 1"
            for idx, h in enumerate(header):
                cell = table.rows[0].cells[idx]
                cell.text = ""
                add_inline(cell.paragraphs[0], h)
                for r in cell.paragraphs[0].runs:
                    r.bold = True
            for row in rows:
                cells = table.add_row().cells
                for idx, val in enumerate(row[: len(header)]):
                    cells[idx].text = ""
                    add_inline(cells[idx].paragraphs[0], val)
            doc.add_paragraph()
            continue

        # ---- headings
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level, txt = len(m.group(1)), m.group(2)
            if level == 1:
                p = doc.add_heading(level=0)
                add_inline(p, txt)
            else:
                p = doc.add_heading(level=level - 1)
                add_inline(p, txt)
            i += 1
            continue

        # ---- horizontal rule
        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            i += 1
            continue

        # ---- blockquote
        if line.startswith(">"):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.35)
            add_inline(p, line.lstrip("> ").strip())
            for r in p.runs:
                r.italic = True
                r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
            i += 1
            continue

        # ---- bullet / numbered list
        mb = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        mn = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if mb:
            level = len(mb.group(1)) // 2
            p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
            add_inline(p, mb.group(2))
            i += 1
            continue
        if mn:
            p = doc.add_paragraph(style="List Number")
            add_inline(p, mn.group(3))
            i += 1
            continue

        # ---- blank
        if not line.strip():
            i += 1
            continue

        # ---- paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        add_inline(p, line.strip())
        i += 1

    doc.save(docx_path)
    return docx_path


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".md"):
            continue
        md = os.path.join(SRC, name)
        title = name.replace(".md", "").replace("_", " ").title()
        out = os.path.join(OUT, name.replace(".md", ".docx"))
        make_document(md, out, title)
        made.append(os.path.basename(out))
    print(f"Converted {len(made)} documents to {OUT}")
    for m in made:
        print("  -", m)


if __name__ == "__main__":
    main()
