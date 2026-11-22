# Week 13 — Final Report, Reflection and Peer Assessment (SP-014)

**Deliverables:** final demonstration, final report, reflection, peer assessment. **Marks: 16**

## 1. Final Demonstration

The final system demonstrates the complete lifecycle end-to-end (script in `week08_demo.md`,
extended with the moderation and security items). Headline capabilities at delivery:

| Capability | Status |
|-----------|--------|
| Lost + found reporting with photos, validation, duplicate warnings | ✔ |
| Search/filter/browse, responsive mobile + desktop, installable PWA with offline shell | ✔ |
| Claim & verify ownership with confirm/reject and rejected-claimant ban | ✔ |
| Lightweight finder responses for lost items with owner moderation | ✔ |
| Private per-pair chat with unread indicators | ✔ |
| Disputes with uphold/dismiss audit trail | ✔ |
| Full report editing (incl. photo), mark-as-found, close, delete | ✔ |
| Accounts (salted+hashed passwords), persistence across restarts | ✔ |
| Server-enforced permissions and privacy projection | ✔ |
| Anti-spam limits and input validation gate | ✔ |
| 28 automated tests, 84 % coverage, CI pipeline | ✔ |

## 2. Final Report

### 2.1 Summary
The AFIT Lost & Found Portal replaces notice boards and WhatsApp threads with a single
searchable system. It was built incrementally over 13 weeks: a working reporting/search core
by Week 7, a full prototype demo (including chat and disputes, ahead of schedule) at Week 8,
feature completion in Week 9, then dedicated testing, security hardening and documentation
weeks. The result is a real, deployable FastAPI + PWA application with a file-persistence
layer designed for a one-line upgrade to PostgreSQL.

### 2.2 Requirements outcome
All 14 functional requirements and 8 non-functional requirements in scope were delivered
(see W2/W12). One change request (CR-001, notifications) was processed and partially delivered
via in-app indicators; the email/SMS variant was deferred with recorded impact analysis.

### 2.3 Engineering quality
- 28-test regression suite; 84 % line coverage (gate: 80 %); 0 open defects.
- Permission matrix enforced server-side with negative tests for every rule.
- Privacy by design: contact details, claim proofs and finder contacts are stripped from API
  responses based on the viewer's relationship to the item.
- Static analysis clean after refactors; complexity within guidelines; presentation fully
  separated from the backend.

### 2.4 Known limitations (honest disclosure)
1. **Identity is email-string based** (no session tokens) — acceptable for the class demo,
   fully analysed in the W11 STRIDE model; token auth is the top v1.1 item.
2. Passwords use salted SHA-256 rather than a KDF; no login rate limiting.
3. `db.json` has no concurrent-write locking (single-process assumption).
4. Email/SMS notifications not implemented (CR-001 deferred).

### 2.5 Future work (v1.1)
Session tokens + login rate limiting → PBKDF2 password hashing → PostgreSQL migration
(schema ready) → SMTP notifications → admin dashboard for security posts → image content
sniffing → audit logging.

## 3. Reflection on the Process

**What went well**
- The incremental model matched the weekly deliverables perfectly; the system was runnable at
  the end of every week, which de-risked the demos.
- Writing tests alongside features caught the two highest-impact bugs (shared chat threads,
  missing permission check) before the demo, not after.
- Recording estimates in W3 and actuals in W8/W12 made the +8 % effort variance visible and
  explainable rather than a surprise.

**What went wrong and what I learned**
1. **Client-side assumptions about server data caused four separate blank-grid/leak incidents**
   (D-01/02/06/07). The lesson: the server decides what exists, the client renders what it is
   given — and every optional field must be guarded. I now write a render smoke test whenever
   a payload shape changes.
2. **The service worker fought me all project long** (stale UI). Fixing it properly
   (network-first + version bumps) cost an afternoon; shipping it broken cost several days of
   confusion. Measure caching behaviour early in any PWA project.
3. **A feature can be correct and still unusable** — finders could technically chat but the
   client guard bounced them. Integration testing from *each role's* perspective (not just the
   happy path) is what surfaced it.
4. **Privacy is a server concern, not a UI concern.** Hiding fields in the UI while the API
   still served them (found in review, D-04) would have been an embarrassing demo moment.

**Process assessment:** the MoSCoW backlog and the risk register earned their keep — R1
(scope creep) and R4 (stale UI) both materialised and both had prepared responses. If I
restarted tomorrow, I would add session-based auth from day one and write the privacy
projection before the first endpoint that returns items, not after.

## 4. Peer Assessment (template — complete with your group)

| Team member | Contribution | Reliability (1–5) | Quality (1–5) | Comments |
|-------------|--------------|-------------------|---------------|----------|
| Mathew Umama | System design, full-stack implementation, testing, documentation | 5 | 5 | Single-developer project — self-assessment |
| *(peer 1)* | *code review pass 1 (found R1–R4)* | | | |
| *(peer 2)* | *code review pass 2, demo audience feedback* | | | |

*(If the course requires reviewing others: rate their delivery against the agreed weekly
deliverables, whether their modules' tests passed on your machine, and how quickly review
findings were fixed.)*

## 5. Deliverable Checklist (Week 13)

- [x] Final demonstration script executed end-to-end (W8 script + moderation/security steps)
- [x] Final report (this document, §1–2)
- [x] Reflection (§3)
- [x] Peer assessment template (§4)
- [x] Complete documentation package W1–W13 in `docs/`
- [x] Repository with Git history and CI configuration
