"""Builds the SP-014 theory presentation: AFIT Lost & Found Portal."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
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
SW, SH = prs.slide_width, prs.slide_height


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


def text(s, x, y, w, h, runs, size=18, color=NAVY, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, space_after=6, line_spacing=1.0):
    """runs: str, or list of paragraphs; each paragraph is str or (str, dict-overrides)."""
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
    box(s, 0, 0, 13.333, 0.16, fill=EMERALD)
    text(s, 0.55, 0.32, 12.3, 0.35, kicker, size=13, color=EMERALD, bold=True)
    text(s, 0.55, 0.62, 12.3, 0.85, title, size=32, color=NAVY, bold=True)


def bullets(s, x, y, w, h, items, size=17, gap=8):
    """items: list of str or (text, indent_level)."""
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


def card(s, x, y, w, h, title, body, tsize=16, bsize=13, accent=EMERALD):
    box(s, x, y, w, h, fill=LIGHT)
    box(s, x, y, 0.07, h, fill=accent)
    text(s, x + 0.25, y + 0.12, w - 0.4, 0.4, title, size=tsize, bold=True, color=NAVY)
    text(s, x + 0.25, y + 0.55, w - 0.4, h - 0.65, body, size=bsize, color=GREY, space_after=3)


def footer(s, n):
    text(s, 0.55, 7.08, 6, 0.3, "AFIT Lost & Found Portal — SP-014", size=10, color=GREY)
    text(s, 12.3, 7.08, 0.6, 0.3, str(n), size=10, color=GREY, align=PP_ALIGN.RIGHT)


n = 0

# ---------------------------------------------------------------- 1 title
s = slide()
box(s, 0, 0, 13.333, 7.5, fill=NAVY)
box(s, 0, 3.62, 13.333, 0.06, fill=EMERALD)
text(s, 1.2, 1.7, 11, 0.5, "SP-014  ·  SOFTWARE ENGINEERING COURSE PROJECT", size=16, color=EMERALD, bold=True)
text(s, 1.2, 2.2, 11, 1.3, "AFIT Lost & Found Portal", size=54, color=WHITE, bold=True)
text(s, 1.2, 3.85, 11, 0.5, "Report it. Search it. Recover it.", size=22, color=RGBColor(0x9C, 0xA3, 0xAF))
text(s, 1.2, 5.1, 11, 1.2, [
    "Mathew Umama  ·  U23CS1067  ·  1mathewumama@gmail.com",
    "Final presentation — single-person project",
], size=16, color=WHITE, space_after=4)

# ---------------------------------------------------------------- 2 problem
n += 1
s = slide()
header(s, "MOTIVATION", "The problem I set out to solve")
text(s, 0.55, 1.7, 12.2, 0.8,
     "Every semester, phones, ID cards, laptops and textbooks go missing on campus — and the "
     "only recovery channels we have are informal ones.",
     size=19, color=NAVY)
cards = [
    ("Notice boards", "Nobody checks them, and a poster from last week looks the same as one from today."),
    ("WhatsApp groups", "Messages get buried within two days. There is no search across months of history."),
    ("Paper logs at security", "Students cannot search them. The record exists, but only for the officer holding the book."),
    ("The result", "Recovered items pile up unclaimed — the finder and the owner simply never meet."),
]
for i, (t, b) in enumerate(cards):
    x = 0.55 + (i % 2) * 6.25
    y = 2.75 + (i // 2) * 1.85
    card(s, x, y, 5.95, 1.6, t, b, accent=EMERALD if i < 3 else AMBER)
footer(s, n)

# ---------------------------------------------------------------- 3 objectives/scope
n += 1
s = slide()
header(s, "WEEK 1 — PROPOSAL", "Objectives and scope")
text(s, 0.55, 1.75, 6, 0.4, "Six SMART objectives", size=18, bold=True, color=EMERALD)
bullets(s, 0.55, 2.25, 6.1, 4.4, [
    "Report a lost or found item in under 2 minutes",
    "Search and filter by type, category, location, keyword",
    "Verified claim-and-return workflow for found items",
    "Lightweight \u201cI found this\u201d flow for lost items, with private chat",
    "An auditable trail of claims, disputes and resolutions",
    "Ship it all as an installable, mobile-friendly PWA",
], size=16)
text(s, 7.0, 1.75, 6, 0.4, "Scope discipline", size=18, bold=True, color=EMERALD)
card(s, 7.0, 2.25, 5.8, 2.1, "In scope (v1.0)",
     "Reporting with photos · search · claims · finder responses · private chat · disputes · "
     "moderation · accounts · validation · anti-spam · PWA · persistence", bsize=13)
card(s, 7.0, 4.55, 5.8, 2.1, "Deliberately out of scope",
     "Email/SMS servers · payments · student-records integration · native apps · multi-campus · "
     "image recognition. Written down in week 1 so I could say no later.", bsize=13, accent=AMBER)
footer(s, n)

# ---------------------------------------------------------------- 4 process model
n += 1
s = slide()
header(s, "WEEK 1 — PROCESS MODEL", "Why I chose the incremental model")
stages = ["Proposal", "Requirements", "Planning", "UML", "Architecture", "Module 1",
          "Demo", "Full system", "Testing", "Security", "Docs", "Final"]
x0, w_each = 0.55, 1.02
for i, st in enumerate(stages):
    shp = box(s, x0 + i * (w_each + 0.03), 2.1, w_each, 0.85, fill=EMERALD if i < 8 else NAVY)
    text(s, x0 + i * (w_each + 0.03), 2.28, w_each, 0.6, st, size=10.5, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER)
text(s, 0.55, 3.1, 12.2, 0.4, "Each week delivers a usable increment — the system was runnable at the end of every week.",
     size=15, color=GREY)
rejected = [
    ("Waterfall", "Feedback would only arrive at the end — too late to act on."),
    ("Pure prototyping", "Throwaway prototypes waste effort when the core flows are clear."),
    ("Scrum", "Strongest rival, but the course is weekly deliverables, not sprints — double bookkeeping."),
]
for i, (t, b) in enumerate(rejected):
    card(s, 0.55, 3.75 + i * 1.05, 12.25, 0.9, t, b, tsize=14, bsize=12, accent=AMBER)
footer(s, n)

# ---------------------------------------------------------------- 5 requirements
n += 1
s = slide()
header(s, "WEEK 2 — REQUIREMENTS ENGINEERING", "Stakeholders and elicitation")
stake = [
    ("Students who lost items", "Get property back, fast", "High"),
    ("Finders", "An official way to hand things in", "High"),
    ("Security / wardens", "A digital handover log per post", "Medium"),
    ("Student affairs", "Dispute oversight, statistics", "Medium"),
]
for i, (t, b, infl) in enumerate(stake):
    x = 0.55 + i * 3.12
    box(s, x, 1.8, 2.95, 1.5, fill=LIGHT)
    box(s, x, 1.8, 0.07, 1.5, fill=EMERALD)
    text(s, x + 0.2, 1.92, 2.6, 0.4, t, size=13.5, bold=True)
    text(s, x + 0.2, 2.35, 2.6, 0.6, b, size=11.5, color=GREY)
    text(s, x + 0.2, 2.95, 2.6, 0.3, "Influence: " + infl, size=10.5, color=EMERALD, bold=True)
text(s, 0.55, 3.6, 12.2, 0.5, "How I gathered requirements (honestly):", size=17, bold=True, color=NAVY)
bullets(s, 0.55, 4.15, 12.2, 2.6, [
    "Interviewed classmates — the answer to \u201cwhat do you do when you lose something?\u201d was almost always \u201cpost in the class WhatsApp group and pray\u201d",
    "Observed the security post's paper log process",
    "Studied how other universities run lost-and-found portals",
    "The tension I found: finders want a light process, owners want verification. The whole design resolves that tension — lost reports get the light flow, found reports get the quiz.",
], size=15, gap=7)
footer(s, n)

# ---------------------------------------------------------------- 6 FRs / MoSCoW
n += 1
s = slide()
header(s, "WEEKS 2–3 — REQUIREMENTS", "14 functional requirements, prioritised MoSCoW")
moscow = [
    ("Must have", "Reporting · validation · search · claim flow · moderation · accounts · persistence", EMERALD),
    ("Should have", "Rejected-claimant ban · finder responses · private chat · disputes · contact gating · anti-spam", NAVY),
    ("Could have", "Duplicate warning · unread dots · PWA offline shell · photo replacement", GREY),
    ("Won't have (v1.0)", "Email/SMS · admin dashboard · payments · multi-campus", AMBER),
]
for i, (t, b, c) in enumerate(moscow):
    y = 1.85 + i * 1.15
    box(s, 0.55, y, 12.25, 1.0, fill=LIGHT)
    box(s, 0.55, y, 0.07, 1.0, fill=c)
    text(s, 0.85, y + 0.1, 3.2, 0.8, t, size=16, bold=True, color=c)
    text(s, 4.2, y + 0.12, 8.4, 0.8, b, size=13.5, color=NAVY)
text(s, 0.55, 6.55, 12.2, 0.5,
     "The \u201cWon't have\u201d list was the most useful row — it stopped me twice when scope creep came knocking.",
     size=14, color=GREY)
footer(s, n)

# ---------------------------------------------------------------- 7 user stories
n += 1
s = slide()
header(s, "WEEK 2 — USER STORIES", "Stories written to be testable")
stories = [
    ("US-1 — Report a lost item",
     "\u201cAs a student who lost my powerbank, I want to report it with details and a photo so finders know what to look for.\u201d",
     "AC: invalid input rejected with a clear error · appears in Browse with a Lost badge · contact hidden from visitors"),
    ("US-4 — Claim a found item",
     "\u201cAs the owner of the found ID card, I want to claim it with proof so the finder can verify me.\u201d",
     "AC: proof required · reporter confirms or rejects · after rejection I cannot claim that item again"),
    ("US-5 — Respond to a lost report",
     "\u201cAs a finder of a reported-lost laptop, I want to click \u2018I Found This Item\u2019 and leave my contact — without an ownership quiz.\u201d",
     "AC: short form · owner sees \u201cN finder responses\u201d · no duplicate responses"),
    ("US-6 — Chat to arrange the return",
     "\u201cAs the owner, I want to chat privately with one finder at a time so messages never reach the wrong person.\u201d",
     "AC: one thread per pair · outsiders get 403 · unread dots clear after reading"),
]
for i, (t, story, ac) in enumerate(stories):
    y = 1.8 + i * 1.32
    box(s, 0.55, y, 12.25, 1.18, fill=LIGHT)
    box(s, 0.55, y, 0.07, 1.18, fill=EMERALD)
    text(s, 0.85, y + 0.07, 11.8, 0.35, t, size=14, bold=True, color=EMERALD)
    text(s, 0.85, y + 0.4, 11.8, 0.45, story, size=12.5, color=NAVY)
    text(s, 0.85, y + 0.82, 11.8, 0.3, ac, size=10.5, color=GREY)
footer(s, n)

# ---------------------------------------------------------------- 8 UML use case
n += 1
s = slide()
header(s, "WEEK 4 — UML", "Use cases and actors")
actors = [("Student", "report lost · search · claim"), ("Finder", "report found · search · respond \u201cI found this\u201d"),
          ("Reporter", "chat · confirm/reject · resolve disputes · edit/close"), ("Third party", "search · file a dispute")]
for i, (a, acts) in enumerate(actors):
    y = 1.85 + i * 1.05
    box(s, 0.55, y, 3.1, 0.9, fill=NAVY)
    text(s, 0.75, y + 0.22, 2.7, 0.5, a, size=15, bold=True, color=WHITE)
    text(s, 3.9, y + 0.18, 8.9, 0.7, acts, size=14, color=NAVY)
box(s, 0.55, 6.2, 12.25, 0.75, fill=LIGHT)
text(s, 0.85, 6.33, 11.7, 0.55,
     "Design note: \u201cReporter\u201d is not a separate kind of user — it is any student once they have filed a report. "
     "Modelling it as its own actor made every permission in the system easier to state.",
     size=13, color=NAVY)
footer(s, n)

# ---------------------------------------------------------------- 9 class model
n += 1
s = slide()
header(s, "WEEK 4 — UML", "Domain model and the status lifecycle")
ents = [
    ("Item", "the report: type, category, title, location, status, photo, contact"),
    ("ClaimDetails", "0..1 per found item — claimant identity + proof of ownership"),
    ("FoundReport", "0..* per lost item — who found it, where, contact"),
    ("Dispute", "0..* while a claim is in progress — upheld or dismissed"),
    ("Conversation / Message", "keyed itemId:partnerEmail — one private thread per pair"),
    ("User", "sign-in identity, salted password hash"),
]
for i, (t, b) in enumerate(ents):
    y = 1.85 + i * 0.78
    box(s, 0.55, y, 6.4, 0.68, fill=LIGHT)
    box(s, 0.55, y, 0.07, 0.68, fill=EMERALD)
    text(s, 0.85, y + 0.05, 6.0, 0.3, t, size=13.5, bold=True)
    text(s, 0.85, y + 0.34, 6.0, 0.3, b, size=10.5, color=GREY)
# lifecycle
text(s, 7.5, 1.9, 5.3, 0.4, "Item status lifecycle", size=17, bold=True, color=EMERALD)
states = [("Active", EMERALD), ("Claim Requested", AMBER), ("Claimed/Returned", NAVY), ("Closed", GREY)]
for i, (st, c) in enumerate(states):
    box(s, 7.5 + (i % 2) * 2.75, 2.5 + (i // 2) * 1.15, 2.5, 0.75, fill=c)
    text(s, 7.5 + (i % 2) * 2.75, 2.68 + (i // 2) * 1.15, 2.5, 0.4, st, size=13, color=WHITE, bold=True,
         align=PP_ALIGN.CENTER)
text(s, 7.5, 5.0, 5.3, 1.9, [
    "Active \u2192 Claim Requested \u2192 Claimed/Returned",
    "Reject path returns the item to Active and bans that claimant",
    "Lost items can also be resolved by the reporter: mark-found or close",
], size=13, color=GREY, space_after=8)
footer(s, n)

# ---------------------------------------------------------------- 10 sequence
n += 1
s = slide()
header(s, "WEEK 4 — UML", "Sequence — the main flow (claim and return)")
steps = [
    ("1", "Reporter submits a found-item report", "validated server-side, persisted, status = Active"),
    ("2", "Claimant submits a claim with proof", "checks: Active? not self-claim? not previously rejected?"),
    ("3", "Status becomes Claim Requested", "the item is now locked to one claim at a time"),
    ("4", "They chat privately", "thread keyed itemId:claimant_email; owner sees an unread dot"),
    ("5", "Reporter confirms the return", "status = Claimed/Returned — or rejects: back to Active, claimant banned"),
]
for i, (num, t, b) in enumerate(steps):
    y = 1.85 + i * 1.02
    box(s, 0.55, y, 0.62, 0.85, fill=EMERALD)
    text(s, 0.55, y + 0.2, 0.62, 0.45, num, size=18, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    text(s, 1.4, y + 0.04, 11.3, 0.4, t, size=15.5, bold=True, color=NAVY)
    text(s, 1.4, y + 0.44, 11.3, 0.4, b, size=12.5, color=GREY)
text(s, 0.55, 7.0, 12.2, 0.4,
     "Chosen as \u201cthe\u201d main flow because it exercises the most of the system: two users, a state transition, validation, chat and a permission check.",
     size=12, color=GREY)
footer(s, n)

# ---------------------------------------------------------------- 11 architecture
n += 1
s = slide()
header(s, "WEEK 5 — ARCHITECTURE", "Layered monolith with a REST boundary")
# drawn component diagram
box(s, 0.7, 2.2, 4.6, 3.6, fill=LIGHT)
text(s, 0.9, 2.3, 4.2, 0.35, "CLIENT — browser / PWA", size=13, bold=True, color=EMERALD)
for i, lbl in enumerate(["index.html + app.js", "Service worker (offline shell)", "localStorage (session, read marks)"]):
    box(s, 1.0, 2.8 + i * 0.95, 4.0, 0.7, fill=WHITE, line=GREY)
    text(s, 1.0, 2.95 + i * 0.95, 4.0, 0.4, lbl, size=12, align=PP_ALIGN.CENTER)
box(s, 8.0, 2.2, 4.6, 3.6, fill=LIGHT)
text(s, 8.2, 2.3, 4.2, 0.35, "SERVER — FastAPI monolith", size=13, bold=True, color=EMERALD)
for i, lbl in enumerate(["REST API  /api/*", "validation gate \u2192 permission checks", "domain logic \u2192 persistence"]):
    box(s, 8.3, 2.8 + i * 0.95, 4.0, 0.7, fill=WHITE, line=GREY)
    text(s, 8.3, 2.95 + i * 0.95, 4.0, 0.4, lbl, size=12, align=PP_ALIGN.CENTER)
arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(5.5), Inches(3.6), Inches(2.3), Inches(0.55))
arrow.fill.solid(); arrow.fill.fore_color.rgb = EMERALD; arrow.line.fill.background()
arrow.shadow.inherit = False
text(s, 5.5, 3.68, 2.3, 0.4, "fetch  JSON / FormData", size=10.5, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
box(s, 8.0, 6.05, 4.6, 0.75, fill=NAVY)
text(s, 8.0, 6.22, 4.6, 0.4, "db.json  +  static/uploads/", size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 0.7, 6.15, 4.9, 0.6, "Why not microservices / serverless? One developer, 13 weeks, "
     "and a demo that must run offline — the monolith buys clarity, the REST boundary buys swap-ability.",
     size=12, color=GREY)
footer(s, n)

# ---------------------------------------------------------------- 12 ERD
n += 1
s = slide()
header(s, "WEEK 5 — DATABASE DESIGN", "ERD designed relational, stored as documents")
tables = [
    ("USER", "id · email (UK) · name · salt · password_hash"),
    ("ITEM", "id · item_type · category · title · location · status · contact_* · reporter_id · security_personnel · custody · image_url"),
    ("CLAIM_DETAILS", "1:0..1 with ITEM — claimant identity, proof description, proof photo"),
    ("FOUND_REPORT", "0..* per lost item — UNIQUE(item_id, finder_email) blocks duplicates"),
    ("DISPUTE", "0..* — message, status (upheld/dismissed), resolved_at"),
    ("MESSAGE", "thread_key = \u201citemId:partnerEmail\u201d · sender · text · time"),
]
for i, (t, b) in enumerate(tables):
    y = 1.8 + i * 0.82
    box(s, 0.55, y, 12.25, 0.72, fill=LIGHT)
    box(s, 0.55, y, 0.07, 0.72, fill=EMERALD)
    text(s, 0.85, y + 0.06, 2.9, 0.6, t, size=13.5, bold=True, color=NAVY)
    text(s, 3.9, y + 0.08, 8.8, 0.6, b, size=11.5, color=GREY)
text(s, 0.55, 6.8, 12.2, 0.5,
     "The PostgreSQL schema in the docs is a direct transcription of this ERD — the migration is planned, not hypothetical.",
     size=13, color=GREY)
footer(s, n)

# ---------------------------------------------------------------- 13 patterns
n += 1
s = slide()
header(s, "WEEK 6 — DESIGN PATTERNS", "Four patterns that emerged, then got named")
pats = [
    ("Repository", "All reads/writes go through save_state() / load_state(). Swapping db.json for PostgreSQL means rewriting one layer, not hunting file writes."),
    ("Strategy", "public_item() picks which fields to emit based on the viewer's relationship; lost vs found run different flows selected on item_type."),
    ("Facade", "The front-end touches domain logic only through the REST surface — one door, stable URLs, internals free to change."),
    ("Observer", "Unread indicators: the UI subscribes (15 s polling), the server publishes per-thread counts. Polling over WebSockets — fewer parts to fail live."),
]
for i, (t, b) in enumerate(pats):
    x = 0.55 + (i % 2) * 6.25
    y = 1.85 + (i // 2) * 2.15
    card(s, x, y, 5.95, 1.95, t, b, tsize=17, bsize=13)
text(s, 0.55, 6.3, 12.2, 0.6,
     "I did not sit down and think \u201cwhich patterns shall I apply today?\u201d — I built the system, recognised the patterns, "
     "then named them and made them consistent. That is how patterns are supposed to arrive in small projects.",
     size=13.5, color=GREY)
footer(s, n)

# ---------------------------------------------------------------- 14 SOLID
n += 1
s = slide()
header(s, "WEEK 6 — SOLID", "My compliant module: public_item(item, viewer_email)")
solid = [
    ("S — Single responsibility", "One job: decide what a given viewer may see. No validation, no persistence, no status logic."),
    ("O — Open/closed", "A new viewer relationship (e.g. security officer) extends the flags inside — endpoints and consumers untouched."),
    ("L — Liskov substitution", "Any viewer type yields a valid projection — every flag always present. Sounds theoretical until a grid goes blank."),
    ("I — Interface segregation", "Consumers get five viewer flags, not the raw internal record with its bookkeeping fields."),
    ("D — Dependency inversion", "Routes depend on this abstraction, not the storage layout — internals were renamed without breaking anything."),
]
for i, (t, b) in enumerate(solid):
    y = 1.8 + i * 0.98
    box(s, 0.55, y, 12.25, 0.88, fill=LIGHT)
    box(s, 0.55, y, 0.07, 0.88, fill=EMERALD)
    text(s, 0.85, y + 0.08, 3.9, 0.7, t, size=14, bold=True, color=NAVY)
    text(s, 4.9, y + 0.1, 7.8, 0.7, b, size=12.5, color=GREY)
text(s, 0.55, 6.8, 12.2, 0.5,
     "Evidence: test_public_api_strips_private_fields — anonymous viewers receive zero private fields; reporters receive their own.",
     size=13, color=EMERALD, bold=True)
footer(s, n)

# ---------------------------------------------------------------- 15 implementation
n += 1
s = slide()
header(s, "WEEK 7 — IMPLEMENTATION", "Module 1, coding standard, version control")
text(s, 0.55, 1.75, 6, 0.4, "Module 1 — the core flow", size=17, bold=True, color=EMERALD)
bullets(s, 0.55, 2.25, 6.0, 3.4, [
    "POST /api/items — multipart report + photo, validation gate, anti-spam limit",
    "GET /api/items — filters plus the per-viewer privacy projection",
    "Front-end: form with live duplicate warning, browse grid, search card",
    "Definition of done written before coding — all five conditions checked",
], size=14.5)
text(s, 7.0, 1.75, 6, 0.4, "Rules I kept (a sample)", size=17, bold=True, color=EMERALD)
bullets(s, 7.0, 2.25, 5.9, 3.4, [
    "Every endpoint docstring states its permission rule",
    "All permission checks server-side, 403 with a reason",
    "Every mutation ends with save_state()",
    "All user strings pass escapeHtml() before rendering",
    "Service-worker cache bumped on every release",
], size=14.5)
box(s, 0.55, 5.85, 12.25, 1.0, fill=NAVY)
text(s, 0.85, 5.97, 11.7, 0.8,
     "Git: feature branches (reporting, claims, chat, moderation, fixes) merged to main only when that module's tests passed. "
     "Merge checklist rule #2: every new behaviour needs a positive test AND a permission-negative test.",
     size=13.5, color=WHITE)
footer(s, n)

# ---------------------------------------------------------------- 16 testing
n += 1
s = slide()
header(s, "WEEK 10 — TESTING", "28 tests, 84 % coverage, zero open defects")
m1 = box(s, 0.55, 1.85, 3.9, 2.2, fill=EMERALD)
text(s, 0.55, 2.15, 3.9, 0.8, "28", size=52, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 0.55, 3.35, 3.9, 0.5, "tests, all passing", size=15, color=WHITE, align=PP_ALIGN.CENTER)
m2 = box(s, 4.7, 1.85, 3.9, 2.2, fill=NAVY)
text(s, 4.7, 2.15, 3.9, 0.8, "84%", size=52, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 4.7, 3.35, 3.9, 0.5, "line coverage (gate: 80 %)", size=15, color=WHITE, align=PP_ALIGN.CENTER)
m3 = box(s, 8.85, 1.85, 3.9, 2.2, fill=AMBER)
text(s, 8.85, 2.15, 3.9, 0.8, "10", size=52, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
text(s, 8.85, 3.35, 3.9, 0.5, "defects found — 0 open", size=15, color=WHITE, align=PP_ALIGN.CENTER)
text(s, 0.55, 4.4, 12.2, 0.4, "What the tests actually check", size=17, bold=True, color=EMERALD)
bullets(s, 0.55, 4.9, 12.2, 2.2, [
    "The full lifecycle: Active \u2192 Claim Requested \u2192 Claimed/Returned — and every illegal shortcut rejected",
    "Nine tests assert that the WRONG user gets a 403 — without them the permission matrix is a claim, not evidence",
    "Privacy: an anonymous API response contains zero contact, claim, finder or dispute fields",
    "The uncovered 16 % is static-file plumbing and defensive branches — I documented what it is rather than chasing the number",
], size=14.5, gap=7)
footer(s, n)

# ---------------------------------------------------------------- 17 security
n += 1
s = slide()
header(s, "WEEK 11 — SECURITY", "STRIDE, OWASP, and what I fixed vs accepted")
fixed = [
    ("Tampering — uploads", "Client-controlled filenames allowed path traversal. Fixed: UUID names, image whitelist, 5 MB cap."),
    ("Info disclosure — API", "Contact details reached the browser even when the UI hid them. Fixed: server-side viewer projection."),
    ("Elevation — confirm-return", "Anyone could confirm a return. Fixed: reporter email required, 403 otherwise."),
    ("DoS — spam", "Open reporting invites abuse. Fixed: 3 active lost reports, 20 disputes/responses per item, 200 messages per chat."),
]
for i, (t, b) in enumerate(fixed):
    x = 0.55 + (i % 2) * 6.25
    y = 1.85 + (i // 2) * 1.7
    card(s, x, y, 5.95, 1.5, t, b, tsize=14, bsize=12)
box(s, 0.55, 5.5, 12.25, 1.4, fill=LIGHT)
box(s, 0.55, 5.5, 0.07, 1.4, fill=AMBER)
text(s, 0.85, 5.62, 11.7, 0.4, "Accepted for v1.0 — stated, not hidden", size=15, bold=True, color=AMBER)
text(s, 0.85, 6.05, 11.7, 0.8,
     "Identity is a plain email string (no session tokens) and passwords use salted SHA-256, not a KDF. "
     "Both are fully analysed in the STRIDE model; token auth is the first v1.1 item. I would rather an examiner "
     "hear this from me than find it.",
     size=13, color=NAVY)
footer(s, n)

# ---------------------------------------------------------------- 18 maintenance
n += 1
s = slide()
header(s, "WEEK 12 — MAINTENANCE", "Change request CR-001, processed properly")
box(s, 0.55, 1.85, 12.25, 1.0, fill=LIGHT)
text(s, 0.85, 1.95, 11.7, 0.8,
     "\u201cNotify me when someone responds to my lost item\u201d — requested by the demo audience after the week-8 prototype.",
     size=16, color=NAVY, bold=True)
impact = [
    ("Backend", "A new outbound dependency — SMTP/SMS gateway I do not have"),
    ("Security", "New attack surface: SMTP credentials, spam-relay risk"),
    ("Schedule", "6–8 h landing on the testing and security weeks"),
    ("Alternative", "In-app unread dots + response badges already shipped"),
]
for i, (t, b) in enumerate(impact):
    x = 0.55 + (i % 2) * 6.25
    y = 3.1 + (i // 2) * 1.35
    card(s, x, y, 5.95, 1.15, t, b, tsize=14, bsize=12)
box(s, 0.55, 6.0, 12.25, 0.95, fill=EMERALD)
text(s, 0.85, 6.12, 11.7, 0.7,
     "Decision: partially approved, re-scoped. v1.0 ships the in-app indicators; email/SMS is deferred to v1.1. "
     "Status: closed — deferred, alternative delivered.",
     size=14.5, color=WHITE, bold=True)
footer(s, n)

# ---------------------------------------------------------------- 19 metrics
n += 1
s = slide()
header(s, "WEEK 12 — METRICS", "The project in numbers")
metrics = [
    ("~530", "lines of backend Python"), ("~1,530", "lines of front-end HTML + JS"),
    ("17", "REST endpoints, all permission-checked"), ("28", "automated tests"),
    ("84%", "line coverage"), ("10 / 0", "defects found / still open"),
    ("54 h", "effort vs 50 h estimate (+8 %)"), ("W8", "feature-complete, a week early"),
]
for i, (num, lbl) in enumerate(metrics):
    x = 0.55 + (i % 4) * 3.12
    y = 1.9 + (i // 4) * 2.0
    box(s, x, y, 2.95, 1.8, fill=LIGHT)
    box(s, x, y, 2.95, 0.07, fill=EMERALD)
    text(s, x, y + 0.25, 2.95, 0.7, num, size=34, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    text(s, x + 0.15, y + 1.05, 2.65, 0.7, lbl, size=12.5, color=GREY, align=PP_ALIGN.CENTER)
text(s, 0.55, 6.2, 12.2, 0.7,
     "The numbers I would point an examiner at: features finished a week early, and the surplus went into testing "
     "and security — which is why the defect log ends at zero open.",
     size=14, color=GREY)
footer(s, n)

# ---------------------------------------------------------------- 20 reflection
n += 1
s = slide()
header(s, "WEEK 13 — REFLECTION", "What the project taught me")
lessons = [
    ("The server decides; the client renders", "Four separate incidents (shared chat thread, finder lockout, two blank grids) were all the same species: the client assumed something about the payload that wasn't true."),
    ("Measure caching behaviour early", "The service worker fought me for days before I understood it. The proper fix cost one afternoon. The asymmetry is the lesson."),
    ("Test from every role's perspective", "A feature can be correct and still unusable — finders could technically chat, but the client guard bounced them."),
    ("Privacy is a server concern", "Hiding fields in the UI while the API served them to anyone was caught in review — before it became an embarrassing demo moment."),
    ("Refactor before the pain", "Extracting the UI from the backend \u201ccost\u201d an afternoon and halved the cost of every feature after it."),
]
for i, (t, b) in enumerate(lessons):
    y = 1.8 + i * 1.02
    box(s, 0.55, y, 12.25, 0.92, fill=LIGHT)
    box(s, 0.55, y, 0.07, 0.92, fill=EMERALD)
    text(s, 0.85, y + 0.06, 4.3, 0.8, t, size=14, bold=True, color=NAVY)
    text(s, 5.3, y + 0.08, 7.4, 0.8, b, size=11.5, color=GREY)
footer(s, n)

# ---------------------------------------------------------------- 21 future work
n += 1
s = slide()
header(s, "WEEK 13 — FUTURE WORK", "What v1.1 would add, in priority order")
fw = [
    ("1", "Session tokens + login rate limiting", "closes the two accepted STRIDE risks (S1, S2)"),
    ("2", "PBKDF2 password hashing", "replaces salted SHA-256 with a proper KDF"),
    ("3", "PostgreSQL migration", "the schema is already written — a transcription, not a redesign"),
    ("4", "Email/SMS notifications", "CR-001, now with an SMTP dependency and a threat-model update"),
    ("5", "Admin dashboard for security posts", "the deferred stakeholder feature"),
    ("6", "Image content sniffing + audit logging", "magic-byte upload checks; an audit trail for admin actions"),
]
for i, (num, t, b) in enumerate(fw):
    y = 1.85 + i * 0.85
    box(s, 0.55, y, 0.62, 0.72, fill=NAVY)
    text(s, 0.55, y + 0.14, 0.62, 0.45, num, size=16, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    text(s, 1.4, y + 0.02, 6.2, 0.6, t, size=15, bold=True, color=NAVY)
    text(s, 7.7, y + 0.06, 5.1, 0.6, b, size=12, color=GREY)
footer(s, n)

# ---------------------------------------------------------------- 22 close
n += 1
s = slide()
box(s, 0, 0, 13.333, 7.5, fill=NAVY)
box(s, 0, 3.55, 13.333, 0.06, fill=EMERALD)
text(s, 1.2, 2.3, 11, 1.0, "Thank you", size=48, color=WHITE, bold=True)
text(s, 1.2, 3.85, 11, 0.5, "Questions?", size=24, color=RGBColor(0x9C, 0xA3, 0xAF))
text(s, 1.2, 5.2, 11, 1.0, [
    "Mathew Umama  ·  U23CS1067  ·  1mathewumama@gmail.com",
    "Live demo available on request — the portal runs from a single command.",
], size=16, color=WHITE, space_after=4)

prs.save("AFIT_Lost_and_Found_Presentation.pptx")
print(f"Saved AFIT_Lost_and_Found_Presentation.pptx with {len(prs.slides.slides if hasattr(prs.slides,'slides') else prs.slides._sldIdLst)} slides")
