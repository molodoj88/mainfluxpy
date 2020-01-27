from settings import *
import requests


class Channel:
    channels = []

    @staticmethod
    def create_channel(token, channel_name):
        url = "{}/channels".format(MAINFLUX_URL)
        headers = {"Authorization": token}
        params = {"name": channel_name}
        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 201:
            return response.headers["Location"].split('/')[-1]

    @staticmethod
    def remove_channel(token, channel_id):
        url = "{}/channels/{}".format(MAINFLUX_URL, channel_id)
        headers = {"Authorization": token}
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            channel = Channel.get_channel_by_id(channel_id)
            if channel:
                Channel.channels.remove(channel)
            return True

    @staticmethod
    def get_channel_by_id(channel_id):
        channel = None
        for c in Channel.channels:
            if c.get_id() == channel_id:
                channel = c
        return channel

    def __init__(self, channel_id, channel_name, user_token):
        self._id = channel_id
        self._name = channel_name
        self._token = user_token
        self._things = []
        self._get_things()
        Channel.channels.append(self)

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


