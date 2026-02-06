import time
import streamlit as st
import requests
import pydeck as pdk

# Remove padding and sidebar
st.set_page_config(layout="wide")

BACKEND_URL = "http://127.0.0.1:5000/api/fires"

# Hide Streamlit header + padding
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none; }
        .block-container { padding: 0 !important; margin: 0 !important; }
        .stApp { margin: 0; padding: 0; }
    </style>
""", unsafe_allow_html=True)



@st.cache_data(ttl=600)
def get_fires():
    try:
        response = requests.get(BACKEND_URL, timeout=5)
        response.raise_for_status()
        fires = response.json()
        print(f"Fetched {len(fires)} fire records at {time.ctime()}")
        return fires
    except Exception as e:
        print("Error fetching fires:", e)
        return []

fires = get_fires()

if not fires:
    st.warning("No fire data available (backend unreachable or returned empty).")
    st.stop()

# Convert to PyDeck-friendly format
# PyDeck expects a list of dicts with lon/lat keys
for f in fires:
    f["lon"] = f["longitude"]
    f["lat"] = f["latitude"]

# PyDeck scatterplot layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=fires,
    get_position='[lon, lat]',
    get_color='[255, 0, 0]',
    get_radius=6,
    radius_units="pixels",
    pickable=True,
)

tooltip = {
    "html": "<b>FRP:</b> {frp}<br/><b>Confidence:</b> {confidence}<br/><b>Date:</b> {acq_date}",
    "style": {"backgroundColor": "black", "color": "white"}
}

view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=2,
    pitch=0,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_provider="carto",     # <-- REQUIRED
    map_style="dark",         # <-- Works without API key
)


st.pydeck_chart(deck)
