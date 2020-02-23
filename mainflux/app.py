from .api import Api
from .channel import ChannelRepository
from .transport import TransportFactory, MQTT
from .thing import ThingsRepository
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
        self.things_repository = ThingsRepository(self)
        self.loop = asyncio.get_event_loop()
        self.tasks = []
        # TODO Add https support

    def run(self):
        """
        Runs the app
        :return:
        """
        self.loop.run_until_complete(asyncio.gather(*self.tasks))

    def add_task(self, task, args=()):
        _task = self.loop.create_task(task(*args))
        self.tasks.append(_task)

    @property
    def ip(self):
        return self.config.MAINFLUX_IP

    async def run_with_delay(self, coro, args, delay: float = 0):
        """
        Run some coroutine with given delay
        :param coro: coroutine to run
        :param args: arguments tuple to pass into coroutine
        :param delay: delay in seconds
        :return:
        """
        await asyncio.sleep(delay)
        await coro(*args)

    def add_signal_handler(self, handler, thing_id):
        """
        Adds signal handler for thing.
        :param handler: a coroutine function whose first argument is thing object. Second argument should be loop.
        See example in pub_example.py
        :param thing_id: id of thing that will send a message on signal
        :return:
        """
        thing = self.things_repository.get_thing(thing_id)
        self.add_task(self.run_with_delay, (handler, (thing, self.loop), 1))
