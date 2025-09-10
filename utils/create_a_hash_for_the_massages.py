import hashlib
from loger.loges_to_a_file import Logger



class Create_hash:
    def __init__(self):
        self.hash_code = None
        self.loger = Logger.get_logger()


    def made_a_hash(self,massage):
        try:
            combined_string = "".join(massage)
            encoded_string = combined_string.encode('utf-8')
            hasher = hashlib.sha256()
            hasher.update(encoded_string)
            self.hash_code = hasher.hexdigest()
            # self.loger.info("{self.hash_code}this the has code for{massage} ")
            return self.hash_code

        except Exception as e:
            self.loger.error(f"connet create hash {e}")
