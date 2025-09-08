from elasticsearch import Elasticsearch
from loger.loges_to_a_file import Logger


class Crud_elastic:
    def __init__(self, elastic_url,index_name):
        self.es = Elasticsearch(elastic_url)
        self.index_name = index_name
        self.loger = Logger.get_logger()
        self.loger.info(f" connect to elastic{self.es.info}")

    @staticmethod
    def create_mapping(mapping=None):
        if mapping is None:
            mapping = {}

        return mapping

    def create_index(self):
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name)

            mapping = self.es.indices.get_mapping(index=self.index_name)
            return mapping
        except Exception as e:
            self.loger.error(f"not create a index {e}")

    def insert_massage(self,hash_id,metadata_to_insert):
        try:
            document = {"metadata":metadata_to_insert}
            self.es.index(index=self.index_name,id=hash_id,body=document)
            self.loger.info(self.es.count())
        except Exception as e:
            self.loger.error(f"the document is not inserted {e}")
