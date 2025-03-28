import streamlit as st
import pandas_gbq
from google.oauth2 import service_account
import plotly.express as px
import pandas as pd
#import warnings
#from helper_functions_notebook import rain_emojis  
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

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

# bigquery
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
project_id = st.secrets["gcp_service_account"]["project_id"]
dataset = "spotify"
table = "universal_top_spotify_songs"
query = f"""
    SELECT DISTINCT artists, country, name, is_explicit, speechiness, danceability, acousticness, liveness
    FROM `{project_id}.{dataset}.{table}` 
    WHERE country IN ('IT','US','FR','ES','GB')
"""  
locations = {
    "Italy": [41.8719, 12.5674, "Page 1"],  
    "US": [38.79468, -74.0060, "Page 2"],  
    "Great Britain": [51.5074, -0.1278, "Page 3"], 
    "France": [46.6034, 1.8883, "Page 4"],  
    "Spain": [40.4637, -3.7492, "Page 5"] 
}

# Initialize the map
m = folium.Map(location=[46.1101, -37.0669], zoom_start=2.5)

# Add markers to the map with country name as popup
marker_cluster = MarkerCluster().add_to(m)
for country, (lat, lon, page) in locations.items():
    folium.Marker(
        location=[lat, lon],
        popup=country,
        tooltip=country,
        icon=folium.Icon(color='blue')
    ).add_to(marker_cluster)

# Display the map in Streamlit
st_folium(m, width=700, height=500)

# Add a selectbox to allow users to choose a country
selected_country = st.selectbox("Select a country to navigate:", list(locations.keys()))
selected_page = locations[selected_country][2]

# Function to display content based on the selected page
def navigate_to_page(page):
    if page == 'Page 1':
        st.write("You are on Page 1!")
        # Add content specific to Page 1
    elif page == 'Page 2':
        st.write("You are on Page 2!")
        # Add content specific to Page 2
    elif page == 'Page 3':
        st.write("You are on Page 3!")
        # Add content specific to Page 3
    elif page == 'Page 4':
        st.write("You are on Page 4!")
        # Add content specific to Page 4
    elif page == 'Page 5':
        st.write("You are on Page 5!")
        # Add content specific to Page 5

# Navigate to the page based on the selected country
navigate_to_page(selected_page)

#streamlit run Spotify_Dashboard.py 