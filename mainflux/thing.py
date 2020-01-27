from . import settings
from .connector import MqttConnector

LIMIT = 100


class Thing:

    @staticmethod
    def create_thing(token, thing_name):
        pass

    @staticmethod
    def remove_thing(token, thing_id):
        pass

    @staticmethod
    def get_all_things(token, offset=0):
        pass

    def __init__(self, thing_id, thing_name, thing_key, user_token):
        self._id = thing_id
        self._name = thing_name
        self._key = thing_key
        self._token = user_token
        self._channels = []
        self._get_connected_channels()
        self.mqtt_connector = MqttConnector(settings.MAINFLUX_IP, self._id, self._key)

    def _get_connected_channels(self, offset=0, limit=100):
        pass

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
        msg = self.mqtt_connector.send_message(message, topic)
        return msg

    def connect_to_channel(self, channel_id):
        pass


class ThingsFactory:
    things = {}

    @classmethod
    def get_thing(cls, *args, **kwargs):
        pass

    @classmethod
    def create_thing(cls):
        pass

    @classmethod
    def remove_thing(cls, thing_id):
        pass
