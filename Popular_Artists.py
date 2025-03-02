import streamlit as st
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

# setting up api
def authenticate_kaggle_api():
    api = KaggleApi()
    api.authenticate()
    return api

# setting up and downloading path
def download_dataset(api, dataset_path):
    api.dataset_download_files(dataset_path, path='./', unzip=True, quiet=False)

# making sure dataset can load properly by skipping bad rows
def get_problematic_rows(file_path):
    problematic_rows = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.count(',') < 10 or len(line.split(',')) > 50:  # used chat gpt to figure this logic out
                problematic_rows.append(i)
    return problematic_rows

# loading dataset
def load_dataset(file_path, skip_rows):
    return pd.read_csv(file_path, skiprows=skip_rows, on_bad_lines='skip')

# calling on API
def call_api(dataset_path, file_name):
    api = authenticate_kaggle_api()
    download_dataset(api, dataset_path)
    
    file_path = f'./{file_name}'
    skip_rows = get_problematic_rows(file_path)
    
    df = load_dataset(file_path, skip_rows)
    return df

# dataset path and file name
dataset_path = 'asaniczka/top-spotify-songs-in-73-countries-daily-updated'
file_name = 'universal_top_spotify_songs.csv'

# calling api
spotify_data = call_api(dataset_path, file_name)

# separate artists into individual categories in case they're grouped together (re. collabs)
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data = spotify_data.explode("artists")

# group artists by average popularity
artist_popularity = spotify_data.groupby("artists")["popularity"].mean()

# select subset of artists to display for simplicity
artist_popularity = artist_popularity.sort_values(ascending=False)
popular_artists = artist_popularity.head(10)

# create widget to choose how many artists you can see
display_widget = st.slider("Number of Artists to Display", min_value=1, max_value=10, value=10, step=1)

# apply widget to artist_popularity subset
popular_artists = popular_artists.head(display_widget)

# make bar chart
st.title("Popular Spotify Artists")
st.bar_chart(popular_artists)
