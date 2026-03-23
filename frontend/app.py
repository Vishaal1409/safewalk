import streamlit as st
import folium
from folium.plugins import LocateControl, MarkerCluster
from streamlit_folium import st_folium
import requests
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
}

st.set_page_config(
    page_title="SafeWalk — Navigate Safely",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styling — Ishitha's Pink Theme ──────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-primary: #FCE7F3;
        --bg-card: #ffffff;
        --bg-input: #fdf2f8;
        --border: #f9a8d4;
        --text-primary: #334155;
        --text-muted: #64748B;
        --accent-pink: #DB2777;
        --accent-dark-pink: #9D174D;
        --accent-red: #DC2626;
        --accent-orange: #D97706;
        --accent-green: #16A34A;
        --accent-blue: #3B82F6;
    }

    .stApp {
        background: var(--bg-primary);
        font-family: 'Poppins', sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #9D174D !important;
        border-right: 2px solid #DB2777;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Poppins', sans-serif !important;
        color: #ffffff !important;
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
        padding: 1rem 1.2rem;
        background: #9D174D;
        border-radius: 12px;
        border-bottom: 2px solid #DB2777;
    }
    .safewalk-logo {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 1.9rem;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .safewalk-logo span {
        color: #fbcfe8;
        font-weight: 500;
    }
    .safewalk-tagline {
        font-family: 'Poppins', sans-serif;
        font-size: 0.75rem;
        color: #fbcfe8;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 2px;
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
        border-radius: 10px;
        padding: 12px 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(219,39,119,0.08);
    }
    .score-card .label {
        font-family: 'Poppins', sans-serif;
        font-size: 0.65rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
    }
    .score-card .value {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.35rem;
    }
    .value-green { color: var(--accent-green); }
    .value-pink { color: var(--accent-pink); }
    .value-red { color: var(--accent-red); }
    .value-blue { color: var(--accent-blue); }

    /* Sidebar form styling */
    .sidebar-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: #ffffff;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #DB2777;
    }
    .sidebar-section {
        font-family: 'Poppins', sans-serif;
        font-size: 0.72rem;
        color: #fbcfe8;
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
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 8px;
        font-size: 0.78rem;
        color: var(--text-primary);
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 1px 4px rgba(219,39,119,0.06);
    }
    .legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    /* Map container */
    iframe {
        border-radius: 12px !important;
        border: 2px solid var(--border) !important;
    }

    /* Streamlit widget overrides */
    .stSelectbox label, .stTextArea label, .stNumberInput label,
    .stFileUploader label, .stTextInput label {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        color: #ffffff !important;
        font-size: 0.85rem !important;
    }

    .stButton > button {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        border-radius: 8px !important;
        background-color: #DB2777 !important;
        color: white !important;
        border: none !important;
    }

    .stButton > button:hover {
        background-color: #9D174D !important;
    }

    div[data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 12px;
        box-shadow: 0 2px 8px rgba(219,39,119,0.08);
    }

    /* Success/Error/Info messages */
    .stSuccess {
        background: #dcfce7 !important;
        border: 1px solid #16A34A !important;
        border-radius: 8px !important;
    }
    .stError {
        background: #fee2e2 !important;
        border: 1px solid #DC2626 !important;
        border-radius: 8px !important;
    }
    .stInfo {
        background: #fdf2f8 !important;
        border: 1px solid #DB2777 !important;
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── API helpers ─────────────────────────────────────────────────────────────
def fetch_hazards(filter_type=None, min_confirmed=None):
    """Fetch hazards from the backend with optional filters."""
    try:
        params = {}
        if filter_type and filter_type != "All":
            params["type"] = filter_type.lower()
        if min_confirmed:
            params["min_confirmed"] = min_confirmed

        resp = requests.get(f"{API_BASE}/hazards", params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", data.get("hazards", []))
    except requests.exceptions.ConnectionError:
        return None
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

# ── Filters ─────────────────────────────────────────────────────────────────
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    filter_type = st.selectbox(
        "🔍 Filter by Hazard Type",
        options=["All", "manhole", "flooding", "no_light", "broken_footpath", "unsafe_area", "no_wheelchair_access"],
        format_func=lambda x: "All Hazards" if x == "All" else HAZARD_CONFIG.get(x, {}).get("label", x)
    )
with col_f2:
    show_confirmed_only = st.checkbox("✅ Confirmed Only")

# Fetch with filters
hazards_raw = fetch_hazards(
    filter_type=filter_type,
    min_confirmed=1 if show_confirmed_only else None
)

# Handle backend offline
if hazards_raw is None:
    st.error("⚠️ Backend is not running. Please start the FastAPI server first.")
    st.stop()

hazards = hazards_raw if hazards_raw else []

if len(hazards) == 0:
    st.warning("No hazards found in this area yet. Be the first to report one!")

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
        score_class = "value-pink"
    else:
        score_class = "value-red"
else:
    score_class = "value-pink"

st.markdown(
    f"""
    <div class="score-strip">
        <div class="score-card">
            <div class="label">Safety Score</div>
            <div class="value {score_class}">{score_val}</div>
        </div>
        <div class="score-card">
            <div class="label">Status</div>
            <div class="value value-pink" style="font-size:0.95rem;">{score_label}</div>
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
    tiles="CartoDB positron",
    control_scale=True,
)
LocateControl(auto_start=False, strings={"title": "Find me"}).add_to(m)

marker_cluster = MarkerCluster().add_to(m)

# Add hazard markers
for h in hazards:
    lat = h.get("latitude")
    lon = h.get("longitude")
    if lat is None or lon is None:
        continue

    h_type = h.get("type", "unknown")
    cfg = HAZARD_CONFIG.get(h_type, {"icon": "circle-info", "color": "gray", "label": h_type})
    conf_count = h.get("confirmed_count", 0)

    safe_desc = html.escape(h.get('description', 'No description'))
    safe_reporter = html.escape(h.get('reported_by', 'anonymous'))

    photo_html = ""
    if h.get("photo_url"):
        photo_html = f'<img src="{h["photo_url"]}" style="width:100%;max-height:120px;object-fit:cover;border-radius:6px;margin-top:8px;">'

    popup_html = f"""
    <div style="font-family:Poppins,sans-serif;min-width:200px;max-width:260px;padding:4px;">
        <div style="font-weight:700;font-size:13px;color:#9D174D;margin-bottom:4px;">
            {cfg['label']}
        </div>
        <div style="font-size:12px;color:#334155;margin-bottom:6px;">
            {safe_desc}
        </div>
        <div style="font-size:11px;color:#64748B;margin-bottom:4px;">
            Reported by <b style="color:#DB2777;">{safe_reporter}</b>
        </div>
        <div style="display:flex;gap:12px;font-size:11px;color:#64748B;">
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

if map_data and map_data.get("last_clicked"):
    st.session_state["clicked_lat"] = map_data["last_clicked"]["lat"]
    st.session_state["clicked_lng"] = map_data["last_clicked"]["lng"]

# ── Legend ──────────────────────────────────────────────────────────────────
COLOR_MAP = {
    "red": "#DC2626",
    "blue": "#3B82F6",
    "darkpurple": "#7b2d8e",
    "orange": "#D97706",
    "darkred": "#9D174D",
    "gray": "#64748B",
}

legend_items = "".join(
    f'<div class="legend-item"><div class="legend-dot" style="background:{COLOR_MAP.get(c["color"], "#888")};"></div>{c["label"]}</div>'
    for c in HAZARD_CONFIG.values()
)
st.markdown(
    f'<div class="legend-grid">{legend_items}</div>',
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🛡️ Report a Hazard</div>', unsafe_allow_html=True)
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
        reported_by = st.text_input("Your Name", placeholder="Enter your name")
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
                    st.rerun()
                else:
                    st.error(msg)

    # ── Confirm hazards ──────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-title" style="margin-top:1.5rem;">✅ Confirm Hazards</div>', unsafe_allow_html=True)

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
                        st.rerun()
                    else:
                        st.error(result)
                st.divider()
    else:
        st.caption("No hazards reported yet. Be the first!")

    # ── Safety score lookup ──────────────────────────────────────────────────
    st.markdown('<div class="sidebar-title" style="margin-top:1.5rem;">🌟 Safety Score Lookup</div>', unsafe_allow_html=True)

    with st.form("score_form"):
        score_lat = st.number_input("Latitude", value=CHENNAI_CENTER[0], format="%.6f", key="score_lat")
        score_lon = st.number_input("Longitude", value=CHENNAI_CENTER[1], format="%.6f", key="score_lon")
        score_radius = st.slider("Radius (km)", min_value=0.5, max_value=5.0, value=1.0, step=0.5)

        if st.form_submit_button("Check Safety", use_container_width=True):
            result = fetch_safety_score(score_lat, score_lon, radius=score_radius / 100)
            if result:
                score = result['safety_score']
                if score >= 80:
                    st.success(f"🟢 Safety Score: {score}/100 — Safe")
                elif score >= 60:
                    st.warning(f"🟡 Safety Score: {score}/100 — Use Caution")
                else:
                    st.error(f"🔴 Safety Score: {score}/100 — High Risk")
                st.caption(f"Nearby hazards: {result['nearby_hazards_count']}")
            else:
                st.error("Could not fetch safety score. Is the backend running?")