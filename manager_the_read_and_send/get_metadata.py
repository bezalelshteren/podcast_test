from pathlib import Path
from loger.loges_to_a_file import Logger


ROOT_PATH = Path(__file__).resolve().parent


class Get_metadata:
    def __init__(self):
        self.loger = Logger.get_logger()
        self.list_all_path_and_metadata = []

    def get_wav_metadata(self,own_path):
        try:
            metadata = {
            "file_name" : own_path.name,
            "time_creation":own_path.stat().st_atime_ns,
            "file_size_bytes": own_path.stat().st_size
            }

            return metadata

        except Exception as e:
            self.loger.error(f"Error read wav {own_path} {e}")
            return None


    def get_the_metadata(self,list_of_path):
        try:

            for path in list_of_path:
                json_metadata = {}
                path = Path(path)
                json_metadata["path"] = str(path)
                json_metadata["metadata"] = self.get_wav_metadata(path)
                self.list_all_path_and_metadata.append(json_metadata)

            self.loger.info("get the metadata")
            return self.list_all_path_and_metadata
        except Exception as e:
            self.loger.error(f"the function not return the metadata{e}")



# g = Get_metadata()
# g.get_the_metadata()
# "nchannels": wf.getnchannels(),
# "sampwidth": wf.getsampwidth(),
# "framerate": wf.getframerate(),
# "nframes": wf.getnframes(),
# "comptype": wf.getcomptype(),
# "compname": wf.getcompname(),