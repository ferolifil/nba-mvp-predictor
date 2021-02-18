from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# for season in np.arange(1980,2021,1):

#     df = pd.read_csv(f'../basketball_reference_dbs/mvp/{season}_mvp.csv', usecols=['Player'])[:5]

#     # Players name standardization

#     df['Status'] = 'Candidate'

#     for i in df.index:
#         if i == 0:
#             df.at[i,'Status'] = 'MVP'


#     df.to_csv(f'../data/mvp/{season}_mvpstd.csv', index=False)


# Removing Games Started column (incomplete information)

###############################################################################################################################################

# for season in np.arange(1980,2021,1):

#     df = pd.read_csv(f'../data/{season}std.csv')
#     df2 = pd.read_csv(f'../data/mvp/{season}_mvpstd.csv')

#     df = df.join(df2.set_index('Player'), on='Player')

#     df[['Status']] = df[['Status']].fillna(value='OOR')

#     df.to_csv(f'../data/{season}std.csv',index=False)


###############################################################################################################################################

for season in np.arange(1980,2021,1):
    data_types_dict = {'Age': 'int32', 'G': 'int32', 'MP': 'int32', 'FG': 'int32', 'FGA': 'int32', '3P': 'int32', '3PA': 'int32',
    '2P': 'int32', '2PA': 'int32', 'FT': 'int32', 'FTA': 'int32', 'ORB': 'int32', 'DRB': 'int32', 'TRB': 'int32', 'AST': 'int32', 
    'STL': 'int32', 'BLK': 'int32', 'TOV': 'int32', 'PF': 'int32', 'PTS': 'int32' }

    df = pd.read_csv(f'../data/{season}std.csv')
    df = df.astype(data_types_dict)
    # print(df.dtypes)

    df['Season'] = season


    df.to_csv(f'../data/{season}std.csv',index=False)
