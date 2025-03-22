"""
Question 1: Data Cleaning and Basic Analysis

Using the provided dataset 'sales_data.csv', perform the following tasks:

1. Load and examine the dataset
2. Clean the data:
   - Handle missing values in the 'price' column (replace with mean)
   - Handle missing values in the 'category' column (replace with mode)
   - Convert 'sale_date' to datetime
3. Create a summary of:
   - Total number of sales per category
   - Average price per category
   - Number of missing values handled

The cleaned dataset should be ready for further analysis.
"""

# Your code here

import numpy as np
import pandas as pd
from urllib.request import urlopen

# Raw file URL
url = r"https://raw.githubusercontent.com/FelipeC-astro/technical-interview/main/technical-interview/data/sales_data.csv"

# Naming raw file to save locally
raw_file = "sales_data.csv"

try:
    # Downloading content from url
    response = urlopen(url)
    content = response.read().decode('utf-8')

    # Creating and saving content to a local file
    with open(raw_file, 'w') as file:
        file.write(content)
except Exception as e:
    print(f"Error downloading or reading the dataset: {e}")


input_data_path = r'./'+raw_file
sales_data = pd.read_csv(input_data_path)

# Testing if dataset is not empty
if sales_data.empty:
    print("Error: Dataset is empty.")

print("\nPreview of initial data:\n")
print(sales_data.head())

# Display initial dataset information
print("\n\nDataset before cleaning:\n")
print(sales_data.info())
print("\nStatistics from dataset before cleaning:")
print(sales_data.describe(include='all'))

# Count missing values before cleaning

missing_price_before = sales_data['price'].isnull().sum()
missing_category_before = sales_data['category'].isnull().sum()

# Fill missing values in 'price' column with the mean
price_mean = sales_data['price'].mean()
sales_data['price'].fillna(price_mean, inplace=True)

# Fill missing values in 'category' column with the mode
category_mode = sales_data['category'].mode()[0]
sales_data['category'].fillna(category_mode, inplace=True)

# Convert 'sale_date' column to datetime format
sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'], errors='coerce')

# Total number of sales per category
sales_per_category = sales_data['category'].value_counts()

# Average price by category rounded to two decimal places
average_price_per_category = np.around(sales_data.groupby('category')['price'].mean(),2)

# Number of missing values handled
missing_summary = {
    'price': missing_price_before,
    'category': missing_category_before
}

# Display dataset information after cleaning
print("\nDataset after cleaning:\n")
print(sales_data.info())
print("\n\nStatistics from dataset after cleaning:\n")
print(sales_data.describe(include='all'))

# Display summary
print("\nSummary:\n")
print(f"Total sales per category:\n{sales_per_category}\n")
print(f"\nAverage price per category:\n{average_price_per_category}\n")
print(f"\nMissing values handled:\n{missing_summary}\n")

# Export cleaned dataset

clean_file = r'./clean_sales_data.csv'

sales_data.to_csv(clean_file, index=False)

print(f"Cleaned data exported to '{clean_file}'")
