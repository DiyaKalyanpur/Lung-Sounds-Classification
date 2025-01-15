# -*- coding: utf-8 -*-
"""breathing_rate.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wpuO_CGXaDUWb7ebjhczS9k8bix4Y837
"""

import os
import re

directory_path = "/content/sample_data/"

# Define the pattern for valid lines
line_pattern = re.compile(r"^(I|E)\s\d{2}:\d{2}:\d{2}\.\d{3}\s\d{2}:\d{2}:\d{2}\.\d{3}$")

# Function to convert a timestamp to seconds
def convert_to_seconds(timestamp):
    hours, minutes, seconds = map(float, timestamp.split(":"))
    return hours * 3600 + minutes * 60 + seconds

# Function to calculate breathing rate from a file
def calculate_breathing_rate(file_path):
    inhalation_times = []
    exhalation_times = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3 and line_pattern.match(line.strip()):
                label = parts[0]
                start_time = parts[1]
                start_time_sec = convert_to_seconds(start_time)

                if label == "I":
                    inhalation_times.append(start_time_sec)
                elif label == "E":
                    exhalation_times.append(start_time_sec)

    # Use the longer list of times for cycle calculations
    if len(inhalation_times) >= len(exhalation_times):
        times = inhalation_times
    else:
        times = exhalation_times

    # Calculate time differences between successive events
    differences = [t2 - t1 for t1, t2 in zip(times[:-1], times[1:])]

    # If no differences, return 0 as the breathing rate
    if not differences:
        return 0, 0

    # Average cycle duration
    avg_cycle_duration = sum(differences) / len(differences)

    # Calculate breathing rate
    breathing_rate = 60 / avg_cycle_duration

    # Calculate expected rate based on the number of differences
    expected_rate = len(differences) * 4

    return breathing_rate, expected_rate

# Main loop to process all files in the directory
results = {}
for file_name in os.listdir(directory_path):
    if file_name.endswith(".txt"):
        file_path = os.path.join(directory_path, file_name)
        breathing_rate, expected_rate = calculate_breathing_rate(file_path)  # Unpack values
        results[file_name] = (breathing_rate, expected_rate)

# Print the results
for file_name, (breathing_rate, expected_rate) in results.items():
    print(f"File: {file_name}, Breathing Rate: {breathing_rate:.0f} BPM, Expected Rate: {expected_rate}")



!pip install pandas openpyxl





'''import matplotlib.pyplot as plt

# Extract breathing rates from the results dictionary
breathing_rates = [rate[0] for rate in results.values()]  # Extract only breathing_rate

# Generate the histogram
plt.figure(figsize=(12, 6))
plt.hist(
    breathing_rates,
    bins=range(int(min(breathing_rates)), int(max(breathing_rates)) + 2),  # Ensure proper binning
    edgecolor='black',
    alpha=0.75,
    color='skyblue'
)
plt.title("Histogram of Breathing Rates", fontsize=16, fontweight='bold')
plt.xlabel("Breathing Rate (BPM)", fontsize=14)
plt.ylabel("Frequency", fontsize=14)
plt.xticks(
    range(int(min(breathing_rates)), int(max(breathing_rates)) + 2, 1), fontsize=12
)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
'''
import matplotlib.pyplot as plt


breathing_rates = [rate[0] for rate in results.values()]


plt.figure(figsize=(12, 6))


counts, bins, _ = plt.hist(
    breathing_rates,
    bins=range(4, 48),
    edgecolor='black',
    alpha=0.75,
    color='skyblue'
)

for i in range(len(counts)):
    plt.text(bins[i] + 0.5 * (bins[i + 1] - bins[i]), counts[i], str(counts[i]),
             ha='center', va='bottom',fontsize=7)

plt.title("Histogram of Breathing Rates", fontsize=16, fontweight='bold')
plt.xlabel("Breathing Rate (BPM)", fontsize=14)
plt.ylabel("Frequency", fontsize=14)


plt.xticks(range(4, 48, 1), fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()



import os
import re
import pandas as pd

directory_path = "/content/sample_data/"


line_pattern = re.compile(r"^(I|E)\s\d{2}:\d{2}:\d{2}\.\d{3}\s\d{2}:\d{2}:\d{2}\.\d{3}$")


def convert_to_seconds(timestamp):
    hours, minutes, seconds = map(float, timestamp.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def calculate_breathing_rate(file_path):
    inhalation_times = []
    exhalation_times = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3 and line_pattern.match(line.strip()):
                label = parts[0]
                start_time = parts[1]
                start_time_sec = convert_to_seconds(start_time)

                if label == "I":
                    inhalation_times.append(start_time_sec)
                elif label == "E":
                    exhalation_times.append(start_time_sec)


    if len(inhalation_times) >= len(exhalation_times):
        times = inhalation_times
    else:
        times = exhalation_times


    differences = [t2 - t1 for t1, t2 in zip(times[:-1], times[1:])]


    if not differences:
        return 0, 0


    avg_cycle_duration = sum(differences) / len(differences)


    breathing_rate = round(60 / avg_cycle_duration)

    return breathing_rate, None


results = {}
for file_name in os.listdir(directory_path):
    if file_name.endswith(".txt"):
        file_path = os.path.join(directory_path, file_name)
        breathing_rate, _ = calculate_breathing_rate(file_path)
        results[file_name] = breathing_rate


file_names = list(results.keys())
breathing_rates = list(results.values())
df_all_data = pd.DataFrame([file_names, breathing_rates])


filtered_data = {file_name: rate for file_name, rate in results.items() if rate == 0 or 30 <= rate <= 50}
df_filtered_data = pd.DataFrame(filtered_data.items(), columns=["File Name", "Breathing Rate"])


output_file = "/content/Breathing_Rates.xlsx"
with pd.ExcelWriter(output_file) as writer:
    df_all_data.to_excel(writer, sheet_name="All Data", index=False, header=False)
    df_filtered_data.to_excel(writer, sheet_name="Filtered Data", index=False)

print(f"Excel file saved to: {output_file}")

from google.colab import files
files.download("/content/Breathing_Rates.xlsx")

import librosa
import scipy.io.wavfile as wavfile
import numpy as np
from google.colab import files

def process_signal(f_name, target_rate, source_rate, output_file, sampling_rate=4000):

    signal, sr = librosa.load(f_name, sr=None)

    new_sr = sr *  source_rate /target_rate


    resampled_signal = librosa.resample(signal, orig_sr=sr, target_sr=new_sr)


    target_length = int(15 * sr)
    if len(resampled_signal) > target_length:
        resampled_signal = resampled_signal[:target_length]
    else:
        padding = target_length - len(resampled_signal)
        resampled_signal = np.pad(resampled_signal, (0, padding), mode="constant")


    wavfile.write(output_file, sr, (resampled_signal * 32767).astype(np.int16))


    files.download(output_file)

if __name__ == "__main__":
    f_name = "/content/sample_data/steth_20190716_10_19_03.wav"
    target_rate = 30
    source_rate = 31
    output_file = "processed_signal.wav"

    process_signal(f_name, target_rate, source_rate, output_file)

import pandas as pd
import librosa
import scipy.io.wavfile as wavfile
import numpy as np
import os
import random


def process_signal(f_name, target_rate, source_rate, output_file):
    """
    Process and resample an audio signal to match a target rate.
    """
    try:
        # Load the audio signal
        signal, sr = librosa.load(f_name, sr=None)

        # Calculate new sample rate
        new_sr = int(sr * source_rate / target_rate)

        # Resample the signal
        resampled_signal = librosa.resample(signal, orig_sr=sr, target_sr=new_sr)

        # Truncate or pad the signal to 15 seconds
        target_length = int(15 * sr)
        if len(resampled_signal) > target_length:
            resampled_signal = resampled_signal[:target_length]
        else:
            padding = target_length - len(resampled_signal)
            resampled_signal = np.pad(resampled_signal, (0, padding), mode="constant")

        # Save the processed audio file
        wavfile.write(output_file, sr, (resampled_signal * 32767).astype(np.int16))
        print(f"Processed and saved: {output_file}")
    except Exception as e:
        print(f"Error processing {f_name}: {e}")


def assign_labels_and_process_audio_with_histogram(excel_file, audio_folder, output_folder):
    """
    Assign labels to audio files and process underrepresented breathing rates.
    """
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Count occurrences of each breathing rate
        breathing_rate_counts = df['BreathingRate'].value_counts()

        # Identify underrepresented breathing rates
        underrepresented_rates = breathing_rate_counts[breathing_rate_counts < 10].index.tolist()
        print(f"Underrepresented breathing rates (less than 10 samples): {underrepresented_rates}")

        # Process each row in the DataFrame
        for index, row in df.iterrows():
            breathing_rate = row['BreathingRate']
            audio_file = row['AudioFile']

            # Assign target_rate
            if breathing_rate in underrepresented_rates:
                target_rate = breathing_rate
            else:
                #print(f"Skipping breathing rate {breathing_rate}, as it is not underrepresented.")
                continue  # Skip processing if the class is not underrepresented

            # Ensure source_rate is valid
            source_rate = max(1, random.randint(target_rate - 5, target_rate - 1))

            # Construct input and output file paths
            input_path = os.path.join(audio_folder, audio_file)
            output_file = os.path.join(output_folder, f"Rate_{breathing_rate}_processed.wav")

            # Process the audio signal
            process_signal(input_path, target_rate, source_rate, output_file)
    except Exception as e:
        print(f"Error in assign_labels_and_process_audio_with_histogram: {e}")


if __name__ == "__main__":
    # Input paths
    excel_file = "/content/sample_data/Breathing_Rates _final (1).xlsx"
    audio_folder = "/content/drive/MyDrive/audio_files"
    output_folder = "processed_audio"

    # Run the processing function
    assign_labels_and_process_audio_with_histogram(excel_file, audio_folder, output_folder)

def assign_labels_and_process_audio_with_histogram(excel_file, audio_folder, output_folder):

    df = pd.read_excel(excel_file)

    target_rate = 30
    os.makedirs(output_folder, exist_ok=True)

    # Analyze distribution of breathing rates
    breathing_rate_counts = df['BreathingRate'].value_counts()

    underrepresented_rates = breathing_rate_counts[breathing_rate_counts < 10].index.tolist()
    print(f"Underrepresented breathing rates (less than 10 samples): {underrepresented_rates}")

    for index, row in df.iterrows():
        breathing_rate = row['BreathingRate']
        audio_file = row['AudioFile']

        if breathing_rate in underrepresented_rates:
            target_rate = breathing_rate
        else:
            print("No more underrepresented classes")
            target_rate = breathing_rate


        source_rate = max(1, random.randint(target_rate - 5, target_rate - 1))

        input_path = os.path.join(audio_folder, audio_file)
        output_file = os.path.join(output_folder, f"Rate_{breathing_rate}_processed.wav")

        process_signal(input_path, target_rate, source_rate, output_file)

import os
import shutil
import pandas as pd
from google.colab import drive
drive.mount('/content/drive')


# Input paths
excel_file = "/content/drive/MyDrive/Colab Notebooks/audio_files/Breathing_Rates _final (1).xlsx"
audio_folder = "/content/drive/MyDrive/Colab Notebooks/audio_files"
output_folder = "/content/sample_data/output_folder"

# Path to save missing files log
missing_files_log = "/content/sample_data/missing_files.txt"

# Read the Excel file
df = pd.read_excel(excel_file)

# Ensure the necessary columns are present
if 'AudioFile' not in df.columns or 'BreathingRate' not in df.columns:
    raise ValueError("Excel file must contain 'AudioFile' and 'BreathingRate' columns.")

# List to store missing files
missing_files = []

# Iterate over the DataFrame to organize files
for index, row in df.iterrows():
    file_name = row['AudioFile']  # Get the file name
    breathing_rate = row['BreathingRate']  # Get the breathing rate

    # Validate the breathing rate
    if not isinstance(breathing_rate, (int, float)):
        print(f"Skipping invalid breathing rate for file {file_name}: {breathing_rate}")
        continue

    # Create the target folder for the breathing rate if it doesn't exist
    rate_folder = os.path.join(output_folder, str(int(breathing_rate)))
    os.makedirs(rate_folder, exist_ok=True)

    # Source and destination paths
    source_path = os.path.join(audio_folder, file_name)
    destination_path = os.path.join(rate_folder, file_name)

    # Copy the file to the target folder or log missing files
    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
        print(f"Copied {file_name} to {rate_folder}")
    else:
        print(f"File not found: {source_path}")
        missing_files.append(file_name)

# Write the missing files to the log
if missing_files:
    with open(missing_files_log, "w") as log:
        log.write("\n".join(missing_files))
    print(f"Missing files log saved to: {missing_files_log}")
else:
    print("All files were successfully copied.")

print("File organization completed.")

import os
import shutil
import pandas as pd
drive_output_folder = "/content/drive/MyDrive/output_folder"
drive.mount('/content/drive', force_remount=True)
if os.path.exists(output_folder):
    shutil.copytree(output_folder, drive_output_folder)
    print(f"Output folder uploaded to Google Drive at: {drive_output_folder}")
else:
    print("Output folder does not exist. Nothing to upload.")