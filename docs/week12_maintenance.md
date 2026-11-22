# Week 12 — Maintenance, Documentation and Software Metrics (SP-014)

**Deliverables:** one processed change request with impact analysis, user manual, technical docs, metrics report. **Marks: 6**

## 1. Change Request CR-001

| Field | Value |
|-------|-------|
| ID / Date | CR-001 — raised after the Week 8 demo feedback |
| Requester | Classmates demo audience (via demonstrator) |
| Title | "Notify me when someone responds to my lost item" |
| Original request | Email/SMS notification when a finder response or chat message arrives |
| Type | New feature (notification) |

### 1.1 Impact Analysis

| Area | Impact |
|------|--------|
| Backend | New outbound dependency (SMTP server / SMS gateway) — none available in the demo environment; credentials and firewall ports required |
| Security | New attack surface (credential storage for SMTP; spam relay risk) — W11 threat model would need S3/D3 entries |
| Front-end | Notification surface (badge/toast) |
| Schedule | Estimated 6–8 h + external approvals; conflicts with W10–W11 testing/security slots |
| Alternative | In-app indicators already shipped (unread dots, "N finder responses" badge, 15 s polling) cover the core need without external dependencies |

### 1.2 Decision (processed)

**Partially approved, re-scoped:** v1.0 ships in-app notification indicators (already
implemented: per-thread unread dots + finder-response badges). Full email/SMS notification is
logged in the "Won't have (v1.0)" list and re-planned for v1.1 with an SMTP dependency.
Status: **Closed — deferred with alternative delivered.** This mirrors the Week-3 validation
downgrade and keeps the baseline stable during the testing/security weeks.

## 2. User Manual (end-user documentation)

### 2.1 Installing the app (phone)
1. Open `http://<portal-address>:8000` in Chrome/Safari.
2. Tap the browser menu → **Add to Home screen / Install**.
3. Launch from the home screen icon — the portal opens full-screen.

### 2.1 Reporting a lost item
1. Sign in (top-right). First time? **Sign up** with your name, email and a password (6+ chars).
2. Go to **Report** → choose **I Lost Something**.
3. Fill category, title, description, location, date; optionally add a photo.
4. Choose **Report To** — the person finders should hand the item to (e.g. *Student* for
   self-managed handover, or the Hall Warden).
5. Check the amber **"Possible matches"** panel — someone may have already found it.
6. Submit. Your item appears in Browse with a *Lost* badge.

### 2.3 Reporting a found item
Same as above but choose **I Found Something**. You must also say who you handed the item to
(Report To) and where it is held (security post / with me).

### 2.4 Recovering your lost item
1. When someone clicks **I Found This Item** on your report, your card shows
   *"N finder responses"*.
2. Click **View** — you see each finder's name, matric, contact and where they found it.
3. **Open Chat** to talk privately with one finder at a time (a red dot shows unread messages).
4. Once the item is back in your hands: **Confirm Return via This Finder** (credits them) or
   simply **Mark as Found**. If you no longer want the report: **Close**.

### 2.5 Claiming a found item
1. On the found item's card click **Claim & Verify Ownership**.
2. Fill your details and describe proof of ownership (serial number, contents, marks); add a
   proof photo if you have one.
3. The reporter is notified (red dot). They will **Confirm Return** or **Reject**.
4. If rejected, you cannot claim that item again — contact the reporter directly if you believe
   it is genuinely yours.

### 2.6 Disputing a claim
If a claim in progress on an item is false, click **Report Item** on the card and describe why.
The reporter reviews it: upheld (claim rejected, item back to Active) or dismissed.

### 2.7 Editing or removing your report
On your own Active report: **Edit** changes any detail (title, description, location, photo,
contact details — the sign-in email stays fixed). **Delete** removes it permanently.

### 2.8 Rules to know
- Contact details stay hidden until someone engages (claim / finder response).
- Maximum 3 active lost reports per student ID; 20 disputes/responses per item.
- All names, phone numbers (e.g. `08031234567`), matric IDs and emails are validated.

## 3. Technical Documentation (maintainer view)

- **Architecture & data:** see `week05_architecture.md` (layers, ERD, PostgreSQL upgrade schema).
- **API surface:** `GET /api/items[?filters&viewer_email]`, `POST /api/items`,
  `PUT/DELETE /api/items/{id}`, `POST /api/items/{id}/claim|reject-claim|confirm-return|
  dispute|found-report|mark-found|close-report|disputes/{i}/resolve`,
  `GET/POST /api/items/{id}/messages`, `GET /api/chat/unread`, `/api/signup`, `/api/login`.
- **Status lifecycle:** Active → Claim Requested → Claimed/Returned | Active; lost items may
  also resolve via mark-found/close. All transitions guarded server-side with 400/403 reasons.
- **Persistence:** `db.json` (items, counter, users, conversations keyed `itemId:partnerEmail`).
  Deleting an item cascades to its threads. Reset = delete `db.json` and restart.
- **Front-end:** vanilla JS, one `itemsCache`, re-render on `loadItems()`; service worker
  network-first for page/app.js, cache bumped per release (`afit-lf-vN`).
- **Run/test:** `python -m uvicorn main:app --port 8000`; `python -m pytest test_main.py --cov=main -q`.

## 4. Software Metrics Report

| Metric | Value | Notes |
|--------|-------|-------|
| Python source lines (`main.py`) | ~530 | single backend module |
| Front-end lines | index.html ~640, app.js ~890 | presentation fully separated |
| Test lines | ~530 | 28 tests |
| Test count / status | 28 / all passing | regression suite |
| Line coverage (`main.py`) | **84 %** | target ≥ 80 % met |
| Endpoints | 17 REST operations | all with permission checks |
| Cyclomatic complexity (max function) | ≈ 5 (`public_item`) | within ≤ 10 guideline |
| Requirements delivered | 14 FR + 8 NFR | 100 % of Must/Should, 100 % of Could |
| Defects found / open | 10 / **0 open** | see W10 defect log |
| Effort | ≈ 54 h vs 50 h estimate | +8 % |
| Schedule | feature-complete 1 week early (W8 vs W9) | absorbed by testing/security weeks |
