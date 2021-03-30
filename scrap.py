from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def scrap(url, head_flag=0):
    
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html,features="lxml")

    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)[head_flag]
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[head_flag].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]
    # headers

    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]

    df = pd.DataFrame(player_stats, columns = headers)
    
    return df

def get_teams(url):
    
    # collect HTML data
    html = urlopen(url)

    # create beautiful soup object from HTML
    soup = BeautifulSoup(html, features="lxml")

    # use getText()to extract the headers into a list
    titles = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    titles = list(titles)
    
    
    divisions = ['Atlantic Division', 'Central Division',
             'Southeast Division', 'Northwest Division',
             'Pacific Division', 'Southwest Division',
             'Midwest Division','W', r'W/L%', r'PS/G', r'SRS',r'L', r'GB', r'PA/G','Eastern Conference','Western Conference']
    teams = []
    
    for t in titles:
        if t not in divisions:
            teams.append(t.split(sep='*')[0])
            
    return teams

def scrap_teams(url, season,head_flag=0):
    
    # this is the HTML from the given URL
    html = urlopen(url)
    soup = BeautifulSoup(html,features="lxml")

    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)[head_flag]
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[head_flag].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]
    # headers

    # avoid the first header row
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]
    
    if season > 2015:
        player_stats = player_stats[:32]

    df = pd.DataFrame(player_stats, columns = headers)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    teams = get_teams(url)
    
    if season > 2015:
        teams = teams[:30]

    df['Teams'] = teams
    
    return df


def scrap_latest(season=2021):
                                    # SCRAPPING LATEST DATA #
    #######################################################################################################

    url = "https://www.basketball-reference.com/leagues/NBA_{}_totals.html".format(season)
    df_totals = scrap(url)
    df_totals.to_csv(f"./basketball_reference_dbs/{season}_totals.csv", index=False)

    url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(season)
    df_advanced = scrap(url)
    df_advanced.to_csv(f"./basketball_reference_dbs/{season}_advanced.csv", index=False)

    url = "https://www.basketball-reference.com/leagues/NBA_{}.html".format(season)
    df_teams = scrap_teams(url,season,head_flag=1)
    df_teams.to_csv(f"./basketball_reference_dbs/teams/{season}_teams.csv",index=False)