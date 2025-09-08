

class Read_to_bin:
    def __init__(self):
        self.content = None

    def reader(self,path):
        with open(path,"rb")as fb:
            self.content = fb.read()
        return self.content