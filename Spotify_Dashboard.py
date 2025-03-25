#import os
import streamlit as st
import plotly.express as px
import pandas as pd
#import warnings
from helper_functions_notebook import call_api, rain_emojis
import pandas_gbq
import pydata_google_auth

# configuration
project_id = "sipa-adv-c-alexa-giulio"
dataset = "spotify"
table = "universal_top_spotify_songs"
full_table_id = f"{project_id}.{dataset}.{table}"
scopes = ["https://www.googleapis.com/auth/cloud-platform"]

# load data from api
print("downloading dataset from kaggle...")
spotify_data = call_api("asaniczka/top-spotify-songs-in-73-countries-daily-updated", "universal_top_spotify_songs.csv")
print("dataset loaded successfully.")

# authenticate with google cloud
print("authenticating with google cloud...")
credentials = pydata_google_auth.get_user_credentials(scopes)

# incremental load logic
try:
    print("checking for existing records in bigquery...")
    existing = pandas_gbq.read_gbq(
        f"SELECT DISTINCT name FROM `{full_table_id}`",
        project_id=project_id,
        credentials=credentials
    )

    existing_names = set(existing['name'].str.lower())
    spotify_data["name_lower"] = spotify_data["name"].str.lower()
    new_data = spotify_data[~spotify_data["name_lower"].isin(existing_names)].drop(columns=["name_lower"])

except Exception as e:
    print(f"could not query existing data: {e}")
    print("uploading entire dataset.")
    new_data = spotify_data

# upload to bigquery
if not new_data.empty:
    print(f"uploading {len(new_data)} new records to bigquery...")
    pandas_gbq.to_gbq(
        new_data,
        full_table_id,
        project_id=project_id,
        credentials=credentials,
        if_exists="append"
    )
    print("upload complete.")
else:
    print("no new records to upload.")

# get GCP credentials from secrets
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

# use credentials to query
PROJECT_ID = st.secrets["gcp_service_account"]["project_id"]
DATASET = "spotify"
TABLE = "universal_top_spotify_songs"
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET}.{TABLE}"

query = f"SELECT * FROM `{FULL_TABLE_ID}` LIMIT 10"
df = pandas_gbq.read_gbq(query, project_id=PROJECT_ID, credentials=credentials)

st.write(df)

#name column cleaning
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data2 = spotify_data.explode("artists")

#filtering italy and US
df_italy = spotify_data2[spotify_data2["country"] == "IT"]
df_us = spotify_data2[spotify_data2["country"] == "US"]

#italy stats
top_artist_italy = df_italy["artists"].value_counts().idxmax()
top_song_italy = df_italy["name"].value_counts().idxmax()

#us stats
top_artist_us = df_us["artists"].value_counts().idxmax()
top_song_us = df_us["name"].value_counts().idxmax()

#explicit songs in italy
df_italy["is_explicit"] = df_italy["is_explicit"].replace({True: " Yes", False: " No"})  
explicit_italy = df_italy.groupby("is_explicit").size().reset_index(name="count") 

italy_pie = px.pie(explicit_italy, 
                names="is_explicit", 
                values="count", 
                hole=0.3, 
                title="Explicit vs Non Explicit Songs in Italy: Do listeners prefer songs with or without profanity?",
                labels={"is_explicit": "Explicit?"}
                )
italy_pie.update_traces(marker=dict(colors=["red", "green"]))

#explicit songs in US
df_us["is_explicit"] = df_us["is_explicit"].replace({True: " Yes", False: " No"})  
explicit_us = df_us.groupby("is_explicit").size().reset_index(name="count")  

us_pie = px.pie(explicit_us, 
                   names="is_explicit", 
                   values="count", 
                   hole=0.3, 
                   title="Explicit vs Non Explicit Songs in US: Do listeners prefer songs with or without profanity?",
                   labels={"is_explicit": "Explicit?"}
                   )

us_pie.update_traces(marker=dict(colors=["red", "blue"]))


# speechiness songs data
it_speechiness = spotify_data[spotify_data["country"] == "IT"]["speechiness"].sum()
us_speechiness = spotify_data[spotify_data["country"] == "US"]["speechiness"].sum()

# merging us and it speechiness
df_speechiness_sum = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Speechiness": [it_speechiness, us_speechiness]
})

# plot speechiness on a bar chart
speechiness_bar = px.bar(df_speechiness_sum, x="Country", y="Total Speechiness",
                         title="Who prefers speechy songs?",
                         labels={"Total Speechiness": "Speechiness Score"},
                         color="Country")




# danceability songs data
it_danceability = spotify_data[spotify_data["country"] == "IT"]["danceability"].sum()
us_danceability = spotify_data[spotify_data["country"] == "US"]["danceability"].sum()

# merging us and it danceability
df_danceability_sum = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Danceability": [it_danceability, us_danceability]
})

# plot danceability on a bar chart
danceability = px.bar(df_danceability_sum, x="Country", y="Total Danceability",
                         title="Who prefers danceable songs?",
                         labels={"Total Danceability": "Danceability Score"},
                         color="Country")



# Compute total acousticness for IT and US
it_acousticness = spotify_data[spotify_data["country"] == "IT"]["acousticness"].sum()
us_acousticness = spotify_data[spotify_data["country"] == "US"]["acousticness"].sum()

# Merge into a DataFrame
df_acousticness_sum = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Acousticness": [it_acousticness, us_acousticness]
})

# Create a bar chart
acousticness_chart = px.bar(df_acousticness_sum, x="Country", y="Total Acousticness",
                            title="Which country has more acoustic songs?",
                            labels={"Total Acousticness": "Acousticness Score"},
                            color="Country")



# Compute total liveness for IT and US
it_liveness = spotify_data[spotify_data["country"] == "IT"]["liveness"].sum()
us_liveness = spotify_data[spotify_data["country"] == "US"]["liveness"].sum()

# Merge into a DataFrame
df_liveness_sum = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Liveness": [it_liveness, us_liveness]
})

# Create a bar chart
liveness_chart = px.bar(df_liveness_sum, x="Country", y="Total Liveness",
                        title="Which country has more live-feeling songs?",
                        labels={"Total Liveness": "Liveness Score"},
                        color="Country")

#dashboard

LOGO_URL_SMALL = "https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Full_Logo_RGB_Green.png"
st.logo(
    LOGO_URL_SMALL,
    link="https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Full_Logo_RGB_Green.png",
    icon_image=LOGO_URL_SMALL,
)
st.title("Spotify Streaming Analysis")
st.header("by Alexa and Giulio")
st.write("Thanks for stopping by our dashboard! This app uses Kaggle's \"Top Spotify Songs in 73 Countries (Daily Updated)\" dataset to analyze music trends in Italy (Giulio's patria) and the US (Alexa's home). Hope you enjoy!")
st.markdown("[Link to dataset](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated?resource=download)")

#creating ability to choose which country to look at
selection = st.selectbox("Country:", ("Both", "Italy", "US"))

#individual pages
if selection == "Both":
    #welcome
    rain_emojis("🇮🇹 🇺🇸")

    #artist stats
    st.write("#1 Trending Artist in 🇮🇹 Today")
    container = st.container(border=True)
    container.write(f"{top_artist_italy}")

    st.write("#1 Trending Artist in 🇺🇸 Today")
    container = st.container(border=True)
    container.write(f"{top_artist_us}")

    #song stats    
    st.write("#1 Trending Song in 🇮🇹 Today")
    container = st.container(border=True)
    container.write(f"{top_song_italy}")
    
    #us
    st.write("#1 Trending Song in 🇺🇸 Today")
    container = st.container(border=True)
    container.write(f"{top_song_us}")

    #explicit songs
    st.plotly_chart(italy_pie)
    st.plotly_chart(us_pie)

    #speechiness songs
    st.plotly_chart(speechiness_bar)

    #danceability songs
    st.plotly_chart(danceability)

    # acousticness songs
    st.plotly_chart(acousticness_chart)

    # liveness songs
    st.plotly_chart(liveness_chart)

elif selection == "Italy":
    #welcome
    rain_emojis("🇮🇹")

    #artist stats
    st.write("#1 Trending Artist 🎤 Today")
    container = st.container(border=True)
    container.write(f"{top_artist_italy}")

    #song stats
    st.write("#1 Trending Song 🎵 Today")
    container = st.container(border=True)
    container.write(f"{top_song_italy}")

    #explicit chart
    st.plotly_chart(italy_pie)

elif selection == "US":
    #welcome
    rain_emojis("🇺🇸")

    #artist stats
    st.write("#1 Trending Artist 🎤 Today")
    container = st.container(border=True)
    container.write(f"{top_artist_us}")

    #song stats
    st.write("#1 Trending Song 🎵 Today")
    container = st.container(border=True)
    container.write(f"{top_song_us}")

    #explicit chart
    st.plotly_chart(us_pie)
