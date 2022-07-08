from flair.models import TextClassifier
from flair.data import Sentence
import pandas as pd
import time


sia = TextClassifier.load('en-sentiment')

def flair_prediction(x):
    sentence = Sentence(x)
    sia.predict(sentence)
    score = sentence.labels[0]
    if "POSITIVE" in str(score):
        return "pos"
    elif "NEGATIVE" in str(score):
        return "neg"
    else:
        return "neu"

def classify(filename):
    df = pd.read_csv('ParsedReviewData/'+filename+'.csv')
    df["Sentiment"] = df["ReviewText"].apply(flair_prediction)
    df.to_csv('AnalysisResults/'+filename+'.csv')
    print("Done")

start = time.time()
classify('Groww')
end = time.time()
print('Execution Time : '+str(end-start))