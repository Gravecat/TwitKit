# twitkit_common.py -- Common functions used amongst the TwitKit scripts.
# Copyright (c) 2022 Raine "Gravecat" Simmons. Released under the MIT License.

import os


def txt_to_set(filename):
    try:
        txt_file = open(os.path.dirname(__file__) + '\\' + filename, 'r')
        txt_list = [i.replace('\n', '') for i in txt_file.readlines()]
        txt_file.close()
        return set(txt_list)
    except: return set()
