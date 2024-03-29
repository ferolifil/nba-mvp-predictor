import pandas as pd
import numpy as np

def adjust_main(df):

    rows_to_drop = []
    # Players name standardization
    for i in df.index:
        if pd.isna(df.at[i,'Player']):
            rows_to_drop.append(i)  # avoiding empty rows
        else:
            df.at[i, 'Player'] = df.at[i, 'Player'].split('*')[0]   # removing the * mark

    # Some null fields should be 0.00 (e.g. 3pt shooting)
    df = df.fillna(0.00)

    # Dropping the duplicated rows
    df = df.drop(rows_to_drop)

    # Returning the standardized DataFrame
    return df  

def merging_df(df1,df2, keys):

    df1 = df1.join(df2.set_index(keys), on=keys)

#     df[['Status']] = df[['Status']].fillna(value='OOR')

    # df1.to_csv(f'./data/{season}_std.csv',index=False)
    
    return df1
    
def adjust_mvp(df):
    
    # Players name standardization
    df['Status'] = 'Candidate'
    df.at[0,'Status'] = 'MVP'
    
    rows_to_drop = []
    flag = False
    
    for i in df.index:
        if pd.isna(df.at[i,'Player']):
            flag = True
        
        if flag is True:
            rows_to_drop.append(i)
    
    df = df.drop(rows_to_drop)

    # df.to_csv(f'./data/mvp/{season}_mvp_std.csv', index=False)
     
    return df

def transfered_players(df):

    transfered_players = []
    rows_to_drop = []

    for i in df.index:
        if df.at[i,'Tm'] == 'TOT':
            transfered_players.append(df.at[i,'Player'])
            rows_to_drop.append(i)

    df_aux = df.drop(rows_to_drop)
    transfered_players_dict = {}

    for i in df_aux.index:
        if df_aux.at[i,'Player'] in transfered_players:
            pl = df_aux.at[i,'Player']
            if pl in transfered_players_dict.keys():
                transfered_players_dict[pl].extend([df_aux.at[i,'Tm'],int(df_aux.at[i,'G'])])
            else:
                transfered_players_dict[pl] = [df_aux.at[i,'Tm'],int(df_aux.at[i,'G'])]

    for player in transfered_players_dict.keys():
        max_played = 0
        for i in transfered_players_dict[player]:
            if isinstance(i,int):
                if i > max_played:
                    transfered_players_dict[player] = team
                    max_played = i
            else:
                team = i

    rows_to_drop.clear()

    for i in df.index:
        if df.at[i,'Player'] in transfered_players:
            if df.at[i,'Tm'] == 'TOT':
                df.at[i,'Tm'] = transfered_players_dict[df.at[i,'Player']]
            else:
                rows_to_drop.append(i)
                
    df = df.drop(rows_to_drop)

    return df

def teams_std(df, season):
    
    team_dict = {
    'Atlanta Hawks' : 'ATL',
    'Boston Celtics' : 'BOS',
    'Brooklyn Nets' : 'BRK',
    'Charlotte Hornets' : 'CHO', # 2015 - now
    'Chicago Bulls' : 'CHI',
    'Cleveland Cavaliers' : 'CLE',
    'Dallas Mavericks' : 'DAL',
    'Denver Nuggets' : 'DEN',
    'Detroit Pistons' : 'DET',
    'Golden State Warriors' : 'GSW',
    'Houston Rockets' : 'HOU',
    'Indiana Pacers' : 'IND',
    'Los Angeles Clippers' : 'LAC',
    'Los Angeles Lakers' : 'LAL',
    'Memphis Grizzlies' : 'MEM',
    'Miami Heat' : 'MIA',
    'Milwaukee Bucks' : 'MIL',
    'Minnesota Timberwolves' : 'MIN',
    'New Orleans Pelicans' : 'NOP',
    'New York Knicks' : 'NYK',
    'Oklahoma City Thunder' : 'OKC',
    'Orlando Magic' : 'ORL',
    'Philadelphia 76ers' : 'PHI',
    'Phoenix Suns' : 'PHO',
    'Portland Trail Blazers' : 'POR',
    'Sacramento Kings' : 'SAC',
    'San Antonio Spurs' : 'SAS',
    'Toronto Raptors' : 'TOR',
    'Utah Jazz' : 'UTA',
    'Washington Wizards' : 'WAS',
    'Seattle SuperSonics' : 'SEA',
    'San Diego Clippers' : 'SDC',
    'Kansas City Kings' : 'KCK',
    'Washington Bullets' : 'WSB',
    'New Jersey Nets' : 'NJN',
    'Charlotte Hornets CLASSIC' : 'CHH', # 1989 - 2002 
    'Vancouver Grizzlies' : 'VAN',
    'New Orleans Hornets' : 'NOH', # 2003 - 2005 / 2008 - 2014
    'Charlotte Bobcats' : 'CHA',
    'New Orleans/Oklahoma City Hornets' : 'NOK', # 2006 - 2007
    }

    chh_issue = np.arange(1989,2003,1)
    tm_list = []
    rows_to_drop = []

    for i in df.index:
        team  = df.at[i,'Teams']
        if season < 2021:
            team = team[:-1]

        if season == 2021:
            if '(' in team:
                team  = team.split(sep="(")[0]
                team = team[:-1]

        if team == 'Charlotte Hornets' and season in chh_issue:
            tm_list.append('CHH')
        elif team in team_dict.keys():
            tm_list.append(team_dict[team])
        else:
            rows_to_drop.append(i)

    df = df.drop(rows_to_drop)        
    df['Tm'] = tm_list
    df = df[['Tm','W/L%']]
    df.sort_values(r'W/L%',ascending=False)
    
    return df

def std_latest(season=2021):
                                        # STANDARDZING #
    ######################################################################################################

    df1 = pd.read_csv(f'./basketball_reference_dbs/{season}_totals.csv')
    # Removing empty column
    df1 = df1.drop(columns=['GS'])
    df1 = adjust_main(df1)

    # Removing empty columns
    col = []
    for i in range(28):
        if i != 18 and i != 23:
            col.append(i)
    df2 = pd.read_csv(f'./basketball_reference_dbs/{season}_advanced.csv',usecols=col) 
    df2 = adjust_main(df2)

    # Merging both DataFrames
    df1 = merging_df(df1,df2,['Player','Pos', 'Age','G', 'MP','Tm']) 

    df1 = df1.fillna(0.0)
    df1['First'] = 0
    df1['Share'] = 0
    df1['Status'] = 'OOR'

    df1[['Season']] = season

    df1 = transfered_players(df1)

    df4 = pd.read_csv(f"./basketball_reference_dbs/teams/{season}_teams.csv")
    df4 = teams_std(df4,season)

    df1 = merging_df(df1,df4,['Tm'])

    data_types_dict = {'Age': 'int32', 'G': 'int32', 'MP': 'int32', 'FG': 'int32', 'FGA': 'int32', '3P': 'int32', '3PA': 'int32',
    '2P': 'int32', '2PA': 'int32', 'FT': 'int32', 'FTA': 'int32', 'ORB': 'int32', 'DRB': 'int32', 'TRB': 'int32', 'AST': 'int32', 
    'STL': 'int32', 'BLK': 'int32', 'TOV': 'int32', 'PF': 'int32', 'PTS': 'int32', 'Season': 'object', 'W/L%' : 'float64'}

    df1 = df1.astype(data_types_dict)

    df1.to_csv(f'./data/{season}_std.csv',index=False)

    return df1