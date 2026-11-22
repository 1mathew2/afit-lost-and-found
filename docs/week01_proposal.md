# Week 1 — Project Proposal (SP-014: Campus Lost-and-Found App)

**Deliverables:** project proposal, process-model justification, repository link. **Marks: 4**

## 1. Problem Statement

Every semester, students and staff at the Air Force Institute of Technology (AFIT) misplace
phones, ID cards, laptops, chargers, wallets and textbooks in lecture halls, the library,
hostels, the canteen and around campus. Today the only recovery channels are word of mouth,
notice boards and ad-hoc WhatsApp messages. The result:

- Owners rarely know whether their property was found or handed to security.
- Finders have no standard, official way to hand in or report found property.
- The security post keeps paper records that cannot be searched by students.
- Recovered items pile up unclaimed because the right people are never matched.

There is no single, searchable, campus-wide system connecting "I lost this" with "I found this".

## 2. Target Users

| User | Needs |
|------|-------|
| Student who lost an item | Report a loss quickly, search found items, respond to finders, verify and recover |
| Finder of an item | Report what they found, state where it is held, connect with the rightful owner |
| Campus security / hall wardens | A digital log of reported and handed-in property per post |
| Student affairs / school administration | Oversight, dispute trail, usage statistics |

## 3. Objectives (SMART)

1. Provide a web portal where any AFIT student can report a lost or found item in under 2 minutes.
2. Provide search and filtering (type, category, location, keyword) over all active reports.
3. Provide a verified claim-and-return workflow for found items (ownership questions + reporter confirmation).
4. Provide a lightweight "I found this" response workflow for lost items, with private 1-to-1 chat.
5. Keep an auditable trail of claims, disputes and resolutions.
6. Deliver the above as an installable mobile-friendly PWA by week 13.

## 4. Scope

**In scope (v1.0):** lost/found reporting with photos, search/filter, claim + verification flow,
finder responses, private chat, dispute reports, reporter moderation (confirm/reject/edit/close),
account sign-up/sign-in, validation, anti-spam limits, PWA install + offline shell, file persistence.

**Out of scope (v1.0):** email/SMS notification servers, payment/reward handling, integration with
the official student records system, native mobile apps, multi-campus tenancy, image recognition.

## 5. Process Model — Selection and Justification

**Selected: Incremental (iterative) model with weekly deliverables.**

| Candidate | Assessment |
|-----------|-----------|
| Waterfall | All requirements are not known up front; feedback from demo-ing to classmates would arrive too late (only at the end). Rejected. |
| Pure prototyping | Throwaway prototypes waste effort when the core flows are clear. Rejected. |
| Agile/Scrum (sprints) | Strong candidate, but the course is fixed to 13 weekly deliverables with graded artifacts each week. Rejected in its pure form. |
| **Incremental** | Each week delivers a usable increment (proposal → requirements → plan → model → architecture → first module → demo → full system → hardening → tests → security → docs → final). Feedback from the Week 8 demo is absorbed before the final build. Matches the course structure exactly. **Selected.** |

Incremental delivery means the Week 8 prototype (report + browse + claim) is already a working
system, and weeks 9–13 add chat, disputes, moderation, testing, security and documentation
without rewriting the core.

## 6. Repository

- Local repository initialised at the project root with Git (`main` branch).
- Initial commit: `SP-014: AFIT Lost & Found Portal - core system (FastAPI + PWA)`.
- Layout: `main.py` (backend), `static/` (PWA front-end), `test_main.py` (tests),
  `docs/` (this package), `requirements.txt`, `README.md`.
