# Frontend Bug Fixes (March 14)

This document outlines the bug fixes applied to `frontend/app.py` to resolve critical mapping application issues.

## 1. Map UI Sync (Caching Issue)
**Problem**: The "Confirmations" text and total hazard counts were not updating in real-time when a hazard was confirmed or reported.
**Root Cause**: The `fetch_hazards()` API call was heavily cached using Streamlit's `@st.cache_data(ttl=30)` decorator. This caused the UI to occasionally serve stale data from memory when re-rendering components.
**Fix**: Removed the `@st.cache_data` decorator from `fetch_hazards()`. The app now executes fresh API fetches ensuring accurate real-time data syncs on every user action.

## 2. Popup Rendering Event Trigger
**Problem**: Map popups completely failed to open upon clicking a marker if the hazard description contained certain quotes or raw text styles.
**Root Cause**: Folium generates marker popups by injecting the strings into raw HTML templates. User descriptions containing unsafe characters broke the underlying Leaflet JavaScript execution, silently failing the click event listeners.
**Fix**: Imported the standard library `html` module and added `html.escape()` around the `description` and `reported_by` fields securely sanitizing the text before injecting them into the Folium HTML template. 

## 3. Partial Set of Markers (Overlapping)
**Problem**: It visually appeared that only a partial set of markers was loading on the map, despite the backend querying and returning 20+ active hazard records.
**Root Cause**: Many hazard stress-test reports shared the exact same GPS coordinates (`13.0827, 80.2707`). Leaflet was rendering all of them mathematically stacked on top of each other, cleanly obscuring all but the top marker.
**Fix**: Imported and implemented `folium.plugins.MarkerCluster`. Markers are now dynamically added to a clustered group layer instead of directly to the map instance. Overlapping coordinates are automatically aggregated into interactive clusters that expand on click.
