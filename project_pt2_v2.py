import streamlit as st
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

# trying this out using the API set up I made last week
api = KaggleApi()
api.authenticate()

dataset_path = 'asaniczka/top-spotify-songs-in-73-countries-daily-updated'
api.dataset_download_files(dataset_path, path='./', unzip=True)
file_path = "universal_top_spotify_songs.csv"  

# loading data into pandas
spotify_data = pd.read_csv(file_path, skiprows=[1306857])

# separate artists into individual categories in case they're grouped together (re. collabs)
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data = spotify_data.explode("artists")

# group artists by average popularity
artist_popularity = spotify_data.groupby("artists")["popularity"].mean() 

# select subset of artists to display for simplicity
top_artists = artist_popularity.head(40)

# create widget to choose how many artists you can see
display_widget = st.slider("Number of Artists to Display", min_value=1, max_value=40, value=20, step=1)

# apply widget to artist_popularity subset
top_artists = top_artists.head(display_widget)

# make bar chart
st.title("Top 40 Spotify Artists")
st.bar_chart(artist_popularity)

# $streamlit run project_pt2.py  

# disclaimer: used ChatGPT to figure out the .explode() function and to troubleshoot API loading issues in order to recategorize the artists properly