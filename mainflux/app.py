from .api import Api
from .channel import ChannelRepository
from .transport import TransportFactory, MQTT
from types import SimpleNamespace
import asyncio
import os

# TODO Add logs


class ApplicationException(Exception):
    pass


class URLNotProvidedError(ApplicationException):
    pass


class UserEmailNotProvided(ApplicationException):
    pass


class UserPasswordNotProvided(ApplicationException):
    pass


class Config(SimpleNamespace):
    pass


class MainfluxApp:
    def __init__(self, url: str = None, port: str = "80", transport: str = MQTT, user_email: str = None, user_password: str = None):
        if url is None:
            raise URLNotProvidedError("You should provide url for connection to mainflux")
        mainflux_url = f"http://{url}:{port}"
        user_email = user_email or os.getenv('MAINFLUX_USER')
        if not user_email:
            raise UserEmailNotProvided
        user_password = user_password or os.getenv('MAINFLUX_USER_PASSWORD')
        if not user_password:
            raise UserPasswordNotProvided
        self.config = Config(
            MAINFLUX_IP=url,
            MAINFLUX_PORT=port,
            MAINFLUX_USER_EMAIL=user_email,
            MAINFLUX_USER_PASSWORD=user_password,
            MAINFLUX_URL=mainflux_url,
            TRANSPORT=transport
        )
        self.api = Api(self)
        self.channel_repository = ChannelRepository(self)
        self.transport_factory = TransportFactory(self.config.TRANSPORT)
        self.loop = asyncio.get_event_loop()
        self.tasks = []
        # TODO Add https support

    def run(self):
        wait_tasks = asyncio.wait(self.tasks)
        self.loop.run_until_complete(wait_tasks)

    def add_task(self, task, args=()):
        _task = self.loop.create_task(task(*args))
        self.tasks.append(_task)

    @property
    def ip(self):
        return self.config.MAINFLUX_IP
