import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import time
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import tree
from tqdm import tqdm

def limit_calc(column):
    q1 = column.quantile(0.25)
    q3 = column.quantile(0.75)
    amplitude = q3 - q1
    return q1 - 1.5 * amplitude, q3 + 1.5 * amplitude

def main():

    nba_dataset = pd.DataFrame()

    for season in np.arange(1981,2022,1):
        df = pd.read_csv(f'./data/{season}_std.csv', low_memory=False)    
        nba_dataset = nba_dataset.append(df)

    cols = ['MP','FG','FG%','3P','2P','FT','TRB','DRB%','ORB%','OWS','DWS','WS/48','OBPM','DBPM','First']
    nba_dataset = nba_dataset.drop(columns=cols)

    nba_dataset = nba_dataset.loc[((nba_dataset['3P%'] >= 0.0) & (nba_dataset['3P%'] <= 0.6)) 
                                | (nba_dataset['3P%'] > 0.6) & (nba_dataset['3PA'] >= 50)
                                | (nba_dataset['Status'] != 'OOR'), :]

    min_val, max_val = limit_calc(nba_dataset['2P%'])

    nba_dataset = nba_dataset.loc[((nba_dataset['2P%'] >= min_val) & (nba_dataset['2P%'] <= max_val)) 
                                | (nba_dataset['2P%'] > max_val) & (nba_dataset['2PA'] >= 250)
                                | (nba_dataset['Status'] != 'OOR'), :]

    nba_dataset = nba_dataset.loc[(nba_dataset['FTA'] >= 50)
                                | (nba_dataset['Status'] != 'OOR'), :]

    

    nba_dataset = nba_dataset.drop(columns=['3PA','2PA','FTA','FGA','3PAr','FTr'])

    full_nba_dataset = nba_dataset

    df_test = full_nba_dataset.drop(['Player','Pos','Age','Tm','Status'],axis=1)

    feature_list = ['VORP', 'WS', 'W/L%', 'PER', 'BPM', 'PTS','Season','Share']

    nba_dataset = nba_dataset[feature_list]  

    model = RandomForestRegressor(n_estimators=10,criterion='mse',max_depth=5)

    iterations = 100
    season = 2021
    
    y_train = nba_dataset.loc[(nba_dataset['Season'] != season),['Share']]
    y_train = np.ravel(y_train)

    X_train = nba_dataset.loc[(nba_dataset['Season'] != season),:].drop(['Share','Season'], axis=1)
    X_test = nba_dataset.loc[(nba_dataset['Season'] == season),:].drop(['Share','Season'], axis=1)

    players_rank = dict()
    players_first = dict()
    df = full_nba_dataset.loc[(full_nba_dataset['Season'] == season),:]

    for i in range(iterations):

        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        df['Pred'] = pred.tolist()
        df = df[['Player','Pred']]
        df_pred = df.sort_values('Pred', ascending=False)

        for j in range(10):
            if df_pred.iat[j,0] in players_rank.keys():
                players_rank[df_pred.iat[j,0]] += (10-(j*1))
            else:
                players_rank[df_pred.iat[j,0]] = (10-(j*1))

        players_columns = list(players_rank.keys())
        votes_columns = []

        for k in players_columns:
            votes_columns.append(players_rank[k])

        if df_pred.iat[0,0] in players_first.keys():
            players_first[df_pred.iat[0,0]] += 10
        else:
            players_first[df_pred.iat[0,0]] = 10

        players_first_list = list(players_first.keys())
        votes_first = []

        for k in players_first_list:
            votes_first.append(players_first[k])

    data = dict()
    data['Player'] = players_columns
    data['Pred'] = votes_columns

    df_pred_final = pd.DataFrame(data)
    df_pred_final = df_pred_final.sort_values(by='Pred', ascending=False)
    df_pred_final.to_csv(f"./last_prediction.csv")


    data2 = dict()
    data2['Player'] = players_first_list
    data2['First'] = votes_first

    df_temp = pd.DataFrame(data2)
    df_temp2 = df_pred_final.join(df_temp.set_index('Player'), on='Player')
    df_temp2 = df_temp2.fillna(0)
    
    print(df_temp2)

    # df1 = df1.join(df2.set_index(keys), on=keys)

    # df_pred_final = df_pred_final[:5]

    # for i in df_pred_final.index:
    #     print(i) 



if __name__ == "__main__":
    main()