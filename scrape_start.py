# import requests
# from bs4 import BeautifulSoup as bs
# from bs4 import Comment as Comment
# import numpy as np
# import pandas as pd
# import pymongo


# url = 'https://www.pro-football-reference.com/years/2019/passing.htm'
# user_agent = {'User-agent':'Mozilla/5.0'}

# r = requests.get(url, user_agent)
# print(r.text)

from pymongo import MongoClient
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)


#need to figure out how to go to players page and grab height/weight

#NFL scraping- fantasy stats going back to 1970 and saving as CSV
nfl_years = list(range(2010, 2020))
for i in nfl_years:
    url = 'https://www.pro-football-reference.com'

    r = requests.get(url+'/years/' +str(i)+'/passing_advanced.htm')

    soup = BeautifulSoup(r.content, 'html.parser')
    parsed_table = soup.find_all('table')[0]


    rows= []
    for tr in parsed_table.find_all('tr')[1:]:
        cells = []
        tds = tr.find_all('td')
        if len(tds) == 0:
            ths = tr.find_all('th')
            for th in ths:
                cells.append(th.text.strip())
        else:
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    del rows[0][0]

    df = pd.DataFrame(rows)
    df.columns = df.iloc[0]
    df = df[1:]
    df.to_csv('~/Python/week4cap/NFL-Analysis'+str(i)+'.csv')
