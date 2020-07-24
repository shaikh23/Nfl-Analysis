# from pymongo import MongoClient
import pprint
# import pandas as pd
# import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import csv
# client = MongoClient('localhost', 27017)


#need to figure out how to go to players page and grab height/weight

def scrape_player_height_weight(path):
    base_url = 'https://www.pro-football-reference.com'

    r = requests.get(base_url + path)

    # result of parsing specific player's main page
    soup = BeautifulSoup(r.content, 'html.parser')

    height = soup.find('span', itemprop='height').text
    weight = soup.find('span', itemprop='weight').text

    return height, weight

#NFL scraping- fantasy stats going back to 2010 and saving as CSV
nfl_years = list(range(2015, 2020))
for i in nfl_years:
    url = 'https://www.pro-football-reference.com'

    # r = requests.get(url+'/years/' +str(i)+'/passing_advanced.htm') # for advanced passing
    r = requests.get(url+'/years/' +str(i)+'/receiving.htm') # for standard passing

    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find_all('table')[0]

    rows = []

    # scrape and parse the header row for lables
    #header_row = table.select('thead > tr')[1] # for Advanced Passing
    header_row = table.select('thead > tr')[0] # for 'standard' passing

    col_names = header_row.find_all('th')[1:]
    header_row = []
    for col_name in col_names:
      header_row.append(col_name.text)
    header_row.append('Height')
    header_row.append('Weight')
    rows.append(header_row)

    # loop through and scrape each non-header row
    for tr in table.select('tbody > tr')[:76]: # only want top 75 or so passers
      row = []
      cols = tr.find_all('td')
      if cols:
        player_url = cols[0].find('a')['href']
        height, weight = scrape_player_height_weight(player_url)
        for col in cols:
          row.append(col.text)
        row.append(height)
        row.append(weight)
        rows.append(row)

    # write result to CSV file
    # https://www.geeksforgeeks.org/writing-data-from-a-python-list-to-csv-row-wise/
    file = open('Receiving_' + str(i) + '.csv', 'w+', newline ='')

    with file:
      write = csv.writer(file)
      write.writerows(rows)


    # for tr in parsed_table.find_all('tr')[1:]:
    #     cells = []
    #     tds = tr.find_all('td')
    #     if len(tds) == 0:
    #         ths = tr.find_all('th')
    #         for th in ths:
    #             cells.append(th.text.strip())
    #     else:
    #         for td in tds:
    #             cells.append(td.text.strip())
    #     rows.append(cells)
    # del rows[0][0]

    # df = pd.DataFrame(rows)
    # df.columns = df.iloc[0]
    # df = df[1:]
    # df.to_csv('~/Python/week4cap/NFL-Analysis'+str(i)+'.csv')
