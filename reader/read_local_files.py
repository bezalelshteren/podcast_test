import logging
import wave
# import scipy.io.wavfile as wav
import soundfile as sf
import json
import os
from dotenv import load_dotenv
import numpy as np
from pathlib import Path
ROOT_PATH = Path(__file__).resolve().parent

load_dotenv()

wav_path = os.getenv("PATH_TO_FILES")

class Read_local_files:
    def __init__(self,path):
        self.file_path = path
        self.all_data = None


    def read_wav_to_json(self):
        data, samplerate = sf.read(self.file_path)

        audio_data_list = data.tolist()
        num_channels = 1

        wav_info = {
            "samplerate": samplerate,
            "channels": num_channels,
            "audio_data": audio_data_list
        }
        return json.dumps(wav_info, indent=4)

    def get_wav_metadata(self):

        try:
            with wave.open(str(self.file_path), 'rb') as wf:
                metadata = {
                    "nchannels": wf.getnchannels(),
                    "sampwidth": wf.getsampwidth(),
                    "framerate": wf.getframerate(),
                    "nframes": wf.getnframes(),
                    "comptype": wf.getcomptype(),
                    "compname": wf.getcompname()
                }
                return metadata
        except wave.Error as e:
            print(f"Error reading WAV file {self.file_path}: {e}")
            return None

# Example usage:
r = Read_local_files(path=wav_path)
json_output = r.read_wav_to_json()
print(json_output)
metadata = r.get_wav_metadata()
print(metadata)