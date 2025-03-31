import streamlit as st
import plotly.express as px
import sys
import os
import folium
from streamlit_folium import st_folium
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Spotify_Dashboard import spotify_data2 # noqa: E402
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
utils_path = os.path.join(project_root, "utils")
if utils_path not in sys.path:
    sys.path.append(utils_path)
from helper_functions_notebook import rain_emojis # noqa: E402

#Intro
st.header("Bienvenue en France!")
rain_emojis("🇫🇷")

#sectioning country specific data
df_france = spotify_data2[spotify_data2["country"] == "FR"]

#artist data
df_france["artists"] = df_france["artists"].astype(str) 
artist_counts = df_france["artists"].value_counts()
top_artist = artist_counts.idxmax()

#top artist
st.write("#1 Trending Artist in 🇫🇷 Today")
container = st.container(border=True)
container.write(f"{top_artist} 🎤 ")

#song data
df_france["name"] = df_france["name"].astype(str)
song_counts = df_france["name"].value_counts()
top_song = song_counts.idxmax()

#top song
st.write("#1 Trending Song in 🇫🇷 Today")
container = st.container(border=True)
container.write(f"{top_song} 🎵")

#map
coordinates = [46.6034, 1.8883]
map = folium.Map(location=[coordinates[0], coordinates[1]], zoom_start=6)

folium.Marker(
    location=[coordinates[0], coordinates[1]],
    popup="France",
    tooltip="France",
    icon=folium.Icon(color="red")
).add_to(map)

st_folium(map, width=700, height=500)

#explicit pie
df_france["is_explicit"] = df_france["is_explicit"].astype(str).replace({"True": "Yes (With Profanity)", "False": "No (Without Profanity)"})
explicit_df = df_france.groupby("is_explicit").size().reset_index(name="count") 

explicit_pie = px.pie(explicit_df, 
                names="is_explicit", 
                values="count", 
                hole=0.3, 
                title="Do listeners prefer songs with or without profanity?",
                labels={"is_explicit": "Explicit?"}
                )
explicit_pie.update_traces(marker=dict(colors=["red", "green"]))

st.plotly_chart(explicit_pie)