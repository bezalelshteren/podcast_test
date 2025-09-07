import hashlib


class Create_hash:
    def __init__(self):
        self.hash_code = None


    def made_a_hash(self,massage):
        metadata = massage.values()
        combined_string = "_".join(metadata)
        encoded_string = combined_string.encode('utf-8')
        hasher = hashlib.sha256()
        hasher.update(encoded_string)
        self.hash_code = hasher.hexdigest()
        print(self.hash_code)
        return self.hash_code



c = Create_hash()
c.made_a_hash({"cdjshbjbhvhjhsjhb":"h;hb"})

