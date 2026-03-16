# SafeWalk Design Notes

## Overview
SafeWalk is a community-powered navigation app that helps users avoid unsafe walking routes by identifying hazards such as open manholes, flooding, broken footpaths, and poorly lit areas.

The UI is designed as a **mobile-first interface** with three primary screens.

---

# App Screens

## 1. Map View
Purpose: Display nearby hazards and the overall safety level of the area.

Features:
- Interactive map showing hazard markers
- Safety score indicator
- Hazard count and confirmation count
- Color-coded hazard markers
- Quick access to report hazards
- Legend explaining hazard types

Displayed information:
- Safety Score
- Total Hazards
- Confirmed Hazards
- Hazard locations on the map

Marker Colors:
- Red → Manhole
- Blue → Flooding
- Orange → Broken Footpath
- Purple → No Streetlight
- Dark Red → Unsafe Area
- Gray → No Wheelchair Access

---

## 2. Report Hazard Screen
Purpose: Allow users to report hazards in their surroundings.

Features:
- Hazard type selection
- Description input
- Photo upload
- Automatic GPS location detection
- Submit hazard report button

Hazard types available:
- Open Manhole
- Flooding
- No Streetlight
- Broken Footpath
- Unsafe Area
- No Wheelchair Access

The report is sent to the backend and stored in the Supabase database.

---

## 3. Route Result Screen
Purpose: Show the safest route between two locations.

Features:
- Visual route preview on a map
- Comparison between:
  - Normal Route
  - SafeWalk Route
- Distance and estimated time
- Hazard count on the route
- Highlight of the safest route

Displayed route information:

Normal Route
- Distance
- Travel Time
- Number of hazards

SafeWalk Route
- Distance
- Travel Time
- Hazards avoided
- Marked as the recommended route

Additional section:
- List of hazards detected on the normal route

Example:
- Open Manhole — Velachery Main Road
- Flooding — Anna Salai Junction

Action Button:
Start Safe Navigation

---

# Design Principles

The UI follows these principles:

- **Clarity:** Hazard information is easy to understand
- **Safety-first:** Safe routes are visually highlighted
- **Minimal interaction:** Reporting hazards takes only a few steps
- **Community-driven:** Hazard confirmation improves reliability

---

# Tools Used

Design Tool:
Figma

Frontend:
Streamlit + Folium

Backend:
FastAPI

Database & Storage:
Supabase

---

# Figma Wireframe

Figma Design Link:
https://www.figma.com/design/GOZJallbNpSrONZJk2yvJs/safewalk-wireframe

The wireframe includes the complete UI layout for:
- Map View
- Report Hazard
- Route Result