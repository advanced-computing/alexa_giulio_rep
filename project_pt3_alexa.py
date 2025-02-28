#creating a general function to clean the artist name column
import pandas as pd

#separates out multiple artists that are credited on a single song
def name_cleaning(df: pd.DataFrame, column_name: str):
    df[column_name] = df[column_name].str.split(", ")
    return name_separating(df, column_name)


#puts the individual artists into their own rows as a list
def name_separating(df: pd.DataFrame, column_name: str):
    df = df.explode(column_name)[column_name].tolist()
    return df

