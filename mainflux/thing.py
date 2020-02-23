from .channel import PubChannel, SubChannel
from .message import Message
from typing import Callable
import uuid
import json


PUB_CHANNEL_TEMPLATE = "pub_channel_for_{}"
SUB_CHANNEL_TEMPLATE = "sub_channel_for_{}"


class ThingException(Exception):
    pass


class NoSuchThingException(ThingException):
    pass


class Thing:
    """
    Base class implements mainflux thing
    """
    def __init__(self, app, thing_id: str = None, thing_name: str = None):
        self._id = thing_id
        self._app = app
        self._name = thing_name
        self._key = None
        self._channels = []
        self._pub_channel: PubChannel = None
        self._sub_channel: SubChannel = None
        self._init_thing()

    def __str__(self):
        thing_dict = {
            "Thing": {
                "id": self._id,
                "name": self._name,
                "key": self._key,
                "Pub channel": str(self._pub_channel),
                "Sub channel": str(self._sub_channel)
            }
        }
        thing_str = json.dumps(thing_dict, indent=4)
        return thing_str

    def _init_thing(self):
        self._get_thing_params()
        self._get_connected_channels()

    def _get_thing_params(self):
        """
        Gets thing name and key and stores it
        """
        if self._id is None:
            if self._name is None:
                self._name = str(uuid.uuid4())
            self._id = self._app.api.create_thing(self._name)
        params = self._app.api.get_thing(self._id)
        if not params:
            raise NoSuchThingException("There is no such thing in mainflux database")
        self._name = params["name"]
        self._key = params["key"]

    def _get_connected_channels(self):
        """
        Gets connected channels (for publishing and subscribing) and stores it.
        If there are no connected channels, or if their names do not match the template,
        creates new channels and connects them to thing
        """
        channels = self._app.api.get_connected_channels(self._id)
        self._channels = channels
        if channels:
            for channel in channels:
                if PUB_CHANNEL_TEMPLATE.format(self._id) in channel["name"]:
                    if self._pub_channel:
                        continue   # If we already have pub channel for this thing
                    self._pub_channel = self._app.channel_repository.get_pub_channel(self, channel["id"], channel["name"])
                elif SUB_CHANNEL_TEMPLATE.format(self._id) in channel["name"]:
                    if self._sub_channel:
                        continue   # If we already have sub channel for this thing
                    self._sub_channel = self._app.channel_repository.get_sub_channel(self, channel["id"], channel["name"])
                else:
                    self._create_channels()
        else:
            self._create_channels()

    def _create_channels(self):
        """
        Creates and assigns sub and pub channel for thing
        :return:
        """
        pub_channel_name = PUB_CHANNEL_TEMPLATE.format(self._id)
        sub_channel_name = SUB_CHANNEL_TEMPLATE.format(self._id)
        # Create pub channel first and connect it
        pub_channel_id = self._app.api.create_channel(pub_channel_name)
        self.connect_to_channel(pub_channel_id)
        # Create sub channel and connect it
        sub_channel_id = self._app.api.create_channel(sub_channel_name)
        self.connect_to_channel(sub_channel_id)
        self._pub_channel = self._app.channel_repository.get_pub_channel(self, pub_channel_id, pub_channel_name)
        self._sub_channel = self._app.channel_repository.get_sub_channel(self, sub_channel_id, sub_channel_name)

    def connect_to_channel(self, channel_id):
        self._app.api.connect_thing_to_channel(self._id, channel_id)

    @property
    def connected_channels(self):
        return self._channels

    @property
    def name(self):
        return self._name

    @property
    def thing_id(self):
        return self._id

    @property
    def key(self):
        return self._key

    def send_message(self, message: Message):
        """
        Sends message over pub channel
        :param message: message instance
        :return:
        """
        self._app.add_task(self._pub_channel.send_message, (message,))

    def start_publishing(self):
        """
        Starts publishing process (waits messages from assigned signal handler)
        :return:
        """
        self._app.add_task(self._pub_channel.start_publishing)

    @staticmethod
    def _message_received_callback(message):
        packet = message.publish_packet
        print("%s => %s" % (packet.variable_header.topic_name, str(packet.payload.data)))

    def subscribe(self, message_received_callback: Callable = None):
        """
        Subscribes to connected channel and assigns callback
        for delivered messages
        :param message_received_callback: callable, callback for received messages. First argument should be a message.
                                          Message is an instance of hbmqtt.session.ApplicationMessage class
        :return:
        """
        if message_received_callback is not None:
            self._message_received_callback = message_received_callback
        self._app.add_task(self._sub_channel.subscribe, (self._message_received_callback,))


class ThingsRepository:
    __things = {}

    def __init__(self, app):
        self._app = app

    def get_thing(self, thing_id=None, thing_name=None):
        """
        If no thing found in self.__things, creates new thing
        :param thing_id: thing_id
        :param thing_name: thing_name
        :return:
        """
        if thing_id is None:
            if thing_name is None:
                # If thing_id and thing_name is not provided
                thing = Thing(self._app)
                self.__things[thing.thing_id] = thing
                return thing
            else:
                # If no thing_id, but thing_name provided
                thing = None
                for thing_id, _thing in self.__things.items():
                    if _thing.name == thing_name:
                        return _thing
                if thing is None:
                    thing = Thing(self._app, thing_name=thing_name)
                    self.__things[thing.thing_id] = thing
                    return thing
        else:
            # If thing_id is provided, ignore thing_name
            if not isinstance(thing_id, str):
                raise ThingException("Thing id should be an str.")
            if thing_id not in self.__things.keys():
                thing = Thing(self._app, thing_id)
                self.__things[thing_id] = thing
                return thing
            else:
                return self.__things[thing_id]
