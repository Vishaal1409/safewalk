"""
Test the fixed route_engine: point_to_segment_distance + get_hazards_along_route.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 
    "/Users/fi-it/Documents/projects/safewalk/backend"))

from src.services.route_engine import (
    haversine_distance,
    point_to_segment_distance,
    get_hazards_along_route,
)

PASS = 0
FAIL = 0

def check(name, condition, detail=""):
    global PASS, FAIL
    status = "✅ PASS" if condition else "❌ FAIL"
    if not condition:
        FAIL += 1
    else:
        PASS += 1
    print(f"  {status}: {name}" + (f"  ({detail})" if detail else ""))

print("=" * 60)
print("TEST 1: Degenerate segment (start == end)")
print("=" * 60)
# When start == end, distance should equal haversine to that single point
d = point_to_segment_distance(13.0, 80.0, 13.0, 80.0, 13.0, 80.0)
check("Same point → 0 km", abs(d) < 0.001, f"d={d:.6f}")

d = point_to_segment_distance(13.01, 80.0, 13.0, 80.0, 13.0, 80.0)
expected = haversine_distance(13.01, 80.0, 13.0, 80.0)
check("Degenerate segment matches haversine", abs(d - expected) < 0.001,
      f"d={d:.4f}, expected={expected:.4f}")

print()
print("=" * 60)
print("TEST 2: Hazard ON the segment midpoint")
print("=" * 60)
# Route: (13.0, 80.0) → (13.0, 80.1)  (east-west)
# Hazard at midpoint: (13.0, 80.05)
d = point_to_segment_distance(13.0, 80.05, 13.0, 80.0, 13.0, 80.1)
check("Midpoint hazard → ~0 km", d < 0.01, f"d={d:.6f}")

print()
print("=" * 60)
print("TEST 3: Hazard perpendicular to segment (should be close to perp distance)")
print("=" * 60)
# Route: (13.0, 80.0) → (13.0, 80.1)  (east-west along lat 13.0)
# Hazard at (13.001, 80.05) — slightly north of midpoint
d = point_to_segment_distance(13.001, 80.05, 13.0, 80.0, 13.0, 80.1)
perp = haversine_distance(13.001, 80.05, 13.0, 80.05)
check("Perpendicular distance ≈ haversine to nearest point", 
      abs(d - perp) < 0.05, f"d={d:.4f}, perp={perp:.4f}")

print()
print("=" * 60)
print("TEST 4: Hazard FAR off to the side (OLD bug scenario)")
print("=" * 60)
# Route: (13.0, 80.0) → (13.0, 80.1)   ~11 km east-west
# Hazard: (13.05, 80.05) — ~5.5 km north of midpoint
d = point_to_segment_distance(13.05, 80.05, 13.0, 80.0, 13.0, 80.1)
check("Far-side hazard NOT in 100m corridor", d > 0.1,
      f"d={d:.2f} km (should be ~5.5 km)")

# The OLD ellipse check would have accepted this:
route_dist = haversine_distance(13.0, 80.0, 13.0, 80.1)
ds = haversine_distance(13.0, 80.0, 13.05, 80.05)
de = haversine_distance(13.0, 80.1, 13.05, 80.05)
old_would_accept = (ds + de) <= (route_dist + 0.1)
check("Old ellipse would have WRONGLY accepted this", old_would_accept,
      f"ds+de={ds+de:.2f}, route+0.1={route_dist+0.1:.2f}")

print()
print("=" * 60)
print("TEST 5: get_hazards_along_route integration")
print("=" * 60)
hazards = [
    {"id": "on_route",   "latitude": 13.0,   "longitude": 80.05, "type": "manhole"},
    {"id": "near_route",  "latitude": 13.0005,"longitude": 80.05, "type": "flooding"},
    {"id": "far_away",   "latitude": 13.05,  "longitude": 80.05, "type": "broken_footpath"},
    {"id": "no_coords",  "type": "manhole"},  # missing lat/lon
]

result = get_hazards_along_route(13.0, 80.0, 13.0, 80.1, hazards, proximity_km=0.1)
ids = [h["id"] for h in result]
check("On-route hazard included", "on_route" in ids, f"ids={ids}")
check("Near-route hazard included", "near_route" in ids, f"ids={ids}")
check("Far-away hazard excluded", "far_away" not in ids, f"ids={ids}")
check("Missing-coords hazard excluded", "no_coords" not in ids, f"ids={ids}")

print()
print("=" * 60)
print("TEST 6: Hazard beyond segment endpoint (clamping test)")
print("=" * 60)
# Route: (13.0, 80.0) → (13.0, 80.1)
# Hazard at (13.0, 80.2) — beyond the end, 0.1° east of endpoint
d = point_to_segment_distance(13.0, 80.2, 13.0, 80.0, 13.0, 80.1)
d_to_end = haversine_distance(13.0, 80.2, 13.0, 80.1)
check("Beyond-endpoint → distance equals dist to endpoint",
      abs(d - d_to_end) < 0.05, f"d={d:.2f}, to_end={d_to_end:.2f}")

print()
print("=" * 60)
print(f"RESULTS: {PASS} passed, {FAIL} failed")
print("=" * 60)

sys.exit(1 if FAIL > 0 else 0)
