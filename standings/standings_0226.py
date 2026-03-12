import pandas as pd
from bs4 import BeautifulSoup
import os
import time

from seleniumbase import Driver


urls = {"PremierLeague": "https://fbref.com/en/comps/9/Premier-League-Stats",
        "LaLiga":"https://fbref.com/en/comps/12/La-Liga-Stats",
        "SeriaA":"https://fbref.com/en/comps/11/Serie-A-Stats",
        "Bundesliga":"https://fbref.com/en/comps/20/Bundesliga-Stats",
        "Ligue1": "https://fbref.com/en/comps/13/Ligue-1-Stats",
        "PrimeiraLiga": "https://fbref.com/en/comps/32/Primeira-Liga-Stats"
        }

id_maintable = {"PremierLeague": "results2025-202691_overall",
        "LaLiga":"results2025-2026121_overall",
        "SeriaA":"results2025-2026111_overall",
        "Bundesliga":"results2025-2026201_overall",
        "Ligue1": "results2025-2026131_overall",
        "PrimeiraLiga": "results2025-2026321_overall"
        }


script_dir = os.path.dirname(os.path.abspath(__file__))

for standings_url in urls:

    driver = Driver(uc=True)

    csv_path = os.path.join(script_dir, f"{standings_url}26.csv")

    driver.get(urls[standings_url])
    driver.uc_gui_click_captcha()
    time.sleep(10)
    driver.wait_for_element("table.stats_table")
    time.sleep(10)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    table_el = soup.find("table", {"id": id_maintable[standings_url]})
    rows = [r for r in table_el.select("tbody tr") if r.find("td")]

    def cell(row, stat):
        el = row.find(attrs={"data-stat": stat})
        return el.get_text(strip=True) if el else ""

    records = []
    for row in rows:
        records.append({
            "Position": cell(row, "rank"),
            "Team":     cell(row, "team"),
            "Mp":       cell(row, "games"),
            "Pts":      cell(row, "points"),
            "Top scorer": cell(row, "top_team_scorers"),
            "Gls/90":   cell(row, "goals_for"),
        })

    df = pd.DataFrame(records)
    n_teams = len(df)
    #matches_per_team = (n_teams - 1) * 2

    df["Gls/90"] = (pd.to_numeric(df["Gls/90"], errors="coerce") / pd.to_numeric(df["Mp"], errors="coerce")).round(2)
    #df["Xg/90"]  = (pd.to_numeric(df["Xg/90"],  errors="coerce") / matches_per_team).round(2)

    df.to_csv(csv_path, index=False)

    time.sleep(10)
