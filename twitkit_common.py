# twitkit_common.py -- Common functions used amongst the TwitKit scripts.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import os
import time
import tweepy


# Loads either the following or followers list from Twitter, and compares the two.
# This is the bulk of the code for twitter_check_following.py and twitter_check_followers.py, but because the code is near-identical,
# I'm making it generic here to save writing the almost exact same code twice.
def compare_friends(api_call, file, friend_type, wait_before_exit):
    friends_old = txt_to_set(file)
    friends_old_count = len(friends_old)
    if friends_old_count:
        print('Successfully read {} {}{} from {}'.format(
            friends_old_count,
            friend_type,
            's' if friends_old_count != 1 else '',
            file))
    
    friend_set, friend_count = get_friends(api_call, friend_type)

    try:
        set_to_txt(file, friend_set)
        print('Successfully updated {} list. Processed {} {}{}.'.format(
            friend_type,
            friend_count,
            friend_type,
            's' if friend_count != 1 else ''))
    except:
        print('Could not open file for writing!')
        done(wait_before_exit)

    if not friends_old_count: return

    new_friends = friend_set - friends_old
    lost_friends = friends_old - friend_set
    new_friend_count = len(new_friends)
    lost_friend_count = len(lost_friends)

    if new_friend_count:
        print('\n{} {} new {}{}: {}'.format(
            'Gained' if friend_type == 'follower' else 'Added',
            new_friend_count,
            friend_type,
            's' if new_friend_count != 1 else '',
            ', '.join(new_friends)))
    
    if lost_friend_count:
        print('\n{} {} {}{}: {}'.format(
            'Lost' if friend_type == 'follower' else 'Removed',
            lost_friend_count,
            friend_type,
            's' if lost_friend_count != 1 else '',
            ', '.join(lost_friends)))

    if not new_friend_count and not lost_friend_count:
        if friend_type == 'follower': print('\nNo followers gained or lost since last check.')
        else: print('\nNo friends added or removed since last check.')


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
def txt_to_list(filename):
    try:
        txt_file = open(os.path.dirname(__file__) + '/' + filename, 'r')
        txt_list = [i.replace('\n', '') for i in txt_file.readlines()]
        txt_file.close()
        return txt_list
    except: return []

# Loads a text file, and converts it to a set of individual lines without trailing newlines.
def txt_to_set(filename):
    return set(txt_to_list(filename))


if __name__ == '__main__': print('This script contains only library functions and should not be executed directly.')
