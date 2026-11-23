"""Builds the SP-014 theory presentation: AFIT Lost & Found Portal (short version)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
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


def text(s, x, y, w, h, runs, size=22, color=NAVY, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, space_after=8, line_spacing=1.0):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    if isinstance(runs, str):
        runs = [runs]
    for i, para in enumerate(runs):
        opts = {}
        if isinstance(para, tuple):
            para, opts = para
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = opts.get("align", align)
        p.space_after = Pt(opts.get("space_after", space_after))
        p.line_spacing = opts.get("line_spacing", line_spacing)
        r = p.add_run()
        r.text = para
        f = r.font
        f.size = Pt(opts.get("size", size))
        f.bold = opts.get("bold", bold)
        f.color.rgb = opts.get("color", color)
        f.name = "Calibri"
    return tb


def header(s, kicker, title):
    box(s, 0, 0, 13.333, 0.18, fill=EMERALD)
    text(s, 0.55, 0.35, 12.3, 0.4, kicker, size=17, color=EMERALD, bold=True)
    text(s, 0.55, 0.72, 12.3, 0.95, title, size=38, color=NAVY, bold=True)


def bullets(s, x, y, w, h, items, size=20, gap=10):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, it in enumerate(items):
        lvl = 0
        if isinstance(it, tuple):
            it, lvl = it
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = lvl
        p.space_after = Pt(gap)
        marker = "" if lvl else "\u2022  "
        r = p.add_run()
        r.text = marker + it
        r.font.size = Pt(size if not lvl else size - 2)
        r.font.color.rgb = NAVY if not lvl else GREY
        r.font.name = "Calibri"
    return tb


def card(s, x, y, w, h, title, body, tsize=20, bsize=16, accent=EMERALD):
    box(s, x, y, w, h, fill=LIGHT)
    box(s, x, y, 0.08, h, fill=accent)
    text(s, x + 0.28, y + 0.14, w - 0.45, 0.5, title, size=tsize, bold=True, color=NAVY)
    text(s, x + 0.28, y + 0.62, w - 0.45, h - 0.75, body, size=bsize, color=GREY, space_after=4)


def footer(s, num):
    text(s, 0.55, 7.1, 6, 0.3, "AFIT Lost & Found Portal — SP-014", size=12, color=GREY)
    text(s, 12.3, 7.1, 0.6, 0.3, str(num), size=12, color=GREY, align=PP_ALIGN.RIGHT)


n = 0

# ================================================================ 1 TITLE
s = slide()
box(s, 0, 0, 13.333, 7.5, fill=NAVY)
box(s, 0, 3.55, 13.333, 0.07, fill=EMERALD)
text(s, 1.2, 1.6, 11, 0.5, "SP-014  ·  SOFTWARE ENGINEERING COURSE PROJECT", size=20, color=EMERALD, bold=True)
text(s, 1.2, 2.15, 11, 1.4, "AFIT Lost & Found Portal", size=60, color=WHITE, bold=True)
text(s, 1.2, 3.8, 11, 0.6, "Report it. Search it. Recover it.", size=28, color=RGBColor(0x9C, 0xA3, 0xAF))
text(s, 1.2, 5.1, 11, 1.7, [
    "Mathew Umama  ·  U23CS1067",
    "CSC 403  ·  Computer Science",
    "Final presentation — single-person project",
], size=21, color=WHITE, space_after=6)

# ================================================================ 2 PROBLEM
n += 1
s = slide()
header(s, "MOTIVATION", "The problem I set out to solve")
text(s, 0.55, 1.9, 12.2, 1.0,
     "Every semester, phones, ID cards, laptops and textbooks go missing on campus — and the "
     "only recovery channels we have are informal ones.",
     size=24, color=NAVY)
cards = [
    ("Notice boards", "Nobody checks them — and last week's poster looks the same as today's."),
    ("WhatsApp groups", "Messages get buried within two days. No search across months of history."),
    ("Paper logs at security", "Students cannot search them. The record exists, but only for the officer holding the book."),
    ("The result", "Recovered items pile up unclaimed — the finder and the owner never meet."),
]
for i, (t, b) in enumerate(cards):
    x = 0.55 + (i % 2) * 6.25
    y = 3.1 + (i // 2) * 1.85
    card(s, x, y, 5.95, 1.6, t, b, tsize=21, bsize=17, accent=EMERALD if i < 3 else AMBER)
footer(s, n)

# ================================================================ 3 OBJECTIVES & SCOPE
n += 1
s = slide()
header(s, "WEEK 1 — PROPOSAL", "Objectives and scope")
text(s, 0.55, 1.95, 6, 0.5, "Six SMART objectives", size=23, bold=True, color=EMERALD)
bullets(s, 0.55, 2.55, 6.1, 4.2, [
    "Report a lost or found item in under 2 minutes",
    "Search and filter by type, category, location, keyword",
    "Verified claim-and-return workflow for found items",
    "Lightweight \u201cI found this\u201d flow for lost items, with private chat",
    "An auditable trail of claims, disputes and resolutions",
    "Ship it all as an installable, mobile-friendly PWA",
], size=19, gap=12)
text(s, 7.0, 1.95, 6, 0.5, "Scope discipline", size=23, bold=True, color=EMERALD)
card(s, 7.0, 2.55, 5.8, 2.0, "In scope (v1.0)",
     "Reporting with photos · search · claims · finder responses · private chat · disputes · "
     "moderation · accounts · validation · anti-spam · PWA · persistence", tsize=20, bsize=16)
card(s, 7.0, 4.75, 5.8, 2.0, "Deliberately out of scope",
     "Email/SMS servers · payments · student-records integration · native apps · multi-campus · "
     "image recognition. Written down in week 1 so I could say no later.", tsize=20, bsize=16, accent=AMBER)
footer(s, n)

# ================================================================ 4 PROCESS MODEL
n += 1
s = slide()
header(s, "WEEK 1 — PROCESS MODEL", "Why I chose the incremental model")
stages = ["Proposal", "Requirements", "Planning", "UML", "Architecture", "Module 1",
          "Demo", "Full system", "Testing", "Security", "Docs", "Final"]
x0, w_each = 0.55, 1.02
for i, st in enumerate(stages):
    box(s, x0 + i * (w_each + 0.03), 2.2, w_each, 0.9, fill=EMERALD if i < 8 else NAVY)
    text(s, x0 + i * (w_each + 0.03), 2.4, w_each, 0.6, st, size=13, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER)
text(s, 0.55, 3.3, 12.2, 0.5,
     "Each week delivers a usable increment — the system was runnable at the end of every week.",
     size=19, color=GREY)
rejected = [
    ("Waterfall", "Feedback would only arrive at the end — too late to act on."),
    ("Pure prototyping", "Throwaway prototypes waste effort when the core flows are clear."),
    ("Scrum", "Strongest rival, but the course is weekly deliverables, not sprints."),
]
for i, (t, b) in enumerate(rejected):
    card(s, 0.55, 4.0 + i * 1.05, 12.25, 0.9, t, b, tsize=18, bsize=16, accent=AMBER)
footer(s, n)

# ================================================================ 5 REQUIREMENTS
n += 1
s = slide()
header(s, "WEEKS 2–3 — REQUIREMENTS", "Stakeholders, 14 requirements, MoSCoW")
text(s, 0.55, 1.9, 6, 0.5, "Who I built it for", size=22, bold=True, color=EMERALD)
bullets(s, 0.55, 2.5, 6.0, 1.9, [
    "Students who lost items — get property back, fast",
    "Finders — an official way to hand things in",
    "Security / wardens — a digital handover log",
    "Student affairs — dispute oversight",
], size=18, gap=7)
text(s, 0.55, 4.55, 6, 0.5, "How I found the requirements", size=22, bold=True, color=EMERALD)
bullets(s, 0.55, 5.15, 6.0, 1.8, [
    "Interviewed classmates — \u201cpost in the group and pray\u201d",
    "Observed the security post's paper log",
    "Studied other universities' portals",
], size=18, gap=7)
moscow = [
    ("Must have", "Reporting · validation · search · claims · moderation · accounts · persistence", EMERALD),
    ("Should have", "Rejected-claimant ban · finder responses · private chat · disputes · contact gating", NAVY),
    ("Could have", "Duplicate warning · unread dots · PWA offline shell", GREY),
    ("Won't have (v1.0)", "Email/SMS · admin dashboard · payments · multi-campus", AMBER),
]
text(s, 7.0, 1.9, 6, 0.5, "MoSCoW prioritisation", size=22, bold=True, color=EMERALD)
for i, (t, b, c) in enumerate(moscow):
    y = 2.5 + i * 1.12
    box(s, 7.0, y, 5.8, 1.0, fill=LIGHT)
    box(s, 7.0, y, 0.08, 1.0, fill=c)
    text(s, 7.3, y + 0.08, 5.3, 0.4, t, size=18, bold=True, color=c)
    text(s, 7.3, y + 0.5, 5.3, 0.5, b, size=14.5, color=NAVY)
footer(s, n)

# ================================================================ 6 UML
n += 1
s = slide()
header(s, "WEEK 4 — UML", "Use cases, domain model, sequence")
text(s, 0.55, 1.9, 6, 0.5, "Actors and their use cases", size=22, bold=True, color=EMERALD)
bullets(s, 0.55, 2.5, 6.0, 2.3, [
    "Student — report lost · search · claim",
    "Finder — report found · search · \u201cI found this\u201d",
    "Reporter — chat · confirm/reject · resolve disputes · edit/close",
    "Third party — search · file a dispute",
], size=18, gap=8)
text(s, 0.55, 5.0, 6, 0.5, "Main flow (sequence diagram)", size=22, bold=True, color=EMERALD)
bullets(s, 0.55, 5.6, 6.0, 1.5, [
    "Report found item \u2192 claim with proof \u2192 Claim Requested",
    "Private chat \u2192 reporter confirms the return",
    "Reject path: back to Active, claimant banned",
], size=18, gap=8)
text(s, 7.0, 1.9, 6, 0.5, "Item status lifecycle", size=22, bold=True, color=EMERALD)
states = [("Active", EMERALD), ("Claim Requested", AMBER), ("Claimed/Returned", NAVY), ("Closed", GREY)]
for i, (st, c) in enumerate(states):
    box(s, 7.0 + (i % 2) * 2.95, 2.55 + (i // 2) * 1.25, 2.75, 0.85, fill=c)
    text(s, 7.0 + (i % 2) * 2.95, 2.75 + (i // 2) * 1.25, 2.75, 0.5, st, size=17, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER)
box(s, 7.0, 5.35, 5.8, 1.5, fill=LIGHT)
text(s, 7.3, 5.5, 5.3, 1.2,
     "Domain entities: Item · ClaimDetails (0..1) · FoundReport (0..*) · Dispute (0..*) · "
     "Conversation/Message · User",
     size=16.5, color=NAVY)
footer(s, n)

# ================================================================ 7 ARCHITECTURE
n += 1
s = slide()
header(s, "WEEK 5 — ARCHITECTURE", "Layered monolith with a REST boundary")
box(s, 0.7, 2.1, 4.6, 3.3, fill=LIGHT)
text(s, 0.9, 2.2, 4.2, 0.4, "CLIENT — browser / PWA", size=17, bold=True, color=EMERALD)
for i, lbl in enumerate(["index.html + app.js", "Service worker (offline shell)", "localStorage (session, read marks)"]):
    box(s, 1.0, 2.7 + i * 0.85, 4.0, 0.65, fill=WHITE, line=GREY)
    text(s, 1.0, 2.82 + i * 0.85, 4.0, 0.4, lbl, size=15, align=PP_ALIGN.CENTER)
box(s, 8.0, 2.1, 4.6, 3.3, fill=LIGHT)
text(s, 8.2, 2.2, 4.2, 0.4, "SERVER — FastAPI monolith", size=17, bold=True, color=EMERALD)
for i, lbl in enumerate(["REST API  /api/*", "validation \u2192 permission checks", "domain logic \u2192 persistence"]):
    box(s, 8.3, 2.7 + i * 0.85, 4.0, 0.65, fill=WHITE, line=GREY)
    text(s, 8.3, 2.82 + i * 0.85, 4.0, 0.4, lbl, size=15, align=PP_ALIGN.CENTER)
arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(5.5), Inches(3.4), Inches(2.3), Inches(0.6))
arrow.fill.solid(); arrow.fill.fore_color.rgb = EMERALD; arrow.line.fill.background()
arrow.shadow.inherit = False
text(s, 5.5, 3.5, 2.3, 0.4, "fetch JSON / forms", size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
box(s, 8.0, 5.65, 4.6, 0.75, fill=NAVY)
text(s, 8.0, 5.82, 4.6, 0.4, "db.json  +  static/uploads/", size=16, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 0.7, 5.65, 4.9, 1.2, "Why not microservices or serverless? One developer, 13 weeks, "
     "and a demo that must run offline.", size=16, color=GREY)
footer(s, n)

# ================================================================ 8 DATABASE
n += 1
s = slide()
header(s, "WEEK 5 — DATABASE DESIGN", "ERD — designed relational, stored as documents")
tables = [
    ("USER", "id · email (unique) · name · salt · password_hash"),
    ("ITEM", "type · category · title · location · status · contact · reporter · custody · photo"),
    ("CLAIM_DETAILS", "1 : 0..1 with Item — claimant identity and proof of ownership"),
    ("FOUND_REPORT", "0..* per lost item — unique(item, finder email) blocks duplicates"),
    ("DISPUTE", "0..* while a claim is open — upheld or dismissed, with timestamps"),
    ("MESSAGE", "thread key = \u201citemId:partnerEmail\u201d — one private thread per pair"),
]
for i, (t, b) in enumerate(tables):
    y = 1.95 + i * 0.85
    box(s, 0.55, y, 12.25, 0.75, fill=LIGHT)
    box(s, 0.55, y, 0.08, 0.75, fill=EMERALD)
    text(s, 0.85, y + 0.08, 3.1, 0.6, t, size=18, bold=True, color=NAVY)
    text(s, 4.1, y + 0.1, 8.6, 0.6, b, size=16, color=GREY)
text(s, 0.55, 7.0, 12.2, 0.4,
     "The PostgreSQL schema in the docs is a direct transcription of this ERD — the migration is planned, not hypothetical.",
     size=16, color=GREY)
footer(s, n)

# ================================================================ 9 PATTERNS + SOLID
n += 1
s = slide()
header(s, "WEEK 6 — DESIGN", "Design patterns and my SOLID module")
pats = [
    ("Repository", "All reads/writes through save_state() / load_state() — PostgreSQL becomes a one-layer swap."),
    ("Strategy", "public_item() picks which fields to emit based on who is viewing."),
    ("Facade", "The front-end touches domain logic only through the REST surface."),
    ("Observer", "Unread dots: UI subscribes, server publishes counts (15 s polling)."),
]
for i, (t, b) in enumerate(pats):
    x = 0.55 + (i % 2) * 6.25
    y = 1.95 + (i // 2) * 1.7
    card(s, x, y, 5.95, 1.5, t, b, tsize=20, bsize=15.5)
box(s, 0.55, 5.5, 12.25, 1.5, fill=LIGHT)
box(s, 0.55, 5.5, 0.08, 1.5, fill=EMERALD)
text(s, 0.85, 5.62, 11.7, 0.4, "SOLID module: public_item(item, viewer_email)", size=20, bold=True, color=EMERALD)
text(s, 0.85, 6.08, 11.7, 0.9,
     "One job — decide what a viewer may see. Extensible to new viewer roles, always returns a valid "
     "projection, hides internal fields, and shields routes from the storage layout. "
     "Verified by test_public_api_strips_private_fields.",
     size=16, color=NAVY)
footer(s, n)

# ================================================================ 10 IMPLEMENTATION
n += 1
s = slide()
header(s, "WEEK 7 — IMPLEMENTATION", "Module 1, coding standard, version control")
text(s, 0.55, 1.95, 6, 0.5, "Module 1 — the core flow", size=22, bold=True, color=EMERALD)
bullets(s, 0.55, 2.55, 6.0, 3.0, [
    "POST /api/items — multipart report + photo, validated, rate-limited",
    "GET /api/items — filters plus the per-viewer privacy projection",
    "Front-end: form with live duplicate warning, browse grid, search",
    "Definition of done written before coding — all five conditions met",
], size=18, gap=11)
text(s, 7.0, 1.95, 6, 0.5, "Coding rules I kept", size=22, bold=True, color=EMERALD)
bullets(s, 7.0, 2.55, 5.9, 3.0, [
    "Every endpoint docstring states its permission rule",
    "All permission checks server-side — 403 with a reason",
    "Every mutation ends with save_state()",
    "All user strings pass escapeHtml() before rendering",
], size=18, gap=11)
box(s, 0.55, 5.85, 12.25, 1.1, fill=NAVY)
text(s, 0.85, 5.98, 11.7, 0.9,
     "Git: feature branches merged to main only when that module's tests passed. "
     "Merge rule: every new behaviour needs a positive test AND a permission-negative test.",
     size=17, color=WHITE)
footer(s, n)

# ================================================================ 11 TESTING + SECURITY
n += 1
s = slide()
header(s, "WEEKS 10–11 — TESTING & SECURITY", "28 tests, 84 % coverage, zero open defects")
m1 = box(s, 0.55, 1.95, 3.9, 1.9, fill=EMERALD)
text(s, 0.55, 2.2, 3.9, 0.8, "28", size=50, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 0.55, 3.15, 3.9, 0.5, "tests, all passing", size=18, color=WHITE, align=PP_ALIGN.CENTER)
m2 = box(s, 4.7, 1.95, 3.9, 1.9, fill=NAVY)
text(s, 4.7, 2.2, 3.9, 0.8, "84%", size=50, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 4.7, 3.15, 3.9, 0.5, "line coverage (gate: 80 %)", size=18, color=WHITE, align=PP_ALIGN.CENTER)
m3 = box(s, 8.85, 1.95, 3.9, 1.9, fill=AMBER)
text(s, 8.85, 2.2, 3.9, 0.8, "10 / 0", size=50, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 8.85, 3.15, 3.9, 0.5, "defects found / open", size=18, color=WHITE, align=PP_ALIGN.CENTER)
text(s, 0.55, 4.15, 6, 0.5, "What the tests prove", size=22, bold=True, color=EMERALD)
bullets(s, 0.55, 4.7, 6.0, 2.3, [
    "The full claim lifecycle — and every illegal shortcut rejected",
    "Nine tests assert the WRONG user gets a 403",
    "Anonymous API responses contain zero private fields",
], size=17.5, gap=9)
text(s, 7.0, 4.15, 6, 0.5, "Security: fixed vs accepted", size=22, bold=True, color=EMERALD)
bullets(s, 7.0, 4.7, 5.9, 2.3, [
    "Fixed: upload traversal, API contact leaks, unauthenticated confirm-return, spam limits",
    "Accepted for v1.0: email-string identity, salted SHA-256 — both analysed in the STRIDE model",
], size=17.5, gap=9)
footer(s, n)

# ================================================================ 12 METRICS + REFLECTION
n += 1
s = slide()
header(s, "WEEKS 12–13 — METRICS & REFLECTION", "The project in numbers, and what it taught me")
metrics = [
    ("~530", "lines of backend Python"), ("17", "REST endpoints"),
    ("28", "automated tests"), ("84%", "line coverage"),
    ("10 / 0", "defects found / open"), ("54 h", "effort vs 50 h estimate"),
]
for i, (num, lbl) in enumerate(metrics):
    x = 0.55 + (i % 3) * 4.15
    y = 1.95 + (i // 3) * 1.7
    box(s, x, y, 3.95, 1.5, fill=LIGHT)
    box(s, x, y, 3.95, 0.08, fill=EMERALD)
    text(s, x, y + 0.2, 3.95, 0.7, num, size=34, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    text(s, x + 0.15, y + 0.95, 3.65, 0.5, lbl, size=16, color=GREY, align=PP_ALIGN.CENTER)
text(s, 0.55, 5.5, 12.2, 0.5, "Reflection — the lesson behind the numbers", size=22, bold=True, color=EMERALD)
text(s, 0.55, 6.05, 12.2, 1.2,
     "Four separate bugs (shared chat thread, finder lockout, two blank grids) shared one root cause: the client "
     "assumed something about the server's payload that wasn't true. The fix class was always the same — "
     "the server decides, the client renders. Features finished a week early; the surplus went into testing and security.",
     size=17.5, color=NAVY)
footer(s, n)

# ================================================================ 13 CLOSE
n += 1
s = slide()
box(s, 0, 0, 13.333, 7.5, fill=NAVY)
box(s, 0, 3.5, 13.333, 0.07, fill=EMERALD)
text(s, 1.2, 2.2, 11, 1.1, "Thank you", size=54, color=WHITE, bold=True)
text(s, 1.2, 3.75, 11, 0.6, "Questions?", size=30, color=RGBColor(0x9C, 0xA3, 0xAF))
text(s, 1.2, 5.0, 11, 0.6, "Future work: session tokens · PBKDF2 · PostgreSQL · notifications · admin dashboard",
     size=19, color=EMERALD, bold=True)
text(s, 1.2, 5.9, 11, 1.4, [
    "Mathew Umama  ·  U23CS1067  ·  Computer Science",
    "CSC 403",
    "Live demo available on request — the portal runs from a single command.",
], size=19, color=WHITE, space_after=6)

NOTES = [
    # 1 title
    "Good morning. My name is Mathew Umama, matric number U23CS1067, Computer Science, CSC 403. "
    "My project is the AFIT Lost & Found Portal: a web application that connects students who lose "
    "property on campus with the people who find it. I built this alone over the thirteen weeks of "
    "this course, and it is deployed and running on the internet right now - not a mock-up.",
    # 2 problem
    "I want to start with why this problem exists. When you lose something on this campus, the only "
    "channels you have are informal ones. Notice boards that nobody checks, where last week's poster "
    "looks exactly like today's. WhatsApp groups where your message is buried within two days and "
    "you cannot search back through months of history. And a paper log at the security post that "
    "students are not allowed to search. The result is that items are handed in honestly and still "
    "never get claimed - not because people are dishonest, but because the finder and the owner "
    "never meet in the middle. That gap is the problem I chose to solve.",
    # 3 objectives and scope
    "I set six SMART objectives: report an item in under two minutes, search and filter across all "
    "reports, a verified claim-and-return workflow for found items, a lighter finder-response flow "
    "for lost items with private chat, an auditable trail of claims and disputes, and delivery as an "
    "installable mobile app. Then scope discipline. In scope: reporting, search, claims, chat, "
    "disputes, moderation, accounts, validation and anti-spam. Deliberately out of scope: email "
    "servers, payments, student-record integration, native apps and image recognition. Writing that "
    "second list down in week one was not paperwork - it stopped me twice later when I was tempted "
    "to add things I did not have time for.",
    # 4 process model
    "I chose the incremental model, and I want to justify that against the alternatives, because the "
    "choice shaped the whole project. Waterfall was tempting since the requirements felt clear, but "
    "it only gives you feedback at the very end - too late to act on it. Pure prototyping would have "
    "thrown away effort on flows that are already well understood. Scrum was the strongest rival, "
    "but this course is organised as thirteen graded weekly deliverables, not sprints, so it would "
    "have meant double bookkeeping. The payoff of incremental was concrete: the system was runnable "
    "at the end of every single week, and the feedback I got at the week eight demo went straight "
    "into weeks nine to thirteen without rewriting the core.",
    # 5 requirements
    "Week two was requirements engineering. I identified four stakeholder groups: students who lose "
    "things, finders, security and hall wardens, and student affairs. I gathered requirements by "
    "interviewing classmates - and the honest answer to 'what do you do when you lose something' "
    "was almost always 'post it in the class WhatsApp group and pray'. The interesting finding was "
    "a tension: finders want a light process, owners want verification. My whole design resolves "
    "that tension - lost reports get the light flow, found reports get the ownership quiz. Then I "
    "prioritised with MoSCoW. The 'will not have' row turned out to be the most useful one in the "
    "table.",
    # 6 UML
    "Week four, the UML models. The use case diagram has four actors and thirteen use cases. One "
    "modelling decision worth pointing out: 'Reporter' is not a separate kind of user - it is any "
    "student once they have filed a report. Modelling it separately made every permission rule in "
    "the system easier to state. The class diagram gives the domain model, and the heart of it is "
    "the status lifecycle: Active, then Claim Requested, then Claimed or Returned - with the reject "
    "path going back to Active. I drew two sequence diagrams because the system has two mirrored "
    "flows: found items get claimed with proof of ownership, and lost items get finder responses "
    "where the owner does the verifying.",
    # 7 architecture
    "Week five, architecture. I evaluated four candidates and rejected three. Microservices buy you "
    "distributed systems problems in exchange for benefits I did not need as one developer in "
    "thirteen weeks. Event-driven did not fit because I deliberately chose polling over WebSockets. "
    "Serverless would have made a live demo depend on cold starts and a vendor. So: a layered "
    "monolith with a REST boundary - presentation, API, domain and persistence. The important part "
    "is the boundary: the front end talks only to slash A P I, which is why I could restructure the "
    "internals repeatedly later without touching the interface.",
    # 8 database
    "Week five also covered the data design. One deliberate decision: I designed the ERD as if it "
    "were relational, even though the storage is a JSON file - so the PostgreSQL migration in the "
    "documentation is a transcription, not a redesign. Three decisions worth explaining. Claim "
    "details are one-to-zero-or-one with an item, because only one claim can be active at a time. "
    "Chat threads are keyed on item I D plus the partner's email - and that is exactly what prevents "
    "two finders of the same laptop from seeing each other's messages, which was a real bug I later "
    "found and fixed. And status is an enum-style field enforced in the domain layer, never trusted "
    "from the client.",
    # 9 patterns + SOLID
    "Week six, design patterns and the SOLID module. I will be honest about the process: I did not "
    "sit down and decide which patterns to apply. I built the system, recognised the patterns that "
    "had emerged, and then named them so they stayed consistent. Repository - all reads and writes "
    "go through two functions, so swapping the storage is one layer. Strategy - the privacy "
    "projection decides what a viewer may see based on their relationship to the item. Facade - the "
    "front end touches domain logic only through REST. Observer - unread indicators work by polling. "
    "Then my SOLID-compliant module: public_item. One responsibility, extensible to new viewer "
    "roles, always returns a valid projection, hides internal fields, and shields the routes from "
    "the storage layout. One test proves it holds.",
    # 10 implementation
    "Week seven, the first working module: report, validate, browse, search. Three rules from the "
    "coding standard that mattered most. Every endpoint docstring states its permission rule, so the "
    "permission matrix stays visible. Every mutation ends by saving state, which is the durability "
    "invariant. And every user-supplied string is escaped before rendering, which is the X S S "
    "defence. On version control: feature branches, merged only when that module's tests pass, with "
    "a merge rule that every new behaviour needs a positive test AND a permission-negative test. "
    "That second half is the rule that later caught a missing permission check before the demo, not "
    "after it.",
    # 11 testing + security
    "Weeks ten and eleven together, because they tell the same story. Twenty-eight automated tests, "
    "eighty-four percent line coverage against an eighty percent gate, and ten defects found with "
    "zero still open. The most valuable tests are not the happy paths - they are the nine that "
    "assert the wrong user receives a four-oh-three. Without those, the permission matrix is a claim; "
    "with them, it is evidence. On security: four real fixes - upload path traversal, contact details "
    "leaking through the API even when the UI hid them, an unauthenticated confirm-return endpoint, "
    "and missing spam limits. And two things I accepted openly rather than hiding: identity is an "
    "email string rather than a session token, and passwords use salted SHA-256 rather than a proper "
    "key-derivation function. Both are analysed in the STRIDE model, and token-based sessions are the "
    "first item on the v1.1 list.",
    # 12 metrics + reflection
    "The numbers: about five hundred and thirty lines of backend, seventeen REST endpoints all "
    "permission-checked, twenty-eight tests, eighty-four percent coverage, fifty-four hours of effort "
    "against a fifty-hour estimate. But the number I care about is the last one - features finished a "
    "week early, and I spent that surplus on testing and security, which is why the defect log ends "
    "at zero open. And the lesson behind all of it: four separate bugs - a shared chat thread, finders "
    "locked out of chat, and two blank grids - were all the same species. The client assumed something "
    "about the server's payload that was not true. The fix class was always the same: the server "
    "decides what exists, the client renders what it is given.",
    # 13 close
    "To close: the AFIT Lost & Found Portal replaces notice boards and WhatsApp threads with one "
    "searchable system, it is deployed and installable on a phone, and every claim, dispute and "
    "resolution leaves an audit trail. The future work is honest and specific: session tokens, proper "
    "password hashing, the PostgreSQL migration, and notifications. Thank you - I am happy to take "
    "questions, and I can demonstrate the live app on my phone if you would like to see it working.",
]

for sl, note in zip(prs.slides, NOTES):
    sl.notes_slide.notes_text_frame.text = note

prs.save("AFIT_Lost_and_Found_Presentation_v2.pptx")
print(f"Saved with {len(prs.slides._sldIdLst)} slides and speaker notes")
