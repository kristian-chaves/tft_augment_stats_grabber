from functions import *

top_player_list = []
augments = {}

# insert how many player pages desired - 
    # each page translates to 100 players
    # max pages: 10
player_pages = 10

# insert how many match pages you want to pull from
    # translates to 10 matches
    # accuracy of this metric heavily depends on
    # how recent the patch was - keeping it high
    # if a patch has recently released will result
    # in data from the previous patch being pulled
    # recommended amount: 4
match_pages = 4
    

if __name__ == '__main__':
    top_player_list = grab_top_players(player_pages)
    augments = grab_augment_list()
    augments = collect_augment_placements(player_pages, match_pages, top_player_list, augments)
    #augments = generate_average_score(augments)
    #output_stats(augments)
    print(f"data from {player_pages * 100 * match_pages * 10} matches pulled")
