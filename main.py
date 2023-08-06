from grab_top_players import *

top_player_list = []
augments = {}


if __name__ == '__main__':
    print("w")
    top_player_list = grab_top_players()
    augments = grab_augment_data()
    augments = collect_augment_placements(top_player_list, augments)
    print("done")
