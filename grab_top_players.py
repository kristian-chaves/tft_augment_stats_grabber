from bs4 import BeautifulSoup
from urllib.request import urlopen
from statistics import mean 
import pandas as pd
import time
#import re

#https://tftactics.gg/db/augments

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

#creates an augment's data, called by grab augment data, returns a dictionary element
# if tier unknown, initialize as 3
def create_augment(tier, score_entry):
    # augment info: int list scores, int tier, int average
    scores = []
    augment_data = [scores, 0, 0] 
    augment_data[1] = tier
    if(score_entry != 0):
        augment_data[0].append(score_entry)
    return augment_data

#collects all augments, adds to and returns dictionary
def grab_augment_list():
    augments = dict()
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
                augments[a[0].strip()] = create_augment(tier-1, 0)

        print(f"all {augment_tiers[tier-1]} augments grabbed" )
    # add hero augments - not included in lolchess add for some reason
    hero_augments = ["The Boss", "Riftwalk", "Winds of War", "Demonflare", "Ravenous Hunter"]
    for x in hero_augments:
        augments[x] = create_augment(1, 0)
    print("all augments added to list")
    return augments

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

def generate_average_score(augments):
    for x in augments:
        if(len(augments[x][0]) > 0 ):
            augments[x][2] = round(mean(augments[x][0]), 2)
    return augments

def create_excel_column():
    tier_augments =  {"Augment": [], "Average Winrate": [], "Sample Size": []}
    return tier_augments

def add_augment_data(tier_augment, augments, x):
    tier_augment["Augment"].append(x) 
    tier_augment["Average Winrate"].append(augments[x][2])
    tier_augment["Sample Size"].append(len(augments[x][0]))
    return tier_augment

def output_stats(augments):
    silver_augments = create_excel_column()
    gold_augments = create_excel_column()
    prismatic_augments = create_excel_column()
    misc_augments = create_excel_column()
    augment_collections = [silver_augments, gold_augments, prismatic_augments, misc_augments]
    
    for x in augments:
        augment_collections[augments[x][1]] = add_augment_data(augment_collections[augments[x][1]], augments, x)
    
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
        worksheet.set_column(2, 2, 15)    
    writer.close()

