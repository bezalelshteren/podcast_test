from elasticsearch import Elasticsearch,helpers
from elasticsearch.helpers import scan
from loger.loges_to_a_file import Logger
import os
from dotenv import load_dotenv

load_dotenv()

class Crud_elastic:
    def __init__(self, elastic_url,index_name):
        self.es = Elasticsearch(elastic_url)
        self.index_name = index_name
        self.loger = Logger.get_logger()
        self.loger.info(f" connect to elastic{self.es.info}")

    @staticmethod
    def create_mapping(mapping=None):
        if mapping is None:
            mapping = {
                "properties": {
                "size": {"type": "keyword"},
                "CreateDate": {"type": "keyword"},
                "name": {"type": "keyword"},
                "text": {"type": "text",
                "fields": {"raw": {"type": "keyword"}}}
                    }}

        return mapping

    def create_index(self):
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name)

            mapping = self.es.indices.get_mapping(index=self.index_name)
            return mapping
        except Exception as e:
            self.loger.error(f"not create a index {e}")

    def search_by_query(self,document_id):
        try:
            response = self.es.get(index=self.index_name, id=document_id)
            if response["found"]:
                self.loger.info(f"{response["found"]} is the doc whet we need to update")
                return response
            else:
                self.loger.error(f"{document_id} not return a document")
                return None
        except Exception as e:
            self.loger.error(f"{document_id} not return a document")

    def insert_massage(self,hash_id,metadata_to_insert):
        try:
            document = {"metadata":metadata_to_insert}
            self.es.index(index=self.index_name,id=hash_id,body=document)
            self.loger.info(self.es.count())
        except Exception as e:
            self.loger.error(f"the document is not inserted {e}")


    def update_document(self,doc_id,update_doc):
        try:
            res_update = self.es.update(index=self.index_name, id=doc_id, body=update_doc)
            return f"{res_update} is updated"
        except Exception as e:
            self.loger.error(f"{update_doc} is not updated")

