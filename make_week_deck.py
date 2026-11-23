"""Builds the weekly-tasks deck: one slide per week of the 13-week plan."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

NAVY = RGBColor(0x1F, 0x29, 0x37)
EMERALD = RGBColor(0x05, 0x96, 0x69)
GREY = RGBColor(0x6B, 0x72, 0x80)
LIGHT = RGBColor(0xF3, 0xF4, 0xF6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
AMBER = RGBColor(0xB4, 0x53, 0x09)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def box(s, x, y, w, h, fill=None, line=None):
    shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    shp.shadow.inherit = False
    return shp


def text(s, x, y, w, h, runs, size=18, color=NAVY, bold=False, align=PP_ALIGN.LEFT, space_after=8):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    if isinstance(runs, str):
        runs = [runs]
    for i, para in enumerate(runs):
        opts = {}
        if isinstance(para, tuple):
            para, opts = para
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = opts.get("align", align)
        p.space_after = Pt(opts.get("space_after", space_after))
        r = p.add_run()
        r.text = para
        f = r.font
        f.size = Pt(opts.get("size", size))
        f.bold = opts.get("bold", bold)
        f.color.rgb = opts.get("color", color)
        f.name = "Calibri"
    return tb


def bullets(s, x, y, w, h, items, size=16, gap=9):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        r = p.add_run()
        r.text = "\u2022  " + it
        r.font.size = Pt(size)
        r.font.color.rgb = NAVY
        r.font.name = "Calibri"
    return tb


# ---------------------------------------------------------------- week content
WEEKS = [
    dict(n=1, marks=4, topic="Introduction to Software Engineering and Process Models",
         task="Write a project proposal for your chosen topic, justify the process model you will "
              "follow, and set up your source repository.",
         did=["Proposal: problem, 4 stakeholder groups, 6 SMART objectives, in/out of scope",
              "Incremental model chosen and justified against waterfall, prototyping and Scrum",
              "Local Git repository initialised with the core system committed"],
         evidence="docs/week01_proposal.md  \u00b7  first commit 9cefa6a"),
    dict(n=2, marks=8, topic="Requirements Engineering",
         task="Produce SRS sections 1\u20133 \u2014 introduction, stakeholders, functional and "
              "non-functional requirements \u2014 plus user stories with acceptance criteria.",
         did=["14 functional and 8 non-functional requirements, numbered for traceability",
              "8 user stories, each with testable acceptance criteria",
              "Requirements traced forward to tests in week 10"],
         evidence="docs/week02_srs.md  \u00b7  every FR maps to a pytest case"),
    dict(n=3, marks=6, topic="Requirements Validation and Planning",
         task="Validate the requirements, prioritise them with MoSCoW, estimate effort, build a "
              "13-week plan and a risk register.",
         did=["Validation pass that cut two requirements (email alerts, admin dashboard)",
              "MoSCoW with a binding \u201cWon't have\u201d list, estimates vs actuals (+8 %)",
              "Scored risk register \u2014 R1 and R4 both materialised and were mitigated"],
         evidence="docs/week03_planning.md  \u00b7  50 h estimated, 54 h actual"),
    dict(n=4, marks=8, topic="System Modelling with UML",
         task="Model the system: use case, class, sequence (main flow) and activity diagrams.",
         did=["Use case diagram: 4 actors, 13 use cases",
              "Domain class model with the Item status lifecycle",
              "2 sequence diagrams (claim flow, finder response) + 2 activity diagrams"],
         evidence="docs/week04_uml.md  \u00b7  all diagrams in Mermaid, render on GitHub"),
    dict(n=5, marks=8, topic="Software Architecture and Database Design",
         task="Select and justify an architecture, produce a component diagram, an ERD and a "
              "database schema script.",
         did=["Layered monolith with a REST boundary \u2014 three alternatives explicitly rejected",
              "Component diagram (client PWA \u2194 FastAPI \u2194 db.json/uploads)",
              "ERD plus a 7-table PostgreSQL schema as the migration path"],
         evidence="docs/week05_architecture.md  \u00b7  migration is a transcription, not a redesign"),
    dict(n=6, marks=6, topic="Design Patterns and UI/UX Design",
         task="Apply at least two design patterns, produce wireframes, and deliver one "
              "SOLID-compliant module.",
         did=["4 patterns: Repository, Strategy, Facade, Observer (polling)",
              "6 wireframes incl. mobile layout and the modals",
              "SOLID analysis of public_item() \u2014 the privacy sanitizer"],
         evidence="docs/week06_design.md  \u00b7  patterns named after they emerged, then enforced"),
    dict(n=7, marks=6, topic="Implementation I and Version Control",
         task="Set a coding standard, deliver the first core module, and use branches/PRs with a "
              "clear Git history.",
         did=["9-rule coding standard (permission docstrings, save_state invariant, escaping)",
              "Module 1: report form, validation, browse grid, search, duplicate warning",
              "Feature branches + a 4-point merge checklist, incl. permission-negative tests"],
         evidence="docs/week07_implementation.md  \u00b7  main.py + static/"),
    dict(n=8, marks=10, topic="Mid-Semester Review: Prototype Demo",
         task="Demonstrate the working prototype covering the main user flow, report progress "
              "against the plan, and update the backlog.",
         did=["12-step, 7-minute demo script with an offline fallback path",
              "Progress report: prototype complete, features a week ahead of schedule",
              "Backlog updated with 3 items found during demo preparation"],
         evidence="docs/week08_demo.md  \u00b7  chat and disputes already working at W8"),
    dict(n=9, marks=6, topic="Implementation II, Refactoring and Code Quality",
         task="Deliver the remaining modules, record a peer code-review log, refactor, and run "
              "static analysis.",
         did=["6 modules: finder responses, chat, disputes, moderation, accounts, PWA",
              "Code-review log with 10 findings (4 high severity, all fixed)",
              "6 refactors incl. extracting the whole UI out of main.py"],
         evidence="docs/week09_quality.md  \u00b7  pyflakes and node --check clean"),
    dict(n=10, marks=8, topic="Software Testing",
         task="Write a test plan and test cases, produce a coverage report, and keep a defect log.",
         did=["28 automated tests, 84 % line coverage against an 80 % gate",
              "9 tests assert the wrong user receives 403 \u2014 the permission matrix as evidence",
              "Defect log: 10 defects, root causes traced, 0 open"],
         evidence="docs/week10_testing.md  \u00b7  python -m pytest --cov=main -q"),
    dict(n=11, marks=8, topic="Secure Development and DevOps",
         task="Produce a STRIDE threat model, check the OWASP Top 10, set up CI, and deploy.",
         did=["12-entry STRIDE model with honest residual risks (identity, hashing)",
              "OWASP Top 10 table \u2014 partials marked as partial, not rounded up",
              "GitHub Actions CI with coverage gate + live deployment on Render"],
         evidence="docs/week11_security_devops.md  \u00b7  .github/workflows/ci.yml"),
    dict(n=12, marks=6, topic="Maintenance, Documentation and Software Metrics",
         task="Process one change request with an impact analysis, write the user manual and "
              "technical documentation, and report software metrics.",
         did=["CR-001 processed: email notifications deferred, in-app indicators shipped",
              "8-section user manual plus maintainer documentation",
              "12-metric report incl. effort variance and defect closure"],
         evidence="docs/week12_maintenance.md  \u00b7  84 % coverage, 0 open defects"),
    dict(n=13, marks=16, topic="Final Demonstration, Report and Reflection",
         task="Give the final demonstration, submit the final report, reflect on the process, "
              "and complete the peer assessment.",
         did=["Final demo: full lifecycle on the deployed app",
              "Final report with 4 known limitations stated plainly",
              "Reflection on 4 lessons \u2014 chief among them: server decides, client renders"],
         evidence="docs/week13_final_report.md  \u00b7  live at afit-lost-and-found.onrender.com"),
]


def week_slide(w, idx):
    s = slide()
    box(s, 0, 0, 13.333, 0.18, fill=EMERALD)

    text(s, 0.55, 0.34, 8, 0.4, f"WEEK {w['n']} OF 13", size=15, bold=True, color=EMERALD)
    text(s, 0.55, 0.72, 10.4, 1.0, w["topic"], size=32, bold=True, color=NAVY)

    # marks pill
    box(s, 11.55, 0.4, 1.25, 0.55, fill=AMBER)
    text(s, 11.55, 0.5, 1.25, 0.35, f"{w['marks']} MARKS", size=12, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER)

    # the task
    box(s, 0.55, 2.0, 12.25, 1.35, fill=LIGHT)
    box(s, 0.55, 2.0, 0.09, 1.35, fill=EMERALD)
    text(s, 0.9, 2.1, 2.0, 0.35, "THE TASK", size=12.5, bold=True, color=EMERALD)
    text(s, 0.9, 2.45, 11.6, 0.85, w["task"], size=17, color=NAVY)

    # what was delivered
    text(s, 0.55, 3.6, 8, 0.4, "WHAT I DELIVERED", size=12.5, bold=True, color=EMERALD)
    bullets(s, 0.55, 4.05, 12.25, 2.2, w["did"], size=16.5, gap=11)

    # evidence strip
    box(s, 0.55, 6.55, 12.25, 0.62, fill=NAVY)
    text(s, 0.85, 6.7, 11.7, 0.4, "Evidence:  " + w["evidence"], size=13, color=WHITE)

    text(s, 12.3, 7.1, 0.6, 0.3, str(idx), size=10, color=GREY, align=PP_ALIGN.RIGHT)
    return s


# ---------------------------------------------------------------- title slide
s = slide()
box(s, 0, 0, 13.333, 7.5, fill=NAVY)
box(s, 0, 3.62, 13.333, 0.07, fill=EMERALD)
text(s, 1.2, 1.5, 11, 0.5, "SP-014  \u00b7  CSC 403  \u00b7  COMPUTER SCIENCE", size=18, bold=True, color=EMERALD)
text(s, 1.2, 2.05, 11, 1.3, "13 Weeks, 13 Deliverables", size=56, bold=True, color=WHITE)
text(s, 1.2, 3.85, 11, 0.6, "The weekly task breakdown for the AFIT Lost & Found Portal",
     size=22, color=RGBColor(0x9C, 0xA3, 0xAF))
text(s, 1.2, 5.15, 11, 1.3, [
    "Mathew Umama  \u00b7  U23CS1067",
    "Every week's given task, and what was delivered against it",
], size=19, color=WHITE, space_after=6)

# ---------------------------------------------------------------- the week slides
for i, w in enumerate(WEEKS, start=1):
    week_slide(w, i)

# ---------------------------------------------------------------- closing slide
s = slide()
box(s, 0, 0, 13.333, 7.5, fill=NAVY)
box(s, 0, 3.5, 13.333, 0.07, fill=EMERALD)
text(s, 1.2, 1.6, 11, 0.6, "THE THROUGH-LINE", size=16, bold=True, color=EMERALD)
text(s, 1.2, 2.1, 11, 1.2, "100 marks, 13 increments", size=46, bold=True, color=WHITE)
text(s, 1.2, 3.75, 11, 2.0, [
    "Each week produced something runnable, reviewable or measurable \u2014 never just paperwork.",
    "The plan from week 3 was exercised, not followed blindly: two requirements were cut at "
    "validation, and the week-8 demo sent three new items into the backlog.",
    "Testing and security were scheduled as their own weeks, which is why the defect log ends "
    "at zero open.",
], size=18, color=WHITE, space_after=12)
text(s, 1.2, 6.3, 11, 0.5, "Mathew Umama  \u00b7  U23CS1067  \u00b7  Computer Science  \u00b7  CSC 403",
     size=16, color=RGBColor(0x9C, 0xA3, 0xAF))

NOTES = [
    "This deck walks through the thirteen weeks of the course, one slide per week: the task I was "
    "given, and what I actually delivered against it. Thirteen weeks, one hundred marks.",
    # W1
    "Week one: the proposal. I was asked to propose a project, justify a process model, and set up a "
    "repository. I delivered the proposal with the problem, four stakeholder groups, six SMART "
    "objectives and an explicit out-of-scope list, justified the incremental model against waterfall, "
    "prototyping and Scrum, and initialised the Git repository.",
    # W2
    "Week two: requirements engineering. The task was SRS sections one to three plus user stories with "
    "acceptance criteria. I wrote fourteen functional and eight non-functional requirements, numbered "
    "so they could be traced to tests later, and eight user stories whose acceptance criteria I could "
    "actually test in week ten.",
    # W3
    "Week three: validation and planning. I validated my own requirements and that exercise cut two "
    "requirements outright - email notifications and an admin dashboard. Then MoSCoW prioritisation, "
    "estimates against actuals, the thirteen-week schedule, and a scored risk register. Two of those "
    "risks, scope creep and the stale-browser problem, actually happened later.",
    # W4
    "Week four: UML modelling. Use case diagram with four actors and thirteen use cases, the domain "
    "class model with the item status lifecycle, two sequence diagrams for the two mirrored flows, "
    "and two activity diagrams. All in Mermaid, so they render directly on GitHub.",
    # W5
    "Week five: architecture and database design. I justified a layered monolith over three "
    "alternatives, produced the component diagram, the ERD, and a full PostgreSQL schema as the "
    "migration path. That schema has seven tables and is a direct transcription of the ERD.",
    # W6
    "Week six: design patterns and UI. Four patterns - Repository, Strategy, Facade and Observer - "
    "plus six wireframes including the mobile layout, and a SOLID analysis of the privacy module, "
    "public_item, which is the piece of the system I am most confident defends itself on every "
    "principle.",
    # W7
    "Week seven: implementation one. The task was a coding standard, the first core module, and "
    "proper version control. I delivered a nine-rule standard, the complete reporting and browse "
    "module, and a branch workflow with a merge checklist that requires a permission-negative test "
    "for every new behaviour.",
    # W8
    "Week eight: the mid-semester prototype demo. Twelve steps, about seven minutes, with an offline "
    "fallback path rehearsed. At this point I was ahead of schedule - chat and disputes were already "
    "working - and the three questions the audience asked went straight into the backlog.",
    # W9
    "Week nine: implementation two and code quality. Six more modules, a peer review log with ten "
    "findings of which four were high severity and all were fixed, six refactors including extracting "
    "the entire UI out of the backend file, and a static analysis pass that came back clean.",
    # W10
    "Week ten: testing. Twenty-eight automated tests, eighty-four percent line coverage against an "
    "eighty percent gate, twenty-three documented test cases, and a defect log of ten defects with "
    "correct root causes and zero still open.",
    # W11
    "Week eleven: security and DevOps. A twelve-entry STRIDE threat model with honest residual risks, "
    "an OWASP Top Ten table where the partials are marked as partial rather than rounded up, a GitHub "
    "Actions pipeline with a coverage gate, and a real deployment that redeploys automatically on "
    "every push.",
    # W12
    "Week twelve: maintenance and metrics. I processed change request CR-001 properly - impact "
    "analysis, decision to defer email notifications while shipping the in-app alternative - wrote "
    "the eight-section user manual, and reported twelve metrics including effort variance.",
    # W13
    "Week thirteen: the final demonstration, report and reflection. The capability checklist covers "
    "twelve items, the final report states four known limitations plainly instead of hiding them, "
    "and the reflection is built around the four lessons the defect log taught me.",
    # close
    "So: one hundred marks across thirteen increments, and the through-line is the same every week - "
    "each week produced something runnable, reviewable or measurable, never just paperwork. Thank you.",
]

for sl, note in zip(prs.slides, NOTES):
    sl.notes_slide.notes_text_frame.text = note

OUT = "AFIT_SP014_Weekly_Tasks_Slides.pptx"
try:
    prs.save(OUT)
except PermissionError:
    OUT = "AFIT_SP014_Weekly_Tasks_Slides_v2.pptx"
    prs.save(OUT)
    print("(original was open in PowerPoint - saved under a v2 name instead)")
print(f"Saved {OUT} with {len(prs.slides._sldIdLst)} slides and speaker notes")
