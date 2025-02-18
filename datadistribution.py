#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:50:44 2025

@author: diyakalyanpur
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the final processed CSV file
file_path = "/Users/diyakalyanpur/Downloads/HF_Lung_V1-master/breathing_rate_final.csv"
df = pd.read_csv(file_path)

# Ensure the expected breathing rate column exists
if "Expected Breathing Rate" not in df.columns:
    raise ValueError("Expected Breathing Rate column is missing from the dataset.")

# Plot histogram
plt.figure(figsize=(10, 6))
plt.hist(df["Expected Breathing Rate"], bins=range(4, 42, 1), edgecolor="black", alpha=0.7)

# Add labels and title
plt.xlabel("Breathing Rate (bpm)")
plt.ylabel("Frequency")
plt.title("Histogram of Expected Breathing Rate (4 to 40 bpm)")
plt.xticks(range(4, 41, 1))  # Ensure each breathing rate is displayed
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Display the frequency of each breathing rate on the bars
for rate in range(4, 41):
    count = (df["Expected Breathing Rate"] == rate).sum()
    if count > 0:
        plt.text(rate, count, str(count), ha="center", va="bottom", fontsize=10)

# Show the plot
plt.show()
