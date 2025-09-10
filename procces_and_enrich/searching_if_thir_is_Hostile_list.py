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
        score_of_less_hostile_words = {}
        score_of_hostile_words = {}

    def search_words(self):
        for word in self.list_hostile_words_to_check:
            query_body = {"query":{"match_phrase":{"content":word}}}
            e = self.elastic.search_by_multy_query(query_body)
            print(e)


    def get_all_docs_from_elastic(self):
        all_docs = self.elastic.get_all_doc()
        print(all_docs)
        return all_docs

    def check_the_score_in_every_doc(self,list_hostile_words,doc,list_of_score):
            text = doc["_source"]["text_from_wav"]
            length = len(text)
            the_words_we_find = {}
            for word in list_hostile_words:
                if word in text:
                    if word in the_words_we_find:
                        the_words_we_find[word] +=1
                    else:
                        the_words_we_find[word] = 1
                else:
                    the_words_we_find[word] = 0
                the_words_we_find[word] = the_words_we_find[word]/length
                if not list_of_score[word]:
                    list_of_score[word] = 0
                list_of_score[word] += the_words_we_find[word]
            return the_words_we_find


    def insert_the_new_fields(self):
        if_thir_is_a_word = False
        score = 0
        score_of_all_docs = {}
        all_docs = self.get_all_docs_from_elastic()
        for doc in all_docs:
            score_of_doc = self.check_the_score_in_every_doc(self.list_hostile_words_to_check,doc,self.list_hostile_words_to_check)
            if len(score_of_doc.keys()) > 0:
                if_thir_is_a_word = True
            for word, score_docs in score_of_doc.items():
                if word in score_of_all_docs:
                    score_of_all_docs[word] += score_docs
                score += score_docs * score_of_all_docs[word]

search = Searching_in_elastic(elasticserch_url,indices_name)
# search.search_words()
# search.search_words_in_doc(search.list_hostile_words_to_check,)
search.get_all_docs_from_elastic()