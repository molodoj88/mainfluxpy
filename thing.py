from settings import *
import requests
import paho.mqtt.client as mqtt


class Thing:
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
            self._channels.extend(response.json()["channels"])

    def get_connected_channels(self):
        return self._channels

    def get_name(self):
        return self._name

    def get_key(self):
        return self._key

    def get_id(self):
        return self._id

    def set_up_mqtt_client(self):
        print("Setting up mqtt client for thing {}".format(self._name))
        def on_connect(client, userdata, flags, rc):
            print("Connected to mainflux mqtt broker with result code " + str(rc))
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.username_pw_set(self._id, self._key)
        try:
            self.mqtt_client.connect(MAINFLUX_IP)
        except Exception as e:
            print("Error:\n{}".format(e))

    def send_message(self, message, channel_id):
        topic = "channels/{}/messages".format(channel_id)
        self.mqtt_client.publish(topic, message)

    @classmethod
    def create_mainflux_thing(cls, token, thing_name):
        url = "{}/things".format(MAINFLUX_URL)
        headers = {"Authorization": token}
        params = {"name": thing_name}
        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 201:
            return response.headers["Location"].split('/')[-1]

    @classmethod
    def remove_mainflux_thing(cls, token, thing_id):
        url = "{}/things/{}".format(MAINFLUX_URL, thing_id)
        headers = {"Authorization": token}
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return True
