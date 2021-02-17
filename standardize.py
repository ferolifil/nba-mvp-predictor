import pandas as pd
import numpy as np

class Standardize:

    def __init__(self, path):
        self.path = path
        self.df = pd.read_csv(self.path, sep=",")

    def std_func(self):

        df = self.df

        # Removing Games Started column (incomplete information)
        rows_to_drop = list()
        df = df.drop(columns=['GS']) 

        # Players name standardization
        for i in df.index:
            if pd.isna(df.at[i,'Player']):
                rows_to_drop.append(i)  # avoiding empty rows
            else:
                df.at[i, 'Player'] = df.at[i, 'Player'].split('*')[0]   # removing the * mark

        # Some null fields should be 0.00 (e.g. 3pt shooting)
        df = df.fillna(0.00)

        # Players that moved between franchises have the TOT (total) line
        # Get which players are those
        duplicated = list(df.loc[df['Tm'] == 'TOT',:].loc[:,'Player'])

        # Filling the arrays with the duplicated rows
        for i in df.index:
            if df.at[i,'Player'] in duplicated and df.at[i,'Tm'] != 'TOT':
                rows_to_drop.append(i)

        # Dropping the duplicated rows
        df = df.drop(rows_to_drop)

        # Dropping the Franchise column that we don't need anymore
        df = df.drop(columns=['Tm'])

        # Returning the standardized DataFrame
        return df

    def save_df(self, df_tosave, path_tosave):
        df_tosave.to_csv(path_tosave, index=False)


    def mvp_std_func(self):
        df = self.df

        print("worked")









        # # Filling array with the right franchise
        # for i in duplicated_team_choice.keys():
        #     max_played = 0
        #     for k in duplicated_team_choice[i]:
        #         for z in k:
        #             if(isinstance(z, np.int64) and z > max_played):
        #                 max_played = z
        #                 max_pch = aux
        #             elif isinstance(z, str):
        #                 aux = z
                
        #         duplicated_team_choice[i] = max_pch
        
        # # Overwriting TOT for the right franchise
        # for i in df.index:
        #     if df.at[i, 'Player'] in duplicated_team_choice.keys():
        #         df.at[i, 'Tm'] = duplicated_team_choice[df.at[i, 'Player']]