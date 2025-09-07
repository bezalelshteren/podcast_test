import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch,helpers
from elasticsearch.helpers import scan
from loger.loges_to_a_file import logging
load_dotenv()


indices_name = os.getenv("INDEX_NAME")


class Crud_elastic:
    def __init__(self, elastic_url):
        self.es = Elasticsearch(elastic_url)
        self.index_name = indices_name

    @staticmethod
    def create_mapping(mapping=None):
        if mapping is None:
            mapping = {}

        return mapping

    def create_index(self):
        try:
            if self.es.indices.exists(index=self.index_name):
                self.es.indices.delete(index=self.index_name)
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name,mappings=self.create_mapping())

            mapping = self.es.indices.get_mapping(index=self.index_name)
            print(mapping)
            return mapping
        except Exception as e:
            raise e

    def insert_all(self,list_of_podcast):
        try:

            insert_one = [{"_index": self.index_name,"_id": myhash,"_source":podcast}
            for myhash ,podcast in enumerate(list_of_podcast)]

            helpers.bulk(self.es,insert_one )
            self.es.indices.refresh(index=self.index_name)
            return self.es.count()
        except Exception as e:
            raise e
