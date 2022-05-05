# twitter_check_followers.py -- Retrieves a list of the people who follow you on Twitter, and compares to a previous list to check for new followers/unfollowers.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import twitkit_common as tk


def main():
    wait_before_exit = True     # Set this to False to no longer wait for the user to press Enter before exiting.

    api = tk.get_api()
    if (api == None): tk.done(wait_before_exit)
    tk.compare_friends(api.get_followers, 'twitter_followers.txt', 'follower', wait_before_exit)
    tk.done(wait_before_exit)


if __name__ == '__main__': main()
