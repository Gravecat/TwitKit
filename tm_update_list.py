# tm_update_list.py -- Reads the twitter_following.txt (from Twitter) and following_accounts.csv
# (from Mastodon) files, and condenses them into a single list of followed people
# (tm_combined_following.txt) in random order.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import csv
import os
import random
import twitkit_common as tk


def main():
    wait_before_exit = True     # Set this to False to no longer wait for the user to press Enter before exiting.
    twitter_friends = list(tk.txt_to_set('twitter_following.txt'))
    
    with open(os.path.dirname(__file__) + '/following_accounts.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    masto_friends = []
    for entry in data:
        if entry[0] != "Account address":
            masto_friends.append(entry[0])
    
    combined_friends = twitter_friends + masto_friends;
    random.shuffle(combined_friends)
    
    tk.set_to_txt('tm_combined_following.txt', combined_friends)
    
    print('Updated combined following list with %s friends!' % len(combined_friends))

    tk.done(wait_before_exit)


if __name__ == '__main__': main()
