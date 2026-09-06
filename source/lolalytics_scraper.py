#required imports
import requests
from bs4 import BeautifulSoup

#normalize champ's name
def name_formatter(champ_name):
    champ_name = champ_name.strip().lower()
    champ_name = champ_name.replace(" ", "")
    champ_name = champ_name.replace(".", "")
    champ_name = champ_name.replace("'", "")
    return champ_name

def find_lola_url(champ_name, role):
    champ_web = name_formatter(champ_name)
    url = f"https://lolalytics.com/lol/{champ_web}/counters/?lane={role}&patch=30"
    return url

#extracting html from champ's lolalytics page
def get_html(player_champ, role):
    url = find_lola_url(player_champ, role)
    print("Fetching...", url)
    response = requests.get(url)
    response.raise_for_status()
    return response.text


#find and extract the matchup information
def get_matchwr(player_champ, enemy_champ, role):
    html = get_html(player_champ, role)
    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    page_text_l = page_text.lower()
    enemy = enemy_champ.strip()
    search = f"{player_champ.lower()} wins against {enemy.lower()}"
    index = page_text_l.find(search)
    if index == -1:
        return "No Matchup/Insufficient Data"
    snip = page_text[index:index + 120]
    words = snip.split()
    if len(words) >= 5:
        return words[4]
    else:
        return "Matchup WR not found"#fixed url finder


#get player input
def main():
    player_champ = input("Your champion: ").strip()
    enemy_champ = input("Lane opponent: ").strip()
    role = input("Your lane/role: ").strip().lower()
    matchup = get_matchwr(player_champ, enemy_champ,  role)
    print(matchup)

main()

#To-do: fix the url editing, some champs have their lane in their url since it isn't their main role
