from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import streamlit as st
import plotly.express as px

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
# Filter for US and Italy
df_US_IT = spotify_data[spotify_data["country"].isin(["US", "IT"])]
df_US_IT2 = df_US_IT[df_US_IT["snapshot_date"].isin(["2025-03-01"])]
# Define custom colors for US and Italy
custom_colors = {
    "US": "#1f77b4",  # Blue shade for the US
    "IT": "#d62728"   # Red shade for Italy
}

# Create bar chart with custom colors
fig = px.bar(df_US_IT2, 
             x="name", 
             y="daily_rank", 
             color="country", 
             barmode="group",
             title="Top 10 Songs in the US vs Italy",
             labels={"daily_rank": "Daily Rank", "name": "Song"},
             height=500,
             color_discrete_map=custom_colors)  # Apply custom color mapping

# Invert the rank axis (1st is best)
fig.update_yaxes(autorange="reversed")

# Show the chart
fig.show()


# Show in Streamlit
#import streamlit as st
#st.title("Top 10 Songs in the US vs Italy")
#st.plotly_chart(fig)