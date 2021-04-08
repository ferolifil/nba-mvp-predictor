import streamlit as st
import time
from scrap import scrap_latest
from std import std_latest
from model import limit_calc, pred_latest
import pandas as pd
import numpy as np
from pyngrok import ngrok

def main():

  season = 2021

  st.write("""
  # NBA MVP Predictor
  """)

  submit = st.button('Start now')
  if submit:

    scrap_latest(season)
    nba2021 = std_latest(season)
    df_top5, mvp_stats = pred_latest()     

    st.table(df_top5)

    mvp_stats = mvp_stats.set_index('Player')
    st.table(mvp_stats.style.format({"PTS" : "{:.2f}", 'TRB' : "{:.2f}", 'AST' : "{:.2f}", 'BLK' : "{:.2f}", 'STL' : "{:.2f}", 'FG%' : "{:.2%}", 'FT%' : "{:.2%}"}))


    st.image('./nikola.jpg')
  try:
    public_url = ngrok.connect('8501')

    # public_url
    # http://72eec084c813.ngrok.io
  except:
    pass

if __name__ == "__main__":
    main()