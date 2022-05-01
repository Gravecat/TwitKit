# twitter_check_followers.py -- Retrieves a list of the people who follow you on Twitter, and optionally compares to a previous list to check for new followers/unfollowers.
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
    followers_old_file = open(os.path.dirname(__file__) + '\\twitter_followers_old.txt', 'r')
    followers_old = followers_old_file.readlines()
    followers_old = set([i.replace('\n', '') for i in followers_old])
    followers_old_file.close()
except:
    if wait_before_exit:
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
    os.rename(os.path.dirname(__file__) + '/twitter_followers.txt', os.path.dirname(__file__) + '/twitter_followers_old.txt')
except: pass

try:
    list = open(os.path.dirname(__file__) + '/twitter_followers.txt', 'w')
except:
    print('Could not open file for writing!')
    if wait_before_exit:
        print('\nPlease press Enter to quit.')
        input()
    exit()

try:
    followers = tweepy.Cursor(api.get_followers, count = 100).items()
    print('Processing followers list...')
except:
    print('Could not retrieve followers list fdrom Twitter API.')
    if wait_before_exit:
        print('\nPlease press Enter to quit.')
        input()
    exit()
follower_count = 0

while True:
    try:
        user = next(followers)
        list.write(user.screen_name + '\n')
        follower_count += 1
    except StopIteration:
        break
    except tweepy.TooManyRequests:
        print('Twitter API rate limit reached. Sleeping for 15 minutes...')
        time.sleep(900)
        user = next(user)
        list.write(user.screen_name + '\n')
        follower_count += 1
    except:
        print('Unexpected exception caight!')
        list.close()
        if wait_before_exit:
            print('\nPlease press Enter to quit.')
            input()
        exit()

list.close()
print('Successfully updated following list. Processed', follower_count, 'followers.')

followers_current_file = open(os.path.dirname(__file__) + '\\twitter_followers.txt', 'r')
followers_current = followers_current_file.readlines()
followers_current = set([i.replace('\n', '') for i in followers_current])
followers_current_file.close()

new_followers = followers_current - followers_old
lost_followers = followers_old - followers_current
new_follower_count = len(new_followers)
lost_follower_count = len(lost_followers)

if new_follower_count:
    gained_str = '\nGained ' + str(new_follower_count) + ' new follower'
    if (new_follower_count > 1): gained_str += 's: '
    else: gained_str += ': '
    print (gained_str + (', '.join(new_followers)))

if lost_follower_count:
    lost_str = '\nLost ' + str(lost_follower_count) + ' follower'
    if (lost_follower_count > 1): lost_str += 's: '
    else: lost_str += ': '
    print(lost_str + (', '.join(lost_followers)))

if not new_follower_count and not lost_follower_count:
    print('\nNo followers gained or lost since last check.')

if wait_before_exit:
    print('\nPlease press Enter to quit.')
    input()
