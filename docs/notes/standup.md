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
