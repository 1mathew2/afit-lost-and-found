# Week 2 — Software Requirements Specification, Sections 1–3 (SP-014)

**Deliverables:** stakeholders, SRS §1–3, user stories with acceptance criteria. **Marks: 8**

## 1. Introduction

### 1.1 Purpose
This document records what the **AFIT Lost & Found Portal** is supposed to do before I got
deep into building it. I wrote it so that when I inevitably forgot why I made a decision in
week 9, I could come back and read why it was made in week 2.

### 1.2 Scope
The portal covers item reporting (lost/found), search, claim verification, finder responses,
private chat, dispute handling and reporter moderation. Things I'm explicitly not doing in
v1.0: notification servers, payments, and integration with student records.

### 1.3 A few terms I'll use throughout
- **Reporter** — the person who filed a report. If it's a lost report, they're the owner; if
  it's a found report, they're the finder holding the item.
- **Claimant** — someone asserting "this found item is mine" through the claim flow.
- **Finder response** — a lighter thing: an "I found your lost item" submission on a lost report.
- **Dispute** — a third party flagging a claim in progress as false.

## 2. Stakeholders

| Stakeholder | What they care about | Influence |
|---|---|---|
| Students who lost items | Getting their property back, quickly | High — the main users |
| Finders | An easy, official way to hand things in | High — the other main users |
| Campus security / hall wardens | A digital handover log per post | Medium |
| Student affairs | Dispute oversight, statistics | Medium |
| Course instructor | Correct SE process and a working system | Medium |
| Me (developer/admin) | Data integrity, moderation, keeping the demo alive | High |

### 2.1 How I actually gathered the requirements
I want to be honest about this part, because it wasn't a formal process. I did three things:
I interviewed a handful of classmates about what happens when they lose something (the answer
was almost always "post in the class WhatsApp group and pray"), I watched how the security
post's paper log works, and I looked at how other universities run their lost-and-found
portals. The requirement that surprised me most came out of this: finders don't want a
burdensome process, and owners *do* want verification. Those two pressures pulled the design
in different directions and I talk about how I resolved that in the user stories.

## 3. Functional Requirements

I've numbered these so I can trace them to tests later (week 10).

**FR-1 Reporting.** An authenticated user can file a report classified as *lost* or *found*,
with title, description, category, location, date, an optional photo, their identification
(full name, matric/ID, phone, email) and a preferred contact method (email/phone/both).

**FR-2 Validation.** The system rejects reports with invalid names, emails, phone numbers
(Nigerian format `0[789]XXXXXXXX` or `+234[789]XXXXXXXX`) or matric/IDs (letters plus digits).
I enforce this in the browser *and* on the server — I learned early that client-only
validation is a suggestion, not a control.

**FR-3 Search and filter.** Anyone can search by keyword and filter by type, category,
location and status, without signing in.

**FR-4 Duplicate warning.** While someone types a report title, the system shows similar
existing reports (token overlap ≥ 34%) so duplicates surface *before* submission, not after.

**FR-5 Claim flow (found items).** A user other than the reporter submits a claim with
identification, contact details, a proof description and an optional proof photo. The item
moves to *Claim Requested*. The reporter then either confirms the return (item becomes
*Claimed/Returned*) or rejects it (back to *Active*).

**FR-6 Rejected claimants.** If your claim was rejected, you're permanently barred from
claiming that same item again — and I enforce this on the server, because a client-side
message would be trivially bypassed.

**FR-7 Finder responses (lost items).** A user other than the reporter can respond "I found
this item" with identification, contact details, where it was found and an optional note. The
reporter sees all responses, can chat with each finder individually, and resolves the report
by marking it returned (optionally crediting a specific finder) or closing it.

**FR-8 Private chat.** The reporter and one claimant/finder exchange messages in a private
per-pair thread. Outsiders get a 403. Unread message indicators show what's new.

**FR-9 Disputes.** While a claim is in progress, any third party can file a dispute with name,
email and reason (capped at 20 per item). The reporter upholds the dispute (claim rejected,
item back to Active) or dismisses it. Resolved disputes disappear from the active badge but
stay in the audit trail.

**FR-10 Moderation.** The reporter can edit every field of their own *Active* report —
including the photo and contact details, though not the identity email — and can delete it,
mark a lost item as found, or close it.

**FR-11 Accounts.** Users sign up (name, email, password ≥ 6 chars) and sign in. Passwords are
stored salted and hashed. I would not ship plain-text passwords for a class project any more
than for a real one.

**FR-12 Anti-spam.** Each reporter ID is limited to 3 active portal-submitted lost reports,
20 disputes per item, 20 finder responses per item and 200 messages per chat. Open systems
without limits get abused; I've seen it happen in class group chats.

**FR-13 Contact gating.** Contact details (email/phone) are visible only to the reporter, the
active claimant, or a finder on that item — enforced by the server, not just hidden in the UI.
This one cost me a rewrite later (see week 9), and I'm glad I wrote it down as a requirement
from the start.

**FR-14 Persistence.** Everything survives a server restart. For a demo, this is non-negotiable.

## 4. Non-Functional Requirements

| ID | Category | What I committed to |
|----|----------|--------------------|
| NFR-1 | Usability | A report takes ≤ 2 minutes to file; the UI works on a 360 px phone screen |
| NFR-2 | Performance | Search over 1,000 items responds in ≤ 1 s on a laptop-class machine |
| NFR-3 | Security | Salted+hashed passwords; private data stripped server-side; uploads restricted to images ≤ 5 MB with generated filenames |
| NFR-4 | Reliability | State written to disk on every mutation; a restart loses nothing |
| NFR-5 | Availability | PWA installs on a phone home screen; the shell and last-seen items work offline |
| NFR-6 | Maintainability | One backend module, a separated front-end, 28 automated tests, 84 % line coverage (achieved — see W10) |
| NFR-7 | Portability | Runs on any machine with Python 3.10+; no database server to install |
| NFR-8 | Legal/ethical | Contact details shown only to involved parties; disputes keep a neutral audit trail |

## 5. User Stories (with acceptance criteria)

I wrote these from the four stakeholder perspectives. Each one has acceptance criteria I could
actually test later, which turned out to matter more than I expected.

**US-1 — Report a lost item.** *As a student who lost my powerbank, I want to report it with
details and a photo so finders know what to look for.*
- AC1: the form validates everything; a bad phone/matric/email gets a clear, specific error.
- AC2: after submitting, the item shows up in Browse with a *Lost* badge and status *Active*.
- AC3: my contact details are not shown to random visitors (FR-13).

**US-2 — Report a found item.** *As a finder of an ID card, I want to log it and say where
it's held so the owner can reach it.*
- AC1: the form requires the designated handover person/officer (FR-1).
- AC2: the card shows where the item is held — security post or with the finder.

**US-3 — Search.** *As a student, I want to search "HP laptop" and filter by location so I can
quickly check whether mine turned up.*
- AC1: keywords match title, description, location and category; filters combine.
- AC2: results show type, status and location badges at a glance.

**US-4 — Claim a found item.** *As the owner of the found ID card, I want to claim it with
proof so the finder can verify me.*
- AC1: the claim form requires ID, contact and a proof description; proof photo optional.
- AC2: the reporter sees Confirm / Reject; confirm → *Claimed/Returned*, reject → *Active*.
- AC3: after a rejection I can't claim that item again (FR-6).

**US-5 — Respond to a lost report.** *As a finder of a reported-lost laptop, I want to click
"I Found This Item" and leave my contact so the owner can reach me — without being quizzed on
ownership I can't prove.*
- AC1: a short form — name, matric, phone, email, where I found it, optional note.
- AC2: the owner sees "N finder responses" and can open each one.
- AC3: I can't spam the same response twice from the same email.

**US-6 — Chat to arrange the return.** *As the owner, I want to chat privately with one finder
at a time so messages never reach the wrong person.*
- AC1: each reporter↔finder pair gets its own thread; a message to finder A never lands in
  finder B's chat. (This broke in testing once — see week 10's defect log.)
- AC2: an outsider opening the thread gets "This chat is private…".
- AC3: unread dots appear on new messages and clear once read.

**US-7 — Dispute a claim.** *As the real owner, I want to report a false claim so it gets
reviewed.*
- AC1: the dispute is recorded with name, email and reason; the reporter sees an amber badge.
- AC2: uphold → claim rejected and the item goes back to Active; dismiss → the claim stands;
  either way there's an audit entry.

**US-8 — Moderate my report.** *As the reporter, I want to edit or close my report when
details change or the item turns up in my bag.*
- AC1: Edit opens a pre-filled form covering every field except the identity email.
- AC2: Mark as Found / Close resolve the report and update badges everywhere.

## 6. What I'd flag about this SRS

Reading it back, the requirement that shaped the whole system was FR-13. Everything about the
viewer-based data projection, and eventually the week-11 security work, grew out of that one
line. If I were starting again I'd have written it even earlier and more explicitly.
