**Project Title: "Global Trends in Music Popularity"**

We will use Kaggle's "Top Spotify Songs in 73 Countries (Daily Updated)" dataset. This dataset is updated daily to include the top songs and artists streamed across the world. We are interested in answering some of the following questions:

- Which songs and artists are most popular in which countries?
- Which country listens to the most danceable and acoustic music? How does this compare between countries?
- Do countries prefer explicit music or non explicit music?

**Setup/usage instructions**
Please use Python 3.12.2 or older

Follow these steps: 
1. clone the repository, 
2. create and activate the virtual environment (depending on your computer and Windows version you can use a variation of: (1) python -m venv .venv for creation and (2) .venv\Scripts\activate for activation)
3. install the requirements (pip install -r requirements.txt), 
4. copy your BigQuery key into the secrets file and save it (remember not to commit the secrets file), 
5. run the main dashboard page (streamlit run Spotify_Dashboard.py) with Streamlit.
