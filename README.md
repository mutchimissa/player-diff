# player-diff
## Overview (Never played League):
League of Legends is a competitive multiplayer online game where 5 players (with different roles) on 2 teams try to win through completing different strategic objectives. League of Legends: Wild Rift is the mobile port of the original PC game. Players choose from a pool of over a hundred champions with varying skills, synergy and competitive value. By using Python-based web-scraping, this program returns information on the type of damage your opponent (i.e. the player on the other team who has the same role as you) deals, your champion's win rate and your champion's win rate against your opponent's champion.

## Overview (Plays League):
Web scraper that scrapes the LoL Wiki, Wild Rift official site and LoLalytics for adaptive type, individual win rate and matchup win rate from user input.

This is for use with Wild Rift only! Not PC League (because OP works min wage and cannot afford a PC).

Uses Python, requests and BeautifulSoup

## How to run:
1. input your role (ONLY INPUT ONE OF THESE: top, bottom, jungle, mid, middle, support)
2. input your champ and your opponent's; if the name contains punctuation PUT IT IN (E.g. Dr. Mundo, Kai'sa)
3. press enter

if it doesn't work or does not give full results, possible causes are as follows:
1. you are playing (or against) wukong (haven't gotten to fixing issue with him yet)
2. you inputted the role or name in the wrong format (refer to above)
3. some issue with the URLs
