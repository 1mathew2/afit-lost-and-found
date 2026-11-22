# Week 13 — Final Report, Reflection and Peer Assessment (SP-014)

**Deliverables:** final demonstration, final report, reflection, peer assessment. **Marks: 16**

## 1. The final demonstration

The final demo runs the complete lifecycle end to end — the week-8 script, extended with the
moderation and security steps. What the delivered system can do:

| Capability | Status |
|-----------|--------|
| Lost + found reporting with photos, validation, duplicate warnings | ✔ |
| Search/filter/browse, responsive mobile + desktop, installable PWA with an offline shell | ✔ |
| Claim & verify ownership with confirm/reject and a rejected-claimant ban | ✔ |
| Lightweight finder responses for lost items with owner moderation | ✔ |
| Private per-pair chat with unread indicators | ✔ |
| Disputes with an uphold/dismiss audit trail | ✔ |
| Full report editing (incl. photo), mark-as-found, close, delete | ✔ |
| Accounts (salted+hashed passwords), persistence across restarts | ✔ |
| Server-enforced permissions and a privacy projection | ✔ |
| Anti-spam limits and an input validation gate | ✔ |
| 28 automated tests, 84 % coverage, a CI pipeline | ✔ |

## 2. Final report

### 2.1 Summary
The AFIT Lost & Found Portal replaces notice boards and WhatsApp threads with one searchable
system. I built it incrementally over the 13 weeks: a working report-search-claim core by
week 7, a full prototype demo (with chat and disputes already in, ahead of schedule) at
week 8, feature completion in week 9, then dedicated weeks for testing, security hardening
and documentation. What ships is a real, deployable FastAPI + PWA application with a
file-persistence layer designed so the PostgreSQL migration is a transcription, not a
redesign.

### 2.2 Requirements outcome
All 14 functional requirements and 8 non-functional requirements in scope were delivered
(weeks 2 and 12). One change request (CR-001, notifications) was processed and partially
delivered via the in-app indicators; the email/SMS variant was deferred with a recorded
impact analysis rather than implemented on a whim.

### 2.3 Engineering quality
- A 28-test regression suite; 84 % line coverage against an 80 % gate; **zero open defects**.
- The permission matrix is enforced server-side, with negative tests asserting every rule.
- Privacy by design: contact details, claim proofs and finder contacts are stripped from API
  responses based on the viewer's relationship to the item.
- Static analysis clean after the refactors; complexity within guidelines; presentation fully
  separated from the backend.

### 2.4 Known limitations — stated plainly
I'd rather an examiner hear these from me than find them:

1. **Identity is email-string based** (no session tokens). Acceptable for the class demo and
   fully analysed in the week-11 STRIDE model; token auth is the first v1.1 item.
2. Passwords use salted SHA-256 rather than a proper KDF, and there's no login rate limiting.
3. `db.json` has no concurrent-write locking — the single-process assumption.
4. Email/SMS notifications are not implemented (CR-001, deferred with an alternative shipped).

### 2.5 Future work (v1.1)
Session tokens + login rate limiting → PBKDF2 password hashing → the PostgreSQL migration
(schema ready) → SMTP notifications → an admin dashboard for security posts → image content
sniffing → audit logging.

## 3. Reflection

### What went well
- The incremental model matched the weekly deliverables so well that it almost felt like
  cheating. The system was runnable at the end of every single week, which de-risked both
  demos enormously — I was never "hoping it works by Friday".
- Writing tests alongside features caught the two highest-impact bugs (the shared chat thread,
  the missing permission check) *before* the demo, not after. That alone justified the time.
- Recording estimates in week 3 and actuals in weeks 8 and 12 made the +8 % effort variance a
  visible, explainable number instead of a vague feeling of being behind.

### What went wrong, and what it taught me
1. **Client-side assumptions about server data caused four separate incidents** — the shared
   thread (D-01), the finder chat lockout (D-02), and two blank-grid crashes (D-06, D-07).
   The lesson I've actually internalised: the server decides what exists; the client renders
   what it's given; and *every* optional field gets guarded. I now write a render smoke test
   whenever a payload shape changes, because I've paid for not doing it twice.
2. **The service worker fought me the whole project.** Stale UI after every release, several
   days of confusion before I understood what was happening. Fixing it properly
   (network-first + version bumps) cost one afternoon. The asymmetry is the lesson: measure
   your caching behaviour early in any PWA project.
3. **A feature can be correct and still unusable.** Finders could technically chat, but the
   client guard bounced them with "this chat is private". Integration testing from *each
   role's* perspective — not just the happy path — is what surfaced it.
4. **Privacy is a server concern, not a UI concern.** Hiding fields in the interface while the
   API cheerfully served them to anyone (D-04, caught in review) would have been an
   embarrassing moment in front of an audience. The sanitizer now enforces it at the source.

### My process assessment
The MoSCoW backlog and the risk register both earned their keep. R1 (scope creep) and R4
(stale UI) from the week-3 register both materialised, and both had prepared responses waiting
— which is the difference between a risk register and a wish list. If I restarted tomorrow I
would change two things: session-based auth from day one, and the privacy projection written
*before* the first endpoint that returns items, not after the review found the hole.

## 4. Peer assessment

| Team member | Contribution | Reliability (1–5) | Quality (1–5) | Comments |
|-------------|--------------|-------------------|---------------|----------|
| Mathew Umama | System design, full-stack implementation, testing, documentation | 5 | 5 | Single-developer project — self-assessment |
| *(peer 1)* | *code review pass 1 (findings R1–R4)* | | | |
| *(peer 2)* | *code review pass 2, demo audience feedback* | | | |

*(If the course requires reviewing others, my criteria would be: did they deliver against the
agreed weekly deliverables, did their modules' tests pass on my machine, and how quickly did
they fix review findings?)*

## 5. Week-13 checklist

- [x] Final demonstration script executed end to end (the W8 script + moderation/security steps)
- [x] Final report (§1–2)
- [x] Reflection (§3)
- [x] Peer assessment template (§4)
- [x] Complete documentation package W1–W13 in `docs/`
- [x] Repository with Git history and CI configuration
