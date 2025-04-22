from google.oauth2 import service_account
from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import storage, bigquery
import pandas as pd
import pandas_gbq
import os
import zipfile
import json

SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive',
]

bucket_name = "run-sources-sipa-adv-c-alexa-giulio-us-central1"
kaggle_dataset = "asaniczka/top-spotify-songs-in-73-countries-daily-updated"
local_zip = "top-spotify-songs-in-73-countries-daily-updated.zip"
local_csv = "universal_top_spotify_songs.csv"
compressed_csv = "latest_snapshot.csv.gz"
dataset_id = "spotify"
table_id = "universal_top_spotify_songs"

def get_bq_credentials():
    bq_credentials_env = os.environ.get("GCP_SERVICE_ACCOUNT")
    if bq_credentials_env:
        bq_credentials = json.loads(bq_credentials_env)
    else:
        with open("gcp_service_account.json") as f:
            bq_credentials = json.load(f)

    return service_account.Credentials.from_service_account_info(
        bq_credentials,
        scopes=SCOPES
    )

def get_kaggle_api():
    api = KaggleApi()
    api.authenticate()  # this only runs when the function is called
    return api

def update_bigquery_from_kaggle():
    try:
        credentials = get_bq_credentials()
        project_id = credentials.project_id
        table_ref = f"{project_id}.{dataset_id}.{table_id}"

        api = get_kaggle_api()
        api.dataset_download_files(kaggle_dataset, path=".", unzip=False)

        with zipfile.ZipFile(local_zip, 'r') as zip_ref:
            zip_ref.extractall(".")

        df = pd.read_csv(local_csv, parse_dates=['snapshot_date'])
        latest_snapshot = df['snapshot_date'].max()

        df_latest = df[
            (df['snapshot_date'] == latest_snapshot) &
            (df['country'].isin(['US', 'FR', 'IT', 'ES', 'MX']))
        ]
        df_latest.to_csv(compressed_csv, index=False, compression='gzip')

        storage_client = storage.Client(credentials=credentials, project=project_id)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(compressed_csv)
        blob.upload_from_filename(compressed_csv)

        bq_client = bigquery.Client(credentials=credentials, project=project_id)
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            compression_type=bigquery.Compression.GZIP,
        )

        uri = f"gs://{bucket_name}/{compressed_csv}"
        load_job = bq_client.load_table_from_uri(uri, table_ref, job_config=job_config)
        load_job.result()

        os.remove(local_csv)
        os.remove(compressed_csv)

        return str(latest_snapshot)

    except Exception as e:
        print(f"ETL failed: {e}")
        return None
