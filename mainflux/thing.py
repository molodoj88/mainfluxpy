from .app import MainfluxApp
from .channel import Channel


class ThingException(Exception):
    pass


class NoSuchThingException(ThingException):
    pass


class Thing:
    """
    Base class implements mainflux thing
    """
    def __init__(self, thing_id: str, app: MainfluxApp):
        self._id = thing_id
        self._app = app
        self._name = None
        self._key = None
        self._channels = []
        self._init_thing()

    def _init_thing(self):
        self._get_thing_params()
        self._get_connected_channels()

    def _get_thing_params(self):
        """
        Gets thing name and key and stores it
        """
        params = self._app.api.get_thing(self._id)
        if not params:
            raise NoSuchThingException("There is no such thing in mainflux database")
        self._name = params["name"]
        self._key = params["key"]

    def _get_connected_channels(self):
        channels = self._app.api.get_connected_channels(self._id)
        self._channels.extend([self._app.channel_repository.get_channel(ch["id"], ch["name"]) for ch in channels])

    @property
    def connected_channels(self):
        return self._channels

    @property
    def name(self):
        return self._name

    def send_message(self, message, channel_id):
        pass

    def connect_to_channel(self, channel_id):
        pass
