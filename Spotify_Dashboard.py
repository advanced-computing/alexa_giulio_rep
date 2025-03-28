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

# loading
spotify_data = pandas_gbq.read_gbq(query, project_id=project_id, credentials=credentials)


# Sample data
locations = {
    'Italy': [37.7749, -122.4194, 'Page 1'],
    'New York': [40.7128, -74.0060, 'Page 2'],
    'Los Angeles': [34.0522, -118.2437, 'Page 3'],
}

# Initialize the map
m = folium.Map(location=[39, -98], zoom_start=3)

# Add markers with click functionality
marker_cluster = MarkerCluster().add_to(m)
for city, (lat, lon, page) in locations.items():
    folium.Marker(
        location=[lat, lon],
        popup=city,
        tooltip=city,
        icon=folium.Icon(color='blue')
    ).add_to(marker_cluster)

# Display the map
st_folium(m, width=700, height=500)

# Handle simulated navigation
selected_city = st.selectbox("Select a city to navigate:", list(locations.keys()))
selected_page = locations[selected_city][2]

if selected_page == 'Page 1':
    st.write("You are on Page 1!")
    # Add content for Page 1
elif selected_page == 'Page 2':
    st.write("You are on Page 2!")
    # Add content for Page 2
elif selected_page == 'Page 3':
    st.write("You are on Page 3!")
    # Add content for Page 3