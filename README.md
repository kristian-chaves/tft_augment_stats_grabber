# tft_augment_stats_grabber

mortdog taught me that stats are a lie and that i should never believe them

## project notes
tft dev team recently made augment winrate stats private. some friends of mine mentioned wanting to have access to the stats so this is an attempt to give them access to them. 

### random notes:
- data is output to the excel doc unsorted - you'll have to go into the document and sort the data
- program will (eventually) crash if excel file is open while running program
- data will probably be top 4 skewed on the basis that this data comes from the top 1000 players and because of how riot matchmaking works, these players will have to play in lobbies where most other players will be decently worse than them
- because this pulls from the last n*10 games played and not every top player is a degenerate rat, some data may be from previous patches. because of how decay works, this probably wont be too much of an issue, but i definitely saw some top players with like 70 or so ranked games played total this set, so chances are that some data may be outdated. i think as the set goes on, the average challenger lp will go up and degenerate rat players will be more incentivized for grabbing augment data
- some games only have 2, 1, or 0 augment entries because riot has fully privatized what hero augments are taken each game
- lolchess.gg doesnt have all augments on their augment page despite it being an "augment page". hero augments arent included (they're sorta manually added in the code), and legend augments arent included for reasons beyond me. that being said... if the augment is offered as its non legend augment variant, most of the time its not included. as a result, almost all of these are in the misc section, with the stats included there being almost exclusively the regular versions of these augments 
- some augments will have their stats skewed/inflated by low player counts.  id chalk this up to some top players having playstyles that orient heavily around these stats while other players avoid the augments because they might just not be good/heavily favour very specific playstyles
- some augments might actually be good, but not viable being played in these top lobbies. something like the draven stage 2 hero augments (spoils of war) might be in a good place, but odds are it wont play/perform well in a lobby entirely made of top players where skill gaps are a lot smaller than other elos
- honestly i think biggest take away working on this is that blindly following stats sorta oversimplifies the meaning of the stats. however conceding this means mortdog wins so i will blindly follow the stats 1st or 8th all day no thoughts head empty

## dependencies
- have python installed
- beautiful soup
- pandas
- XlxsWriter
- openpyxl
- installation instructions for zia:
  - ok so you wanna open up your command prompt, run it as administrator (type cmd in windows search -> right click and click 'run as administrator'), and then you wanna type pip install [dependency name here] - make sure you already have python installed and dont think about the consequences, there arent any consequences, why would there be consequences, trust me zia, this will have no (0) lasting consequences on your computer/python installation -- also you have access to tft stats now you can play like k3soju, dont you wanna be like k3soju, i know you wanna be like k3soju, just install the dependencies, dont think about it, just do it, you can do it, i believe in you, just be like soju, ez!

## potential future improvements for someone who forks this repository who isn't me because i do not wanna work on this anymore and soemone forking this repository would make the dopamine part of my brain go happy happy 
- the excel document that outputs the data doesnt have the code sorted. it can probably be sorted, but it'd take me like 30 mins of figuring it out, and imo the user can just sorta get around it with legit 12 clicks in excel - would be nice to have though 
- lolchess only holds the information of the top 1000 players, but the stats would be more accurate with more players. mobalytics does have information for i think approx the top ~22,000 players, so a potential solution could be to grab the username from mobalytics, append it to a url which is basically [lolchess url] + [username] + [lolchess match history specifications] + [page number], but when i tried implementing this at 5am i had issues with converting the html link using the openurl functions and i promptly fell asleep. in theory this can be worked around, i just got bored of the project before doing it - if you wanna work on this, i have some scuffed code in one of the previous versions with the name "mistake" - probably in the playground file
- the code in the collect_augment_placements function can take a while to run. i looked at the code and im p sure its a collection of O(1) and O(n) checks to a total of O(n) runtime, but also someone smarter than me could probably figure out a way to optimize this code
- stats in the misc section dont have an attached augment rarity attached to them and i couldn't really figure out an intuitive way of getting them. lolchess lists the legend augments without the rarity attached in the html. My best guess would be cross-referencing across multiple augment repositories but a lot of sources dont host the information the same way - like ik bunnymuffins hosts the entry for endless hordes as "endless horde" which caused some checks to fail. there's probs a solution here, but i dont know what it is
