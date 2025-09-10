import speech_recognition as sr
from loger.loges_to_a_file import Logger


path_file = r"C:\Users\User\Downloads\podcasts\podcasts\download (1).wav"


class Speach_to_text:
    def __init__(self):
        self.loger = Logger.get_logger()
        self.recognizer = sr.Recognizer()
        self.text = None

    def try_to_read(self,path):
        try:
            with sr.AudioFile(path) as audio_file:
                audio = self.recognizer.record(audio_file)
            self.text = self.recognizer.recognize_google(audio)
            self.loger.info(f"this is the texst of the wav file :{self.text}")
            return self.text
        except Exception as e:
            self.loger.error("connet convert rom speach to text")
            return None


# s= Speach_to_text(path_file)
# s.try_to_read()