# twitter_check_followers.py -- Retrieves a list of the people who follow you on Twitter, and optionally compares to a previous list to check for new followers/unfollowers.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import os
import twitkit_common


def main():
    wait_before_exit = True     # Set this to False to no longer wait for the user to press Enter before exiting.

    api = twitkit_common.get_api()
    if (api == None): twitkit_common.done(wait_before_exit)

    followers_old = twitkit_common.txt_to_set('twitter_followers.txt')
    followers_old_count = len(followers_old)
    if followers_old_count:
        print('Successfully read {} follower{} from twitter_followers.txt'.format(followers_old_count, 's' if followers_old_count != 1 else ''))

    follower_set, follower_count = twitkit_common.get_friends(api.get_followers, 'followers')

    try:
        list_file = open(os.path.dirname(__file__) + '/twitter_followers.txt', 'w')
        for follower in follower_set:
            list_file.write(follower + '\n')
        list_file.close()
        print('Successfully updated following list. Processed {} follower{}.'.format(follower_count, 's' if follower_count != 1 else ''))
    except:
        print('Could not open file for writing!')
        twitkit_common.done(wait_before_exit)

    if not followers_old_count: twitkit_common.done(wait_before_exit)

    new_followers = follower_set - followers_old
    lost_followers = followers_old - follower_set
    new_follower_count = len(new_followers)
    lost_follower_count = len(lost_followers)

    if new_follower_count:
        print('\nGained {} new follower{}: {}'.format(
            new_follower_count,
            's' if new_follower_count != 1 else '',
            ', '.join(new_followers)))

    if lost_follower_count:
        print('\nLost {} follower{}: {}'.format(
            lost_follower_count,
            's' if lost_follower_count != 1 else '',
            ', '.join(lost_followers)))

    if not new_follower_count and not lost_follower_count:
        print('\nNo followers gained or lost since last check.')

    twitkit_common.done(wait_before_exit)


if __name__ == '__main__': main()
