import sys
sys.path.insert(1, '/Users/damiancharczuk/Documents/Projects/TORi/v3/NLP')
from nlp import NLP
from CoreStructure import Core
from time import sleep

print("Creating Core object...")
core = Core()
print("Creating NLP class object")
nlp = NLP()

# print("Calling nlp.listen()")
# in_sentence = nlp.listen()
# print("Retrieved: ", in_sentence)

# prediction = nlp.predict_class(in_sentence)
# print('Prediction: ', prediction)

# if prediction[0]['intent'] == 'wake':
#     print("-- Wake Word Detected --")
in_sentence = nlp.listen()
print("Retrieved: ", in_sentence)

prediction = nlp.predict_class(in_sentence)
print('Prediction: ', prediction)

print("Calling process()...")
core.process(prediction, in_sentence)

print("Done")
# sleep(5)
# core.process([{'intent': 'modes', 'probability': '0.90'}], 'set desk to christmas and bed to party')
# print("Done")