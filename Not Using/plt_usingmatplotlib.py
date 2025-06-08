import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Step 1: Load or simulate data ---
time = pd.date_range("2025-01-01", periods=100, freq="S")

# Replace these with real CSVs
utf = pd.read_csv('UDP-Prague.csv')
tfcubic = pd.read_csv('Cubic.csv')
baseline_propagation_delay_df = pd.read_csv('Baseline_Propagation_Delay.csv')

# Ensure 'Time' column is converted to datetime format if not already
utf['Time'] = pd.to_datetime(utf['Time'])
tfcubic['Time'] = pd.to_datetime(tfcubic['Time'])
baseline_propagation_delay_df['Time'] = pd.to_datetime(baseline_propagation_delay_df['Time'])

# --- Step 2: Plot the data ---
plt.figure(figsize=(10, 6))

# Plot for UDP-Prague
plt.plot(utf['Time'], utf['SmoothedRTT'], label='UDP-Prague', color='blue')

# Plot for Cubic
plt.plot(tfcubic['Time'], tfcubic['SmoothedRTT'], label='Cubic', color='green')

# Plot for Baseline Propagation Delay
plt.plot(baseline_propagation_delay_df['Time'], baseline_propagation_delay_df['SmoothedRTT'], label='Baseline Propagation Delay', color='red')

# Add labels and title
plt.xlabel('Time')
plt.ylabel('Smoothed RTT')
plt.title('RTT Comparison across Different DataFrames')

# Add a legend to differentiate the lines
plt.legend()

# Show the plot
plt.show()
