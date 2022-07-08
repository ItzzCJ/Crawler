import re
from rake_nltk import Rake
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import pytorch_cos_sim # cosine silarity
import pandas as pd
from nltk.corpus import stopwords
import string
from nltk.stem.wordnet import WordNetLemmatizer
import time

import warnings
warnings.simplefilter('ignore')
from itertools import chain


stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()



r = Rake()


def clean(text):
    stop_free = ' '.join([word for word in text.lower().split() if word not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = ' '.join([lemma.lemmatize(word) for word in punc_free.split()])
    return normalized


def findTopic(filename):
    df = pd.read_csv('AnalysisResults/'+filename+'.csv')
    reviews = pd.DataFrame()

############################
    dfNeg = df[df['Sentiment'] == 'neg']
    dfPos = df[df['Sentiment'] == 'pos']


    reviews['ReviewText'] = dfNeg.iloc[:,5]
    reviews['Cleaned'] = reviews['ReviewText'].apply(clean)
    
    # keyphrases = []
    r.extract_keywords_from_sentences(list(reviews['Cleaned']))
    keyphrases = r.get_ranked_phrases_with_scores()
    final = {}
    phraseList = []
    for weight, phrase in keyphrases:
        if weight > 40.0:
            final[phrase] = weight
            phraseList.append(phrase)
    
    ansDF = pd.DataFrame()
    model = SentenceTransformer('stsb-roberta-large')
    embeddings = model.encode(phraseList)
    print("Writing")
    markup = [0]*len(embeddings)
    for i in range(len(embeddings)):
        if markup[i] == 0:
            markup[i] = 1
            dic={}
            ansList = [] 
            totalWeight = final[phraseList[i]]
            for j in range(len(embeddings[i:])):
                if pytorch_cos_sim(embeddings[i], embeddings[j]).item() > 0.4:
                    markup[j]=1
                    ansList.append(phraseList[j])
                    totalWeight += final[phraseList[i]]
            dic['KeyPhrase'] = phraseList[i]
            dic['CombinedWeight'] = totalWeight
            dic['SimilarPhrases'] = '|'.join(ansList)
            ansDF = ansDF.append(dic, ignore_index=True)
    ansDF.to_csv('TestData/blah.csv')
    
start = time.time()
print("Starting at : "+str(start))
findTopic('Paytm Money')
end = time.time()
print("Execution time : "+str(end-start))