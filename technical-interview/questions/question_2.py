"""
Question 2: Customer Purchase Analysis

Using the provided dataset 'customer_purchases.csv', perform the following analyses:

1. Calculate the following metrics per customer:
   - Total amount spent
   - Average purchase value
   - Number of purchases
   - Most frequently bought category

2. Create a summary DataFrame with:
   - Top 5 customers by total spend
   - Bottom 5 customers by total spend

3. Calculate the monthly purchase trends:
   - Total sales per month
   - Average purchase value per month

Bonus: Identify any customers who haven't made a purchase in the last 3 months
"""

# Your code here

import pandas as pd
import numpy as np
from urllib.request import urlopen

# Raw file URL
url = r"https://raw.githubusercontent.com/FelipeC-astro/technical-interview/main/technical-interview/data/customer_purchases.csv"

# Naming output file to save locally
output_file = "customer_purchases.csv"

try:
    # Downloading content from url
    response = urlopen(url)
    content = response.read().decode('utf-8')

    # Creating and saving content to a local file
    with open(output_file, 'w') as file:
        file.write(content)
except Exception as e:
    print(f"Error downloading or reading the dataset: {e}")


input_data_path = r'./'+output_file
customer_purchases_data = pd.read_csv(input_data_path)

# Testing if dataset is not empty
if customer_purchases_data.empty:
    print("Error: Dataset is empty.")

print("\nPreview of initial data:\n")
print(customer_purchases_data.head())

# Display initial dataset information
print("\n\nDataset before cleaning:\n")
print(customer_purchases_data.info())
print("\nStatistics from dataset before cleaning:")
print(customer_purchases_data.describe(include='all'))

# Convert 'sale_date' column to datetime format
customer_purchases_data['purchase_date'] = pd.to_datetime(customer_purchases_data['purchase_date'], errors='coerce')

# Grouping by customer_id and aggregating the required metrics
customer_metrics = customer_purchases_data.groupby('customer_id').agg(
    total_amount_spent=('amount', 'sum'),           # Total amount spent by the customer
    average_purchase_value=('amount', 'mean'),      # Average value per purchase
    number_of_purchases=('amount', 'count'),        # Total number of purchases
    most_frequent_category=('category', lambda x: x.mode().iloc[0] if not x.mode().empty else None)  # Most frequent purchase category
).reset_index()

customer_metrics['average_purchase_value'] = np.around(customer_metrics['average_purchase_value'],2)

# Display the calculated metrics
print("\nCustomer metrics:\n")
print(customer_metrics.head())

# Saving results for possible future analysis
customer_metrics.to_csv(r'./customer_metrics.csv', index=False)

# Sorting customers by total spend in descending order for Top 5
top_5_customers = customer_metrics.sort_values(by='total_amount_spent', ascending=False).head(5)

# Sorting customers by total spend in ascending order for Bottom 5
bottom_5_customers = customer_metrics.sort_values(by='total_amount_spent', ascending=True).head(5)

print("\nTop 5 customers by total amount spent:\n")
print(top_5_customers)
top_5_customers.to_csv(r'./top_5_customers.csv', index=False)

print("\n\n\nBottom 5 customers by total amount spent:\n")
print(bottom_5_customers)
bottom_5_customers.to_csv(r'./bottom_5_customers.csv', index=False)

# Extract year-month from 'purchase_date' to sort by months
customer_purchases_data['year_month'] = customer_purchases_data['purchase_date'].dt.to_period('M')

# Group by Year-Month to get monthly sales and average purchase values
monthly_trends = customer_purchases_data.groupby('year_month').agg(
    total_sales=('amount', 'sum'),             # Total sales per month
    avg_purchase_value=('amount', 'mean')      # Average purchase value per month
).reset_index()

print("\nMonthly purchase trends:\n")
print(monthly_trends)

# Most recent purchase date in the dataset
latest_date = customer_purchases_data['purchase_date'].max()

# Threshold date (latest date minus 3 months)
last_3_months = latest_date - pd.DateOffset(months=3)

# Group by customer_id to get their latest purchase date
inactive_customers = customer_purchases_data.groupby('customer_id').agg(
    last_purchase=('purchase_date', 'max')
).reset_index()

# Filter customers who have not made any purchases in the last 3 months
inactive_customers = inactive_customers[inactive_customers['last_purchase'] < last_3_months]

print("\nCustomers who have not made any purchases in the last 3 months:\n")
print(inactive_customers)
inactive_customers.to_csv(r'./inactive_customers.csv', index=False)
