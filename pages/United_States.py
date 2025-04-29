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
from helper_functions_notebook import danceability_us_it, acousticness_us_it, danceability_us_mex, acousticness_us_mex, danceability_us_fr, acousticness_us_fr, danceability_us_es, acousticness_us_es # noqa: E402

#Intro
st.header("Welcome to the US!")
rain_emojis("🇺🇸")

#sectioning country specific data
df_us = spotify_data2[spotify_data2["country"] == "US"]

#artist data
df_us["artists"] = df_us["artists"].astype(str) 
artist_counts = df_us["artists"].value_counts()
top_artist = artist_counts.idxmax()

#top artist
st.write("#1 Trending Artist in 🇺🇸 Today")
container = st.container(border=True)
container.write(f"{top_artist} 🎤 ")

#song data
df_us["name"] = df_us["name"].astype(str)
song_counts = df_us["name"].value_counts()
top_song = song_counts.idxmax()

#top song
st.write("#1 Trending Song in 🇺🇸 Today")
container = st.container(border=True)
container.write(f"{top_song} 🎵")

#map
coordinates = [39.8283, -98.5795]
map = folium.Map(location=[coordinates[0], coordinates[1]], zoom_start=4)

folium.Marker(
    location=[coordinates[0], coordinates[1]],
    popup="US",
    tooltip="US",
    icon=folium.Icon(color="red")
).add_to(map)

st_folium(map, width=700, height=500)

#explicit pie
df_us["is_explicit"] = df_us["is_explicit"].astype(str).replace({"True": "Yes (With Profanity)", "False": "No (Without Profanity)"})
explicit_us = df_us.groupby("is_explicit").size().reset_index(name="count") 

explicit_pie = px.pie(explicit_us, 
                names="is_explicit", 
                values="count", 
                hole=0.3, 
                title=" Do listeners prefer songs with or without profanity?",
                labels={"is_explicit": "Explicit?"}
                )
explicit_pie.update_traces(marker=dict(colors=["red", "green"]))

st.plotly_chart(explicit_pie)

#loudness histogram
df_us['loudness'] = df_us['loudness'].astype(float)

loudness_hist = px.histogram(df_us, x='loudness', nbins=30,
                              labels={"loudness": "Loudness"},
                              title="How Loud Is Music in the US? A Look at the Distribution of Decibel Levels in Songs")

loudness_hist.add_vline(
    x=-14,  # Position of the line at -14 dB
    line=dict(color="red", width=2, dash="dash"),  # Red dashed line
    annotation_text="Spotify's Target Loudness (-14 dB)",
    annotation_position="top left"
)

st.plotly_chart(loudness_hist)

selection = st.pills(
    "Select a country:",
    options=["Mexico","France","Italy","Spain"]
)

if selection == "Italy":
    st.plotly_chart(danceability_us_it)
    st.plotly_chart(acousticness_us_it)
elif selection == "Mexico":
    st.plotly_chart(danceability_us_mex)
    st.plotly_chart(acousticness_us_mex)
elif selection == "Spain":
    st.plotly_chart(danceability_us_es)
    st.plotly_chart(acousticness_us_es)
elif selection == "France":
    st.plotly_chart(danceability_us_fr) 
    st.plotly_chart(acousticness_us_fr)
