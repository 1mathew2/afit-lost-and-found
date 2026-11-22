# SP-014 — AFIT Lost & Found Portal: Documentation Package

This folder is the written record of my 13-week Software Engineering course project: the
**AFIT Lost & Found Portal**, a web app that connects people who lose property on campus with
people who find it.

Each week's file matches that week's graded deliverable. The system itself lives in the repo
root — a FastAPI backend (`main.py`), a vanilla-JS PWA front-end (`static/`), a file-persisted
store (`db.json`), and 28 automated tests (`test_main.py`) at 84 % line coverage.

| Week | Topic | What I delivered | Marks |
|------|-------|------------------|-------|
| 1 | Introduction to SE and Process Models | [week01_proposal.md](week01_proposal.md) — proposal, process-model justification, repository | 4 |
| 2 | Requirements Engineering | [week02_srs.md](week02_srs.md) — stakeholders, SRS §1–3, user stories | 8 |
| 3 | Requirements Validation and Planning | [week03_planning.md](week03_planning.md) — MoSCoW, estimates, 13-week plan, risk register | 6 |
| 4 | System Modelling with UML | [week04_uml.md](week04_uml.md) — use case, class, sequence and activity diagrams | 8 |
| 5 | Software Architecture and Database Design | [week05_architecture.md](week05_architecture.md) — architecture choice, component diagram, ERD, schema | 8 |
| 6 | Design Patterns and UI/UX Design | [week06_design.md](week06_design.md) — patterns, wireframes, my SOLID module | 6 |
| 7 | Implementation I and Version Control | [week07_implementation.md](week07_implementation.md) — coding standard, module 1, Git history | 6 |
| 8 | Mid-Semester Review: Prototype Demo | [week08_demo.md](week08_demo.md) — demo script, progress report, backlog update | 10 |
| 9 | Implementation II, Refactoring, Code Quality | [week09_quality.md](week09_quality.md) — modules 2+, review log, static analysis | 6 |
| 10 | Software Testing | [week10_testing.md](week10_testing.md) — test plan, cases, coverage, defect log | 8 |
| 11 | Secure Development and DevOps | [week11_security_devops.md](week11_security_devops.md) — STRIDE, OWASP, CI, deployment | 8 |
| 12 | Maintenance, Documentation and Metrics | [week12_maintenance.md](week12_maintenance.md) — change request, user manual, metrics | 6 |
| 13 | Final Demonstration, Report and Reflection | [week13_final_report.md](week13_final_report.md) — final report, reflection, peer assessment | 16 |
| | | **Total** | **100** |

Run the system: `python -m uvicorn main:app --port 8000` → http://localhost:8000
Run the tests: `python -m pytest test_main.py --cov=main -q`
