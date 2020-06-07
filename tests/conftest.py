from mainflux.app import MainfluxApp
import pytest
import uuid
import httpx
from .common import THINGS_TO_DELETE, CHANNELS_TO_DELETE

APP_KWARGS = {
    'url': "your_ip_to_mainflux",
    'port': "80",
    'user': "your_user_email",
    'password': "your_password"
}


class TestManager:
    def __init__(self, **app_args):
        self.app = MainfluxApp(url=app_args['url'],
                               port=app_args['port'],
                               user_email=app_args['user'],
                               user_password=app_args['password'])

    def __new__(cls, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TestManager, cls).__new__(cls)
        return cls.instance


@pytest.fixture(scope='module')
def app():
    test_manager = TestManager(**APP_KWARGS)
    app = test_manager.app
    return app


@pytest.fixture(scope='module')
def http_client():
    client = httpx.Client()
    yield client
    client.close()


@pytest.fixture
def random_thing_name():
    def make_random_name():
        return str(uuid.uuid4())
    return make_random_name


@pytest.fixture(scope='module')
def clean_things():
    yield
    app = TestManager(**APP_KWARGS).app
    for thing in THINGS_TO_DELETE:
        app.api.delete_thing(thing)


@pytest.fixture(scope='module')
def clean_channels():
    yield
    app = TestManager(**APP_KWARGS).app
    for channel in CHANNELS_TO_DELETE:
        app.api.delete_thing(channel)
