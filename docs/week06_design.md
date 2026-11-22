# Week 6 — Design Patterns and UI/UX Design (SP-014)

**Deliverables:** design-patterns note (≥ 2 patterns), wireframes, one SOLID-compliant module. **Marks: 6**

## 1. Design Patterns Applied

### Pattern 1 — Repository (persistence abstraction)
All reads/writes of the data store go through two functions, `save_state()` and `load_state()`,
plus module-level collections (`items_db`, `users_db`, `conversations`). The rest of the code
never touches the file directly.

- **Why:** the Week-5 plan calls for a PostgreSQL upgrade path. Because every mutation funnels
  through the repository functions, swapping `db.json` for SQL means reimplementing one layer,
  not hunting down file writes across the codebase.
- **Where:** `main.py` — `save_state()` called after every mutation; `load_state()` at startup
  (including the thread-key migration, which is itself repository behaviour).

### Pattern 2 — Strategy (pluggable validation and permission policies)
Behaviour that varies by context is selected at runtime rather than hard-coded in branches:

- **Contact gating strategy** — `public_item(item, viewer_email)` chooses which fields to emit
  based on the viewer's relationship to the item (reporter / claimant / finder / stranger).
  The same endpoint serves all four audiences; the *strategy* is the viewer relationship.
- **Report-type strategies** — lost and found reports run different flows (finder-response vs
  claim-with-proof, different required fields, different resolution actions). The form and the
  card renderer switch field sets and action buttons on `item_type`.
- **Thread resolution strategy** — `resolve_thread()` maps (user, peer) to a thread key
  depending on who is the non-reporter partner (claimant or one of many finders).

### Pattern 3 — Facade (single-entry API surface)
The front-end never touches domain logic; every operation is one facade call on the REST
surface (`/api/items`, `/api/items/{id}/claim`, `/api/items/{id}/messages`, …). The facade
hides validation, permission checks, persistence and status transitions behind stable URLs.

### Pattern 4 — Observer (polling-based notification)
Unread chat indicators implement the observer intent: the browse view subscribes (15 s
interval + on-demand `loadItems()`), the server publishes per-thread counts via
`GET /api/chat/unread`, and the UI reacts (red dot on Chat / finder-response buttons).
Chosen over WebSockets deliberately for demo robustness.

## 2. SOLID-Compliant Module: the privacy sanitizer (`public_item`)

```
main.py :: public_item(item, viewer_email)
```

- **S — Single responsibility:** it does exactly one thing — decide what a given viewer may
  see of an item. No validation, no persistence, no status logic.
- **O — Open/closed:** adding a new viewer relationship (e.g. "security officer") means adding
  a flag inside `public_item`; the endpoint and every consumer stay untouched.
- **L — Liskov:** any viewer type produces a valid item projection; consumers never receive a
  shape they cannot render (all flags always present, booleans always defined).
- **I — Interface segregation:** consumers receive only the flags they need
  (`viewer_is_reporter`, `viewer_is_claimant`, `viewer_is_finder`, `viewer_is_rejected`,
  `found_reports_count`) instead of the raw internal record with `rejected_claimants` and
  `seeded` bookkeeping.
- **D — Dependency inversion:** the API route depends on this abstraction, not on the storage
  layout — which is why the front-end and the tests were unaffected when internal fields were
  renamed during refactoring.

Evidence: the privacy tests (`test_public_api_strips_private_fields`) verify that anonymous
viewers receive zero private fields while reporters receive their own — the module is the
single enforcement point.

## 3. Wireframes (key screens)

### 3.1 Browse (home) — desktop
```
+--------------------------------------------------------------------------+
| [AF] AFIT Lost & Found Portal            Search...        [Sign in]      |
+--------------------------------------------------------------------------+
| ========================================================================= |
| =  (dark hero band)                              Total Logged: 11        =
| =  AFIT Lost & Found Portal                      Active Cases: 11        =
| =  Report it. Search it. Recover it.                                     =
| ========================================================================= |
| +---------------- search card ----------------+                          |
| | ( ) Lost  (o) Found   [What are you looking |                          |
| |  for_______] [Where? v]  [Search Items]     |                          |
| +---------------------------------------------+                          |
| +------------------+ +------------------+ +------------------+           |
| | [photo] LOST     | | [photo] FOUND    | | [photo] LOST     |           |
| | Black School Bag | | AFIT ID Card     | | HP Laptop        |           |
| | Location: Mosque | | Bush Canteen     | | Library          |           |
| | Status: Active   | | Status: Active   | | Status: Active   |           |
| | Report To: ...   | | Custody: ...     | | Report To: ...   |           |
| | Contact: hidden* | | Contact: hidden* | | Contact: hidden* |           |
| | [I Found This    | | [Claim & Verify  | | [I Found This    |           |
| |  Item]           | |  Ownership]      | |  Item]           |           |
| +------------------+ +------------------+ +------------------+           |
|   * contact details shown only to reporter / claimant / finder           |
+--------------------------------------------------------------------------+
```

### 3.2 Browse — mobile (360 px)
```
+---------------------------+
| [AF] Portal        [in]   |
| ========================= |
| AFIT Lost & Found Portal  |
| Report it. Search it.     |
| Recover it.               |
| [What are you looking     |
|  for________]             |
| [Where?        v]         |
| [     Search Items      ] |
| +-----------------------+ |
| | [photo]        LOST   | |
| | Black School Bag      | |
| | Mosque Area - Active  | |
| | [I Found This Item]   | |
| +-----------------------+ |
| +-----------------------+ |
| | ...next card...       | |
+---------------------------+
```

### 3.3 Report form (lost vs found differences)
```
+----------------------------------------------+
| Submit Lost or Found Property Report         |
| Report Classification: (I Lost Something v)  |
| Item Category:         [Electronics       v] |
| Title / Description / Location / Date       |
| + duplicate warning panel (amber, live)     |
|   "Possible matches already on the portal"  |
| Photo (optional)                             |
| Report To: [Campus Security Desk / ...  v]  |  <- both types; hint differs
| Reporter Verification: name/matric/phone    |
| Contact email: [x]  Preferred: (o)both      |
| [Submit Report]  [Cancel]                    |
+----------------------------------------------+
  found-only extras: custody select (security post / with me)
```

### 3.4 Claim modal (found items)
```
+----------------------------------------------+
| Claim This Item: AFIT Student ID Card        |
| Full name / Matric / Phone / Email           |
| Proof of ownership: [describe serial, ...]   |
| Proof photo (optional)                       |
| Contact preference: (o) email ( ) phone      |
| [Submit Claim]                               |
| Security notice: item shows returned only    |
| after the handover is confirmed.             |
+----------------------------------------------+
```

### 3.5 Finder response + owner moderation (lost items)
```
Finder card button:            Owner card:
[ I Found This Item ]          Your report - 2 finder responses
                               [Mark as Found] [Close] [View]
Owner "View" panel:
+----------------------------------------------+
| Finder Responses: HP Pavilion Gaming Laptop  |
| Musa Abu (U23CS1067) - 09:14                 |
| mmsocialwork0@gmail.com - 080...             |
| Found at: Library ground floor               |
| [Open Chat] [Confirm Return via This Finder] |
+----------------------------------------------+
```

### 3.6 Chat with unread indicator
```
Card action row:  [Chat (.)<- red dot when unread]
+---------------- Chat: Black School Bag ------+
| (finder)  It is at the mosque committee box  |
|           09:14                              |
|                (owner) Thank you! 4pm today? |
|                           09:20              |
| [message input.....................] [Send]  |
+----------------------------------------------+
```

## 4. UX decisions recorded
- Institutional look: white header, emerald accents, no emoji icons (matches stakeholder feedback).
- Contact details gated behind engagement (claim / finder response) to protect privacy while
  keeping the reporting path friction-free.
- Lost reporters get a lighter flow ("I Found This Item") because they are the victim, not the
  verifier; found reporters get the ownership quiz because they hold the property.
- Duplicate warning is non-blocking — it informs but never prevents a legitimate report.
