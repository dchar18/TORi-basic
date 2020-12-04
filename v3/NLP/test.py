from nlp import NLP

nlp = NLP()
print("Created instance of NLP")
nlp.retrain_model()
print("Retrained model")
nlp.predict("Calculate the circumference of the earth")