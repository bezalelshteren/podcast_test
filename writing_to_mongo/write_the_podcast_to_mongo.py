import os
import pymongo
from gridfs import GridFS
# gridefs

class MongoWriter:
    def __init__(self,col_name):
        self.uri = os.getenv("MONGO_CONN")
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[os.getenv("MONGO_DB")]
        self.col = self.db[os.getenv("COLLECTION_NAME")]

    def insert_event(self,message):
        if isinstance(message,dict):
            doc = message
        else:
            doc = {"value": message.value}
        return self.col.insert_one(doc)


    client = MongoClient('mongodb://localhost:27017/')
    db = client.mydatabase  # Replace 'mydatabase' with your database name
    fs = GridFS(db)

    file_path = 'path/to/your/large_file.txt'  # Replace with your file path
    with open(file_path, 'rb') as f:
        file_id = fs.put(f, filename='large_file.txt', contentType='text/plain')
    print(f"File stored with ID: {file_id}")