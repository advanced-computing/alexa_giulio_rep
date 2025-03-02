import streamlit as st
import pandas as pd
import plotly.express as px


# Page Title
st.title("Spotify Streaming Analysis")

# Dataset Section
st.header("What dataset are you going to use?")
st.write("We will use Kaggle's \"Top Spotify Songs in 73 Countries (Daily Updated)\" dataset. This dataset is updated daily to include the top songs and artists streamed across the world.")
st.markdown("[Link to dataset](https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated?resource=download)")

# Research Questions
st.header("What are your research question(s)?")
st.write("We are interested in answering the following questions:")
st.markdown("""
- Which genres of music and artists are most popular in which countries over time?
- What is the relationship between song features (speechiness, explicitness, etc) and their popularity?
- Do countries tend to listen to domestic music (i.e. music produced in the user's country or sung in the home language) more than foreign music?
- Which songs/artists are most popular and when do they start to lose popularity?
            
We integrated Roberto's feedback and eliminated "which country listens to the most music". We also slightly modified the wording when it comes to song features.
""")

# Notebook Link
st.header("What's the link to your notebook?")
st.markdown("[Link to our notebook](https://colab.research.google.com/drive/1H0l4hN8gyangmzVwuEojwT8GAi1kykyc?usp=sharing)")

# Target Visualization
st.header("What's your target visualization?")
st.write("Depending on which research question we choose, we have several ideas for how to graph this data (such as a choropleth map of artist popularity across the world or a word cluster chart that shows the name of the most popular artists globally).")
st.write("If we choose to do a line graph of song/artist popularity over time (where each line represents one song or artist), then our target visualization could look like this:")

# Known Unknowns
st.header("What are your known unknowns?")
st.markdown("""
- The dataset specifies that it pulls data from 73 countries -- are these countries biased towards certain continents?
- Are there inconsistencies with how the song/artist titles are written (meaning all upper case/lower case, special characters, etc.) that may make it difficult to properly aggregate the frequency for individual songs?
""")

# Anticipated Challenges
st.header("What challenges do you anticipate?")
st.markdown("""
- If we choose to do a geographic representation of our data, then linking country codes could present a challenge
- Making sure that the data is written uniformly may be time-consuming
- Normalizing the rankings of each song/artist between differently sized countries to better understand a song's popularity
""")







st.markdown("<br><br>", unsafe_allow_html=True)






# loading data as a csv instead of api for simplicity 
spotify_data = pd.read_csv("spotify_data_top_us.csv")

# separate artists into individual categories in case they're grouped together (re. collabs)
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data = spotify_data.explode("artists")

# group artists by average popularity
artist_popularity = spotify_data.groupby("artists")["popularity"].mean()

# create widget to choose how many artists you can see
display_widget = st.slider("Number of Artists to Display", min_value=1, max_value=40, value=20, step=1)

# apply widget to artist_popularity subset
artist_popularity = artist_popularity.head(display_widget)

# make bar chart
st.title("Top 40 Spotify Artists by Alexa and Giulio")
st.bar_chart(artist_popularity)







st.markdown("<br><br>", unsafe_allow_html=True)






# Filter for US and Italy
df_US_IT = spotify_data[spotify_data["country"].isin(["US", "IT"])]

# Select top 10 songs for each country based on daily rank
df_top_10 = df_US_IT.groupby("country").apply(lambda x: x.nsmallest(10, "daily_rank")).reset_index(drop=True)

# Create bar chart
fig = px.bar(df_top_10, 
             x="song", 
             y="daily_rank", 
             color="country", 
             barmode="group",
             title="Top 10 Songs in the US vs Italy",
             labels={"daily_rank": "Daily Rank", "song": "Song"},
             height=500)

# Invert the rank axis (1st is best)
fig.update_yaxes(autorange="reversed")

# Show in Streamlit
import streamlit as st
st.title("Top 10 Songs in the US vs Italy")
st.plotly_chart(fig)













# $streamlit run spotify.py 