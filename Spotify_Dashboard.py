import os
import zipfile
import gzip
import shutil
import pandas as pd
import streamlit as st
import pandas_gbq
from google.oauth2 import service_account
from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import storage
from google.cloud import bigquery
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from streamlit_extras.let_it_rain import rain

# setup
bucket_name = "run-sources-sipa-adv-c-alexa-giulio-us-central1"
kaggle_dataset = "asaniczka/top-spotify-songs-in-73-countries-daily-updated"
local_zip = "top-spotify-songs-in-73-countries-daily-updated.zip"
local_csv = "universal_top_spotify_songs.csv"

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
project_id = st.secrets["gcp_service_account"]["project_id"]
dataset_id = "spotify"
table_id = "universal_top_spotify_songs"
table_ref = f"{project_id}.{dataset_id}.{table_id}"

# cache and big query
@st.cache_data(ttl=3600)
def update_bigquery_from_kaggle():
    try:
        api = KaggleApi()
        api.authenticate()

        api.dataset_download_files(kaggle_dataset, path=".", unzip=False)
        with zipfile.ZipFile(local_zip, 'r') as zip_ref:
            zip_ref.extractall(".")

        df = pd.read_csv(local_csv, parse_dates=['snapshot_date'])
        latest_snapshot = df['snapshot_date'].max()

        df_latest = df[
            (df['snapshot_date'] == latest_snapshot) &
            (df['country'].isin(['US', 'FR', 'IT', 'ES', 'MX']))
        ]

        compressed_csv = "latest_snapshot.csv.gz"
        df_latest.to_csv(compressed_csv, index=False, compression='gzip')

        storage_client = storage.Client(credentials=credentials, project=project_id)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(compressed_csv)
        blob.upload_from_filename(compressed_csv)

        bq_client = bigquery.Client(credentials=credentials, project=project_id)
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            compression_type=bigquery.Compression.GZIP,
        )

        uri = f"gs://{bucket_name}/{compressed_csv}"
        load_job = bq_client.load_table_from_uri(uri, table_ref, job_config=job_config)
        load_job.result()

        os.remove(local_csv)
        os.remove(compressed_csv)

        return latest_snapshot

    except Exception as e:
        return None

# loading data
#with st.spinner("⏳ Updating dataset from Kaggle to BigQuery..."):
    #latest_snapshot = update_bigquery_from_kaggle()
latest_snapshot = update_bigquery_from_kaggle()

if latest_snapshot is None:
    latest_date_query = f"SELECT MAX(snapshot_date) AS latest_date FROM `{table_ref}`"
    latest_date_df = pandas_gbq.read_gbq(latest_date_query, project_id=project_id, credentials=credentials)
    latest_snapshot = latest_date_df['latest_date'][0]

#st.info(f"📅 Latest data in BigQuery: {latest_snapshot}")

query = f"""
    SELECT DISTINCT artists, country, name, is_explicit, speechiness, danceability, acousticness, liveness
    FROM `{table_ref}`
    WHERE country IN ('IT','US','FR','ES','MX')
    AND snapshot_date = DATE('{latest_snapshot}')
"""
spotify_data = pandas_gbq.read_gbq(query, project_id=project_id, credentials=credentials)

# cleaning and visuals

# cleaning the data
spotify_data["artists"] = spotify_data["artists"].astype(str).str.split(", ")
spotify_data2 = spotify_data.explode("artists")
spotify_data2["artists"] = spotify_data2["artists"].str.strip("[]'\" ")

#intro
LOGO_URL_SMALL = "https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Full_Logo_RGB_Green.png"
st.logo(
    LOGO_URL_SMALL,
    link="https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Full_Logo_RGB_Green.png",
    icon_image=LOGO_URL_SMALL,
)
st.title("Spotify Streaming Analysis")
st.header("by Alexa and Giulio")
st.write("Thanks for stopping by our dashboard! This app uses Kaggle's \"Top Spotify Songs in 73 Countries (Daily Updated)\" dataset to analyze music trends across the world. Hope you enjoy!")
st.markdown("[Link to dataset](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated?resource=download)")

def rain_emojis(emoji):
        rain(
            emoji=emoji,
            font_size=54,
            falling_speed=10,
            animation_length=5,
        )
rain_emojis("🎵") 

#creating list of coordinates and corresponding pages
locations = {
    "Italy": [41.8719, 12.5674, "pages/Italy.py"],  
    "United States": [38.79468, -74.0060, "pages/United_States.py"],  
    "Mexico": [19.4326, -99.1332, "pages/Mexico.py"], 
    "France": [46.6034, 1.8883, "pages/France.py"],  
    "Spain": [40.4637, -3.7492, "pages/Spain.py"] 
}

#setting initial location for map
map = folium.Map(location=[46.1101, -37.0669], zoom_start=2)

#adding country markers on map
marker_cluster = MarkerCluster().add_to(map)
for country, (lat, lon, page) in locations.items():
    folium.Marker(
        location=[lat, lon],
        popup=country,
        tooltip=country,
        icon=folium.Icon(color='blue')
    ).add_to(marker_cluster)

#choosing country
selection = st.pills(
    "Select a country:",
    options=list(locations.keys()),
)

# Automatically redirect if a selection is made
if selection:
    st.switch_page(locations[selection][2])
    
#display map
st.write("Check out this map to see which countries we feature on our app:")
st_folium(map, width=700, height=500)

#streamlit run Spotify_Dashboard.py 