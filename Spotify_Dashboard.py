import streamlit as st
import pandas_gbq
from google.oauth2 import service_account
import plotly.express as px
import pandas as pd
import warnings
from helper_functions_notebook import rain_emojis  # keep this for visuals

# biquery
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

# loading
spotify_data = pandas_gbq.read_gbq(query, project_id=project_id, credentials=credentials)

# cleaning
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