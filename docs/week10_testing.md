# Week 10 — Software Testing (SP-014)

**Deliverables:** test plan, test cases, coverage report, defect log. **Marks: 8**

## 1. Test Plan

### 1.1 Scope
All backend behaviour of the AFIT Lost & Found Portal: reporting, validation, search, claims,
finder responses, chat, disputes, moderation, accounts, persistence and the permission matrix.
The front-end is covered indirectly through API-contract tests plus manual cross-browser/
mobile checks (documented in W8/W12).

### 1.2 Strategy
| Level | Tool | Focus |
|-------|------|-------|
| Unit / integration | pytest + FastAPI `TestClient` | endpoint behaviour, permission rules, validation, state transitions |
| Regression | full suite on every change | 28 tests must stay green |
| Coverage | pytest-cov | line coverage of `main.py`, target ≥ 80 % |
| Exploratory | manual | two-browser chat, phone viewport, restart persistence |

### 1.3 Entry / exit criteria
- Entry: feature code compiles; server imports cleanly.
- Exit: 28/28 tests pass; no high-severity open defects; coverage ≥ 80 %.

### 1.4 Test environment
Windows, Python 3.13, FastAPI/TestClient against a fresh in-process state (`db.json` removed
before each run so seeds are deterministic).

## 2. Test Cases (representative — the suite is the executable spec)

| ID | Test | Verifies | Result |
|----|------|----------|--------|
| T-01 | `test_read_root` | App serves the PWA shell | Pass |
| T-02 | `test_signup_and_login_workflow` | FR-11 accounts; password never stored in plain text | Pass |
| T-03 | `test_claim_then_confirm_return_workflow` | FR-5 lifecycle: Active → Claim Requested → Claimed/Returned; confirm is reporter-only | Pass |
| T-04 | `test_claim_blocked_once_already_requested` | FR-5 second claim while pending → 400 | Pass |
| T-05 | `test_reject_claim_returns_item_to_active` | FR-5/FR-6 reject → Active; rejected claimant → 403; others may still claim | Pass |
| T-06 | `test_only_reporter_can_delete` | FR-10 delete permission (stranger → 403) | Pass |
| T-07 | `test_dispute_flow` | FR-9 dispute recorded; reporter sees email; anonymous view strips email; empty message → 400 | Pass |
| T-08 | `test_reporter_can_resolve_disputes` | FR-9 uphold → claim rejected + item Active; stranger → 403; double-resolve → 400 | Pass |
| T-09 | `test_input_validation_rejects_nonsense` | FR-2 bad phone / matric / email / name → 400 with field-specific messages; valid data passes | Pass |
| T-10 | `test_lost_report_rate_limit` | FR-12 anti-spam: 3 portal lost reports, 4th → 429 | Pass |
| T-11 | `test_custom_location_and_category_accepted` | "Other (specify)" free-text values accepted | Pass |
| T-12 | `test_chat_is_private_to_reporter_and_claimant` | FR-8 claimant posts, both read, thread integrity | Pass |
| T-13 | `test_rejected_claimant_cannot_reclaim` | FR-6 repeat claim → 403 "rejected" | Pass |
| T-14 | `test_chat_unread_counts` | FR-8 unread counts per thread; strangers excluded | Pass |
| T-15 | `test_security_personnel_rules` | Found requires Report To; lost does not | Pass |
| T-16 | `test_finder_response_flow` | FR-7 self-response → 400; bad phone → 400; duplicate → 400; finder chat access; stranger → 403; **second finder has an independent thread** | Pass |
| T-17 | `test_similar_items_matching` | FR-4 token-overlap match; nonsense matches nothing | Pass |
| T-18 | `test_public_api_strips_private_fields` | FR-13 anonymous: no contact/claim/finder/rejected fields; reporter sees own contact | Pass |
| T-19 | `test_finder_and_claimant_private_endpoints` | `/finders` reporter-only; `/claim` claimant-only | Pass |
| T-20 | `test_upload_validation` | FR-2/NFR-3 non-image → 400; traversal filename neutralised (UUID name) | Pass |
| T-21 | `test_mark_found_by_owner` | FR-10 mark-found via finder credited ("Returned by …"); stranger → 403; double → 400 | Pass |
| T-22 | `test_close_report_by_owner` | FR-10 close; stranger → 403; double → 400 | Pass |
| T-23 | `test_reporter_can_edit_report` | FR-10 full edit incl. photo replace; stranger → 403; bad phone/date → 400 | Pass |

*(+5 further account/persistence tests — 28 total.)*

## 3. Coverage Report (measured)

```
$ python -m pytest test_main.py --cov=main -q
28 passed

Name      Stmts   Miss  Cover
-----------------------------
main.py     525     82    84%
TOTAL       525     82    84%
```

**84 % line coverage** (target ≥ 80 % met). The uncovered 16 % is dominated by:
- the static file/`FileResponse` plumbing and `uvicorn` startup path (exercised manually),
- defensive branches for malformed multipart input that TestClient cannot easily produce,
- the service worker (JavaScript, outside the Python coverage scope — syntax-checked instead).

## 4. Defect Log

| ID | Date found | Defect | Severity | Root cause | Fix | Status |
|----|-----------|--------|----------|-----------|-----|--------|
| D-01 | W8 testing | Message to one finder reached all finders (shared thread) | High | conversations keyed by item only | thread key `itemId:partnerEmail` + leak test | Closed |
| D-02 | W8 testing | Finders could not open chat ("private" alert) | High | client guard ignored finder responses | server-side `resolve_thread`; guard removed | Closed |
| D-03 | W8 review | `confirm-return` had no permission check | High | endpoint written before permission pass | reporter email required, 403 | Closed |
| D-04 | W8 review | API leaked contact/claim/finder data despite UI hiding | High | raw dicts returned | `public_item` sanitizer + tests | Closed |
| D-05 | W8 review | Upload path traversal via client filename | High | filename used raw | UUID + whitelist + size cap | Closed |
| D-06 | W9 regression | Item grid blank after sanitizer change (`escapeHtml(undefined)`) | High | render assumed fields always present | guards + smoke test of render path | Closed |
| D-07 | W9 regression | Second blank-grid incident (finder count / claim preview) | High | same root cause as D-06 | same fix class; lesson: every sanitized field guarded | Closed |
| D-08 | W9 testing | Rate limit blocked the demo reporter (6 seed lost items) | Medium | seeds counted toward the portal limit | limit applies to portal submissions only (`seeded` flag) | Closed |
| D-09 | W9 testing | Deleting an item left orphan chat threads | Medium | old integer key popped | prefix-based cleanup | Closed |
| D-10 | W1–W13 | Browser served stale UI after releases | Medium | service worker cache-first | network-first for page/app.js + version bump per release | Closed |

**Open defects: 0.** Recurring theme logged for the reflection (W13): client-side assumptions
about server payloads caused D-01/02/06/07 — the fix class was "server decides, client renders".
