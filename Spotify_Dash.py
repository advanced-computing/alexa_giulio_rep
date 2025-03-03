from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import streamlit as st
import altair as alt

#setting up api
def authenticate_kaggle_api():
    api = KaggleApi()
    api.authenticate()
    return api

#setting up and downloading path
def download_dataset(api, dataset_path):
    try:
        api.dataset_download_files(dataset_path, path='./', unzip=True, quiet=False)
    except Exception as e:
        raise RuntimeError(f"Error downloading dataset: {e}")

#making sure dataset can load properly by skipping bad rows
def get_problematic_rows(file_path):
    problematic_rows = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.count(',') < 10 or len(line.split(',')) > 50: #used chat gpt to figure this logic out
                problematic_rows.append(i)
    return problematic_rows

#loading dataset
def load_dataset(file_path, skip_rows):
    try:
        df = pd.read_csv(file_path, skiprows=skip_rows)
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {e}")

#calling on API
def call_api(dataset_path, file_name):
    api = authenticate_kaggle_api()
    download_dataset(api, dataset_path)
    
    file_path = f'./{file_name}'
    skip_rows = get_problematic_rows(file_path)
    
    df = load_dataset(file_path, skip_rows)
    return df

# dataset path and file name
dataset_path = 'asaniczka/top-spotify-songs-in-73-countries-daily-updated'
file_name = 'universal_top_spotify_songs.csv'

# calling api
spotify_data = call_api(dataset_path, file_name)

# separate artists into individual categories in case they're grouped together (re. collabs)
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data = spotify_data.explode("artists")

# Filter for US and Italy
df_US_IT = spotify_data[spotify_data["country"].isin(["US", "IT"])]
df_US_IT2 = df_US_IT[df_US_IT["snapshot_date"].isin(["2025-03-01"])]

country_artist_count = df_US_IT2.groupby(["country", "artists"]).size().reset_index(name="song_count")

##donut chart

# Create a donut chart with Plotly
#fig = px.pie(country_artist_count, 
            # names="artists", 
             #values="song_count", 
             #color="country", 
            # hole=0.3,  # To make it a donut chart
             #title="Spotify Song Popularity by Artist (US & Italy)",
             #labels={'artists': 'Artist', 'song_count': 'Number of Songs'})

# Display chart in Streamlit
#fig.show()

# Count the number of songs per country
country_counts = df_US_IT2['country'].value_counts()

# Calculate the percentage of songs from US and Italy
total_songs = country_counts.sum()
us_percentage = (country_counts.get('US', 0) / total_songs) * 100
it_percentage = (country_counts.get('IT', 0) / total_songs) * 100

# Function to create a donut chart
def make_donut(input_response, input_text, input_color):
    if input_color == 'blue':
        chart_color = ['#29b5e8', '#155F7A']
    elif input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    elif input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    elif input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']

    # Data for donut chart
    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100 - input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })

    # Create the donut chart
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color=alt.Color("Topic:N", scale=alt.Scale(domain=[input_text, ''], range=chart_color), legend=None),
    ).properties(width=130, height=130)

    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(
        text=alt.value(f'{input_response} %')
    )
    
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color=alt.Color("Topic:N", scale=alt.Scale(domain=[input_text, ''], range=chart_color), legend=None),
    ).properties(width=130, height=130)
    
    return plot_bg + plot + text

# Combine the US and Italy percentages into one donut
combined_percentage = [us_percentage, it_percentage]
labels = ['US', 'Italy']

# Create the donut chart
donut_chart = make_donut(combined_percentage[0], 'US', 'blue') + make_donut(combined_percentage[1], 'Italy', 'green')

# Display the donut chart in Streamlit
st.write('### Proportion of Songs from US vs Italy')
st.altair_chart(donut_chart)
