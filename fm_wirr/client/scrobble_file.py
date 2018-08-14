#!/usr/bin/env python
import os
from pprint import pprint
import requests
import sys

from conn_settings import API, PASSWORD, PORT, SERVER, USER

SCRIPTPATH = os.path.dirname(__file__)
ROCKBOX_FILE_DEFAULT = os.path.join(SCRIPTPATH, ".scrobbler.log")


def parser_scrobbler(rockbox_file=ROCKBOX_FILE_DEFAULT):
    with open(rockbox_file, "r") as f:
        for line in f:
            line = line.replace("\n", "")
            line = line.rsplit("\t")

            yield line


def format_json(data):

    fm_json = {
        "date_listen": data[6],
        "song": {"title": data[2], "length": data[4]},
        "album": {"title": data[1]},
        "artist": {"name": data[0]},
    }
    return fm_json


def send_scrobble_card(fm_json):
    api = requests.post(API, json=fm_json, auth=(USER, PASSWORD))
    pprint(api.json())
    return api


if __name__ == "__main__":
    try:
        rockbox_file = sys.argv[1]
        for line in parser_scrobbler(rockbox_file):
            fm_json = format_json(line)
            send_scrobble_card(fm_json=fm_json)

    except IndexError:
        print("Please give me /path/.scrobbler.log")

    except FileNotFoundError:
        print("=" * 80, "\nFile not found! Please give me correct path to file! ")
