import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs


def parseReviewFiles(filename):
    df = pd.DataFrame()
    try:
        reader = open('RawReviewData/'+filename)
        lines = reader.readlines()
    except:
        print("Couldnot open file")
        return []
    for line in  lines:
        reviewDict = {}
        item = line[:-1]
        bsObj = bs(item, 'lxml')
        if len(str(bsObj))>200:
            try:
                reviewDict['Customer_name'] = bsObj.find_all('div', {'class':'X5PpBb'})[0].text
                reviewDict['Date'] = bsObj.find_all('span', {'class':'bp9Aid'})[0].text
                txt = bsObj.find_all('div', {'class':'iXRFPc'})[0]['aria-label']
                for word in txt:
                    if word.isdigit():
                        reviewDict['Rating'] = word
                reviewDict['ReviewText'] = bsObj.find_all('div', {'class':'h3YV2d'})[0].text
                df = df.append(reviewDict, ignore_index = True)         #Use concat instead
            except:
                continue
    print("Parsed "+str(df.shape[0])+" reviews")
    df.to_csv('ParsedReviewData/'+filename+'.csv')

start = time.time()  
df = parseReviewFiles('IndMoney')
end = time.time()
print("Execution Time = "+str(end-start))
