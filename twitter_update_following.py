# twitter_update_following.py -- Retrieves a list of the people you follow on Twitter, and stores it in the text file twitter_following.txt
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import twitkit_common as tk

def main():
    wait_before_exit = True     # Set this to False to no longer wait for the user to press Enter before exiting.

    api = tk.get_api()
    if (api == None): tk.done(wait_before_exit)

    following_set, following_count = tk.get_friends(api.get_friends, 'friends')
    try:
        tk.set_to_txt('twitter_following.txt', following_set)
        print('Successfully updated following list. Processed {} friend{}.'.format(following_count, 's' if following_count != 1 else ''))
    except:
        print('Could not open file for writing!')
    
    tk.done(wait_before_exit)

if __name__ == '__main__': main()
