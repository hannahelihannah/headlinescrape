# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 13:05:43 2018

@author: hnnhr
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from requests import get
import pandas as pd
from dateutil.parser import parse
import datetime

##set up webdriver and basic variables
driver = webdriver.Chrome()
url = 'https://www.idsnews.com/section/news.html?page=1&ajax=1'
response = get(url)

##create workbook where data will go
ids_head = []
ids_date = []

##set up URL loop with beautifulsoup inside
url_pattern = 'https://www.idsnews.com/section/news.html?page={}&ajax=1'
##set up text replacement function to allow for replacing months
def replace_all(text, dic):
    for i,j in dic.items():
        text = text.replace(i,j)
    return text

## set up headline and date scraping
for i in range(1, 100):
    url_up = url_pattern.format(i)
    page = requests.get(url_up)
    soup = BeautifulSoup(page.text, 'html.parser')
    headline = soup.find_all('h2', class_='no-top-marg')
    date = soup.find_all(class_='text-secondary')
    ##scrapes and changes dates
    for y in date:
            y = y.text.encode('utf-8').strip()
            if ' ' in y:
                if 'ago' not in y:
                    date = parse(y)
                    fin = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
                    ##string replaces
                    replaces = {'Dec':'12', 'Nov':'11', 'Oct':'10','Sep':'9','Aug':'8'}
                    fin2 = replace_all(fin, replaces)
                    fin3 = parse(fin2)
                    ids_date.append(fin3)
                else:
                    print y
                    fin = datetime.datetime.today().strftime('%m-%d-%Y')
                    ids_date.append(fin)
    ##scrapes headlines
    for x in headline:
        x = x.text.encode('utf-8').strip()
        ids_head.append(x)
    i = i+1
##add all data to dataframe and export to csv
data = pd.DataFrame({'Headline': ids_head,'Date': ids_date})
data.to_csv('IDSHeads.csv', index=True)
print("1")
driver.close



