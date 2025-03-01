#pip install pytest

import pandas as pd
from io import StringIO
from country_functions_test_pt3 import load_and_prepare_data  # Adjust the import to your project structure

# Mock CSV Data
mock_csv_data = """
Country Name,2023
China,1444216107
India,1393409038
United States,332915073
Indonesia,276361783
Pakistan,225199937
Brazil,214326223
Nigeria,211400708
Bangladesh,166303498
Russia,143446060
Mexico,130262216
"""

# Helper function to simulate reading from a CSV
def get_mock_csv():
    return StringIO(mock_csv_data)

# Test 1: Check if the function loads the correct number of countries
def test_load_and_prepare_data_num_countries():
    # Use StringIO to simulate a file
    df = load_and_prepare_data(get_mock_csv(), 5)

    # Check if the output is a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Check if the number of countries is as requested
    assert len(df) == 5

# Test 2: Check if countries are sorted by population
def test_load_and_prepare_data_sorted():
    df = load_and_prepare_data(get_mock_csv(), 3)

    # Extract population data
    populations = df["2023"].tolist()

    # Check if sorted in descending order
    assert populations == sorted(populations, reverse=True)

# Test 3: Check if the function returns the correct countries
def test_load_and_prepare_data_correct_countries():
    df = load_and_prepare_data(get_mock_csv(), 3)

    # Extract country names
    countries = df["Country Name"].tolist()

    # Expected output
    expected_countries = ["China", "India", "United States"]

    # Check if the countries are as expected
    assert countries == expected_countries

#python -m pytest country_test_pt3.py