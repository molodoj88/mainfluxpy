from .api import Api
from .channel import ChannelRepository
from types import SimpleNamespace
from . import settings
import os

# TODO Add logs


class Config(SimpleNamespace):
    MAINFLUX_IP: str = settings.MAINFLUX_IP
    MAINFLUX_PORT: str = settings.MAINFLUX_PORT
    DB_READER_IP: str = MAINFLUX_IP
    DB_READER_PORT: str = settings.DB_READER_PORT
    MAINFLUX_USER_EMAIL: str = os.getenv('MAINFLUX_USER')
    MAINFLUX_USER_PASSWORD: str = os.getenv('MAINFLUX_USER_PASSWORD')
    MAINFLUX_URL: str = f"http://{MAINFLUX_IP}:{MAINFLUX_PORT}"
    DB_READER_URL: str = f"http://{DB_READER_IP}:{DB_READER_IP}"


class MainfluxApp:
    def __init__(self, config: Config = Config()):
        self.config = config
        self.api = Api(self)
        self.api.token = self.api.get_token()
        self.channel_repository = ChannelRepository(self)
        # TODO Add https support
