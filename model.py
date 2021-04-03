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

def boxplot(column):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(15, 5)
    sns.boxplot(x=column, ax=ax1)
    ax2.set_xlim(limit_calc(column))
    sns.boxplot(x=column, ax=ax2)
    
# def histogram(column,color=None):
#     plt.figure(figsize=(15, 5))
#     sns.histplot(column,color=color)

def bar_chart(column):  
    plt.figure(figsize=(15, 5))
    ax = sns.barplot(x=column.value_counts().index, y=column.value_counts())
    ax.set_xlim(limit_calc(column))

# def model_score(dataframe,full_nba_dataset,model,features,iterations=1,path='./misses/trash'):
    
#     pbar = tqdm(total = 40)
    
#     features.remove('Share')
#     features.remove('Season')
    
#     nro_of_corrects = 0
#     nro_of_top3_corrects = 0

#     file = open(f"{path}/output.txt","w")
    
#     file.write('Model : {}\n{} features : {}\n'.format(model,len(features),features))

#     t1 = time.time()

#     for season in np.arange(1981,2021,1):

#         text = f' {season} |'

#         y_train = dataframe.loc[(dataframe['Season'] != season),['Share']]
#         y_train = np.ravel(y_train)
#         y_test = dataframe.loc[(dataframe['Season'] == season),['Share']]
#         y_test = np.ravel(y_test)

#         X_train = dataframe.loc[(dataframe['Season'] != season),:].drop(['Share','Season'], axis=1)
#         X_test = dataframe.loc[(dataframe['Season'] == season),:].drop(['Share','Season'], axis=1)

#         players_rank = dict()
#         df = full_nba_dataset.loc[(full_nba_dataset['Season'] == season),['Player','Share','Season']]
#         df_truth = df.sort_values(by='Share', ascending=False)

#         for i in range(iterations):

#             model.fit(X_train, y_train)
#             pred = model.predict(X_test)

#             df['Pred'] = pred.tolist()
#             df_pred = df.drop(['Share'],axis=1).sort_values(by='Pred', ascending=False)

#             for j in range(5):
#                 if df_pred.iat[j,0] in players_rank.keys():
#                     players_rank[df_pred.iat[j,0]] += (10-(j*2))
#                 else:
#                     players_rank[df_pred.iat[j,0]] = (10-(j*2))

#         players_columns = list(players_rank.keys())
#         votes_columns = []

#         for k in players_columns:
#             votes_columns.append(players_rank[k])

#         data = dict()
#         data['Player'] = players_columns
#         data['Season'] = season
#         data['Pred'] = votes_columns

#         df_pred_final = pd.DataFrame(data)
#         df_pred_final = df_pred_final.sort_values(by='Pred', ascending=False)
#         df_pred_final.to_csv(f"./predictions/{season}_pred.csv")

#         pred_top3 = list(df_pred_final['Player'].iloc[:3])
#         top3 = list(df_truth['Player'].iloc[:3]) 
#         top3_success = list()

#         for z in pred_top3:
#             if z in top3:
#                 top3_success.append(z)

#         df_comp = pd.DataFrame()

#         if pred_top3[0] == top3[0]:
#             sorf = 'Success'
#             nro_of_corrects += 1
#         else:
#             sorf = 'Fail'
#             df_comp = full_nba_dataset.loc[(full_nba_dataset['Season'] == season) & (full_nba_dataset['Player'] == top3[0]) ,:]
#             df_comp = df_comp.append(full_nba_dataset.loc[(full_nba_dataset['Season'] == season) & (full_nba_dataset['Player'] == pred_top3[0]) ,:])
#             df_comp['Label'] = ['Correct','Predicted']
#             df_comp.to_csv('{}/{}_miss.csv'.format(path,season),index=False)

#         text += '{:^10s}| '.format(sorf)


#         text += f'{len(top3_success)} from de top3 correct | {top3_success} |\n'
#         nro_of_top3_corrects += len(top3_success)

#         file.write(str(text))
        
#         pbar.update()

#     text = "GLOBAL_SUCCESS_RATE : {:.2%}\nGLOBAL_SUCCESS_RATE_TOP3 : {:.2%}\n".format((nro_of_corrects/40),(nro_of_top3_corrects/120))
#     file.write(str(text))
#     t2 = time.time()

#     text = 'Time elapsed: {:.2f} seconds'.format(t2-t1)
#     file.write(str(text))
#     file.close()
    
#     return (nro_of_corrects/40),(nro_of_top3_corrects/120)

# def feature_selection(dataframe, model):
    
#     if 'Season' in dataframe.columns:
#         dataframe = dataframe.drop(columns='Season')
        
#     try:
#         X = dataframe.drop(['Share'], axis=1)
#         y = dataframe['Share']
#     except:
#         print('Share feature must be in')
        
#     X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8, random_state=10)
    
#     model.fit(X_train, y_train)

#     data_dict = {'Features' : X_train.columns, 'Importance' : model.feature_importances_}
#     features = pd.DataFrame(data_dict).sort_values(by='Importance',ascending=False)
#     features = features.loc[(features['Importance'] > 0) , :]
#     feature_list = features['Features'].to_list()

#     return feature_list

# def test_model(dataframe,model,iterations,path='./misses/trash'):
    
#     feature_list = feature_selection(dataframe=dataframe,model=model)
#     feature_list.extend(['Share', 'Season'])

#     df = full_nba_dataset[feature_list]

#     nro_of_corrects, nro_of_top3_corrects = model_score(dataframe=dataframe,model=model,features=feature_list,iterations=iterations,path=path)

#     return nro_of_corrects, nro_of_top3_corrects


def main():

    #######################################################################################################################################

    nba_dataset = pd.DataFrame()

    for season in np.arange(1981,2021,1):
        df = pd.read_csv(f'./data/{season}_std.csv', low_memory=False)    
        nba_dataset = nba_dataset.append(df)

    # display(nba_dataset)
    # display(nba_dataset.info())

    #######################################################################################################################################

    cols = ['G','MP','FG','FG%','3P','2P','FT','TRB','DRB%','ORB%','OWS','DWS','WS/48','OBPM','DBPM','First']
    # print(f"Removing {len(cols)} features.")
    nba_dataset = nba_dataset.drop(columns=cols)

    #######################################################################################################################################

    min_val = 0.0
    max_val = 0.6

    # df_size = nba_dataset.shape[0]
    nba_dataset = nba_dataset.loc[((nba_dataset['3P%'] >= min_val) & (nba_dataset['3P%'] <= max_val)) 
                                | (nba_dataset['3P%'] > max_val) & (nba_dataset['3PA'] >= 50)
                                | (nba_dataset['Status'] != 'OOR'), :]
    # removed_rows = df_size - nba_dataset.shape[0]
    # print('{} rows removed'.format(removed_rows))

    #######################################################################################################################################

    min_val, max_val = limit_calc(nba_dataset['2P%'])

    # df_size = nba_dataset.shape[0]
    nba_dataset = nba_dataset.loc[((nba_dataset['2P%'] >= min_val) & (nba_dataset['2P%'] <= max_val)) 
                                | (nba_dataset['2P%'] > max_val) & (nba_dataset['2PA'] >= 250)
                                | (nba_dataset['Status'] != 'OOR'), :]
    # removed_rows = df_size - nba_dataset.shape[0]
    # print('{} rows removed'.format(removed_rows))

    #######################################################################################################################################

    # df_size = nba_dataset.shape[0]
    nba_dataset = nba_dataset.loc[(nba_dataset['FTA'] >= 50)
                                | (nba_dataset['Status'] != 'OOR'), :]
    # removed_rows = df_size - nba_dataset.shape[0]
    # print('{} rows removed'.format(removed_rows))

    #######################################################################################################################################

    nba_dataset = nba_dataset.drop(columns=['3PA','2PA','FTA','FGA','3PAr','FTr'])
    # display(nba_dataset)
    # nba_dataset.info()

    #######################################################################################################################################

    full_nba_dataset = nba_dataset

    #######################################################################################################################################

    df_test = full_nba_dataset.drop(['Player','Pos','Age','Tm','Status'],axis=1)

    #######################################################################################################################################

    choosen_model = RandomForestRegressor(n_estimators=10,criterion='mse',max_depth=5)
    # nro_of_corrects, nro_of_top3_corrects = test_model(dataframe=df_test,model=choosen_model,iterations=5,path='./misses/random_forest')

    feature_list = feature_selection(df_test, choosen_model)
    feature_list = feature_list[:6]
    # display(feature_list)
    feature_list.extend(['Share', 'Season'])
    nro_of_corrects, nro_of_top3_corrects = model_score(dataframe=df_test,full_nba_dataset=full_nba_dataset,model=choosen_model,features=feature_list,iterations=10)

    print("GLOBAL_SUCCESS_RATE : {:.2%}\nGLOBAL_SUCCESS_RATE_TOP3 : {:.2%}\n".format((nro_of_corrects),(nro_of_top3_corrects)))   


if __name__ == "__main__":
    main()