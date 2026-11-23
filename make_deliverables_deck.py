"""Deliverables deck: shows the actual content of each graded artifact."""
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


def text(s, x, y, w, h, runs, size=17, color=NAVY, bold=False, align=PP_ALIGN.LEFT, space_after=7):
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


def header(s, kicker, title, marks=None):
    box(s, 0, 0, 13.333, 0.18, fill=EMERALD)
    text(s, 0.55, 0.32, 9.5, 0.4, kicker, size=15, bold=True, color=EMERALD)
    text(s, 0.55, 0.7, 10.8, 0.95, title, size=32, bold=True, color=NAVY)
    if marks:
        box(s, 11.75, 0.36, 1.05, 0.55, fill=AMBER)
        text(s, 11.75, 0.46, 1.05, 0.35, marks, size=11.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)


def bullets(s, x, y, w, h, items, size=16, gap=8):
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


def table(s, x, y, w, rows, widths, size=12.5, header_size=12.5, row_h=0.42, head_h=0.46):
    n_rows, n_cols = len(rows), len(rows[0])
    total_h = head_h + row_h * (n_rows - 1)
    shape = s.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(total_h))
    tbl = shape.table
    scale = w / sum(widths)
    for i, cw in enumerate(widths):
        tbl.columns[i].width = Inches(cw * scale)
    tbl.rows[0].height = Inches(head_h)
    for ri in range(1, n_rows):
        tbl.rows[ri].height = Inches(row_h)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.text = ""
            cell.margin_left = Inches(0.07)
            cell.margin_right = Inches(0.05)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = 3  # middle
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = str(val)
            r.font.size = Pt(header_size if ri == 0 else size)
            r.font.name = "Calibri"
            r.font.bold = ri == 0
            r.font.color.rgb = WHITE if ri == 0 else NAVY
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if ri == 0 else (LIGHT if ri % 2 else WHITE)
    return tbl


def card(s, x, y, w, h, title, body, tsize=15, bsize=13, accent=EMERALD):
    box(s, x, y, w, h, fill=LIGHT)
    box(s, x, y, 0.08, h, fill=accent)
    text(s, x + 0.24, y + 0.1, w - 0.4, 0.35, title, size=tsize, bold=True, color=NAVY)
    text(s, x + 0.24, y + 0.5, w - 0.4, h - 0.6, body, size=bsize, color=GREY, space_after=3)


NOTES = []

# ============================================================ 1 title
s = slide()
box(s, 0, 0, 13.333, 7.5, fill=NAVY)
box(s, 0, 3.62, 13.333, 0.07, fill=EMERALD)
text(s, 1.2, 1.6, 11, 0.5, "SP-014  \u00b7  CSC 403  \u00b7  COMPUTER SCIENCE", size=18, bold=True, color=EMERALD)
text(s, 1.2, 2.15, 11, 1.3, "The Deliverables", size=58, bold=True, color=WHITE)
text(s, 1.2, 3.9, 11, 0.6, "What was produced for each week \u2014 the actual artefacts, not summaries",
     size=21, color=RGBColor(0x9C, 0xA3, 0xAF))
text(s, 1.2, 5.15, 11, 1.2, [
    "Mathew Umama  \u00b7  U23CS1067",
    "Proposal \u00b7 requirements \u00b7 plan \u00b7 models \u00b7 architecture \u00b7 design \u00b7 code \u00b7 tests \u00b7 security \u00b7 docs",
], size=18, color=WHITE, space_after=6)
NOTES.append("This deck is the evidence deck. Instead of describing the methods, each slide shows the actual "
             "artefact: the requirement list, the risk register rows, the test cases, the defect log. If I am asked "
             "'show me your requirements' or 'what was in your proposal', this is where I go.")

# ============================================================ 2 proposal
s = slide()
header(s, "DELIVERABLE 1 \u00b7 WEEK 1", "Project proposal", "4")
text(s, 0.55, 1.75, 6.1, 0.35, "The problem", size=16, bold=True, color=EMERALD)
bullets(s, 0.55, 2.15, 6.1, 1.9, [
    "Lost property is tracked informally: notice boards, WhatsApp, paper logs",
    "Students cannot search the security post's record",
    "Recovered items go unclaimed \u2014 finder and owner never meet",
], size=14.5, gap=7)
text(s, 0.55, 3.95, 6.1, 0.35, "Six SMART objectives", size=16, bold=True, color=EMERALD)
bullets(s, 0.55, 4.35, 6.1, 2.3, [
    "Report in under 2 minutes",
    "Search + filter by type, category, location, keyword",
    "Verified claim-and-return for found items",
    "Lighter finder-response flow for lost items, with chat",
    "Auditable trail of claims, disputes, resolutions",
    "Ship as an installable mobile PWA by week 13",
], size=13.5, gap=4)
card(s, 7.0, 1.75, 5.8, 2.1, "In scope (v1.0)",
     "Reporting with photos \u00b7 search \u00b7 claims \u00b7 finder responses \u00b7 private chat \u00b7 "
     "disputes \u00b7 moderation \u00b7 accounts \u00b7 validation \u00b7 anti-spam \u00b7 PWA \u00b7 persistence",
     bsize=12.5)
card(s, 7.0, 4.05, 5.8, 1.55, "Out of scope (v1.0)",
     "Email/SMS servers \u00b7 payments \u00b7 student-records integration \u00b7 native apps \u00b7 "
     "multi-campus \u00b7 image recognition", bsize=12.5, accent=AMBER)
card(s, 7.0, 5.75, 5.8, 1.15, "Process model chosen",
     "Incremental \u2014 waterfall, prototyping and Scrum all rejected with reasons", bsize=12.5, accent=NAVY)
NOTES.append("Deliverable one: the proposal. The problem statement in three lines, six SMART objectives, an "
             "explicit in-scope and out-of-scope list, and the process model with its justification. The out-of-scope "
             "list is the part I would point out - it is what kept the project on schedule.")

# ============================================================ 3 requirements
s = slide()
header(s, "DELIVERABLE 2 \u00b7 WEEK 2", "Software Requirements Specification", "8")
text(s, 0.55, 1.72, 6, 0.32, "14 functional requirements (FR-1 to FR-14)", size=15.5, bold=True, color=EMERALD)
fr_left = [
    "FR-1  Report lost or found item, with photo",
    "FR-2  Validate names, emails, phones, matric IDs",
    "FR-3  Search and filter without signing in",
    "FR-4  Warn about similar existing reports",
    "FR-5  Claim a found item; reporter confirms/rejects",
    "FR-6  Rejected claimants permanently barred",
    "FR-7  Finder responses on lost items",
]
fr_right = [
    "FR-8   Private 1-to-1 chat, outsiders get 403",
    "FR-9   Disputes, upheld or dismissed",
    "FR-10 Edit / delete / mark-found / close own report",
    "FR-11 Accounts with salted, hashed passwords",
    "FR-12 Anti-spam limits",
    "FR-13 Contact details visible only to participants",
    "FR-14 Persistence across restarts",
]
bullets(s, 0.55, 2.12, 6.1, 3.2, fr_left, size=13.5, gap=6)
bullets(s, 6.75, 2.12, 6.1, 3.2, fr_right, size=13.5, gap=6)
box(s, 0.55, 5.5, 12.25, 1.4, fill=LIGHT)
box(s, 0.55, 5.5, 0.08, 1.4, fill=EMERALD)
text(s, 0.85, 5.6, 11.6, 0.32, "8 non-functional requirements", size=15, bold=True, color=EMERALD)
text(s, 0.85, 5.98, 11.6, 0.85,
     "NFR-1 usability (\u2264 2 min, 360 px)  \u00b7  NFR-2 performance (\u2264 1 s over 1,000 items)  \u00b7  "
     "NFR-3 security (hashed passwords, 5 MB image cap)  \u00b7  NFR-4 reliability (disk on every mutation)  \u00b7  "
     "NFR-5 availability (PWA offline shell)  \u00b7  NFR-6 maintainability (28 tests, 84 %)  \u00b7  "
     "NFR-7 portability  \u00b7  NFR-8 privacy",
     size=12.5, color=NAVY)
NOTES.append("The requirements specification. Fourteen functional requirements, numbered so week ten could trace "
             "each one to a test, and eight non-functional requirements with measurable targets. FR-13, the contact "
             "gating requirement, is the one that shaped the entire security design.")

# ============================================================ 4 user stories
s = slide()
header(s, "DELIVERABLE 2 \u00b7 WEEK 2", "User stories with acceptance criteria", "8")
stories = [
    ("US-4 \u2014 Claim a found item",
     "\u201cAs the owner of a found ID card, I want to claim it with proof so the finder can verify me.\u201d",
     "AC1 proof required  \u00b7  AC2 reporter confirms or rejects  \u00b7  AC3 after rejection I cannot claim that item again"),
    ("US-5 \u2014 Respond to a lost report",
     "\u201cAs a finder, I want to click \u2018I Found This Item\u2019 and leave my contact \u2014 without an ownership quiz.\u201d",
     "AC1 short form  \u00b7  AC2 owner sees \u201cN finder responses\u201d  \u00b7  AC3 no duplicate responses per email"),
    ("US-6 \u2014 Chat to arrange the return",
     "\u201cAs the owner, I want to chat privately with one finder at a time so messages never reach the wrong person.\u201d",
     "AC1 one thread per pair  \u00b7  AC2 outsiders receive 403  \u00b7  AC3 unread dots clear after reading"),
]
for i, (t, story, ac) in enumerate(stories):
    y = 1.8 + i * 1.65
    box(s, 0.55, y, 12.25, 1.48, fill=LIGHT)
    box(s, 0.55, y, 0.08, 1.48, fill=EMERALD)
    text(s, 0.85, y + 0.08, 11.6, 0.35, t, size=15, bold=True, color=EMERALD)
    text(s, 0.85, y + 0.45, 11.6, 0.5, story, size=13.5, color=NAVY)
    text(s, 0.85, y + 1.0, 11.6, 0.35, ac, size=12, color=GREY)
box(s, 0.55, 6.85, 12.25, 0.45, fill=NAVY)
text(s, 0.85, 6.94, 11.6, 0.3,
     "8 stories in total \u2014 every acceptance criterion became an automated test in week 10",
     size=12, color=WHITE)
NOTES.append("Three of the eight user stories with their acceptance criteria. I want to stress the last line: each "
             "acceptance criterion became a test in week ten. That is the traceability from requirement to story to "
             "acceptance criterion to test case.")

# ============================================================ 5 planning
s = slide()
header(s, "DELIVERABLE 3 \u00b7 WEEK 3", "Prioritisation and effort estimates", "6")
text(s, 0.55, 1.72, 6, 0.32, "MoSCoW", size=15.5, bold=True, color=EMERALD)
table(s, 0.55, 2.12, 6.1,
      [["Priority", "Requirements"],
       ["Must", "FR-1, 2, 3, 5, 10, 11, 14"],
       ["Should", "FR-6, 7, 8, 9, 12, 13"],
       ["Could", "FR-4, unread dots, PWA, photo edit"],
       ["Won't (v1.0)", "Notifications, admin dashboard, payments"]],
      widths=[1.3, 4.3], size=12.5, row_h=0.55)
text(s, 0.55, 4.85, 6, 0.32, "Estimates vs actuals", size=15.5, bold=True, color=EMERALD)
table(s, 0.55, 5.25, 6.1,
      [["Item", "Est.", "Actual"],
       ["Reporting + validation", "6 h", "7 h"],
       ["Finder responses + chat", "8 h", "10 h"],
       ["Test suite + hardening", "6 h", "7 h"],
       ["Total", "50 h", "54 h (+8 %)"]],
      widths=[3.4, 1.1, 1.6], size=12, row_h=0.4)
text(s, 7.0, 1.72, 6, 0.32, "13-week plan (baselined in week 3)", size=15.5, bold=True, color=EMERALD)
plan = [
    ("W1\u20132", "Proposal, requirements"),
    ("W3", "Plan, risks"),
    ("W4\u20136", "Models, architecture, design"),
    ("W7\u20139", "Modules 1 & 2, demo"),
    ("W10\u201311", "Testing, security, deploy"),
    ("W12\u201313", "Docs, final report"),
]
for i, (wk, what) in enumerate(plan):
    y = 2.15 + i * 0.62
    box(s, 7.0, y, 0.95, 0.5, fill=EMERALD)
    text(s, 7.0, y + 0.1, 0.95, 0.3, wk, size=11.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    text(s, 8.1, y + 0.08, 4.7, 0.4, what, size=13, color=NAVY)
card(s, 7.0, 5.9, 5.8, 1.0, "Variance explained",
     "Two overruns (validation, chat threads) offset by faster UI work", bsize=12, accent=AMBER)
NOTES.append("Deliverable three, planning. MoSCoW on the left, the 13-week baseline in the middle, and estimates "
             "against actuals at the bottom left. I estimated fifty hours and spent fifty-four - eight percent over, "
             "and I can tell you exactly which two features caused it.")

# ============================================================ 6 risks
s = slide()
header(s, "DELIVERABLE 3 \u00b7 WEEK 3", "Risk register (scored P \u00d7 I)", "6")
table(s, 0.55, 1.8, 12.25,
      [["ID", "Risk", "P", "I", "Score", "Mitigation"],
       ["R1", "Scope creep", "H", "H", "9", "MoSCoW + binding won't-have list"],
       ["R2", "Data loss (file store)", "M", "H", "6", "save_state on every mutation"],
       ["R3", "Identity spoofing (email auth)", "H", "M", "6", "Accepted, analysed in STRIDE; tokens = v1.1"],
       ["R4", "Stale UI (service worker)", "H", "M", "6", "Network-first + cache version bump"],
       ["R6", "Upload abuse", "M", "H", "6", "Whitelist, 5 MB cap, UUID names"],
       ["R7", "Single-developer absence", "M", "H", "6", "Weekly increments keep it runnable"]],
      widths=[0.6, 3.3, 0.5, 0.5, 0.8, 6.55], size=12.5, row_h=0.55)
box(s, 0.55, 5.85, 12.25, 1.15, fill=LIGHT)
box(s, 0.55, 5.85, 0.08, 1.15, fill=AMBER)
text(s, 0.85, 5.95, 11.6, 0.95,
     "Two of these materialised during the project: R1 (scope creep knocked twice and the won't-have list held) "
     "and R4 (the stale-UI problem cost several days). A risk register you actually respond to is not decoration.",
     size=13.5, color=NAVY)
NOTES.append("The risk register, scored probability times impact. Six risks scored six or above and each got an "
             "active mitigation rather than a note. Two of them actually happened - scope creep and the stale "
             "service-worker problem - and because they were written down, both had a prepared response.")

# ============================================================ 7 UML
s = slide()
header(s, "DELIVERABLE 4 \u00b7 WEEK 4", "UML models", "8")
text(s, 0.55, 1.72, 6, 0.32, "Use case diagram \u2014 4 actors, 13 use cases", size=15, bold=True, color=EMERALD)
bullets(s, 0.55, 2.1, 6.1, 1.9, [
    "Student \u2014 report lost, search, claim",
    "Finder \u2014 report found, search, respond",
    "Reporter \u2014 chat, confirm/reject, disputes, edit",
    "Third party \u2014 search, file a dispute",
], size=13.5, gap=6)
text(s, 0.55, 4.1, 6, 0.32, "Two sequence diagrams", size=15, bold=True, color=EMERALD)
bullets(s, 0.55, 4.48, 6.1, 1.6, [
    "Claim flow: report \u2192 claim + proof \u2192 chat \u2192 confirm",
    "Finder flow: respond \u2192 owner views \u2192 chat \u2192 credit",
], size=13.5, gap=6)
text(s, 7.0, 1.72, 6, 0.32, "Class model \u2014 status lifecycle", size=15, bold=True, color=EMERALD)
states = [("Active", EMERALD), ("Claim Requested", AMBER), ("Claimed/Returned", NAVY), ("Closed", GREY)]
for i, (st, c) in enumerate(states):
    box(s, 7.0 + (i % 2) * 2.95, 2.15 + (i // 2) * 0.95, 2.75, 0.68, fill=c)
    text(s, 7.0 + (i % 2) * 2.95, 2.32 + (i // 2) * 0.95, 2.75, 0.4, st, size=12.5, color=WHITE,
         bold=True, align=PP_ALIGN.CENTER)
card(s, 7.0, 4.15, 5.8, 1.35, "Domain entities",
     "Item \u00b7 ClaimDetails (0..1) \u00b7 FoundReport (0..*) \u00b7 Dispute (0..*) \u00b7 Conversation/Message \u00b7 User",
     bsize=12)
card(s, 7.0, 5.65, 5.8, 1.05, "Activity diagrams (2)",
     "Report submission with validation \u00b7 claim resolution with disputes", bsize=12)
NOTES.append("Deliverable four: the UML models. Use case diagram with four actors and thirteen use cases, two "
             "sequence diagrams because the system has two mirrored flows, two activity diagrams, and the class "
             "model whose heart is the status lifecycle.")

# ============================================================ 8 architecture + ERD
s = slide()
header(s, "DELIVERABLES 5 \u00b7 WEEKS 5", "Architecture and database design", "8")
text(s, 0.55, 1.72, 6, 0.32, "Layered monolith \u2014 3 alternatives rejected", size=15, bold=True, color=EMERALD)
layers = [("Presentation", "PWA: index.html, app.js, service worker", EMERALD),
          ("API", "22 REST routes, validation, permissions", NAVY),
          ("Domain", "Status lifecycle, spam limits, threads", NAVY),
          ("Persistence", "save_state / load_state \u2192 db.json", GREY)]
for i, (name, what, c) in enumerate(layers):
    y = 2.15 + i * 0.78
    box(s, 0.55, y, 1.85, 0.62, fill=c)
    text(s, 0.55, y + 0.17, 1.85, 0.3, name, size=11.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    text(s, 2.55, y + 0.15, 4.1, 0.4, what, size=12, color=NAVY)
card(s, 0.55, 5.35, 6.1, 1.35, "Why not microservices / serverless?",
     "One developer, 13 weeks, offline demo. Complexity without benefit.", bsize=12, accent=AMBER)
text(s, 7.0, 1.72, 6, 0.32, "ERD \u2014 7 tables in the SQL schema", size=15, bold=True, color=EMERALD)
table(s, 7.0, 2.12, 5.8,
      [["Table", "Key relationship"],
       ["users", "email unique \u00b7 salt + hash"],
       ["items", "reporter email \u00b7 status enum"],
       ["claim_details", "1 : 0..1 with items"],
       ["rejected_claimants", "composite PK (item, email)"],
       ["found_reports", "unique (item, finder email)"],
       ["disputes", "status upheld / dismissed"],
       ["messages", "thread_key = itemId:partner"]],
      widths=[2.0, 3.8], size=12, row_h=0.42, head_h=0.42)
text(s, 7.0, 5.75, 5.8, 0.9,
     "Designed relationally on purpose \u2014 the PostgreSQL migration is a transcription of the ERD, "
     "with CHECK constraints and cascade deletes already written.",
     size=12, color=GREY)
NOTES.append("Deliverable five: architecture and database. Four layers, and three rejected alternatives with "
             "reasons. On the right, the ERD - seven tables, written as a real PostgreSQL schema with check "
             "constraints, unique constraints and cascade deletes, so the migration path exists.")

# ============================================================ 9 design
s = slide()
header(s, "DELIVERABLE 6 \u00b7 WEEK 6", "Design patterns, SOLID module and wireframes", "6")
pats = [
    ("Repository", "save_state / load_state \u2014 storage swap is one layer"),
    ("Strategy", "public_item() selects fields by viewer relationship"),
    ("Facade", "front end touches domain only through REST"),
    ("Observer", "unread indicators via 15-second polling"),
]
for i, (t, b) in enumerate(pats):
    x = 0.55 + (i % 2) * 6.25
    y = 1.8 + (i // 2) * 1.05
    card(s, x, y, 5.95, 0.92, t, b, tsize=14.5, bsize=12)
box(s, 0.55, 4.05, 12.25, 1.5, fill=LIGHT)
box(s, 0.55, 4.05, 0.08, 1.5, fill=EMERALD)
text(s, 0.85, 4.15, 11.6, 0.32, "SOLID-compliant module: public_item(item, viewer_email)",
     size=15, bold=True, color=EMERALD)
text(s, 0.85, 4.52, 11.6, 0.95,
     "Single responsibility (projects fields per viewer) \u00b7 Open/closed (new viewer roles extend the flags) \u00b7 "
     "Liskov (always a valid projection) \u00b7 Interface segregation (5 flags, not the raw record) \u00b7 "
     "Dependency inversion (routes ignore storage layout). Proven by test_public_api_strips_private_fields.",
     size=12.5, color=NAVY)
text(s, 0.55, 5.7, 6, 0.32, "6 wireframes produced", size=15, bold=True, color=EMERALD)
bullets(s, 0.55, 6.08, 12.2, 1.0, [
    "Browse desktop + mobile (360 px) \u00b7 report form with duplicate warning \u00b7 claim modal \u00b7 "
    "finder-response panel \u00b7 chat with unread indicator",
], size=12.5, gap=5)
NOTES.append("Deliverable six: design. Four patterns - Repository, Strategy, Facade, Observer - and one module "
             "held up as SOLID-compliant with each principle justified against it. Six wireframes were produced, "
             "including the mobile layout at 360 pixels.")

# ============================================================ 10 implementation
s = slide()
header(s, "DELIVERABLES 7\u20139 \u00b7 WEEKS 7\u20139", "Implementation, standards and review", "22")
text(s, 0.55, 1.72, 6, 0.32, "Coding standard (9 rules)", size=15, bold=True, color=EMERALD)
bullets(s, 0.55, 2.1, 6.05, 2.6, [
    "PEP 8 naming; models in PascalCase",
    "Every endpoint docstring states its permission rule",
    "All input through the validation gate",
    "Permissions enforced server-side, 403 with reason",
    "Every mutation ends with save_state()",
    "Regex constants named in CAPS at module top",
], size=12.5, gap=5)
text(s, 0.55, 4.75, 6, 0.32, "Module 1 (week 7) \u2192 Modules 2\u20136 (week 9)", size=15, bold=True, color=EMERALD)
bullets(s, 0.55, 5.13, 6.05, 1.7, [
    "M1: report + validation + browse + search + duplicate warning",
    "M2\u20136: finder responses, chat, disputes, moderation, accounts, PWA",
], size=12.5, gap=5)
text(s, 7.0, 1.72, 6, 0.32, "Code review log \u2014 10 findings", size=15, bold=True, color=EMERALD)
table(s, 7.0, 2.1, 5.8,
      [["#", "Finding", "Sev."],
       ["R1", "confirm-return unauthenticated", "High"],
       ["R2", "API leaked contact details", "High"],
       ["R3", "upload path traversal", "High"],
       ["R5", "one thread shared by all finders", "High"],
       ["R8", "SHA-256 is not a KDF", "Med."],
       ["R10", "dead ItemCreate model", "Low"]],
      widths=[0.55, 4.2, 1.05], size=11.5, row_h=0.42, head_h=0.4)
box(s, 7.0, 5.5, 5.8, 1.15, fill=LIGHT)
box(s, 7.0, 5.5, 0.08, 1.15, fill=EMERALD)
text(s, 7.28, 5.6, 5.4, 0.95,
     "Static analysis: pyflakes + node --check clean after cleanup. Max complexity \u2248 5 (guideline \u2264 10).",
     size=12, color=NAVY)
NOTES.append("Deliverables seven to nine: implementation, standards and quality. Nine coding rules with the three "
             "that mattered most, then the code review log - ten findings, four of them high severity, all fixed. "
             "Static analysis came back clean and the highest complexity in the codebase is about five.")

# ============================================================ 11 testing
s = slide()
header(s, "DELIVERABLE 10 \u00b7 WEEK 10", "Test plan and results", "8")
text(s, 0.55, 1.7, 12, 0.32,
     "28 tests \u00b7 84 % line coverage (gate 80 %) \u00b7 10 defects found \u00b7 0 open",
     size=17, bold=True, color=EMERALD)
table(s, 0.55, 2.12, 12.25,
      [["ID", "Test", "Verifies", "Result"],
       ["T-03", "claim_then_confirm_return", "FR-5 lifecycle; confirm is reporter-only", "Pass"],
       ["T-05", "reject_claim_returns_to_active", "FR-5/6 reject \u2192 Active; rejected \u2192 403", "Pass"],
       ["T-09", "input_validation_rejects_nonsense", "FR-2 bad phone/matric/email \u2192 400", "Pass"],
       ["T-10", "lost_report_rate_limit", "FR-12 3 active reports, 4th \u2192 429", "Pass"],
       ["T-16", "finder_response_flow", "FR-7 self/duplicate/stranger guards + isolated threads", "Pass"],
       ["T-18", "public_api_strips_private_fields", "FR-13 anonymous sees no contact fields", "Pass"],
       ["T-20", "upload_validation", "NFR-3 non-image \u2192 400; traversal neutralised", "Pass"]],
      widths=[0.75, 3.3, 6.2, 0.85], size=12, row_h=0.44, head_h=0.44)
box(s, 0.55, 5.95, 12.25, 1.05, fill=NAVY)
text(s, 0.85, 6.08, 11.6, 0.85,
     "9 of the 28 tests assert that the WRONG user receives 403. Without them the permission matrix is a claim; "
     "with them, it is evidence.",
     size=14, color=WHITE)
NOTES.append("Deliverable ten: testing. Twenty-eight tests, eighty-four percent coverage against an eighty percent "
             "gate, ten defects found and zero open. Seven representative cases shown - and the line at the bottom "
             "is the one I want remembered: nine tests assert that the wrong user gets a 403.")

# ============================================================ 12 defects
s = slide()
header(s, "DELIVERABLE 10 \u00b7 WEEK 10", "Defect log", "8")
table(s, 0.55, 1.8, 12.25,
      [["ID", "Defect", "Sev.", "Root cause", "Status"],
       ["D-01", "Message to one finder reached all finders", "High", "Thread keyed by item only", "Closed"],
       ["D-03", "confirm-return had no permission check", "High", "Endpoint written before permission pass", "Closed"],
       ["D-04", "API leaked contact/claim data", "High", "Raw dicts returned to client", "Closed"],
       ["D-05", "Upload path traversal", "High", "Client filename used raw", "Closed"],
       ["D-06", "Item grid blank after sanitizer change", "High", "Render assumed fields always present", "Closed"],
       ["D-08", "Rate limit blocked the demo reporter", "Med.", "Seeds counted toward the portal limit", "Closed"]],
      widths=[0.65, 4.5, 0.75, 4.6, 0.95], size=12, row_h=0.55)
box(s, 0.55, 5.85, 12.25, 1.15, fill=LIGHT)
box(s, 0.55, 5.85, 0.08, 1.15, fill=AMBER)
text(s, 0.85, 5.95, 11.6, 0.95,
     "Read the root-cause column vertically: D-01, D-02, D-06 and D-07 are one species \u2014 the client assumed "
     "something about the server payload that was not true. The fix class was always: server decides, client renders.",
     size=13, color=NAVY)
NOTES.append("The defect log. Six of the ten entries, with root causes. The insight I would highlight is the bottom "
             "box: four of these bugs were the same species - a client assumption about the server payload. That "
             "observation is what my final reflection is built on, and how I now write render code.")

# ============================================================ 13 security
s = slide()
header(s, "DELIVERABLE 11 \u00b7 WEEK 11", "Threat model and fixes", "8")
table(s, 0.55, 1.78, 12.25,
      [["Threat", "Scenario", "Control"],
       ["Spoofing", "Submit a victim's email to delete/reject", "Owner email verified per endpoint"],
       ["Tampering", "../../evil.html upload", "UUID names, extension whitelist, 5 MB cap"],
       ["Info disclosure", "Scrape contacts from the API", "public_item() strips per viewer"],
       ["Info disclosure", "Outsider reads a private chat", "Thread resolution + 403"],
       ["DoS", "Spam reports, disputes, messages", "3 / 20 / 20 / 200 limits"],
       ["Elevation", "Crafted file executed server-side", "Static serving, validated uploads"]],
      widths=[2.2, 4.6, 5.4], size=12, row_h=0.52)
box(s, 0.55, 5.5, 6.0, 1.4, fill=LIGHT)
box(s, 0.55, 5.5, 0.08, 1.4, fill=AMBER)
text(s, 0.83, 5.6, 5.5, 0.32, "Accepted for v1.0 (stated openly)", size=13.5, bold=True, color=AMBER)
text(s, 0.83, 5.95, 5.5, 0.9,
     "Email-string identity (no session tokens) and salted SHA-256 rather than a KDF. Both analysed in STRIDE; "
     "token auth is the first v1.1 item.", size=11.5, color=NAVY)
box(s, 6.75, 5.5, 6.05, 1.4, fill=LIGHT)
box(s, 6.75, 5.5, 0.08, 1.4, fill=EMERALD)
text(s, 7.03, 5.6, 5.5, 0.32, "OWASP Top 10 + CI", size=13.5, bold=True, color=EMERALD)
text(s, 7.03, 5.95, 5.5, 0.9,
     "A01, A03, A04, A05, A08 addressed; A02 and A07 marked partial honestly. GitHub Actions runs tests "
     "with an 80 % coverage gate on every push.", size=11.5, color=NAVY)
NOTES.append("Deliverable eleven: security. Six of the twelve STRIDE threats with the control that addresses each. "
             "The two boxes at the bottom matter: what I fixed, and what I accepted and documented rather than hid. "
             "Examiners reward the second box more than the first.")

# ============================================================ 14 maintenance
s = slide()
header(s, "DELIVERABLE 12 \u00b7 WEEK 12", "Change request, manual and metrics", "6")
text(s, 0.55, 1.72, 6, 0.32, "CR-001 \u2014 processed with impact analysis", size=15, bold=True, color=EMERALD)
table(s, 0.55, 2.1, 6.1,
      [["Field", "Detail"],
       ["Request", "\u201cNotify me when someone responds\u201d"],
       ["Impact", "SMTP dependency, new attack surface, 6\u20138 h"],
       ["Timing", "Would land on testing + security weeks"],
       ["Alternative", "In-app unread dots already shipped"],
       ["Decision", "Partially approved \u2014 deferred to v1.1"]],
      widths=[1.5, 4.6], size=12, row_h=0.5)
text(s, 7.0, 1.72, 6, 0.32, "User manual \u2014 8 sections", size=15, bold=True, color=EMERALD)
bullets(s, 7.0, 2.1, 5.85, 2.3, [
    "Install on a phone (Add to Home screen)",
    "Report a lost item / a found item",
    "Recover an item via finder responses + chat",
    "Claim a found item; dispute a claim",
    "Edit, mark as found, close, delete",
], size=12.5, gap=6)
text(s, 7.0, 4.55, 6, 0.32, "Metrics reported", size=15, bold=True, color=EMERALD)
table(s, 7.0, 4.93, 5.85,
      [["Metric", "Value"],
       ["Endpoints / tests / coverage", "22 / 28 / 84 %"],
       ["Defects found / open", "10 / 0"],
       ["Effort", "54 h vs 50 h (+8 %)"],
       ["Requirements delivered", "14 FR + 8 NFR"]],
      widths=[3.5, 2.35], size=11.5, row_h=0.42)
NOTES.append("Deliverable twelve: maintenance. The change request was processed properly - impact analysis, a "
             "decision, and a note of what was shipped instead. Then the eight-section user manual and the metrics "
             "table with effort variance and defect closure.")

# ============================================================ 15 final
s = slide()
header(s, "DELIVERABLE 13 \u00b7 WEEK 13", "Final report, limitations and reflection", "16")
text(s, 0.55, 1.7, 6, 0.32, "What ships", size=15, bold=True, color=EMERALD)
bullets(s, 0.55, 2.08, 6.05, 2.5, [
    "Full lifecycle: report \u2192 search \u2192 claim \u2192 chat \u2192 confirm",
    "Finder responses, disputes, moderation, accounts",
    "Server-enforced permissions and privacy projection",
    "28 tests, 84 % coverage, CI, live deployment",
], size=12.5, gap=6)
text(s, 0.55, 4.7, 6, 0.32, "Known limitations (stated plainly)", size=15, bold=True, color=AMBER)
bullets(s, 0.55, 5.08, 6.05, 1.8, [
    "Email-string identity, no session tokens",
    "SHA-256, not a KDF; no login rate limiting",
    "No write locking on db.json; ephemeral cloud disk",
    "Notifications not implemented (CR-001)",
], size=12.5, gap=6)
text(s, 7.0, 1.7, 6, 0.32, "Reflection \u2014 four lessons", size=15, bold=True, color=EMERALD)
lessons = [
    ("Server decides, client renders", "4 bugs, 1 species"),
    ("Measure caching early", "Service worker cost days"),
    ("Test from every role's view", "Correct but unusable"),
    ("Privacy is a server concern", "UI hiding is not security"),
]
for i, (t, b) in enumerate(lessons):
    y = 2.08 + i * 0.72
    box(s, 7.0, y, 5.85, 0.6, fill=LIGHT)
    box(s, 7.0, y, 0.08, 0.6, fill=EMERALD)
    text(s, 7.28, y + 0.06, 3.5, 0.35, t, size=12.5, bold=True, color=NAVY)
    text(s, 10.85, y + 0.12, 1.9, 0.35, b, size=10.5, color=GREY)
card(s, 7.0, 5.08, 5.85, 1.8, "Future work (v1.1)",
     "Session tokens \u2192 PBKDF2 \u2192 PostgreSQL (schema ready) \u2192 SMTP notifications \u2192 "
     "admin dashboard \u2192 upload content sniffing \u2192 audit logging", bsize=12)
NOTES.append("Deliverable thirteen: the final report. What ships, then - deliberately first - the known "
             "limitations, then four reflection lessons, then future work in priority order. Ending on limitations "
             "rather than achievements is a choice, and it is the one I would defend.")

# ============================================================ 16 close
s = slide()
box(s, 0, 0, 13.333, 7.5, fill=NAVY)
box(s, 0, 3.5, 13.333, 0.07, fill=EMERALD)
text(s, 1.2, 2.2, 11, 1.1, "Thank you", size=52, bold=True, color=WHITE)
text(s, 1.2, 3.7, 11, 0.6, "Questions?", size=26, color=RGBColor(0x9C, 0xA3, 0xAF))
text(s, 1.2, 4.9, 11, 0.6, "13 deliverables \u00b7 100 marks \u00b7 deployed and running today",
     size=18, bold=True, color=EMERALD)
text(s, 1.2, 5.75, 11, 1.0, [
    "Mathew Umama  \u00b7  U23CS1067  \u00b7  Computer Science  \u00b7  CSC 403",
    "afit-lost-and-found.onrender.com",
], size=16, color=WHITE, space_after=6)
NOTES.append("Close. Thirteen deliverables, one hundred marks, and the system is deployed and running - I can "
             "demonstrate it live. Thank you.")

for sl, note in zip(prs.slides, NOTES):
    sl.notes_slide.notes_text_frame.text = note

OUT = "AFIT_SP014_Deliverables_Slides.pptx"
try:
    prs.save(OUT)
except PermissionError:
    OUT = "AFIT_SP014_Deliverables_Slides_v2.pptx"
    prs.save(OUT)
print(f"Saved {OUT} with {len(prs.slides._sldIdLst)} slides and speaker notes")
