import streamlit as st
import time
from scrap import scrap_latest
from std import std_latest
from model import limit_calc, pred_latest
import pandas as pd
import numpy as np

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
  # st.dataframe(df_top5.set_index('Player'))
  # st.table(mvp_stats.set_index('Player'))

  # mvp_stats = mvp_stats.astype({'PTS' : 'object', 'TRB' : 'object', 'AST' : 'object', 'BLK' : 'object', 'STL' : 'object', 'TOV' : 'object', 'PF' : 'object'})

  # for col in np.arange(0,11,1):
  #   if col not in [0,1,2,3]:
  #     mvp_stats.iat[0,col] = '{:.2f}'.format(mvp_stats.iat[0,col])

  mvp_stats = mvp_stats.set_index('Player')
  st.table(mvp_stats.style.format({"PTS" : "{:.2f}", 'TRB' : "{:.2f}", 'AST' : "{:.2f}", 'BLK' : "{:.2f}", 'STL' : "{:.2f}", 'FG%' : "{:.2%}", 'FT%' : "{:.2%}"}))


  st.image('./nikola.jpg')

  # st.balloons() 

  # st.dataframe(mvp_stats)

  # latest_iteration = st.empty()
  # bar = st.progress(0)

  # for i in range(100):
  #   latest_iteration.text(f'Iteration {i+1}')
  #   bar.progress(i + 1)
  #   time.sleep(0.1)
