import streamlit as st
import pandas_gbq
from google.oauth2 import service_account
import plotly.express as px
import pandas as pd
import warnings
from helper_functions_notebook import rain_emojis  # keep this for visuals

# Google Cloud BigQuery Setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
project_id = st.secrets["gcp_service_account"]["project_id"]
dataset = "spotify"
table = "universal_top_spotify_songs"
query = f"""
    SELECT * 
    FROM `{project_id}.{dataset}.{table}` 
    LIMIT 2000
"""  # limit to 2000 rows for performance

# Load Data from BigQuery
spotify_data = pandas_gbq.read_gbq(query, project_id=project_id, credentials=credentials)

# Cleaning & Transformations
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data2 = spotify_data.explode("artists")

df_italy = spotify_data2[spotify_data2["country"] == "IT"]
df_us = spotify_data2[spotify_data2["country"] == "US"]

top_artist_italy = df_italy["artists"].value_counts().idxmax()
top_song_italy = df_italy["name"].value_counts().idxmax()

top_artist_us = df_us["artists"].value_counts().idxmax()
top_song_us = df_us["name"].value_counts().idxmax()

# Pie Charts
df_italy["is_explicit"] = df_italy["is_explicit"].astype("object").replace({True: "Yes", False: "No"})  
explicit_italy = df_italy.groupby("is_explicit").size().reset_index(name="count") 

italy_pie = px.pie(explicit_italy, 
                names="is_explicit", 
                values="count", 
                hole=0.3, 
                title="Explicit vs Non Explicit Songs in Italy",
                labels={"is_explicit": "Explicit?"})
italy_pie.update_traces(marker=dict(colors=["red", "green"]))

df_us["is_explicit"] = df_us["is_explicit"].astype("object").replace({True: " Yes", False: " No"})  
explicit_us = df_us.groupby("is_explicit").size().reset_index(name="count")  

us_pie = px.pie(explicit_us, 
                names="is_explicit", 
                values="count", 
                hole=0.3, 
                title="Explicit vs Non Explicit Songs in US",
                labels={"is_explicit": "Explicit?"})
us_pie.update_traces(marker=dict(colors=["red", "blue"]))

# Speechiness
df_speechiness_sum = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Speechiness": [
        df_italy["speechiness"].sum(),
        df_us["speechiness"].sum()
    ]
})
speechiness_bar = px.bar(df_speechiness_sum, x="Country", y="Total Speechiness",
                         title="Who prefers speechy songs?",
                         labels={"Total Speechiness": "Speechiness Score"},
                         color="Country")

# Danceability
df_danceability_sum = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Danceability": [
        df_italy["danceability"].sum(),
        df_us["danceability"].sum()
    ]
})
danceability = px.bar(df_danceability_sum, x="Country", y="Total Danceability",
                      title="Who prefers danceable songs?",
                      labels={"Total Danceability": "Danceability Score"},
                      color="Country")

# Acousticness
df_acousticness_sum = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Acousticness": [
        df_italy["acousticness"].sum(),
        df_us["acousticness"].sum()
    ]
})
acousticness_chart = px.bar(df_acousticness_sum, x="Country", y="Total Acousticness",
                            title="Which country has more acoustic songs?",
                            labels={"Total Acousticness": "Acousticness Score"},
                            color="Country")

# Liveness
df_liveness_sum = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Liveness": [
        df_italy["liveness"].sum(),
        df_us["liveness"].sum()
    ]
})
liveness_chart = px.bar(df_liveness_sum, x="Country", y="Total Liveness",
                        title="Which country has more live-feeling songs?",
                        labels={"Total Liveness": "Liveness Score"},
                        color="Country")

# Streamlit App UI
LOGO_URL = "https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Full_Logo_RGB_Green.png"
st.logo(LOGO_URL, link=LOGO_URL, icon_image=LOGO_URL)

st.title("Spotify Streaming Analysis")
st.header("by Alexa and Giulio")
st.write("This dashboard uses BigQuery to analyze Spotify streaming trends in Italy and the US.")
st.markdown("[Link to dataset](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated?resource=download)")

selection = st.selectbox("Country:", ("Both", "Italy", "US"))

if selection == "Both":
    rain_emojis("🇮🇹 🇺🇸")
    st.write("#1 Trending Artist in 🇮🇹 Today")
    st.container(border=True).write(f"{top_artist_italy}")
    st.write("#1 Trending Artist in 🇺🇸 Today")
    st.container(border=True).write(f"{top_artist_us}")
    st.write("#1 Trending Song in 🇮🇹 Today")
    st.container(border=True).write(f"{top_song_italy}")
    st.write("#1 Trending Song in 🇺🇸 Today")
    st.container(border=True).write(f"{top_song_us}")
    st.plotly_chart(italy_pie)
    st.plotly_chart(us_pie)
    st.plotly_chart(speechiness_bar)
    st.plotly_chart(danceability)
    st.plotly_chart(acousticness_chart)
    st.plotly_chart(liveness_chart)

elif selection == "Italy":
    rain_emojis("🇮🇹")
    st.write("#1 Trending Artist 🎤 Today")
    st.container(border=True).write(f"{top_artist_italy}")
    st.write("#1 Trending Song 🎵 Today")
    st.container(border=True).write(f"{top_song_italy}")
    st.plotly_chart(italy_pie)

elif selection == "US":
    rain_emojis("🇺🇸")
    st.write("#1 Trending Artist 🎤 Today")
    st.container(border=True).write(f"{top_artist_us}")
    st.write("#1 Trending Song 🎵 Today")
    st.container(border=True).write(f"{top_song_us}")
    st.plotly_chart(us_pie)