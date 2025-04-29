import streamlit as st
import plotly.express as px
import sys
import os
import folium
from streamlit_folium import st_folium
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Spotify_Dashboard import spotify_data2, rain_emojis # noqa: E402
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
utils_path = os.path.join(project_root, "utils")
if utils_path not in sys.path:
    sys.path.append(utils_path)
from helper_functions_notebook import danceability_fr_it, acousticness_fr_it, danceability_fr_us, acousticness_fr_us, danceability_fr_mex, acousticness_fr_mex, danceability_fr_es, acousticness_fr_es # noqa: E402

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

#loudness histogram
df_france['loudness'] = df_france['loudness'].astype(float)

loudness_hist = px.histogram(df_france, x='loudness', nbins=30,
                              labels={"loudness": "Loudness"},
                              title="How Loud Is Music in France? A Look at the Distribution of Decibel Levels in Songs")

loudness_hist.add_vline(
    x=-14,  # Position of the line at -14 dB
    line=dict(color="red", width=2, dash="dash"),  # Red dashed line
    annotation_text="Spotify's Target Loudness (-14 dB)",
    annotation_position="top left"
)

st.plotly_chart(loudness_hist)

selection = st.pills(
    "Select a country:",
    options=["United States","Mexico","Italy","Spain"]
)

if selection == "Italy":
    st.plotly_chart(danceability_fr_it)
    st.plotly_chart(acousticness_fr_it)
elif selection == "Mexico":
    st.plotly_chart(danceability_fr_mex)
    st.plotly_chart(acousticness_fr_mex)
elif selection == "Spain":
    st.plotly_chart(danceability_fr_es)
    st.plotly_chart(acousticness_fr_es)
elif selection == "United States":
    st.plotly_chart(danceability_fr_us)
    st.plotly_chart(acousticness_fr_us)
