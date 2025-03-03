import helper_functions_notebook 
import streamlit as st
import plotly.express as px

#loading dataset
dataset_path = 'asaniczka/top-spotify-songs-in-73-countries-daily-updated'
file_name = 'universal_top_spotify_songs.csv'
spotify_data = helper_functions_notebook.call_api(dataset_path, file_name)

#filtering italy and US
df_italy = spotify_data[spotify_data["country"] == "IT"]
df_us = spotify_data[spotify_data["country"] == "US"]

#explicit songs in italy
df_italy["is_explicit"] = df_italy["is_explicit"].replace({True: " Yes", False: " No"})  
explicit_italy = df_italy.groupby("is_explicit").size().reset_index(name="count")  

italy_pie = px.pie(explicit_italy, 
                   names="is_explicit", 
                   values="count", 
                   hole=0.3, 
                   title="Explicit vs Non Explicit Songs in Italy",
                   labels={"is_explicit": "Explicit?"}
                   )

st.plotly_chart(italy_pie)

#explicit songs in US
df_us["is_explicit"] = df_us["is_explicit"].replace({True: " Yes", False: " No"})  
explicit_us = df_us.groupby("is_explicit").size().reset_index(name="count")  

us_pie = px.pie(explicit_us, 
                   names="is_explicit", 
                   values="count", 
                   hole=0.3, 
                   title="Explicit vs Non Explicit Songs in US",
                   labels={"is_explicit": "Explicit?"}
                   )
st.plotly_chart(us_pie)

#$streamlit run linechart_practice.py