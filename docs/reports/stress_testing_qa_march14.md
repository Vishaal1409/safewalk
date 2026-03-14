# SafeWalk Stress Testing & QA Report (March 14) – Arun

## Extreme Safety Score Testing ✔
Tested boundary cases for the `radius` parameter at `[0, 0.01, 5, 10, 50]` km:
- **Radius 0 / 0.01**: Strict filtering works correctly. (Hazard count: 12, Score: 90.4 -> Safe)
- **Radius 5+**: Expanded filtering works correctly, hitting the ceiling of currently reported hazards in the test area. (Hazard count: 18, Score: 85.23 -> Safe)
- **Conclusion**: The backend safety score logic scales appropriately without breaking at edge cases.

## Duplicate Confirmation Test ✔
- Confirmed a single hazard 10 times consecutively via the `/confirm` API endpoint.
- **Result**: The API correctly incremented the confirmation count linearly (`1, 2, ..., 10`) without failing or throwing race-condition errors.
- **Improvement**: *The API lacks rate limiting or user-based validation (e.g., one user = one confirm), allowing confirmation spam. Consider adding a `user_id` validation to the confirmation logic.*

## Map Consistency Tests & Bug Hunt 🐞
A comprehensive visual QA sweep of the Streamlit frontend revealed significant syncing and presentation bugs:

### 1. Critical Map Rendering Bug (Map is Empty)
Despite the backend reporting 18 nearby hazards (and the Safety Score reflecting a decrease from 89.9 to 88.9 upon a new report submission), **ZERO hazard markers appear on the Leaflet map.** The map simply fails to render the data points fetched from the backend.

### 2. Summary Metric Decoupling (Dashboard Shows 0)
The metric cards at the top of the dashboard for "Hazards" and "Confirmed" consistently display **"0"**, completely ignoring the active hazards queried by the Safety Score calculator, highlighting a decoupling event in the Streamlit state.

### 3. Sidebar Hazards Sync Issue
The "Confirm Hazards" section in the sidebar indicates "No hazards reported yet. Be the first!" This means the sidebar is also failing to fetch or render the active dataset from the application cache or API.

### 4. Hazard Type UI Mismatch
The 'other' hazard type (which was reported via API and requested for testing) **does not exist** in the Streamlit UI "Hazard Type" dropdown. This means users cannot actively select 'other' even though the backend supports it.

### 5. UI Slider Restriction
The frontend radius slider strictly limits testing to values between `0.5km` and `5.0km`. To perform true edge case testing (like `radius=50`), users must bypass the UI and hit the API directly. Consider expanding the slider bounds or allowing manual raw input.
