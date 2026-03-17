# SafeWalk QA Report (March 13) – Arun
**Advanced Testing & Bug Detection**

## Edge Case Testing ✔
- **Radius `0`**: Correctly filters very strictly (Nearby hazards: 12, Score: 90.4)
- **Radius `5`**: Expanding the radius increases hazard count effectively (Nearby hazards: 18, Score: 85.6)
- **Radius `10`**: Max hazards captured smoothly (Nearby hazards: 18, Score: 85.6)
- **Unusual Coordinates (`lat 0`, `lon 0`)**: Safely handled with logical fallbacks. Did not crash. (Nearby hazards: 0, Score: 100.0)

## Check Map Behaviour ✔
- ✅ Markers appear accurately at their coordinates.
- ✅ Popups correctly open on click with all expected data points.
- ✅ Hazard photos (if provided) are handled without breaking popups.
- ✅ Coordinates from API and Map accurately match.

## Detailed Bug Reports & UI Improvements 🐞

### 1. Hazard Type Case Formatting Inconsistency (Bug)
While the sidebar dropdown renders hazard types in Title Case (e.g., "Open Manhole"), the actual popup renders them based on their raw database string values, which are sometimes lowercase or snake_case (e.g., `other`, ` manhole`, `broken_footpath`). The text in the popup header should be normalized/Title Cased for display consistency.

### 2. Markdown Rendering Issue in Sidebar (Bug)
There is a rendering issue in the hazard cards within the sidebar. Sometimes, raw string representations of markdown styles (like `** manhole**`) are literally rendered rather than visually converted to bold text.

### 3. Missing 'Confirm' Action inside Map Popups (Improvement)
Currently, a user has to find a hazard on the map, then scroll through the sidebar to find the corresponding card to hit "Confirm ✅". To improve UX, a "Confirm Flag" button should be added directly inside the leaflet map popups so users can confirm hazards geographically.

### 4. Scroll Interference UX (Improvement)
When scrolling down the full Streamlit dashboard page, if the mouse hovers over the Leaflet map container, it hijacks the page scroll and starts scrolling/zooming the map instead. This can be frustrating. A fix would be requiring a modifier key (like `Ctrl` + Scroll) inside the map config, or simply turning map scrolling off entirely and relying on +/- buttons.
