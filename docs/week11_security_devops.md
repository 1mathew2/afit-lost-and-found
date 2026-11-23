# Week 11 — Secure Development and DevOps (SP-014)

**Deliverables:** STRIDE threat model, OWASP Top 10 check, CI pipeline, deployed build. **Marks: 8**

## 1. Threat model — what I'm protecting, and from whom

Before the STRIDE table, the assets, because threats only mean something relative to what's
worth stealing or breaking: **user passwords** (hashed), **personal contact details** (emails,
phones, matric numbers), **item data**, **chat messages**, **uploaded images**, and the
**service's availability** during demos.

The honest headline: the biggest weakness in this system is that identity is a plain email
string. I knew that going in, I've documented it in every week where it mattered, and I'd
rather analyse it openly than pretend it isn't there.

| # | Threat (STRIDE) | Scenario | Existing control | Residual risk / plan |
|---|-----------------|----------|------------------|----------------------|
| S1 | **Spoofing** — acting as another user | An attacker submits a victim's `reporter_email` to delete/reject/mark-found, or to read a chat | Endpoints verify the email matches the item owner; chat threads resolve server-side | **High residual**: identity is a plain email string, no token. Documented and accepted for v1.0; future work: session tokens issued at `/api/login`, required on every mutating endpoint |
| S2 | **Spoofing** — brute-force sign-in | Automated password guessing on `/api/login` | Passwords salted+hashed; no lockout | Medium: add login rate limiting + PBKDF2/argon2 |
| T1 | **Tampering** — forged/oversized/malicious uploads | `../../evil.html` path traversal, a 2 GB file, stored-XSS via an HTML upload | UUID filenames, image-extension whitelist, 5 MB cap | Low residual: content-type sniffing (verify magic bytes) as future work |
| T2 | **Tampering** — editing another user's report | `PUT /api/items/{id}` with a victim's email | 403 unless the email matches the owner; only Active reports are editable | Tied to S1's residual risk |
| R3 | **Repudiation** — "I never claimed that item" | A dispute over who claimed what | Audit trail: `claim_details`, `disputes` (status + `resolved_at`), `resolved_via`, `rejected_claimants` | Low for v1.0's scope |
| I1 | **Information disclosure** — contact details exposed | A visitor scrapes emails/phones from the API | `public_item()` strips contact/claim/finder/rejected fields per viewer; disputes are anonymised for non-reporters | Low for v1.0; TLS/HTTPS in production deployment |
| I2 | **Information disclosure** — chat eavesdropping | An outsider reads a private thread | Thread participants resolved server-side; 403 otherwise; the unread endpoint excludes strangers | Tied to S1's residual risk |
| I3 | **Information disclosure** — user enumeration | `/api/login` returning 404 reveals an email exists | Present | Low: return a uniform 401 (future work) |
| D1 | **Denial of service** — spam flooding | Thousands of reports/disputes/messages | Limits: 3 active portal lost reports per ID, 20 disputes/item, 20 finder responses/item, 200 messages/thread; the validation gate | Medium: per-IP limits at a reverse proxy in production |
| D2 | **Denial of service** — disk exhaustion via uploads | Many 5 MB uploads | 5 MB cap per file | Medium: total-quota monitoring in production |
| E1 | **Elevation of privilege** — code execution via upload/db.json | A crafted file executed server-side | Static files are served, not executed; uploads validated; the JSON store is only written by the app | Low for v1.0 |

Reading the table honestly: every "Low residual" row is low *because of work I actually did*
(the sanitizer, the upload hardening, the server-side thread checks). The two Medium/High
residuals (S1, S2) are both the same root cause — no session tokens — and they're the first
thing I'd fix in v1.1.

## 2. OWASP Top 10 check (2021)

| Category | Status | Evidence |
|----------|--------|----------|
| A01 Broken Access Control | **Addressed (with the S1 caveat)** | Every mutating endpoint checks ownership server-side; the privacy projection strips data per viewer; negative tests assert the 403s (T-03/05/06/08/16/19/21/22/23) |
| A02 Cryptographic Failures | **Partially** | Salted SHA-256 for passwords — not a KDF, and I say so; no secrets in code; HTTPS listed for production |
| A03 Injection | **Addressed** | No string-built SQL (file store; the SQL upgrade uses a parameterised schema); FastAPI/pydantic typing; no `eval` or shell calls |
| A04 Insecure Design | **Addressed** | The permission matrix was designed up front; lost and found flows are separated; anti-spam limits were designed in, not bolted on |
| A05 Security Misconfiguration | **Addressed** | No debug mode in the deployment command; `.gitignore` excludes `db.json` and uploads; CORS not opened (same-origin) |
| A06 Vulnerable Components | **Monitored** | Pinned minimums in `requirements.txt`; the TestClient/httpx deprecation warnings are tracked |
| A07 Identification & Authentication Failures | **Partially** | Password minimum length; salted hashes; no lockout or rate limit (documented future work) |
| A08 Software & Data Integrity | **Addressed** | State written atomically per mutation from a single process; uploads are content-typed |
| A09 Logging & Monitoring Failures | **Partial** | Uvicorn access logs on; no audit log of admin actions (future work) |
| A10 SSRF | **Not applicable** | The server makes no outbound requests with user-supplied URLs |

I marked the honest "Partials" rather than rounding them up to "Addressed" — A02 and A07 are
the same SHA-256 / no-rate-limit gap, and inflating them would just make the threat model
lie to me.

## 3. CI pipeline

`.github/workflows/ci.yml` in the repository:

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
the same gate the project passes locally at 84 %.

## 4. Deployment

The portal is deployed to production, not just a test laptop. After comparing options, I chose
**Render's free web-service tier** over alternatives:

- **Why Render:** permanent public HTTPS URL on the free plan, no credit card, deploys straight
  from the GitHub repo, and the free tier's quirks (sleep, ephemeral disk) are acceptable for a
  campus demo. A named Cloudflare tunnel needed a paid domain; keeping the laptop as the server
  would make the app unreachable whenever my machine is off.
- **How it deploys:** `render.yaml` in the repo root is a Blueprint — Render installs
  `requirements.txt` and runs `uvicorn main:app --host 0.0.0.0 --port $PORT`. The health check is
  `GET /api/items`. Every push to `main` redeploys automatically, so the deployed build always
  matches the repository.
- **Live URL:** `https://afit-lost-and-found.onrender.com`
- **Verified post-deploy:** portal, API, manifest, service worker and icons all return 200; the
  11 seed items load; and the privacy sanitizer works on the deployed instance (anonymous API
  responses contain no contact fields).
- **Because it is HTTPS**, the PWA now installs fully on phones (Android "Install app" /
  iOS "Add to Home Screen") with the offline service-worker shell — over plain-HTTP LAN links
  browsers refuse full installation, which the tunnel sharing phase made obvious.

**Free-tier limitations, stated honestly:**
1. The service sleeps after ~15 minutes without visitors; the first request afterwards waits
   ~30–60 s while it wakes. For demos I open the link a minute early.
2. The disk is ephemeral: on wake, `db.json` and `static/uploads/` reset, so the portal returns
   to its 11 seed items. For a demo this doubles as a clean-state guarantee, but it also means
   user data is not durable in production — the first real fix would be Render's paid persistent
   disk or the PostgreSQL migration (§6 in week 5).

**Production hardening checklist (beyond the free tier):** session tokens (S1), login rate
limiting (S2), per-IP limits (D1), persistent storage or PostgreSQL, and monitoring/uptime
alerts. The deployment command, blueprint and CI gate are already in the repository, so each of
these is an increment, not a rebuild.
