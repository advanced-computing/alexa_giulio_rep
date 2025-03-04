import os
import pandas as pd
import matplotlib.pyplot as plt
from kaggle.api.kaggle_api_extended import KaggleApi
from streamlit_extras.let_it_rain import rain

#kaggle api key
os.environ["KAGGLE_USERNAME"] = "alexashuetkaychan" 
os.environ["KAGGLE_KEY"] = "84bfb4133ffe7bbd8e0f0d1d4d14b20f" 
api = KaggleApi()
api.authenticate()

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
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.count(',') < 10 or len(line.split(',')) > 50: #used chat gpt to figure this logic out
                problematic_rows.append(i)
    return problematic_rows

# %%
#loading dataset
def load_dataset(file_path, skip_rows):
    try:
        df = pd.read_csv(file_path, skiprows=skip_rows)
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading dataset: {e}")

# %%
#calling on API
def call_api(dataset_path, file_name):
    api = authenticate_kaggle_api()
    download_dataset(api, dataset_path)
    
    file_path = f'./{file_name}'
    skip_rows = get_problematic_rows(file_path)
    
    df = load_dataset(file_path, skip_rows)
    return df

# %%
#dash elements: emoji rain 

def rain_emojis(emoji):
        rain(
            emoji=emoji,
            font_size=54,
            falling_speed=10,
            animation_length=5,
        )

