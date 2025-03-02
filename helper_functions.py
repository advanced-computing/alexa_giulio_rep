import pandas as pd
import matplotlib.pyplot as plt
from kaggle.api.kaggle_api_extended import KaggleApi

#giulio functions

def load_and_prepare_data(file_path, num_countries):
    # Load data and select relevant columns
    df = pd.read_csv(file_path, usecols=["Country Name", "2023"])

    # Sort and select most populated countries
    df = df.sort_values(by="2023", ascending=False).head(num_countries)

    return df

def create_population_chart(df):
    # Create bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(df["Country Name"], df["2023"], color="skyblue")
    ax.set_xlabel("Country Name", fontsize=12)
    ax.set_ylabel("Population in 2023", fontsize=12)
    ax.set_title("Population by Country in 2023", fontsize=14)
    ax.set_xticklabels(df["Country Name"], rotation=90)

    return fig

#alexa functions

#separates out multiple artists that are credited on a single song
def name_cleaning(df: pd.DataFrame, column_name: str):
    df[column_name] = df[column_name].str.split(", ")
    return name_separating(df, column_name)

#puts the individual artists into their own rows as a list
def name_separating(df: pd.DataFrame, column_name: str):
    df = df.explode(column_name)[column_name].tolist()
    return df



    

