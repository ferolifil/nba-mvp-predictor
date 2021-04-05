import streamlit as st
import time

st.write("""
# My first app
Hello *world!*
""")

# 'Starting a long computation...'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)
