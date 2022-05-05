# twitter_check_both.py -- The same functionality as running both twitter_check_following.py and twitter_check_followers.py, in a single script.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import twitkit_common as tk


def main():
    wait_before_exit = True     # Set this to False to no longer wait for the user to press Enter before exiting.

    api = tk.get_api()
    if (api == None): tk.done(wait_before_exit)
    tk.compare_friends(api.get_followers, 'twitter_followers.txt', 'follower', wait_before_exit)
    print('\n')
    tk.compare_friends(api.get_friends, 'twitter_following.txt', 'friend', wait_before_exit)
    tk.done(wait_before_exit)


if __name__ == '__main__': main()
