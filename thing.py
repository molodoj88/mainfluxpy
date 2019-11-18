from settings import *
import requests
from connector import MqttConnector

LIMIT = 100


class Thing:

    @staticmethod
    def create_thing(token, thing_name):
        url = "{}/things".format(MAINFLUX_URL)
        headers = {"Authorization": token}
        params = {"name": thing_name}
        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 201:
            thing_id = response.headers["Location"].split('/')[-1]
            all_things = Thing.get_all_things(token)
            thing = [t for t in all_things if t['id'] == thing_id][0]
            return ThingsFactory.get_thing(thing["id"], thing["name"], thing["key"], token)

    @staticmethod
    def remove_thing(token, thing_id):
        url = "{}/things/{}".format(MAINFLUX_URL, thing_id)
        headers = {"Authorization": token}
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            ThingsFactory.remove_thing(thing_id)
            return True

    @staticmethod
    def get_all_things(token, offset=0):
        url = "{}/things".format(MAINFLUX_URL)
        headers = {"Authorization": token}
        params = {"limit": LIMIT, "offset": offset}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            response_json = response.json()
            total = response_json['total']
            things = response_json['things']
            if offset < total:
                offset += LIMIT
                things += Thing.get_all_things(token, offset)
            return things

    def __init__(self, thing_id, thing_name, thing_key, user_token):
        self._id = thing_id
        self._name = thing_name
        self._key = thing_key
        self._token = user_token
        self._channels = []
        self._get_connected_channels()
        self.mqtt_connector = MqttConnector(MAINFLUX_IP, self._id, self._key)

    def _get_connected_channels(self, offset=0, limit=100):
        url = "{}/things/{}/channels".format(MAINFLUX_URL, self._id)
        headers = {"Authorization": self._token}
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            self._channels = response.json()["channels"]

    def get_connected_channels(self):
        return self._channels

    def get_name(self):
        return self._name

    def get_key(self):
        return self._key

    def get_id(self):
        return self._id

    def send_message(self, message, channel_id):
        topic = "channels/{}/messages".format(channel_id)
        return self.mqtt_connector.send_message(message, topic)

    def connect_to_channel(self, channel_id):
        url = "{}/channels/{}/things/{}".format(MAINFLUX_URL, channel_id, self._id)
        headers = {"Authorization": self._token}
        response = requests.put(url, headers=headers)
        if response.status_code == 200:
            pass
        else:
            print(response.status_code)


class ThingsFactory:
    things = []

    @classmethod
    def get_thing(cls, *args, **kwargs):
        thing_id, thing_name, thing_key, user_token = args
        thing = cls._get_thing_by_id(thing_id)
        if not thing:
            thing = Thing(thing_id, thing_name, thing_key, user_token)
            cls.things.append(thing)
        return thing

    @classmethod
    def _get_thing_by_id(cls, thing_id):
        thing = None
        for t in cls.things:
            if t.get_id() == thing_id:
                thing = t
        return thing

    @classmethod
    def remove_thing(cls, thing_id):
        thing = cls._get_thing_by_id(thing_id)
        if thing:
            cls.things.remove(thing)
