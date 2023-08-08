from bs4 import BeautifulSoup
from urllib.request import urlopen
from statistics import mean 
import pandas as pd

from grab_top_players import *

match_pages = 1
top_player_list = grab_top_players(1)
augments = grab_augment_list()

<<<<<<< HEAD
<<<<<<< HEAD
def collect_augment_placements(match_pages, top_player_list, augments):
    match_history_1 = "https://lolchess.gg/profile/na/"
    match_history_2 = "/s9/matches/ranked/"
    player_count = 0
    for player in top_player_list:
        for x in range(1, match_pages+1):
            valid_url = True
            url = match_history_1 + str(player) + match_history_2 + str(x)
            sleep = 0
            for i in range(4):
                try:
                    html = urlopen(url).read()
                    break
                except:
                    if i==3:
                        valid_url = False
                        break
                    time.sleep(sleep)
                    sleep += 2
            if valid_url == True:
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

augments = collect_augment_placements(match_pages, top_player_list, augments)
=======
silver_augments = {"Augment": [],
                   "Average Winrate": []}
gold_augments = {"Augment": [],
                 "Average Winrate": []}
prismatic_augments = {"Augment": [],
                      "Average Winrate": []}
misc_augments = {"Augment": [],
                 "Average Winrate": []}
=======
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
>>>>>>> parent of a8414e8 (Collect Augment Placement Optimization)

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
>>>>>>> parent of a8414e8 (Collect Augment Placement Optimization)

print("w")