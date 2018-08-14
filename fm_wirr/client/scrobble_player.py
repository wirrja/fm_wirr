#!/usr/bin/python3
from pprint import pprint
import requests
import time
from conn_settings import API, PASSWORD, USER
from gi.repository import Playerctl, GLib


player = Playerctl.Player()
checker = []


class Scrobbler:
    @classmethod
    def run(cls):
        return player.on("metadata", cls._collect_data)

    @classmethod
    def _collect_data(cls, player, data):
        data = dict(data)
        json = {
            "date_listen": int(time.time()),
            "song": {"title": data["xesam:title"], "length": data["mpris:length"]},
            "album": {"title": data["xesam:album"]},
            "artist": {"name": data["xesam:artist"][0]},
        }
        with open("audio.log", "a+") as log:
            log.writelines(str(json) + "\n")
        return cls._post(json)

    @classmethod
    def _post(cls, json):
        return requests.post(API, json=json, auth=(USER, PASSWORD))


Scrobbler.run()
main = GLib.MainLoop()
main.run()
