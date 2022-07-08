import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup as bs
import urllib.parse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import time



def fetchIds(company, debug=False):
    if debug:
        ("Trying to find Ids for apps:")
    baseUrl = 'https://www.google.com/search?q='
    url = baseUrl+company+'playstore'+'reviews'+'finance'
    ids = []
    try:
        response = requests.get(url)
        content = bs(response.text, "lxml")
        div_content = content.find_all('a')
        if debug:
            print("Hit : "+company)
        for ele in div_content:
            for word in str(ele).split():
                if "https://play.google.com/" in word:
                    ansUrl = urllib.parse.unquote_plus(ele['href'])
                    initial = ansUrl.find('id=')
                    final = ansUrl[initial:].find('&')
                    if debug:
                        print("appending")
                    ids.append(ansUrl[initial+3: initial+final])
    except ConnectionError:
        if debug:
            print("Miss : "+company)
            print("URL trid : "+url)
            
    return ids

def getReviews(company, debug=False):
    if debug:
        print("Trying to fetch reviews:")
    ids = fetchIds(company)
    driver = webdriver.Firefox()
    numberOfReviews = 0
    for id in ids:
        try:
            url = 'https://play.google.com/store/apps/details?id='+id+'&hl=en_IN&gl=US'
            driver.get(url)
            arrow = driver.find_element(By.XPATH,'/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/header/div/div[2]/button/i')
            arrow.click()
            reviews = driver.find_element(By.CSS_SELECTOR, '.VfPpkd-cnG4Wd > div:nth-child(1)')
            time.sleep(1)
            crawlWriter = open('RawReviewData/'+company, 'w')
            actions = ActionChains(driver)
            actions.click(reviews)
            prevLen = 0 
            i=0
            while i<50: 
                actions.send_keys(Keys.PAGE_DOWN).perform()
                reviewsList = bs(reviews.get_attribute('innerHTML'), 'lxml').find_all('div', {'class':'RHo1pe'})#
                if len(reviewsList) > prevLen:
                    print("Reviews : "+str(len(reviewsList)))
                    for review in reviewsList[prevLen:]:
                        crawlWriter.write("%s\n" % review)
                    prevLen = len(reviewsList)
                    i=0
                i+=1
                if len(reviewsList)>5000:
                    break
        except:
            if debug:
                print("FUCKED : "+id)
    time.sleep(3)
    driver.quit()

company = input('Enter name of Company : ')
getReviews(company)


# IndMoney, Groww, Scripbox, Dezerv, Stack, Et Money, Kuvera, Fisdom, Fintoo, CubeWelath, Dhan, Spenny, Jar, coin by zerodha, fi Money, smallcase, mycams, kfintech, glide invest, cashRich, smallcase, 

# mutual fund uiverse data
# historical index data nse india
# calculate beta and alpha against benchmarknifty



