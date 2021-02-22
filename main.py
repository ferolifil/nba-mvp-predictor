import pandas as pd
import numpy as np
import standardize as std 

def main():

    # veja que legal rany

    # Opening Dataframe 
    
    # Standardizing all dataframes from 1980 -> 2020
    for season in np.arange(1980,2021,1):

        x = std.Standardize(f"./basketball_reference_dbs/{season}.csv")
        x.save_df(x.std_func(),f"./data/{season}std.csv")

    # df.to_csv("./1980_std.csv", index=False)

if __name__ == "__main__":
    main()