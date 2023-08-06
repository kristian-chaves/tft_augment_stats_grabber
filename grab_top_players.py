from bs4 import BeautifulSoup
from urllib.request import urlopen
from statistics import mean 
import pandas as pd
#import re

#https://tftactics.gg/db/augments

def grab_top_players(pages):
    top_player_list = []
    original_link = "https://lolchess.gg/leaderboards?mode=ranked&region=na&page="
    for page_number in range(1,pages+1):

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

    print(f"grabbed top {pages*100} players")
    return top_player_list

#creates an augment's data, called by grab augment data, returns a dictionary element
# if tier unknown, initialize as 3
def create_augment(tier):
    # augment info: int list scores, int tier, int average
    scores = []
    augment_data = [scores, 0, 0] 
    augment_data[1] = tier
    return augment_data

#collects all augments, adds to and returns dictionary
def grab_augment_data():
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
                augments[a] = create_augment(tier)
        tier += 1
    print(f"all {augment_tiers[tier-1]} augments grabbed" )

    print("all augments added to list")
    return augments

def collect_augment_placements(matches, top_player_list, augments):
    match_history = "/s9/matches/ranked/"
    player_count = 0
    for link in top_player_list:
        for x in range(1, matches+1):

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
                        augments[augment] = create_augment(3)

        player_count+=1
        print(f"player: {player_count}")
    return augments

def generate_average_score(augments):
    for x in augments:
        augments[x][2] = round(mean(augments[x][0]), 2)
        return augments


def output_stats(augments):
    silver_augments = {"Augment": [],
                   "Average Winrate": []}
    gold_augments = {"Augment": [],
                    "Average Winrate": []}
    prismatic_augments = {"Augment": [],
                        "Average Winrate": []}
    misc_augments = {"Augment": [],
                    "Average Winrate": []}

    for x in augments:
        if augments[x][1] == 0:
            silver_augments["Augment"].append(x) 
            silver_augments["Average Winrate"].append(augments[x][2])
        elif augments[x][1] == 1:
            gold_augments["Augment"].append(x) 
            gold_augments["Average Winrate"].append(augments[x][2])
        elif augments[x][1] == 2:
            prismatic_augments["Augment"].append(x) 
            prismatic_augments["Average Winrate"].append(augments[x][2])
        elif augments[x][1] == 3:
            misc_augments["Augment"].append(x) 
            misc_augments["Average Winrate"].append(augments[x][2])

    df1 = pd.DataFrame(silver_augments)
    df2 = pd.DataFrame(gold_augments)
    df3 = pd.DataFrame(prismatic_augments)
    df4 = pd.DataFrame(misc_augments)

    path = "augment_data.xlsx"
    sheets = [df1, df2, df3, df4]
    tier = ["silver", "gold", "prismatic", "misc"]

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for x in range(0,4):
        sheets[x].to_excel(writer, sheet_name=tier[x], index = False)
        column_width = 25
        worksheet = writer.sheets[tier[x]]
        worksheet.set_column(0, 1, column_width)    
    writer.close()

