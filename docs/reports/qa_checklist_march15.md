# SafeWalk QA Checklist — March 15, 2026

**Prepared by:** Arun  
**Status:** ✅ Final QA Sweep Complete

---

## Functional Checklist

| #  | Feature                        | Status | Notes                                                                 |
|----|--------------------------------|--------|-----------------------------------------------------------------------|
| 1  | Map loads correctly            | ✔ Pass | Folium map renders on `CartoDB dark_matter` tiles with Chennai center |
| 2  | Hazard markers display         | ✔ Pass | Markers load via `MarkerCluster`; icons match `HAZARD_CONFIG` types   |
| 3  | Hazard popup works             | ✔ Pass | Popups show type label, description, reporter, coords, confirm count  |
| 4  | Image loads in popup           | ✔ Pass | `photo_url` images render inside popup with `max-height: 120px`       |
| 5  | Confirm count updates          | ✔ Pass | `POST /hazards/{id}/confirm` increments `confirmed_count` correctly   |
| 6  | Safety score changes correctly | ✔ Pass | Score decreases as hazards increase; weighted by type, recency, time  |

## API Endpoint Checklist

| Endpoint                        | Method | Status | Notes                                         |
|---------------------------------|--------|--------|-----------------------------------------------|
| `/`                             | GET    | ✔ Pass | Health check returns `status: online`          |
| `/hazards`                      | GET    | ✔ Pass | Returns all hazards; optional location filter  |
| `/hazards`                      | POST   | ✔ Pass | Validates type, coords, description; uploads photo to Supabase Storage |
| `/hazards/{id}/confirm`         | POST   | ✔ Pass | Increments confirmed count atomically          |
| `/safety-score`                 | GET    | ✔ Pass | Returns score, label, and nearby hazard count  |

## Input Validation Checklist

| Validation                       | Status | Notes                                             |
|----------------------------------|--------|---------------------------------------------------|
| Invalid hazard type rejected     | ✔ Pass | Server returns 400 for types not in `ALLOWED_TYPES` |
| Latitude bounds checked          | ✔ Pass | Rejects values outside `[-90, 90]`                |
| Longitude bounds checked         | ✔ Pass | Rejects values outside `[-180, 180]`              |
| Empty description rejected       | ✔ Pass | Server returns 400 for blank descriptions         |
| Invalid image file rejected      | ✔ Pass | Pillow `verify()` catches non-image uploads       |
| HTML injection in popup escaped  | ✔ Pass | `html.escape()` applied to description & reporter |

---

## Improvement Suggestions

### 1. Rate-Limit the `/confirm` Endpoint
The confirmation endpoint currently allows unlimited confirmations from any source. A single user can spam-confirm a hazard indefinitely, inflating its `confirmed_count` and artificially degrading the safety score. **Implement a `user_id` or IP-based one-confirm-per-user guard** to ensure community verification integrity.

### 2. Add Hazard Expiry / Auto-Archival
Hazards reported weeks or months ago may no longer be relevant (e.g. a pothole that was repaired). The recency factor in the scoring algorithm already down-weights old reports, but stale markers still clutter the map. **Add an auto-archive mechanism** (e.g., hazards older than 30 days with no recent confirmations are hidden from the map but retained in the database).

### 3. Expand the `ALLOWED_TYPES` List and Sync with Frontend
The backend's `ALLOWED_TYPES` list does not include `"other"`, but the frontend `HAZARD_CONFIG` does. This means a user selecting "Other" in the UI will receive a 400 error on submission. **Sync both lists** and consider allowing user-submitted custom types with moderation.
