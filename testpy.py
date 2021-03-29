from scrap import scrap, scrap_teams, get_teams
from std import adjust_main, adjust_mvp, transfered_players, merging_df, teams_std
import pandas as pd

season = 2021


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


                                    # RUNNING THE ANALYSIS #
######################################################################################################

