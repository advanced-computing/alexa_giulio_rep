import os
import streamlit as st
import plotly.express as px
from kaggle.api.kaggle_api_extended import KaggleApi
from helper_functions_notebook import call_api, rain_emojis

#kaggle api key
os.environ["KAGGLE_USERNAME"] = st.secrets["KAGGLE_USERNAME"]
os.environ["KAGGLE_KEY"] = st.secrets["KAGGLE_KEY"]
api = KaggleApi()
api.authenticate()

#loading dataset
dataset_path = 'asaniczka/top-spotify-songs-in-73-countries-daily-updated'
file_name = 'universal_top_spotify_songs.csv'
spotify_data = call_api(dataset_path, file_name)

#name column cleaning
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data = spotify_data.explode("artists")

#filtering italy and US
df_italy = spotify_data[spotify_data["country"] == "IT"]
df_us = spotify_data[spotify_data["country"] == "US"]

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
                title="Explicit vs Non Explicit Songs in Italy",
                subtitle="Do listeners prefer songs with or without profanity?",
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
                   title="Explicit vs Non Explicit Songs in US",
                   subtitle="Do listeners prefer songs with or without profanity?",
                   labels={"is_explicit": "Explicit?"}
                   )

us_pie.update_traces(marker=dict(colors=["red", "blue"]))

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
    container.write(f"{top_artist_italy} 🎤")

    st.write("#1 Trending Artist in 🇺🇸 Today")
    container = st.container(border=True)
    container.write(f"{top_artist_us} 🎤")

    #song stats    
    st.write("#1 Trending Song in 🇮🇹 Today")
    container = st.container(border=True)
    container.write(f"{top_song_italy} 🎵")
    
    #us
    st.write("#1 Trending Song in 🇺🇸 Today")
    container = st.container(border=True)
    container.write(f"{top_song_us} 🎵")

    #explicit songs
    st.plotly_chart(italy_pie)
    st.plotly_chart(us_pie)

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
