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
    augments = []
    scores = []
    # augment info: string name, int list scores, int tier, int average
    augment_data = ["name", scores, 0, 0] 
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
                augment_data[0] = a[0].strip()
                augment_data[2] = tier - 1;
                augments.append(augment_data.copy())
        print(f"all {augment_tiers[tier-1]} augments grabbed" )

    print("all augments added to list")
    return augments

