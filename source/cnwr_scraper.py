import requests

#contains list of champs and their respective ids
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
    "top": "2",
    "bottom": "3",
    "support": "4",
    "jungle": "5"
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

#user input
player_champ = input("Your champion: ").strip()
lane = input("Your lane/role: ").strip().lower()
enemy_champ = input("Lane opponent: ").strip()

player_wr = get_wr(player_champ, lane)
enemy_wr = get_wr(enemy_champ, lane)
print()
print("Current Matchup Information (Diamond+):")
print("Player: ", player_champ, "|", "WR:", player_wr, "%")
print("Enemy: ", enemy_champ, "|", "WR:", enemy_wr, "%")
