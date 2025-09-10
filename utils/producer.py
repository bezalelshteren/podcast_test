from kafka import KafkaProducer
import json

from loger.loges_to_a_file import Logger


class Producer:

    def __init__(self):
        self.loger = Logger.get_logger()
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        self.loger.info(f"connection created {self.producer}")


    def publish_message(self, topic, message):
        self.producer.send(topic, value=message)
        self.producer.flush()


