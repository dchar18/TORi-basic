import speech_recognition as sr     # records audio and turns it into text
from gtts import gTTS               # converts text to speech - allows program to respond
# requires internet
import os
import subprocess
# import random
# import cv2

# libraries for Google searches
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# libraries for application launch
# from elasticsearch import Elasticsearch
# from elasticsearch.helpers import bulk
#
# es = Elasticsearch(['localhost:9200'])
# bulk(es, records, index='voice_assistant', doc_type='text', raise_on_error=True)


def greeting(verified):
    if verified:
        say("Hello Damian, how may I assist you?")
        return verified
    else:
        say("Hello. Authentication please")
        verified = facial_recognition()
        print("Verified")
        greeting(verified)
    return verified


def facial_recognition():  # TODO
    return True


def speak(phrase):  # vocal response - slower/unused
    myobj = gTTS(text=phrase, lang='en', slow=False)
    myobj.save("speak.mp3")
    os.system("mpg321 speak.mp3")
    print("TORi: " + phrase)


def say(text):  # vocal response - faster generation of speech
    subprocess.call(['say', text])
    print("TORi: " + text)


def activate(phrase='hey tori'):  # currently unused
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.75)
        audio = r.listen(source)
        transcript = r.recognize_google(audio)
        if transcript.lower() == phrase:
            return True
        else:
            return False


def command():  # receive command
    r = sr.Recognizer()
    microphone = sr.Microphone(chunk_size=1024)

    with microphone as source:
        r.adjust_for_ambient_noise(source, duration=0.75)
        print("Speak now")
        r.pause_threshold = 1  # may need to adjust - TEST
        audio = r.listen(source)

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        transcription = r.recognize_google(audio)
        return transcription
    except sr.RequestError:
        # API was unreachable or unresponsive
        return "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        return "Unintelligible speech"
    # return "No command received"


# def response():
#     # text_response = 'Hello. Authentication please'
#     # text_response = 'Good morning, Damian. What would you like me to do?'
#     responses = ("Hello", "Good morning Damian. How are you doing today?",
#                  "Good afternoon Damian. How are you doing today?",
#                  "Good evening Damian. How are you doing today?",
#                  "Hello. Authentication please")
#     # text_response = random.choice(responses)

#     if command_received == "facial":
#         text_response = "Initializing facial recognition"
#     else:
#         text_response = responses[4]

#     speak(text_response)


# def search_es(query):
#     res = es.search(index="voice_assistant", doc_type="text", body={
#         "query": {
#             "match": {
#                 "voice_command": {
#                     "query": query,
#                     "fuzziness": 2
#                 }
#             }
#         },
#     })
#     return res['hits']['hits'][0]['_source']['sys_command']


# def store_apps():
#     d = '/Applications'
#     records = []
#     apps = os.listdir(d)
#     for app in apps:
#         record = {}
#         record['voice_command'] = 'open ' + app.split('.app')[0]
#         record['sys_command'] = 'open ' + d + '/%s' % app.replace(' ', '\ ')
#         records.append(record)


def search_google(query):
    chrome_path = "/usr/local/bin/chromedriver"
    browser = webdriver.Chrome(chrome_path)
    browser.get('http://www.google.com')
    search = browser.find_element_by_name('q')
    search.send_keys(query)
    search.send_keys(Keys.RETURN)


def open_app(app):
    d = '/Applications'
    os.system('open ' + d + '/%s.app' % app.replace(' ', '\ '))


def open_file():  # creates and opens new sublime text file - TODO
    lol = 0


def bluetooth():  # TODO
    say("Initializing connection")


verified = False
search_trigger = 'look up '
application_trigger = 'open '
new_text_file_trigger = 'create a new text file'
verified = greeting(verified)
keep_going = True
while keep_going:
    command_received = command()
    print("> " + command_received)

    if search_trigger in command_received.lower():
        search = command_received.lower().split(search_trigger)[-1]
        search_google(search)
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
    elif application_trigger in command_received.lower():
        app = command_received.lower().split(application_trigger)[-1]
        open_app(app)
    elif new_text_file_trigger in command_received.lower():
        # text_file = command_received.lower().split(new_text_file_trigger)[-1]
        open_file()
    elif command_received == "stop":
        speak("Shutting down")
        keep_going = False
