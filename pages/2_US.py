#US

# loading
spotify_data = pandas_gbq.read_gbq(query, project_id=project_id, credentials=credentials)

# cleaning
spotify_data["artists"] = spotify_data["artists"].str.split(", ")
spotify_data2 = spotify_data.explode("artists")

df_us = spotify_data2[spotify_data2["country"] == "US"]

top_artist_us = df_us["artists"].value_counts().idxmax()
top_song_us = df_us["name"].value_counts().idxmax()

#pie charts
df_us["is_explicit"] = df_us["is_explicit"].astype("object").replace({True: " Yes", False: " No"})  
explicit_us = df_us.groupby("is_explicit").size().reset_index(name="count")  

us_pie = px.pie(explicit_us, 
                names="is_explicit", 
                values="count", 
                hole=0.3, 
                title="Explicit vs Non Explicit Songs in US",
                labels={"is_explicit": "Explicit?"})
us_pie.update_traces(marker=dict(colors=["red", "blue"]))

#speechiness
us_speechiness = spotify_data[spotify_data["country"] == "US"]["speechiness"].sum()

#danceability
us_danceability = spotify_data[spotify_data["country"] == "US"]["danceability"].sum()
