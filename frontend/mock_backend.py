"""
SafeWalk — Mock FastAPI Backend
Run with: uvicorn mock_backend:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Literal, Optional
import uuid

app = FastAPI(title="SafeWalk API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HazardType = Literal["poor_lighting", "broken_infrastructure", "crime_hotspot", "flood_water", "pothole"]

# ── In-memory store ──
hazards_db: list[dict] = [
    {"id": 1,  "type": "poor_lighting",        "lat": 12.9716, "lon": 77.5946, "severity": 1, "description": "Street lights out near bus stop",    "reported_at": "2026-03-07T21:30:00"},
    {"id": 2,  "type": "crime_hotspot",         "lat": 12.9750, "lon": 77.5990, "severity": 3, "description": "Multiple incidents reported",         "reported_at": "2026-03-08T01:15:00"},
    {"id": 3,  "type": "broken_infrastructure", "lat": 12.9680, "lon": 77.5900, "severity": 2, "description": "Pothole blocking footpath",            "reported_at": "2026-03-07T18:00:00"},
    {"id": 4,  "type": "flood_water",           "lat": 12.9700, "lon": 77.6010, "severity": 2, "description": "Waterlogging after rain",              "reported_at": "2026-03-08T06:45:00"},
    {"id": 5,  "type": "poor_lighting",         "lat": 12.9730, "lon": 77.5870, "severity": 1, "description": "Dark alley with no lights",            "reported_at": "2026-03-08T20:00:00"},
    {"id": 6,  "type": "crime_hotspot",         "lat": 12.9760, "lon": 77.5950, "severity": 2, "description": "Bag snatching reported",               "reported_at": "2026-03-07T23:00:00"},
    {"id": 7,  "type": "broken_infrastructure", "lat": 12.9690, "lon": 77.5970, "severity": 1, "description": "Broken railing on bridge",             "reported_at": "2026-03-08T10:00:00"},
    {"id": 8,  "type": "pothole",               "lat": 12.9724, "lon": 77.5961, "severity": 2, "description": "Large pothole near junction",          "reported_at": "2026-03-08T08:30:00"},
    {"id": 9,  "type": "pothole",               "lat": 12.9705, "lon": 77.5932, "severity": 3, "description": "Deep crater blocks half the road",     "reported_at": "2026-03-08T07:15:00"},
    {"id": 10, "type": "pothole",               "lat": 12.9742, "lon": 77.5983, "severity": 1, "description": "Small pothole on footpath",            "reported_at": "2026-03-07T16:00:00"},
]


class HazardCreate(BaseModel):
    type: HazardType
    lat: float
    lon: float
    severity: int = 1
    description: str
    reported_at: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok", "service": "SafeWalk API"}


@app.get("/hazards")
def get_hazards(type: Optional[HazardType] = None, min_severity: int = 1):
    result = hazards_db
    if type:
        result = [h for h in result if h["type"] == type]
    result = [h for h in result if h["severity"] >= min_severity]
    return result


@app.get("/hazards/{hazard_id}")
def get_hazard(hazard_id: int):
    for h in hazards_db:
        if h["id"] == hazard_id:
            return h
    raise HTTPException(status_code=404, detail="Hazard not found")


@app.post("/hazards", status_code=201)
def create_hazard(hazard: HazardCreate):
    new_id = max((h["id"] for h in hazards_db), default=0) + 1
    entry = hazard.dict()
    entry["id"] = new_id
    entry["reported_at"] = entry["reported_at"] or datetime.utcnow().isoformat()
    hazards_db.append(entry)
    return entry


@app.delete("/hazards/{hazard_id}")
def delete_hazard(hazard_id: int):
    global hazards_db
    before = len(hazards_db)
    hazards_db = [h for h in hazards_db if h["id"] != hazard_id]
    if len(hazards_db) == before:
        raise HTTPException(status_code=404, detail="Hazard not found")
    return {"deleted": hazard_id}
