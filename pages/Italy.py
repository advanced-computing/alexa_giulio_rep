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
from helper_functions_notebook import danceability_it_us, acousticness_it_us, danceability_it_mex, acousticness_it_mex, danceability_it_fr, acousticness_it_fr, danceability_it_es, acousticness_it_es # noqa: E402

#Intro
st.header("Benvenuto in Italia!")
rain_emojis("🇮🇹")

#sectioning country specific data
df_italy = spotify_data2[spotify_data2["country"] == "IT"]

#artist data
df_italy["artists"] = df_italy["artists"].astype(str) 
artist_counts = df_italy["artists"].value_counts()
top_artist = artist_counts.idxmax()

#top artist
st.write("#1 Trending Artist in 🇮🇹 Today")
container = st.container(border=True)
container.write(f"{top_artist} 🎤 ")

#song data
df_italy["name"] = df_italy["name"].astype(str)
song_counts = df_italy["name"].value_counts()
top_song = song_counts.idxmax()

#top song
st.write("#1 Trending Song in 🇮🇹 Today")
container = st.container(border=True)
container.write(f"{top_song} 🎵")

#map
coordinates = [41.8719, 12.5674]
map = folium.Map(location=[coordinates[0], coordinates[1]], zoom_start=6)

folium.Marker(
    location=[coordinates[0], coordinates[1]],
    popup="Italy",
    tooltip="Italy",
    icon=folium.Icon(color="red")
).add_to(map)

st_folium(map, width=700, height=500)

#explicit pie
df_italy["is_explicit"] = df_italy["is_explicit"].astype(str).replace({"True": "Yes (With Profanity)", "False": "No (Without Profanity)"})
explicit_italy = df_italy.groupby("is_explicit").size().reset_index(name="count") 

explicit_pie = px.pie(explicit_italy, 
                names="is_explicit", 
                values="count", 
                hole=0.3, 
                title=" Do listeners prefer songs with or without profanity?",
                labels={"is_explicit": "Explicit?"})
explicit_pie.update_traces(marker=dict(colors=["red", "green"]))

st.plotly_chart(explicit_pie)

#loudness histogram
df_italy['loudness'] = df_italy['loudness'].astype(float)

loudness_hist = px.histogram(df_italy, x='loudness', nbins=30,
                              labels={"loudness": "Loudness"},
                              title="How Loud do Italians like their music? Distribution of Decibel Levels in Songs")

st.plotly_chart(loudness_hist)

selection = st.pills(
    "Select a country:",
    options=["United States","Mexico","France","Spain"]
)

if selection == "United States":
    st.plotly_chart(danceability_it_us)
    st.plotly_chart(acousticness_it_us)
elif selection == "Mexico":
    st.plotly_chart(danceability_it_mex)
    st.plotly_chart(acousticness_it_mex)
elif selection == "Spain":
    st.plotly_chart(danceability_it_es)
    st.plotly_chart(acousticness_it_es)
elif selection == "France":
    st.plotly_chart(danceability_it_fr)
    st.plotly_chart(acousticness_it_fr)