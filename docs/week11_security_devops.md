# Week 11 — Secure Development and DevOps (SP-014)

**Deliverables:** STRIDE threat model, OWASP Top 10 check, CI pipeline, deployed build. **Marks: 8**

## 1. STRIDE Threat Model

Assets: user passwords (hashes), personal contact details (email/phone/matric), item data,
chat messages, uploaded images, service availability.

| # | Threat (STRIDE) | Scenario | Existing control | Residual risk / plan |
|---|-----------------|----------|------------------|----------------------|
| S1 | **Spoofing** — acting as another user | Attacker submits `reporter_email` of a victim to delete/reject/mark-found, or reads a chat | Endpoints verify the email matches the item owner; chat resolves threads server-side | **High residual**: identity is a plain email string (no token). Documented accepted risk for v1.0; future work: session tokens issued at `/api/login`, required on mutating endpoints |
| S2 | **Spoofing** — brute-force sign-in | Automated password guessing on `/api/login` | Passwords salted+hashed; no lockout | Medium: add login rate limiting + PBKDF2/argon2 (future work) |
| T1 | **Tampering** — forged/oversized/malicious uploads | `../../evil.html` path traversal, 2 GB file, stored-XSS via HTML upload | UUID filenames, image-extension whitelist, 5 MB cap | Low residual: content-type sniffing (verify magic bytes) as future work |
| T2 | **Tampering** — editing another user's report | `PUT /api/items/{id}` with victim email | 403 unless email matches owner; only Active reports editable | Tied to S1 residual |
| R3 | **Repudiation** — "I never claimed that item" | Dispute over who claimed | Audit trail: `claim_details`, `disputes` (status + `resolved_at`), `resolved_via`, `rejected_claimants` | Low for v1.0 scope |
| I1 | **Information disclosure** — contact details exposed | Visitor scrapes emails/phones from the API | `public_item()` strips contact/claim/finder/rejected fields per viewer; disputes anonymised for non-reporters | Low for v1.0; TSL/HTTPS in production deployment |
| I2 | **Information disclosure** — chat eavesdropping | Outsider reads a private thread | Thread participants resolved server-side; 403 otherwise; unread endpoint excludes strangers | Tied to S1 residual |
| I3 | **Information disclosure** — user enumeration | `/api/login` 404 reveals an email exists | Present | Low: return uniform 401 (future work) |
| D1 | **Denial of service** — spam flooding | Thousands of reports/disputes/messages | Limits: 3 active portal lost reports per ID, 20 disputes/item, 20 finder responses/item, 200 messages/thread; validation gate | Medium: per-IP limits at reverse proxy in production |
| D2 | **Denial of service** — disk exhaustion via uploads | Many 5 MB uploads | 5 MB cap per file | Medium: total-quota monitoring in production |
| E1 | **Elevation of privilege** — code execution via upload/db.json | Crafted file executed server-side | Static files served, not executed; uploads validated; JSON store only written by the app | Low for v1.0 |

## 2. OWASP Top 10 Check (2021)

| Category | Status | Evidence |
|----------|--------|----------|
| A01 Broken Access Control | **Addressed (with S1 caveat)** | Every mutating endpoint checks ownership server-side; privacy projection strips data per viewer; negative tests assert 403s (T-03/05/06/08/16/19/21/22/23) |
| A02 Cryptographic Failures | **Partially** | Salted SHA-256 for passwords (not a KDF — documented); no secrets in code; HTTPS listed for production |
| A03 Injection | **Addressed** | No string-built SQL (file store; parameterised schema for the SQL upgrade); FastAPI/pydantic typing; no `eval`/shell calls |
| A04 Insecure Design | **Addressed** | Permission matrix designed up front; lost vs found flows separated; anti-spam limits designed in |
| A05 Security Misconfiguration | **Addressed** | No debug mode in deployment command; `.gitignore` excludes `db.json` and uploads; CORS not opened (same-origin) |
| A06 Vulnerable Components | **Monitored** | Pinned minimums in `requirements.txt`; deprecation warnings from TestClient tracked |
| A07 Identification & Authentication Failures | **Partially** | Password minimum length; salted hashes; no lockout/rate limit (documented future work) |
| A08 Software & Data Integrity | **Addressed** | State written atomically per mutation from a single process; uploads content-typed |
| A09 Logging & Monitoring Failures | **Partial** | Uvicorn access logs on; no audit log of admin actions (future work) |
| A10 SSRF | **Not applicable** | Server performs no outbound requests with user-supplied URLs (image URLs are fixed seeds) |

## 3. CI Pipeline (GitHub Actions)

`.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - name: Syntax checks
        run: |
          python -m py_compile main.py
          node --check static/app.js || true
      - name: Tests with coverage
        run: python -m pytest test_main.py --cov=main --cov-report=term -q
      - name: Coverage gate
        run: python -m pytest test_main.py --cov=main --cov-fail-under=80 -q
```

Every push runs the syntax checks and the full 28-test suite with an 80 % coverage gate —
the same gate the project passed locally (84 %).

## 4. Deployment (test environment)

- **Target:** campus-demo laptop + phone on the same Wi-Fi (test environment for v1.0).
- **Run:** `python -m uvicorn main:app --host 0.0.0.0 --port 8000` — reachable at
  `http://<laptop-ip>:8000` from the phone; the PWA installs to the home screen.
- **Production hardening checklist (documented for the final report):** run behind
  `nginx`/`caddy` with TLS, serve via `--workers 2` with the store moved to PostgreSQL
  (schema in W5 §6), add session tokens (S1), login rate limiting (S2), per-IP limits (D1).
- **Reset procedure for demos:** stop server → delete `db.json` → restart (seeds reload).
