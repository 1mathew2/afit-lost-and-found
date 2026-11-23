"""One clean deck: one idea per slide, large type, minimal styling."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

NAVY = RGBColor(0x14, 0x1C, 0x2B)
EMERALD = RGBColor(0x04, 0x6B, 0x4E)
GREY = RGBColor(0x55, 0x5D, 0x6B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RULE = RGBColor(0x04, 0x6B, 0x4E)
HEAD = "Georgia"
BODY = "Calibri"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

L = 0.85          # left margin
W = 11.6          # content width


def slide():
    return prs.slides.add_slide(BLANK)


def rule(s, y=2.08, w=1.9, h=0.055):
    bar = s.shapes.add_shape(1, Inches(L), Inches(y), Inches(w), Inches(h))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RULE
    bar.line.fill.background()
    bar.shadow.inherit = False
    return bar


def kicker(s, txt):
    tb = s.shapes.add_textbox(Inches(L), Inches(0.62), Inches(W), Inches(0.35))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = txt.upper()
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.name = BODY
    r.font.color.rgb = EMERALD


def title(s, txt, size=38):
    tb = s.shapes.add_textbox(Inches(L), Inches(0.98), Inches(W), Inches(1.05))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = txt
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.name = HEAD
    r.font.color.rgb = NAVY
    rule(s)


def headline(s, txt, size=26, y=5.0):
    """One-sentence statement under the content."""
    tb = s.shapes.add_textbox(Inches(L), Inches(y), Inches(W), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = txt
    r.font.size = Pt(size)
    r.font.name = BODY
    r.font.color.rgb = GREY
    return tb


def items(s, lines, y=2.4, size=24, gap=16, x=L, w=W, numbered=False):
    h = min(7.15 - y, len(lines) * (size * 0.0192 + gap / 72) + 0.25)
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        r = p.add_run()
        r.text = (f"{i + 1}.  " if numbered else "\u2014  ") + ln
        r.font.size = Pt(size)
        r.font.name = BODY
        r.font.color.rgb = NAVY
    return tb


def table(s, rows, widths, y=2.4, size=16, row_h=0.56, head_h=0.6, x=L, w=W):
    n = len(rows)
    shape = s.shapes.add_table(n, len(rows[0]), Inches(x), Inches(y), Inches(w),
                               Inches(head_h + row_h * (n - 1)))
    tbl = shape.table
    scale = w / sum(widths)
    for i, cw in enumerate(widths):
        tbl.columns[i].width = Inches(cw * scale)
    tbl.rows[0].height = Inches(head_h)
    for ri in range(1, n):
        tbl.rows[ri].height = Inches(row_h)
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.text = ""
            cell.margin_left = Inches(0.1)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = 3
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = str(val)
            r.font.size = Pt(size)
            r.font.name = BODY
            r.font.bold = ri == 0
            r.font.color.rgb = WHITE if ri == 0 else NAVY
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if ri == 0 else WHITE
    return tbl


NOTES = []

# ---------------------------------------------------------------- 1 title
s = slide()
tb = s.shapes.add_textbox(Inches(L), Inches(1.55), Inches(W), Inches(0.4))
p = tb.text_frame.paragraphs[0]
r = p.add_run()
r.text = "COURSE PROJECT  SP-014"
r.font.size, r.font.bold, r.font.name = Pt(14), True, BODY
r.font.color.rgb = EMERALD

tb = s.shapes.add_textbox(Inches(L), Inches(2.1), Inches(W), Inches(2.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run()
r.text = "AFIT Lost & Found Portal"
r.font.size, r.font.bold, r.font.name = Pt(50), True, HEAD
r.font.color.rgb = NAVY
p2 = tf.add_paragraph()
r2 = p2.add_run()
r2.text = "A verified lost-property portal for AFIT"
r2.font.size, r2.font.name = Pt(22), BODY
r2.font.color.rgb = GREY

rule(s, y=4.28, w=2.4)

tb = s.shapes.add_textbox(Inches(L), Inches(4.7), Inches(W), Inches(1.5))
tf = tb.text_frame
for i, ln in enumerate(["Mathew Umama  \u00b7  U23CS1067",
                        "Computer Science  \u00b7  CSC 403",
                        "afit-lost-and-found.onrender.com"]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.space_after = Pt(6)
    r = p.add_run()
    r.text = ln
    r.font.size, r.font.name = Pt(19), BODY
    r.font.color.rgb = NAVY
NOTES.append("Good morning. I am Mathew Umama, U23CS1067, Computer Science, and this is SP-014 - the AFIT "
             "Lost and Found Portal. It is deployed and running, so anything I mention can be demonstrated live.")

# ---------------------------------------------------------------- 2 the problem
s = slide()
kicker(s, "The problem")
title(s, "Lost property at AFIT is tracked informally")
items(s, [
    "Reports live on notice boards, WhatsApp groups and a paper log",
    "A student cannot search what security has already collected",
    "Found items are handed in, then sit unclaimed for weeks",
], y=2.5, size=27, gap=22)
headline(s, "The failure is not dishonesty. The finder and the owner never meet.",
         size=21, y=5.4)
NOTES.append("The problem is not that people are dishonest. It is that the finder and the owner never meet, "
             "because the record of a found item lives on a board or in a WhatsApp group that the owner cannot "
             "search.")

# ---------------------------------------------------------------- 3 objectives
s = slide()
kicker(s, "Objectives")
title(s, "What the system has to achieve")
items(s, [
    "Report a lost or found item in under two minutes",
    "Search and filter by type, category, location and keyword",
    "Verified claim and confirmed return for found items",
    "A lighter finder-response flow for lost items, with chat",
    "An auditable record of claims, disputes and resolutions",
    "Ship as an installable mobile app by week 13",
], y=2.45, size=25, gap=17, numbered=True)
NOTES.append("Six objectives. Each one is measurable: two minutes to report, a search that works without signing "
             "in, a claim that is verified rather than assumed, a finder response that is lighter than a claim, a "
             "record that can be audited, and a mobile app a student can install.")

# ---------------------------------------------------------------- 4 scope
s = slide()
kicker(s, "Scope")
title(s, "What is in, and what is deliberately out")
items(s, [
    "Reporting with photos and validation",
    "Search and filtering",
    "Claims, finder responses, private chat",
    "Disputes, moderation, accounts",
    "Installable mobile app, persistence",
], y=2.45, size=22, gap=13, x=L, w=6.0)
items(s, [
    "Email and SMS servers",
    "Payments",
    "Student records integration",
    "Native Android or iOS apps",
    "Multi-campus, image recognition",
], y=2.45, size=22, gap=13, x=7.15, w=5.3)
tb = s.shapes.add_textbox(Inches(L), Inches(6.55), Inches(W), Inches(0.4))
p = tb.text_frame.paragraphs[0]
r = p.add_run()
r.text = "Writing the out-of-scope list in week 1 stopped scope creep twice."
r.font.size, r.font.name = Pt(19), BODY
r.font.color.rgb = GREY
NOTES.append("In scope on the left, deliberately out of scope on the right. Writing the out-of-scope list in "
             "week one is what let me say no twice later, when the project could easily have grown past thirteen "
             "weeks.")

# ---------------------------------------------------------------- 5 process
s = slide()
kicker(s, "Process model")
title(s, "Incremental delivery, chosen over three alternatives")
table(s, [["Model", "Why it was not chosen"],
          ["Waterfall", "No feedback until week 13 - too late to change anything"],
          ["Prototyping", "Effort spent on screens that get thrown away"],
          ["Scrum", "Built for teams; weekly deliverables already double as sprints"],
          ["Incremental", "Something runnable, reviewable and measurable every week"]],
      widths=[2.0, 9.3], size=18, row_h=0.78)
NOTES.append("I chose incremental. Waterfall would have given me no feedback until the end. Prototyping builds "
             "screens you throw away. Scrum assumes a team and adds bookkeeping on top of the weekly deliverables. "
             "Incremental gave me something runnable every single week.")

# ---------------------------------------------------------------- 6 plan
s = slide()
kicker(s, "Plan")
title(s, "Thirteen weeks, thirteen checkpoints")
table(s, [["Weeks", "What was produced"],
          ["1 - 2", "Proposal, requirements specification, user stories"],
          ["3", "Validation, MoSCoW, schedule, risk register"],
          ["4 - 6", "UML models, architecture, database, design, wireframes"],
          ["7 - 8", "Working module one, prototype demonstration"],
          ["9 - 10", "Remaining modules, code review, test suite"],
          ["11 - 12", "Security, CI pipeline, deployment, user manual"],
          ["13", "Final report and demonstration"]],
      widths=[1.8, 9.5], size=18, row_h=0.58)
NOTES.append("The thirteen-week baseline. I estimated fifty hours of work and spent fifty-four - eight percent "
             "over - and the two features that caused the overrun were evidence validation and the chat threading.")

# ---------------------------------------------------------------- 7 FR 1
s = slide()
kicker(s, "Requirements  \u00b7  1 of 2")
title(s, "Functional requirements, FR-1 to FR-7")
items(s, [
    "FR-1   Report a lost or found item, with a photo",
    "FR-2   Validate names, emails, phone numbers, matric IDs",
    "FR-3   Search and filter without signing in",
    "FR-4   Warn when a similar report already exists",
    "FR-5   Claim a found item; the reporter confirms or rejects",
    "FR-6   A rejected claimant cannot claim that item again",
    "FR-7   Finder responses on lost items",
], y=2.45, size=22, gap=13)
NOTES.append("Fourteen functional requirements in total. These seven are reporting, validation, search, duplicate "
             "detection, and the claim lifecycle. FR-5 and FR-6 are the ones that carry the most marks, because a "
             "claim is only real if the reporter confirms the return.")

# ---------------------------------------------------------------- 8 FR 2
s = slide()
kicker(s, "Requirements  \u00b7  2 of 2")
title(s, "Functional requirements, FR-8 to FR-14")
items(s, [
    "FR-8    Private chat between the reporter and one person",
    "FR-9    Disputes, upheld or dismissed with a record",
    "FR-10   Edit, delete, mark as found, close own report",
    "FR-11   Accounts with salted, hashed passwords",
    "FR-12   Anti-spam limits on reports and messages",
    "FR-13   Contact details visible only to participants",
    "FR-14   Data survives a server restart",
], y=2.45, size=22, gap=13)
NOTES.append("FR-8 to FR-14 cover chat, disputes, moderation, accounts, anti-spam, contact privacy and "
             "persistence. FR-13 is the requirement that shaped the whole security design: contact details are "
             "hidden until a claim or a finder response exists.")

# ---------------------------------------------------------------- 9 NFR
s = slide()
kicker(s, "Requirements")
title(s, "Non-functional requirements")
table(s, [["Requirement", "Measurable target"],
          ["Usability", "Report in under two minutes; usable at 360 px wide"],
          ["Performance", "Search results in under a second over 1,000 items"],
          ["Security", "Passwords salted and hashed; images capped at 5 MB"],
          ["Reliability", "Every change written to disk immediately"],
          ["Availability", "The page still opens offline once installed"],
          ["Maintainability", "28 automated tests, 84 percent coverage"],
          ["Privacy", "Contacts hidden until a claim or response exists"]],
      widths=[3.0, 8.3], size=17, row_h=0.5)
NOTES.append("Eight non-functional requirements, and each one has a number attached, because a requirement you "
             "cannot measure is an opinion. The security and reliability rows are the two I can demonstrate: five "
             "megabyte image cap, and a disk write on every mutation.")

# ---------------------------------------------------------------- 10 stories
s = slide()
kicker(s, "User stories")
title(s, "Two stories, with the criteria that test them")
table(s, [["Story", "Acceptance criteria"],
          ["US-4  As the owner of a found ID card, I want to claim it with proof so the finder can verify me.",
           "Proof required \u00b7 reporter confirms or rejects \u00b7 after rejection I cannot claim that item again"],
          ["US-6  As the owner, I want to chat privately with one finder at a time so messages never reach the wrong person.",
           "One thread per pair \u00b7 outsiders get a 403 \u00b7 unread dots clear after reading"]],
      widths=[6.2, 5.6], size=17, row_h=1.55, head_h=0.55)
headline(s, "All eight stories' acceptance criteria became automated tests in week 10.", size=19, y=6.3)
NOTES.append("Every acceptance criterion here became an automated test in week ten. The right-hand column of "
             "US-6 is literally the assertion in one of my tests: an outsider asking for that chat gets a 403.")

# ---------------------------------------------------------------- 11 risks
s = slide()
kicker(s, "Risk management")
title(s, "Six risks I actively managed")
table(s, [["ID", "Risk", "P x I", "Response"],
          ["R1", "Scope creep", "9", "MoSCoW plus a binding will-not-have list"],
          ["R2", "Data loss in a file store", "6", "Save to disk on every mutation"],
          ["R3", "Identity spoofing by email", "6", "Accepted, analysed in the threat model"],
          ["R4", "Stale interface from the service worker", "6", "Network-first, versioned cache"],
          ["R6", "Upload abuse", "6", "Extension whitelist, 5 MB cap, random names"],
          ["R7", "Single developer unavailable", "6", "Weekly increments keep it runnable"]],
      widths=[0.8, 5.2, 1.0, 6.4], size=16, row_h=0.66)
NOTES.append("Six risks scored probability times impact, each with an active response rather than a note. Two of "
             "them actually happened during the project - scope creep and the stale service worker - and because "
             "they were written down in week three, both had a prepared answer.")

# ---------------------------------------------------------------- 12 uml
s = slide()
kicker(s, "Modelling")
title(s, "Four actors, thirteen use cases, one lifecycle")
items(s, [
    "Student       report lost, search, claim",
    "Finder        report found, search, respond",
    "Reporter      chat, confirm, reject, dispute, edit",
    "Third party   search, file a dispute",
], y=2.4, size=21, gap=11, x=L, w=6.2)
items(s, [
    "Active",
    "Claim Requested",
    "Claimed / Returned",
    "Closed",
], y=2.4, size=21, gap=11, x=7.1, w=5.0)
tb = s.shapes.add_textbox(Inches(7.1), Inches(5.0), Inches(5.0), Inches(1.9))
tf = tb.text_frame
tf.word_wrap = True
for i, ln in enumerate(["The status lifecycle is the spine of the model:",
                        "every rule in the system is a rule about",
                        "which transition is allowed, and by whom."]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.space_after = Pt(4)
    r = p.add_run()
    r.text = ln
    r.font.size, r.font.name = Pt(18), BODY
    r.font.color.rgb = GREY
NOTES.append("Four actors and thirteen use cases. The right-hand column is the status lifecycle, which is the "
             "spine of the design - every business rule in the system is a rule about which transition is allowed, "
             "and which user is allowed to make it.")

# ---------------------------------------------------------------- 13 architecture
s = slide()
kicker(s, "Architecture")
title(s, "A layered monolith, on purpose")
table(s, [["Layer", "Responsibility"],
          ["Presentation", "Installable app: one page, one script, one service worker"],
          ["API", "Twenty-two endpoints: validation, permissions, status changes"],
          ["Domain", "Claim lifecycle, spam limits, thread resolution"],
          ["Persistence", "Save and load to a JSON file"]],
      widths=[2.6, 8.7], size=18, row_h=0.72)
headline(s, "Microservices and serverless were rejected: one developer, thirteen weeks, offline demonstrations.",
         size=19, y=6.1)
NOTES.append("Four layers. I rejected microservices, serverless and a single-file script, all for the same "
             "reason: one developer, thirteen weeks, and demonstrations that have to work on a phone with poor "
             "Wi-Fi. The layer boundary is what later let me move the whole interface out of the backend file in "
             "hours instead of weeks.")

# ---------------------------------------------------------------- 14 database
s = slide()
kicker(s, "Database design")
title(s, "Seven tables, designed relationally")
table(s, [["Table", "Key relationship"],
          ["users", "Email is unique; password stored as salt plus hash"],
          ["items", "Reporter email, status, category, location"],
          ["claim_details", "One to zero-or-one with items"],
          ["rejected_claimants", "Composite key: item and email"],
          ["found_reports", "Unique item and finder email"],
          ["disputes", "Upheld or dismissed, always kept"],
          ["messages", "Thread key: item plus the other person"]],
      widths=[3.0, 8.3], size=17, row_h=0.6)
NOTES.append("Seven tables designed relationally even though version one stores JSON, so the PostgreSQL "
             "migration is a transcription rather than a redesign. The schema already exists with check "
             "constraints, unique constraints and cascade deletes.")

# ---------------------------------------------------------------- 15 design
s = slide()
kicker(s, "Design")
title(s, "Four patterns, and one module held to SOLID")
items(s, [
    "Repository        save and load isolate storage from the API",
    "Strategy            the privacy projection picks fields per viewer",
    "Facade               the interface only talks to the domain over REST",
    "Observer           unread indicators by polling, not coupling",
], y=2.4, size=20, gap=13)
headline(s, "public_item() satisfies all five SOLID principles, and one test keeps it honest.", size=20, y=5.85)
NOTES.append("Four patterns, each with a reason. The line at the bottom is the one I would defend: the privacy "
             "function satisfies all five SOLID principles, and a single test asserts that it never leaks a "
             "private field to an anonymous viewer.")

# ---------------------------------------------------------------- 16 implementation
s = slide()
kicker(s, "Implementation")
title(s, "Standards I held myself to")
items(s, [
    "Every endpoint docstring states its permission rule",
    "All input goes through one validation gate",
    "Permissions are enforced on the server, never the screen",
    "Every mutation ends with a save",
    "Every new behaviour needs a positive test and a refusal test",
], y=2.45, size=23, gap=18)
NOTES.append("Five of the nine coding rules, and the last one is the one that changed the quality of the "
             "system: every new behaviour needs a test that it works, and a test that the wrong user is refused.")

# ---------------------------------------------------------------- 17 testing
s = slide()
kicker(s, "Testing")
title(s, "28 tests, 84 percent coverage, 10 defects, none open")
items(s, [
    "Nine tests assert that the wrong user receives a 403",
    "Every requirement traced to at least one test",
    "The most valuable test found a chat leak between finders",
    "Coverage gate of 80 percent enforced by CI on every push",
], y=2.45, size=23, gap=18)
NOTES.append("Twenty-eight automated tests at eighty-four percent coverage against an eighty percent gate. The "
             "first line matters most: nine of those tests assert that the wrong user is refused. Without them the "
             "permission matrix would be a claim; with them it is evidence.")

# ---------------------------------------------------------------- 18 defects
s = slide()
kicker(s, "Quality")
title(s, "What the defect log actually taught me")
table(s, [["Defect", "Root cause"],
          ["A message reached every finder", "Thread keyed by the item alone"],
          ["Return could be confirmed by anyone", "Endpoint written before the permission pass"],
          ["The API exposed contact details", "Raw records returned to the interface"],
          ["Item grid went blank", "The screen assumed a field always exists"]],
      widths=[5.3, 6.0], size=17, row_h=0.82)
headline(s, "Four of the ten defects were one species: the screen assumed something about the data.",
         size=19, y=6.4)
NOTES.append("Four of my ten defects were the same species. The screen assumed something about what the server "
             "would send it. The fix class became a rule I now follow: the server decides, the screen only "
             "renders.")

# ---------------------------------------------------------------- 19 security
s = slide()
kicker(s, "Security")
title(s, "Threats addressed, and two accepted in the open")
table(s, [["Threat", "Control"],
          ["Spoofing", "Owner identity checked on every state change"],
          ["Tampering", "Random file names, extension whitelist, 5 MB cap"],
          ["Information disclosure", "Privacy projection for every response"],
          ["Denial of service", "Report, dispute and message rate limits"],
          ["Elevation of privilege", "Uploads served statically, never executed"]],
      widths=[3.4, 7.9], size=17, row_h=0.66)
headline(s, "Accepted for version one: email-based identity, and SHA-256 instead of a key-derivation function.",
         size=18, y=6.45)
NOTES.append("Five threat classes with the control that answers each. The line at the bottom is the honest part: "
             "version one identifies users by email string rather than session tokens, and hashes with SHA-256 "
             "rather than a key derivation function. Both are documented, and token authentication is the first "
             "item in version 1.1.")

# ---------------------------------------------------------------- 20 maintenance
s = slide()
kicker(s, "Maintenance")
title(s, "A change request, processed properly")
table(s, [["Field", "Detail"],
          ["Request", "Notify me when someone responds to my report"],
          ["Impact", "Mail dependency, new attack surface, six to eight hours"],
          ["Timing", "Would land on the testing and security weeks"],
          ["Alternative", "In-app unread indicators, already built"],
          ["Decision", "Partly approved, deferred to version 1.1"]],
      widths=[2.2, 9.1], size=18, row_h=0.75)
NOTES.append("One real change request, handled as a change request: impact analysis, a decision, and a note of "
             "what was shipped instead. I deferred email notifications rather than compromise the testing and "
             "security weeks.")

# ---------------------------------------------------------------- 21 final
s = slide()
kicker(s, "Final report")
title(s, "What works, and what it does not do yet")
items(s, [
    "Complete lifecycle: report, search, claim, chat, confirm",
    "Finder responses, disputes, moderation, accounts",
    "Limitation: email identity, no session tokens",
    "Limitation: no password key derivation, no login throttling",
    "Limitation: no write locking; cloud disk is ephemeral",
], y=2.45, size=22, gap=16)
NOTES.append("Three capabilities and three limitations, stated plainly. I would rather name the limitations "
             "myself than be asked about them, and every one of them has a documented path to a fix.")

# ---------------------------------------------------------------- 22 reflection
s = slide()
kicker(s, "Reflection")
title(s, "Four lessons the defects taught me")
items(s, [
    "The server decides; the screen only renders",
    "Measure caching behaviour before trusting it",
    "Test from every role's point of view, not just the happy one",
    "Privacy is a server concern; hiding a field is not security",
], y=2.5, size=24, gap=22, numbered=True)
NOTES.append("Four lessons, each one paid for by a defect. If I had to compress the whole project into one "
             "sentence it would be the first line: the server decides, and the screen only renders.")

# ---------------------------------------------------------------- 23 close
s = slide()
kicker(s, "SP-014")
title(s, "Thank you", size=48)
items(s, [
    "Mathew Umama  \u00b7  U23CS1067  \u00b7  Computer Science  \u00b7  CSC 403",
    "afit-lost-and-found.onrender.com",
    "Questions, or a live demonstration?",
], y=2.75, size=22, gap=20)
NOTES.append("Thank you. The system is live at that address, so I am happy to take questions or demonstrate any "
             "flow on my phone.")

for sl, note in zip(prs.slides, NOTES):
    sl.notes_slide.notes_text_frame.text = note

OUT = "AFIT_SP014_Presentation_FINAL.pptx"
try:
    prs.save(OUT)
except PermissionError:
    OUT = "AFIT_SP014_Presentation_FINAL_v2.pptx"
    prs.save(OUT)
print(f"Saved {OUT} - {len(prs.slides._sldIdLst)} slides, notes on all")
