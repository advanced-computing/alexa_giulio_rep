from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import streamlit as st

#setting up api
def authenticate_kaggle_api():
    api = KaggleApi()
    api.authenticate()
    return api

#setting up and downloading path
def download_dataset(api, dataset_path):
    try:
        api.dataset_download_files(dataset_path, path='./', unzip=True, quiet=False)
    except Exception as e:
        raise RuntimeError(f"Error downloading dataset: {e}")

#making sure dataset can load properly by skipping bad rows
def get_problematic_rows(file_path):
    problematic_rows = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.count(',') < 10 or len(line.split(',')) > 50: #used chat gpt to figure this logic out
                problematic_rows.append(i)
    return problematic_rows

#loading dataset
def load_dataset(file_path, skip_rows):
    try:
        df = pd.read_csv(file_path, skiprows=skip_rows)
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {e}")

#calling on API
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

# Filter for Italy and select the snapshot date
df_italy = spotify_data[spotify_data["country"] == "IT"]

# Get the most frequent artist (the #1 artist from Italy)
top_artist_italy = df_italy['artists'].value_counts().idxmax()

with st.container():
    # Use Markdown for a styled title
    st.markdown(
        f"""
        <div style="padding: 20px; background-color: #f2f2f2; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="text-align: center; color: #1DB954;">🎶 #1 Singer from Italy 🎶</h3>
            <h4 style="text-align: center; color: #1DB954;">{top_artist_italy}</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )