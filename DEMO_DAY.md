# Demo Day Checklist — AFIT Lost & Found Portal (SP-014)

## Tonight / before leaving
- [x] Cloud deployment live: https://afit-lost-and-found.onrender.com (verified: portal, API, seeds)
- [x] Database reset to the 11 seed items (fresh demo state)
- [x] Slides ready: `AFIT_Lost_and_Found_Presentation_v2.pptx` (13 slides, large text)
- [ ] Charge laptop + phone; test the projector cable if you can

## Morning of the demo
1. **Wake the server early** — the free tier sleeps after ~15 min idle and takes 30–60 s to
   wake. Open the portal link in your laptop browser a few minutes before you present.
2. **Use the cloud URL on every device** — laptop (projector) and phone must BOTH be on
   `https://afit-lost-and-found.onrender.com`. Nothing done on `localhost` will appear on the
   phone, and vice versa.
3. **Sign in on the laptop before the audience arrives** — if the cloud database was reset,
   accounts were reset too; re-signing up takes 20 seconds. Do it before, not during.
4. **Have a backup tab open** with the browse page already loaded, in case of a slow wake.

## If something goes wrong
| Problem | Response |
|---------|----------|
| Portal slow / "waking up" | Wait 30–60 s, refresh. Talk over it — the slides cover the wait. |
| Venue Wi-Fi dead for phones | Fallback: double-click `Start Portal.bat` on the laptop, phones join the laptop's Wi-Fi hotspot or same network and use the printed LAN link. Note: cloud data won't be there — the LAN server has its own seeds. |
| Phone shows old UI | Hard refresh / clear site data (service worker cache). |
| Report filed but not visible on phone | You're on two different servers — check the URL bar on BOTH devices says onrender.com. |
| Data looks wrong / missing | The database resets to seeds on wake. Re-file live; it takes 2 minutes (that IS the demo). |

## Demo flow (7 min, from docs/week08_demo.md)
1. Portal on laptop AND phone side by side (responsive PWA)
2. Search + filter as a visitor (contact details hidden)
3. Report a found item — show validation by trying a bad phone number first
4. Second account claims it → status becomes Claim Requested
5. Chat between them; owner sees the unread dot → Confirm Return
6. On a lost seed item: "I Found This Item" → owner's finder list → chat → confirm via finder
7. Dispute: third party files → owner upholds → claim rejected, claimant banned
8. Edit a report, Mark as Found, reload to show persistence

## Key numbers to quote if asked
- 28 automated tests, 84 % line coverage, 0 open defects
- 17 REST endpoints, all permission-checked server-side
- ~54 h effort vs 50 h estimated; feature-complete a week early
- Deployed with CI: every push re-runs the tests + 80 % coverage gate
