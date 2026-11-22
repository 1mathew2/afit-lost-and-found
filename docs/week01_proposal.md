# Week 1 — Project Proposal (SP-014: Campus Lost-and-Found App)

**Deliverables:** project proposal, process-model justification, repository link. **Marks: 4**

## Why I picked this problem

Losing property on campus is such a common experience that nobody treats it as a systems
problem anymore — we just shrug and post in a WhatsApp group. Every semester at AFIT, phones,
ID cards, laptops, chargers and textbooks go missing in lecture halls, the library, hostels
and the canteen. And the recovery channels we actually have are all informal: word of mouth,
a notice board nobody checks, scattered WhatsApp messages that get buried within two days.

I kept running into the same four frustrations when I asked classmates about their experiences:

- If you lose something, you have no way of knowing whether it was even found, let alone
  handed to the security post.
- If you *find* something, there is no official way to report it — you either hold onto it
  awkwardly or hand it to security and hope the owner shows up.
- The security post keeps paper records, which students can't search.
- So recovered items pile up unclaimed, because the person who found it and the person who
  lost it never meet in the middle.

That last gap is what convinced me: the problem isn't a lack of goodwill, it's the absence of
a single searchable place where "I lost this" and "I found this" can meet. That became my
project.

## Who I'm building this for

I identified four groups of users, and I tried to keep all of them in mind while designing:

- **The student who lost something** — they want to report the loss fast, search what's
  already been found, talk to finders privately, and verify ownership to get the item back.
- **The finder** — they want a quick, legitimate way to log what they found and say where
  it's being held, without getting stuck with the item or hounded by strangers.
- **Campus security and hall wardens** — they currently keep paper logs; a digital record of
  what was reported and what was handed in, per post, is a genuine improvement for them too.
- **Student affairs / administration** — they care about the dispute trail and overall usage,
  though for v1.0 they're consumers of the audit trail rather than active users.

## What I set out to achieve (SMART objectives)

1. Any AFIT student should be able to report a lost or found item in under two minutes.
2. All active reports should be searchable and filterable by type, category, location and keyword.
3. Found items should go through a *verified* claim-and-return flow — the finder asks ownership
   questions and confirms the return, not just anyone who says "that's mine".
4. Lost items should get a lighter "I found this" response flow, plus a private one-to-one chat
   so the owner and a finder can arrange the handover.
5. Every claim, dispute and resolution should leave an auditable trail.
6. All of the above should ship as an installable, mobile-friendly PWA by week 13.

## Scope

I had to be disciplined here — this is a 13-week single-person project, and my instinct was to
promise everything.

**In scope for v1.0:** lost/found reporting with photos, search and filtering, the claim and
verification flow, finder responses, private chat, dispute reports, reporter moderation
(confirm / reject / edit / close), account sign-up and sign-in, input validation, anti-spam
limits, PWA install with an offline shell, and file-based persistence.

**Deliberately out of scope:** email/SMS notification servers (no mail server available to me),
payment or reward handling, integration with the official student records system, native mobile
apps, multi-campus support, and image recognition. I wrote these down early so that when the
temptation came mid-project, I could point at this list and say no.

## Which process model I chose, and why

I went with the **incremental model**, structured around the course's weekly deliverables.

I did seriously consider the alternatives:

- **Waterfall** was tempting because the requirements felt clear to me at the start. But they
  weren't, really — I knew I'd learn the most from putting a working system in front of
  classmates, and waterfall only gives you that feedback at the very end. Too late to act on.
- **Pure prototyping** didn't fit either, because the core flows (report → search → claim) are
  well-understood problems; throwing away prototypes would just burn effort.
- **Scrum** was the strongest competitor. The problem is that this course isn't organised into
  sprints — it's organised into 13 graded weekly deliverables. Running Scrum on top of that
  would mean double bookkeeping.

The incremental model matches the course structure almost exactly: each week delivers a usable
increment (proposal → requirements → plan → models → architecture → first module → demo →
full system → hardening → testing → security → docs → final). The practical payoff showed up
at the Week 8 prototype demo: by then I already had a working report-browse-claim system, and
the feedback from that demo fed straight into weeks 9–13 without any rewrite of the core.

## Repository

I initialised a local Git repository at the project root (`main` branch) and made the first
commit once the core system was stable:

```
9cefa6a SP-014: AFIT Lost & Found Portal - core system (FastAPI + PWA)
```

The layout is simple: `main.py` (backend), `static/` (the PWA front-end), `test_main.py`
(automated tests), `docs/` (this package), plus `requirements.txt` and `README.md`.
