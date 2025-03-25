import streamlit as st
import pandas_gbq

# get GCP credentials from secrets
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

# use credentials to query
PROJECT_ID = st.secrets["gcp_service_account"]["project_id"]
DATASET = "spotify"
TABLE = "universal_top_spotify_songs"
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET}.{TABLE}"

query = f"SELECT * FROM `{FULL_TABLE_ID}` LIMIT 10"
df = pandas_gbq.read_gbq(query, project_id=PROJECT_ID, credentials=credentials)

st.write(df)
