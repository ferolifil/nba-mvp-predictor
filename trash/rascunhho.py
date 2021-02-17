from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# Getting all players stats from 1979-80 to 2019-20 season 
# Data from basketball-reference.com

for season in np.arange(1980,2021,1):

    # URL page we will scraping (see image above)
    url = "https://www.basketball-reference.com/leagues/NBA_{}_totals.html".format(season)
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
 
    df.to_csv(f"./basketball_reference_dbs/{season}.csv", index=False)