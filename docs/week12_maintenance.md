# Week 12 — Maintenance, Documentation and Software Metrics (SP-014)

**Deliverables:** one processed change request with impact analysis, user manual, technical docs, metrics report. **Marks: 6**

## 1. Change request CR-001

This is the change request that came out of the week-8 demo audience, processed properly
rather than just implemented on impulse — which is the whole point of having a process.

| Field | Value |
|-------|-------|
| ID / Date | CR-001 — raised after the Week 8 demo feedback |
| Requester | Classmates in the demo audience (via me, as demonstrator) |
| Title | "Notify me when someone responds to my lost item" |
| Original request | Email/SMS notification when a finder response or chat message arrives |
| Type | New feature (notification) |

### 1.1 Impact analysis

| Area | Impact |
|------|--------|
| Backend | A new outbound dependency — an SMTP server or SMS gateway. Neither is available in my demo environment; this means credentials, firewall ports and a third party I don't control |
| Security | A whole new attack surface: credential storage for SMTP, and the classic spam-relay risk. The week-11 threat model would need new S3/D3 entries |
| Front-end | Some notification surface (badge/toast) |
| Schedule | I estimated 6–8 hours plus external approvals — which lands squarely on top of the W10 testing and W11 security weeks, the two weeks I least wanted to disturb |
| Alternative | In-app indicators already shipped: unread dots, the "N finder responses" badge, 15-second polling. They cover the core need ("someone responded — go look") without any external dependency |

### 1.2 The decision

**Partially approved, re-scoped.** v1.0 ships the in-app notification indicators (already
implemented: per-thread unread dots plus finder-response badges). Full email/SMS notification
goes on the "Won't have (v1.0)" list and is re-planned for v1.1 with an SMTP dependency.
Status: **Closed — deferred, with the alternative delivered.**

This mirrors the week-3 requirements-validation downgrade, which I take as a sign the process
is consistent rather than that I'm repeating myself. The baseline stayed stable through the
testing and security weeks, which was the entire point of saying no at the right time.

## 2. User manual

Written for the actual end user — a student who has never read any of the other documents.

### 2.1 Installing the app on your phone
1. Open `http://<portal-address>:8000` in Chrome or Safari.
2. Tap the browser menu → **Add to Home screen / Install**.
3. Launch it from the home screen icon — it opens full-screen, like an app.

### 2.2 Reporting a lost item
1. Sign in (top-right). First time? **Sign up** with your name, email and a password of at
   least 6 characters.
2. Go to **Report** → choose **I Lost Something**.
3. Fill in the category, title, description, location and date; add a photo if you have one.
4. Choose **Report To** — the person finders should hand the item to (for example *Student*
   if you'd rather handle the handover yourself, or the Hall Warden).
5. Watch the amber **"Possible matches"** panel while you type the title — someone may have
   already found it.
6. Submit. Your item now appears in Browse with a *Lost* badge.

### 2.3 Reporting a found item
Same as above, but choose **I Found Something**. You must also say who you handed the item to
(Report To) and where it's being held — the security post, or with you.

### 2.4 Recovering your lost item
1. When someone clicks **I Found This Item** on your report, your card shows
   *"N finder responses"*.
2. Click **View** — you'll see each finder's name, matric, contact details and where they
   found it.
3. **Open Chat** to talk privately with one finder at a time (a red dot tells you when there
   are unread messages).
4. Once the item is back in your hands: **Confirm Return via This Finder** (which credits
   them) or simply **Mark as Found**. If you no longer want the report at all: **Close**.

### 2.5 Claiming a found item
1. On the found item's card, click **Claim & Verify Ownership**.
2. Fill in your details and describe your proof of ownership — a serial number, the contents,
   a distinguishing mark. A proof photo helps if you have one.
3. The reporter gets notified (the red dot). They will either **Confirm Return** or **Reject**
   your claim.
4. If your claim is rejected, you can't claim that item again — if you genuinely believe it's
   yours, your route now is contacting the reporter directly.

### 2.6 Disputing a claim
If a claim in progress on an item is false, click **Report Item** on the card and describe
why. The reporter reviews it and either upholds it (the claim is rejected and the item goes
back to Active) or dismisses it (the claim stands).

### 2.7 Editing or removing your report
On your own Active report: **Edit** changes any detail — title, description, location, photo,
contact details. (The sign-in email stays fixed; it's the ownership identity.) **Delete**
removes the report permanently.

### 2.8 The rules, so nothing surprises you
- Contact details stay hidden until someone actually engages — a claim or a finder response.
- Maximum 3 active lost reports per student ID; 20 disputes or responses per item.
- Names, phone numbers (e.g. `08031234567`), matric IDs and emails are all validated — typos
  bounce with a message telling you which field.

## 3. Technical documentation (for whoever maintains this after me)

- **Architecture and data:** `week05_architecture.md` — layers, ERD, and the PostgreSQL
  upgrade schema.
- **API surface:** `GET /api/items[?filters&viewer_email]`, `POST /api/items`,
  `PUT/DELETE /api/items/{id}`, `POST /api/items/{id}/claim|reject-claim|confirm-return|
  dispute|found-report|mark-found|close-report|disputes/{i}/resolve`,
  `GET/POST /api/items/{id}/messages`, `GET /api/chat/unread`, `/api/signup`, `/api/login`.
- **Status lifecycle:** Active → Claim Requested → Claimed/Returned | Active; lost items can
  also resolve via mark-found/close. Every transition is guarded server-side with a distinct
  400/403 reason.
- **Persistence:** `db.json` holds items, the counter, users, and conversations keyed
  `itemId:partnerEmail`. Deleting an item cascades to its threads. Reset = delete `db.json`
  and restart.
- **Front-end:** vanilla JS with a single `itemsCache`, re-rendered by `loadItems()`; the
  service worker is network-first for page/app.js with the cache bumped per release
  (`afit-lf-vN`).
- **Run/test:** `python -m uvicorn main:app --port 8000`;
  `python -m pytest test_main.py --cov=main -q`.

## 4. Metrics report

| Metric | Value | Notes |
|--------|-------|-------|
| Python source lines (`main.py`) | ~530 | one backend module |
| Front-end lines | index.html ~640, app.js ~890 | presentation fully separated |
| Test lines | ~530 | 28 tests |
| Test count / status | 28 / all passing | the regression suite |
| Line coverage (`main.py`) | **84 %** | target was ≥ 80 % |
| Endpoints | 17 REST operations | all with permission checks |
| Cyclomatic complexity (max function) | ≈ 5 (`public_item`) | guideline is ≤ 10 |
| Requirements delivered | 14 FR + 8 NFR | 100 % of Must/Should, 100 % of Could |
| Defects found / open | 10 / **0 open** | the week-10 defect log |
| Effort | ≈ 54 h against a 50 h estimate | +8 % |
| Schedule | feature-complete a week early (W8 vs W9) | the headroom went to testing and security |

The metric I'd point an examiner at is the last two rows together: I finished the features
early and spent the surplus on testing and security, and the defect log shows that trade
paying off — ten defects found and fixed, zero still open.
