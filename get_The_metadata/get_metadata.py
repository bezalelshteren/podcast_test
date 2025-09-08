import wave
from pathlib import Path
from loger.loges_to_a_file import Logger
# loger = Logger.get_logger()

ROOT_PATH = Path(__file__).resolve().parent


class Get_metadata:
    def __init__(self):
        self.list_all_path_and_metadata = []

    def get_wav_metadata(self,own_path):
        try:
            with wave.open(str(own_path), 'rb') as wf:
                metadata = {
                "file_name" : own_path.name,
                "file_size_bytes": own_path.stat().st_size
                }
                return metadata
        except wave.Error as e:
            print(f"Error read wav {own_path}: {e}")
            return None


    def get_the_metadata(self,list_of_path):
        try:

            for path in list_of_path:
                json_metadata = {}
                path = Path(path)
                json_metadata["path"] = str(path)
                json_metadata["metadata"] = self.get_wav_metadata(path)
                self.list_all_path_and_metadata.append(json_metadata)
                logging.info(f"the function get metadata {self.list_all_path_and_metadata}")

            print("get the metadata")
            return self.list_all_path_and_metadata
        except Exception as e:
            logging.error(f"the function not return the metadata{e}")



# g = Get_metadata()
# g.get_the_metadata()
# "nchannels": wf.getnchannels(),
# "sampwidth": wf.getsampwidth(),
# "framerate": wf.getframerate(),
# "nframes": wf.getnframes(),
# "comptype": wf.getcomptype(),
# "compname": wf.getcompname(),