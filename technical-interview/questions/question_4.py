"""
Question 4: Statistical Analysis and Error Handling

Using scipy and the cleaned dataset from Question 1, perform the following tasks:

1. Implement error handling for the following analyses:
   - Perform a one-way ANOVA test to compare prices across different categories
   - Calculate and plot the confidence intervals for mean prices in each category
   - Identify potential outliers using z-scores

2. Debug and fix the following code snippet that attempts to perform a chi-square test:
   ```python
   def perform_chi_square(data):
       observed = data.groupby(['category', 'status']).size()
       chi2, p_value = stats.chi2_contingency(observed)
       return chi2, p_value
   ```

3. Implement proper logging to track:
   - Any statistical assumptions violations
   - Data type mismatches
   - Invalid calculations

Your solution should be robust against various edge cases and include appropriate error messages.
"""

# Your code here

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Loading the dataset cleaned in Question 1
sales_data_path = r'./clean_sales_data.csv'
sales_data = pd.read_csv(sales_data_path)

# Convert 'sale_date' column to datetime format
sales_data['sale_date'] = pd.to_datetime(sales_data['sale_date'], errors='coerce')

# One-way ANOVA test to compare prices across different categories
try:
    df = sales_data[['category', 'price']].dropna()
    categories = df['category'].unique()

    if len(categories) >= 2:
        price_groups = [df[df['category'] == cat]['price'] for cat in categories]
        f_stat, p_value = stats.f_oneway(*price_groups)
        logging.info(f"ANOVA completed: F = {f_stat:.2f}, p = {p_value:.4f}")
    else:
        logging.warning("Not enough categories to perform ANOVA.")
except Exception as e:
    logging.error(f"Error during ANOVA: {e}")
    
# Confidence intervals for mean prices in each category
try:
    means = []
    conf_intervals = []
    for cat in categories:
        prices = df[df['category'] == cat]['price']
        if len(prices) < 2:
            logging.warning(f"Not enough data in category '{cat}' for confidence interval.")
            continue
        mean = prices.mean()
        sem = stats.sem(prices)
        ci_low, ci_high = stats.t.interval(0.95, len(prices)-1, loc=mean, scale=sem)
        means.append(mean)
        conf_intervals.append((ci_low, ci_high))
        logging.info(f"{cat}: mean = {mean:.2f}, 95% CI = [{ci_low:.2f}, {ci_high:.2f}]")
    
    # Simple plot
    plt.bar(categories, means, yerr=[(high - low) / 2 for low, high in conf_intervals], capsize=5)
    plt.xlabel('Category')
    plt.ylabel('Mean Price')
    plt.title('Mean Prices with 95% Confidence Intervals')
    plt.tight_layout()
    plt.savefig('./confidence_intervals.png')
    plt.show()
except Exception as e:
    logging.error(f"Error calculating confidence intervals: {e}")

# Outlier detection using z-score
try:
    df['z_score'] = df.groupby('category')['price'].transform(lambda x: stats.zscore(x, nan_policy='omit'))
    outliers = df[np.abs(df['z_score']) > 3]
    logging.info(f"Outliers found: {len(outliers)}")
except Exception as e:
    logging.error(f"Error detecting outliers: {e}")
    
def perform_chi_square(data):
    
    try:
        # Using pd.crosstab() to create a contingency table, as expected by chi2_contingency()
        contingency_table = pd.crosstab(data['category'], data['status'])
        
        # Perform chi-square test on the contingency table
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        logging.info(f"Chi-square test completed: chi2 = {chi2:.2f}, p = {p_value:.4f}")
        return chi2, p_value

    # Error handling if expected columns are missing in the dataframe
    except KeyError as e:
        logging.error(f"Missing column in data: {e}")
        return None, None
    
    # General exception handling for any other unexpected errors
    except Exception as e:
        logging.error(f"Error performing chi-square test: {e}")
        return None, None

# Example of using this function
chi2_result, p_val = perform_chi_square(sales_data)
