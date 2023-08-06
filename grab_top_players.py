from bs4 import BeautifulSoup
from urllib.request import urlopen
#import re

#https://tftactics.gg/db/augments

def grab_top_players():
    top_player_list = []
    original_link = "https://lolchess.gg/leaderboards?mode=ranked&region=na&page="
    for page_number in range(1,2):

        url = original_link + str(page_number)
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        #anchors = [a for a in (td.find('a') for td in soup.findAll('td')) if a]
        for td in soup.findAll('td'):
            a = td.find('a')
            if a:
                top_player_list.append(a['href'])
        print(f"grabbed information from page {page_number}" )

    print("grabbed top 1000 players")
    return top_player_list

#creates an augment's data, called by grab augment data, returns a dictionary element
# if tier unknown, initialize as 4
def create_augment(tier):
    scores = []
    augment_data = [scores, 0, 0] 
    augment_data[1] = tier
    return augment_data

#collects all augments, adds to and returns dictionary
def grab_augment_data():
    augments = {}
    tier = 0;
    # augment info: string name, int list scores, int tier, int average
    augment_tiers = ["silver", "gold", "prismatic"]
    original_link = "https://bunnymuffins.lol/augments/"

    url = original_link
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    #three tables
    for table in soup.findAll("figure", {"class": "wp-block-table"}):
        for tr in table.findAll('tr'):
            #a = tr.contents
            a = (tr.find('td')).get_text()
            if a != "NAME":
                augments[a] = create_augment(tier)
        tier += 1
    print(f"all {augment_tiers[tier-1]} augments grabbed" )

    print("all augments added to list")
    return augments

def collect_augment_placements(top_player_list, augments):
    match_history = "/s9/matches/ranked/"
    player_count = 0
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
                    #check if the augment exists in the pre-generated list, if it doesnt, create it
                    if augment in augments:
                        #pretty ugly solution but couldn't figure out how to get around python adding multiple values in this location
                        temp_list_1 = augments[augment][0]
                        temp_list_2 = temp_list_1.copy()
                        temp_list_2.append(score)
                        augments[augment][0] = temp_list_2
                    else:
                        augments[augment] = create_augment(4)

        player_count+=1
        print(f"player: {player_count}")
    return augments
