from settings import *
import requests
import paho.mqtt.client as mqtt


class Thing:

    @staticmethod
    def create_thing(token, thing_name):
        url = "{}/things".format(MAINFLUX_URL)
        headers = {"Authorization": token}
        params = {"name": thing_name}
        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 201:
            return response.headers["Location"].split('/')[-1]

    @staticmethod
    def remove_thing(token, thing_id):
        url = "{}/things/{}".format(MAINFLUX_URL, thing_id)
        headers = {"Authorization": token}
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            ThingsFactory.remove_thing(thing_id)
            return True

    def __init__(self, thing_id, thing_name, thing_key, user_token):
        self._id = thing_id
        self._name = thing_name
        self._key = thing_key
        self._token = user_token
        self._channels = []
        self._get_connected_channels()
        self.mqtt_client = mqtt.Client()
        self.set_up_mqtt_client()

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

    def set_up_mqtt_client(self):
        def on_connect(client, userdata, flags, rc):
            print("Connected to mainflux mqtt broker with result code " + str(rc))
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.username_pw_set(self._id, self._key)
        try:
            self.mqtt_client.connect(MAINFLUX_IP)
        except Exception as e:
            print("Error while setting up mqtt client for thing {}:\n{}".format(self._id, e))

    def send_message(self, message, channel_id):
        topic = "channels/{}/messages".format(channel_id)
        return self.mqtt_client.publish(topic, message)

    def connect_to_channel(self, channel_id):
        url = "{}/channels/{}/things/{}".format(MAINFLUX_URL, channel_id, self._id)
        headers = {"Authorization": self._token}
        response = requests.put(url, headers=headers)
        print(response)
        if response.status_code == 200:
            self._get_connected_channels()
            return True


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
