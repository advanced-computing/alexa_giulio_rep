import gzip
import shutil
import streamlit as st
import pandas_gbq
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from streamlit_extras.let_it_rain import rain
from spotifydataload import table_ref, latest_snapshot, project_id, credentials, folium, get_bq_credentials

query = f"""
    SELECT DISTINCT artists, country, name, is_explicit, speechiness, danceability, acousticness, liveness
    FROM `{table_ref}`
    WHERE country IN ('IT','US','FR','ES','MX')
    AND snapshot_date = DATE('{latest_snapshot}')
"""
credentials = get_bq_credentials()

spotify_data = pandas_gbq.read_gbq(query, project_id=project_id, credentials=credentials)

# cleaning and visuals

# cleaning the data
spotify_data["artists"] = spotify_data["artists"].astype(str).str.split(", ")
spotify_data2 = spotify_data.explode("artists")
spotify_data2["artists"] = spotify_data2["artists"].str.strip("[]'\" ")

#intro
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

def rain_emojis(emoji):
        rain(
            emoji=emoji,
            font_size=54,
            falling_speed=10,
            animation_length=5,
        )
rain_emojis("🎵") 

#creating list of coordinates and corresponding pages
locations = {
    "Italy": [41.8719, 12.5674, "pages/Italy.py"],  
    "United States": [38.79468, -74.0060, "pages/United_States.py"],  
    "Mexico": [19.4326, -99.1332, "pages/Mexico.py"], 
    "France": [46.6034, 1.8883, "pages/France.py"],  
    "Spain": [40.4637, -3.7492, "pages/Spain.py"] 
}

#setting initial location for map
map = folium.Map(location=[46.1101, -37.0669], zoom_start=2)

#adding country markers on map
marker_cluster = MarkerCluster().add_to(map)
for country, (lat, lon, page) in locations.items():
    folium.Marker(
        location=[lat, lon],
        popup=country,
        tooltip=country,
        icon=folium.Icon(color='blue')
    ).add_to(marker_cluster)

#choosing country
selection = st.pills(
    "Select a country:",
    options=list(locations.keys()),
)

# Automatically redirect if a selection is made
if selection:
    st.switch_page(locations[selection][2])
    
#display map
st.write("Check out this map to see which countries we feature on our app:")
st_folium(map, width=700, height=500)

#streamlit run Spotify_Dashboard.py 