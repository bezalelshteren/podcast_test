from kafka import KafkaConsumer
from dotenv import load_dotenv
import os
import json
from loger.loges_to_a_file import Logger


load_dotenv()

topic_name = os.getenv("TOPIC_NAME")


class Consumer:
    def __init__(self,topic,group):
        self.loger = Logger.get_logger()
        self.topic = topic
        self.group = group


    def get_consumer_events(self):
        consumer = KafkaConsumer(
            self.topic ,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            group_id= self.group
        )
        self.loger.info("the consumer worked")
        return consumer
