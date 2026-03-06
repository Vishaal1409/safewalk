# 🚶 SafeWalk
### Crowdsourced Pedestrian Safety Navigation

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![FOSS Hack 2026](https://img.shields.io/badge/FOSS%20Hack-2026-teal.svg)](https://fossunited.org/fosshack/2026)
[![Built with OpenStreetMap](https://img.shields.io/badge/Maps-OpenStreetMap-blue.svg)](https://www.openstreetmap.org/)

> **Navigation apps show you the fastest route. SafeWalk shows you the safest one.**

SafeWalk is a crowdsourced map layer that lets users report pedestrian hazards — broken sidewalks, open manholes, flooded streets, poor lighting, and more — and receive safety-optimised walking routes that avoid them.

Built for Indian cities. Built for everyone who walks.

---

## 🎯 The Problem

Every year in cities like Chennai, Mumbai, and Bengaluru, people fall into open drains, get stranded on flooded roads, or are forced to walk through unsafe areas at night. Google Maps will happily route you through a dark, broken-footpath alley — because it doesn't know any better.

**SafeWalk does.**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🕳 **Hazard Reporting** | Report broken footpaths, open manholes, waterlogging, no streetlights, and more |
| 🗺 **Live Hazard Map** | All reports visualised on OpenStreetMap with colour-coded hazard icons |
| 🌟 **Street Safety Score** | Algorithm scores street segments based on nearby hazard density and type |
| 🔀 **Safer Route Mode** | Route planner avoids high-hazard streets, even if the path is slightly longer |
| ♿ **Wheelchair Mode** | Routes that avoid steps, broken footpaths, and accessibility blockers |
| ✅ **Community Verification** | Other users confirm reports to improve accuracy; unconfirmed reports expire in 7 days |

---

## 🛠 Tech Stack

All tools are 100% open source.

- **Frontend:** React + Vite + Tailwind CSS + Leaflet.js + OpenStreetMap
- **Mobile:** Flutter
- **Backend:** Node.js + Express
- **Database:** PostgreSQL + PostGIS
- **Routing:** OSRM (self-hosted) / pgRouting
- **Auth:** JWT + bcrypt
- **Infrastructure:** Docker + Docker Compose

---

## 🚀 Quick Start

**Prerequisites:** Docker and Docker Compose installed.

```bash
# 1. Clone the repo
git clone https://github.com/Vishaal1409/safewalk.git
cd safewalk

# 2. Copy environment config
cp .env.example .env

# 3. Start everything
docker compose up --build

# 4. Open in browser
open http://localhost:5173
```

That's it! The API runs on `localhost:3000`, the frontend on `localhost:5173`.

---

## 📱 Mobile App (Flutter)

```bash
cd mobile
flutter pub get
flutter run
```

Set the API URL in `mobile/lib/config.dart` to point to your backend.

---

## 📁 Project Structure

```
safewalk/
├── backend/          # Node.js + Express API
│   ├── src/
│   │   ├── routes/   # hazards.js, auth.js, routes.js
│   │   ├── models/   # Hazard.js, User.js
│   │   └── services/ # safetyScore.js, routeEngine.js
│   └── Dockerfile
├── frontend/         # React + Vite + Tailwind
│   └── src/
│       ├── components/  # Map, HazardForm, RoutePanel
│       └── pages/       # Home, Report, Routes
├── mobile/           # Flutter app
│   └── lib/
│       └── screens/  # MapScreen, ReportScreen
├── db/
│   └── init.sql      # PostGIS schema
├── docs/
│   └── architecture.png
├── docker-compose.yml
├── LICENSE
└── README.md
```

---

## 🗺 How It Works

1. **A user spots a hazard** (e.g. open manhole on Velachery Main Rd, Chennai)
2. **They open SafeWalk**, tap the location on the map, select hazard type, optionally upload a photo, and submit
3. **The hazard appears on the community map** instantly
4. **Other users walking nearby see the hazard icon** and are warned
5. **When requesting a route**, SafeWalk queries the safety score of each street segment and returns a path that avoids high-hazard areas
6. **Community members confirm or dispute the report** — confirmed reports get higher weight in the safety algorithm

---

## 🧮 Safety Score Algorithm

Each street segment gets a score (0–100, higher = safer) based on:

- Number of active hazard reports within 50m
- Hazard severity weights (open manhole > broken footpath)
- Report recency (newer = higher weight)
- Community confirmation count
- Time of day (lighting hazards weighted higher at night)

The route engine uses these scores as edge weights to find the safest path.

---

## 🤝 Contributing

This is a FOSS Hack 2026 project. Contributions, issues, and feature requests are welcome!

1. Fork the repo
2. Create your branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push and open a PR

---

## 👥 Team — Random Forest Rangers 🌲

| Name | Role |
|---|---|
| Vishaal S | Backend, Database & Safety Algorithm |
| Arun Balaji | Backend, Documentation & Project Manager |
| Shruthika Nair | Frontend & Map Interface |
| Ishitha Ilan | UI/UX Design & Accessibility |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgements

- [OpenStreetMap](https://www.openstreetmap.org/) contributors
- [Leaflet.js](https://leafletjs.com/) — open-source map library
- [OSRM](http://project-osrm.org/) — open-source routing machine
- [PostGIS](https://postgis.net/) — geospatial PostgreSQL extension
- [FOSS United](https://fossunited.org/) for organising FOSS Hack 2026

---

<p align="center">Made with ❤️ for safer streets in India • Random Forest Rangers 🌲</p>
