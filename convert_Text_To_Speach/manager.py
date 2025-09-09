from loger.loges_to_a_file import Logger
from convert_to_speach import Speach_to_text
from manager_the_read_and_send.producer import Producer
from manage_consumer_and_writing_to_mongo_and_elastic.read_path_to_bin import Read_to_bin
from manager_the_read_and_send.read_local_files import Read_local_files
from manage_consumer_and_writing_to_mongo_and_elastic.writing_to_elastic import Crud_elastic
from manage_consumer_and_writing_to_mongo_and_elastic.consumer_from_kafka import Consumer
from manage_consumer_and_writing_to_mongo_and_elastic.create_a_hash_for_the_massages import Create_hash
from dotenv import load_dotenv
from pathlib import  Path
import time
import os

load_dotenv()

elasticserch_url = os.getenv("ELASTIC_URL","http://localhost:9200")
indices_name = os.getenv("INDEX_NAME")
wav_path = Path(os.getenv("PATH_TO_FILES"))
topic_text = os.getenv("TOPIC_TEXT")

class Send_to_kafka_the_text:
    def __init__(self,path):
        self.loger = Logger.get_logger()
        self.read_the_files = Read_local_files(path)
        self.stt = Speach_to_text()
        self.producer = Producer()

    def send_text_from_audio_to_kafka(self,topic_name):
        try:
            all_path = self.read_the_files.read_the_all_paths()
            for path in all_path:
                text_from_wav = self.stt.try_to_read(path)
                massage = {"path":path,"massage":text_from_wav}
                self.producer.publish_message(topic_name,massage)
                break
        except Exception as e:
            self.loger.error("canot insert the text to elastic")


class Read_the_text_from_kafka_and_write_to_elastic:
    def __init__(self,topic_name,group,elastic_url,index_name):
        self.loger = Logger.get_logger()
        self.read_bin = Read_to_bin()
        self.create_hash = Create_hash()
        self.consumer = Consumer(topic_name,group)
        self.writing_to_elastic = Crud_elastic(elastic_url,index_name)

    def write_the_text_to_elastic(self):
        # try:
            for massage in self.consumer.get_consumer_events():
                data = massage.value
                contecst = self.read_bin.reader(data["path"])
                print(data["path"])
                hash_id = self.create_hash.made_a_hash(str(contecst))
                print(hash_id)
                doc_to_apdate = self.writing_to_elastic.search_by_query({"match":{"id":hash_id}})
                # status = self.writing_to_elastic.update_document(hash,doc_to_apdate)
                for doc in doc_to_apdate:
                    if doc == hash_id:
                        print(doc)
                    else:
                        print("=============================================================")
                print(doc_to_apdate)
                # print(status)
        # except Exception as e:
        #     self.loger.error("didnt work to insert the text to elastic")


s = Send_to_kafka_the_text(wav_path)
s.send_text_from_audio_to_kafka(topic_text)

# time.sleep(5)
r = Read_the_text_from_kafka_and_write_to_elastic(topic_text,"uhg",elasticserch_url,indices_name)
r.write_the_text_to_elastic()