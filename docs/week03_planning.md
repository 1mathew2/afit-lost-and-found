# Week 3 — Requirements Validation, Planning and Risk Register (SP-014)

**Deliverables:** MoSCoW backlog, effort estimates, 13-week schedule, risk register. **Marks: 6**

## 1. Requirements Validation

Each Week-2 requirement was checked against the four validation tests (unambiguous, testable,
feasible in the timeframe, necessary for v1.0). Two early drafts were changed as a result:

- "Real-time notifications by email" → downgraded to in-app unread indicators (no mail server
  available; NFR constraint). Recorded as a change request in Week 12.
- "Admin dashboard for security staff" → deferred to a future version (out of v1.0 scope).

## 2. MoSCoW Prioritisation

| Priority | Requirements |
|----------|-------------|
| **Must have** | FR-1 reporting, FR-2 validation, FR-3 search/filter, FR-5 claim flow, FR-10 moderation (delete/confirm/reject), FR-11 accounts, FR-14 persistence |
| **Should have** | FR-6 rejected-claimant ban, FR-7 finder responses, FR-8 private chat, FR-9 disputes, FR-13 contact gating, FR-12 anti-spam |
| **Could have** | FR-4 duplicate warning, unread dots, PWA install/offline shell, photo replacement in edit |
| **Won't have (v1.0)** | Email/SMS notifications, admin dashboard, payment/rewards, multi-campus |

## 3. Effort Estimates (planning poker, person-hours)

| Item | Estimate | Actual (recorded W8/W13) |
|------|----------|--------------------------|
| Reporting + validation | 6 h | 7 h (validation added twice: client + server) |
| Browse/search/filter UI | 4 h | 3 h |
| Claim + confirm/reject flow | 6 h | 6 h |
| Finder responses + per-pair chat | 8 h | 10 h (thread-key redesign) |
| Disputes + resolution | 4 h | 4 h |
| Accounts + persistence | 4 h | 4 h |
| PWA + polish | 4 h | 5 h |
| Test suite + hardening | 6 h | 7 h |
| Documentation package | 8 h | 8 h |
| **Total** | **50 h** | **54 h** |

## 4. Backlog (incremental order)

1. Project skeleton + static serving (W1)
2. Report form + validation + browse grid + search (W2–W3 build)
3. Claim flow with confirm/reject (W4–W6 build)
4. Accounts, persistence, anti-spam (W6–W7 build)
5. **Prototype demo** (W8) — items 1–4
6. Finder responses + private chat + unread dots (W9)
7. Disputes + resolution + moderation (edit/mark-found/close) (W9)
8. Test suite, coverage, hardening (W10)
9. Security fixes (privacy sanitizer, upload hardening, confirm-return auth) + CI (W11)
10. Change request processing, user manual, metrics (W12)
11. Final report + reflection (W13)

## 5. 13-Week Schedule

| Week | Milestone | Deliverable due |
|------|-----------|-----------------|
| 1 | Proposal approved | Proposal, process model, repo |
| 2 | Requirements agreed | SRS §1–3, user stories |
| 3 | Plan baselined | Backlog, schedule, risk register |
| 4 | Model agreed | UML set |
| 5 | Architecture frozen | Architecture doc, ERD, schema |
| 6 | Design patterns applied | Patterns note, wireframes |
| 7 | Module 1 working | Reporting module, Git history |
| 8 | **Prototype demo** | Live demo, progress report |
| 9 | Feature complete | Chat, disputes, moderation |
| 10 | Test suite green | Test plan, coverage, defect log |
| 11 | Hardened + deployed | Threat model, CI, deployed build |
| 12 | Docs complete | Change request, manual, metrics |
| 13 | **Final demo** | Final report, reflection, peer review |

## 6. Risk Register

| ID | Risk | P | I | Score | Mitigation / Response |
|----|------|---|---|-------|----------------------|
| R1 | Scope creep (features beyond 13 weeks) | H | H | 9 | MoSCoW backlog; "Won't have" list enforced; change requests go through W12 process |
| R2 | Data loss (file-based store) | M | H | 6 | `db.json` written on every mutation; demo-day reset procedure documented |
| R3 | Identity spoofing (email-only auth) | H | M | 6 | Accepted for v1.0 class demo; documented in W11 threat model; token upgrade listed as future work |
| R4 | Browser serves stale UI (service worker) | H | M | 6 | Network-first SW for page/app.js; cache bumped per release; Ctrl+Shift+R fallback |
| R5 | Spam/abuse of open reporting | M | M | 4 | Rate limits: 3 active lost reports, 20 disputes/responses per item, 200 messages per chat |
| R6 | Upload abuse (huge/malicious files) | M | H | 6 | Image-only whitelist, 5 MB cap, UUID filenames (W11) |
| R7 | Single-developer illness/absence | M | H | 6 | Weekly increments keep system runnable at every week-end; docs kept current |
| R8 | Demo-day environment failure | L | H | 4 | Local server script, offline PWA shell, seed data reproducible from code |
| R9 | Privacy complaint (contact exposure) | M | M | 4 | Server-side field stripping by viewer (W11); contact shown only to involved parties |

Scoring: P (probability) and I (impact) ∈ {L=1, M=2, H=3}; Score = P × I. Risks ≥ 6 are
actively mitigated; R1 and R4 materialised during the project and their mitigations were applied.
