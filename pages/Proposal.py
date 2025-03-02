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