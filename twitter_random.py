# twitter_random.py -- Visits a random person from twitter_following.txt, which can be generated with twitter_update_followers.py
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import os
import random
import webbrowser

friends = open(os.path.dirname(__file__) + '\\twitter_following.txt', 'r')
lines = friends.readlines()
friends.close()

print('Press Enter to visit a random friend, or anything else (then enter) to exit.')
while True:
    key = input()
    if (len(key)):
        print('Goodbye!')
        exit()
    fren = random.choice(lines).strip('\n')
    print('Visiting ' + fren + '!')
    webbrowser.open('https://twitter.com/' + fren)
