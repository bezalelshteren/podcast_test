from kafka import KafkaProducer
import json


class Producer:

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        print(self.producer)

# producer send message
    def publish_message(self, topic, message):
        print("connect")
        self.producer.send(topic, value=message)
        self.producer.flush()
        print("publish the massage")


# p = Producer()
# p.publish_message("huihui","huix")