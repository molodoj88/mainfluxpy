from settings import *
import requests


class Channel:
    def __init__(self, channel_id, channel_name, user_token):
        self._id = channel_id
        self._name = channel_name
        self._token = user_token
        self._things = []
        self._get_things()

    def _get_things(self, offset=0, limit=100):
        url = "{}/channels/{}/things".format(MAINFLUX_URL, self._id)
        headers = {"Authorization": self._token}
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            self._things.extend(response.json()["things"])

    def get_things(self):
        return self._things

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id
