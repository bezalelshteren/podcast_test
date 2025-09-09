from loger.loges_to_a_file import Logger
from convert_to_speach import Speach_to_text
from manager_the_read_and_send.producer import Producer
from manager_the_read_and_send.read_local_files import Read_local_files



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
        except Exception as e:
            self.loger.error("canot insert the text to elastic")


# s = Send_to_kafka_the_text(wav_path)
# s.send_text_from_audio_to_kafka(topic_text)