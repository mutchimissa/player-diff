import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

#creating functions to edit 
#fixes weird champ names (e.g. Kha'zix, Dr. Mundo, Aurelion Sol)
def name_formatter(champ_name): 
    champ_name = champ_name.strip()
    champ_name = champ_name.replace(" ", "_")
    champ_name = quote(champ_name)
    return champ_name

def get_html(champ_name):
    formatted_name = name_formatter(champ_name)
    url = f"https://wiki.leagueoflegends.com/en-us/WR:{formatted_name}"
    print("Fetching ", url)

    response = requests.get(url)
    response.raise_for_status() #check if html request successful
    return response.text

def get_adaptive_type(champ_name):
    html = get_html(champ_name)
    soup = BeautifulSoup(html, 'html.parser')

    label = soup.find("div", class_="infobox-data-label", string="Adaptive type")

    if label is None:
        return "Adaptive type not found"
    
    row = label.parent
    row_text = row.get_text(" ", strip=True)

    #There are only 2 Adaptive types: Magic or Physical
    if "Magic" in row_text:
        return "Magic"
    elif "Physical" in row_text:
        return "Physical"
    else:
        return "Unknown"

url = 'https://game.gtimg.cn/images/lgamem/act/lrlib/js/heroList/hero_list.js'

response = requests.get(url)
response.raise_for_status()
hero_data = response.json()

champ_id_map = {}

#Normalizing all names to be lowercase with no special characters
def norm_name(name):
    name = name.lower()
    name = name.replace(" ", "")
    name = name.replace(".", "")
    name = name.replace("'", "")
    return name

#WR stats has each champ = a champ ID and its in chinese so we use the jpg name (e.g. Garen_0.jpg) to map each champ to their champ ID
for hero_id, hero_info in hero_data["heroList"].items():
    poster_url = hero_info["poster"]
    filename = poster_url.split("/")[-1]
    eng_name = filename.rsplit("_", 1)[0]
    clean_name = norm_name(eng_name)
    champ_id_map[clean_name] = hero_id

#containts wr and champ ids
rank_url = 'https://mlol.qt.qq.com/go/lgame_battle_info/hero_rank_list_v2'
rank_response = requests.get(rank_url)
rank_response.raise_for_status()
rank_data = rank_response.json()

#there's actually a rank 0 that doesn't show on the website but I didn't include it
rank_map = {
    "diamond+": "1",
    "master+": "2",
    "challenger+": "3",
    "sovereign": "4"
}

position_map = {
    "mid": "1",
    "middle": "1",
    "top": "2",
    "bottom": "3",
    "support": "4",
    "jungle": "5"
}

lolalytics_role_map = {
    "mid": "middle",
    "middle": "middle",
    "top": "top",
    "bottom": "bottom",
    "support": "support",
    "jungle": "jungle"
}

#function that gathers champ info 
def get_wr(champ_name, role, rank_group="diamond+"): #e.g. (Nautilus, support, diamond+)
    hero_id = champ_id_map[norm_name(champ_name)] #convert to id and position + rank keys
    position = position_map[role.lower()]
    rank_key = rank_map[rank_group.lower()]

    for champ in rank_data['data'][rank_key][position]:
        if champ["hero_id"] == hero_id:
            return champ["win_rate_percent"]
    return None

def find_lola_url(champ_name, role):
    champ_web = name_formatter(champ_name)
    lola_role =lolalytics_role_map[role.lower()]
    url = f"https://lolalytics.com/lol/{champ_web.lower()}/counters/?lane={lola_role}&patch=30"
    return url

#extracting html from champ's lolalytics page
def get_anal_html(player_champ, role):
    url = find_lola_url(player_champ, role)
    print("Fetching...", url)
    response = requests.get(url)
    response.raise_for_status()
    return response.text


#find and extract the matchup information
def get_matchwr(player_champ, enemy_champ, role):
    html = get_anal_html(player_champ, role)
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
        return "Matchup WR not found"

def display_results(
    role,
    enemy_champ,
    enemy_adaptive_type,
    enemy_wr,
    my_champ,
    my_wr,
    matchup_wr
):

    print("\n" + "=" * 40)
    print("MATCHUP SUMMARY")
    print("=" * 40)

    print(f"\nRole: {role.title()}")

    print("\nENEMY")
    print(f"Champion: {enemy_champ.title()}")
    print(f"Adaptive Type: {enemy_adaptive_type}")
    print(f"Win Rate: {enemy_wr}%")

    print("\nYOU")
    print(f"Champion: {my_champ.title()}")
    print(f"Win Rate: {my_wr}%")

    print("\nMATCHUP")
    print(
        f"{my_champ.title()} vs "
        f"{enemy_champ.title()}: {matchup_wr}"
    )

    print("=" * 40)

#defining what main() does --> inputs for role, enemy, player + logic
def main():
    role = input("Role assigned:")
    enemy_champ = input("Lane opponent:")
    my_champ = input("Champion selected:")

    enemy_adaptive_type = get_adaptive_type(enemy_champ)

    player_champ = my_champ.strip()
    lane = role.strip().lower()
    enemy_champ = enemy_champ.strip()

    player_wr = get_wr(player_champ, lane)
    enemy_wr = get_wr(enemy_champ, lane)
    matchup_wr = get_matchwr(player_champ, enemy_champ,  role)

    display_results(
        role=role,
        enemy_champ=enemy_champ,
        enemy_adaptive_type=enemy_adaptive_type,
        enemy_wr=enemy_wr,
        my_champ=my_champ,
        my_wr=player_wr,
        matchup_wr=matchup_wr
    )

main()
