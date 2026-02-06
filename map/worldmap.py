import streamlit as st
import folium
from streamlit_folium import st_folium

# Remove padding and sidebar
st.set_page_config(layout="wide")

st.markdown(""" <style> header[data-testid="stHeader"] { display: none; } </style> """, unsafe_allow_html=True)

# Inject CSS to remove all margins
st.markdown("""
    <style>
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }
        .stApp {
            margin: 0;
            padding: 0;
        }
    </style>
""", unsafe_allow_html=True)



# Create full-screen map
m = folium.Map(location=[39.5, -98.35], zoom_start=4)

# Render map at full width & height
st_folium(m, width="100%", height=800)
