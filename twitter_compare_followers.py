# twitter_compare_followers.py -- Takes the text-file outputs from twitter_check_followers.py and twitter_update_following.py and
# compares the two to list one-way follows.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import twitkit_common


def main():
    wait_before_exit = True # Set this to False to no longer wait for the user to press Enter before exiting.

    following = twitkit_common.txt_to_set('twitter_following.txt')
    if not len(following):
        print('Could not read from twitter_following.txt, or file is empty. Please run twitter_update_following.py first.')
        twitkit_common.done(wait_before_exit)
    followers = twitkit_common.txt_to_set('twitter_followers.txt')
    if not len(following):
        print('Could not read from twitter_followers.txt, or file is empty. Please run twitter_check_followers.py first.')
        twitkit_common.done(wait_before_exit)

    not_following_me_back = following - followers
    im_not_following = followers - following

    if not len(not_following_me_back) and not len(im_not_following):
        if not len(following): print('You are not following anyone.')
        else: print('All of your follows are mutual.')

    else:
        if (not_following_me_back): print('Not following you back:', ', '.join(not_following_me_back))
        if (im_not_following): print("You're not following: ", ', '.join(im_not_following))

    twitkit_common.done(wait_before_exit)


if __name__ == '__main__': main()
