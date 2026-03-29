# SafeWalk Project Notes

## Standup Notes - March 7, 2026

**What did we accomplish today?**
**Arun:**
- **Backend Infrastructure**: Bootstrapped the Python environment with FastAPI, Uvicorn, Python-Multipart, and Pillow.
- **API Development**: 
  - Implemented the `/` root health check endpoint.
  - Created the `POST /hazards` endpoint to receive report data (type, description, location, user info).
  - Added strict server-side image validation using Pillow to ensure only valid images are accepted before uploading them to storage.
- **Testing**: Validated endpoints locally and simulated API requests, verifying both valid image uploads and error handling for invalid files.
- **Repository Setup**:
  - Added `.venv` and `__pycache__` to `.gitignore`.
  - Generated a clean `requirements.txt` for backend dependencies.
  - Updated the `README.md` setup section with clearer instructions for the backend.
  - Committed and pushed all foundational backend code to the repository.
- **Project Management**: Installed and authenticated the GitHub CLI (`gh`). Created custom labels (`backend`, `frontend`, `design`) and generated all 10 project tracking issues directly on the GitHub repository.

**What's next?**
- Integrate Supabase to store Hazard and User data (Issue #1).
- Connect the validated image from the `POST /hazards` endpoint to the Supabase Storage bucket (Issue #8).
- Scaffold the React frontend and map out the Leaflet UI (Issue #3 & #4).

**Any blockers?**
- None at the moment! The project foundation is solid and ready for the next phase.

## Standup Notes - March 14, 2026

**What did we accomplish today?**
**Arun:**
- **Quality Assurance & Stress Testing**: Conducted rigorous backend API testing on the `/safety-score` and `/confirm` endpoints testing boundaries (e.g., 50km radius) and concurrent spam confirmations without locks.
- **Frontend Bug Hunting**: Utilized browser automation to verify the Leaflet map state, identifying a major decoupling incident where markers and metric cards failed to load backend data.
- **GitHub Issue Automation**: Translated the findings from 2 days of QA reports into a bash script, automatically generating and labelling 10 native issues on the GitHub repository using the `gh` CLI.
- **Frontend Bug Fixes**:
  - Removed state-blocking `@st.cache_data` caching from the `fetch_hazards` pipeline, restoring real-time map data syncs.
  - Mitigated an HTML injection vulnerability inside Folium popups using `html.escape()`.
  - Implemented `folium.plugins.MarkerCluster` to gracefully collapse overlapping hazard coordinates.
- **Documentation**: Generated the `stress_testing_qa_march14.md` and `frontend_bugfixes_march14.md` reports tracking the root causes of the bugs and mapped solutions. All changes successfully committed to `main`.

**What's next?**
- Begin squashing the remaining UI/UX issues logged in the GitHub repository.
- Implement rate limiting or a `user_id` check on the `/confirm` endpoint to prevent spam inflation.

**Any blockers?**
- None currently. The map is rendering correctly and frontend/backend communication is verified under stress loads.

## Standup Notes - March 15, 2026

**What did we accomplish today?**
**Arun:**
- **Final QA Checklist**: Created a comprehensive QA checklist (`docs/reports/qa_checklist_march15.md`) covering functional tests, API endpoint validation, and input validation checks across the entire SafeWalk application.
- **QA Results**: Verified all 6 core features — map loading, hazard marker display, popup functionality, image loading, confirm count updates, and safety score calculations — all passing.
- **Improvement Suggestions**: Documented 3 actionable improvements:
  1. Rate-limit the `/confirm` endpoint to prevent spam confirmations.
  2. Add hazard auto-archival for stale reports older than 30 days.
  3. Sync `ALLOWED_TYPES` between backend and frontend (the `"other"` type is missing from the backend).

**What's next?**
- Perform hazard density testing to validate the route safety algorithm under varying hazard concentrations.

**Any blockers?**
- None. No critical bugs remain after the final QA sweep.

## Standup Notes - March 16, 2026

**What did we accomplish today?**
**Arun:**
- **Hazard Density Testing**: Analyzed how hazard density affects route safety scores across three scenarios — low (0–2 hazards), medium (3–5 hazards), and high (8+ hazards) density areas. Full report at `docs/reports/hazard_density_testing_march16.md`.
- **Algorithm Validation**: Confirmed the scoring algorithm correctly differentiates density levels:
  - Low density → 90–100 (✅ Safe)
  - Medium density → 60–80 (⚠️ Use Caution)
  - High density → 0–40 (🔴 High Risk)
- **Key Findings**: Night-time uplift (1.5× for `no_light`), community confirmation boost (+10% per confirm), and recency decay (old hazards weighted at 10%) all function as designed.
- **Edge Case Verified**: Score correctly floors at 0 when total danger exceeds 100 — no negative scores produced.

**What's next?**
- Address the 3 improvement suggestions from the QA checklist (rate limiting, auto-archival, type sync).
- Begin final pre-deployment checks and documentation updates.

**Any blockers?**
- None. The route safety algorithm is validated and no critical bugs remain.
## Standup Notes - March 23, 2026

**What did we accomplish today?**
**Arun:**
- **Frontend Migration**: Successfully migrated the fragile Streamlit frontend to a robust, static HTML/JS architecture (`index.html`, `app.js`).
- **UI Redesign**: Implemented a complete frontend redesign featuring a modern Dark Theme, a Heatmap view, tabbed navigation, and a dynamic hazard grid.
- **QA Automation**: Built out the `FINAL_QA_TEST` suite (`01_full_stress_test.sh`), creating automated, reusable curl tests to rigorously validate backend API contracts under stress.
- **Regression Testing**: Executed the full post-migration QA sprint, proving the FastAPI backend handled the migration seamlessly with **zero regressions**.

**What's next?**
- Transition deployment infrastructure (Docker) from Streamlit to standard static HTML serving.
- Address any subtle geometry or security edge-cases lingering in the backend code.

**Any blockers?**
- None. The migration was a complete success and the decoupling of frontend/backend is finished.

## Standup Notes - March 24, 2026

**What did we accomplish today?**
**Arun:**
- **Critical Bug Fixes**: Identified and resolved 4 major backend bugs during the post-migration QA phase:
  1. **Hazard Sorting**: Fixed a contradiction in `/hazards` where negated sort keys with `reverse=False` caused unexpected ascending sorts. Now predictably sorts highest confirmed → newest first.
  2. **JWT Expiration**: Added a 24-hour `exp` claim to JWT tokens in `auth.py` so tokens no longer live forever.
  3. **Password CPU DoS**: Heavily clamped string lengths in `RegisterRequest` and `LoginRequest` (e.g., max 128 chars for passwords) to prevent bcrypt CPU starvation attacks, and added an alphanumeric validator for usernames.
  4. **Route Geometry Fix**: Replaced the flawed triangle-inequality (ellipse) hazard detection with a true perpendicular point-to-segment corridor check in `route_engine.py`.
- **Testing Validation**: Added `backend/test/test_route_engine.py` with 6 detailed test cases proving the geometry fix successfully rejects hazards far off the route axis that the old ellipse method mistakenly caught.
- **Docker Re-Architecture**:
  - Reorganized all Docker files into a dedicated `docker/` folder.
  - Built a new `frontend.Dockerfile` and `nginx.conf` to serve the static HTML and reverse-proxy `/api/` traffic to the backend.
  - Upgraded the backend image to `python:3.11.9-slim` and synced `requirements.txt`.
- **Documentation**: Updated `startup.md` to cleanly reflect the new architecture (removing all legacy Streamlit instructions).

**What's next?**
- Monitor error logs on the newly migrated HTML frontend to ensure stable API connections.
- Final launch preparations.

**Any blockers?**
- None. The backend is secure, stable, decoupled, and containerized successfully.

## Standup Notes - March 23, 2026

**What did we accomplish today?**
**Arun:**
- **Frontend Migration**: Successfully migrated the fragile Streamlit frontend to a robust, static HTML/JS architecture (`index.html`).
- **UI Redesign**: Implemented a complete frontend redesign featuring a modern Dark Theme, a Heatmap view, tabbed navigation, and a dynamic hazard grid.
- **QA Automation**: Built out the `FINAL_QA_TEST` suite (`01_full_stress_test.sh`), creating automated, reusable curl tests to rigorously validate backend API contracts under stress.
- **Regression Testing**: Executed the full post-migration QA sprint, proving the FastAPI backend handled the migration seamlessly with **zero regressions**.

**What's next?**
- Transition deployment infrastructure (Docker) from Streamlit to standard static HTML serving.
- Address any subtle geometry or security edge-cases lingering in the backend code.

**Any blockers?**
- None. The migration was a complete success and the decoupling of frontend/backend is finished.

## Standup Notes - March 24, 2026

**What did we accomplish today?**
**Arun:**
- **Critical Bug Fixes**: Identified and resolved 4 major backend bugs during the post-migration QA phase:
  1. **Hazard Sorting**: Fixed a contradiction in `/hazards` where negated sort keys with `reverse=False` caused unexpected ascending sorts. Now predictably sorts highest confirmed → newest first.
  2. **JWT Expiration**: Added a 24-hour `exp` claim to JWT tokens in `auth.py` so tokens no longer live forever.
  3. **Password CPU DoS**: Heavily clamped string lengths in `RegisterRequest` and `LoginRequest` (e.g., max 128 chars for passwords) to prevent bcrypt CPU starvation attacks, and added an alphanumeric validator for usernames.
  4. **Route Geometry Fix**: Replaced the flawed triangle-inequality (ellipse) hazard detection with a true perpendicular point-to-segment corridor check in `route_engine.py`.
- **Testing Validation**: Added `backend/test/test_route_engine.py` with 6 detailed test cases proving the geometry fix successfully rejects hazards far off the route axis that the old ellipse method mistakenly caught.
- **Docker Re-Architecture**:
  - Reorganized all Docker files into a dedicated `docker/` folder.
  - Built a new `frontend.Dockerfile` and `nginx.conf` to serve the static HTML and reverse-proxy `/api/` traffic to the backend.
  - Upgraded the backend image to `python:3.11.9-slim`.
- **Documentation**: Updated `startup.md` to cleanly reflect the new architecture (removing all legacy Streamlit instructions).

**What's next?**
- Monitor error logs on the newly migrated HTML frontend to ensure stable API connections.
- Final launch preparations.

**Any blockers?**
- None. The backend is secure, stable, decoupled, and containerized successfully.

**QA & Testing Updates (Just Now):**
- **Supabase Data Integration:** ✅ Passed. Submitted a dummy hazard report; successfully updated the database (hazard count incremented) and rendered the new marker on the map in real-time.
- **Heatmap Toggle:** ✅ Passed. Toggled the heatmap ON; the visual heatmap overlay correctly rendered on the map.
- **Image Upload:** 🔴 Blocked/Failed. Attempted to upload an image during report submission, but the "Click to upload photo" UI element is a bare `<label>` without a focusable `<input type="file">`, preventing programmatic file uploads and posing an accessibility issue. Fixing this HTML structure is required.
