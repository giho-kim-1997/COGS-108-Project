import json
import requests
from bs4 import BeautifulSoup


URL = "https://www.worldfootball.net/players_list/eng-premier-league-{}-{}/nach-groesse/{}/"


def extract_players_from_page(start_y, page):
    """Return None if page doesn't exists"""
    soccer_html = requests.get(URL.format(start_y, start_y + 1, page))
    soup = BeautifulSoup(soccer_html.text, features="html.parser")
    players = []
    for row in soup.find_all("tr"):
        toks = row.text.split("\n")
        if len(toks) != 10:
            continue
        name, team, born, height, position = toks[1], toks[5], toks[6], toks[7], toks[8]
        try:
            players.append([name, start_y, team, born, int(height[:3]), position])
        except ValueError:
            pass  # When height is ???

    print(f"extracted {len(players)} players from {start_y} page {page}")
    return players


def extract_start_year(start_y):
    """Player Class"""
    print(f"extracting year {start_y}")
    players = []
    for page in range(1, 100):
        cur_players = extract_players_from_page(start_y, page)
        if len(cur_players) == 0:
            break  # Last page
        players.extend(cur_players)
    return players


if __name__ == "__main__":
    all_players = []
    for y in range(1950, 2022):
        all_players.extend(extract_start_year(y))

    with open("a.json", "w") as f:
        json.dump(all_players, f)
