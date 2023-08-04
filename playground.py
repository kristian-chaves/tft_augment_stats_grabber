from bs4 import BeautifulSoup
from urllib.request import urlopen

augments = []
scores = []
# augment info: string name, int list scores, int tier, int average
augment_info = ["name", scores, 0, 0] 
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
            augment_info[0] = a[0].strip()
            augment_info[2] = tier - 1;
            augments.append(augment_info.copy())
    print(f"all {augment_tiers[tier-1]} augments grabbed" )

print("all augments added to list")
