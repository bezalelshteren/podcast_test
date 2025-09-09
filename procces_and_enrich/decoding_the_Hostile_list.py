import base64


class Decoding_hostile_list:
    @staticmethod
    def decoding(string_words):
        string_decod = base64.b64decode(string_words)
        list_decoding = str(string_decod).split(",")
        return list_decoding


# d = Decoding_hostile_list()
# d.decoding(hostile_list)