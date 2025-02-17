import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Title for the Streamlit app
st.title("🌍 Population by Country in 2023")

# Load the CSV file (Replace with the actual file path)
file_path = "population_by_country.csv"  # Ensure the file is in the correct directory

# Read only "Country Name" and "2023" columns
df = pd.read_csv(file_path, usecols=["Country Name", "2023"])

# Allow user to select the number of countries to display
num_countries = st.slider("Select number of countries to display", min_value=5, max_value=len(df), value=20)

# Select top N countries based on population
df = df.sort_values(by="2023", ascending=False).head(num_countries)

# Create the bar chart
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(df["Country Name"], df["2023"], color="skyblue")

# Labels and title
ax.set_xlabel("Country Name", fontsize=12)
ax.set_ylabel("Population in 2023", fontsize=12)
ax.set_title("Population by Country in 2023", fontsize=14)
ax.set_xticklabels(df["Country Name"], rotation=90)

# Display the chart in Streamlit
st.pyplot(fig)