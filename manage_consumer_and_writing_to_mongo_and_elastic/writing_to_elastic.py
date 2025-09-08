from elasticsearch import Elasticsearch
# from loger.loges_to_a_file import Logger
# loger = Logger.get_logger()



class Crud_elastic:
    def __init__(self, elastic_url,index_name):
        self.es = Elasticsearch(elastic_url)
        self.index_name = index_name
        print(self.es.info)

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
            raise e

    def insert_massage(self,hash_id,metadata_to_insert):
        try:
            document = {"metadata":metadata_to_insert}
            is_inserted = self.es.index(index=self.index_name,id=hash_id,body=document)
            self.es.indices.refresh(index=self.index_name)
            print(is_inserted)
            return self.es.count()
        except Exception as e:
            print()
            # loger.error(f"the document is not inserted {e}")
