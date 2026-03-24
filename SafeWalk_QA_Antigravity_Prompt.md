# 🚶 SafeWalk — QA Final Verification
### ANTIGRAVITY MASTER PROMPT · Random Forest Rangers 🌲 · FOSS Hack 2026
**Prepared by:** Arun Balaji · **QA Owner:** Arun Balaji · **Stack:** Streamlit + FastAPI + Supabase

---

## 0. How to Use This Prompt in Antigravity

Paste this entire document into Antigravity as your system context. Then give it the instruction below.

> **Instruction to give Antigravity after pasting:**
>
> *"You are the QA Engineer for SafeWalk, a crowdsourced pedestrian hazard navigation app built for FOSS Hack 2026. The app is live at http://localhost:8501 (Streamlit frontend) and http://localhost:8000 (FastAPI backend). Use this document as your test plan. Execute every test case in order, record PASS or FAIL for each, and output a final QA report with: overall status, pass rate, list of failures with root cause, and a GO/NO-GO verdict for submission. Be ruthless — a bug that ships is a bug the judges see."*

---

## 1. Project Context (Read First)

SafeWalk is a crowdsourced pedestrian hazard map for Indian cities. Users report hazards (broken footpaths, open manholes, waterlogging, poor lighting), the community confirms them, and the app routes walkers around danger zones.

**Repo:** https://github.com/Vishaal1409/safewalk

| Layer | Technology | Where It Runs |
|---|---|---|
| Frontend | Streamlit + Folium + OpenStreetMap | http://localhost:8501 |
| Backend API | Python + FastAPI | http://localhost:8000 |
| Database | PostgreSQL + PostGIS (Supabase cloud) | Supabase dashboard |
| Auth | JWT tokens | FastAPI built-in |
| Map | Leaflet via Folium, OpenStreetMap tiles | Embedded in Streamlit |
| Image Storage | Supabase Storage + Pillow validation | Supabase dashboard |

---

## 2. Pre-Flight Setup (Do Before Any Tests)

Both services must be up and healthy before running any test cases.

```bash
# Terminal 1 — Backend
cd safewalk/backend && uvicorn src.main:app --reload

# Terminal 2 — Frontend
cd safewalk/frontend && streamlit run app.py
```

| # | Test | Expected | Result |
|---|---|---|---|
| P0 | Backend health check: `GET http://localhost:8000/` or `/health` returns HTTP 200 | ✅ HTTP 200 | [ ] |
| P0 | Swagger docs load: `http://localhost:8000/docs` renders without error | ✅ Page loads | [ ] |
| P0 | Frontend loads: `http://localhost:8501` opens Streamlit app in browser | ✅ Map visible | [ ] |
| P0 | Map renders: Folium/Leaflet map centred on Chennai is visible | ✅ Tiles load | [ ] |
| P0 | `.env` is loaded: No "missing env var" or DB connection errors in backend terminal | ✅ No errors | [ ] |

---

## 3. 🔴 MUST DO — Full Flow Test (Re-Test After Every Fix)

> This is the critical path. Run it in full every time a fix is applied. Every step depends on the previous one.

---

### 3A — Hazard Report Flow

**Goal:** Report a hazard → it appears on the map → it is stored in DB → the confirm button works.

| # | Test | Expected | Result |
|---|---|---|---|
| 1 | Open `http://localhost:8501` — report form is visible on screen | ✅ Form visible | [ ] |
| 2 | Fill in: Hazard Type = `Open Manhole`, Location = click map or enter lat/lng, Description = `Test hazard QA` | ✅ Fields accept input | [ ] |
| 3 | Submit form — no error shown, success message or confirmation appears | ✅ Success message | [ ] |
| 4 | Hazard marker appears on the Folium map without needing to refresh the page | ✅ Marker appears | [ ] |
| 5 | Marker is the correct icon/colour for `Open Manhole` hazard type | ✅ Correct icon | [ ] |
| 6 | Click the marker — popup shows hazard type, description, and reporter info | ✅ Popup correct | [ ] |
| 7 | Open Supabase dashboard → hazards table → row for this hazard exists with correct data | ✅ Row in DB | [ ] |
| 8 | `GET /hazards` API call (via Swagger or Postman) returns the new hazard in the response | ✅ In API response | [ ] |

---

### 3B — Community Confirm Flow

**Goal:** Confirm a hazard → confirmation count increments by 1 → UI reflects updated count.

| # | Test | Expected | Result |
|---|---|---|---|
| 9 | Confirmation count on the hazard starts at 0 (or blank) before any confirm action | ✅ 0 confirmations | [ ] |
| 10 | Click `Confirm` or upvote button on the hazard reported in Step 3 | ✅ Button clickable | [ ] |
| 11 | Confirmation count increments to 1 — visible in popup or sidebar without full page reload | ✅ Count = 1 | [ ] |
| 12 | `POST /hazards/{id}/confirm` returns HTTP 200 and updated count in response body | ✅ HTTP 200, count++ | [ ] |
| 13 | Confirm again (same session) — app prevents double-confirm or shows appropriate message | ✅ Blocked or warned | [ ] |
| 14 | Check Supabase DB — `confirm_count` column for this hazard = 1 (not 2) | ✅ DB count = 1 | [ ] |

---

### 3C — Filter Flow

**Goal:** Filter by hazard type → only matching markers show on map → clear filter restores all.

| # | Test | Expected | Result |
|---|---|---|---|
| 15 | Add at least 2 more hazards of different types (e.g. `Broken Footpath`, `Waterlogging`) — 3 total on map | ✅ 3 markers visible | [ ] |
| 16 | Use the filter control (dropdown or sidebar) to select `Open Manhole` only | ✅ Filter applied | [ ] |
| 17 | Map shows ONLY the Open Manhole marker — other types are hidden | ✅ 1 marker visible | [ ] |
| 18 | Filter to `Broken Footpath` — only that marker shows | ✅ Correct marker | [ ] |
| 19 | Clear filter / select `All` — all 3 markers reappear on map | ✅ All 3 restored | [ ] |
| 20 | `GET /hazards?type=open_manhole` (or equivalent) returns only matching hazards | ✅ Filtered response | [ ] |

---

### 3D — Stats / Dashboard Flow

**Goal:** Stats panel shows accurate counts that match the actual DB state.

| # | Test | Expected | Result |
|---|---|---|---|
| 21 | Stats panel (sidebar or dashboard) shows total hazard count — matches number of reports submitted | ✅ Count accurate | [ ] |
| 22 | Hazard breakdown by type shows correct counts (1 Open Manhole, 1 Broken Footpath, 1 Waterlogging etc.) | ✅ Breakdown correct | [ ] |
| 23 | After adding a new hazard, stats update without full page reload (or within 1 refresh cycle) | ✅ Stats refresh | [ ] |
| 24 | Confirmation count in stats matches the DB value (`confirm_count = 1` from Step 14) | ✅ Confirms match DB | [ ] |
| 25 | Safety score for the street segment near the hazard has decreased (lower = more dangerous) | ✅ Score changed | [ ] |

---

## 4. 🟡 Stress Test (Quick — 15 Minutes)

> Simulate real-world usage with volume. These tests expose race conditions, UI lag, and backend edge cases that single-hazard tests miss.

---

### 4A — Volume Test (10–15 Hazards)

**Goal:** Add 10–15 hazards rapidly. App stays stable, map doesn't crash, DB rows are all present.

Use this mix of hazard types:
- 3 × Open Manhole
- 3 × Broken Footpath
- 2 × Waterlogging
- 2 × No Street Light
- 2 × Unsafe Area
- 1 × Construction Blocking Path
- 1 × Stray Animal Gathering

| # | Test | Expected | Result |
|---|---|---|---|
| 26 | Submit all 14 hazards one by one — no submission throws a 422, 500, or timeout error | ✅ All 200s | [ ] |
| 27 | Map renders all 14 markers without freezing or crashing the browser | ✅ Map stable | [ ] |
| 28 | Clicking any marker opens its correct popup (no wrong data shown) | ✅ Popups correct | [ ] |
| 29 | Supabase hazards table has exactly 14+ rows (plus the 3 from Section 3 = 17+ total) | ✅ Row count matches | [ ] |
| 30 | Filter by `Open Manhole` shows exactly 3 markers | ✅ Filter = 3 | [ ] |
| 31 | Stats panel shows updated counts for all hazard types | ✅ Stats correct | [ ] |
| 32 | Backend terminal shows no Python tracebacks or unhandled exceptions | ✅ Clean logs | [ ] |

---

### 4B — Confirm Spam Test (After Fix Applied)

> ⚠️ **Only run this after the double-confirm bug fix from Step 13 is applied and deployed.**

| # | Test | Expected | Result |
|---|---|---|---|
| 33 | Pick 1 hazard. Click Confirm 5 times rapidly (fast clicks or repeated API calls) | ✅ Blocked after 1 | [ ] |
| 34 | DB `confirm_count` for that hazard = 1 (not 5) | ✅ DB = 1 | [ ] |
| 35 | UI shows appropriate feedback: `Already confirmed` or disabled button | ✅ Feedback shown | [ ] |
| 36 | `POST /hazards/{id}/confirm` called 5× with same session — 1 returns 200, rest return 400 or 409 | ✅ 4× error response | [ ] |
| 37 | No negative or zero confirm counts possible (no decrement bugs) | ✅ Count >= 0 | [ ] |

---

## 5. Edge Cases & Boundary Tests

> These are the tests judges are most likely to stumble into accidentally. Handle them before submission.

| # | Test | Expected | Result |
|---|---|---|---|
| 38 | Submit hazard form with empty Description field — form validates and shows error, does not crash | ✅ Validation error | [ ] |
| 39 | Submit hazard with coordinates outside Chennai (e.g. Delhi lat/lng) — accepted or rejected gracefully | ✅ No crash | [ ] |
| 40 | Upload a non-image file (e.g. `.txt`) as hazard photo — Pillow/backend rejects it with clear error | ✅ Error shown | [ ] |
| 41 | Upload an image > 5MB — app handles it (rejects or resizes), no 500 error | ✅ Handled | [ ] |
| 42 | Open the app with no hazards in DB (fresh DB) — map loads normally, no crash, empty state shown | ✅ Empty state OK | [ ] |
| 43 | Kill the FastAPI backend mid-session — frontend shows connection error, does not white-screen crash | ✅ Error message | [ ] |
| 44 | Reload the page after submitting a hazard — hazard persists on map (loaded from DB, not in-memory) | ✅ Persists on reload | [ ] |
| 45 | Submit two identical hazards at the exact same location — both are accepted and shown | ✅ Duplicates allowed | [ ] |

---

## 6. API Contract Verification (via Swagger /docs)

> Open `http://localhost:8000/docs` and run each endpoint through the Swagger UI. Judges will hit the API directly.

| # | Test | Expected | Result |
|---|---|---|---|
| 46 | `GET /` or `GET /health` → HTTP 200, JSON response with `status: ok` | ✅ 200 | [ ] |
| 47 | `POST /hazards` → HTTP 201, returns created hazard with `id`, `lat`, `lng`, `type`, `created_at` | ✅ 201 + body | [ ] |
| 48 | `GET /hazards` → HTTP 200, returns array of all hazard objects | ✅ 200 + array | [ ] |
| 49 | `GET /hazards?lat=13.05&lng=80.21&radius=500` → returns only hazards within 500m | ✅ Spatial filter works | [ ] |
| 50 | `POST /hazards/{id}/confirm` → HTTP 200, `confirm_count` incremented in response | ✅ 200 + count++ | [ ] |
| 51 | `GET /hazards/{id}` → HTTP 200 with full hazard detail, or 404 for non-existent id | ✅ 200 or 404 | [ ] |
| 52 | `POST /auth/register` → creates user, returns JWT token | ✅ Token returned | [ ] |
| 53 | `POST /auth/login` → valid credentials return JWT, invalid return 401 | ✅ 401 on bad creds | [ ] |
| 54 | All endpoints return JSON with `Content-Type: application/json` header | ✅ JSON headers | [ ] |
| 55 | Swagger UI at `/docs` shows all endpoints with correct parameters and response schemas | ✅ Docs complete | [ ] |

---

## 7. Submission Readiness Checklist

> Every item must be checked before **5 PM IST March 31**. Don't wait until 6 PM.

| # | Item | Owner | Done? |
|---|---|---|---|
| 56 | GitHub repo is **PUBLIC** — anyone can view it without logging in | Vishaal | [ ] |
| 57 | `MIT LICENSE` file exists in repo root | Vishaal | [ ] |
| 58 | `README.md` has: project description, problem it solves, tech stack, setup instructions | Arun | [ ] |
| 59 | README has screenshots or a GIF of the app running | Arun | [ ] |
| 60 | All 4 team members (Vishaal, Arun, Shruthika, Ishitha) have commits in March 2026 | Everyone | [ ] |
| 61 | Demo video is max 3 minutes, uploaded to YouTube, link in README | Arun | [ ] |
| 62 | `docker-compose.yml` is present and runs OR README has clear manual setup steps | Vishaal | [ ] |
| 63 | No API keys, Supabase passwords, or `.env` secrets committed to the repo | Vishaal | [ ] |
| 64 | `requirements.txt` in `/backend` is up to date and matches actual imports | Vishaal | [ ] |
| 65 | Submission link filled at fossunited.org/fosshack/2026 before 5 PM IST Mar 31 | Vishaal | [ ] |

---

## 8. Required Output Format from Antigravity

After running all tests, Antigravity must return a report in exactly this format:

```
=== SAFEWALK QA REPORT ===
Date: [date]
Tester: Antigravity (AI QA Agent)

SUMMARY
Total Tests:    65
Passed:         [N]
Failed:         [N]
Blocked:        [N]  (tests that could not run due to a blocker)
Pass Rate:      [N]%

VERDICT: [ GO / NO-GO ]
(GO = all P0 tests pass + pass rate >= 90%)

FAILURES
[Test #] | [Test Name] | Root Cause | Suggested Fix

BLOCKERS
List any tests that could not be executed and why.

NOTES FOR ARUN
Any observations, risks, or things to double-check before submission.
```

---

## 9. Bug Log — Arun Fills This In

| # | Severity | Description | Root Cause | Owner | Status |
|---|---|---|---|---|---|
| 1 | | | | | [ ] Open [ ] Fixed [ ] Verified |
| 2 | | | | | [ ] Open [ ] Fixed [ ] Verified |
| 3 | | | | | [ ] Open [ ] Fixed [ ] Verified |
| 4 | | | | | [ ] Open [ ] Fixed [ ] Verified |
| 5 | | | | | [ ] Open [ ] Fixed [ ] Verified |
| 6 | | | | | [ ] Open [ ] Fixed [ ] Verified |
| 7 | | | | | [ ] Open [ ] Fixed [ ] Verified |
| 8 | | | | | [ ] Open [ ] Fixed [ ] Verified |

---

*Random Forest Rangers 🌲 — Ship SafeWalk. Make Every Walk Safer. 🚶*
*FOSS Hack 2026 · Submit before 5 PM IST March 31 · github.com/Vishaal1409/safewalk*
