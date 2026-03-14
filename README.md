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

- **Frontend:** Streamlit + Folium + OpenStreetMap
- **Backend:** Python + FastAPI
- **Database:** PostgreSQL + PostGIS (via Supabase)
- **Routing:** OSRM / pgRouting
- **Auth:** JWT tokens
- **Infrastructure:** Supabase (cloud hosted)

---

## 🚀 Quick Start

**Prerequisites:** Python 3.x installed.

```bash
# 1. Clone the repo
git clone https://github.com/Vishaal1409/safewalk.git
cd safewalk

# 2. Copy environment config
cp .env.example .env
# Add your Supabase keys to .env

# 3. Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# 4. Install frontend dependencies
pip install -r frontend/requirements.txt

# 5. Run the backend
cd backend
uvicorn src.main:app --reload

# 6. In a new terminal, run the frontend
cd frontend
streamlit run app.py
```

The API runs on `http://localhost:8000` and the frontend opens automatically at `http://localhost:8501`.

---

## 📁 Project Structure

```
safewalk/
├── backend/              # Python + FastAPI
│   ├── src/
│   │   ├── routes/       # hazards.py, auth.py
│   │   ├── models/       # hazard.py, user.py
│   │   └── services/     # safety_score.py, route_engine.py
│   └── requirements.txt
├── frontend/             # Streamlit app
│   └── app.py
├── docs/
│   └── architecture.png
├── .env.example
├── .gitignore
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
- [Folium](https://python-visualization.github.io/folium/) — Python map visualisation library
- [Streamlit](https://streamlit.io/) — open-source Python web framework
- [FastAPI](https://fastapi.tiangolo.com/) — modern Python API framework
- [Supabase](https://supabase.com/) — open-source Firebase alternative
- [FOSS United](https://fossunited.org/) for organising FOSS Hack 2026

---

<p align="center">Made with ❤️ for safer streets in India • Random Forest Rangers 🌲</p>
