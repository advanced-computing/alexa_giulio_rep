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
from helper_functions_notebook import danceability_mex_it, acousticness_mex_it, danceability_mex_us, acousticness_mex_us, danceability_mex_fr, acousticness_mex_fr, danceability_mex_es, acousticness_mex_es # noqa: E402

#Intro
st.header("Bienvenido a Messico!")
rain_emojis("🇲🇽")

#sectioning country specific data
df_mex = spotify_data2[spotify_data2["country"] == "MX"]

#artist data
df_mex["artists"] = df_mex["artists"].astype(str) 
artist_counts = df_mex["artists"].value_counts()
top_artist = artist_counts.idxmax()

#top artist
st.write("#1 Trending Artist in 🇲🇽 Today")
container = st.container(border=True)
container.write(f"{top_artist} 🎤 ")

#song data
df_mex["name"] = df_mex["name"].astype(str)
song_counts = df_mex["name"].value_counts()
top_song = song_counts.idxmax()

#top song
st.write("#1 Trending Song in 🇲🇽 Today")
container = st.container(border=True)
container.write(f"{top_song} 🎵")

#map
coordinates = [23.6345, -102.5528]
map = folium.Map(location=[coordinates[0], coordinates[1]], zoom_start=6)

folium.Marker(
    location=[coordinates[0], coordinates[1]],
    popup="Mexico",
    tooltip="Mexico",
    icon=folium.Icon(color="red")
).add_to(map)

st_folium(map, width=700, height=500)

#explicit pie
df_mex["is_explicit"] = df_mex["is_explicit"].astype(str).replace({"True": "Yes (With Profanity)", "False": "No (Without Profanity)"})
explicit_df = df_mex.groupby("is_explicit").size().reset_index(name="count") 

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
df_mex['loudness'] = df_mex['loudness'].astype(float)

loudness_hist = px.histogram(df_mex, x='loudness', nbins=30,
                              labels={"loudness": "Loudness"},
                              title="How Loud Is Music in Mexico? A Look at the Distribution of Decibel Levels in Songs")

loudness_hist.add_vline(
    x=-14,  # Position of the line at -14 dB
    line=dict(color="red", width=2, dash="dash"),  # Red dashed line
    annotation_text="Spotify's Target Loudness (-14 dB)",
    annotation_position="top left"
)

st.plotly_chart(loudness_hist)

selection = st.pills(
    "Select a country:",
    options=["United States","France","Italy","Spain"]
)

if selection == "Italy":
    st.plotly_chart(danceability_mex_it)
    st.plotly_chart(acousticness_mex_it)
elif selection == "France":
    st.plotly_chart(danceability_mex_fr)
    st.plotly_chart(acousticness_mex_fr)
elif selection == "Spain":
    st.plotly_chart(danceability_mex_es)
    st.plotly_chart(acousticness_mex_es)
elif selection == "United States":
    st.plotly_chart(danceability_mex_us)
    st.plotly_chart(acousticness_mex_us)
