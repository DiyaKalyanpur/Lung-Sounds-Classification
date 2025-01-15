
import os
import random
from scipy.io import wavfile
import librosa
import numpy as np

def process_signal(f_name, target_rate, source_rate, output_file):
    try:
        signal, sr = librosa.load(f_name, sr=None)

        sr = 4000

        new_sr = sr * source_rate / target_rate
        if new_sr <= 0:
            raise ValueError(f"Invalid new sample rate ({new_sr}). Check source_rate and target_rate.")

        # Resample the signal
        resampled_signal = librosa.resample(signal, orig_sr=sr, target_sr=new_sr)

        target_length = int(15 * sr)
        if len(resampled_signal) > target_length:
            resampled_signal = resampled_signal[:target_length]
        else:
            padding = target_length - len(resampled_signal)
            resampled_signal = np.pad(resampled_signal, (0, padding), mode="constant")

        wavfile.write(output_file, sr, (resampled_signal * 32767).astype(np.int16))
        print(f"Processed and saved: {output_file}")
    except Exception as e:
        print(f"Error processing {f_name}: {e}")

def process_underrepresented_classes(base_folder, min_files=20):

    used_target_rates = {}

    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)


        if not os.path.isdir(folder_path):
            continue


        try:
            source_rate = int(folder)
        except ValueError:
            print(f"Skipping folder: {folder} (not a valid breathing rate)")
            continue


        if source_rate < 5 or source_rate > 40:
            print(f"Skipping folder: {folder} (out of processing range)")
            continue

        audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

        if len(audio_files) >= min_files:
            continue

        print(f"Processing underrepresented class: {folder} (Files: {len(audio_files)})")

        files_to_generate = min_files - len(audio_files)

        if source_rate <= 30:
            available_rates = list(range(source_rate + 1, source_rate + 11))
        else:
            available_rates = list(range(5, 41))

        if source_rate in used_target_rates:
            available_rates = [rate for rate in available_rates if rate not in used_target_rates[source_rate]]
            
        print(f"Available rates for source rate {source_rate}: {available_rates}")
        
        if len(available_rates) < files_to_generate:
            print(f"Warning: Not enough unique target rates for source rate {source_rate}. ")
            files_to_generate = len(available_rates)

        target_rates = random.sample(available_rates, files_to_generate)

        if source_rate not in used_target_rates:
            used_target_rates[source_rate] = []

        used_target_rates[source_rate].extend(target_rates)

        for i, target_rate in enumerate(target_rates):
            
            random_file = random.choice(audio_files)
            random_file_path = os.path.join(folder_path, random_file)

            new_file_name = f"generated_{source_rate}_to_{target_rate}_{i}.wav"
            output_file_path = os.path.join(folder_path, new_file_name)

            try:
                process_signal(
                    f_name=random_file_path,
                    target_rate=target_rate,
                    source_rate=source_rate,
                    output_file=output_file_path
                )
            except Exception as e:
                print(f"Error processing file {random_file}: {e}")


base_folder = "/Users/diyakalyanpur/Downloads/output_folder"  
process_underrepresented_classes(base_folder)



