import pandas as pd
import numpy as np

df = pd.read_csv('reaction_kinetics.csv') # reads the CSV file into a DataFrame
df_clean = df[df['concentration'] > 0].copy() # drop negative concentrations

df_clean['zero_order'] = df_clean['concentration'] # zero-order reaction [kinetics law]
df_clean['first_order'] = np.log(df_clean['concentration']) # first-order reaction [kinetics law]
df_clean['second_order'] = 1 / df_clean['concentration'] # second-order reaction [kinetics law]

# linear regression model

from scipy.stats import linregress

# define the x variable
time_s= df_clean["time"]

# run the linear regression for all models: 0th/1st/2nd order reactions
zero_fit = linregress(time_s, df_clean["zero_order"])
first_fit = linregress(time_s, df_clean["first_order"])
second_fit = linregress(time_s, df_clean["second_order"])

# find the R-squared values for each model
zero_r_squared = zero_fit.rvalue ** 2
first_r_squared = first_fit.rvalue ** 2
second_r_squared = second_fit.rvalue ** 2

# print the R-squared values for each model
print(f"Zero-order R-squared: {zero_r_squared:.4f}") # R^2 value to 4 decimal places
print(f"First-order R-squared: {first_r_squared:.4f}") # R^2 value to 4 decimal places
print(f"Second-order R-squared: {second_r_squared:.4f}") # R^2 value to 4 decimal places

# determine the best fit model based on R^2 values
best_fit = max(zero_r_squared, first_r_squared, second_r_squared)

if best_fit == zero_r_squared:
    print("The best fit model is the zero-order reaction.")
elif best_fit == first_r_squared:
    print("The best fit model is the first-order reaction.")
else:
    print("The best fit model is the second-order reaction.")




# visual plot using matplotlib

from time import time

import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Plot 1: Zero Order [A] vs t
ax1.scatter(time_s, df_clean['zero_order'], color='red', alpha=0.6, label='Simulated Data')
zero_line = zero_fit.slope * time_s + zero_fit.intercept # y = mx + c
ax1.plot(time_s, zero_line, color='black', linestyle='--', label='Fit')
ax1.set_title(f"Zero Order\nR² = {zero_r_squared:.4f}")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("[N2O5]")
ax1.legend()

# Plot 2: First Order ln[A] vs t
ax2.scatter(time_s, df_clean['first_order'], color='lime', alpha=0.6, label='Simulated Data')
first_line = first_fit.slope * time_s + first_fit.intercept
ax2.plot(time_s, first_line, color='black', linestyle='--', label='Fit')
ax2.set_title(f"First Order (Best Fit)\nR² = {first_r_squared:.4f}")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("ln[N2O5]")
ax2.legend()

# Plot 3: Second Order 1/[A] vs t
ax3.scatter(time_s, df_clean['second_order'], color='fuchsia', alpha=0.6, label='Simulated Data')
second_line = second_fit.slope * time_s + second_fit.intercept
ax3.plot(time_s, second_line, color='black', linestyle='--', label='Fit')
ax3.set_title(f"Second Order\nR² = {second_r_squared:.4f}")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("1/[N2O5]")
ax3.legend()

# 2. Adjust spacing
plt.tight_layout()
plt.savefig('Kinetics_Analysis_Result.png', dpi=300)
plt.show()
