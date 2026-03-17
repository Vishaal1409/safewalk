from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates in kilometers.
    Uses Haversine formula.
    """
    R = 6371  # Earth radius in km

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


def get_hazards_along_route(
    start_lat: float, start_lon: float,
    end_lat: float, end_lon: float,
    hazards: list,
    proximity_km: float = 0.1
) -> list:
    """
    Find hazards that are close to the straight line route.
    proximity_km = how close a hazard needs to be to count (default 100m)
    """
    hazards_on_route = []

    for hazard in hazards:
        hazard_lat = hazard.get("latitude")
        hazard_lon = hazard.get("longitude")

        if hazard_lat is None or hazard_lon is None:
            continue

        # Check distance from start
        dist_from_start = haversine_distance(
            start_lat, start_lon,
            hazard_lat, hazard_lon
        )

        # Check distance from end
        dist_from_end = haversine_distance(
            end_lat, end_lon,
            hazard_lat, hazard_lon
        )

        # Total route distance
        route_distance = haversine_distance(
            start_lat, start_lon,
            end_lat, end_lon
        )

        # If hazard is within proximity of the route path
        if dist_from_start + dist_from_end <= route_distance + proximity_km:
            hazards_on_route.append(hazard)

    return hazards_on_route


def calculate_route_safety(hazards_on_route: list) -> dict:
    """
    Calculate penalty score based on hazards along route.
    Higher penalty = more dangerous route.
    """
    HAZARD_WEIGHTS = {
        "manhole": 10,
        "flooding": 9,
        "unsafe_area": 8,
        "no_light": 7,
        "no_wheelchair_access": 6,
        "broken_footpath": 5,
    }

    total_penalty = 0
    for hazard in hazards_on_route:
        hazard_type = hazard.get("type", "broken_footpath")
        weight = HAZARD_WEIGHTS.get(hazard_type, 5)
        confirmations = hazard.get("confirmed_count", 0)
        confirmation_boost = 1 + (confirmations * 0.1)
        total_penalty += weight * confirmation_boost

    return {
        "hazard_count": len(hazards_on_route),
        "penalty_score": round(total_penalty, 2)
    }