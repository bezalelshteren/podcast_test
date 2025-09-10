import os
import pymongo
from gridfs import GridFS, GridFSBucket
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

    def connect_and_read(self):
        fs = GridFSBucket(self.db)

        for file_document in fs.find({}):
            print(file_document._id)
        return fs
        # return self.gridfs.get()
        # my_db = self.client[self.db_name]
        # my_coll = my_db[self.collection_name]
        # data = my_coll.find()
        #


# m = MongoWriter()
# m.connect_and_read()
