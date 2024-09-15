import os
import requests
import threading
import uuid
import typing

from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from api_error import ApiError
from elevenlabs.client import ElevenLabs

class AudioGenerator:
    """
    A class used to generate audio files from text input using the ElevenLabs API.
    """

    def __init__(self, input_file, key):
        """
        Initializes the AudioGenerator object with an input file and API key.

        Args:
            input_file (str): The path to the input file containing text to be converted to audio.
            key (str): The ElevenLabs API key.
        """
        self.client = ElevenLabs(api_key=key)  # Initialize the ElevenLabs client with the API key
        self.input_file = input_file  # Store the input file path
        self.cancelled = False  # Flag to track if the process has been cancelled
        self.error_count = 0  # Counter for errors encountered during audio generation
        self.successfully_converted = self.read_successfully_converted()  # Read previously successfully converted words

    def read_words(self):
        """
        Reads the input file and returns a list of words to be converted to audio.

        Returns:
            list: A list of words to be converted to audio.
        """
        with open(self.input_file, 'r') as f:  # Open the input file in read mode
            return [line.strip() for line in f.readlines()]  # Read and strip each line, returning a list of words

    def read_successfully_converted(self):
        """
        Reads a file containing previously successfully converted words and returns them as a list.

        Returns:
            list: A list of previously successfully converted words.
        """
        try:
            with open('successfully_converted.txt', 'r') as f:  # Open the file containing successfully converted words
                return [line.strip() for line in f.readlines()]  # Read and strip each line, returning a list of words
        except FileNotFoundError:  # Handle the case where the file does not exist
            return []  # Return an empty list if the file does not exist

    def write_successfully_converted(self, word):
        """
        Writes a successfully converted word to the file.

        Args:
            word (str): The word to be written to the file.
        """
        with open('successfully_converted.txt', 'r+') as f:  # Open the file in read and write mode
            lines = f.readlines()  # Read the existing lines in the file
            if lines and not lines[-1].endswith('\n'):  # Check if the last line does not end with a newline
                f.write('\n')  # Add a newline if necessary
            f.write(word + '\n')  # Write the word to the file

    def generate_audio(self, word):
        """
        Uses the ElevenLabs API to generate audio data for a given word.

        Args:
            word (str): The word to be converted to audio.

        Returns:
            bytes: The generated audio data.
        """
        response = self.client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=word,
            model_id="eleven_turbo_v2",  # Use the turbo model for low latency
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            )
        )
        audio_data = b''  # Initialize an empty bytes object to store the audio data
        for chunk in response:  # Iterate over the response chunks
            audio_data += chunk  # Append each chunk to the audio data

        if audio_data:  # Check if audio data was generated
            print("Audio data generated successfully")  # Print a success message
            return audio_data  # Return the generated audio data
        else:
            self.error_count += 1  # Increment the error counter
            print(f"Error generating audio file for {word}")  # Print an error message
            return None  # Return None to indicate an error

    def run(self):
        """
        Runs the audio generation process, reading words from the input file, generating audio, and writing successfully converted words to the file.

        Returns:
            list: A list of tuples containing the word and generated audio data.
        """
        words = self.read_words()  # Read the words from the input file
        audio_data_list = []  # Initialize an empty list to store the generated audio data
        success_count = 0  # Initialize a counter for successfully generated audio
        successfully_converted_words = set(self.successfully_converted)  # Create a set of previously successfully converted words

        for word in words:  # Iterate over the words
            if self.cancelled:  # Check if the process has been cancelled
                print("Cancelled by user")  # Print a cancellation message
                break  # Exit the loop

            if word in successfully_converted_words:  # Check if the word has already been successfully converted
                continue  # Skip to the next word

            try:
                audio_data = self.generate_audio(word)  # Generate audio for the word
            except ApiError as e:  # Handle API errors
                print(f"API Error: {e}")  # Print an error message
                print("Terminating due to API error")  # Print a termination message
                break  # Exit the loop

            if audio_data is not None:  # Check if audio data was generated
                audio_data_list.append((word, audio_data))  # Append the word and audio data to the list
                success_count += 1  # Increment the success counter
                successfully_converted_words.add(word)  # Add the word to the set of successfully converted words
                self.write_successfully_converted(word)  # Write the word to the file

                if success_count >= 100:  # Check if 100 words have been successfully converted
                    break  # Exit the loop

            if self.error_count >= 2:  # Check if 2 or more errors have occurred
                print("Terminating due to 2 or more consecutive errors")  # Print a termination message
                break  # Exit the loop

        return audio_data_list  # Return the list of generated audio data


def cancel_script(generator):
    input("Press Enter to cancel...")
    generator.cancelled = True


if __name__ == '__main__':
    api_key = "you_api_key"
    audio_generator = AudioGenerator('just_english.txt', api_key)
    cancel_thread = threading.Thread(target=cancel_script, args=(audio_generator,))
    cancel_thread.start()
    audio_data_list = audio_generator.run()
    output_dir = "assets"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for word, audio_data in audio_data_list:
        filename = f"{word}.wav"
        with open(os.path.join(output_dir, filename), 'wb') as f:
            f.write(audio_data)
        print(f"Generated audio file for {word}")