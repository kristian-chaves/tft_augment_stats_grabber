# beauty_soup.py

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

top_player_list = []
original_link = "https://lolchess.gg/leaderboards?mode=ranked&region=na&page="
for page_number in range(1,11):

    url = original_link + str(page_number)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    anchors = [a for a in (td.find('a') for td in soup.findAll('td')) if a]
    for x in anchors:
        top_player_list.append(x['href'])

print(top_player_list[999])
print("grabbed top 1000 players")
