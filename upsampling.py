
'''
def process_signal(f_name, target_rate, source_rate, output_file):
    try:
        signal, sr = librosa.load(f_name, sr=None)

    
        new_sr = sr * target_rate / source_rate
        if new_sr <= 0:
            raise ValueError(f"Invalid new sample rate ({new_sr}).")


        resampled_signal = librosa.resample(signal, orig_sr=sr, target_sr=new_sr)

      
        target_length = int(15 * sr)
        if len(resampled_signal) > target_length:
            resampled_signal = resampled_signal[:target_length]
        else:
            padding = target_length - len(resampled_signal)
            resampled_signal = np.pad(resampled_signal, (0, padding), mode="")

    
        wavfile.write(output_file, sr, (resampled_signal * 32767).astype(np.int16))
        print(f"Processed and saved: {output_file}")
    except Exception as e:
        print(f"Error processing {f_name}: {e}")

def process_underrepresented_classes(base_folder, min_files=20):
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

        # Determine target rates
        if source_rate + 5 <= 40:
            available_rates = list(range(source_rate + 1, source_rate + 6))
        elif source_rate == 40:
            available_rates = list(range(35, 40))
        else:
            available_rates = list(range(source_rate + 1, 41))

        target_rates = [random.choice(available_rates) for _ in range(files_to_generate)]

        for i, target_rate in enumerate(target_rates):
            random_file = random.choice(audio_files)
            random_file_path = os.path.join(folder_path, random_file)

            
            target_folder_path = os.path.join(base_folder, str(target_rate))
            if not os.path.exists(target_folder_path):
                print(f"Target folder does not exist: {target_folder_path}")
                continue

           
            new_file_name = f"generated_{source_rate}_to_{target_rate}_{i}.wav"
            output_file_path = os.path.join(target_folder_path, new_file_name)

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
'''
import os
import random
from scipy.io import wavfile
import librosa
import numpy as np

def process_signal(f_name, target_rate, source_rate, output_file):
    try:
        signal, sr = librosa.load(f_name, sr=None)
        
        new_sr = sr * source_rate / target_rate
        
        # if target_rate > source_rate:
        #     new_sr = sr * target_rate / source_rate
        #     print("Yes")
        # else:
        #     new_sr = sr * source_rate / target_rate
        #     print("No", new_sr, sr * source_rate / target_rate)

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

    except Exception as e:
        print(f"Error processing {f_name}: {e}")

def process_underrepresented_classes(base_folder, min_files=20):
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

        if source_rate + 5 <= 40:
            available_rates = list(range(source_rate + 1, source_rate + 6))
        elif source_rate == 40:
            available_rates = list(range(35, 40))
        else:
            available_rates = list(range(source_rate + 1, 41))

        target_rates = [random.choice(available_rates) for _ in range(files_to_generate)]

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
