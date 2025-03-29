import streamlit as st
import plotly.express as px
import pandas as pd
from Spotify_Dashboard import spotify_data
from helper_functions_notebook import rain_emojis 

st.page("pages/1_Italy.py")

# cleaning
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data2 = spotify_data.explode("artists")

df_italy = spotify_data2[spotify_data2["country"] == "IT"]

top_artist_italy = df_italy["artists"].value_counts().idxmax()
top_song_italy = df_italy["name"].value_counts().idxmax()

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

# speechiness songs data
it_speechiness = spotify_data[spotify_data["country"] == "IT"]["speechiness"].sum()

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