**README**
===============

**Database Generation**
--------------------

To generate the database, follow these steps:

1. Run `dict_extraction.py` to extract the English spellings and IPA spellings from `dict.tsv` and create
    * A smaller dictionary `small_dictionary.txt`,
    * A `dictionary.pls` document used tie the pronunciation of english words to their IPA counterpart. It is used by elevenlabs,
    * A full dictionary of all english words `just_english.txt`.

**Audio File Generation**
----------------------

To generate audio files, follow these steps:

1. Install the required dependencies:
	* `ffmpeg`
	* `elevenlabs`
	* `dotenv`
2. Run `audio_generator.py` to generate audio files for each word in
    * The `small_dictionary.txt` file, or
    * The `just_english.txt` file
3. When generating from the audio files from `small_dictionary.txt`, they will be saved in the `assets_small` directory.
4. When generating from the audio files from `just_english.txt`, they will be saved in the `assets` directory.
5. To utlize the eleven labs api, add your elevenlabs api key as `api_key` = your_api_key under the main() section of `audio_generator.py`

**Audio File Formatting**
----------------------

The audio files must be formatted in `.wav` format, sampled at 16 kHz, and 16-bit array.
**Pushing to Hugging Face**
-------------------------

To push the dataset to Hugging Face, follow these steps:

1. Install the required dependencies:
	* `huggingface_hub`
	* `datasets`
2. Run `build_dataset.py` to 
    * Create a dataset object.
    * Push to huggingface via the `huggingface_hub` library


**Required Dependencies**
-----------------------

* `pandas`
* `ffmpeg`
* `elevenlabs`
* `dotenv`
* `huggingface_hub`
* `datasets`

**Code Structure**
-----------------

The code is structured as follows:

* `dict_extraction.py`: extracts English spellings and IPA spellings from `dict.tsv` and creates a dictionary.
* `build_dataset.py`: creates a dictionary of IPA spellings and English spellings, and generates a dataset object.
* `audio_generator.py`: generates audio files for each word in the dictionary.