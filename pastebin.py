from bs4 import BeautifulSoup
from urllib.request import urlopen

from grab_top_players import *

#top_player_list = grab_top_players()
top_player_list = ["https://lolchess.gg/profile/na/d%C4%B1shsoap", "https://lolchess.gg/profile/na/casparwu"]
match_history = "/s9/matches/ranked/"
#augments = grab_augment_data()

print("data grabbed")

augments = grab_augment_data()
scores = []
# augment info: string name, int list scores, int tier, int average
augment_data = ["name", scores, 0, 0] 
for link in top_player_list:
    for x in range(1, 11):

        url = link + match_history + str(x)
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
