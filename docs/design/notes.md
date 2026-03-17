# SafeWalk — Design Notes

**Ishitha Ilan · UI/UX Design · Random Forest Rangers · FOSS Hack 2026**

---

## Overview

SafeWalk is a community-powered safety navigation platform that helps users avoid unsafe routes by identifying real-time hazards — open manholes, flooding, broken footpaths, and poorly lit areas.

It combines live hazard mapping, safety scoring, community reporting, and smart route comparison into a single clean mobile experience.

---

## Figma File

[safewalk-wireframe](https://www.figma.com/design/GOZJallbNpSrONZJk2yvJs/safewalk-wireframe)

Includes: Map View · Report Screen · Route Comparison · Error States

---

## App Screens

### 01 · Map View
The home screen. Shows nearby hazards on a live map with safety context.

**Features**
- Interactive map with hazard markers and clustering
- Filter chips by hazard type + confirmed-only toggle
- 📍 Use current location button
- ➕ Quick report FAB button
- Hazard legend (color-coded)

**Displays**
- Safety Score (0–100) and status label (Safe / Moderate / Dangerous)
- Total hazards + confirmed hazard count

**Map Marker Colors**

| Color | Hazard Type |
|-------|-------------|
| 🔴 Red | Open Manhole |
| 🔵 Blue | Flooding |
| 🟠 Orange | Broken Footpath |
| 🟣 Purple | No Streetlight |
| 🔺 Dark Red | Unsafe Area |
| ⚪ Gray | No Wheelchair Access |

**Marker Popup Shows**
- Hazard type (bold + colored)
- Description
- Reporter name
- Confirmation count (large, prominent)
- Coordinates
- Photo (if uploaded)

---

### 02 · Report Hazard
Lets users report a hazard in seconds.

**Features**
- Hazard type selector (6 icon buttons in bento grid)
- Description and name input fields
- Photo upload (JPG / PNG, max 5MB)
- GPS auto-fill with manual coordinate override
- Map tap to set location

**Feedback States**

| State | Message |
|-------|---------|
| ✅ Success | "Hazard Reported! Thank you." |
| ⚠️ API Error | "Couldn't connect — backend offline" |
| ❗ Validation | "Description is required" / "Name is required" |

---

### 02b · Error State
Same as Report screen but with red borders on empty required fields and inline error text under each field. Demonstrates full validation UX for demo purposes.

---

### 03 · Route Comparison
Shows two routes side by side so users can choose the safer one.

**Route Cards**

| | 🔴 Normal Route | 🟢 SafeWalk Route |
|-|----------------|------------------|
| Distance | 1.2 km | 1.5 km |
| Time | 15 mins | 18 mins |
| Hazards | 3 on route | 0 hazards |
| Status | — | ✅ Recommended |

**Also shows**
- Safety Score: 92 / 100
- Time comparison tile with "+3 min · ✅ Safer Route Recommended" callout
- Hazard breakdown list — each hazard with type, color dot, and location reason:
  - 🔴 Open Manhole — Velachery Rd
  - 🔵 Flooding — Anna Salai
  - 💡 No Streetlight — Side street

**Design note:** Safety > shortest distance. The longer route is always highlighted as recommended when it avoids hazards.

---

## UX Flow

```
Open app → See map + hazards
    ↓
Tap marker → View hazard popup
    ↓
Tap + → Report new hazard → Submit → Success / Error feedback
    ↓
Search route → Compare Normal vs SafeWalk → Start navigation
```

---

## Color System

| Role | Hex | Where used |
|------|-----|------------|
| Black | `#1a1a1a` | Headers, buttons, active nav |
| Orange | `#ff6b35` | FAB, submit button, nav dot |
| Green | `#22c55e` | Safe route, success, 0 hazards |
| Red | `#ef4444` | Danger / Manhole |
| Orange-Red | `#f97316` | Broken path marker |
| Blue | `#3b82f6` | Flooding marker |
| Off-white | `#f5f3ee` | Phone background |
| Warm grey | `#edeae3` | Page background |

**Rule:** Red = danger, Blue = flooding, Orange = path issues — consistent across map markers, legend, route screen, and hazard breakdown everywhere.

---

## Design Principles

- **Clarity** — every element has one clear purpose
- **Safety-first** — risks are always visually prominent
- **Minimal effort** — reporting takes under 30 seconds
- **Community-driven** — confirmations increase reliability
- **Consistent** — same colors, same icons, same language everywhere

---

## UI Polish

- Hover effects on all interactive elements (chips, buttons, markers)
- Map markers staggered to prevent label overlap
- Bottom navigation bar on every screen — active tab bold/dark, inactive faded
- Popup card layout with proper spacing and type hierarchy
- Both success and error states fully designed (demo-proof)
- Field-level validation messages in error state

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Design | Figma |
| Frontend | Streamlit + Folium |
| Backend | FastAPI |
| Database | Supabase |

---

## Frontend Notes (for Shruthika)

The improved `app.py` includes:
- Form section dividers (Hazard Type / Details / Location)
- Hazard legend with section heading
- `st.success()` on successful submit
- `st.error()` on API failure or validation error
- All 6 hazard types with unique emoji, FontAwesome icon, and hex color
- `unsafe_area` uses black marker (distinct from manhole red)

---

*Last updated: March 17, 2026*