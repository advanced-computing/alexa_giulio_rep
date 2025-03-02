import streamlit as st
import helper_functions
#from kaggle.api.kaggle_api_extended import KaggleApi

#loading dataset
dataset_path = 'asaniczka/top-spotify-songs-in-73-countries-daily-updated'
file_name = 'universal_top_spotify_songs.csv'
spotify_data = helper_functions.call_api(dataset_path, file_name)

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
st.title("Popular 10 Spotify Artists")
st.bar_chart(popular_artists) 

#$streamlit run project_pt4.py  