# twitter_update_followers.py -- Retrieves a list of the people you follow on Twitter, and stores it in the text file twitter_following.txt
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import os
import time
import tweepy

api_key = ''        # Put your Twitter API key here.
api_secret = ''     # Put your Twitter API secret key here.
access_token = ''   # Put your Twitter access token here.
access_secret = ''  # Put your Twitter access secret token here.
wait_before_exit = False    # Set this to True to wait for the user to press enter before exiting the script.

try:
    auth = tweepy.auth.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    if (api.verify_credentials):
        print('Logged into Twitter API successfully.')
    else:
        print('Could not verify Twitter API credentials.')
        if wait_before_exit: input()
        exit()
except:
    print('Could not verify Twitter API credentials.')
    if wait_before_exit: input()
    exit()

try:
    list = open(os.path.dirname(__file__) + '/twitter_following.txt', 'w')
except:
    print('Could not open file for writing!')
    if wait_before_exit: input()
    exit()

try:
    friends = tweepy.Cursor(api.get_friends, count = 100).items()
    print('Processing friends list...')
except:
    print('Could not retrieve following list fdrom Twitter API.')
    if wait_before_exit: input()
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
        print('Twitter API timeout. Sleeping for 15 minutes...')
        time.sleep(900)
        user = next(user)
        list.write(user.screen_name + '\n')
        friend_count += 1
    except:
        print('Unexpected exception caight!')
        list.close()
        if wait_before_exit: input()
        exit()

list.close()
print('Successfully updated following list. Processed', friend_count, 'friends.')
if wait_before_exit: input()
