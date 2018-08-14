#!/usr/bin/env python3
from collections import deque
from multiprocessing import Process, Manager
import os
import requests
from time import time, sleep
from mpd import MPDClient
from conn_settings import API, PASSWORD, USER, MPD_SERVER, MPD_SERVER_PORT


client = MPDClient()  # create client object
client.timeout = None  # network timeout in seconds (floats allowed), default: None
client.idletimeout = None  # timeout for fetching the result of the idle command

# is handled seperately, default: None
client.connect(MPD_SERVER, MPD_SERVER_PORT)

# client.command_list_ok_begin()
# client.update()  # insert the update command into the list
# client.status()  # insert the status command into the list
# results = client.command_list_end()


def get_status():
    return client.currentsong(), client.status()


def store_data(data: tuple, store: list):
    try:
        artist = data[0].pop("artist")
        album = data[0].pop("album")
        song = data[0].pop("title")
        time = data[1].pop("time")
        state = data[1].pop("state")
        elapse, duration = (int(x) for x in time.split(":"))
        li = ((artist, album, song), elapse, duration)
    except KeyError:
        state = "turnedoff"

    if state == "play":
        store.append(li)
        if len(store) > 2:
            print(store[0])
            print(store[1])
            print(store[2])

            a = store.remove(store[1])
            # print(store[0][0][2], store[0])
            # print(store_)
            # store.remove(store[1:3])
            # store.remove(store[1])
            # store.remove(store[2])
            # store.remove(store[3])

            print(store)
            print("-" * 10)
        # else:
        #     print(store, len(store))

    elif state == "pause":
        print("player on pause")
    elif state == "turnedoff":
        print("Player turned off")
        sleep(5)
    else:
        print("looks like player stop")
    # return store


if __name__ == "__main__":
    with Manager() as manager:
        store = manager.list()
        while True:
            p = Process(target=store_data, args=(get_status(), store))
            p.start()
            p.join()

            sleep(1)
