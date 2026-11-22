# Week 8 — Mid-Semester Review: Prototype Demo (SP-014)

**Deliverables:** live demo covering the main user flow, progress report, backlog update. **Marks: 10**

## 1. The demo script

This is the script I actually follow when demonstrating — timed at about 7 minutes for the
main flow.

**Before starting:** `python -m uvicorn main:app --port 8000` → http://localhost:8000;
hard-refresh (Ctrl+Shift+R); database reset to the 11 seed items (all reported by Mathew
Umama, U23CS1067, 1mathewumama@gmail.com). A clean state matters — a half-tested item on
screen derails the story.

| # | Action | What it demonstrates |
|---|--------|----------------------|
| 1 | Open the portal on the laptop **and** on a phone (same Wi-Fi) | Responsive PWA, installable, institutional design |
| 2 | Browse as a visitor: search "laptop", filter Found + Library | FR-3 search/filter; contact details hidden (FR-13) |
| 3 | Sign in (or sign up with a second email) | FR-11 accounts |
| 4 | Report a **found** item: fill the form, show the live duplicate warning, pick "Report To: Student", upload a photo | FR-1, FR-2 validation, FR-4 duplicate warning, custody |
| 5 | First try an invalid phone ("abcdefghijk") | Server *and* client validation with clear messages |
| 6 | As a second user, **claim** the found item: fill the proof questions | FR-5 claim flow; status → Claim Requested |
| 7 | Show the chat: claimant sends a message; owner sees the red unread dot and replies | FR-8 private chat, unread indicators |
| 8 | As the owner, **Confirm Return** | Status → Claimed/Returned |
| 9 | On a **lost** seed item (HP laptop): click "I Found This Item" as the second user; owner opens View → finder list → chat with one finder → Confirm Return via This Finder | FR-7 finder responses, per-pair threads |
| 10 | Show the dispute flow on a claimed item: third party files a dispute; owner upholds → claim rejected, claimant banned from re-claiming | FR-9, FR-6 |
| 11 | Edit a report (change location + photo), then Mark as Found / Close | FR-10 moderation |
| 12 | Reload the page: everything persisted | FR-14 |

Step 5 is deliberate — showing the *rejection* first makes the validation believable. A demo
where everything works on the first try looks scripted; one where the system catches a bad
input looks real, because it is.

**Fallback if the Wi-Fi fails:** the PWA shell renders offline from the service worker cache
and the whole demo runs on localhost. I rehearsed this path too.

## 2. Progress against the plan (end of week 8)

| Planned (W3 schedule) | Status | Evidence |
|-----------------------|--------|----------|
| Reporting + validation (items 1–2) | **Done** | `POST /api/items`, validation gate, rate limits |
| Browse/search/filter | **Done** | `GET /api/items` filters; search card UI |
| Claim + confirm/reject | **Done** | Claim endpoints + status lifecycle tests |
| Accounts + persistence | **Done** | `/api/signup`, `/api/login`, salted SHA-256, `db.json` |
| Prototype demo (item 5) | **Done** | this document |
| Chat, disputes, moderation (planned W9) | **Ahead of schedule** | already implemented and tested |
| Test suite (planned W10) | **Ahead** | 28 tests passing at W8 |

Honest accounting of the variance: I'm about a week ahead on features. Effort to date is
roughly 30 hours against 28 planned. Validation took longer than I estimated (it needed both
a client and a server pass), and the chat thread redesign cost me two extra hours — but the UI
work went faster than planned, which absorbed most of it.

## 3. Backlog update after the demo

| Item | Change |
|------|--------|
| Finder responses + per-pair chat | **Done** (pulled forward from W9) — thread key redesigned after the shared-thread bug |
| Disputes + resolution | **Done** (pulled forward) |
| Edit report / mark-found / close | **Done** (pulled forward) |
| Privacy sanitizer + upload hardening + confirm-return auth | **Added** (from the W8 code review) — scheduled W11 |
| Coverage measurement + defect log | **Added** — W10 |
| CI pipeline + deployment | Unchanged — W11 |
| Change request: email notifications | **Added** — W12 (impact analysis: out of v1.0, in-app indicators remain) |
| Email/SMS notifications | **Stays "Won't have"** for v1.0 |

The three "added" rows all came from actually using and reviewing the system during demo
preparation — which is exactly what the mid-semester checkpoint is supposed to force.

## 4. Feedback from the demo audience

I demoed to classmates and wrote down what they asked, because questions are requirements in
disguise:

1. *"Can the finder and the owner talk?"* — chat already existed; I promoted it to a headline
   demo item.
2. *"What stops someone claiming everything?"* — anti-spam + the rejected-claimant ban +
   disputes; I demonstrated all three in step 10.
3. *"Will it work on my phone?"* — the PWA install, demonstrated in step 1.

All three questions were answerable from the system itself. That felt like the milestone
working as intended.
