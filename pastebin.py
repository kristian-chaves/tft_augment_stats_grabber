from bs4 import BeautifulSoup
from urllib.request import urlopen

from grab_top_players import *

#top_player_list = grab_top_players()
top_player_list = grab_top_players()
match_history = "/s9/matches/ranked/"
#augments = grab_augment_data()

print("data grabbed")

augments = grab_augment_list()
score = 0
# augment info: string name, int list scores, int tier, int average
#augment_data = ["name", scores, 0, 0] 
n = 0
for link in top_player_list:
    for x in range(1, 4):

        url = link + match_history + str(x)
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        matches = soup.find("div", {"class": "profile__match-history-v2__items"}).contents
        #lines 0,2,...,40 are blank, lines 3,7,...,39 is item data
        for x in range(1, 41, 4):
            match = matches[x].contents
            #placement is at index 01, augments at 07
            placement_data = (match[1].contents)
            score = int((placement_data[1].string).replace("#", ""))
            augment_data = match[7].contents
            #check length, then add based on appearances
            for y in range(1, len(augment_data), 2):
                augment =  "\n".join([img['alt'] for img in augment_data[y].find_all('img', alt=True)])
                #pretty ugly solution but couldn't figure out how to get around python adding multiple values in this location
                temp_list_1 = augments[augment][0]
                temp_list_2 = temp_list_1.copy()
                temp_list_2.append(score)
                augments[augment][0] = temp_list_2
    n+=1
    print(f"player: {n}")

print(f"all augments grabbed" )


