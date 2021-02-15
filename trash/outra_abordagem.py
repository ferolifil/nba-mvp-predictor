import pandas as pd
import numpy as np

# Opening Dataframe 
df = pd.read_csv("./basketball_reference_dbs/1980T.csv",sep=",")

# Removing Rank (useless) and Games Started (incomplete information) columns
df = df.drop(columns=['GS','Rk']) 

# Players name standardization
for i in df.index:
    df.at[i, 'Player'] = df.at[i, 'Player'].split('\\')[1]

df = df.fillna(0.00)

print(df.index)

duplicated = list(df.loc[df['Tm'] == 'TOT',:].loc[:,'Player'])

print(duplicated)

duplicated_team_choice = dict()
rows_to_drop = list()

for i in df.index:
    if df.at[i,'Player'] in duplicated and df.at[i,'Tm'] != 'TOT':
        rows_to_drop.append(i)
        if df.at[i,'Player'] in duplicated_team_choice.keys():
            duplicated_team_choice[df.at[i,'Player']] = [duplicated_team_choice[df.at[i,'Player']], [df.at[i,'Tm'], df.at[i,'G']]]
        else:
            duplicated_team_choice[df.at[i,'Player']] = [df.at[i,'Tm'], df.at[i,'G']]

df = df.drop(rows_to_drop)

for i in duplicated_team_choice.keys():
    max_played = 0
    for k in duplicated_team_choice[i]:
        for z in k:
            if(isinstance(z, np.int64) and z > max_played):
                max_played = z
                max_pch = aux
            elif isinstance(z, str):
                aux = z

    duplicated_team_choice[i] = max_pch


for i in df.index:
    if df.at[i, 'Player'] in duplicated_team_choice.keys():
        df.at[i, 'Tm'] = duplicated_team_choice[df.at[i, 'Player']]


# df.to_csv("./ALALIO.csv", index=False)




    


            

        

    
