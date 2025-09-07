import logging
import wave
import os
from dotenv import load_dotenv
from pathlib import Path
ROOT_PATH = Path(__file__).resolve().parent

load_dotenv()

wav_path = Path(os.getenv("PATH_TO_FILES"))

class Read_local_files:
    def __init__(self,path):
        self.file_path = path
        self.all_data = None

    def read_the_all_paths(self):
        try:
            file_paths = []
            for entry in self.file_path.iterdir():
                if entry.is_file():  # Check if it's a file
                    file_paths.append(str(entry.resolve()))
            logging.info(f"read file paths successfully{file_paths}")
            return file_paths
        except Exception as e:
            logging.error(e)
            raise e

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

# example
# r = Read_local_files(wav_path)
# json_output = r.read_the_all_paths()
# print(json_output)
# metadata = r.get_wav_metadata()
# print(metadata)