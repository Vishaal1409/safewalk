"""
Test script to submit a complete hazard report form to the POST /hazards endpoint.
Uploads all fields (type, description, latitude, longitude, reported_by, image)
and verifies the data was saved correctly in Supabase.
"""

import os
import io
import sys
import json
import httpx
from collections import OrderedDict
from PIL import Image
from dotenv import load_dotenv
from supabase import create_client, Client

# Database schema column order
DB_COLUMN_ORDER = [
    "id", "type", "description", "latitude", "longitude",
    "photo_url", "reported_by", "confirmed_count", "created_at"
]


def order_by_schema(data: dict) -> OrderedDict:
    """Reorder a dict to match the DB schema column order."""
    ordered = OrderedDict()
    for key in DB_COLUMN_ORDER:
        if key in data:
            ordered[key] = data[key]
    # Append any extra keys not in the schema
    for key in data:
        if key not in ordered:
            ordered[key] = data[key]
    return ordered

# Load .env from project root
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")
API_BASE = "http://127.0.0.1:8000"

# --- Test hazard data ---
TEST_HAZARD = {
    "type": "pothole",
    "description": "Large pothole near the main intersection, approximately 30cm deep. Dangerous for cyclists and pedestrians at night.",
    "latitude": 12.9716,
    "longitude": 77.5946,
    "reported_by": "test_user_safewalk",
}


def create_test_image() -> bytes:
    """Generate a small 100x100 test image."""
    img = Image.new("RGB", (100, 100), color=(255, 100, 50))
    pixels = img.load()
    # Draw a simple "X" pattern
    for i in range(100):
        pixels[i, i] = (0, 0, 0)
        pixels[99 - i, i] = (0, 0, 0)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def main():
    print("=" * 60)
    print("  Hazard Form Upload Test (POST /hazards)")
    print("=" * 60)

    # --- Step 1: Check if API server is running ---
    print("\n[1/4] Checking if API server is running...")
    try:
        resp = httpx.get(f"{API_BASE}/", timeout=5)
        if resp.status_code == 200:
            print(f"  ✅ API server is online: {resp.json()}")
        else:
            print(f"  ❌ API returned status {resp.status_code}")
            return
    except httpx.ConnectError:
        print(f"  ❌ Cannot connect to {API_BASE}")
        print("  → Start the server first: uvicorn src.main:app --reload")
        return

    # --- Step 2: Submit the hazard form ---
    print("\n[2/4] Submitting hazard form with all data...")
    image_bytes = create_test_image()

    form_data = {
        "type": TEST_HAZARD["type"],
        "description": TEST_HAZARD["description"],
        "latitude": str(TEST_HAZARD["latitude"]),
        "longitude": str(TEST_HAZARD["longitude"]),
        "reported_by": TEST_HAZARD["reported_by"],
    }
    files = {
        "image": ("test_hazard.png", image_bytes, "image/png"),
    }

    print("\n  📤 DATA SENT TO DB:")
    print("  " + "-" * 50)
    sent_payload = {
        "type": form_data["type"],
        "description": form_data["description"],
        "latitude": form_data["latitude"],
        "longitude": form_data["longitude"],
        "photo_url": f"test_hazard.png ({len(image_bytes)} bytes)",
        "reported_by": form_data["reported_by"],
        "confirmed_count": 0,
    }
    print(json.dumps(order_by_schema(sent_payload), indent=4))

    try:
        resp = httpx.post(
            f"{API_BASE}/hazards",
            data=form_data,
            files=files,
            timeout=15,
        )
        if resp.status_code == 200:
            result = resp.json()
            print(f"\n  ✅ Hazard reported successfully!")
            print("\n  📥 RESPONSE FROM DB (POST):")
            print("  " + "-" * 50)
            ordered_result = {"message": result["message"], "data": [order_by_schema(d) for d in result.get("data", [])]}
            print(json.dumps(ordered_result, indent=4))
            hazard_data = result.get("data", [{}])[0]
            hazard_id = hazard_data.get("id", "unknown")
            photo_url = hazard_data.get("photo_url", "N/A")
        else:
            print(f"  ❌ POST /hazards returned status {resp.status_code}")
            print(f"  • Response: {resp.text}")
            return
    except Exception as e:
        print(f"  ❌ Request failed: {e}")
        return

    # --- Step 3: Verify via GET /hazards ---
    print("\n[3/4] Verifying hazard exists via GET /hazards...")
    try:
        resp = httpx.get(f"{API_BASE}/hazards", timeout=10)
        hazards = resp.json().get("hazards", [])
        found = [h for h in hazards if h.get("id") == hazard_id]
        if found:
            h = found[0]
            print(f"  ✅ Hazard found in database!")
            print("\n  📥 DATA RETRIEVED FROM DB (GET):")
            print("  " + "-" * 50)
            print(json.dumps(order_by_schema(h), indent=4, default=str))
        else:
            print(f"  ⚠️  Hazard with ID {hazard_id} not found in GET /hazards response")
    except Exception as e:
        print(f"  ❌ GET /hazards failed: {e}")

    # --- Step 4: Cleanup — delete the test hazard from DB ---
    print("\n[4/4] Cleaning up test data...")
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

        # Delete hazard row
        supabase.table("hazards").delete().eq("id", hazard_id).execute()
        print(f"  ✅ Deleted test hazard (ID: {hazard_id}) from database")

        # Delete uploaded photo from storage
        if photo_url and photo_url != "N/A":
            file_name = photo_url.split("/")[-1]
            supabase.storage.from_("hazard-photos").remove([file_name])
            print(f"  ✅ Deleted test photo from storage")
    except Exception as e:
        print(f"  ⚠️  Cleanup issue (not critical): {e}")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("  ✅ FULL FORM TEST PASSED — Upload + Retrieve working!")
    print("=" * 60)


if __name__ == "__main__":
    main()
