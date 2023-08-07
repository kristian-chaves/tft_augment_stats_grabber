from bs4 import BeautifulSoup
from urllib.request import urlopen
from grab_top_players import *


"""
hosting alternative functions here in case theres an issue with implementation
"""


#lolchess.gg doesnt givee all augments and adding them manually just isnt working/makes me deeply unhappy
#nvm i found a workaround, lolchess may be optimal
def grab_augment_list():
    augments = {}
    scores = []
    # augment info: string name, int list scores, int tier, int average
    augment_data = [scores, 0, 0] 
    augment_tiers = ["silver", "gold", "prismatic"]
    original_link = "https://lolchess.gg/guide/augments/set9?tier="

    for tier in range(1,4):
        url = original_link + str(tier)
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        for x in soup.findAll("h3", {"class": "guide-augments__title"}):
            a = x.contents
            if a:
                augment_data[1] = tier - 1;
                augments[a[0].strip()] = augment_data.copy()
                #augments.append(augment_data.copy())
        print(f"all {augment_tiers[tier-1]} augments grabbed" )

    #some augments are missing for some reason, just add them in here
    #for future make this part more automated
    #Medium Forge:
    augment_data = [scores, 0, 0]
    augments["Job's Done"] = augment_data.copy()
    augments["Small Forge"] = augment_data.copy()
    augments["Medium-End Shopping"] = augment_data.copy()
    augments["Knowledge Download"] = augment_data.copy()
    augments["It Pays To Learn"] = augment_data.copy()
    augments["Seeing Double I"] = augment_data.copy()
    augments["Tiny Grab Bag"] = augment_data.copy()
    augments["Rolling For Days I"] = augment_data.copy()

    augment_data = [scores, 1, 0]
    augments["Medium Forge"] = augment_data.copy()
    augments["The Boss"] = augment_data.copy()
    augments["Riftwalk"] = augment_data.copy()
    augments["Winds of War"] = augment_data.copy()
    augments["Demonflare"] = augment_data.copy()
    augments["Ravenous Hunter"] = augment_data.copy()
    augments["Job Well Done"] = augment_data.copy()
    augments["Knowledge Download II"] = augment_data.copy()
    augments["It Pays to Learn II"] = augment_data.copy()
    augments["Big Grab Bag"] = augment_data.copy()
    augments["Seeing Double II"] = augment_data.copy()
    augments["Rolling For Days II"] = augment_data.copy()
    augment_data = [scores, 2, 0]
    augments["Well-Earned Comforts III"] = augment_data.copy()
    augments["Large Forge"] = augment_data.copy()
    augments["Masterful Job"] = augment_data.copy()
    augments["Knowledge Download III"] = augment_data.copy()
    augments["It Pays to Learn III"] = augment_data.copy()
    augments["Seeing Double III"] = augment_data.copy()
    augments["Giant Grab Bag"] = augment_data.copy()
    augments["Rolling For Days III"] = augment_data.copy()


    
    print("all augments added to list")
    return augments


def grab_augment_list_2():
    augments = {}
    tier = 0;
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
                augments[a] = create_augment(tier, 0)
        tier += 1
        print(f"all {augment_tiers[tier-1]} augments grabbed" )

    print("all augments added to list")
    return augments

#grab top players from lolchess.gg
def grab_top_players(player_pages):
    top_player_list = []
    original_link = "https://lolchess.gg/leaderboards?mode=ranked&region=na&page="
    for page_number in range(1,player_pages+1):

        url = original_link + str(page_number)
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        #anchors = [a for a in (td.find('a') for td in soup.findAll('td')) if a]
        for td in soup.findAll('td'):
            a = td.find('a')
            if a:
                top_player_list.append(a['href'])
        print(f"grabbed information from player page {page_number}" )

    print(f"grabbed top {player_pages*100} players")
    return top_player_list

#version that works with grab_top_players using lolchess
def collect_augment_placements(match_pages, top_player_list, augments):
    match_history = "/s9/matches/ranked/"
    player_count = 0
    for link in top_player_list:
        for x in range(1, match_pages+1):
            url = link + match_history + str(x)
            sleep = 0
            for i in range(4):
                try:
                    html = urlopen(url).read()
                    break
                except:
                    if i==3:
                        raise
                    time.sleep(sleep)
                    sleep += 5
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
                    augment = (augment_data[y].find('img', alt=True))['alt']
                    #check if the augment exists in the pre-generated list, if it doesnt, create it
                    if augment in augments:
                        #pretty ugly solution but couldn't figure out how to get around python adding multiple values in this location
                        augments[augment][0].append(score)
                    else:
                        augments[augment] = create_augment(3, score)
                        
        player_count+=1
        print(f"player: {player_count}")
        # every 100 data pulls, back up all data
        if(player_count % 100 == 0):
            augments = generate_average_score(augments)
            output_stats(augments)
    return augments
