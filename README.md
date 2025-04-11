**Project Title: "Global Trends in Music Popularity"**

We will use Kaggle's "Top Spotify Songs in 73 Countries (Daily Updated)" dataset. This dataset is updated daily to include the top songs and artists streamed across the world. We are interested in answering some of the following questions:

- Which songs and artists are most popular in which countries?
- Which country listens to the most danceable and acoustic music? How does this compare between countries?
- Do countries prefer explicit music or non explicit music?

**Lab 11**

**Setup/Usage instructions**
Please use Python 3.12.2 or older

Follow these steps: 
1. Clone the repository 
2. Create and activate the virtual environment (depending on your computer and Windows version you can use a variation of: (1) python -m venv .venv for creation and (2) .venv\Scripts\activate for activation)
3. Install the requirements (pip install -r requirements.txt). Please exercise patience. It takes a really long time :(
4. Run the main dashboard page (streamlit run Spotify_Dashboard.py) with Streamlit.

Deployed App link: https://advanced-computing-alexa-giulio-rep-spotify-dashboard-zvzfpp.streamlit.app/

**Takeaways**
What are participants getting confused by / stuck on?
- The first step that participants were getting stuck on was Step 2. This issue was mainly due to the fact that each computer/system had a different command for creating and activating the virtual environment, so it took some time to figure out which variation of the python -m venv .venv and .venv\Scripts\activate commmand worked for certain users. We also realized that Step 3 took a really long time to finish. Participants' computers were stuck on the dependecy loading stage for at least 5 minutes. However, the code eventually finished -- it just took a long time to process.
  
What steps did they need to take that aren't documented (well)? What can be clearer?
- One step that participants needed to take that wasn't documented well was ensuring that Python 3.12.2 or older was installed. It wasn't clear that our app relied on a certain version of Python to load due to its requirements. We believe that this may have affected the loading time of dependencies, so we made sure to specify that users should use this or older versions of Python when using our app.

