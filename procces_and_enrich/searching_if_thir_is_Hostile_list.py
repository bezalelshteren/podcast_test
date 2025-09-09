from manage_consumer_and_writing_to_mongo_and_elastic.writing_to_elastic import Crud_elastic
from loger.loges_to_a_file import Logger
from procces_and_enrich.decoding_the_Hostile_list import Decoding_hostile_list
from manager_the_read_and_send.producer import Producer
from dotenv import load_dotenv
import os

load_dotenv()

hostile_list = os.getenv("HOSTILE_LIST")
less_hostile_list = os.getenv("LASS_HOSTILE_LIST")
indices_name = os.getenv("INDEX_NAME")
elasticserch_url = os.getenv("ELASTIC_URL","http://localhost:9200")


class Searching_in_elastic:
    def __init__(self,elastic_url,index_name):
        self.producer = Producer()
        self.decoder = Decoding_hostile_list()
        self.elastic = Crud_elastic(elastic_url,index_name)
        self.loger = Logger.get_logger()
        self.list_hostile_words_to_check = self.decoder.decoding(hostile_list)
        self.list_less_hostile_words_to_check = self.decoder.decoding(less_hostile_list)

    def search_words(self,doc_id):
        for word in self.list_hostile_words_to_check:
            query_body = {"query": {"bool": {"filter": [{
                "term": {"_id": doc_id}}],"must": [
                {"match": {"text_from_wav": word}}]}}}
            e = self.elastic.search_by_multy_query(query_body)
            print(e)


# search = Searching_in_elastic(elasticserch_url,indices_name)
# search.search_words()