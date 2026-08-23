#The purpose of this file is to scrape wiki.leagueoflegends.com for information on "Adaptive Type" in the Wild Rift tab of the champion profile

#required imports
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

def main():
    champ_name = input("Enter champion name: ").strip()
    adaptive_type = get_adaptive_type(champ_name)
    print('Adaptive type: ', adaptive_type)

main()
