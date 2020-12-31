from nlp import NLP
import speech_recognition as sr
import time
import numpy as np

nlp = NLP()
print("Created instance of NLP")
# nlp.retrain_model()
# print("Retrained model")
start = time.time()
result = nlp.predict_class("Calculate the circumference of the earth")
end = time.time()
print(result)
print(end - start)

result = nlp.predict_class("Start study mode")
print(result)

result = nlp.predict_class("Open up your documentation")
print(result)

result = nlp.predict_class("Start a new text file")
print(result)

result = nlp.predict_class("What is four squared?")
print(result)

try:
    print(result[0])
except:
    print('cannot access at 0-th index')

try:
    print('Intent: ', result[0]['intent'])
except:
    print('cannot access intent')
# r = sr.Recognizer()
# mic = sr.Microphone()
# print(sr.Microphone.list_microphone_names())

# query = ""
# with mic as source:
#     r.adjust_for_ambient_noise(source, duration=0.5)
#     print("Listening...")
#     audio = r.listen(source)
#     query = r.recognize_google(audio)
#     print(query)

# result = nlp.predict_class(query)
# print(result)

