from datetime import datetime, timezone

# Hazard severity weights (higher = more dangerous)
HAZARD_WEIGHTS = {
    "manhole": 10,
    "flooding": 9,
    "no_light": 7,
    "broken_footpath": 5,
    "unsafe_area": 8,
    "no_wheelchair_access": 6,
}

def get_hazard_weight(hazard_type: str) -> int:
    """Returns severity weight for a hazard type."""
    return HAZARD_WEIGHTS.get(hazard_type.lower(), 5)

def get_recency_factor(created_at: str) -> float:
    """
    Returns a recency factor between 0.1 and 1.0.
    Newer reports have higher weight.
    Reports older than 7 days get very low weight.
    """
    try:
        report_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        hours_old = (now - report_time).total_seconds() / 3600

        if hours_old < 24:
            return 1.0       # Less than 1 day old — full weight
        elif hours_old < 72:
            return 0.7       # 1-3 days old
        elif hours_old < 168:
            return 0.4       # 3-7 days old
        else:
            return 0.1       # Older than 7 days — very low weight
    except:
        return 0.5

def get_time_of_day_factor(hazard_type: str) -> float:
    """
    Lighting hazards are more dangerous at night.
    Returns extra weight multiplier based on current time.
    """
    current_hour = datetime.now().hour
    is_night = current_hour >= 20 or current_hour <= 6

    if hazard_type.lower() == "no_light" and is_night:
        return 1.5   # 50% more dangerous at night
    return 1.0

def calculate_street_safety_score(hazards: list) -> float:
    """
    Calculate a safety score for a street/area based on nearby hazards.
    
    Score is 0-100 where:
    - 100 = perfectly safe (no hazards)
    - 0 = extremely dangerous
    
    Args:
        hazards: list of hazard dicts from Supabase
    
    Returns:
        float: safety score between 0 and 100
    """
    if not hazards:
        return 100.0  # No hazards = perfectly safe

    total_danger = 0

    for hazard in hazards:
        # Base severity
        weight = get_hazard_weight(hazard.get("type", "unknown"))

        # Recency factor
        recency = get_recency_factor(hazard.get("created_at", ""))

        # Time of day factor
        time_factor = get_time_of_day_factor(hazard.get("type", ""))

        # Community confirmations boost the score
        confirmations = hazard.get("confirmed_count", 0)
        confirmation_boost = 1 + (confirmations * 0.1)  # Each confirmation adds 10%

        # Calculate danger score for this hazard
        danger = weight * recency * time_factor * confirmation_boost
        total_danger += danger

    # Convert danger to safety score (inverse relationship)
    # Cap danger at 100 to keep score between 0-100
    safety_score = max(0, 100 - total_danger)

    return round(safety_score, 2)


def get_safety_label(score: float) -> str:
    """Returns a human readable label for the safety score."""
    if score >= 80:
        return "✅ Safe"
    elif score >= 60:
        return "⚠️ Use Caution"
    elif score >= 40:
        return "🟠 Moderate Risk"
    else:
        return "🔴 High Risk"