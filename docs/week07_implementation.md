# Week 7 — Implementation I and Version Control (SP-014)

**Deliverables:** project set-up with a coding standard, working module 1, Git history. **Marks: 6**

## 1. How the project is laid out

I kept the structure deliberately boring — one backend file, one front-end folder, tests at
the root. Boring is findable at 11 pm before a demo.

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

Run it with `python -m uvicorn main:app --port 8000`; test it with
`python -m pytest test_main.py -q`.

## 2. My coding standard

I wrote this down as rules for myself, because with no teammates the only reviewer of my code
is future me — and future me at debugging time needs to recognise past me's intentions.

| Rule | Why I keep it |
|------|---------------|
| PEP 8 naming: `snake_case` for functions/variables, `PascalCase` for models (`ItemCreate`, `RejectClaimRequest`) | Python convention; no surprises for any reader |
| Every endpoint has a docstring stating its purpose **and its permission rule** | This one saved me repeatedly — the permission matrix stays visible at a glance |
| All user input passes the validation gate (`validate_contact_details`) or explicit length checks | One choke point for data quality, instead of checks scattered everywhere |
| All permission checks are server-side and explicit (`403` with a human-readable reason) | I learned this lesson the hard way: client-side hiding is cosmetic, not security |
| All mutations end with `save_state()` | The durability invariant — break this rule and a restart eats someone's report |
| Regex constants named in CAPS at module top (`PHONE_RE`, `EMAIL_RE`, `NAME_RE`, `MATRIC_RE`) | Single source of truth for validation; the HTML `pattern` attributes mirror them |
| No secrets in code; uploads get UUID filenames | Basic hygiene that prevents entire bug classes |
| Front-end: every user-supplied string passes `escapeHtml()` before rendering | XSS defence at the render boundary |
| Service worker cache name bumped on every front-end release (`afit-lf-vN`) | Exists purely because of the stale-UI incidents — see the risk register, R4 |

## 3. Module 1 — reporting and browse

Module 1 is the primary user flow, end to end. If this doesn't work, nothing else matters.

1. **Report creation** — `POST /api/items` (multipart): classification (lost/found), all
   fields, optional photo, the validation gate, the anti-spam limit, persistence.
2. **Browse** — `GET /api/items` with `item_type`, `category`, `location`, `status` and
   `search` filters, plus the privacy projection (`public_item`) applied per viewer.
3. **Front-end** — the report form with client-side validation patterns, the live
   duplicate-warning panel, the browse grid with badges, the search card, and a layout that
   actually works at phone width.

My definition of done for module 1, written before I started: a visitor can search; a signed-in
user can file both a lost and a found report; invalid input is rejected on *both* client and
server; data survives a restart; and the whole flow works on a phone-sized viewport. I checked
each of those five before calling it done.

## 4. Git history and branching

The repository is local Git on a `main` branch, with conventional-commit style messages:

```
9cefa6a SP-014: AFIT Lost & Found Portal - core system (FastAPI + PWA)
```

**The branching workflow I used** — each feature branch was merged to `main` only after that
module's tests passed:

| Branch | Purpose | Merged when |
|--------|---------|-------------|
| `feature/reporting` | report form, validation, browse grid | module 1 tests green |
| `feature/claims` | claim flow, confirm/reject, rejected-claimant ban | claim tests green |
| `feature/chat` | per-pair threads, unread dots | chat privacy tests green |
| `feature/moderation` | disputes, edit, mark-found, close | moderation tests green |
| `fix/privacy-sanitizer` | server-side field stripping | privacy tests green |
| `fix/upload-hardening` | UUID filenames, type/size checks | upload tests green |

Every merge went through the same checklist:

1. Tests pass locally (`pytest -q`).
2. New behaviour has at least one test — a positive case *and* a permission-negative case.
3. No endpoint changed its permission rule without updating the permission matrix in the docs.
4. The front-end cache version is bumped if `static/` changed.

Rule 2 is the one I'd keep if I kept nothing else. The permission-negative tests are what
caught the confirm-return hole later (week 9, finding R1).

## 5. Commit convention

`<type>: <summary>`, with types `feat`, `fix`, `test`, `docs`, `refactor`, `chore`. Example
from the actual history: `fix: confirm-return now requires the reporter email (403 otherwise)`.
Small, boring, greppable — which is the point.
