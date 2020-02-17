

class ChannelException(Exception):
    pass


class NoSuchChannelException(ChannelException):
    pass


class Channel:
    def __init__(self, app, channel_id: str, channel_name: str = None):
        self._app = app
        self._id = channel_id
        self._name = channel_name

    @property
    def name(self):
        if self._name is None:
            channel = self._app.api.get_channel(self._id)
            if not channel:
                raise NoSuchChannelException("There is no such channel in mainflux database")
            else:
                self._name = channel["name"]
                return self._name


class ChannelRepository:
    __channels = {}

    def __init__(self, app):
        self._app = app
        self.__dict__ = self.__channels

    def get_channel(self, channel_id, channel_name=None):
        if channel_id not in self.__dict__.keys():
            channel = Channel(self._app, channel_id, channel_name)
            self.__dict__[channel_id] = channel
            return channel
        else:
            return self.__dict__[channel_id]
