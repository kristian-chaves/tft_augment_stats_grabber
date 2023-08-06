from bs4 import BeautifulSoup
from urllib.request import urlopen
from statistics import mean 
import pandas as pd

from grab_top_players import *

augments = grab_augment_data()

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

