# tm_visit_friend.py -- Reads the tm_combined_following.txt file (generated by tm_update_list.py)
# and visits the Twitter or Mastodon page for the first friend on the list. It then rewrites the
# list file, moving that friend to the bottom of the list.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import os
import twitkit_common as tk
import webbrowser


def main():
    tweets_only = False # Set this to True to default to only seeing the friend's tweets, not their retweets.
    use_home = True     # If this is set to True and you enter your Mastodon home instance's URL in masto_home.txt (e.g. 'meow.social'), Mastodon friend pages will be displayed on your home server's view.
    friends = tk.txt_to_list('tm_combined_following.txt')
    if (use_home):
        if (os.path.isfile(os.path.dirname(__file__) + '/masto_home.txt')):
            masto_home_file = open(os.path.dirname(__file__) + '/masto_home.txt')
            masto_home = masto_home_file.readline().strip()
            if (not len(masto_home)): use_home = False
            masto_home_file.close()
        else:
            use_home = False
    
    # A list of Mastodon servers that don't use @ in their URL for usernames.
    masto_no_at = ['fedi.neon.moe']
    
    print('Press Enter to visit the next friend on your list, Q (then enter) to exit, or T to toggle tweets-only (no retweets) mode (Twitter only, has no effect on Mastodon friends).')
    print('Tweets-only mode is currently', 'enabled.' if tweets_only else 'disabled.')
    print('Mastodon home mode is currently', 'enabled.' if use_home else 'disabled.')
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
                print('Press Enter to visit the next friend on your list, Q (then enter) to exit, or T to toggle tweets-only (no retweets) mode (Twitter only, has no effect on Mastodon friends).')
        else:
            fren = friends[0]
            print('Visiting ' + fren + '!')
            if ('@' in fren):
                split = fren.split('@')
                if (use_home):
                    masto_url = 'https://' + masto_home + '/@'
                    if (split[1] == masto_home): masto_url += split[0]
                    else: masto_url += fren
                    webbrowser.open(masto_url)
                else:
                    masto_url = 'https://' + split[1]
                    if (split[1] in masto_no_at): masto_url += '/'
                    else: masto_url += '/@'
                    masto_url += split[0]
                    webbrowser.open(masto_url)
            else:
                if tweets_only: webbrowser.open('https://twitter.com/search?q=from%3A' + fren + '&src=typed_query&f=live')
                else: webbrowser.open('https://twitter.com/' + fren)
            friends.append(friends.pop(0))
            tk.set_to_txt('tm_combined_following.txt', friends)

if __name__ == '__main__': main()