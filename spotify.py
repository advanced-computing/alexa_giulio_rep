import streamlit as st
import pandas as pd
import plotly.express as px

# loading data as a csv instead of api for simplicity
spotify_data = pd.read_csv("spotify_data_top_us.csv")

# separate artists into individual categories in case they're grouped together (re. collabs)
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data = spotify_data.explode("artists")

# group artists by average popularity
artist_popularity = spotify_data.groupby("artists")["popularity"].mean()

# create widget to choose how many artists you can see
display_widget = st.slider("Number of Artists to Display", min_value=1, max_value=40, value=20, step=1)

# apply widget to artist_popularity subset
artist_popularity = artist_popularity.head(display_widget)

# make bar chart
st.title("Top 40 Spotify Artists by Alexa and Giulio")
st.bar_chart(artist_popularity)



# $streamlit run spotify.py 