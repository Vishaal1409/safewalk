# SafeWalk Design Notes

## Overview
SafeWalk is a mobile-first safety navigation application designed to help users identify hazards and choose safer walking routes using community-reported data.

The interface allows users to:
- View hazards on a map
- Report hazards in real time
- Compare normal routes vs safer routes

The design focuses on **simple navigation, clear hazard visibility, and quick reporting**.

---

# App Screens

## Screen 1 — Map View
The Map View acts as the **main dashboard** of the SafeWalk application.

Features:
- Interactive map displaying hazard markers
- Safety score indicator
- Hazard count and confirmed hazard count
- Hazard filters (Manhole, Flood, Light, Path)
- Floating **"+" button** to report a hazard
- Bottom navigation bar

Hazards are shown directly on the map using colored markers.

---

## Screen 2 — Report Hazard Form
This screen allows users to **report hazards they encounter**.

Fields included:
- Hazard type selector
- Hazard description
- Reporter name
- Photo upload option
- GPS-based location detection
- Submit Hazard Report button

Supported hazard types:
- Manhole
- Flooding
- No Streetlight
- Broken Footpath
- Unsafe Area
- Accessibility Issue

---

## Screen 3 — Route Result
This screen displays **navigation options based on safety**.

Features:
- Map displaying the route
- Route comparison cards
- Hazard warnings along routes
- "Start Safe Navigation" button

Example comparison:

Normal Route  
- Distance: 1.2 km  
- Time: 15 mins  
- Hazards: 3  

SafeWalk Route  
- Distance: 1.5 km  
- Time: 18 mins  
- Hazards: 0  

The SafeWalk route prioritizes **safety over distance**.

---

# Completed Screens
All 3 wireframes completed by **Ishitha — March 10, 2026**.

Final wireframes updated with **Shruthika's detailed mobile layout improvements**.

---

# Colour Codes

## Primary UI Colours
- Dark Pink Header: `#9D174D`
- Hot Pink Buttons: `#DB2777`
- Light Pink Background: `#FCE7F3`

## Hazard Indicators
- Red Hazard Marker (High Risk): `#DC2626`
- Orange Marker (Medium Risk): `#D97706`
- Blue Marker (Low Risk): `#3B82F6`

## Navigation Indicators
- Green Safe Route: `#16A34A`

## Text Colours
- Dark Gray Text: `#334155`
- Medium Gray Subtext: `#64748B`

---

# Figma Design Link
SafeWalk Wireframe:

https://www.figma.com/design/GOZJallbNpSrONZJk2yvJs/safewalk-wireframe?node-id=28-139&t=HQrlX5D1dLX6RVnJ-1