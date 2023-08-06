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
