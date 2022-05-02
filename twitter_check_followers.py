# twitter_check_followers.py -- Retrieves a list of the people who follow you on Twitter, and optionally compares to a previous list to check for new followers/unfollowers.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import twitkit_common as tk


def main():
    wait_before_exit = True     # Set this to False to no longer wait for the user to press Enter before exiting.

    api = tk.get_api()
    if (api == None): tk.done(wait_before_exit)

    followers_old = tk.txt_to_set('twitter_followers.txt')
    followers_old_count = len(followers_old)
    if followers_old_count:
        print('Successfully read {} follower{} from twitter_followers.txt'.format(followers_old_count, 's' if followers_old_count != 1 else ''))

    follower_set, follower_count = tk.get_friends(api.get_followers, 'followers')

    try:
        tk.set_to_txt('twitter_followers.txt', follower_set)
        print('Successfully updated followers list. Processed {} follower{}.'.format(follower_count, 's' if follower_count != 1 else ''))
    except:
        print('Could not open file for writing!')
        tk.done(wait_before_exit)

    if not followers_old_count: tk.done(wait_before_exit)

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

    tk.done(wait_before_exit)


if __name__ == '__main__': main()
