# Week 6 — Design Patterns and UI/UX Design (SP-014)

**Deliverables:** design-patterns note (≥ 2 patterns), wireframes, one SOLID-compliant module. **Marks: 6**

## 1. The design patterns I actually used

I want to frame this honestly: I didn't sit down and think "which patterns shall I apply
today?" — I built the thing, then recognised which patterns had emerged, and then *named* them
and made sure they were applied consistently. That's how patterns are supposed to work in
small projects, I think.

### Pattern 1 — Repository (persistence abstraction)

Every read and write of the data store goes through two functions: `save_state()` and
`load_state()`, operating on module-level collections (`items_db`, `users_db`,
`conversations`). Nothing else in the codebase touches the file directly.

Why this mattered: my week-5 plan calls for a PostgreSQL upgrade path. Because every mutation
funnels through the repository functions, swapping `db.json` for SQL means reimplementing one
layer, not hunting down file writes scattered across the codebase. It also gave me one place
to put the "write on every mutation" durability rule.

### Pattern 2 — Strategy (pluggable behaviour selected at runtime)

Several places in the system where behaviour varies by context, and instead of hard-coding
branches everywhere, the variation is packaged and selected at runtime:

- **Contact gating.** `public_item(item, viewer_email)` decides which fields to emit based on
  the viewer's relationship to the item — reporter, claimant, finder, or stranger. One
  endpoint serves all four audiences; the *strategy* is the viewer relationship.
- **Report-type strategies.** Lost and found reports run genuinely different flows: finder
  responses versus claims-with-proof, different required fields, different resolution actions.
  The form and the card renderer switch field sets and buttons on `item_type`.
- **Thread resolution.** `resolve_thread()` maps a (user, peer) pair to a thread key depending
  on who the non-reporter partner is — a claimant or one of several finders.

### Pattern 3 — Facade (one door into the system)

The front-end never touches domain logic. Every operation is a single call on the REST surface
(`/api/items`, `/api/items/{id}/claim`, `/api/items/{id}/messages`, …). The facade hides
validation, permission checks, persistence and status transitions behind stable URLs, which is
why I could reorganise the internals repeatedly without the front-end noticing.

### Pattern 4 — Observer (polling-based notification)

The unread chat indicators follow the observer intent: the browse view subscribes (a 15-second
interval plus an on-demand refresh), the server publishes per-thread counts via
`GET /api/chat/unread`, and the UI reacts with a red dot. I chose polling over WebSockets
deliberately — fewer moving parts to fail during a live demo.

## 2. The SOLID module: the privacy sanitizer

```
main.py :: public_item(item, viewer_email)
```

I'm holding this function up as my SOLID-compliant module because it's the piece of the system
I'm most confident defends itself on every principle:

- **Single responsibility.** It does exactly one thing — decide what a given viewer may see of
  an item. No validation, no persistence, no status logic. One job.
- **Open/closed.** If I add a new viewer relationship (say, "security officer"), I extend the
  flags inside `public_item`; the endpoint and every consumer stay untouched.
- **Liskov substitution.** Any viewer type produces a valid item projection. Consumers never
  receive a shape they can't render — all flags are always present, booleans always defined.
  (This sounds theoretical until you've had a grid go blank because a field was missing. I
  have. Twice. See the week-10 defect log.)
- **Interface segregation.** Consumers get only the flags they need (`viewer_is_reporter`,
  `viewer_is_claimant`, `viewer_is_finder`, `viewer_is_rejected`, `found_reports_count`)
  instead of the raw internal record with its `rejected_claimants` and `seeded` bookkeeping.
- **Dependency inversion.** The API route depends on this abstraction, not on the storage
  layout — which is why internal fields could be renamed during refactoring without breaking
  the front-end or the tests.

Evidence it works: the privacy test (`test_public_api_strips_private_fields`) verifies that an
anonymous viewer receives zero private fields while a reporter sees their own. This function
is the single enforcement point for the whole privacy story.

## 3. Wireframes

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

### 3.3 Report form (the lost/found differences)

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

## 4. The UX decisions behind the wireframes

A few choices I made consciously, with reasons:

- **Institutional look.** White header, emerald accents, no emoji icons. Early feedback on my
  first design was that it looked like a toy; the reference design I matched is what a campus
  office would actually deploy.
- **Contact details gated behind engagement.** Shown only after someone files a claim or a
  finder response. This protects privacy without making reporting itself harder — the two
  audiences have different needs, and the gate sits exactly between them.
- **Lost reporters get the lighter flow.** "I Found This Item" is one click because the lost
  reporter is the victim, not the verifier. Found reporters get the ownership quiz, because
  they hold the property and bears the risk of handing it to the wrong person.
- **The duplicate warning never blocks.** It informs. Two people really can lose the same
  model of phone in the same week, and a hard block would turn them away.
