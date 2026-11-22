# Week 9 — Implementation II, Refactoring and Code Quality (SP-014)

**Deliverables:** remaining modules, peer code-review log, refactoring record, static-analysis report. **Marks: 6**

## 1. What I built after the prototype

| Module | What it does | Key endpoints / files |
|--------|--------------|----------------------|
| Finder responses | The "I Found This Item" flow for lost items, duplicate prevention, the owner's finder list | `POST /api/items/{id}/found-report`, `GET /api/items/{id}/finders` |
| Private chat | Per-pair threads (`itemId:partnerEmail`), 200-message cap, unread counts | `GET/POST /api/items/{id}/messages`, `GET /api/chat/unread` |
| Disputes | File / uphold / dismiss, with an audit trail | `POST /api/items/{id}/dispute`, `POST /api/items/{id}/disputes/{i}/resolve` |
| Moderation | Full report edit (multipart, photo replacement), mark-found (with finder credit), close | `PUT /api/items/{id}`, `POST .../mark-found`, `POST .../close-report` |
| Accounts | Sign-up/sign-in, salted SHA-256, persisted user registry | `/api/signup`, `/api/login` |
| PWA | Manifest, icons, service worker (network-first for page/app.js, offline fallback) | `static/sw.js`, `static/manifest.webmanifest` |

## 2. The code-review log

I had a classmate review the code in two passes against the week-7 checklist. I'm logging
every finding — including the ones that stung — because the stinging ones were the valuable
ones.

| # | Finding | Severity | What I did |
|---|---------|----------|-----------|
| R1 | "Anyone can hit confirm-return — no reporter check" | High | Fixed: the endpoint now requires `reporter_email`, 403 otherwise; test added |
| R2 | "Contact details still travel to the browser in the API response even though the UI hides them" | High | Fixed: `public_item()` viewer-based projection; 3 tests added |
| R3 | "Upload filename comes from the client — `../../` writes outside uploads" | High | Fixed: UUID filenames, extension whitelist, 5 MB cap; tests added |
| R4 | "Deleting an item leaves its chat threads in db.json" | Medium | Fixed: delete removes every `itemId:*` thread |
| R5 | "One conversation per item — a message to one finder reaches all finders" | High (found in my own testing) | Fixed: thread key redesigned to `itemId:partnerEmail`; leak test added |
| R6 | "Finders cannot open the chat — the client guard only knows reporter/claimant" | High (found in my own testing) | Fixed: server-side thread resolution; the client guard removed |
| R7 | "Card renderer crashes when contact fields are absent" (this happened twice) | High | Fixed: all sanitized-field accesses guarded; render smoke test added |
| R8 | "SHA-256 is not a password KDF; no login rate limit" | Medium | **Accepted for v1.0**, documented in the W11 threat model; PBKDF2 listed as future work |
| R9 | "Seed data contained values not selectable in the Report To dropdown" | Low | Fixed: seeds mapped to dropdown options; later personalised to the reporter |
| R10 | "Dead code: `ItemCreate` model unused" | Low | Removed |

The pattern in R5–R7 is worth naming: they weren't logic errors, they were *assumption
mismatches* between what the client believed the server would send and what the server
actually sends. That pattern recurs in the defect log and shaped my reflection in week 13.

## 3. The refactoring record

| Refactor | Before | After | Why |
|----------|--------|-------|-----|
| UI extraction | all HTML/JS embedded in `main.py` (855 lines) | `static/index.html` + `static/app.js`; presentation fully separated | Maintainability; the presentation/domain split I claimed in week 5, made real |
| Viewer projection | raw dicts returned to clients | `public_item()` as the single enforcement point | Privacy, plus the SOLID analysis in week 6 |
| Thread model | `conversations[item_id]` (shared per item) | `conversations["itemId:partnerEmail"]` | Correctness for multiple finders |
| Validation | ad-hoc checks scattered | `validate_contact_details` + named regex constants | A single choke point |
| Upload handling | client filename used raw | `save_image_upload()` (uuid, whitelist, size cap) | Security |
| Status transitions | implicit | explicit guards per endpoint with distinct 400/403 reasons | Testability; a clear API contract |

The UI extraction was the biggest one and I nearly didn't do it — the embedded version
"worked". But every later feature cost roughly double while the UI lived inside the backend
file, and after extracting it the cost dropped back to normal. Lesson logged for the
reflection: refactor *before* the pain, not after.

## 4. Static analysis

Tools: **pyflakes / py_compile** for Python, **node --check** for front-end syntax, plus a
manual complexity review.

```
$ python -m py_compile main.py && python -m pyflakes main.py
(main.py):1: 'typing.List' imported but unused      <- removed in cleanup
$ node --check static/app.js && node --check static/sw.js
(no output = syntax OK)
```

What I did with the findings:

| Tool output | Disposition |
|-------------|-------------|
| Unused imports (`List`, an early `Depends`) | Removed |
| Two long functions (`create_item`, the card renderer) | Reviewed and *kept* — they're linear form/route logic with early returns; splitting them would obscure the permission sequence. Documented as accepted debt |
| No unused variables or redefinitions after cleanup | Clean |
| Deprecation warnings from test tooling (Starlette TestClient/httpx) | External library warning, tracked, no action for v1.0 |

**Complexity spot-check:** the highest-branch function is `public_item` at 4 decision points
(cyclomatic complexity ≈ 5) — comfortably inside the ≤ 10 guideline. The permission checks are
sequential guards, so nesting never goes deeper than 2.
