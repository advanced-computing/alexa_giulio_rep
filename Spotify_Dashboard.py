import streamlit as st
import pandas_gbq
from google.oauth2 import service_account
import plotly.express as px
import pandas as pd
#import warnings
import folium
from helper_functions_notebook import rain_emojis
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

LOGO_URL_SMALL = "https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Full_Logo_RGB_Green.png"
st.logo(
    LOGO_URL_SMALL,
    link="https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Full_Logo_RGB_Green.png",
    icon_image=LOGO_URL_SMALL,
)
st.title("Spotify Streaming Analysis")
st.header("by Alexa and Giulio")
st.write("Thanks for stopping by our dashboard! This app uses Kaggle's \"Top Spotify Songs in 73 Countries (Daily Updated)\" dataset to analyze music trends across the world. Hope you enjoy!")
st.markdown("[Link to dataset](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated?resource=download)")

# bigquery
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
project_id = st.secrets["gcp_service_account"]["project_id"]
spotify_data = "spotify"
table = "universal_top_spotify_songs"
query = f"""
    SELECT DISTINCT artists, country, name, is_explicit, speechiness, danceability, acousticness, liveness
    FROM `{project_id}.{spotify_data}.{table}` 
    WHERE country IN ('IT','US','FR','ES','GB')
"""  
spotify_data = pandas_gbq.read_gbq(query, project_id=project_id, credentials=credentials)

# cleaning the data
spotify_data["artists"] = spotify_data["artists"].astype(str).str.split(", ")
spotify_data2 = spotify_data.explode("artists")
spotify_data2["artists"] = spotify_data2["artists"].str.strip("[]'\" ")


#creating list of coordinates and corresponding pages
locations = {
    "Italy": [41.8719, 12.5674, "pages/1_Italy.py"],  
    "US": [38.79468, -74.0060, "pages/2_US.py"],  
    "Great Britain": [51.5074, -0.1278, "pages/3_Great_Britain.py"], 
    "France": [46.6034, 1.8883, "pages/4_France.py"],  
    "Spain": [40.4637, -3.7492, "pages/5_Spain.py"] 
}

#setting initial location for map
m = folium.Map(location=[46.1101, -37.0669], zoom_start=2.5)

#adding country markers on map
marker_cluster = MarkerCluster().add_to(m)
for country, (lat, lon, page) in locations.items():
    folium.Marker(
        location=[lat, lon],
        popup=country,
        tooltip=country,
        icon=folium.Icon(color='blue')
    ).add_to(marker_cluster)

#display map
st.write("Check out this map to see which countries we feature on our app:")
st_folium(m, width=700, height=500)

#emoji rain
rain_emojis("🎵") 

#choosing country
selection = st.selectbox("Select a country:", list(locations.keys()))

if st.button("Go to selected page"):
    st.switch_page(locations[selection][2])

#rating
st.write("Rate us:")
with st.form("feedback_form"):
    rating = st.feedback(options="stars")
    submitted = st.form_submit_button("Submit")

if submitted:
    st.session_state.rating = rating
    st.write(f"Thanks for rating us!")
#streamlit run Spotify_Dashboard.py 

