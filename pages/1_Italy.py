import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Spotify_Dashboard import spotify_data2
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
utils_path = os.path.join(project_root, "utils")
if utils_path not in sys.path:
    sys.path.append(utils_path)
from helper_functions_notebook import call_api, rain_emojis 

#Intro
st.header("Benvenuto a Italia!")
rain_emojis("🇮🇹")

#sectioning country specific data
df_italy = spotify_data2[spotify_data2["country"] == "IT"]

#artist data
df_italy["artists"] = df_italy["artists"].astype(str) 
artist_counts = df_italy["artists"].value_counts()
top_artist_italy = artist_counts.idxmax()

#top artist
st.write("#1 Trending Artist in 🇮🇹 Today")
container = st.container(border=True)
container.write(f"{top_artist_italy}")

#song data
df_italy["name"] = df_italy["name"].astype(str)
song_counts = df_italy["name"].value_counts()
top_song_italy = song_counts.idxmax()

#top song
st.write("#1 Trending Song in 🇮🇹 Today")
container = st.container(border=True)
container.write(f"{top_song_italy}")

#explicit pie
df_italy["is_explicit"] = df_italy["is_explicit"].astype(str).replace({"True": "Yes", "False": "No"})
explicit_italy = df_italy.groupby("is_explicit").size().reset_index(name="count") 

italy_pie = px.pie(explicit_italy, 
                names="is_explicit", 
                values="count", 
                hole=0.3, 
                title="Explicit vs Non Explicit Songs in Italy: Do listeners prefer songs with or without profanity?",
                labels={"is_explicit": "Explicit?"}
                )
italy_pie.update_traces(marker=dict(colors=["red", "green"]))

st.plotly_chart(italy_pie)
