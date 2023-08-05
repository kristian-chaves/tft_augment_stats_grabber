from bs4 import BeautifulSoup
from urllib.request import urlopen
#import re



def grab_top_players():
    top_player_list = []
    original_link = "https://lolchess.gg/leaderboards?mode=ranked&region=na&page="
    for page_number in range(1,11):

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

    print(top_player_list[999])
    print("grabbed top 1000 players")
    return top_player_list

def grab_augment_data():
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
