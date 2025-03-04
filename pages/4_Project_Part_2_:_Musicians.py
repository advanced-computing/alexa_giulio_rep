import pandas as pd
import streamlit as st

#loading shortened version of dataset
spotify_data = pd.read_csv("spotify_data_top_us.csv")

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
