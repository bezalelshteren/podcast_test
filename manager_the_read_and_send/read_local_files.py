from loger.loges_to_a_file import Logger
import os
from dotenv import load_dotenv
from pathlib import Path
ROOT_PATH = Path(__file__).resolve().parent

load_dotenv()

wav_path = Path(os.getenv("PATH_TO_FILES"))

class Read_local_files:
    def __init__(self,path):
        self.loger = Logger.get_logger()
        self.file_path = path
        self.all_data = None

    def read_the_all_paths(self):
        try:
            file_paths = []
            for entry in self.file_path.iterdir():
                if entry.is_file():
                    file_paths.append(str(entry.resolve()))
            self.loger.info(f"read file paths successfully{file_paths}")

            return file_paths
        except Exception as e:
            self.loger.error(f"read the files didnt work: {e}")
