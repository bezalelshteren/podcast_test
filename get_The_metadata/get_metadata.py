import wave
import logging
from reader.read_local_files import Read_local_files
from pathlib import Path
from dotenv import load_dotenv
import os
ROOT_PATH = Path(__file__).resolve().parent

load_dotenv()

wav_path = Path(os.getenv("PATH_TO_FILES"))


class Get_metadata:
    def __init__(self):
        self.reader = Read_local_files(wav_path)
        self.list_of_path = self.reader.read_the_all_paths()
        self.json_metadata = {}

    def get_wav_metadata(self,own_path):
        try:
            with wave.open(str(own_path), 'rb') as wf:
                metadata = {
                "file_name" : own_path.name,
                "file_size_bytes": own_path.stat()
                }
                return metadata
        except wave.Error as e:
            print(f"Error read wav {self.list_of_path}: {e}")
            return None


    def get_the_metadata(self):
        try:
            list_all_path_and_metadata = []
            for path in self.list_of_path:
                path = Path(path)
                self.json_metadata[path] = self.get_wav_metadata(path)
                list_all_path_and_metadata.append(self.json_metadata)
                logging.info(f"the function get metadata {list_all_path_and_metadata}")
        except Exception as e:
            logging.error(f"the function not return the metadata{e}")



g = Get_metadata()
g.get_the_metadata()
# "nchannels": wf.getnchannels(),
# "sampwidth": wf.getsampwidth(),
# "framerate": wf.getframerate(),
# "nframes": wf.getnframes(),
# "comptype": wf.getcomptype(),
# "compname": wf.getcompname(),