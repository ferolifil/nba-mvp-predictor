import streamlit as st
import time
from lib.scrap import scrap_latest
from lib.std import std_latest
from lib.model import limit_calc, pred_latest
import pandas as pd
import numpy as np
from pyngrok import ngrok

def main():

  img_dict = {
    'Nikola Jokić' : 'nikola.jpg', 
    'James Harden' : 'harden.jpg', 
    'Joel Embiid' : 'joel.jpg', 
    'Damian Lillard' : 'dame.jpg' , 
    'Kawhi Leonard' : 'kawhi.jpg', 
    'Giannis Antetokounmpo' : 'giannis.jpg', 
    'Kevin Durant' : 'kd.jpg', 
    'Kyrie Irving' : 'kyrie.jpg', 
    'LeBron James' : 'lbj.jpg', 
    'Luka Dončić' : 'luka.jpg', 
    'Rudy Gobert' : 'rudy.jpg'  }

  season = 2021

  st.write("""
  # NBA MVP Predictor
  """)

  submit = st.button('Start now')
  if submit:

    scrap_latest(season)
    nba2021 = std_latest(season)
    df_top5, mvp_stats = pred_latest()   

    mvp = mvp_stats.iat[0,0]  
    print(mvp)

    st.table(df_top5)

    mvp_stats = mvp_stats.set_index('Player')
    st.table(mvp_stats.style.format({"PTS" : "{:.2f}", 'TRB' : "{:.2f}", 'AST' : "{:.2f}", 'BLK' : "{:.2f}", 'STL' : "{:.2f}", 'FG%' : "{:.2%}", 'FT%' : "{:.2%}"}))

    st.image('./img/{}'.format(img_dict[mvp]))

  try:
    public_url = ngrok.connect('8501')
  except:
    pass

if __name__ == "__main__":
    main()