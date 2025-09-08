from consumer.consumer_from_kafka import Consumer
from hashcode.create_a_hash_for_the_massages import Create_hash
from writing_to_mongo.write_to_mongo import MongoWriter
from write_to_ekasticserch.writing_to_elastic import Crud_elastic
from read_path_to_bin import Read_to_bin
from dotenv import load_dotenv
import os
# from loger.loges_to_a_file import Logger
# loger = Logger.get_logger()

load_dotenv()

topic_name = os.getenv("TOPIC_NAME")
group = os.getenv("GROUP_NAME")
indices_name = os.getenv("INDEX_NAME")
elasticserch_url = os.getenv("ELASTIC_URL","http://localhost:9200")

class Manage_consumer:
    def __init__(self,topic,group_name,elast_url,name_index):
        self.consumer = Consumer(topic,group_name)
        self.create_hash = Create_hash()
        self.write_to_mongo = MongoWriter()
        self.reader = Read_to_bin()
        self.write_to_elastic = Crud_elastic(elast_url,name_index)
        self.write_to_elastic.create_index()

    def send_the_data_to_mongo_and_the_metadata_to_elastic(self):
        for podcaste in self.consumer.get_consumer_events():
            data = podcaste.value
            content = self.reader.reader(data["path"])
            hash_to_id = self.create_hash.made_a_hash(str(content))
            print(hash_to_id)
            print(type(hash_to_id))
            status = self.write_to_mongo.insert_event(content,hash_to_id)
            is_insert = self.write_to_elastic.insert_massage(hash_to_id,data["metadata"])
            print(status)
            print(is_insert)


if __name__ == "__main__":
    manage = Manage_consumer(topic_name,group,elasticserch_url,indices_name)
    manage.send_the_data_to_mongo_and_the_metadata_to_elastic()