from loger.loges_to_a_file import Logger
from utils.read_path_to_bin import Read_to_bin
from utils.writing_to_elastic import Crud_elastic
from utils.consumer_from_kafka import Consumer
from utils.create_a_hash_for_the_massages import Create_hash



class Read_the_text_from_kafka_and_write_to_elastic:
    def __init__(self,topic_name,group,elastic_url,index_name):
        self.loger = Logger.get_logger()
        self.read_bin = Read_to_bin()
        self.create_hash = Create_hash()
        self.consumer = Consumer(topic_name,group)
        self.writing_to_elastic = Crud_elastic(elastic_url,index_name)

    def write_the_text_to_elastic(self):
        try:
            for massage in self.consumer.get_consumer_events():
                data = massage.value
                contecst = self.read_bin.reader(data["path"])
                hash_id = self.create_hash.made_a_hash(str(contecst))
                doc_to_apdate = self.writing_to_elastic.search_by_query(hash_id)
                status = self.writing_to_elastic.update_document(hash_id,{"doc":{"text_from_wav":data["massage"]}})
                self.loger.info(f"{status}")
        except Exception as e:
            self.loger.error("didnt work to insert the text to elastic")



# r = Read_the_text_from_kafka_and_write_to_elastic(topic_text,"uyhg",elasticserch_url,indices_name)
# r.write_the_text_to_elastic()