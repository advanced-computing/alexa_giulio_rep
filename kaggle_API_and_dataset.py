# $pip install kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

#setting up kaggle API 
api = KaggleApi()
api.authenticate()

#setting up and downloading path
dataset_path = 'asaniczka/top-spotify-songs-in-73-countries-daily-updated'
api.dataset_download_files(dataset_path, path='./', unzip=True)

#loading into pandas
file_path = './universal_top_spotify_songs.csv'  
df = pd.read_csv(file_path, skiprows=[1306857])
print(df.head())

#lets hope this works