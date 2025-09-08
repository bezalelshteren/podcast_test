from consumer.consumer_from_kafka import Consumer
from hashcode.create_a_hash_for_the_massages import Create_hash
from writing_to_mongo.write_to_mongo import MongoWriter
from read_path_to_bin import Read_to_bin
from dotenv import load_dotenv
import os
# from loger.loges_to_a_file import logging

load_dotenv()

topic_name = os.getenv("TOPIC_NAME")

class Manage_consumer:
    def __init__(self,topic):
        self.consumer = Consumer(topic,"aimjiiiii")
        self.create_hash = Create_hash()
        self.write_to_mongo = MongoWriter()
        self.reader = Read_to_bin()

    def send_the_data_to_mongo_and_the_metadata_to_elastic(self):
        for podcaste in self.consumer.get_consumer_events():
            print(podcaste)
            print(podcaste.value)
            data = podcaste.value






manage = Manage_consumer(topic_name)
manage.send_the_data_to_mongo_and_the_metadata_to_elastic()