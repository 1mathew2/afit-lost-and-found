# Week 2 — Software Requirements Specification, Sections 1–3 (SP-014)

**Deliverables:** stakeholders, SRS §1–3, user stories with acceptance criteria. **Marks: 8**

## 1. Introduction

### 1.1 Purpose
This document specifies the functional and non-functional requirements of the **AFIT Lost &
Found Portal**, a web application that connects people who lose property on the AFIT campus
with people who find it.

### 1.2 Scope
The portal covers item reporting (lost/found), search, claim verification, finder responses,
private chat, dispute handling and reporter moderation. Notification servers, payments and
integration with student records are out of scope for v1.0.

### 1.3 Definitions
- **Reporter** — the person who filed a report (owner of a lost item; finder of a found item).
- **Claimant** — a person asserting ownership of a found item via the claim flow.
- **Finder response** — a light-weight "I found your lost item" submission on a lost report.
- **Dispute** — a third-party report that a claim in progress is false.

## 2. Stakeholders

| Stakeholder | Interest / stake | Influence |
|---|---|---|
| Students (lost-item owners) | Fast recovery of property | High — primary users |
| Students/staff (finders) | Easy, official way to report finds | High — primary users |
| Campus security / hall wardens | Digital handover log per post | Medium |
| Student affairs division | Dispute oversight, statistics | Medium |
| Course instructor / examiners | Correct SE process and working system | Medium |
| Portal administrator (developer) | Data integrity, moderation, uptime | High |

### 2.1 Elicitation notes
Requirements were elicited from: (1) interviews with classmates about how they currently
search for lost property (notice boards, WhatsApp groups), (2) observation of the security
post paper log process, (3) analysis of similar public systems (university lost-and-found
portals), (4) the course workbook constraints (13 weekly deliverables).

## 3. Functional Requirements

**FR-1 Reporting.** An authenticated user shall file a report classified as *lost* or *found*,
with title, description, category, location, date, optional photo, reporter identification
(full name, matric/ID, phone, email) and preferred contact method (email/phone/both).

**FR-2 Validation.** The system shall reject reports with invalid names, email addresses,
phone numbers (Nigerian format `0[789]XXXXXXXX` / `+234[789]XXXXXXXX`) or matric/IDs
(letters + digits), both in the browser and on the server.

**FR-3 Search and filter.** Any visitor shall search reports by keyword and filter by type
(lost/found), category, location and status without signing in.

**FR-4 Duplicate warning.** While typing a report title, the system shall show similar
existing reports (token-overlap ≥ 34%) so duplicates surface before submission.

**FR-5 Claim flow (found items).** A user other than the reporter shall submit a claim with
identification, contact details, proof description and optional proof photo. The item status
becomes *Claim Requested*. The reporter shall confirm the return (status → *Claimed/Returned*)
or reject it (status → *Active*).

**FR-6 Rejected claimants.** A user whose claim was rejected shall be permanently barred from
claiming that same item again, enforced server-side.

**FR-7 Finder responses (lost items).** A user other than the reporter shall respond
"I found this item" with identification, contact details, where it was found and an optional
note. The reporter shall view all responses, chat with each finder and resolve the report by
marking it returned (optionally crediting a specific finder) or closing it.

**FR-8 Private chat.** The reporter and one claimant/finder shall exchange direct messages in
a private per-pair thread. Outsiders shall receive 403. Unread message indicators shall be shown.

**FR-9 Disputes.** While a claim is in progress, any third party shall file a dispute with
name, email and reason (max 20 per item). The reporter shall uphold the dispute (claim rejected,
item back to Active) or dismiss it. Resolved disputes disappear from the active badge but
remain in the audit trail.

**FR-10 Moderation.** The reporter shall edit every field of their own *Active* report
(including photo and contact details, except the identity email), delete it, mark a lost item
as found, or close it.

**FR-11 Accounts.** Users shall sign up (name, email, password ≥ 6 chars) and sign in.
Passwords shall be stored salted and hashed, never in plain text.

**FR-12 Anti-spam.** The system shall limit each reporter ID to 3 active portal-submitted
lost reports, 20 disputes per item, 20 finder responses per item and 200 messages per chat.

**FR-13 Contact gating.** Contact details (email/phone) shall be visible only to the reporter,
the active claimant, or a finder on that item — enforced by the server, not just hidden in the UI.

**FR-14 Persistence.** All items, users, conversations and counters shall survive server restarts.

## 4. Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-1 | Usability | A report can be filed in ≤ 2 minutes; the UI works on a 360 px phone screen |
| NFR-2 | Performance | Search over 1,000 items responds in ≤ 1 s on a laptop-class machine |
| NFR-3 | Security | Passwords salted+hashed; private data stripped server-side; uploads restricted to images ≤ 5 MB with generated filenames |
| NFR-4 | Reliability | State persisted to disk on every mutation; server restart loses nothing |
| NFR-5 | Availability | PWA installs on a phone home screen; the app shell and last-seen items work offline |
| NFR-6 | Maintainability | One backend module (`main.py`), separated front-end (`static/app.js`), 28 automated tests, 84 % line coverage |
| NFR-7 | Portability | Runs on any machine with Python 3.10+; no external database server required |
| NFR-8 | Legal/ethical | Personal contact details are shown only to involved parties; disputes keep a neutral audit trail |

## 5. User Stories (with acceptance criteria)

**US-1 — Report a lost item.** *As a student who lost my powerbank, I want to report it with
details and a photo so finders know what to look for.*
- AC1: form validates all fields; invalid phone/matric/email is rejected with a clear message.
- AC2: after submit, the item appears in Browse with a *Lost* badge and status *Active*.
- AC3: my contact details are not shown to visitors until they engage (FR-13).

**US-2 — Report a found item.** *As a finder of an ID card, I want to log it and say where it
is held so the owner can reach it.*
- AC1: the form requires the designated handover person/officer (FR-1).
- AC2: the card shows "Custody" (security post or with finder).

**US-3 — Search.** *As a student, I want to search "HP laptop" and filter by location so I can
quickly check whether mine was found.*
- AC1: keyword matches title/description/location/category; filters combine.
- AC2: results show type, status and location badges.

**US-4 — Claim a found item.** *As the owner of the found ID card, I want to claim it with
proof so the finder can verify me.*
- AC1: claim form requires ID, contact and proof description; optional proof photo.
- AC2: reporter sees Confirm / Reject; confirm → *Claimed/Returned*, reject → item *Active*.
- AC3: after rejection I cannot claim that item again (FR-6).

**US-5 — Respond to a lost report.** *As a finder of a reported-lost laptop, I want to click
"I Found This Item" and leave my contact so the owner can reach me — without an ownership quiz.*
- AC1: short form (name, matric, phone, email, where found, note).
- AC2: owner sees "N finder responses" and can open each response.
- AC3: duplicate responses from the same email are rejected.

**US-6 — Chat to arrange return.** *As the owner, I want to chat privately with one finder at
a time so messages never reach the wrong person.*
- AC1: each reporter↔finder pair has its own thread; a message to finder A never reaches finder B.
- AC2: an outsider opening the thread gets "This chat is private…".
- AC3: unread dots appear on new messages and clear after reading.

**US-7 — Dispute a claim.** *As the real owner, I want to report a false claim so it is reviewed.*
- AC1: dispute recorded with name/email/reason; reporter sees an amber badge.
- AC2: uphold → claim rejected and item Active; dismiss → claim stands; both leave an audit entry.

**US-8 — Moderate my report.** *As the reporter, I want to edit or close my report when details
change or the item turns up.*
- AC1: Edit opens a pre-filled form covering every report field except the identity email.
- AC2: Mark as Found / Close resolve the report and update badges everywhere.
