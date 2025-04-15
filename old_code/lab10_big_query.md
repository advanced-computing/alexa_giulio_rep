Question: What type of data loading will you use? Why? Explain as Markdown in your repository.

Answer: We are using truncate load because we are retrieving the entire dataset from BQ every time we load the data. 
Since our project is not comparing music trends over time (at this current version), we are not interested in keeping old versions of our data stored.
Additionally, since we're interested in showing what's popular right now in each country, we only care about pulling the most recent data.
Therefore, we decided to use truncate load because we want to replace our dataset with the newest data each time we load the app.
