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

for season in np.arange(1980,2021,1):

    df = pd.read_csv(f'../data/{season}std.csv')
    df2 = pd.read_csv(f'../data/mvp/{season}_mvpstd.csv')

    df = df.join(df2.set_index('Player'), on='Player')

    df[['Status']] = df[['Status']].fillna(value='OOR')

    df.to_csv(f'../data/{season}std.csv',index=False)
