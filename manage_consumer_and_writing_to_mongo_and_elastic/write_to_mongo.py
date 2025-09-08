import os
import pymongo
from gridfs import GridFS
from loger.loges_to_a_file import Logger




class MongoWriter:
    def __init__(self):
        self.uri = os.getenv("MONGO_CONN")
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[os.getenv("MONGO_DB")]
        self.gridfs = GridFS(self.db)
        self.loger = Logger.get_logger()

    def insert_event(self,message,hash_id):
        try:
            # print(message)
            if self.gridfs.exists(hash_id):
                return self.gridfs.get(hash_id)
            status = self.gridfs.put(message,_id=hash_id)
            return status
        except Exception as e:
            self.loger.error(f" cent writing to mongo: {e}")