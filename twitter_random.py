# twitter_random.py -- Visits a random person from twitter_following.txt, which can be generated with twitter_update_followers.py
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import os
import random
import webbrowser

tweets_only = True  # Set this to False to default to visiting the friend's page directly.

friends = open(os.path.dirname(__file__) + '\\twitter_following.txt', 'r')
lines = friends.readlines()
friends.close()

print('Press Enter to visit a random friend, Q (then enter) to exit, or T to toggle tweets-only (no retweets) mode.')
print('Tweets-only mode is currently', 'enabled.' if tweets_only else 'disabled.')
while True:
    key = input()
    if (len(key)):
        if (key[0] == 'q' or key[0] == 'Q'):
            print('Goodbye!')
            exit()
        elif (key[0] == 't' or key[0] == 'T'):
            tweets_only = not tweets_only
            print('Tweets-only mode is currently', 'enabled.' if tweets_only else 'disabled.')
        else:
            print('Press Enter to visit a random friend, Q (then enter) to exit, or T to toggle tweets-only (no retweets) mode.')
    else:
        fren = random.choice(lines).strip('\n')
        print('Visiting ' + fren + '!')
        if tweets_only: webbrowser.open('https://twitter.com/search?q=from%3A' + fren + '&src=typed_query&f=live')
        else: webbrowser.open('https://twitter.com/' + fren)
