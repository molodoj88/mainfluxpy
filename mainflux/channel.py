from .transport import AbstractTransport
from typing import Callable


class ChannelException(Exception):
    pass


class NoSuchChannelException(ChannelException):
    pass


class Channel:
    def __init__(self, app, thing, channel_id: str, channel_name: str = None):
        self._app = app
        self._id = channel_id
        self._name = channel_name
        self._thing = thing
        self._transport: AbstractTransport = app.transport_factory.create_transport(self)
        self._connect()

    def __str__(self):
        return f"Channel object:\nid: {self._id}\nname: {self._name}\ntransport: {self._app.config.TRANSPORT}"

    def _connect(self):
        self._app.add_task(self._transport.connect)

    @property
    def name(self):
        if self._name is None:
            channel = self._app.api.get_channel(self._id)
            if not channel:
                raise NoSuchChannelException("There is no such channel in mainflux database")
            else:
                self._name = channel["name"]
                return self._name

    @property
    def app(self):
        return self._app

    @property
    def thing(self):
        return self._thing


class PubChannel(Channel):
    def __init__(self, app, thing, channel_id: str, channel_name: str):
        super().__init__(app, thing, channel_id, channel_name)
        self.topic = f"channels/{self._id}/messages/"

    async def send_message(self, message):
        await self._transport.send_message(message, self.topic)


class SubChannel(Channel):
    def __init__(self, app, thing, channel_id: str, channel_name: str):
        super().__init__(app, thing, channel_id, channel_name)
        self.topic = f"channels/{self._id}/messages/#"

    async def subscribe(self, message_received_cb: Callable = None):
        await self._transport.subscribe(self.topic, message_received_cb)


class ChannelRepository:
    __channels = {}

    def __init__(self, app):
        self._app = app

    def get_pub_channel(self, thing, channel_id, channel_name=None):
        if channel_id not in self.__channels.keys():
            channel = PubChannel(self._app, thing, channel_id, channel_name)
            self.__channels[channel_id] = channel
            return channel
        else:
            return self.__channels[channel_id]

    def get_sub_channel(self, thing, channel_id, channel_name=None):
        if channel_id not in self.__channels.keys():
            channel = SubChannel(self._app, thing, channel_id, channel_name)
            self.__channels[channel_id] = channel
            return channel
        else:
            return self.__channels[channel_id]
