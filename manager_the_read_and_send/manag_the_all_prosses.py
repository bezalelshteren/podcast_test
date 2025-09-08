from manager_the_read_and_send.producer import Producer
from manager_the_read_and_send.read_local_files import Read_local_files
from manager_the_read_and_send.get_metadata import Get_metadata
from pathlib import Path
from dotenv import load_dotenv
# loger = Logger.get_logger()
import os


load_dotenv()

topic_name = os.getenv("TOPIC_NAME")
wav_path = Path(os.getenv("PATH_TO_FILES"))

class Manager:
    def __init__(self,path,topic):
        self.reader = Read_local_files(path)
        self.get_metadata = Get_metadata()
        self.producer = Producer()
        self.topic_name = topic

    def start_all_proces(self):
        try:
            print("start all proces")
            all_paths = self.reader.read_the_all_paths()
            all_path_and_metadata = self.get_metadata.get_the_metadata(all_paths)

            for massage in all_path_and_metadata:
                self.producer.publish_message(self.topic_name,massage)
                print(f"publish {massage}")
                # logging.info(f"publish {massage}")
            print("Finish all publish")
            # logging.info("connect_to_producer")
        except Exception as e:
            # logging.error(f"not publish")
            print()

manage = Manager(wav_path,topic_name)
manage.start_all_proces()


# def start_all_proces(self):
#     try:
#         mass = []
#         print("start all proces")
#         all_paths = self.reader.read_the_all_paths()
#         all_path_and_metadata = self.get_metadata.get_the_metadata(all_paths)
#         # print(all_path_and_metadata)
#         for massage in all_path_and_metadata:
#             for key, value in massage.items():
#                 mass.append(key)
#                 mass.append(value)
#                 # self.producer.publish_message(self.topic_name,mass)
#                 # logging.info(f"publish {massage}")
#                 print(mass)
#             break
#         print("Finish all publish")
#         logging.info("connect_to_producer")
#     except Exception as e:
#         logging.error(f"not publish")