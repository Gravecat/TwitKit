# twitkit_common.py -- Common functions used amongst the TwitKit scripts.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import os
import time
import tweepy


# Finishes execution, but optionally waits for the user to press Enter first.
def done(wait_before_exit):
    if wait_before_exit:
        print('\nPlease press Enter to quit.')
        input()
    exit()

# Loads the user's Twitter API keys from apikeys.txt, and returns an API handle
def get_api():
    try:
        api_key_file = open(os.path.dirname(__file__) + '/apikeys.txt', 'r')
        key_lines = api_key_file.readlines()
        api_key_file.close()
        api_key = key_lines[0].strip('\n')
        api_secret = key_lines[1].strip('\n')
        access_token = key_lines[2].strip('\n')
        access_secret = key_lines[3].strip('\n')
    except OSError:
        print('Could not open apikeys.txt!')
        print('To use this script, create a file called apikeys.txt in the same folder, with four lines of plain text. These should be, in order:')
        print('Your Twitter API key (consumer key)')
        print('Your Twitter API key secret (consumer key secret)')
        print('Your Twitter access token')
        print('Your Twitter access token secret')
        print('Do not ever share these keys or tokens with anyone!')
        return None

    auth = tweepy.auth.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    if (api.verify_credentials):
        print('Logged into Twitter API successfully.')
    else:
        print('Could not verify Twitter API credentials.')
        return None
    return api

# Retrieves either the user's following or followers, as a set.
def get_friends(api_call, type_str):
    print('Processing', type_str, 'list...')
    friends = tweepy.Cursor(api_call, count = 100).items()

    friend_count = 0
    friend_set = set()
    while True:
        try:
            friend = next(friends)
            friend_set.add(friend.screen_name)
            friend_count += 1
        except StopIteration:
            return friend_set, friend_count
        except tweepy.TooManyRequests:
            print('Twitter API rate limit reached. Sleeping for 15 minutes...')
            for i in range(0, 15):
                time.sleep(60)
                print('.', end = '')
            print('\n')
            friend = next(friends)
            friend_set.add(friend.screen_name)
            friend_count += 1

# Saves a set to a text file, with trailing newlines.
def set_to_txt(filename, set_data):
    list_file = open(os.path.dirname(__file__) + '/' + filename, 'w')
    for d in set_data:
        list_file.write(d + '\n')
    list_file.close()

# Loads a text file, and converts it to a set of individual lines without trailing newlines.
def txt_to_set(filename):
    try:
        txt_file = open(os.path.dirname(__file__) + '/' + filename, 'r')
        txt_list = [i.replace('\n', '') for i in txt_file.readlines()]
        txt_file.close()
        return set(txt_list)
    except: return set()


if __name__ == '__main__': print('This script contains only library functions and should not be executed directly.')
