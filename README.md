# player-diff
Web scraper that scrapes the LoL Wiki, Wild Rift official site and LoLalytics for adaptive type, individual win rate and matchup win rate from user input.

This is for use with Wild Rift only! Not PC League (because OP works min wage and cannot afford a PC).

uses Python, requests and BeautifulSoup

How to run:
1. input your role (ONLY INPUT ONE OF THESE: top, bottom, jungle, mid, middle, support)
2. input your champ and your opponent's; if the name contains punctuation PUT IT IN (E.g. Dr. Mundo, Kai'sa)
3. press enter

if it doesn't work or does not give full results, possible causes are as follows:
1. you are playing (or against) wukong (haven't gotten to fixing issue with him yet)
2. you inputted the role or name in the wrong format (refer to above)
3. some issue with the URLs
