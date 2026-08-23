import requests

url = 'https://mlol.qt.qq.com/go/lgame_battle_info/hero_rank_list_v2'

response = requests.get(url)
data = response.json()

print(data.keys())
print(data["data"].keys())
print(data["data"]["0"].keys())

for position_key in data["data"]["0"]:
    print("Position:", position_key)
    champs = data["data"]["0"][position_key]
    for champ in champs[:5]:
        print(champ)

    print()
