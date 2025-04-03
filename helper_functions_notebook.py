import pandas as pd
import random
import plotly_express as px
import matplotlib.pyplot as plt
from kaggle.api.kaggle_api_extended import KaggleApi
from Spotify_Dashboard import spotify_data2

# %%
#data prep function
def load_and_prepare_data(file_path, num_countries):
    # Load data and select relevant columns
    df = pd.read_csv(file_path, usecols=["Country Name", "2023"])

    # Sort and select most populated countries
    df = df.sort_values(by="2023", ascending=False).head(num_countries)

    return df

# %%
#bar chart function
def create_population_chart(df):
    # Create bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df["Country Name"], df["2023"], color="skyblue")
    ax.set_xlabel("Country Name", fontsize=12)
    ax.set_ylabel("Population in 2023", fontsize=12)
    ax.set_title("Population by Country in 2023", fontsize=14)
    ax.set_xticklabels(df["Country Name"], rotation=90)

    return fig

# %%
#separates out multiple artists that are credited on a single song
def name_cleaning(df: pd.DataFrame, column_name: str):
    df[column_name] = df[column_name].str.split(", ")
    return name_separating(df, column_name)

# %%
#puts the individual artists into their own rows as a list
def name_separating(df: pd.DataFrame, column_name: str):
    df = df.explode(column_name)
    return df

# %%
#setting up api
def authenticate_kaggle_api():
    api = KaggleApi()
    api.authenticate()
    return api

# %%
#setting up and downloading path
def download_dataset(api, dataset_path):
    try:
        api.dataset_download_files(dataset_path, path='./', unzip=True, quiet=False)
    except Exception as e:
        raise RuntimeError(f"Error downloading dataset: {e}")

# %%
#making sure dataset can load properly by skipping bad rows
def get_problematic_rows(file_path):
    problematic_rows = []
    with open(file_path, 'r', encoding="iso-8859-1", errors="replace") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.count(',') < 10 or len(line.split(',')) > 50: #used chat gpt to figure this logic out
                problematic_rows.append(i)
    return problematic_rows

# %%
#loading dataset
def load_dataset(file_path, skip_rows, sample_size=1000):
    try:
        total_rows = sum(1 for _ in open(file_path, 'r', encoding="iso-8859-1")) - 1  
        
        available_rows = list(set(range(1, total_rows + 1)) - set(skip_rows)) 
        sampled_rows = sorted(random.sample(available_rows, min(sample_size, len(available_rows))))
        
        df = pd.read_csv(file_path, skiprows=lambda x: x not in sampled_rows and x != 0) 
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {e}")

# %%
#calling on API
def call_api(dataset_path, file_name, sample_size=1000):
    api = authenticate_kaggle_api()
    download_dataset(api, dataset_path)
    
    file_path = f'./{file_name}'
    skip_rows = get_problematic_rows(file_path)
    
    df = load_dataset(file_path, skip_rows)
    return df

# %%


  #analysis for other graphs
#country vs country

# Define the countries and their labels
countries = {
    "IT": "Italy (IT)",
    "US": "United States (US)",
    "MX": "Mexico (MX)",
    "FR": "France (FR)",
    "ES": "Spain (ES)"
}

# Calculate total danceability per country
danceability_scores = {
    code: spotify_data2[spotify_data2["country"] == code]["danceability"].sum()
    for code in countries
}

# Function to generate bar chart between two countries
def compare_danceability(base="IT", other="US"):
    df = pd.DataFrame({
        "Country": [countries[base], countries[other]],
        "Total Danceability": [danceability_scores[base], danceability_scores[other]]
    })
    return px.bar(
        df,
        x="Country",
        y="Total Danceability",
        title="Who prefers danceable songs?",
        labels={"Total Danceability": "Danceability Score"},
        color="Country"
    )

# Generate plots
danceability_it_us = compare_danceability("IT", "US")
danceability_it_mex = compare_danceability("IT", "MX")
danceability_it_fr = compare_danceability("IT", "FR")
danceability_it_es = compare_danceability("IT", "ES")

danceability_us_it = compare_danceability("US", "IT")
danceability_us_mex = compare_danceability("US", "MX")
danceability_us_fr = compare_danceability("US", "FR")
danceability_us_es = compare_danceability("US", "ES")

danceability_mex_us = compare_danceability("MX", "US")
danceability_mex_it = compare_danceability("MX", "IT")
danceability_mex_fr = compare_danceability("MX", "FR")
danceability_mex_es = compare_danceability("MX", "ES")

danceability_fr_us = compare_danceability("FR", "US")
danceability_fr_it = compare_danceability("FR", "IT")
danceability_fr_mex = compare_danceability("FR", "MX")
danceability_fr_es = compare_danceability("FR", "ES")

danceability_es_us = compare_danceability("ES", "US")
danceability_es_it = compare_danceability("ES", "IT")
danceability_es_mex = compare_danceability("ES", "MX")
danceability_es_fr = compare_danceability("ES", "FR")

# Calculate total acousticness per country
acousticness_scores = {
    code: spotify_data2[spotify_data2["country"] == code]["acousticness"].sum()
    for code in countries
}

# Function to compare acousticness between two countries
def compare_acousticness(base="IT", other="US"):
    df = pd.DataFrame({
        "Country": [countries[base], countries[other]],
        "Total Acousticness": [acousticness_scores[base], acousticness_scores[other]]
    })
    return px.bar(
        df,
        x="Country",
        y="Total Acousticness",
        title="Which country prefers acoustic songs?",
        labels={"Total Acousticness": "Acousticness Score"},
        color="Country"
    )

# Generate plots
acousticness_it_us = compare_acousticness("IT", "US")
acousticness_it_mex = compare_acousticness("IT", "MX")
acousticness_it_fr = compare_acousticness("IT", "FR")
acousticness_it_es = compare_acousticness("IT", "ES")

acousticness_us_it = compare_acousticness("US", "IT")
acousticness_us_mex = compare_acousticness("US", "MX")
acousticness_us_fr = compare_acousticness("US", "FR")
acousticness_us_es = compare_acousticness("US", "ES")

acousticness_mex_us = compare_acousticness("MX", "US")
acousticness_mex_it = compare_acousticness("MX", "IT")
acousticness_mex_fr = compare_acousticness("MX", "FR")
acousticness_mex_es = compare_acousticness("MX", "ES")

acousticness_fr_us = compare_acousticness("FR", "US")
acousticness_fr_it = compare_acousticness("FR", "IT")
acousticness_fr_mex = compare_acousticness("FR", "MX")
acousticness_fr_es = compare_acousticness("FR", "ES")

acousticness_es_us = compare_acousticness("ES", "US")
acousticness_es_it = compare_acousticness("ES", "IT")
acousticness_es_mex = compare_acousticness("ES", "MX")
acousticness_es_fr = compare_acousticness("ES", "FR")
