import hashlib
# from loger.loges_to_a_file import Logger
# loger = Logger.get_logger()


class Create_hash:
    def __init__(self):
        self.hash_code = None


    def made_a_hash(self,massage):
        # combined_string = "_".join(massage)
        encoded_string = massage.encode('utf-8')
        hasher = hashlib.sha256()
        hasher.update(encoded_string)
        self.hash_code = hasher.hexdigest()
        return self.hash_code


