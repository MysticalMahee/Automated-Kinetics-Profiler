# Automated Reaction Kinetics for N2O5 Decomposition

import numpy as np
import pandas as pd

k_rate = 0.06 #units of s^-1 since it is 1st order
A_initial = 0.10 # random initial concentration of N2O5

time_s = np.linspace(0, 60, 60) # time in seconds, generating 60 points from 0 to 60 seconds

concentration_exact = A_initial * np.exp(-k_rate * time_s) # first order reaction kinetics equation


np.random.seed(20) # for reproducibility
noise = np.random.normal(loc=0, scale=0.003, size=len(time_s)) # adding some noise to the data
concentration_noisy = concentration_exact + noise
df = pd.DataFrame({'time': time_s, 'concentration': concentration_noisy})

df.to_csv('reaction_kinetics.csv', index=False) # save the data to a CSV file

print("Reaction kinetics data saved to 'reaction_kinetics.csv'")
df_clean = df[df['concentration'] > 0].copy() # drop negative concentrations
print(df_clean)
