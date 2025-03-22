"""
Question 3: Sales Visualization

Using the cleaned dataset from Question 1 ('sales_data.csv'), create the following visualizations:

1. Create a line plot showing daily sales trends over time
   - Include a 7-day moving average line

2. Create a bar plot showing:
   - Total sales by category
   - Include error bars representing standard deviation

3. Create a scatter plot showing:
   - Relationship between quantity and price
   - Color points by category
   - Add a trend line

Requirements:
- Use appropriate labels and titles
- Include a legend where necessary
- Use a consistent color scheme
- Save all plots as PNG files
"""

# Your code here

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Loading the dataset cleaned in Question 1

sales_data_path = r'./clean_sales_data.csv'
sales_data = pd.read_csv(sales_data_path)

# Convert 'sale_date' column to datetime format
sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'], errors='coerce')

# Line plot showing daily sales trends over time with 7-day moving average
# You need to group data by sale_date and then sum the sales for each day
daily_sales = sales_data.groupby('sale_date')['price'].sum()

# Here the 7-day moving average is calculated
daily_sales_ma = daily_sales.rolling(window=7).mean()

# Fitting a polynomial (degree 2 for quadratic) to the daily sales data
# We'll use np.polyfit to find the polynomial coefficients
poly_degree = 2
coefficients = np.polyfit(np.arange(len(daily_sales)), daily_sales, poly_degree)
polynomial = np.poly1d(coefficients)

daily_trend = polynomial(np.arange(len(daily_sales)))

# Plotting the daily sales and moving average
plt.figure(figsize=(10, 6))
plt.plot(daily_sales.index, daily_trend, label='Daily Sales trend', color='orange', alpha=1)
plt.plot(daily_sales_ma.index, daily_sales_ma, label='7-Day Moving Average', color='purple', linewidth=1, alpha=0.7)
plt.title('Daily Sales Trends with 7-Day Moving Average')
plt.xlabel('Date')
plt.ylabel('Total sales')
plt.legend()
plt.xticks(rotation=45)
plt.yticks(np.arange(0,201, 50))
plt.tight_layout()
plt.grid(linestyle='--', alpha=0.6)
plt.savefig('daily_sales_trends.png')  # Save as PNG file
plt.show()

# Bar plot showing total sales by category with error bars (standard deviation)

category_sales = sales_data.groupby('category').agg(
    total_sales=('price', 'sum'),
    sales_std=('price', 'std')
).reset_index()

plt.figure(figsize=(8, 5))
plt.bar(category_sales['category'], category_sales['total_sales'], 
        yerr=category_sales['sales_std'], capsize=5, color='orange', alpha=0.5)

plt.title('Total Sales by Category with Standard Deviation')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig('sales_by_category.png')
plt.show()

plt.figure(figsize=(10, 8))
sns.scatterplot(data=sales_data, x='quantity', y='price', hue='category', palette='Paired')

# Adding a trendline for each category
for category in sales_data['category'].unique():
    sns.regplot(data=sales_data[sales_data['category'] == category],
                x='quantity', y='price', scatter=False, label=f'Trend - {category}', ci=None)

plt.title('Relationship Between Quantity and Price by Category')
plt.xlabel('Quantity')
plt.ylabel('Price')
plt.legend(title='Category', loc = (1.05,0))
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('quantity_price_relationship.png')
plt.show()
