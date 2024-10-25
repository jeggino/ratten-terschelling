import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium
import datetime
from datetime import datetime, timedelta, date
import random

import ast


# ---LAYOUT---
st.set_page_config(
    page_title="Ratten Terschelling - Input App",
    initial_sidebar_state="collapsed",
    page_icon="🐀",
    layout="wide",
    
)


st.markdown(
    """
    <style>
    [data-testid="collapsedControl"] svg {
        height: 0rem;
        width: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)



reduce_header_height_style = """
<style>
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 0rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)


#---DATASET---
ttl = '10m'
ttl_references = '10m'
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl,worksheet="ratten-terschelling")
df_references = conn.read(ttl=ttl_references,worksheet="df_users")

# --- APP ---
if "login" not in st.session_state:
    logIn()
    st.stop()

with st.sidebar:
    logOut()
    st.divider()

    

IMAGE = "icons/logo.png"
st.logo(IMAGE,  link="https://www.elskenecologie.nl/#:~:text=Elsken%20Ecologie%20is%20het%20onafhankelijke%20ecologisch%20advies-%20en", icon_image=None)

try:
    
    df_2 = df_point[df_point['project']=="Ratten Terschelling"]
    df_2["datum"] = pd.to_datetime(df_2["datum"]).dt.date
        
    st.sidebar.subheader("Filter op",divider=False)
    d = st.sidebar.slider("Datum", min_value=df_2.datum.min(),max_value=df_2.datum.max(),value=(df_2.datum.min(), df_2.datum.max()),format="DD-MM-YYYY")
  
    df_2 = df_2[(df_2['datum']>=d[0]) & (df_2['datum']<=d[1])]

    st.sidebar.divider()

    df_2["icon_data"] = df_2.apply(lambda x: icon_dictionary[x["soortgroup"]][x["sp"]][x["functie"]] if x["soortgroup"] in ['Vogels','Vleermuizen'] 
                                   else icon_dictionary[x["soortgroup"]][x["functie"]], 
                                   axis=1
                     )
    
    map = folium.Map(location=(df_2["lat"].mean(), df_2["lng"].mean()),zoom_start=11,tiles=None)
    LocateControl(auto_start=True).add_to(map)
    Fullscreen().add_to(map)
    
    functie_dictionary = {}
    functie_len = df_2['functie'].unique()
    
    for functie in functie_len:
        functie_dictionary[functie] = folium.FeatureGroup(name=functie)     
    
    for feature_group in functie_dictionary.keys():
        map.add_child(functie_dictionary[feature_group])

    folium.TileLayer('OpenStreetMap',overlay=False,show=True,name="Stratenkaart").add_to(map)
    folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False,name="Witte kaart").add_to(map)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',attr='Google_map',overlay=False,show=False,name="Satellietkaart").add_to(map)
    folium.LayerControl().add_to(map)    

    groups={}

    for group in choice_opdracht:
        groups[group] = list(df_2[df_2.soortgroup==group]["functie"].unique())
        feature = [functie_dictionary[i] for i in groups[group]]
    
        key_list = list(DICT_SORTGROUP.keys())
        val_list = list(DICT_SORTGROUP.values())
        position = val_list.index(group)
        
        groups[group] = feature
    
    groups = dict(zip(soortgroup, list(groups.values())))
    GroupedLayerControl(
        groups=groups,
        exclusive_groups=False,
        collapsed=True,
    ).add_to(map)

    for i in range(len(df_2)):

        if df_2.iloc[i]['geometry_type'] == "Point":

            if (df_2.iloc[i]['sp']=="Huismus") & (df_2.iloc[i]['functie'] in ["mogelijke nestlocatie","nestlocatie"]):
                ICON_SIZE_2 = ICON_SIZE_huismus

            elif df_2.iloc[i]['functie'] == "Waarneming rat doorgegeven, geen actie op ondernomen":
                ICON_SIZE_2 = ICON_SIZE_rat_maybe

            else:
                ICON_SIZE_2 = ICON_SIZE
                

            html = popup_html(i)
            popup = folium.Popup(folium.Html(html, script=True), max_width=300)
            fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]
    
            folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                          popup=popup,
                          icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE_2)
                         ).add_to(fouctie_loop)
                

        elif df_2.iloc[i]['geometry_type'] == "LineString":

            folium.PolyLine(df_2.iloc[i]['coordinates']).add_to(fg)

        
    col_1,col_2,col_3 = st.columns([1,11,1],gap="small") 

    with col_2:
        output_2 = st_folium(map,returned_objects=["last_active_drawing"],width=OUTPUT_width, height=OUTPUT_height,feature_group_to_add=list(functie_dictionary.values()))

except:
    st.image("https://media.istockphoto.com/photos/open-empty-cardboard-box-on-a-white-background-picture-id172167710?k=6&m=172167710&s=612x612&w=0&h=Z4fueCweh9q-X_VBRAPCYSalyaAnXG3ioErb8oJSVek=")
    st.stop()
