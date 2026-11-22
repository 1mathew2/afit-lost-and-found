# Week 3 — Requirements Validation, Planning and Risk Register (SP-014)

**Deliverables:** MoSCoW backlog, effort estimates, 13-week schedule, risk register. **Marks: 6**

## 1. Validating my own requirements

Writing requirements is easy; checking them is the part that actually pays. I took each Week-2
requirement through four questions: is it unambiguous? can I test it? can I realistically
build it in 13 weeks alone? and is it genuinely needed for v1.0?

Two requirements failed the check and I changed them:

- My first draft had "real-time notifications by email". It sounded great until I asked myself
  where the mail server was coming from. I don't have one, and signing up for an external
  service mid-project for a class demo is a liability. I downgraded it to in-app unread
  indicators and logged the change properly (it reappears as a formal change request in
  week 12).
- I had also sketched an "admin dashboard for security staff". Honest answer: nice to have,
  nowhere near critical path, and it would have eaten a week I didn't have. Deferred to a
  future version.

Catching both of these in week 3 instead of week 8 is exactly what this exercise was for.

## 2. MoSCoW prioritisation

| Priority | Requirements |
|----------|-------------|
| **Must have** | FR-1 reporting, FR-2 validation, FR-3 search/filter, FR-5 claim flow, FR-10 moderation (delete/confirm/reject), FR-11 accounts, FR-14 persistence |
| **Should have** | FR-6 rejected-claimant ban, FR-7 finder responses, FR-8 private chat, FR-9 disputes, FR-13 contact gating, FR-12 anti-spam |
| **Could have** | FR-4 duplicate warning, unread dots, PWA install/offline shell, photo replacement in edit |
| **Won't have (v1.0)** | Email/SMS notifications, admin dashboard, payment/rewards, multi-campus |

The "Won't have" list turned out to be the most useful row of the whole table. Twice during
the project I reached for something on it, and twice having it written down stopped me.

## 3. Effort estimates

I estimated these the way we were taught — per feature, in focused person-hours — and I've
kept the actuals beside them so the comparison is on the record:

| Item | Estimate | Actual |
|------|----------|--------|
| Reporting + validation | 6 h | 7 h (validation ended up needing both client and server passes) |
| Browse/search/filter UI | 4 h | 3 h |
| Claim + confirm/reject flow | 6 h | 6 h |
| Finder responses + per-pair chat | 8 h | 10 h (the thread design needed a redo — see week 10) |
| Disputes + resolution | 4 h | 4 h |
| Accounts + persistence | 4 h | 4 h |
| PWA + polish | 4 h | 5 h |
| Test suite + hardening | 6 h | 7 h |
| Documentation package | 8 h | 8 h |
| **Total** | **50 h** | **54 h** |

About 8% over. The two overruns (validation, chat threads) were both cases where I
underestimated how much *correctness* work hides behind a feature that looks simple.

## 4. The backlog, in the order I intended to build it

1. Project skeleton + static serving (W1)
2. Report form + validation + browse grid + search (W2–W3)
3. Claim flow with confirm/reject (W4–W6)
4. Accounts, persistence, anti-spam (W6–W7)
5. **Prototype demo** (W8) — items 1–4
6. Finder responses + private chat + unread dots (W9)
7. Disputes + resolution + moderation — edit, mark-found, close (W9)
8. Test suite, coverage, hardening (W10)
9. Security fixes (privacy sanitizer, upload hardening, confirm-return auth) + CI (W11)
10. Change request processing, user manual, metrics (W12)
11. Final report + reflection (W13)

## 5. The 13-week schedule

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

In practice I ran ahead of this — chat, disputes and moderation were done before the week-8
demo rather than after. That headroom got spent on testing and security, which I think was
the right trade.

## 6. Risk register

I scored probability and impact on L=1 / M=2 / H=3 and multiplied. Anything scoring 6 or
above got an active mitigation, not just a note.

| ID | Risk | P | I | Score | Mitigation / response |
|----|------|---|---|-------|----------------------|
| R1 | Scope creep | H | H | 9 | MoSCoW backlog; the "Won't have" list is binding; changes go through the W12 process |
| R2 | Data loss (file-based store) | M | H | 6 | `db.json` written on every mutation; documented demo-day reset procedure |
| R3 | Identity spoofing (email-only auth) | H | M | 6 | Accepted for v1.0 and analysed openly in the W11 threat model; token auth is future work |
| R4 | Browser serves stale UI (service worker) | H | M | 6 | Network-first service worker, cache version bumped per release, Ctrl+Shift+R as the fallback |
| R5 | Spam/abuse of open reporting | M | M | 4 | Limits: 3 active lost reports, 20 disputes/responses per item, 200 messages per chat |
| R6 | Upload abuse (huge/malicious files) | M | H | 6 | Image-only whitelist, 5 MB cap, UUID filenames (W11) |
| R7 | Single-developer illness/absence | M | H | 6 | Weekly increments keep the system runnable at every week-end; docs kept current as I go |
| R8 | Demo-day environment failure | L | H | 4 | Local server script, offline PWA shell, seed data reproducible from code |
| R9 | Privacy complaint (contact exposure) | M | M | 4 | Server-side field stripping by viewer (W11); contact shown only to involved parties |

Worth saying out loud: R1 and R4 both actually happened. Scope creep knocked twice and the
"Won't have" list held; the stale-service-worker problem cost me several confusing days until
I fixed it properly. A risk register isn't decoration — the two risks I took most seriously
were the two that showed up.
