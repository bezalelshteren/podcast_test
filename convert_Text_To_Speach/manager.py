from loger.loges_to_a_file import Logger
from convert_to_text_and_send_to_kafka import Send_to_kafka_the_text
from read_kafka_and_write_to_elastic import Read_the_text_from_kafka_and_write_to_elastic
from dotenv import load_dotenv
from pathlib import Path
import os
import time

load_dotenv()


elasticserch_url = os.getenv("ELASTIC_URL","http://localhost:9200")
indices_name = os.getenv("INDEX_NAME")
wav_path = Path(os.getenv("PATH_TO_FILES"))
topic_text = os.getenv("TOPIC_TEXT")

if __name__ == "__main__":
    send_to_kafka = Send_to_kafka_the_text(wav_path)
    send_to_kafka.send_text_from_audio_to_kafka(topic_text)
    time.sleep(20)
    read_kafka_and_write_to_elastic = Read_the_text_from_kafka_and_write_to_elastic(topic_text,"uyhg",elasticserch_url,indices_name)
    read_kafka_and_write_to_elastic.write_the_text_to_elastic()


