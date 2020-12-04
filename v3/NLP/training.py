import random
from typing import Sequence
from nltk.tag.brill import Word
import numpy as np
import pickle
import json

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD # stochastic gradient descent

def train_nlp_model():
    # construct lemmatizer
    lemmatizer = WordNetLemmatizer()

    # load the intents from the json file
    intents = json.loads(open('intents.json').read())

    # declare lists to store vocabulary and classes
    words = []
    classes = []
    documents = []
    # list of punctuation that will be removed from imput strings 
    ignore_punc = ['?', '!', '.', ',']

    # iterate over intents
    for intent in intents['intents']:
        # iterate over potential input patterns
        for pattern in intent['patterns']:
            # convert each pattern string to tokens
            word_list = nltk.word_tokenize(pattern)
            # add the elements of word_list to the list of words
            words.extend(word_list)
            # indicate that the current word list correspondings to the tag
            documents.append((word_list, intent['tag']))

            # check if class is already in the list of classes
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_punc]
    # remove duplicates and sort the words and the classes
    words = sorted(set(words))
    classes = sorted(set(classes))

    # save list of words and classes as .pkl files for later use
    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))

    # to feed neural network, need to convert words to numeric values
    # use bag of words
    training = []
    output_empty = [0]*len(classes)

    for doc in documents:
        bag = []
        word_patterns = doc[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        # iterate through all the words to see if it occurs in the pattern
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)

        # copy output_empty
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training)

    # features
    X_train = list(training[:, 0]) # take everything in the 0 dimension
    # labels
    y_train = list(training[:, 1]) # take all the labels (tags/classes)

    # build the model
    model = Sequential()
    # input layer has 128 neurons
    model.add(Dense(128, input_shape=(len(X_train[0]),), activation='relu'))
    # add dropout layer to prevent overfitting
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    # output with as many neurons as the number of classes
    # use softmax to scale output so all nodes added together add to 1 (i.e. percentages)
    model.add(Dense(len(y_train[0]), activation='softmax'))

    # define stochastic gradient descent optimizer
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    hist = model.fit(np.array(X_train), np.array(y_train), epochs=200, batch_size=5, verbose=1)
    model.save('nlp_model.h5', hist)
    print("Done training")