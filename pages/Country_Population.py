import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# title
st.title("🌍 Population by Country in 2023")

# load data
file_path = "population_by_country.csv" 

# show only country and year
df = pd.read_csv(file_path, usecols=["Country Name", "2023"])

# make widget to choose number of countries to display
num_countries = st.slider("Select number of countries to display", min_value=5, max_value=len(df), value=20)

# select most populated countries 
df = df.sort_values(by="2023", ascending=False).head(num_countries)

# make chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(df["Country Name"], df["2023"], color="skyblue")
ax.set_xlabel("Country Name", fontsize=12)
ax.set_ylabel("Population in 2023", fontsize=12)
ax.set_title("Population by Country in 2023", fontsize=14)
ax.set_xticklabels(df["Country Name"], rotation=90)

# streamlit
st.pyplot(fig)

# 