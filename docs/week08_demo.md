# Week 8 — Mid-Semester Review: Prototype Demo (SP-014)

**Deliverables:** live demo covering the main user flow, progress report, backlog update. **Marks: 10**

## 1. Demo Script (7 minutes, main user flow)

**Setup before the demo:** `python -m uvicorn main:app --port 8000` → http://localhost:8000;
hard-refresh (Ctrl+Shift+R); database reset to the 11 seed items (all reported by
Mathew Umama, U23CS1067, 1mathewumama@gmail.com).

| # | Action | What it shows |
|---|--------|---------------|
| 1 | Open the portal on the laptop **and** on the phone (same Wi-Fi) | Responsive PWA, installable, institutional design |
| 2 | Browse as a visitor: search "laptop", filter Found + Library | FR-3 search/filter; contact details hidden (FR-13) |
| 3 | Sign in (or sign up with a second email) | FR-11 accounts |
| 4 | Report a **found** item: fill the form, show the live duplicate warning, pick "Report To: Student", upload a photo | FR-1, FR-2 validation, FR-4 duplicate warning, custody |
| 5 | Try an invalid phone ("abcdefghijk") first | Server + client validation with clear messages |
| 6 | As a second user, **claim** the found item: fill proof questions | FR-5 claim flow; status → Claim Requested |
| 7 | Show the chat: claimant sends a message; owner sees the red unread dot and replies | FR-8 private chat, unread indicators |
| 8 | As the owner, **Confirm Return** | Status → Claimed/Returned |
| 9 | On a **lost** seed item (HP laptop): click "I Found This Item" as the second user; owner opens View → finder list → chat with one finder → Confirm Return via This Finder | FR-7 finder responses, per-pair threads |
| 10 | Show the dispute flow on a claimed item: third party files dispute; owner upholds → claim rejected, claimant banned from re-claiming | FR-9, FR-6 |
| 11 | Edit a report (change location + photo), then Mark as Found / Close | FR-10 moderation |
| 12 | Reload the page: everything persisted | FR-14 |

**Fallback if Wi-Fi fails:** the PWA shell renders offline from the service worker cache and
the demo runs on localhost.

## 2. Progress Report Against the Plan (end of Week 8)

| Planned (W3 schedule) | Status | Evidence |
|-----------------------|--------|----------|
| Reporting + validation (items 1–2) | **Done** | `POST /api/items`, validation gate, rate limits |
| Browse/search/filter | **Done** | `GET /api/items` filters; search card UI |
| Claim + confirm/reject | **Done** | Claim endpoints + status lifecycle tests |
| Accounts + persistence | **Done** | `/api/signup`, `/api/login`, salted SHA-256, `db.json` |
| Prototype demo (item 5) | **Done** | this document |
| Chat, disputes, moderation (planned W9) | **Ahead of schedule** | already implemented and tested |
| Test suite (planned W10) | **Ahead** | 28 tests passing at W8 |

**Schedule variance:** +1 week ahead on features; effort 30 h actual vs 28 h planned at this
point (validation and chat-thread redesign took longer, offset by UI work being faster).

## 3. Backlog Update After the Demo

| Item | Change |
|------|--------|
| Finder responses + per-pair chat | **Done** (pulled forward from W9) — thread key redesigned to `itemId:partnerEmail` after the shared-thread bug |
| Disputes + resolution | **Done** (pulled forward) |
| Edit report / mark-found / close | **Done** (pulled forward) |
| Privacy sanitizer + upload hardening + confirm-return auth | **Added** (from the W8 code review) — scheduled W11 |
| Coverage measurement + defect log | **Added** — W10 |
| CI pipeline + deployment | Unchanged — W11 |
| Change request: email notifications | **Added** — W12 (impact analysis: out of v1.0, in-app indicators remain) |
| Email/SMS notifications | **Stays "Won't have"** for v1.0 |

## 4. Demo Feedback Captured

1. "Can the finder and the owner talk?" → chat already existed; promoted to a headline demo item.
2. "What stops someone claiming everything?" → anti-spam + rejected-claimant ban + disputes;
   demonstrated in step 10.
3. "Will it work on my phone?" → PWA install demonstrated in step 1.
