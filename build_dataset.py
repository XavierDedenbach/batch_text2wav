import pandas as pd
import os
from huggingface_hub import login
from datasets import Dataset, Audio, load_dataset

""" # Load the English spellings from small_dictionary.txt
with open('small_dictionary.txt', 'r') as f:
    english_spellings = [line.strip() for line in f.readlines()]

# Create a dictionary to store IPA spellings
ipa_dict = {}

# Iterate over each English spelling
for english in english_spellings:
    # Search for the IPA spelling in dict.tsv
    with open('dict.tsv', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            parts = line.strip().split('\t')
            if len(parts) == 2:
                english_spelling, ipa_spelling = parts
                if english_spelling == english:
                    ipa_dict[english] = ipa_spelling
                    break
            else:
                print(f"Warning: skipping line '{line.strip()}' due to invalid format")

# Create a list of audio files
audio_files = []
english_spellings_with_audio = []
ipa_spellings_with_audio = []

for english in english_spellings:
    audio_file = os.path.join('assets_small', f'{english}.wav')
    if os.path.exists(audio_file):
        audio_files.append(audio_file)
        english_spellings_with_audio.append(english)
        ipa_spellings_with_audio.append(ipa_dict[english])
    else:
        print(f"Warning: audio file for '{english}' is missing")

# Create a dataset
data = {
    'english': english_spellings_with_audio,
    'ipa': ipa_spellings_with_audio,
    'audio': audio_files
}

# Write the dataset structure to a csv file
pd.DataFrame(data).to_csv('dataset.csv', index=False) """

# Login to Hugging Face
login()

# Load the dataset from the csv file
dataset = Dataset.from_pandas(pd.read_csv('dataset.csv'))

# Convert the audio column to an Audio feature
dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))

# Push the dataset to Hugging Face
dataset.push_to_hub("VirtualX/eng_ipa_audioset")