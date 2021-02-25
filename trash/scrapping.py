from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Getting all players stats from 1979-80 to 2019-20 season 
# Data from basketball-reference.com

for season in np.arange(1981,2021,1):

    # URL page we will scraping (see image above)
    url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(season)
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html)

    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]
    # headers

    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]

    df = pd.DataFrame(player_stats, columns = headers)
 
    df.to_csv(f"./basketball_reference_dbs/{season}adv.csv", index=False)

# I know it's ugly, but it's just to be practical

for season in np.arange(1981,2021,1):

    # URL page we will scraping (see image above)
    url = "https://www.basketball-reference.com/awards/awards_{}.html".format(season)
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html)

    # use findALL() to get the column headers
    # limit 2 because there are 2 header rows, [1] because we want the second one
    soup.findAll('tr', limit=2)[1]
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]

    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]

    df = pd.DataFrame(player_stats, columns = headers)
    df = df.iloc[1:]
 
    df.to_csv(f"./basketball_reference_dbs/mvp/{season}_mvp.csv", index=False)