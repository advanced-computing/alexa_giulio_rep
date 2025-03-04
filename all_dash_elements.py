from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import streamlit as st
from streamlit_extras.let_it_rain import rain

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

spotify_data = call_api(dataset_path, file_name)

# Separate artists into individual categories
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data = spotify_data.explode("artists")

# Filter for Italy and the US
df_italy = spotify_data[spotify_data["country"] == "IT"]
df_us = spotify_data[spotify_data["country"] == "US"]

# Create a radio button widget to simulate pill navigation
selection = st.selectbox("Country:", ("Italy", "US", "Both"))

#make it rain: 
def rain_emojis(emoji):
        rain(
            emoji=emoji,
            font_size=54,
            falling_speed=10,
            animation_length=5,
        )

#dashboard per country
if selection == "Italy":
    #italy charts
    rain_emojis("🇮🇹")

elif selection == "US":
#US charts
    rain_emojis("🇺🇸")
elif selection == "Both":
    pass
    rain_emojis("🎵")