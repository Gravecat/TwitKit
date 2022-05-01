# twitter_update_following.py -- Retrieves a list of the people you follow on Twitter, and stores it in the text file twitter_following.txt
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import os
import time
import tweepy

wait_before_exit = True     # Set this to False to no longer wait for the user to press Enter before exiting.

try:
    api_key_file = open(os.path.dirname(__file__) + '\\apikeys.txt', 'r')
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
    print('\nPlease press Enter to quit.')
    input()
    exit()

try:
    auth = tweepy.auth.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    if (api.verify_credentials):
        print('Logged into Twitter API successfully.')
    else:
        print('Could not verify Twitter API credentials.')
        if wait_before_exit:
            print('\nPlease press Enter to quit.')
            input()
        exit()
except:
    print('Could not verify Twitter API credentials.')
    if wait_before_exit:
        print('\nPlease press Enter to quit.')
        input()
    exit()

try:
    list = open(os.path.dirname(__file__) + '/twitter_following.txt', 'w')
except:
    print('Could not open file for writing!')
    if wait_before_exit:
        print('\nPlease press Enter to quit.')
        input()
    exit()

try:
    friends = tweepy.Cursor(api.get_friends, count = 100).items()
    print('Processing friends list...')
except:
    print('Could not retrieve following list fdrom Twitter API.')
    if wait_before_exit:
        print('\nPlease press Enter to quit.')
        input()
    exit()
friend_count = 0

while True:
    try:
        user = next(friends)
        list.write(user.screen_name + '\n')
        friend_count += 1
    except StopIteration:
        break
    except tweepy.TooManyRequests:
        print('Twitter API rate limit reached. Sleeping for 15 minutes...')
        for i in range(0, 15):
            time.sleep(60)
            print('.', end = '')
        print('\n')
        user = next(friends)
        list.write(user.screen_name + '\n')
        friend_count += 1
    except:
        print('Unexpected exception caight!')
        list.close()
        if wait_before_exit:
            print('\nPlease press Enter to quit.')
            input()
        exit()

list.close()
print('Successfully updated following list. Processed', friend_count, 'friends.')
if wait_before_exit:
    print('\nPlease press Enter to quit.')
    input()
