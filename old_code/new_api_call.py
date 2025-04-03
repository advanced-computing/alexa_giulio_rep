import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

#setting up api
def authenticate_kaggle_api():
    api = KaggleApi()
    api.authenticate()
    return api

#setting up and downloading path
def download_dataset(api, dataset_path):
    api.dataset_download_files(dataset_path, path='./', unzip=True)

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
    return pd.read_csv(file_path, skiprows=skip_rows, on_bad_lines='skip')

#calling on API
def call_api(dataset_path, file_name):
    api = authenticate_kaggle_api()
    download_dataset(api, dataset_path)
    
    file_path = f'./{file_name}'
    skip_rows = get_problematic_rows(file_path)
    
    df = load_dataset(file_path, skip_rows)
    return df

#loading
dataset_path = 'asaniczka/top-spotify-songs-in-73-countries-daily-updated'
file_name = 'universal_top_spotify_songs.csv'

df = call_api(dataset_path, file_name)
print(df.head())