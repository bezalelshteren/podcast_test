

class Read_to_bin:

    @staticmethod
    def reader(path):
        with open(path,"rb")as fb:
            content = fb.read()
        return content