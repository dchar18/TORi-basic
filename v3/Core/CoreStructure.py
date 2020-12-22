# Description: this file contains the Core class, which deals with the core functions of TORi.
#              After input is received, it is sent to the Core class which then calls the appropriate
#              function to deal with the command

# order of events:
# 1. nlp.listen() listens for input (trigger followed by command) - TODO*
# 2. input is passed through nlp.predict_class() to find what the intent was
# 3. set is created (ex: [{'intent': 'modes', 'probability': '0.9999721'}])
# 4. the set and the original input are passed to Core.process()
# 5. corresponding function (skill) is called

import sys
sys.path.insert(1, '/Users/damiancharczuk/Documents/Projects/TORi/v3/NLP')
# sys.path.insert(1, '/home/pi/Documents/TORi/v3/NLP')
from nlp import *
# sys.path.insert(2, '/Users/damiancharczuk/Documents/Projects/TORi/v3/Server')
# sys.path.insert(2, '/home/pi/Documents/TORi/v3/Server')
# from server import *

# packages for modes()
import nltk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

class Core():
    skills = [
        'wake', 'about', 'weather', 
        'google', 'math', 'file', 
        'email', 'leds', 'modes', 
        'update'
    ]
    full_command = ''
    intent = ''

    # def __init__(self) -> None:
        # self.app = None

    # inputs:
    #   self - object
    #   prediction - set in format: [{'intent': 'modes', 'probability': '0.9999721'}]
    #   command - full string input recorded
    def process(self, prediction, command):
        self.full_command = command
        self.intent = prediction[0]['intent']
        prob = float(prediction[0]['probability'])
        
        if self.intent in self.skills:
            if prob > 0.95:
                self.add_to_history(self.intent, command)
            if self.intent == 'wake':
                self.wake()
            elif self.intent == 'about':
                self.about()
            elif self.intent == 'weather':
                self.weather()
            elif self.intent == 'google':
                self.google()
            elif self.intent == 'math':
                self.math()
            elif self.intent == 'file':
                self.file()
            elif self.intent == 'email':
                self.email()
            elif self.intent == 'leds':
                self.leds()
            elif self.intent == 'modes':
                self.modes()
            elif self.intent == 'update':
                self.update()

    def wake(self):
        print()

    def about(self):
        print()

    def weather(self):
        print()

    def google(self):
        print()

    def math(self):
        print()

    def file(self):
        print()

    def email(self):
        print()

    def leds(self):
        # temporarily call the modes function
        # will be replaced once Spotify functionality added to modes()
        self.modes()

    def modes(self):
        modes = ['off', 'random', 'christmas', 'study', 'party']
        boards = ['desk', 'bed']
        # if self.app == None:
        #     self.app = server_start()

        url = '' # used to select the appropriate button in the web server
        # parse out what devices should be modified- TODO
        words = nltk.word_tokenize(self.full_command)
        print("Parsing the command...")
        if 'all' in words:
            # send message to both boards
            # find determine what mode is intended
            mode = 'party' # placeholder in case user wants an unregistered mode 
            for m in modes:
                if m in words:
                    mode = m
            url = '/' + mode + '/sync'
        else:
            # 'and' indicates that the user will want to set different modes to each device
            if 'and' in words:
                # split the list into lists containing a single command for each board
                size = len(words) 
                idx_list = [idx + 1 for idx, val in enumerate(words) if val == 'and']
                res = [words[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))]
                # process each sublist
                for r in res:
                    # find the board that is to be updated
                    board = 'desk' # default
                    for b in boards:
                        if b in r:
                            board = b
                    # find the mode that the board will be sent to
                    mode = 'party' # placeholder in case user wants an unregistered mode 
                    for m in modes:
                        if m in r:
                            mode = m
                    url = '/esp8266_' + board + '/' + mode
                    self.send_mode(url)
            else:
                # find the board that is to be updated
                board = 'desk' # default
                for b in boards:
                    if b in words:
                        board = b
                # find the mode that the board will be sent to
                mode = 'party' # placeholder in case user wants an unregistered mode 
                for m in modes:
                    if m in words:
                        mode = m
                url = '/esp8266_' + board + '/' + mode
                self.send_mode(url)

    def send_mode(self, url):
        print("Accessing server through selenium...")
        opt = Options()
        opt.add_argument("--headless") 
        driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=opt)
        # driver = webdriver.Chrome('/home/pi/Documents/TORi/v3/chromedriver', chrome_options=opt)
        driver.get('http://192.168.50.114:8181/')
        driver.find_element_by_xpath('//a[@href="'+url+'"]').click()
        driver.close()

    def wake(self):
        print()

    # when the program is commanded to close, the model will be retrained if new 
    # samples were added to the intents.json file
    def update(self):
        print()

    # add phrase to intents.json to provide the NLP model with more samples
    # use intent as the tag and append phrase to that tag's list of patterns
    # inputs:
    #   intent - corresponds to an entry in the "tag" fields in intents.json 
    #   phrase - pattern to be added to the intent's list of patterns
    def add_to_history(self, intent, phrase):
        # access file that stores the history in the server
        # add the phrases to intents in intents.json
        # save intents.json
        print()