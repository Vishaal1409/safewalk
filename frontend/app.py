import streamlit as st
import folium
from folium.plugins import LocateControl, MarkerCluster
from folium.utilities import JsCode
from streamlit_folium import st_folium
import requests
import json
import html

# ── Config ──────────────────────────────────────────────────────────────────
API_BASE = "http://localhost:8000"
CHENNAI_CENTER = [13.0827, 80.2707]

HAZARD_CONFIG = {
    "manhole": {"icon": "circle-exclamation", "color": "red", "label": "Open Manhole"},
    "flooding": {"icon": "water", "color": "blue", "label": "Flooding"},
    "no_light": {"icon": "lightbulb", "color": "darkpurple", "label": "No Streetlight"},
    "broken_footpath": {"icon": "road", "color": "orange", "label": "Broken Footpath"},
    "unsafe_area": {"icon": "triangle-exclamation", "color": "darkred", "label": "Unsafe Area"},
    "no_wheelchair_access": {"icon": "wheelchair-move", "color": "gray", "label": "No Wheelchair Access"},
    "other": {"icon": "circle-info", "color": "gray", "label": "Other"},
    "POTHOLE": {"icon": "circle-exclamation", "color": "orange", "label": "Pothole"},
    "FLOODING": {"icon": "water", "color": "blue", "label": "Flooding (Caps)"},
}

st.set_page_config(
    page_title="SafeWalk — Navigate Safely",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styling ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-primary: #0b0e14;
        --bg-card: #131720;
        --bg-input: #1a1f2e;
        --border: #232a3b;
        --text-primary: #e8ecf4;
        --text-muted: #6b7a99;
        --accent-amber: #f0a500;
        --accent-red: #e63946;
        --accent-green: #2ec4b6;
        --accent-blue: #4895ef;
    }

    .stApp {
        background: var(--bg-primary);
        font-family: 'Barlow', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--bg-card) !important;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Barlow', sans-serif !important;
    }

    /* Hide default header */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    [data-testid="stDecoration"] { display: none; }

    .block-container {
        padding: 1rem 1.5rem !important;
        max-width: 100% !important;
    }

    /* Title bar */
    .safewalk-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 0.8rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid var(--border);
    }
    .safewalk-logo {
        font-family: 'Barlow', sans-serif;
        font-weight: 800;
        font-size: 1.7rem;
        color: var(--accent-amber);
        letter-spacing: -0.5px;
    }
    .safewalk-logo span {
        color: var(--text-primary);
        font-weight: 500;
    }
    .safewalk-tagline {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-muted);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Safety score cards */
    .score-strip {
        display: flex;
        gap: 10px;
        margin-bottom: 0.8rem;
    }
    .score-card {
        flex: 1;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
    }
    .score-card .label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
    }
    .score-card .value {
        font-family: 'Barlow', sans-serif;
        font-weight: 700;
        font-size: 1.35rem;
    }
    .value-green { color: var(--accent-green); }
    .value-amber { color: var(--accent-amber); }
    .value-red { color: var(--accent-red); }
    .value-blue { color: var(--accent-blue); }

    /* Sidebar form styling */
    .sidebar-title {
        font-family: 'Barlow', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        color: var(--accent-amber);
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
    }
    .sidebar-section {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 1.2rem;
        margin-bottom: 0.4rem;
    }

    /* Legend */
    .legend-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        margin-top: 0.5rem;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 10px;
        background: var(--bg-input);
        border-radius: 6px;
        font-size: 0.78rem;
        color: var(--text-primary);
        font-family: 'Barlow', sans-serif;
    }
    .legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    /* Map container */
    iframe {
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
    }

    /* Streamlit widget overrides */
    .stSelectbox label, .stTextArea label, .stNumberInput label,
    .stFileUploader label, .stTextInput label {
        font-family: 'Barlow', sans-serif !important;
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        font-size: 0.85rem !important;
    }

    .stButton > button {
        font-family: 'Barlow', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        border-radius: 8px !important;
    }

    div[data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── API helpers ─────────────────────────────────────────────────────────────
def fetch_hazards():
    """Fetch all hazards from the backend."""
    try:
        resp = requests.get(f"{API_BASE}/hazards", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", data.get("hazards", []))
    except Exception:
        return []


def report_hazard(hazard_type, description, lat, lon, reported_by, image_file=None):
    """Submit a new hazard report."""
    form_data = {
        "type": hazard_type,
        "description": description,
        "latitude": str(lat),
        "longitude": str(lon),
        "reported_by": reported_by,
    }
    files = {}
    if image_file is not None:
        files["image"] = (image_file.name, image_file.getvalue(), image_file.type)

    try:
        resp = requests.post(
            f"{API_BASE}/hazards", data=form_data, files=files or None, timeout=10
        )
        resp.raise_for_status()
        return True, resp.json().get("message", "Hazard reported!")
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to backend. Is the server running?"
    except Exception as e:
        return False, f"Error: {e}"


def confirm_hazard(hazard_id):
    """Confirm a hazard (community verification)."""
    try:
        resp = requests.post(f"{API_BASE}/hazards/{hazard_id}/confirm", timeout=5)
        resp.raise_for_status()
        return True, resp.json()
    except Exception as e:
        return False, str(e)


def fetch_safety_score(lat, lon, radius=0.01):
    """Get safety score for a location."""
    try:
        resp = requests.get(
            f"{API_BASE}/safety-score",
            params={"latitude": lat, "longitude": lon, "radius": radius},
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


# ── Header ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="safewalk-header">
        <div>
            <div class="safewalk-logo">Safe<span>Walk</span></div>
            <div class="safewalk-tagline">navigate safely · chennai</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Fetch data ──────────────────────────────────────────────────────────────
hazards = fetch_hazards()
safety = fetch_safety_score(CHENNAI_CENTER[0], CHENNAI_CENTER[1])

# ── Score strip ─────────────────────────────────────────────────────────────
score_val = safety["safety_score"] if safety else "—"
score_label = safety["safety_label"] if safety else "Offline"
hazard_count = len(hazards)
confirmed = sum(1 for h in hazards if h.get("confirmed_count", 0) > 0)

if isinstance(score_val, (int, float)):
    if score_val >= 80:
        score_class = "value-green"
    elif score_val >= 60:
        score_class = "value-amber"
    else:
        score_class = "value-red"
else:
    score_class = "value-amber"

st.markdown(
    f"""
    <div class="score-strip">
        <div class="score-card">
            <div class="label">Safety Score</div>
            <div class="value {score_class}">{score_val}</div>
        </div>
        <div class="score-card">
            <div class="label">Status</div>
            <div class="value value-amber" style="font-size:0.95rem;">{score_label}</div>
        </div>
        <div class="score-card">
            <div class="label">Hazards</div>
            <div class="value value-red">{hazard_count}</div>
        </div>
        <div class="score-card">
            <div class="label">Confirmed</div>
            <div class="value value-blue">{confirmed}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Build Folium Map ────────────────────────────────────────────────────────
m = folium.Map(
    location=CHENNAI_CENTER,
    zoom_start=12,
    tiles="CartoDB dark_matter",
    control_scale=True,
)
LocateControl(auto_start=False, strings={"title": "Find me"}).add_to(m)

# Add marker cluster with 500m fixed radius
cluster_radius_js = JsCode("""
function(zoom) {
    var lat = 13.0827;
    var metersPerPixel = 156543.03392 * Math.cos(lat * Math.PI / 180) / Math.pow(2, zoom);
    return 500 / metersPerPixel;
}
""")
marker_cluster = MarkerCluster(options={"maxClusterRadius": cluster_radius_js}).add_to(m)

# Add hazard markers
for h in hazards:
    lat = h.get("latitude")
    lon = h.get("longitude")
    if lat is None or lon is None:
        continue

    h_type = h.get("type", "unknown")
    cfg = HAZARD_CONFIG.get(h_type, {"icon": "circle-info", "color": "gray", "label": h_type})
    conf_count = h.get("confirmed_count", 0)
    
    # Escape description to prevent HTML injection clipping popups
    safe_desc = html.escape(h.get('description', 'No description'))
    safe_reporter = html.escape(h.get('reported_by', 'anonymous'))

    photo_html = ""
    if h.get("photo_url"):
        photo_html = f'<img src="{h["photo_url"]}" style="width:100%;max-height:120px;object-fit:cover;border-radius:6px;margin-top:8px;">'

    popup_html = f"""
    <div style="font-family:Barlow,sans-serif;min-width:200px;max-width:260px;">
        <div style="font-weight:700;font-size:14px;color:#1a1a2e;margin-bottom:4px;">
            {cfg['label']}
        </div>
        <div style="font-size:12px;color:#444;margin-bottom:6px;">
            {safe_desc}
        </div>
        <div style="font-size:11px;color:#888;margin-bottom:4px;">
            Reported by <b>{safe_reporter}</b>
        </div>
        <div style="display:flex;gap:12px;font-size:11px;color:#666;">
            <span>✅ {conf_count} confirmed</span>
            <span>📍 {lat:.4f}, {lon:.4f}</span>
        </div>
        {photo_html}
    </div>
    """

    folium.Marker(
    location=[lat, lon],
    popup=folium.Popup(popup_html, max_width=280),
    tooltip=cfg["label"],
    icon=folium.Icon(color=cfg["color"])
).add_to(marker_cluster)

# Render map
map_data = st_folium(m, height=560, use_container_width=True, returned_objects=["last_clicked"])

# Store clicked location
if map_data and map_data.get("last_clicked"):
    st.session_state["clicked_lat"] = map_data["last_clicked"]["lat"]
    st.session_state["clicked_lng"] = map_data["last_clicked"]["lng"]

# ── Legend ──────────────────────────────────────────────────────────────────
COLOR_MAP = {
    "red": "#e63946",
    "blue": "#4895ef",
    "darkpurple": "#7b2d8e",
    "orange": "#f0a500",
    "darkred": "#9b1d20",
    "gray": "#6b7a99",
}

legend_items = "".join(
    f'<div class="legend-item"><div class="legend-dot" style="background:{COLOR_MAP.get(c["color"], "#888")};"></div>{c["label"]}</div>'
    for c in HAZARD_CONFIG.values()
)
st.markdown(
    f'<div class="legend-grid">{legend_items}</div>',
    unsafe_allow_html=True,
)

# ── Sidebar: Report + Confirm ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">Report a Hazard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-section">Click the map to set location</div>',
        unsafe_allow_html=True,
    )

    clicked_lat = st.session_state.get("clicked_lat", None)
    clicked_lng = st.session_state.get("clicked_lng", None)

    if clicked_lat and clicked_lng:
        st.success(f"📍 {clicked_lat:.5f}, {clicked_lng:.5f}")
    else:
        st.info("Click on the map to pick a location")

    with st.form("report_form", clear_on_submit=True):
        hazard_type = st.selectbox(
            "Hazard Type",
            options=list(HAZARD_CONFIG.keys()),
            format_func=lambda x: HAZARD_CONFIG[x]["label"],
        )
        description = st.text_area("Description", placeholder="Describe the hazard...", max_chars=500)
        reported_by = "Shruthika"
        image = st.file_uploader("Photo (optional)", type=["jpg", "jpeg", "png"])

        col1, col2 = st.columns([1, 1])
        with col1:
            lat_input = st.number_input(
                "Latitude",
                value=clicked_lat if clicked_lat else CHENNAI_CENTER[0],
                format="%.6f",
                step=0.0001,
            )
        with col2:
            lng_input = st.number_input(
                "Longitude",
                value=clicked_lng if clicked_lng else CHENNAI_CENTER[1],
                format="%.6f",
                step=0.0001,
            )

        submitted = st.form_submit_button("🛡️ Submit Report", use_container_width=True, type="primary")

        if submitted:
            if not description.strip():
                st.error("Please add a description.")
            elif not reported_by.strip():
                st.error("Please enter your name.")
            else:
                success, msg = report_hazard(
                    hazard_type, description.strip(), lat_input, lng_input,
                    reported_by.strip(), image
                )
                if success:
                    st.success(msg)
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(msg)

    # ── Confirm existing hazards ────────────────────────────────────────────
    st.markdown('<div class="sidebar-title" style="margin-top:1.5rem;">Confirm Hazards</div>', unsafe_allow_html=True)

    if hazards:
        for h in hazards[:10]:
            h_type = h.get("type", "unknown")
            cfg = HAZARD_CONFIG.get(h_type, {"label": h_type})
            desc_short = (h.get("description", "")[:50] + "...") if len(h.get("description", "")) > 50 else h.get("description", "")
            conf = h.get("confirmed_count", 0)

            with st.container():
                st.markdown(
                    f"**{cfg['label']}** — {desc_short}  \n"
                    f"`✅ {conf} confirmations`"
                )
                if st.button(f"Confirm ✅", key=f"confirm_{h['id']}"):
                    ok, result = confirm_hazard(h["id"])
                    if ok:
                        st.success(f"Confirmed! Count: {result.get('confirmed_count', conf + 1)}")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(result)
                st.divider()
    else:
        st.caption("No hazards reported yet. Be the first!")

    # ── Safety score lookup ─────────────────────────────────────────────────
    st.markdown('<div class="sidebar-title" style="margin-top:1.5rem;">Safety Score Lookup</div>', unsafe_allow_html=True)

    with st.form("score_form"):
        score_lat = st.number_input("Latitude", value=CHENNAI_CENTER[0], format="%.6f", key="score_lat")
        score_lon = st.number_input("Longitude", value=CHENNAI_CENTER[1], format="%.6f", key="score_lon")
        score_radius = st.slider("Radius (km)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)

        if st.form_submit_button("Check Safety", use_container_width=True):
            result = fetch_safety_score(score_lat, score_lon, radius=score_radius / 100)
            if result:
                st.metric("Safety Score", f"{result['safety_score']}/100")
                st.info(result["safety_label"])
                st.caption(f"Nearby hazards: {result['nearby_hazards_count']}")
            else:
                st.error("Could not fetch safety score. Is the backend running?")
