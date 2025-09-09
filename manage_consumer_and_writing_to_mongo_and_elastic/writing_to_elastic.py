from elasticsearch import Elasticsearch,helpers
from elasticsearch.helpers import scan
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

    def search_by_query(self,query=None):
        # try:
            # resp = self.es.get(index="test-index", id=1)
            # print(resp['_source'])
            # all_documents = None
            # all_documents = self.es.search(index=self.index_name, query=query)
            # if all_documents is None:
            all_documents = [hit  for hit in scan(self.es, query={"query":{"match_all":{}}},_source=True, index=self.index_name)]

            return all_documents
        # except Exception as e:
        #     self.loger.error(f"{query} not return a document")

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
            self.loger.info(f"{res_update} is updated")
            return f"{res_update} is updated"
        except Exception as e:
            self.loger.error(f"{update_doc} is not updated")


