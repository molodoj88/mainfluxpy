from settings import *
import requests


class Thing:
    def __init__(self, thing_id, thing_name, thing_key, user_token):
        self._id = thing_id
        self._name = thing_name
        self._key = thing_key
        self._token = user_token
        self._channels = []
        self._get_connected_channels()

    def _get_connected_channels(self, offset=0, limit=100):
        url = "{}/things/{}/channels".format(MAINFLUX_URL, self._id)
        headers = {"Authorization": self._token}
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            self._channels.extend(response.json()["channels"])

    def get_connected_channels(self):
        return self._channels

    def get_name(self):
        return self._name

    def get_key(self):
        return self._key


    #TODO make method for sending messages via mqtt

    #TODO make __str__() method
