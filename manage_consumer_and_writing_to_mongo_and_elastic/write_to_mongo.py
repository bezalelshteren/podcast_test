import os
import pymongo
from gridfs import GridFS
# from loger.loges_to_a_file import Logger
# loger = Logger.get_logger()



class MongoWriter:
    def __init__(self):
        self.uri = os.getenv("MONGO_CONN")
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[os.getenv("MONGO_DB")]
        self.gridfs = GridFS(self.db)

    def insert_event(self,message,hash_id):
        if self.gridfs.exists(hash_id):
            return self.gridfs.get(hash_id)
        status = self.gridfs.put(message,_id=hash_id)
        return status








    #
    # client = MongoClient('mongodb://localhost:27017/')
    # db = client.mydatabase  # Replace 'mydatabase' with your database name
    # fs = GridFS(db)
    #
    # file_path = 'path/to/your/large_file.txt'  # Replace with your file path
    # with open(file_path, 'rb') as f:
    #     file_id = fs.put(f, filename='large_file.txt', contentType='text/plain')
    # print(f"File stored with ID: {file_id}")