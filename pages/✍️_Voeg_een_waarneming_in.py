import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd
from streamlit_gsheets import GSheetsConnection

import geopandas as gpd
import datetime
from datetime import datetime, timedelta, date

from credentials import *




# ---LAYOUT---
st.set_page_config(
    page_title="Ratten Terschelling - Input App",
    initial_sidebar_state="collapsed",
    page_icon="🐀",
    layout="wide",
    
)

st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)



reduce_header_height_style = """
<style>
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 1rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)

from functions import *

# --- APP ---  
# try:        
st.logo(IMAGE_2,  link="https://www.elskenecologie.nl/#:~:text=Elsken%20Ecologie%20is%20het%20onafhankelijke%20ecologisch%20advies-%20en", icon_image=IMAGE_2)

waarnemer = st.session_state.login['name']


conn = st.connection("gsheets", type=GSheetsConnection)
df_old = conn.read(ttl=0,worksheet="ratten-terschelling")

    
output_map = map()
output_map
try:
    if len(output_map["features"]) != 0:
        input_data(output_map,df_old)
except:
    st.stop()
    
# except:
#     st.switch_page("🗺️_Home.py")
