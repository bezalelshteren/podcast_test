from pyaudio import PyAudio


path = r"C:\Users\User\Downloads\podcasts\podcasts\download (1).wav"

import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
# from os import path


audio = sr.AudioData.from_file(path)



r = sr.Recognizer()
# harvard = sr.AudioFile(path)
# with harvard as source:
#     audio = r.record(source)
jackhammer = sr.AudioFile(path)
# with jackhammer as source:
#     audio = r.record(source)
print(str(audio))