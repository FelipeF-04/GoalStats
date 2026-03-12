import requests
import pandas as pd
from io import StringIO 
from bs4 import BeautifulSoup
from time import sleep
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



urls = {"PremierLeague": "https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats",
        "LaLiga":"https://fbref.com/en/comps/12/La-Liga-Stats",
        "SeriaA":"https://fbref.com/en/comps/11/Serie-A-Stats",
        "Bundesliga":"https://fbref.com/en/comps/20/Bundesliga-Stats",
        "Ligue1": "https://fbref.com/en/comps/13/Ligue-1-Stats",
        "PrimeiraLiga": "https://fbref.com/en/comps/32/Primeira-Liga-Stats"
        }

id_maintable = {"PremierLeague": "results2024-202591_overall",
        "LaLiga":"results2024-2025121_overall",
        "SeriaA":"results2024-2025111_overall",
        "Bundesliga":"results2024-2025201_overall",
        "Ligue1": "results2024-2025131_overall",
        "PrimeiraLiga": "results2024-2025321_overall"
        }

script_dir = os.path.dirname(os.path.abspath(__file__))

for standings_url in urls:

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)###
    all_matches = []

    csv_path = os.path.join(script_dir, f"{standings_url}1.csv")

    driver.get(urls[standings_url])
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,"table.stats_table"))
    )
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser") 
    standings_table = soup.select("table.stats_table")[0]# straight html
    #print(standings_table)

    links = [l.get("href") for l in standings_table.find_all('a')]
    links = [l for l in links if '/squads/' in l] #/squads/ as part of the url
    

    matches = pd.read_html(StringIO(html), attrs={'id': id_maintable[standings_url]})#table id

    rk = matches[0]["Rk"]
    squads = matches[0]["Squad"]
    mp = matches[0]["MP"]
    pts = matches[0]["Pts"]
    goalscorer = matches[0]["Top Team Scorer"]

    #MY WAY:         
    #gls = matches[0]["GF"].copy().astype(float)
    #xG = matches[0]["xG"].copy().astype(float)
    ##print(gls[0]*2)
    #l = len(gls)
    #total_matches = ((l-1)*2)
    #
    #for i in range(l):
    #    gls[i] = round(gls[i]/total_matches,2)
    #
    #for i in range(l):
    #    xG[i] = round(xG[i]/total_matches,2)

    df = matches[0]
    matches = (len(df)-1)*2

    df["GF"] = (df["GF"]/matches).round(2)
    df["xG"] = (df["xG"]/matches).round(2)



    table = pd.DataFrame({"Position": rk,
                        "Team":squads,
                        "Mp":mp,
                        "Pts":pts,
                        "Top Scorer": goalscorer,
                        "Gls/90": df["GF"],
                        "xG/90": df["xG"]})

    table.columns = [c.capitalize() for c in table.columns]
    table.to_csv(csv_path,index=False)


    #The first table is ordered by performance(positions), the second one is alphabetically

    #extraStats = pd.read_html(StringIO(html), attrs={'id': "stats_squads_standard_for"})
    #
    #a = extraStats[0]["Per 90 Minutes"]
    #Gls = a["Gls"]
    #xG = a["xG"]
    #
    #table2 = pd.DataFrame({"Gls": Gls,
    #                       "xG": xG})
    
    #table = pd.concat([table,table2],axis=1)
    #table.columns = [c.capitalize() for c in table.columns]
    #table.to_csv(csv_path,index=False)


#notes:
#works but only with the first in the dictionary, the loop is not working


#PROTOTYPE
'''import requests
import pandas as pd
from io import StringIO 
from bs4 import BeautifulSoup
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

all_matches = []
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

driver.get(standings_url)
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR,"table.stats_table"))
)
html = driver.page_source
soup = BeautifulSoup(html,"html.parser") 
standings_table = soup.select("table.stats_table")[0]# straight html
#print(standings_table)

links = [l.get("href") for l in standings_table.find_all('a')]
links = [l for l in links if '/squads/' in l] #/squads/ as part of the url

matches = pd.read_html(StringIO(html), attrs={'id': "results2024-202591_overall"})
rk = matches[0]["Rk"]
squads = matches[0]["Squad"]
mp = matches[0]["MP"]
pts = matches[0]["Pts"]

table = pd.DataFrame({"Position": rk,
                      "Team":squads,
                      "Mp":mp,
                      "Pts":pts})

table.columns = [c.capitalize() for c in table.columns]
table.to_csv("pl.csv",index=False)
'''