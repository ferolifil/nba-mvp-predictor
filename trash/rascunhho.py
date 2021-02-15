import pandas as pd

df = pd.read_csv("./basketball_reference_dbs/1981.csv", sep=",")

print(df.dtypes)

# print(df)
# df.dropna(axis=0, how="all")

# df.to_csv("check.csv",index=False)

for i in df.index:
    
    if pd.isna(df.at[i,'Player']):
        print("Nulao")