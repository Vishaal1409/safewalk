from src.services.route_engine import haversine_distance, get_hazards_along_route, calculate_route_safety
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import io
from PIL import Image, UnidentifiedImageError
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import uuid
from src.routes.auth import router as auth_router

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Allowed hazard types
ALLOWED_TYPES = ["manhole", "flooding", "no_light", "broken_footpath", "unsafe_area", "no_wheelchair_access"]

# Initialize the FastAPI app
app = FastAPI(title="SafeWalk API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Import safety score service
from src.services.safety_score import calculate_street_safety_score, get_safety_label

# 1. Health Check
@app.get("/")
def health_check():
    return {
        "status": "online",
        "message": "SafeWalk Backend is active!"
    }

# 2. Get hazards (with optional location filter)
@app.get("/hazards")
def get_hazards(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: float = 0.01
):
    """
    Fetch hazards from the database.
    If latitude and longitude are provided, return only hazards within the radius.
    Radius is in degrees (~0.01 ≈ 1 km).
    """
    try:
        # Fetch all hazards from Supabase
        response = supabase.table("hazards").select("*").execute()
        hazards = response.data or []

        # If no location filter → return everything
        if latitude is None or longitude is None:
            return {
                "status": "success",
                "message": "Hazards fetched successfully",
                "data": hazards,
                "count": len(hazards)
            }

        # Filter hazards near the location
        nearby_hazards = []
        for hazard in hazards:
            lat_diff = abs(hazard["latitude"] - latitude)
            lon_diff = abs(hazard["longitude"] - longitude)

            if lat_diff <= radius and lon_diff <= radius:
                nearby_hazards.append(hazard)

        return {
            "status": "success",
            "message": "Hazards fetched successfully",
            "data": nearby_hazards,
            "count": len(nearby_hazards)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Post a new hazard
@app.post("/hazards")
async def create_hazard(
    type: str = Form(...),
    description: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    reported_by: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    """Receives a hazard report and saves it to Supabase."""
    photo_url = None

    # Validate and clean inputs
    type = type.strip().lower()

    if type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid hazard type. Allowed types: {ALLOWED_TYPES}"
        )

    if not -90 <= latitude <= 90:
        raise HTTPException(
            status_code=400,
            detail="Invalid latitude. Must be between -90 and 90"
        )

    if not -180 <= longitude <= 180:
        raise HTTPException(
            status_code=400,
            detail="Invalid longitude. Must be between -180 and 180"
        )

    if not description.strip():
        raise HTTPException(
            status_code=400,
            detail="Description cannot be empty"
        )

    # Handle image upload
    if image:
        try:
            file_bytes = await image.read()

            # Validate it's a real image
            img = Image.open(io.BytesIO(file_bytes))
            img.verify()

            # Upload to Supabase Storage
            file_name = f"{uuid.uuid4()}_{image.filename}"
            supabase.storage.from_("hazard-photos").upload(
                file_name,
                file_bytes,
                {"content-type": image.content_type}
            )

            # Get public URL
            photo_url = supabase.storage.from_("hazard-photos").get_public_url(file_name)

        except UnidentifiedImageError:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid image."
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing image: {str(e)}"
            )

    # Save hazard to database
    try:
        hazard_data = {
            "type": type,
            "description": description,
            "latitude": latitude,
            "longitude": longitude,
            "reported_by": reported_by,
            "photo_url": photo_url,
            "confirmed_count": 0
        }
        response = supabase.table("hazards").insert(hazard_data).execute()
        return {
            "status": "success",
            "message": "Hazard reported successfully!",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Confirm a hazard (community verification)
@app.post("/hazards/{hazard_id}/confirm")
def confirm_hazard(hazard_id: str):
    """Increment the confirmed count for a hazard."""
    try:
        # Get current count
        response = supabase.table("hazards").select("confirmed_count").eq("id", hazard_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Hazard not found")

        current_count = response.data[0]["confirmed_count"]

        # Increment by 1
        supabase.table("hazards").update(
            {"confirmed_count": current_count + 1}
        ).eq("id", hazard_id).execute()

        return {
            "status": "success",
            "message": "Hazard confirmed!",
            "confirmed_count": current_count + 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. Get safety score for an area
@app.get("/safety-score")
def get_safety_score(latitude: float, longitude: float, radius: float = 0.01):
    """
    Calculate safety score for a given location.
    Radius is in degrees (~1km = 0.01 degrees)
    """
    try:
        # Fetch hazards near this location from Supabase
        response = supabase.table("hazards").select("*").execute()
        all_hazards = response.data

        # Filter hazards within radius
        nearby_hazards = []
        for hazard in all_hazards:
            lat_diff = abs(hazard["latitude"] - latitude)
            lon_diff = abs(hazard["longitude"] - longitude)
            if lat_diff <= radius and lon_diff <= radius:
                nearby_hazards.append(hazard)

        # Calculate score
        score = calculate_street_safety_score(nearby_hazards)
        label = get_safety_label(score)

        return {
            "status": "success",
            "latitude": latitude,
            "longitude": longitude,
            "nearby_hazards_count": len(nearby_hazards),
            "safety_score": score,
            "safety_label": label
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Safe Route Comparison
@app.get("/safe-route")
def get_safe_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
):
    """
    Compare normal route vs safe route.
    Returns hazard count and distance for both.
    """
    try:
        # Fetch all hazards from Supabase
        response = supabase.table("hazards").select("*").execute()
        all_hazards = response.data or []

        # Calculate straight line distance (normal route)
        normal_distance = haversine_distance(
            start_lat, start_lon,
            end_lat, end_lon
        )

        # Get hazards along normal route
        hazards_on_normal_route = get_hazards_along_route(
            start_lat, start_lon,
            end_lat, end_lon,
            all_hazards,
            proximity_km=0.1
        )

        normal_route_safety = calculate_route_safety(hazards_on_normal_route)

        # Safe route adds 20% distance but avoids high penalty hazards
        safe_distance = round(normal_distance * 1.2, 2)

        # Filter out high penalty hazards for safe route
        safe_hazards = [
            h for h in hazards_on_normal_route
            if h.get("type") not in ["manhole", "flooding", "unsafe_area"]
        ]

        safe_route_safety = calculate_route_safety(safe_hazards)

        return {
            "status": "success",
            "normal_route": {
                "distance_km": round(normal_distance, 2),
                "hazard_count": normal_route_safety["hazard_count"],
                "penalty_score": normal_route_safety["penalty_score"]
            },
            "safe_route": {
                "distance_km": safe_distance,
                "hazard_count": safe_route_safety["hazard_count"],
                "penalty_score": safe_route_safety["penalty_score"]
            },
            "recommendation": "safe_route" if normal_route_safety["hazard_count"] > 0 else "normal_route"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))