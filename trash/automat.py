# import webdriver 
from selenium import webdriver 
   
# import Action chains  
from selenium.webdriver.common.action_chains import ActionChains 

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

import pandas as pd
import time

# options = Options()
# options.add_experimental_option("prefs", {
#   "download.default_directory": r"/home/fernando/Downloads",
#   "download.prompt_for_download": False,
#   "download.directory_upgrade": True,
#   "safebrowsing.enabled": True
# })

# driver = webdriver.Chrome()
# season = str(1980)

# driver.get('https://www.basketball-reference.com/leagues/NBA_' + season + '_totals.html')
# time.sleep(2)
# driver.maximize_window()
# time.sleep(2)
# menu = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[3]/div[1]/div/ul/li[1]/span')
# hidden_submenu = driver.find_element_by_xpath('/html/body/div[2]/div[5]/div[3]/div[1]/div/ul/li[1]/div/ul/li[4]/button')
# ActionChains(driver).move_to_element(menu).double_click(hidden_submenu).perform() 


"""
takes in a specific player url and scrapes the career averages from the per game table.
must use in conjunction with `get_pergame_cols` in order to sync the columns.
"""
driver = webdriver.Chrome()

url = 'https://www.basketball-reference.com/leagues/NBA_1980_totals.html'
driver.get(url)

# share & more
driver.find_element_by_xpath("""//*[@id="totals_stats_sh"]/div/ul/li[1]/span""").click()

# get table as csv (for excel)
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, """//*[@id="totals_stats_sh"]/div/ul/li[1]/div/ul/li[3]/button"""))).click()

# table
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CLASS_NAME, """table_outer_container""")))

# capture csv text
per_game = driver.find_element_by_id("csv_per_game")

# data cleaning
per_game = per_game.text.encode('ascii', 'ignore').split()

for stats in per_game:
    if stats.startswith('Career'):
        per_game = re.findall('(\\d[\\d.,-]+)$', stats)[0]

player_id = re.findall('(\\w+\\d)', url)

per_game_list = [player_id[0]]
for i in per_game.split(','):
    if i == '':
        per_game_list.append(0.0)
    else:
        i = float(i)
        per_game_list.append(i)

print(per_game_list)


