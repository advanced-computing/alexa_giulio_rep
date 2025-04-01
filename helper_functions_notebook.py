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

#danceability
it_danceability = spotify_data2[spotify_data2["country"] == "IT"]["danceability"].sum()
us_danceability = spotify_data2[spotify_data2["country"] == "US"]["danceability"].sum()
mex_danceability = spotify_data2[spotify_data2["country"] == "MX"]["danceability"].sum()
fr_danceability = spotify_data2[spotify_data2["country"] == "FR"]["danceability"].sum()
es_danceability = spotify_data2[spotify_data2["country"] == "ES"]["danceability"].sum()

# italy us danceability
df_danceability_it_us = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Danceability": [it_danceability, us_danceability]
})
danceability_it_us = px.bar(df_danceability_it_us, x="Country", y="Total Danceability",
                         title="Who prefers danceable songs?",
                         labels={"Total Danceability": "Danceability Score"},
                         color="Country")
# italy mex danceability
df_danceability_it_mex = pd.DataFrame({
    "Country": ["Italy (IT)", "Mexico (MX)"],
    "Total Danceability": [it_danceability, mex_danceability]
})
danceability_it_mex = px.bar(df_danceability_it_mex, x="Country", y="Total Danceability",
                         title="Who prefers danceable songs?",
                         labels={"Total Danceability": "Danceability Score"},
                         color="Country")
# italy france danceability
df_danceability_it_fr = pd.DataFrame({
    "Country": ["Italy (IT)", "France (FR)"],
    "Total Danceability": [it_danceability, fr_danceability]
})
danceability_it_fr = px.bar(df_danceability_it_fr, x="Country", y="Total Danceability",
                         title="Who prefers danceable songs?",
                         labels={"Total Danceability": "Danceability Score"},
                         color="Country")

# italy spain danceability
df_danceability_it_es = pd.DataFrame({
    "Country": ["Italy (IT)", "Spain (ES)"],
    "Total Danceability": [it_danceability, es_danceability]
})
danceability_it_es = px.bar(df_danceability_it_es, x="Country", y="Total Danceability",
                         title="Who prefers danceable songs?",
                         labels={"Total Danceability": "Danceability Score"},
                         color="Country")

#acoustic
it_acousticness = spotify_data2[spotify_data2["country"] == "IT"]["acousticness"].sum()
us_acousticness = spotify_data2[spotify_data2["country"] == "US"]["acousticness"].sum()
mex_acousticness = spotify_data2[spotify_data2["country"] == "MX"]["acousticness"].sum()
fr_acousticness = spotify_data2[spotify_data2["country"] == "FR"]["acousticness"].sum()
es_acousticness = spotify_data2[spotify_data2["country"] == "ES"]["acousticness"].sum()

#italy us acousticness
df_acousticness_it_us = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Acousticness": [it_acousticness, us_acousticness]
})
acousticness_it_us = px.bar(df_acousticness_it_us, x="Country", y="Total Acousticness",
                            title="Which country prefers acoustic songs?",
                            labels={"Total Acousticness": "Acousticness Score"},
                            color="Country")

#italy mex acousticness
df_acousticness_it_mex = pd.DataFrame({
    "Country": ["Italy (IT)", "United States (US)"],
    "Total Acousticness": [it_acousticness, mex_acousticness]
})
acousticness_it_mex = px.bar(df_acousticness_it_mex, x="Country", y="Total Acousticness",
                            title="Which country prefers acoustic songs?",
                            labels={"Total Acousticness": "Acousticness Score"},
                            color="Country")

#italy france acousticness
df_acousticness_it_fr = pd.DataFrame({
    "Country": ["Italy (IT)", "France (FR)"],
    "Total Acousticness": [it_acousticness, fr_acousticness]
})
acousticness_it_fr = px.bar(df_acousticness_it_fr, x="Country", y="Total Acousticness",
                            title="Which country prefers acoustic songs?",
                            labels={"Total Acousticness": "Acousticness Score"},
                            color="Country")
#italy spain acousticness
df_acousticness_it_es = pd.DataFrame({
    "Country": ["Italy (IT)", "Spain (Es))"],
    "Total Acousticness": [it_acousticness, es_acousticness]
})
acousticness_it_es = px.bar(df_acousticness_it_es, x="Country", y="Total Acousticness",
                            title="Which country prefers acoustic songs?",
                            labels={"Total Acousticness": "Acousticness Score"},
                            color="Country")
