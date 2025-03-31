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
st.header("Welcome to Great Britain!")
rain_emojis("🇬🇧")

#sectioning country specific data
df_gb = spotify_data2[spotify_data2["country"] == "GB"]

#artist data
df_gb["artists"] = df_gb["artists"].astype(str) 
artist_counts = df_gb["artists"].value_counts()
top_artist = artist_counts.idxmax()

#top artist
st.write("#1 Trending Artist in 🇬🇧 Today")
container = st.container(border=True)
container.write(f"{top_artist} 🎤 ")

#song data
df_gb["name"] = df_gb["name"].astype(str)
song_counts = df_gb["name"].value_counts()
top_song = song_counts.idxmax()

#top song
st.write("#1 Trending Song in 🇬🇧 Today")
container = st.container(border=True)
container.write(f"{top_song} 🎵")

#map
coordinates = [54.7020, -3.2750]
map = folium.Map(location=[coordinates[0], coordinates[1]], zoom_start=6)

folium.Marker(
    location=[coordinates[0], coordinates[1]],
    popup="Great Britain",
    tooltip="Great Britain",
    icon=folium.Icon(color="red")
).add_to(map)

st_folium(map, width=700, height=500)

#explicit pie
df_gb["is_explicit"] = df_gb["is_explicit"].astype(str).replace({"True": "Yes", "False": "No"})
explicit_df = df_gb.groupby("is_explicit").size().reset_index(name="count") 

explicit_pie = px.pie(explicit_df, 
                names="is_explicit", 
                values="count", 
                hole=0.3, 
                title="Explicit vs Non Explicit Songs: Do listeners prefer songs with or without profanity?",
                labels={"is_explicit": "Explicit?"}
                )
explicit_pie.update_traces(marker=dict(colors=["red", "green"]))

st.plotly_chart(explicit_pie)
