# Week 9 — Implementation II, Refactoring and Code Quality (SP-014)

**Deliverables:** remaining modules, peer code-review log, refactoring record, static-analysis report. **Marks: 6**

## 1. Modules Completed After the Prototype (Implementation II)

| Module | Contents | Key endpoints / files |
|--------|----------|----------------------|
| Finder responses | "I Found This Item" flow for lost items, duplicate prevention, owner finder list | `POST /api/items/{id}/found-report`, `GET /api/items/{id}/finders` |
| Private chat | Per-pair threads (`itemId:partnerEmail`), 200-message cap, unread counts | `GET/POST /api/items/{id}/messages`, `GET /api/chat/unread` |
| Disputes | File / uphold / dismiss with audit trail | `POST /api/items/{id}/dispute`, `POST /api/items/{id}/disputes/{i}/resolve` |
| Moderation | Full report edit (multipart, photo replace), mark-found (with finder credit), close | `PUT /api/items/{id}`, `POST .../mark-found`, `POST .../close-report` |
| Accounts | Sign-up/sign-in, salted SHA-256, persisted user registry | `/api/signup`, `/api/login` |
| PWA | Manifest, icons, service worker (network-first for page/app.js, offline fallback) | `static/sw.js`, `static/manifest.webmanifest` |

## 2. Peer Code-Review Log

Reviews were held in two passes with a classmate acting as reviewer (checklist from W7 §4).

| # | Finding (reviewer) | Severity | Action taken |
|---|--------------------|----------|--------------|
| R1 | "Anyone can hit confirm-return — no reporter check" | High | Fixed: endpoint now requires `reporter_email`, 403 otherwise; test added |
| R2 | "Contact details still travel to the browser in the API response even though the UI hides them" | High | Fixed: `public_item()` viewer-based projection; 3 tests added |
| R3 | "Upload filename comes from the client — `../../` writes outside uploads" | High | Fixed: UUID filenames, extension whitelist, 5 MB cap; tests added |
| R4 | "Deleting an item leaves its chat threads in db.json" | Medium | Fixed: delete removes every `itemId:*` thread |
| R5 | "One conversation per item — a message to one finder reaches all finders" | High (found in testing) | Fixed: thread key redesigned to `itemId:partnerEmail`; leak test added |
| R6 | "Finders cannot open the chat — client guard only knows reporter/claimant" | High (found in testing) | Fixed: server-side thread resolution; client guard removed |
| R7 | "Card renderer crashes when contact fields are absent" (twice: contact line, finder count) | High | Fixed: all sanitized-field accesses guarded; render smoke test added |
| R8 | "SHA-256 is not a password KDF; no login rate limit" | Medium | **Accepted for v1.0**, documented in W11 threat model; PBKDF2 listed as future work |
| R9 | "Seed data contained values not selectable in the Report To dropdown" | Low | Fixed: seeds mapped to dropdown options; later personalised to the reporter |
| R10 | "Dead code: `ItemCreate` model unused" | Low | Removed |

## 3. Refactoring Record

| Refactor | Before | After | Why |
|----------|--------|-------|-----|
| UI extraction | all HTML/JS embedded in `main.py` (855 lines) | `static/index.html` + `static/app.js`; backend 375→~530 lines with later features, presentation fully separated | Maintainability; presentation/domain separation |
| Viewer projection | raw dicts returned to clients | `public_item()` single enforcement point | Privacy + SOLID (W6 §2) |
| Thread model | `conversations[item_id]` (shared per item) | `conversations["itemId:partnerEmail"]` | Correctness for multiple finders |
| Validation | ad-hoc checks scattered | `validate_contact_details` + named regex constants | Single choke point |
| Upload handling | client filename used raw | `save_image_upload()` (uuid, whitelist, size cap) | Security |
| Status transitions | implicit | explicit guards per endpoint with distinct 400/403 reasons | Testability, clear API contract |

## 4. Static Analysis Report

Tools: **pyflakes / py_compile** for Python, **node --check** for the front-end syntax,
plus manual complexity review.

```
$ python -m py_compile main.py && python -m pyflakes main.py
(main.py):1: 'typing.List' imported but unused      <- removed in cleanup
$ node --check static/app.js && node --check static/sw.js
(no output = syntax OK)
```

Findings and disposition:

| Tool output | Disposition |
|-------------|-------------|
| Unused imports (`List`, early `Depends`) | Removed |
| Two long functions (`create_item`, card renderer) | Reviewed: kept — linear form/route logic with early returns; splitting would obscure the permission sequence. Documented as accepted debt |
| No unused variables / redefinitions after cleanup | Clean |
| Deprecation warnings from test tooling (Starlette TestClient/httpx) | External library warning, tracked, no action for v1.0 |

**Complexity spot-check:** the highest-branch function is `public_item` (4 decision points,
cyclomatic complexity ≈ 5 — within the ≤ 10 guideline). The permission checks are sequential
guards, keeping nesting shallow (max depth 2).
