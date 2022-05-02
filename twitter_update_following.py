# twitter_update_following.py -- Retrieves a list of the people you follow on Twitter, and stores it in the text file twitter_following.txt
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import twitkit_common

def main():
    wait_before_exit = True     # Set this to False to no longer wait for the user to press Enter before exiting.

    api = twitkit_common.get_api()
    if (api == None): twitkit_common.done(wait_before_exit)

    following_set, following_count = twitkit_common.get_friends(api.get_friends, 'friends')
    try:
        twitkit_common.set_to_txt('twitter_following.txt', following_set)
        print('Successfully updated following list. Processed {} friend{}.'.format(following_count, 's' if following_count != 1 else ''))
    except:
        print('Could not open file for writing!')
    
    twitkit_common.done(wait_before_exit)

if __name__ == '__main__': main()
