# tweets_only.py -- Given the name of a Twitter user as a command-line argument, or through an interactive interface if not,
# displays a search page that shows *only* that user's tweets and none of their retweets.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import sys
import webbrowser

def tweets_only(user):
    print('Opening tweets-only search page for', user)
    webbrowser.open('https://twitter.com/search?q=from%3A' + user + '&src=typed_query&f=live')

if len(sys.argv) > 1:
    args = sys.argv
    args.pop(0)
    for arg in args:
        tweets_only(arg)
    exit()

print('Enter the username of a Twitter user to view their tweets only, or a blank line to exit.')
while True:
    user = input()
    if not len(user):
        print('Goodbye!')
        exit()
    tweets_only(user)
