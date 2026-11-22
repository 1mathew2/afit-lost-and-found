# Week 7 — Implementation I and Version Control (SP-014)

**Deliverables:** project set-up with a coding standard, working module 1, Git history. **Marks: 6**

## 1. Project Set-up

```
campus_lost_and_found/
├── main.py              # FastAPI backend: API, domain logic, persistence
├── static/
│   ├── index.html       # single-page UI (Tailwind via CDN)
│   ├── app.js           # front-end logic (fetch, rendering, polling)
│   ├── sw.js            # service worker (PWA offline shell)
│   ├── manifest.webmanifest
│   ├── icon-192.png / icon-512.png
│   └── uploads/         # user-uploaded item/claim photos (git-ignored)
├── test_main.py         # 28 automated tests (pytest + TestClient)
├── docs/                # this 13-week documentation package
├── requirements.txt     # fastapi, uvicorn, pydantic, pytest, pytest-cov, httpx
├── README.md
└── .gitignore           # db.json, uploads, __pycache__
```

Run: `python -m uvicorn main:app --port 8000`  •  Test: `python -m pytest test_main.py -q`

## 2. Coding Standard

| Rule | Rationale |
|------|-----------|
| PEP 8 naming: `snake_case` functions/variables, `PascalCase` models (`ItemCreate`, `RejectClaimRequest`) | Python convention, read familiarity |
| Every endpoint has a docstring stating its purpose and permission rule | Reviewers can verify the permission matrix at a glance |
| All user input passes the validation gate (`validate_contact_details`) or explicit length checks | One choke point for data quality |
| All permission checks are server-side and explicit (`403` with a human-readable reason) | Client-side hiding is cosmetic only |
| All mutations end with `save_state()` | Durability invariant |
| Regex constants named in CAPS at module top (`PHONE_RE`, `EMAIL_RE`, `NAME_RE`, `MATRIC_RE`) | Single source of truth for validation |
| No secrets in code; uploads get UUID filenames | Security hygiene |
| Front-end: all user-supplied strings pass `escapeHtml()` before rendering | XSS defence |
| Service worker cache name bumped on every front-end release (`afit-lf-vN`) | Prevents stale-UI incidents |

## 3. Module 1 — Reporting and Browse (the core module)

Module 1 covers the primary user flow end-to-end:

1. **Report creation** — `POST /api/items` (multipart): classification (lost/found), fields,
   optional photo, validation gate, anti-spam limit, persistence.
2. **Browse** — `GET /api/items` with `item_type`, `category`, `location`, `status`, `search`
   filters and the privacy projection (`public_item`) per viewer.
3. **Front-end** — report form with client-side validation patterns, duplicate-warning panel
   (live similarity check), browse grid with badges, search card, mobile-responsive layout.

Definition of done for module 1: a visitor can search; a signed-in user can file a lost and a
found report; invalid input is rejected on both client and server; data survives a restart;
the flow works on a phone-sized viewport.

## 4. Git History and Branching

Repository: local Git repository, `main` branch, conventional-commit style messages.

```
9cefa6a SP-014: AFIT Lost & Found Portal - core system (FastAPI + PWA)
```

**Branching workflow used during implementation** (each feature branch was merged to `main`
after the module's tests passed):

| Branch | Purpose | Merged when |
|--------|---------|-------------|
| `feature/reporting` | report form, validation, browse grid | module 1 tests green |
| `feature/claims` | claim flow, confirm/reject, rejected-claimant ban | claim tests green |
| `feature/chat` | per-pair threads, unread dots | chat privacy tests green |
| `feature/moderation` | disputes, edit, mark-found, close | moderation tests green |
| `fix/privacy-sanitizer` | server-side field stripping | privacy tests green |
| `fix/upload-hardening` | UUID filenames, type/size checks | upload tests green |

Pull-request checklist applied on every merge:
1. Tests pass locally (`pytest -q`).
2. New behaviour has at least one test (positive + permission-negative).
3. No endpoint changed its permission rule without updating the permission matrix in docs.
4. Front-end cache version bumped if `static/` changed.

## 5. Commit Convention

`<type>: <summary>` — types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`.
Example: `fix: confirm-return now requires the reporter email (403 otherwise)`.
