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
