
import os
import random
import shutil
import pandas as pd
from scipy.io import wavfile
import librosa
import numpy as np

def process_signal(f_name, target_rate, source_rate, output_file):
    try:
        signal, sr = librosa.load(f_name, sr=None)
        new_sr = sr * source_rate / target_rate

        if new_sr <= 0:
            raise ValueError(f"Invalid new sample rate ({new_sr}).")

        resampled_signal = librosa.resample(signal, orig_sr=sr, target_sr=new_sr)
        target_length = int(15 * sr) 

        if target_rate > source_rate:
            resampled_signal = resampled_signal[:target_length]
        else:
            padding = target_length - len(resampled_signal)
            resampled_signal = np.pad(resampled_signal, (0, max(0, padding)), mode="constant")

        wavfile.write(output_file, sr, (resampled_signal * 32767).astype(np.int16))
        print(f"Processed and saved: {output_file}")

        return output_file, target_rate

    except Exception as e:
        print(f"Error processing {f_name}: {e}")
        return None, None

def process_underrepresented_classes(csv_file, output_folder, min_files=20):
    df = pd.read_csv(csv_file)
    
    # Convert Expected Breathing Rate to int and filter within range 10-40
    df["Expected Breathing Rate"] = df["Expected Breathing Rate"].astype(int)
    df = df[(df["Expected Breathing Rate"] >= 10) & (df["Expected Breathing Rate"] <= 40)]
    
    processed_entries = []

    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Copy existing files to output folder
    for file_path in df["File"].tolist():
        destination_file = os.path.join(output_folder, os.path.basename(file_path))
        if os.path.exists(destination_file):
            continue  # Skip if file already exists to avoid SameFileError
        if os.path.exists(file_path):
            shutil.copy(file_path, destination_file)

    # Count occurrences of each breathing rate
    breathing_rate_counts = df["Expected Breathing Rate"].value_counts().to_dict()
    
    for target_rate, count in breathing_rate_counts.items():
        if count >= min_files:
            continue

        print(f"Processing underrepresented class: {target_rate} (Files: {count})")
        files_to_generate = min_files - count

        # Check for available source rates in the dataset
        available_rates = sorted(df["Expected Breathing Rate"].unique())
        potential_sources = [r for r in range(target_rate + 1, target_rate + 6) if r in available_rates]
        
        if not potential_sources:
            if target_rate == 40:
                potential_sources = [r for r in range(35, 40) if r in available_rates]
            else:
                potential_sources = [r for r in available_rates if r > target_rate]

        if not potential_sources:
            print(f"No suitable source rates found for {target_rate}")
            continue

        source_rates = [random.choice(potential_sources) for _ in range(files_to_generate)]
        
        # Get available files for selected source rates
        for i, source_rate in enumerate(source_rates):
            source_files = df[df["Expected Breathing Rate"] == source_rate]["File"].tolist()
            if not source_files:
                print(f"No files available for source rate {source_rate}")
                continue
            
            random_file = random.choice(source_files)
            new_file_name = f"generated_{source_rate}_to_{target_rate}_{i}_{random.randint(10000,99999)}.wav"
            output_file_path = os.path.join(output_folder, new_file_name)

            try:
                new_file, new_rate = process_signal(
                    f_name=random_file,
                    target_rate=target_rate,
                    source_rate=source_rate,
                    output_file=output_file_path
                )
                if new_file:
                    processed_entries.append({"File": new_file, "Expected Breathing Rate": new_rate})
            except Exception as e:
                print(f"Error processing file {random_file}: {e}")

    # Append new entries to the CSV
    new_df = pd.DataFrame(processed_entries)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(csv_file, index=False)
    print(f"Updated dataset saved to {csv_file}")

csv_file = "/Users/diyakalyanpur/Downloads/HF_Lung_V1-master/breathing_rate_final.csv"
output_folder = "/Users/diyakalyanpur/Downloads/HF_Lung_V1-master/all_processed_files"
process_underrepresented_classes(csv_file, output_folder)
