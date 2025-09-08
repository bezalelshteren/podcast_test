from producer import Producer
from read_local_files import Read_local_files
from get_metadata import Get_metadata
from pathlib import Path
from dotenv import load_dotenv
from loger.loges_to_a_file import Logger
# loger = Logger.get_logger()
import os


load_dotenv()

topic_name = os.getenv("TOPIC_NAME")
wav_path = Path(os.getenv("PATH_TO_FILES"))

class Manager:
    def __init__(self,path,topic):
        self.loger = Logger.get_logger()
        self.reader = Read_local_files(path)
        self.get_metadata = Get_metadata()
        self.producer = Producer()
        self.topic_name = topic

    def start_all_proces(self):
        try:
            self.loger.info("start all proces to read and send to kafka")
            all_paths = self.reader.read_the_all_paths()
            all_path_and_metadata = self.get_metadata.get_the_metadata(all_paths)

            for massage in all_path_and_metadata:
                self.producer.publish_message(self.topic_name,massage)

            self.loger.info("connect_to_producer")
        except Exception as e:
            self.loger.error(f"not publish")


if __name__ == "__main__":
    manage = Manager(wav_path,topic_name)
    manage.start_all_proces()
    manage.loger.info("Finish all publish")