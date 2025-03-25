import pandas as pd
import pandas_gbq
import pydata_google_auth
from helper_functions_notebook import call_api

# configuration
project_id = "sipa-adv-c-alexa-giulio"
dataset = "spotify"
table = "universal_top_spotify_songs"
full_table_id = f"{project_id}.{dataset}.{table}"
scopes = ["https://www.googleapis.com/auth/cloud-platform"]

# load data from api
print("downloading dataset from kaggle...")
df = call_api("asaniczka/top-spotify-songs-in-73-countries-daily-updated", "universal_top_spotify_songs.csv")
print("dataset loaded successfully.")

# authenticate with google cloud
print("authenticating with google cloud...")
credentials = pydata_google_auth.get_user_credentials(scopes)

# incremental load logic
try:
    print("checking for existing records in bigquery...")
    existing = pandas_gbq.read_gbq(
        f"SELECT DISTINCT name FROM `{full_table_id}`",
        project_id=project_id,
        credentials=credentials
    )

    existing_names = set(existing['name'].str.lower())
    df["name_lower"] = df["name"].str.lower()
    new_data = df[~df["name_lower"].isin(existing_names)].drop(columns=["name_lower"])

except Exception as e:
    print(f"could not query existing data: {e}")
    print("uploading entire dataset.")
    new_data = df

# upload to bigquery
if not new_data.empty:
    print(f"uploading {len(new_data)} new records to bigquery...")
    pandas_gbq.to_gbq(
        new_data,
        full_table_id,
        project_id=project_id,
        credentials=credentials,
        if_exists="append"
    )
    print("upload complete.")
else:
    print("no new records to upload.")
