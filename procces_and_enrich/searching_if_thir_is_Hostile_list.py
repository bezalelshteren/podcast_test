from utils.writing_to_elastic import Crud_elastic
from loger.loges_to_a_file import Logger
from procces_and_enrich.decoding_the_Hostile_list import Decoding_hostile_list
from utils.producer import Producer
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
        self.score_of_all_docs = 0

    def check_the_score_in_every_doc(self,list_hostile_words,text):
            the_score_of_this_doc = 0
            length = len(text)
            the_num_words_we_find = 0
            for word in list_hostile_words:
                if word in text:
                    the_num_words_we_find +=1
                the_score_of_this_doc = the_num_words_we_find / length
            self.loger.info("check_the_score_in_every_doc")
            return the_score_of_this_doc


    def calculate_all_scores(self):
        for doc in self.elastic.get_all_doc():
            score_of_doc = self.check_the_score_in_every_doc(self.list_hostile_words_to_check,doc["text_from_wav"])
            score_of_doc += self.check_the_score_in_every_doc(self.list_less_hostile_words_to_check,doc)/2
            self.score_of_all_docs += score_of_doc
        self.loger.info(f"this is the score of all docs calculate together{self.score_of_all_docs}")
        return self.score_of_all_docs

    def divides_the_score_by_proficiency_level(self,score_of_doc):
            cat_to_risk = self.score_of_all_docs /4
            self.loger.info("divides_the_score_by_proficiency_level")
            if score_of_doc > cat_to_risk * 3:
                return "high_risk",score_of_doc
            elif score_of_doc > cat_to_risk * 2:
                return "medium_risk",score_of_doc
            elif score_of_doc > cat_to_risk * 1:
                return "low_risk",score_of_doc
            else:
                return None,score_of_doc


    def insert_new_fields(self):
        try:
            for doc in self.elastic.get_all_doc():
                doc_id = doc["_id"]
                doc_text = doc["_source"]["text_from_wav"]
                is_bds = True
                score_of_doc = self.check_the_score_in_every_doc(self.list_hostile_words_to_check, doc_text)
                score_of_doc += self.check_the_score_in_every_doc(self.list_less_hostile_words_to_check, doc_text) / 2
                bds_threat_level, bds_percent= self.divides_the_score_by_proficiency_level(score_of_doc)
                if bds_threat_level is None:
                    is_bds = False
                field_to_insert = {"doc":{"is_bds":is_bds,"bds_threat_level":bds_threat_level,"bds_percent":bds_percent}}
                status = self.elastic.update_document(doc_id,field_to_insert)
                self.loger.info(f"the score and risk is updated :{status} ")
        except Exception as e:
            self.loger.error("the new field in elastic is not updated")

if __name__ == "__main__":
    search = Searching_in_elastic(elasticserch_url,indices_name)
    search.insert_new_fields()

