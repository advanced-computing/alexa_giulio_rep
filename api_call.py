import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def download_and_load_kaggle_data(dataset_path, file_name, max_retries=3):
#setting up kaggle API 
    api = KaggleApi()
    api.authenticate()

#setting up and downloading path
    api.dataset_download_files(dataset_path, path='./', unzip=True)
    file_path = f'./{file_name}'
    
#detect badrows
    def get_problematic_rows(file_path):
        problematic_rows = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.count(',') < 10 or len(line.split(',')) > 50:
                    problematic_rows.append(i)
        return problematic_rows

#skip bad rows
    retries = 0
    while retries < max_retries:
        try:
            skip_rows = get_problematic_rows(file_path)
            df = pd.read_csv(file_path, skiprows=skip_rows, on_bad_lines='skip')  # 'skip' skips problematic lines
            print(f"File read successfully. Skipped rows: {skip_rows}")
            return df
        except Exception as e:
            print(f"Error while reading the file: {e}. Retrying...")
            retries += 1

    print(f"Failed to read file after {max_retries} attempts.")
    return None


dataset_path = 'asaniczka/top-spotify-songs-in-73-countries-daily-updated'
file_name = 'universal_top_spotify_songs.csv'

# Load the dataset
df = download_and_load_kaggle_data(dataset_path, file_name)

if df is not None:
    print(df.head()) 



